"""
Moteur de jeu pour L'IA Survivante
Gère les stats du personnage et l'intégration avec l'API Google Gemini
"""

import asyncio
import time
import os
import json
from typing import Optional
from google import genai
from google.genai import types
from src.config import (
    GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT, GameConfig, get_gift_info
)


class Character:
    """Représente le personnage joueur avec ses statistiques"""
    
    def __init__(self):
        """Initialise le personnage avec les stats de départ"""
        self.hp = GameConfig.STARTING_HP
        self.max_hp = GameConfig.MAX_HP
        self.level = GameConfig.STARTING_LEVEL
        self.xp = GameConfig.STARTING_XP
        self.inventory = []
        
    def add_hp(self, amount: int) -> int:
        """
        Ajoute des HP au personnage (avec cap au maximum)
        
        Args:
            amount: Nombre de HP à ajouter
            
        Returns:
            HP effectivement ajoutés
        """
        old_hp = self.hp
        self.hp = min(self.hp + amount, self.max_hp)
        return self.hp - old_hp
    
    def remove_hp(self, amount: int) -> bool:
        """
        Retire des HP au personnage
        
        Args:
            amount: Nombre de HP à retirer
            
        Returns:
            True si le personnage est toujours vivant, False sinon
        """
        self.hp = max(0, self.hp - amount)
        return self.hp > 0
    
    def add_xp(self, amount: int) -> bool:
        """
        Ajoute de l'XP et gère le level up
        
        Args:
            amount: Quantité d'XP à ajouter
            
        Returns:
            True si level up, False sinon
        """
        self.xp += amount
        
        # Vérifier si level up
        if self.xp >= GameConfig.XP_PER_LEVEL:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """Monte le personnage de niveau"""
        self.level += 1
        self.xp -= GameConfig.XP_PER_LEVEL
        
        # Augmenter le HP max et restaurer complètement
        self.max_hp += 10
        self.hp = self.max_hp
    
    def add_to_inventory(self, item: str):
        """
        Ajoute un objet à l'inventaire
        
        Args:
            item: Nom de l'objet
        """
        self.inventory.append(item)
        
        # Limiter la taille de l'inventaire pour éviter la surcharge
        if len(self.inventory) > 10:
            self.inventory.pop(0)
    
    def get_stats_text(self) -> str:
        """
        Retourne une représentation textuelle des stats
        
        Returns:
            String formaté pour l'affichage OBS
        """
        xp_progress = f"{self.xp}/{GameConfig.XP_PER_LEVEL}"
        hp_bar = "❤️ " * (self.hp // 10) + "🖤 " * ((self.max_hp - self.hp) // 10)
        
        return f"""╔══════════════════════════════╗
║  🗡️  L'IA SURVIVANTE  🛡️  ║
╚══════════════════════════════╝

💚 PV: {self.hp}/{self.max_hp}
{hp_bar}

⭐ Niveau: {self.level}
✨ XP: {xp_progress}

🎒 Derniers objets: {', '.join(self.inventory[-3:]) if self.inventory else 'Vide'}
"""


class GameEngine:
    """Moteur principal du jeu avec intégration API Gemini"""
    
    def __init__(self):
        """Initialise le moteur de jeu"""
        self.character = Character()
        self.last_api_call = 0  # Timestamp du dernier appel API
        self.api_queue = asyncio.Queue()  # File d'attente pour les requêtes
        self.is_running = False
        
        # Configurer l'API Gemini
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY manquante dans le fichier .env")
        
        # Créer le client avec la nouvelle API google.genai
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Créer les dossiers OBS si nécessaire
        os.makedirs("obs_files", exist_ok=True)
        
        # Initialiser les fichiers OBS
        self._write_stats()
        self._write_action("🎮 L'aventure commence ! En attente des viewers...")
    
    def _write_stats(self):
        """Écrit les stats dans le fichier OBS"""
        with open(GameConfig.OBS_STATS_FILE, "w", encoding="utf-8") as f:
            f.write(self.character.get_stats_text())
        self._write_json_state()
    
    def _write_action(self, action: str):
        """
        Écrit la dernière action dans le fichier OBS
        
        Args:
            action: Texte de l'action à afficher
        """
        with open(GameConfig.OBS_LAST_ACTION_FILE, "w", encoding="utf-8") as f:
            f.write(action)
        self._write_json_state(action)
    
    def _write_json_state(self, last_action: str = None):
        """
        Écrit l'état du jeu en JSON pour l'overlay HTML
        
        Args:
            last_action: Dernière action à inclure (optionnel)
        """
        state = {
            "hp": self.character.hp,
            "max_hp": self.character.max_hp,
            "xp": self.character.xp,
            "xp_for_next_level": GameConfig.XP_PER_LEVEL,
            "level": self.character.level,
            "inventory": self.character.inventory.copy(),
            "last_action": last_action if last_action else "🎮 En attente d'événements..."
        }
        
        json_file = "obs_files/game_state.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    async def _process_api_queue(self):
        """Traite la file d'attente des appels API avec cooldown"""
        while self.is_running:
            try:
                # Attendre une requête dans la queue
                request_data = await asyncio.wait_for(
                    self.api_queue.get(), 
                    timeout=1.0
                )
                
                # Vérifier le cooldown
                time_since_last_call = time.time() - self.last_api_call
                if time_since_last_call < GameConfig.API_COOLDOWN_SECONDS:
                    wait_time = GameConfig.API_COOLDOWN_SECONDS - time_since_last_call
                    await asyncio.sleep(wait_time)
                
                # Effectuer l'appel API
                response = await self._call_gemini_api(request_data)
                
                # Mettre à jour le timestamp
                self.last_api_call = time.time()
                
                # Écrire la réponse dans le fichier OBS
                self._write_action(response)
                
            except asyncio.TimeoutError:
                # Pas de requête dans la queue, continuer
                continue
            except Exception as e:
                print(f"❌ Erreur lors du traitement de la queue API: {e}")
                await asyncio.sleep(1)
    
    async def _call_gemini_api(self, prompt: str) -> str:
        """
        Appelle l'API Gemini de manière asynchrone
        
        Args:
            prompt: Texte du prompt à envoyer
            
        Returns:
            Réponse générée par l'IA
        """
        try:
            # Créer la configuration avec system instruction
            config = types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=1.0
            )
            
            # Générer la réponse avec la nouvelle API
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=GEMINI_MODEL,
                contents=prompt,
                config=config
            )
            
            return response.text.strip()
        except Exception as e:
            print(f"❌ Erreur API Gemini: {e}")
            return "💀 L'aventurier est momentanément désorienté... (erreur API)"
    
    async def handle_gift(self, username: str, gift_name: str):
        """
        Gère la réception d'un cadeau TikTok
        
        Args:
            username: Nom de l'utilisateur qui a envoyé le cadeau
            gift_name: Nom du cadeau
        """
        # Récupérer les infos du cadeau
        gift_info = get_gift_info(gift_name)
        
        # Appliquer les effets
        hp_gained = self.character.add_hp(gift_info["hp"])
        leveled_up = self.character.add_xp(gift_info["xp"])
        self.character.add_to_inventory(gift_name)
        
        # Mettre à jour les stats OBS
        self._write_stats()
        
        # Créer le prompt pour l'IA
        level_info = f" 🎉 LEVEL UP ! Niveau {self.character.level} !" if leveled_up else ""
        prompt = f"""L'utilisateur @{username} t'envoie un cadeau: {gift_name}.
Tu {gift_info['action']}.
Tu gagnes {hp_gained} HP et {gift_info['xp']} XP.{level_info}

Réponds en 1-2 phrases maximum. Remercie @{username} et décris brièvement ton action."""
        
        # Ajouter à la queue API
        await self.api_queue.put(prompt)
    
    async def handle_like(self):
        """Gère un like (soin passif sans appel API)"""
        hp_gained = self.character.add_hp(GameConfig.LIKE_HEAL_AMOUNT)
        
        if hp_gained > 0:
            self._write_stats()
    
    async def handle_like_milestone(self, total_likes: int):
        """
        Gère un palier de likes pour une réaction spéciale
        
        Args:
            total_likes: Nombre total de likes reçus
        """
        hp_bonus = 5
        xp_bonus = 10
        
        self.character.add_hp(hp_bonus)
        self.character.add_xp(xp_bonus)
        self._write_stats()
        
        prompt = f"""Les viewers t'ont envoyé {total_likes} likes au total !
Cette vague d'énergie positive te régénère. +{hp_bonus} HP, +{xp_bonus} XP !

Réagis avec enthousiasme en 1-2 phrases."""
        
        await self.api_queue.put(prompt)
    
    async def start(self):
        """Démarre le moteur de jeu"""
        self.is_running = True
        print("✅ Moteur de jeu démarré")
        print(f"📊 Stats initiales: {self.character.hp} HP, Niveau {self.character.level}")
        
        # Lancer le worker de la queue API
        await self._process_api_queue()
    
    def stop(self):
        """Arrête le moteur de jeu"""
        self.is_running = False
        print("⏹️  Moteur de jeu arrêté")
