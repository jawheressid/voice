# Service de Transcription Audio (Arabe Tunisien)

🎙️ Service de transcription vocale en arabe tunisien utilisant Vosk et FastAPI/Streamlit.

## 📋 Description

Ce projet fournit deux interfaces pour transcrire des fichiers audio en arabe tunisien :
- **API REST** avec FastAPI
- **Interface Web** avec Streamlit

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- ffmpeg (pour la conversion audio)

### Installation de ffmpeg
```bash
# Windows (avec Chocolatey)
choco install ffmpeg

# Ou téléchargez depuis https://ffmpeg.org/download.html
```

### Installation des dépendances Python
```bash
pip install -r requirements.txt
```

## 📁 Structure du projet

```
.
├── app.py                          # API FastAPI
├── streamlit_app.py                # Interface Streamlit
├── requirements.txt                # Dépendances Python
├── vosk-model-small-ar-tn-0.1-linto/  # Modèle Vosk (requis)
├── test_transcribe.py              # Script de test pour l'API
└── test_m4a.py                     # Script de test pour fichiers M4A
```

## 🎯 Utilisation

### Option 1: Interface Web Streamlit (Recommandé)

Lancez l'interface graphique :

```bash
streamlit run streamlit_app.py
```

L'application s'ouvrira dans votre navigateur à `http://localhost:8501`

**Fonctionnalités :**
- 📤 Upload de fichiers audio (MP3, M4A, WAV, OGG, WEBM)
- 🎤 Enregistrement audio en direct
- 📝 Transcription en temps réel
- 💾 Téléchargement des résultats
- 🎨 Interface moderne et intuitive

### Option 2: API REST FastAPI

Démarrez le serveur API :

```bash
uvicorn app:app --host 127.0.0.1 --port 8002
```

**Endpoints disponibles :**
- `GET /health` - Vérifier l'état du service
- `POST /transcribe` - Transcrire un fichier audio

**Exemple d'utilisation avec curl :**

```bash
curl -X POST "http://127.0.0.1:8002/transcribe" \
  -F "file=@votre_audio.mp3"
```

**Exemple avec Python :**

```python
import requests

url = "http://127.0.0.1:8002/transcribe"
with open("audio.mp3", "rb") as f:
    files = {"file": ("audio.mp3", f, "audio/mpeg")}
    response = requests.post(url, files=files)
    
result = response.json()
print(f"Transcription: {result['text']}")
```

## 📊 Formats audio supportés

- MP3
- M4A
- WAV
- OGG
- WEBM
- Et tous les formats supportés par ffmpeg

## 🔧 Configuration

### Limites de taille
Par défaut, la taille maximale des fichiers est de **25 MB**. 
Modifiez cette valeur dans `app.py` :

```python
MAX_MB = 25  # Changez cette valeur
```

### Port du serveur
Pour changer le port de l'API :

```bash
uvicorn app:app --host 127.0.0.1 --port VOTRE_PORT
```

## 📝 Modèle de langue

Ce projet utilise le modèle Vosk **vosk-model-small-ar-tn-0.1-linto** pour l'arabe tunisien.

Si le modèle n'est pas présent, téléchargez-le depuis :
https://alphacephei.com/vosk/models

## 🧪 Tests

### Tester avec un fichier MP3 :
```bash
python test_transcribe.py
```

### Tester avec un fichier M4A :
```bash
python test_m4a.py
```

## 💡 Exemples de résultats

**Fichier audio :** `Test1.m4a`

**Transcription :**
```
عالسلامة صباح الخير أنا اليوم ريت أم قاعدة تضرب في ولدها
```

## 🐛 Résolution de problèmes

### Problème d'affichage de l'arabe dans le terminal
Le terminal PowerShell ne gère pas bien l'affichage RTL de l'arabe. Les résultats sont sauvegardés dans :
- `transcription_result.txt` - Format texte
- `transcription_result.json` - Format JSON

Ouvrez ces fichiers avec un éditeur supportant l'UTF-8 (VS Code, Notepad++, etc.)

### Erreur "ffmpeg not found"
Installez ffmpeg et assurez-vous qu'il est dans le PATH système.

### Erreur "Model folder not found"
Vérifiez que le dossier `vosk-model-small-ar-tn-0.1-linto` existe à côté de `app.py`.

### Port déjà utilisé
Changez le port avec l'option `--port` :
```bash
uvicorn app:app --port 8003
```

## 📄 License

Ce projet utilise le modèle Vosk qui est sous licence Apache 2.0.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📞 Support

Pour toute question ou problème, veuillez ouvrir une issue sur le dépôt du projet.

---

**Développé avec ❤️ pour la communauté tunisienne**
