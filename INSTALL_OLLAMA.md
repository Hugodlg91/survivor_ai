# 🚀 Installation Ollama - Guide Rapide

## 📥 Étape 1 : Télécharger Ollama

1. **Ouvrir le navigateur** et aller sur : **https://ollama.com/download**
2. **Cliquer sur "Download for Windows"**
3. **Télécharger** le fichier `OllamaSetup.exe`

## ⚙️ Étape 2 : Installer Ollama

1. **Double-cliquer** sur `OllamaSetup.exe`
2. **Accepter** les droits administrateur
3. **Suivre** l'assistant d'installation (Next → Next → Install)
4. **Attendre** la fin de l'installation

## ✅ Étape 3 : Vérifier l'Installation

Ouvrir un **nouveau terminal PowerShell** et taper :

```powershell
ollama --version
```

Si ça affiche une version (ex: `ollama version 0.13.5`), c'est bon ! ✅

## 📦 Étape 4 : Télécharger le Modèle

Dans le même terminal, taper :

```powershell
ollama pull llama3.2:3b
```

**⏱️ Temps estimé** : 2-5 minutes (télécharge ~2GB)

**C'est tout !** Une fois terminé, reviens me voir et je pourrai lancer les tests ! 🎮

---

## 🆘 En cas de problème

**"ollama n'est pas reconnu"** :
- Fermer et rouvrir le terminal
- Redémarrer Windows
- Vérifier que Ollama est dans le PATH (normalement automatique)

**WSL2 requis** :
- Ollama peut demander d'installer WSL2
- Suivre les instructions à l'écran
- Redémarrer après installation
