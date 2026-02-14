import streamlit as st
import requests
from pathlib import Path
import json
import time

# Configuration de la page
st.set_page_config(
    page_title="Transcription Audio Arabe Tunisien",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour une belle interface
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stTitle {
        color: #1e3a8a;
        font-weight: 700;
        text-align: center;
        padding: 1rem 0;
    }
    .upload-box {
        border: 2px dashed #3b82f6;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: white;
        margin: 1rem 0;
    }
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .arabic-text {
        font-size: 24px;
        text-align: right;
        direction: rtl;
        line-height: 1.8;
        background-color: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e0f2fe;
        border-left: 4px solid #0284c7;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Titre principal
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🎤 Transcription Audio Arabe Tunisien</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 18px;'>Convertissez vos fichiers audio en texte avec précision</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/200/000000/audio-wave--v1.png", width=150)
    st.markdown("## 📋 Informations")
    st.info("""
    **Formats supportés:**
    - MP3
    - WAV
    - M4A
    - OGG
    - WEBM
    - Et autres formats audio
    
    **Langue:**
    Arabe Tunisien (ar-tn)
    
    **Taille max:**
    25 MB
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Configuration")
    api_url = st.text_input("URL de l'API", value="http://127.0.0.1:8002")
    
    st.markdown("---")
    st.markdown("### 📊 Statistiques")
    if 'transcription_count' not in st.session_state:
        st.session_state.transcription_count = 0
    st.metric("Transcriptions réalisées", st.session_state.transcription_count)

# Colonnes pour une meilleure disposition
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📁 Upload de fichier audio")
    uploaded_file = st.file_uploader(
        "Glissez-déposez votre fichier audio ici",
        type=['mp3', 'wav', 'm4a', 'ogg', 'webm', 'flac', 'aac'],
        help="Formats supportés: MP3, WAV, M4A, OGG, WEBM, FLAC, AAC"
    )
    
    if uploaded_file:
        st.success(f"✅ Fichier chargé: **{uploaded_file.name}**")
        file_size = uploaded_file.size / (1024 * 1024)  # Convertir en MB
        st.info(f"Taille: {file_size:.2f} MB")
        
        # Bouton de transcription
        if st.button("🚀 Lancer la transcription", type="primary", use_container_width=True):
            with st.spinner("🔄 Transcription en cours... Veuillez patienter."):
                try:
                    # Envoyer le fichier à l'API
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{api_url}/transcribe", files=files, timeout=120)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.last_result = result
                        st.session_state.transcription_count += 1
                        st.balloons()
                    else:
                        st.error(f"❌ Erreur {response.status_code}: {response.text}")
                        st.session_state.last_result = None
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Impossible de se connecter à l'API. Assurez-vous que le serveur FastAPI est en cours d'exécution.")
                    st.code(f"uvicorn app:app --host 127.0.0.1 --port {api_url.split(':')[-1]}", language="bash")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
                    st.session_state.last_result = None

with col2:
    st.markdown("### 🎵 Exemples rapides")
    st.info("💡 Vous pouvez aussi tester avec les fichiers existants du projet")
    
    example_files = list(Path(".").glob("*.mp3")) + list(Path(".").glob("*.m4a"))
    if example_files:
        selected_example = st.selectbox(
            "Choisir un fichier d'exemple:",
            ["-- Sélectionner --"] + [f.name for f in example_files]
        )
        
        if selected_example != "-- Sélectionner --" and st.button("📂 Transcrire l'exemple", use_container_width=True):
            with st.spinner("🔄 Transcription en cours..."):
                try:
                    with open(selected_example, "rb") as f:
                        files = {"file": (selected_example, f, "audio/mpeg")}
                        response = requests.post(f"{api_url}/transcribe", files=files, timeout=120)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.last_result = result
                        st.session_state.transcription_count += 1
                        st.balloons()
                    else:
                        st.error(f"❌ Erreur {response.status_code}: {response.text}")
                        st.session_state.last_result = None
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
                    st.session_state.last_result = None

# Affichage des résultats
st.markdown("---")
if 'last_result' in st.session_state and st.session_state.last_result:
    result = st.session_state.last_result
    
    st.markdown("### 📝 Résultat de la transcription")
    
    # Boîte de résultat stylisée
    st.markdown("""
    <div class='result-box'>
        <h2 style='margin-top: 0; text-align: center;'>✨ Transcription réussie ✨</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Informations sur le fichier
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("📄 Fichier", result.get('filename', 'N/A'))
    with col_info2:
        st.metric("🌍 Langue", result.get('language', 'N/A'))
    with col_info3:
        text = result.get('text', '')
        word_count = len(text.split()) if text else 0
        st.metric("📊 Nombre de mots", word_count)
    
    # Texte transcrit en arabe
    st.markdown("### 🎯 Texte transcrit")
    text = result.get('text', '')
    if text:
        st.markdown(f"""
        <div class='arabic-text'>
            {text}
        </div>
        """, unsafe_allow_html=True)
        
        # Options d'export
        st.markdown("### 💾 Exporter le résultat")
        col_export1, col_export2, col_export3 = st.columns(3)
        
        with col_export1:
            st.download_button(
                label="📄 Télécharger TXT",
                data=text,
                file_name="transcription.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_export2:
            json_data = json.dumps(result, ensure_ascii=False, indent=2)
            st.download_button(
                label="📋 Télécharger JSON",
                data=json_data,
                file_name="transcription.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col_export3:
            if st.button("📋 Copier dans le presse-papier", use_container_width=True):
                st.code(text)
                st.info("✅ Copiez le texte ci-dessus")
        
        # Détails segments (optionnel)
        with st.expander("🔍 Voir les détails des segments"):
            segments = result.get('segments', [])
            if segments:
                for i, segment in enumerate(segments, 1):
                    if segment.get('text'):
                        st.json(segment)
            else:
                st.info("Aucun segment disponible")
    else:
        st.warning("⚠️ Aucun texte n'a été détecté dans l'audio")
else:
    # Message d'accueil
    st.markdown("""
    <div class='info-box'>
        <h3>👋 Bienvenue!</h3>
        <p>Commencez par charger un fichier audio pour le transcrire en texte arabe tunisien.</p>
        <p><strong>Instructions:</strong></p>
        <ol>
            <li>Choisissez un fichier audio (MP3, WAV, M4A, etc.)</li>
            <li>Cliquez sur "Lancer la transcription"</li>
            <li>Attendez le résultat et exportez-le si nécessaire</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; padding: 1rem;'>
    <p>🔊 Système de transcription audio Vosk • Modèle: ar-tn (Arabe Tunisien)</p>
    <p>Développé avec ❤️ en utilisant FastAPI + Streamlit</p>
</div>
""", unsafe_allow_html=True)
