"""
Test script pour vérifier le système de paliers de likes
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game_engine import GameEngine

async def test_like_milestones():
    print("=" * 60)
    print("🧪 TEST: Système de Paliers de Likes")
    print("=" * 60)
    
    game = GameEngine()
    
    # Reset total likes for clean test
    game.total_likes = 0
    
    # Spawn a monster
    await game.spawn_monster()
    print(f"\n👹 Monstre: {game.current_monster_name}")
    print(f"   HP Initial: {game.current_monster_hp}/{game.current_monster_max_hp}")
    print(f"   Likes: {game.total_likes}\n")
    
    # Test 1: 50 likes (pas de palier)
    print("📍 Test 1: 50 likes (pas de palier)")
    await game.handle_like(50)
    print(f"   Likes: {game.total_likes}/100")
    print(f"   HP Monstre: {game.current_monster_hp} (devrait être inchangé)")
    assert game.current_monster_hp == game.current_monster_max_hp, "❌ Le monstre ne devrait pas perdre de HP"
    print("   ✅ PASS\n")
    
    # Test 2: 50 likes de plus (franchit palier 100)
    print("📍 Test 2: +50 likes (franchit 100)")
    hp_before = game.current_monster_hp
    await game.handle_like(50)
    print(f"   Likes: {game.total_likes}/200")
    print(f"   HP Monstre: {hp_before} → {game.current_monster_hp}")
    assert game.current_monster_hp == hp_before - 10, "❌ Le monstre devrait perdre 10 HP"
    print("   ✅ PASS\n")
    
    # Test 3: 250 likes d'un coup (franchit 2 paliers: 200 et 300)
    print("📍 Test 3: +250 likes (franchit 2 paliers)")
    hp_before = game.current_monster_hp
    await game.handle_like(250)
    print(f"   Likes: {game.total_likes}/400")
    print(f"   HP Monstre: {hp_before} → {game.current_monster_hp}")
    assert game.current_monster_hp == hp_before - 20, "❌ Le monstre devrait perdre 20 HP (2 paliers)"
    print("   ✅ PASS\n")
    
    # Test 4: 45 likes (pas de nouveau palier)
    print("📍 Test 4: +45 likes (pas de nouveau palier)")
    hp_before = game.current_monster_hp
    await game.handle_like(45)
    print(f"   Likes: {game.total_likes}/400")
    print(f"   HP Monstre: {game.current_monster_hp} (devrait être inchangé)")
    assert game.current_monster_hp == hp_before, "❌ Le monstre ne devrait pas perdre de HP"
    print("   ✅ PASS\n")
    
    # Test 5: 5 likes de plus (franchit palier 400)
    print("📍 Test 5: +5 likes (franchit 400)")
    hp_before = game.current_monster_hp
    await game.handle_like(5)
    print(f"   Likes: {game.total_likes}/500")
    print(f"   HP Monstre: {hp_before} → {game.current_monster_hp}")
    assert game.current_monster_hp == hp_before - 10, "❌ Le monstre devrait perdre 10 HP"
    print("   ✅ PASS\n")
    
    print("=" * 60)
    print("🎉 TOUS LES TESTS RÉUSSIS !")
    print("=" * 60)
    print(f"\n📊 Stats finales:")
    print(f"   Total Likes: {game.total_likes}")
    print(f"   Paliers franchis: {game.total_likes // 100}")
    print(f"   Dégâts totaux: {(game.total_likes // 100) * 10} HP")
    print(f"   HP Monstre: {game.current_monster_hp}/{game.current_monster_max_hp}")

if __name__ == "__main__":
    asyncio.run(test_like_milestones())
