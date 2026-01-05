"""
L'IA Survivante - Jeu TikTok Live Interactif
Point d'entrée principal de l'application
"""

import asyncio
import signal
import sys
from src.game_engine import GameEngine
from src.tiktok_listener import TikTokListener


class Application:
    """Application principale qui orchestre tous les composants"""
    
    def __init__(self):
        """Initialise l'application"""
        self.game_engine = None
        self.tiktok_listener = None
        self.running = False
    
    async def start(self):
        """Démarre l'application"""
        try:
            print("=" * 50)
            print("🎮 L'IA SURVIVANTE - TikTok Live")
            print("=" * 50)
            print()
            
            # Initialiser le moteur de jeu
            print("⚙️  Initialisation du moteur de jeu...")
            self.game_engine = GameEngine()
            
            # Initialiser le listener TikTok
            print("⚙️  Initialisation du listener TikTok...")
            self.tiktok_listener = TikTokListener(self.game_engine)
            
            # Démarrer la connexion TikTok
            await self.tiktok_listener.start()
            
            # Marquer comme en cours d'exécution
            self.running = True
            
            # Démarrer le moteur de jeu (traitement de la queue API)
            print()
            print("=" * 50)
            print("✅ Système opérationnel !")
            print("🎬 En attente des événements TikTok Live...")
            print("💡 Appuyez sur Ctrl+C pour arrêter")
            print("=" * 50)
            print()
            
            await self.game_engine.start()
            
        except KeyboardInterrupt:
            print("\n⏸️  Interruption demandée par l'utilisateur")
            await self.stop()
        except Exception as e:
            print(f"\n❌ Erreur fatale: {e}")
            await self.stop()
            sys.exit(1)
    
    async def stop(self):
        """Arrête proprement l'application"""
        if not self.running:
            return
        
        print("\n🛑 Arrêt de l'application...")
        
        self.running = False
        
        # Arrêter le moteur de jeu
        if self.game_engine:
            self.game_engine.stop()
        
        # Déconnecter de TikTok
        if self.tiktok_listener:
            await self.tiktok_listener.stop()
        
        print("✅ Application arrêtée proprement")
    
    def handle_signal(self, signum, frame):
        """
        Handler pour les signaux du système (Ctrl+C)
        
        Args:
            signum: Numéro du signal
            frame: Frame d'exécution
        """
        print("\n⏸️  Signal d'arrêt reçu")
        asyncio.create_task(self.stop())


async def main():
    """Fonction principale asynchrone"""
    app = Application()
    
    # Configurer les handlers de signaux pour un arrêt propre
    loop = asyncio.get_event_loop()
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(app.stop()))
        except NotImplementedError:
            # Windows ne supporte pas add_signal_handler
            # On gère via KeyboardInterrupt directement
            pass
    
    # Démarrer l'application
    await app.start()


if __name__ == "__main__":
    try:
        # Lancer la boucle asynchrone
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Au revoir !")
        sys.exit(0)
