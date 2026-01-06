"""
Test du système d'attaques automatiques du monstre
"""

import asyncio
import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game_engine import GameEngine

async def test_monster_attacks():
    print("=" * 70)
    print("🧪 TEST: Attaques Automatiques du Monstre")
    print("=" * 70)
    
    game = GameEngine()
    
    # Spawn un monstre
    await game.spawn_monster()
    print(f"\n👹 Monstre: {game.current_monster_name}")
    print(f"   HP: {game.current_monster_hp}/{game.current_monster_max_hp}")
    print(f"   Joueur HP: {game.character.hp}/{game.character.max_hp}")
    
    # Simuler le jeu pendant 35 secondes pour voir 3 attaques
    print("\n⏳ Simulation de 35 secondes (3 attaques attendues)...")
    print("   Intervalle d'attaque: 10 secondes")
    print("   Dégâts par attaque: 25 HP")
    
    # Lancer les boucles de jeu
    game.is_running = True
    attack_task = asyncio.create_task(game._monster_attack_loop())
    
    # Attendre et observer
    for i in range(7):  # 7 x 5s = 35s
        await asyncio.sleep(5)
        print(f"   [{i*5}s] Joueur HP: {game.character.hp}/{game.character.max_hp}")
    
    # Arrêter
    game.is_running = False
    attack_task.cancel()
    
    try:
        await attack_task
    except asyncio.CancelledError:
        pass
    
    print("\n📊 Résultat:")
    print(f"   HP Final: {game.character.hp}/{game.character.max_hp}")
    print(f"   HP Perdus: {game.character.max_hp - game.character.hp}")
    print(f"   Attaques Attendues: 3 (à 10s, 20s, 30s)")
    print(f"   Dégâts Attendus: 75 HP")
    
    if game.character.max_hp - game.character.hp == 75:
        print("\n✅ TEST RÉUSSI ! Le monstre attaque correctement.")
    else:
        print(f"\n⚠️ Dégâts incorrects: attendu 75, reçu {game.character.max_hp - game.character.hp}")

if __name__ == "__main__":
    asyncio.run(test_monster_attacks())
