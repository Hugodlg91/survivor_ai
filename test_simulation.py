"""
Script de simulation pour tester L'IA Survivante sans TikTok Live
Simule des événements de cadeaux et likes pour tester le système
"""

import asyncio
import random
from src.game_engine import GameEngine


class TikTokSimulator:
    """Simule des événements TikTok pour tester le système"""
    
    def __init__(self, game_engine):
        """
        Initialise le simulateur
        
        Args:
            game_engine: Instance de GameEngine
        """
        self.game_engine = game_engine
        self.running = False
        
        # Liste de noms d'utilisateurs fictifs
        self.usernames = [
            "TestUser123", "GamerPro", "StreamFan", "LuckyViewer",
            "AdventureSeeker", "DungeonMaster", "TikTokHero", "MagicWizard"
        ]
        
        # Liste de cadeaux à tester
        self.gifts = [
            "Rose", "Heart", "TikTok", "Finger Heart",
            "Perfume", "Football", "Swan", "Lion"
        ]
    
    async def simulate_gift(self):
        """Simule l'envoi d'un cadeau aléatoire"""
        username = random.choice(self.usernames)
        gift_name = random.choice(self.gifts)
        
        print(f"🎁 [SIMULATION] @{username} envoie {gift_name}")
        await self.game_engine.handle_gift(username, gift_name)
    
    async def simulate_likes(self, count: int = None):
        """
        Simule des likes
        
        Args:
            count: Nombre de likes (si None, entre 1 et 10)
        """
        if count is None:
            count = random.randint(1, 10)
        
        print(f"👍 [SIMULATION] {count} like(s) reçu(s)")
        
        # Traitement par lot
        await self.game_engine.handle_like(count)
    
    async def simulate_like_milestone(self):
        """Simule un palier de likes"""
        total_likes = random.randint(50, 200)
        print(f"✨ [SIMULATION] Palier de {total_likes} likes atteint")
        await self.game_engine.handle_like_milestone(total_likes)
    
    async def random_event_loop(self):
        """Boucle qui génère des événements aléatoires"""
        event_count = 0
        
        while self.running and event_count < 20:  # Max 20 événements
            # Choisir un type d'événement aléatoire
            event_type = random.choices(
                ["gift", "likes", "milestone"],
                weights=[50, 40, 10]  # 50% cadeaux, 40% likes, 10% milestone
            )[0]
            
            if event_type == "gift":
                await self.simulate_gift()
            elif event_type == "likes":
                await self.simulate_likes()
            else:
                await self.simulate_like_milestone()
            
            event_count += 1
            
            # Attendre entre 3 et 8 secondes entre chaque événement
            wait_time = random.uniform(3, 8)
            print(f"⏳ Prochain événement dans {wait_time:.1f}s...\n")
            await asyncio.sleep(wait_time)
        
        print("\n🏁 Simulation terminée!")
        self.running = False
    
    async def run_scenario(self):
        """Execute un scénario de test prédéfini"""
        print("\n" + "="*50)
        print("🎬 SCÉNARIO DE TEST - L'IA Survivante")
        print("="*50 + "\n")
        
        self.running = True
        
        # Étape 1: Quelques likes
        print("📍 ÉTAPE 1: Likes initiaux")
        await self.simulate_likes(5)
        await asyncio.sleep(3)
        
        # Étape 2: Premier cadeau
        print("\n📍 ÉTAPE 2: Premier cadeau")
        await self.game_engine.handle_gift("PlayerOne", "Rose")
        await asyncio.sleep(4)
        
        # Étape 3: Plusieurs cadeaux
        print("\n📍 ÉTAPE 3: Vague de cadeaux")
        for i in range(3):
            await self.simulate_gift()
            await asyncio.sleep(3)
        
        # Étape 4: Palier de likes
        print("\n📍 ÉTAPE 4: Palier de likes")
        await self.simulate_like_milestone()
        await asyncio.sleep(4)
        
        # Étape 5: Cadeau épique
        print("\n📍 ÉTAPE 5: Cadeau épique")
        await self.game_engine.handle_gift("MegaFan", "Lion")
        await asyncio.sleep(4)
        
        # Étape 6: Plus de likes
        print("\n📍 ÉTAPE 6: Vague de likes")
        await self.simulate_likes(15)
        await asyncio.sleep(3)
        
        # Étape 7: Dernier cadeau
        print("\n📍 ÉTAPE 7: Cadeau final")
        await self.game_engine.handle_gift("StreamHero", "Drama Queen")
        await asyncio.sleep(4)
        
        print("\n🎉 Scénario terminé!")
        print("\n💡 Consultez les fichiers OBS pour voir les résultats:")
        print("   - obs_files/last_action.txt")
        print("   - obs_files/stats.txt")
        
        self.running = False


async def main():
    """Fonction principale du test"""
    print("=" * 50)
    print("🧪 MODE TEST - L'IA Survivante")
    print("=" * 50)
    print()
    
    # Initialiser le moteur de jeu
    print("⚙️  Initialisation du moteur de jeu...")
    game_engine = GameEngine()
    
    # Créer le simulateur
    simulator = TikTokSimulator(game_engine)
    
    print("\n" + "=" * 50)
    print("Choisissez un mode de test:")
    print("=" * 50)
    print("1. Scénario prédéfini (recommandé)")
    print("2. Événements aléatoires")
    print("=" * 50)
    
    # Pour l'automatisation, utiliser le scénario par défaut
    choice = "1"
    
    # Créer une tâche pour le moteur de jeu
    game_task = asyncio.create_task(game_engine.start())
    
    # Attendre un peu que le moteur démarre
    await asyncio.sleep(1)
    
    try:
        if choice == "1":
            await simulator.run_scenario()
        else:
            await simulator.random_event_loop()
        
        # Attendre un peu pour les dernières réponses API
        print("\n⏳ Attente des dernières réponses API...")
        await asyncio.sleep(5)
        
    except KeyboardInterrupt:
        print("\n⏸️  Interruption demandée")
    finally:
        # Arrêter le moteur
        game_engine.stop()
        
        # Annuler la tâche du moteur de jeu
        game_task.cancel()
        try:
            await game_task
        except asyncio.CancelledError:
            pass
        
        print("\n✅ Test terminé")


if __name__ == "__main__":
    asyncio.run(main())
