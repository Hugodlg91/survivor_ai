"""
Listener TikTok Live
Gère la connexion au live TikTok et les événements (cadeaux, likes, etc.)
"""

from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, GiftEvent, LikeEvent, CommentEvent
from src.config import TIKTOK_USERNAME, GameConfig


class TikTokListener:
    """Gère la connexion et les événements TikTok Live"""
    
    def __init__(self, game_engine):
        """
        Initialise le listener TikTok
        
        Args:
            game_engine: Instance de GameEngine pour gérer les événements
        """
        self.game_engine = game_engine
        self.client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)
        self.total_likes = 0
        self.likes_since_last_milestone = 0
        
        # Enregistrer les handlers d'événements
        self._register_handlers()
    
    def _register_handlers(self):
        """Enregistre tous les handlers d'événements TikTok"""
        
        @self.client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            """Appelé quand la connexion au live est établie"""
            print(f"✅ Connecté au live de @{event.unique_id}")
            print(f"👥 {event.viewer_count} viewers en ligne")
            print("🎮 L'aventure commence !")
        
        @self.client.on(GiftEvent)
        async def on_gift(event: GiftEvent):
            """
            Appelé quand un cadeau est reçu
            
            Déclenche un appel API pour générer une réaction de l'IA
            """
            # Récupérer les infos du cadeau
            username = event.user.unique_id
            gift_name = event.gift.name
            
            # Pour les cadeaux "streak" (combo), attendre la fin du combo
            if event.gift.streakable and not event.streaking:
                print(f"🎁 @{username} a envoyé {gift_name} x{event.repeat_count}")
                
                # Gérer chaque cadeau du combo
                for _ in range(event.repeat_count):
                    await self.game_engine.handle_gift(username, gift_name)
            
            elif not event.gift.streakable:
                # Cadeau simple (non-combo)
                print(f"🎁 @{username} a envoyé {gift_name}")
                await self. game_engine.handle_gift(username, gift_name)
        
        @self.client.on(LikeEvent)
        async def on_like(event: LikeEvent):
            """
            Appelé quand des likes sont reçus
            
            Traitement local (pas d'appel API) sauf pour les paliers spéciaux
            """
            like_count = event.count
            username = event.user.unique_id
            
            # Incrémenter les compteurs
            self.total_likes += like_count
            self.likes_since_last_milestone += like_count
            
            # Appliquer le soin passif pour chaque like
            for _ in range(like_count):
                await self.game_engine.handle_like()
            
            print(f"👍 @{username} a envoyé {like_count} like(s) (Total: {self.total_likes})")
            
            # Vérifier si on a atteint un palier
            if self.likes_since_last_milestone >= GameConfig.LIKE_THRESHOLD_FOR_REACTION:
                print(f"✨ Palier de likes atteint ! ({self.total_likes} likes au total)")
                await self.game_engine.handle_like_milestone(self.total_likes)
                self.likes_since_last_milestone = 0
        
        @self.client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            """
            Appelé quand un commentaire est posté
            
            Pour l'instant, juste un log. Peut être étendu plus tard.
            """
            username = event.user.unique_id
            comment = event.comment
            print(f"💬 @{username}: {comment}")
    
    async def start(self):
        """Démarre la connexion au live TikTok"""
        try:
            print(f"🔌 Connexion au live de @{TIKTOK_USERNAME}...")
            await self.client.connect()
        except Exception as e:
            print(f"❌ Erreur lors de la connexion TikTok: {e}")
            raise
    
    async def stop(self):
        """Arrête la connexion au live TikTok"""
        try:
            await self.client.disconnect()
            print("⏹️  Déconnecté du live TikTok")
        except Exception as e:
            print(f"⚠️  Erreur lors de la déconnexion: {e}")
