import os
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from vosk import Model, KaldiRecognizer

APP_DIR = Path(__file__).resolve().parent
MODEL_DIR = APP_DIR / "vosk-model-small-ar-tn-0.1-linto"

if not MODEL_DIR.exists():
    raise RuntimeError(
        f"Model folder not found: {MODEL_DIR}\n"
        "Place the unzipped Vosk model folder next to app.py."
    )

# Load model once at startup (important: slow to load each request)
model = Model(str(MODEL_DIR))

app = FastAPI(title="SOS STT Service (Vosk ar-tn)")


def _ensure_ffmpeg_available() -> None:
    if shutil.which("ffmpeg") is None:
        raise HTTPException(
            status_code=500,
            detail="ffmpeg not found. Install ffmpeg to convert audio to WAV 16k mono."
        )


def convert_to_wav_16k_mono(input_path: Path, output_path: Path) -> None:
    """
    Converts any audio file to PCM WAV, 16kHz, mono.
    """
    _ensure_ffmpeg_available()
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-ac", "1",
        "-ar", "16000",
        "-f", "wav",
        str(output_path),
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise HTTPException(
            status_code=400,
            detail=f"Audio conversion failed. ffmpeg error: {p.stderr.decode(errors='ignore')[:800]}"
        )


def transcribe_wav(wav_path: Path) -> dict:
    """
    Streaming transcription using Vosk from a WAV file already in 16k mono.
    Returns dict with full text + optional partial chunks.
    """
    import wave

    with wave.open(str(wav_path), "rb") as wf:
        if wf.getnchannels() != 1 or wf.getframerate() != 16000:
            raise HTTPException(
                status_code=400,
                detail="WAV must be mono 16kHz. Conversion step failed or input is invalid."
            )

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        final_text_parts = []
        results = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                r = json.loads(rec.Result())
                results.append(r)
                t = r.get("text", "").strip()
                if t:
                    final_text_parts.append(t)

        r_final = json.loads(rec.FinalResult())
        results.append(r_final)
        t_final = r_final.get("text", "").strip()
        if t_final:
            final_text_parts.append(t_final)

        full_text = " ".join(final_text_parts).strip()
        return {
            "text": full_text,
            "segments": results
        }


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_DIR.name}


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), language: Optional[str] = "ar-tn"):
    """
    Upload audio -> returns Tunisian Arabic transcription.
    Supports: wav/mp3/m4a/ogg/webm... (anything ffmpeg can read)
    """
    # basic size limit (adjust)
    MAX_MB = 25
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_MB:
        raise HTTPException(status_code=413, detail=f"File too large (> {MAX_MB}MB).")

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        raw_path = td_path / f"input_{file.filename}"
        wav_path = td_path / "audio_16k_mono.wav"

        raw_path.write_bytes(content)

        # Convert to WAV 16k mono (even if input already wav, this normalizes)
        convert_to_wav_16k_mono(raw_path, wav_path)

        # Transcribe
        out = transcribe_wav(wav_path)

    return JSONResponse({
        "language": language,
        "filename": file.filename,
        "text": out["text"],
        # if you want lighter responses, remove segments
        "segments": out["segments"],
    })
