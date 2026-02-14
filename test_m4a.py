import requests
import time
import json

# Attendre que le serveur soit prêt
time.sleep(1)

# Envoyer le fichier pour transcription
url = "http://127.0.0.1:8002/transcribe"
with open("Test1.m4a", "rb") as f:
    files = {"file": ("Test1.m4a", f, "audio/m4a")}
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
    
    # Sauvegarder dans un fichier avec encodage UTF-8
    output_file = "transcription_result.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Fichier: {result.get('filename', 'N/A')}\n")
        f.write(f"Langue: {result.get('language', 'N/A')}\n\n")
        f.write(f"Texte transcrit:\n{result.get('text', '')}\n")
    
    print(f"\n✓ Résultat sauvegardé dans: {output_file}")
    print("  Ouvrez ce fichier avec Notepad ou VS Code pour voir l'arabe correctement.")
    
    # Sauvegarder aussi en JSON
    json_file = "transcription_result.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON complet sauvegardé dans: {json_file}")
else:
    print(f"Erreur: {response.status_code}")
    print(response.text)
