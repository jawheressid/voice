import requests
import time

# Attendre que le serveur soit prêt
time.sleep(2)

# Envoyer le fichier pour transcription
url = "http://127.0.0.1:8002/transcribe"
with open("son.mp3", "rb") as f:
    files = {"file": ("son.mp3", f, "audio/mpeg")}
    response = requests.post(url, files=files)

if response.status_code == 200:
    result = response.json()
    print("=" * 60)
    print("TRANSCRIPTION RÉUSSIE")
    print("=" * 60)
    print(f"Fichier: {result.get('filename', 'N/A')}")
    print(f"Langue: {result.get('language', 'N/A')}")
    print(f"\nTexte transcrit:\n{result.get('text', '')}")
    print("=" * 60)
else:
    print(f"Erreur: {response.status_code}")
    print(response.text)
