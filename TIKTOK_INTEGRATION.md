# 🎬 Guide d'Intégration - TikTok Live Studio

## 📺 Ajouter l'Overlay HTML à TikTok Live Studio

### 🎯 Méthode Recommandée : Source Navigateur

L'overlay HTML (`overlay.html`) offre une interface **beaucoup plus spectaculaire** que les fichiers texte simples, avec :
- ✨ Animations fluides
- 🎨 Design moderne et coloré
- 📊 Barres de progression animées
- 🌟 Effets visuels professionnels

---

## 🚀 Étapes d'Intégration

### 1. Lancer le jeu

Ouvrez un terminal dans le dossier du projet et lancez :

```bash
python main.py
```

Ou pour tester sans TikTok Live :

```bash
python test_simulation.py
```

### 2. Ouvrir TikTok Live Studio

1. Lancez **TikTok Live Studio**
2. Configurez votre scène de base (webcam, etc.)

### 3. Ajouter l'Overlay comme Source Navigateur

#### Option A : Source Navigateur (Recommandé) ✨

1. **Cliquez sur `+ Ajouter une source`** (ou `Add Source`)
2. **Sélectionnez `Navigateur`** (ou `Browser Source`)
3. **Configurez la source** :
   - **URL** : `file:///C:/Users/Hugo/Documents/survivor_ai/overlay.html`
   - **Largeur** : `1920`
   - **Hauteur** : `1080`
   - **FPS** : `30` ou `60`
4. **Validez** ✅

L'overlay apparaîtra immédiatement avec :
- Titre animé en haut
- Stats (HP/XP) à gauche
- Badge de niveau à droite
- Inventaire en bas à gauche
- Dernière action de l'IA en bas (centre)

#### Option B : Sources Texte Simples (Alternative)

Si TikTok Live Studio n'a pas de Source Navigateur, utilisez les fichiers texte :

1. **Cliquer sur `+ Ajouter une source`**
2. **Choisir `Texte`** ou **`Text`**
3. **Configurer** :
   - ✅ Cocher **"Lire depuis un fichier"** / **"Read from file"**
   - 📁 Naviguer vers `C:\Users\Hugo\Documents\survivor_ai\obs_files\stats.txt`
   - 🎨 Personnaliser police, taille, couleur
4. **Répéter** pour `last_action.txt`

---

## 🎨 Personnalisation de l'Overlay

### Ajuster la Taille et Position

Dans TikTok Live Studio :
- **Redimensionner** : Glisser les coins de la source
- **Déplacer** : Glisser la source
- **Transparence** : L'overlay a un fond transparent, seuls les éléments UI sont visibles

### Modifier le Design

Éditez `overlay.html` avec un éditeur de texte :

**Changer les couleurs** :
```css
/* Ligne 44 - Couleur du titre */
background: linear-gradient(135deg, #ff6b9d 0%, #ffa06b 50%, #ffd56b 100%);

/* Ligne 109 - Couleur barre HP */
background: linear-gradient(90deg, #ff1744 0%, #ff6b9d 100%);

/* Ligne 139 - Couleur barre XP */
background: linear-gradient(90deg, #00d4ff 0%, #64b5f6 100%);
```

**Changer la taille des éléments** :
```css
/* Ligne 41 - Taille du titre */
font-size: 72px; /* Modifier cette valeur */
```

---

## 🔄 Mises à Jour Automatiques

L'overlay se met à jour **automatiquement toutes les 500ms** :
- ✅ Pas besoin de rafraîchir manuellement
- ✅ Les barres HP/XP s'animent automatiquement
- ✅ Les nouvelles actions apparaissent avec une animation

---

## 🧪 Tester l'Overlay

### Sans TikTok Live

1. **Lancer la simulation** :
   ```bash
   python test_simulation.py
   ```

2. **Ouvrir dans le navigateur** :
   - Ouvrir `overlay.html` dans Chrome/Firefox
   - Observer les mises à jour en temps réel

3. **Observer** :
   - Les barres HP/XP qui changent
   - Le niveau qui augmente
   - L'inventaire qui se remplit
   - Les actions de l'IA qui s'affichent

### Avec TikTok Live

1. **Être en live** sur TikTok avec le compte configuré
2. **Lancer** : `python main.py`
3. **Demander aux viewers** d'envoyer des cadeaux et likes
4. **Observer** l'overlay réagir en temps réel ! 🎉

---

## 💡 Conseils & Astuces

### Positionnement Optimal

**Configuration recommandée** :
- Overlay en **plein écran** (1920x1080)
- Votre webcam/contenu **par-dessus** l'overlay
- Position webcam : **centre** ou **coin**

### Performance

- L'overlay est **très léger** (aucune image lourde)
- Utilise uniquement CSS et JavaScript
- Pas d'impact sur les performances du stream

### Dépannage

**L'overlay ne se met pas à jour** :
- ✅ Vérifier que le jeu est lancé (`python main.py` ou `test_simulation.py`)
- ✅ Vérifier que le fichier `obs_files/game_state.json` existe
- ✅ Ouvrir la console du navigateur (F12) pour voir les erreurs

**L'overlay ne s'affiche pas** :
- ✅ Vérifier le chemin du fichier (doit être absolu)
- ✅ Utiliser `file:///...` et pas juste `C:\...`
- ✅ Redémarrer TikTok Live Studio

**Les animations sont saccadées** :
- ✅ Réduire le FPS de la source navigateur (passer de 60 à 30)
- ✅ Fermer d'autres applications gourmandes

---

## 📸 Aperçu de l'Overlay

L'overlay affiche :

![Aperçu de l'overlay](file:///C:/Users/Hugo/.gemini/antigravity/brain/d8638aa7-e2c0-4911-92a0-6f3109f2ea53/overlay_initial_state_1767654788911.png)

- **Titre** : "L'IA SURVIVANTE" avec effet de glow
- **Barre HP** : Rouge/rose avec glow, affiche les PV actuels
- **Barre XP** : Bleue avec glow, progression vers le niveau suivant
- **Badge Niveau** : Cercle doré avec le niveau actuel
- **Inventaire** : Les 3 derniers objets reçus
- **Dernière Action** : Grande zone pour les réponses de l'IA

---

## 🎮 Fichiers Générés

Le jeu génère automatiquement :

1. **`obs_files/game_state.json`** → Données pour l'overlay HTML
2. **`obs_files/stats.txt`** → Stats formatées (backup texte)
3. **`obs_files/last_action.txt`** → Dernière action (backup texte)

---

**Bon stream ! 🚀 L'overlay va WOW tes viewers ! 🌟**
