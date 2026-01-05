# 🎮 L'IA Survivante - Jeu TikTok Live Interactif

Jeu interactif pour TikTok Live où une IA contrôle un aventurier survivant dans un donjon mystérieux. Les viewers influencent l'aventure via leurs cadeaux et likes !

## 📋 Description

**L'IA Survivante** est un jeu interactif innovant qui transforme votre TikTok Live en aventure RPG. Une IA (powered by Google Gemini) incarne un personnage coincé dans le "Donjon TikTok" et réagit en temps réel aux actions des viewers :

- 🎁 **Cadeaux** → Actions narratives + Gain de HP/XP
- 👍 **Likes** → Soin passif du personnage
- 💬 **Commentaires** → Interaction avec le chat (logged)

L'IA génère des réponses drôles, dynamiques et contextuelles grâce au prompt système personnalisé.

## ✨ Fonctionnalités

- ✅ **Intégration API Google Gemini** (modèle `gemini-1.5-flash` gratuit)
- ✅ **Système de file d'attente** avec cooldown (2s) pour respecter les rate limits
- ✅ **Gestion intelligente des événements** :
  - Cadeaux → Appel API pour réaction narrative
  - Likes → Traitement local (pas d'API) + paliers tous les 50 likes
- ✅ **Système de progression** : HP, XP, Niveaux, Inventaire
- ✅ **Fichiers OBS** pour affichage en stream :
  - `obs_files/last_action.txt` → Dernière phrase de l'IA
  - `obs_files/stats.txt` → Stats du personnage (HP, Niveau, XP)
- ✅ **Code modulaire** et commenté en français
- ✅ **Architecture asynchrone** (asyncio)

## 📦 Prérequis

- Python 3.8+
- Compte TikTok avec accès au Live
- Clé API Google Gemini (gratuite) : [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- (Optionnel) OBS Studio pour afficher les fichiers texte en stream

## 🚀 Installation

### 1. Cloner ou télécharger le projet

```bash
cd survivor_ai
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet (copiez `.env.example`) :

```env
# Configuration pour L'IA Survivante

# Clé API Google Gemini (obligatoire)
GEMINI_API_KEY=votre_vraie_cle_api_ici

# Nom d'utilisateur TikTok pour se connecter au Live
TIKTOK_USERNAME=@votre_username_tiktok
```

**Important** :
- Obtenez votre clé API Gemini sur [Google AI Studio](https://aistudio.google.com/app/apikey)
- Remplacez `@votre_username_tiktok` par votre username TikTok (avec ou sans @)

## 🎮 Utilisation

### Lancer le jeu

```bash
python main.py
```

Le programme va :
1. Se connecter au live TikTok de l'utilisateur configuré
2. Initialiser le moteur de jeu
3. Commencer à écouter les événements (cadeaux, likes, commentaires)

### Arrêter le jeu

Appuyez sur `Ctrl+C` pour arrêter proprement l'application.

## 🎥 Intégration avec OBS Studio

Pour afficher les stats et actions de l'IA dans votre stream :

1. **Ouvrez OBS Studio**
2. **Ajoutez une source "Texte (GDI+)"** pour chaque fichier :
   - Source 1 : `obs_files/last_action.txt` (dernière action de l'IA)
   - Source 2 : `obs_files/stats.txt` (stats du personnage)
3. **Configurez les sources** :
   - ✅ Cochez "Lire depuis un fichier"
   - ✅ Sélectionnez le fichier correspondant
   - ✅ Choisissez la police, taille et couleur
   - ✅ Positionnez sur votre scène

Les fichiers se mettent à jour automatiquement en temps réel !

## 📁 Structure du Projet

```
survivor_ai/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration (API, prompts, cadeaux)
│   ├── game_engine.py         # Moteur de jeu + API Gemini
│   └── tiktok_listener.py     # Listener TikTok Live
├── obs_files/
│   ├── last_action.txt        # Dernière phrase de l'IA (OBS)
│   └── stats.txt              # Stats du personnage (OBS)
├── main.py                    # Point d'entrée principal
├── requirements.txt           # Dépendances Python
├── .env.example               # Template de configuration
├── .env                       # Configuration (à créer, non versionné)
├── .gitignore
└── README.md
```

## ⚙️ Configuration Avancée

### Modifier le Prompt Système

Éditez `src/config.py` → `SYSTEM_PROMPT` pour changer la personnalité de l'IA.

### Ajouter des Cadeaux

Éditez `src/config.py` → `GIFT_ACTIONS` :

```python
"MyCoolGift": {
    "hp": 20,
    "xp": 40,
    "action": "utilise ce cadeau pour faire quelque chose d'incroyable"
}
```

### Ajuster les Paramètres de Jeu

Éditez `src/config.py` → `GameConfig` :

```python
class GameConfig:
    MAX_HP = 100                        # HP maximum
    LIKE_HEAL_AMOUNT = 1                # HP par like
    LIKE_THRESHOLD_FOR_REACTION = 50    # Palier de likes pour réaction
    API_COOLDOWN_SECONDS = 2.0          # Cooldown entre appels API
```

## 🔧 Dépannage

### Erreur "GEMINI_API_KEY manquante"
- Vérifiez que le fichier `.env` existe et contient la clé API
- Assurez-vous que la clé est valide (testez sur [Google AI Studio](https://aistudio.google.com/))

### Erreur de connexion TikTok
- Vérifiez que le username est correct dans `.env`
- Assurez-vous que le compte est en live au moment de lancer le script
- La librairie TikTokLive peut nécessiter des mises à jour selon l'API TikTok

### L'IA ne répond pas
- Vérifiez les logs dans la console
- Le cooldown de 2s entre appels API peut créer un délai
- Vérifiez que l'API Gemini fonctionne (rate limits, quota)

### Les fichiers OBS ne se mettent pas à jour
- Vérifiez que le dossier `obs_files/` existe
- Rechargez les sources dans OBS (clic droit → Propriétés)
- Vérifiez les permissions d'écriture du dossier

## 📝 Licence

Projet open source - Libre d'utilisation et de modification.

## 🙏 Crédits

- **TikTokLive** : [https://github.com/isaackogan/TikTokLive](https://github.com/isaackogan/TikTokLive)
- **Google Gemini API** : [https://ai.google.dev/](https://ai.google.dev/)
- **Python-dotenv** : [https://github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)

---

**Bon stream et que l'aventure commence ! 🎮🗡️🛡️**
