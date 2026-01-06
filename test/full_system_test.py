"""
Test Complet - Survivor AI
Teste TOUTES les fonctionnalités du système
"""

import asyncio
import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game_engine import GameEngine

async def full_system_test():
    print("=" * 70)
    print("🧪 TEST COMPLET - SURVIVOR AI")
    print("=" * 70)
    
    game = GameEngine()
    game.total_likes = 0  # Reset pour test propre
    
    print("\n📍 Phase 1: Test Système de Likes (Paliers)")
    print("-" * 70)
    
    # Test 1.1: 50 likes (pas de dégâts)
    print("1.1 - Envoyer 50 likes (pas de palier)")
    hp_before = game.character.hp
    await game.handle_like(50)
    assert game.total_likes == 50, "❌ Compteur likes incorrect"
    expected_hp = min(hp_before + 50, game.character.max_hp)  # Cap at max HP
    assert game.character.hp == expected_hp, f"❌ Heal incorrect: {game.character.hp} vs {expected_hp}"
    print(f"   ✅ Likes: {game.total_likes}, HP Joueur: {game.character.hp}/{game.character.max_hp}")
    
    # Test 1.2: 50 likes de plus (franchit 100)
    print("1.2 - Envoyer 50 likes de plus (franchit palier 100)")
    await game.spawn_monster()
    initial_monster_hp = game.current_monster_hp
    await game.handle_like(50)
    assert game.total_likes == 100, "❌ Compteur likes incorrect"
    assert game.current_monster_hp == initial_monster_hp - 10, "❌ Dégâts pas appliqués"
    print(f"   ✅ Monstre HP: {initial_monster_hp} → {game.current_monster_hp}")
    
    # Test 1.3: 200 likes d'un coup (2 paliers)
    print("1.3 - Envoyer 200 likes d'un coup (2 paliers)")
    hp_before = game.current_monster_hp
    await game.handle_like(200)
    assert game.current_monster_hp == hp_before - 20, "❌ Multi-paliers incorrect"
    print(f"   ✅ Monstre HP: {hp_before} → {game.current_monster_hp} (-20 pour 2 paliers)")
    
    print("\n📍 Phase 2: Test Système de Cadeaux")
    print("-" * 70)
    
    # Test 2.0: Perdre du HP d'abord pour pouvoir tester le heal
    print("2.0 - Perdre HP pour tester le heal")
    game.character.remove_hp(50)
    print(f"  HP réduit à: {game.character.hp}/{game.character.max_hp}")
    
    # Test 2.1: Cadeau Rose (HP + XP)
    print("2.1 - Recevoir cadeau 'Rose'")
    hp_before = game.character.hp
    xp_before = game.character.xp
    await game.handle_gift("TestUser", "Rose")
    assert game.character.hp >= hp_before, f"❌ HP pas gagné: {hp_before} → {game.character.hp}"
    assert game.character.xp > xp_before, "❌ XP pas gagné"
    print(f"   ✅ HP: {hp_before} → {game.character.hp} (+{game.character.hp - hp_before})")
    print(f"   ✅ XP: {xp_before} → {game.character.xp} (+{game.character.xp - xp_before})")
    
    # Test 2.2: Cadeau épique Lion (gros gains)
    print("2.2 - Recevoir cadeau épique 'Lion'")
    hp_before = game.character.hp
    xp_before = game.character.xp
    await game.handle_gift("VIPUser", "Lion")
    print(f"   ✅ HP: {hp_before} → {game.character.hp} (+{game.character.hp - hp_before})")
    print(f"   ✅ XP: {xp_before} → {game.character.xp} (+{game.character.xp - xp_before})")
    
    print("\n📍 Phase 3: Test Consommation d'Objets")
    print("-" * 70)
    
    # Test 3.1: Vérifier que les objets sont consommés
    print("3.1 - Vérifier liste des objets récents")
    assert len(game.character.recent_items) <= 3, "❌ Limite de 3 objets dépassée"
    print(f"   ✅ Objets récents ({len(game.character.recent_items)}): {game.character.recent_items}")
    
    # Test 3.2: Envoyer 5 cadeaux, vérifier FIFO
    print("3.2 - Envoyer 5 cadeaux (test FIFO)")
    for i, gift in enumerate(["Rose", "Heart", "Perfume", "Swan", "Lion"]):
        await game.handle_gift(f"User{i}", gift)
    assert len(game.character.recent_items) == 3, "❌ Devrait y avoir 3 objets max"
    assert "Rose" not in game.character.recent_items, "❌ Rose devrait être supprimé (FIFO)"
    print(f"   ✅ Derniers 3 objets: {game.character.recent_items}")
    
    print("\n📍 Phase 4: Test Cycle de Vie du Monstre")
    print("-" * 70)
    
    # Test 4.1: Spawn monstre
    print("4.1 - Spawn nouveau monstre")
    await game.spawn_monster()
    assert game.current_monster_hp > 0, "❌ Monstre pas spawn"
    assert game.current_monster_name is not None, "❌ Monstre sans nom"
    print(f"   ✅ Monstre: {game.current_monster_name} ({game.current_monster_hp}/{game.current_monster_max_hp} HP)")
    
    # Test 4.2: Dommage monstre
    print("4.2 - Infliger dégâts au monstre")
    hp_before = game.current_monster_hp
    await game.damage_monster(30)
    assert game.current_monster_hp == hp_before - 30, "❌ Dégâts incorrects"
    print(f"   ✅ HP Monstre: {hp_before} → {game.current_monster_hp}")
    
    # Test 4.3: Tuer monstre
    print("4.3 - Tuer le monstre")
    xp_before = game.character.xp
    await game.damage_monster(game.current_monster_hp)
    assert game.current_monster_hp == 0, "❌ Monstre devrait être mort"
    assert game.character.xp > xp_before, "❌ XP bonus pas reçu"
    print(f"   ✅ Monstre vaincu ! Bonus XP: +{game.character.xp - xp_before}")
    
    print("\n📍 Phase 5: Test Level Up")
    print("-" * 70)
    
    # Test 5.1: Forcer level up
    print("5.1 - Forcer level up en donnant assez d'XP")
    game.character.xp = 95  # Proche du seuil
    level_before = game.character.level
    max_hp_before = game.character.max_hp
    game.character.add_xp(20)  # Dépasse le seuil de 100
    assert game.character.level == level_before + 1, "❌ Level pas augmenté"
    assert game.character.max_hp == max_hp_before + 10, "❌ Max HP pas augmenté"
    assert game.character.hp == game.character.max_hp, "❌ HP pas restauré"
    print(f"   ✅ Level Up ! {level_before} → {game.character.level}")
    print(f"   ✅ Max HP: {max_hp_before} → {game.character.max_hp}")
    print(f"   ✅ HP restauré à {game.character.hp}")
    
    print("\n📍 Phase 6: Test JSON State")
    print("-" * 70)
    
    # Test 6.1: Vérifier état JSON
    print("6.1 - Vérifier game_state.json")
    with open('obs_files/game_state.json', 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    assert 'hp' in state, "❌ HP manquant dans JSON"
    assert 'xp' in state, "❌ XP manquant dans JSON"
    assert 'level' in state, "❌ Level manquant dans JSON"
    assert 'recent_items' in state, "❌ recent_items manquant dans JSON"
    assert 'total_likes' in state, "❌ total_likes manquant dans JSON"
    assert 'likes_to_next_milestone' in state, "❌ likes_to_next_milestone manquant dans JSON"
    assert 'monster' in state, "❌ monster manquant dans JSON"
    
    print(f"   ✅ HP: {state['hp']}/{state['max_hp']}")
    print(f"   ✅ XP: {state['xp']}/{state['xp_for_next_level']}")
    print(f"   ✅ Level: {state['level']}")
    print(f"   ✅ Likes: {state['total_likes']} (prochain palier: {state['likes_to_next_milestone']})")
    print(f"   ✅ Objets récents: {state['recent_items']}")
    if state['monster']:
        print(f"   ✅ Monstre: {state['monster']['name']} ({state['monster']['hp']}/{state['monster']['max_hp']})")
    
    print("\n" + "=" * 70)
    print("🎉 TOUS LES TESTS RÉUSSIS !")
    print("=" * 70)
    
    print("\n📊 Résumé Final:")
    print(f"   Joueur: Niveau {game.character.level}, {game.character.hp}/{game.character.max_hp} HP, {game.character.xp} XP")
    print(f"   Likes Totaux: {game.total_likes} (paliers franchis: {game.total_likes // 100})")
    print(f"   Objets Récents: {game.character.recent_items}")
    if game.current_monster_hp > 0:
        print(f"   Monstre Actif: {game.current_monster_name} ({game.current_monster_hp}/{game.current_monster_max_hp} HP)")
    else:
        print(f"   Aucun monstre actif")

if __name__ == "__main__":
    asyncio.run(full_system_test())
