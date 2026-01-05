"""
Configuration pour L'IA Survivante
Contient les paramètres du jeu, le prompt système et les mappings de cadeaux
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# ============================================================================
# CONFIGURATION API GEMINI
# ============================================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"  # Modèle rapide avec quota disponible

# ============================================================================
# CONFIGURATION TIKTOK
# ============================================================================

TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME", "@votre_username")

# ============================================================================
# PROMPT SYSTÈME POUR L'IA
# ============================================================================

SYSTEM_PROMPT = """Tu es un aventurier courageux coincé dans le Donjon TikTok, un labyrinthe mystérieux rempli de dangers.
Ta survie dépend entièrement des viewers qui te regardent en live.

RÈGLES IMPORTANTES:
- Réponds toujours en 1-2 phrases maximum (concis et percutant)
- Sois drôle, dynamique et réactif
- Remercie les viewers pour leurs actions
- Mentionne toujours le nom de l'utilisateur qui t'aide
- Décris brièvement l'action que tu effectues avec l'objet/aide reçu(e)
- Reste dans le rôle d'un aventurier dans un donjon fantastique

Exemples de bonnes réponses:
- "Merci @Jean pour la Rose ! Je l'utilise pour charmer un gobelin et il me laisse passer. +10 HP !"
- "@Marie m'envoie un Coeur ! Je le transforme en bouclier d'énergie. Je me sens invincible ! +5 HP !"
- "Les likes s'accumulent ! L'énergie positive me régénère lentement... +2 HP"
"""

# ============================================================================
# PARAMÈTRES DU JEU
# ============================================================================

class GameConfig:
    """Configuration des mécaniques de jeu"""
    
    # Statistiques de base
    MAX_HP = 100
    STARTING_HP = 100
    STARTING_LEVEL = 1
    STARTING_XP = 0
    
    # Progression
    XP_PER_LEVEL = 100  # XP nécessaire pour passer au niveau suivant
    
    # Likes
    LIKE_HEAL_AMOUNT = 1  # HP régénérés par like
    LIKE_THRESHOLD_FOR_REACTION = 50  # Réaction spéciale tous les X likes
    
    # Cooldown API
    API_COOLDOWN_SECONDS = 2.0  # Temps minimum entre 2 appels API
    
    # Fichiers OBS
    OBS_LAST_ACTION_FILE = "obs_files/last_action.txt"
    OBS_STATS_FILE = "obs_files/stats.txt"


# ============================================================================
# MAPPING DES CADEAUX TIKTOK
# ============================================================================

GIFT_ACTIONS = {
    # Format: "nom_du_cadeau": {"hp": X, "xp": Y, "description": "text"}
    
    # Cadeaux communs (1-100 pièces)
    "Rose": {
        "hp": 5,
        "xp": 10,
        "action": "attaque un monstre avec la rose enchantée"
    },
    "TikTok": {
        "hp": 3,
        "xp": 5,
        "action": "utilise le logo TikTok comme bouclier magique"
    },
    "Heart": {
        "hp": 8,
        "xp": 15,
        "action": "absorbe l'énergie du coeur pour se régénérer"
    },
    "Finger Heart": {
        "hp": 5,
        "xp": 8,
        "action": "lance un sort d'amour pour apaiser les monstres"
    },
    
    # Cadeaux moyens (100-500 pièces)
    "Perfume": {
        "hp": 15,
        "xp": 30,
        "action": "utilise le parfum pour endormir les gardes"
    },
    "Football": {
        "hp": 12,
        "xp": 25,
        "action": "lance le ballon pour déclencher un piège à distance"
    },
    "Sunglasses": {
        "hp": 10,
        "xp": 20,
        "action": "porte les lunettes pour voir les passages secrets"
    },
    
    # Cadeaux rares (500-1000 pièces)
    "Swan": {
        "hp": 25,
        "xp": 50,
        "action": "chevauche le cygne pour traverser une rivière de lave"
    },
    "Gaming Keyboard": {
        "hp": 20,
        "xp": 45,
        "action": "hack le système de sécurité du donjon"
    },
    
    # Cadeaux épiques (1000+ pièces)
    "Lion": {
        "hp": 40,
        "xp": 100,
        "action": "invoque un lion spirituel qui terrasse les ennemis"
    },
    "Falcon": {
        "hp": 35,
        "xp": 90,
        "action": "envoie le faucon en reconnaissance pour éviter les pièges"
    },
    "Drama Queen": {
        "hp": 50,
        "xp": 120,
        "action": "utilise l'énergie dramatique pour détruire un mur"
    },
    
    # Cadeau par défaut pour les cadeaux non mappés
    "default": {
        "hp": 5,
        "xp": 10,
        "action": "utilise ce cadeau mystérieux avec ingéniosité"
    }
}


def get_gift_info(gift_name: str) -> dict:
    """
    Récupère les informations d'un cadeau
    
    Args:
        gift_name: Nom du cadeau TikTok
        
    Returns:
        Dictionnaire avec hp, xp et action
    """
    return GIFT_ACTIONS.get(gift_name, GIFT_ACTIONS["default"])
