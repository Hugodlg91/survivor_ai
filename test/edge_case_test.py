"""
Edge Case Testing for Survivor AI
Tests boundary conditions and unusual scenarios
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game_engine import GameEngine
import json

class EdgeCaseTester:
    def __init__(self):
        self.game_engine = GameEngine()
        self.results = []
        
    def log_result(self, test_name, passed, details=""):
        status = "✅ PASS" if passed else "❌ FAIL"
        result = f"{status} | {test_name}"
        if details:
            result += f" | {details}"
        print(result)
        self.results.append({
            "test": test_name,
            "passed": passed,
            "details": details
        })
    
    async def test_player_hp_zero(self):
        """Test: Player HP at 0"""
        print("\n🧪 Test: Player HP = 0")
        self.game_engine.character.hp = 0
        self.game_engine._write_stats()
        
        with open('obs_files/game_state.json', 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        passed = state['hp'] == 0
        self.log_result("Player HP = 0", passed, f"HP in JSON: {state['hp']}")
        
    async def test_monster_hp_negative(self):
        """Test: Monster HP goes negative (should clamp to 0)"""
        print("\n🧪 Test: Monster HP negative clamping")
        await self.game_engine.spawn_monster()
        await self.game_engine.damage_monster(999999)
        
        passed = self.game_engine.current_monster_hp == 0
        self.log_result("Monster HP clamping", passed, 
                       f"HP after massive damage: {self.game_engine.current_monster_hp}")
    
    async def test_likes_no_monster(self):
        """Test: Likes received when no monster exists"""
        print("\n🧪 Test: Likes with no monster")
        self.game_engine.current_monster_hp = 0
        self.game_engine.current_monster_name = None
        
        try:
            await self.game_engine.handle_like(10)
            passed = True
            details = "No crash"
        except Exception as e:
            passed = False
            details = f"Exception: {e}"
        
        self.log_result("Likes without monster", passed, details)
    
    async def test_multiple_spawns(self):
        """Test: Multiple monster spawns in succession"""
        print("\n🧪 Test: Multiple consecutive spawns")
        
        names = []
        for i in range(3):
            await self.game_engine.spawn_monster()
            names.append(self.game_engine.current_monster_name)
            await self.game_engine.damage_monster(self.game_engine.current_monster_max_hp)
            await asyncio.sleep(0.5)
        
        passed = len(set(names)) >= 2  # At least 2 different names
        self.log_result("Multiple spawns", passed, f"Names: {names}")
    
    async def test_gift_double_spawn(self):
        """Test: Gift while monster is alive (should not double spawn)"""
        print("\n🧪 Test: Gift while monster alive")
        
        await self.game_engine.spawn_monster()
        first_name = self.game_engine.current_monster_name
        
        await self.game_engine.handle_gift("TestUser", "Rose")
        second_name = self.game_engine.current_monster_name
        
        passed = first_name == second_name
        self.log_result("No double spawn", passed, 
                       f"First: {first_name}, Second: {second_name}")
    
    async def test_xp_overflow(self):
        """Test: XP overflow on level up"""
        print("\n🧪 Test: XP overflow handling")
        
        self.game_engine.character.xp = 95
        initial_level = self.game_engine.character.level
        
        self.game_engine.character.add_xp(120)  # Should level up + 15 XP overflow
        
        leveled_up = self.game_engine.character.level > initial_level
        has_overflow = self.game_engine.character.xp > 0
        
        passed = leveled_up and has_overflow
        self.log_result("XP overflow", passed, 
                       f"Level: {self.game_engine.character.level}, Overflow XP: {self.game_engine.character.xp}")
    
    async def test_massive_like_batch(self):
        """Test: Processing 1000 likes at once"""
        print("\n🧪 Test: Massive like batch (1000)")
        
        await self.game_engine.spawn_monster()
        initial_hp = self.game_engine.current_monster_hp
        
        try:
            await self.game_engine.handle_like(1000)
            passed = True
            final_hp = self.game_engine.current_monster_hp
            details = f"HP: {initial_hp} → {final_hp}"
        except Exception as e:
            passed = False
            details = f"Exception: {e}"
        
        self.log_result("Massive like batch", passed, details)
    
    async def test_ollama_fallback(self):
        """Test: Ollama fallback name on API failure"""
        print("\n🧪 Test: Ollama fallback mechanism")
        
        # Force invalid URL by temporarily modifying config
        import src.config as config
        original_url = config.OLLAMA_API_URL
        config.OLLAMA_API_URL = "http://invalid-url:9999/api/generate"
        
        await self.game_engine.generate_monster_name()
        
        # Restore URL
        config.OLLAMA_API_URL = original_url
        
        # Check if fallback name was used
        fallback_names = ["Ombre Menaçante", "La Bête"]
        passed = self.game_engine.current_monster_name in fallback_names
        
        self.log_result("Ollama fallback", passed, 
                       f"Name generated: {self.game_engine.current_monster_name}")
    
    async def run_all_tests(self):
        """Run all edge case tests"""
        print("=" * 60)
        print("🧪 EDGE CASE TESTING - Survivor AI")
        print("=" * 60)
        
        await self.test_player_hp_zero()
        await self.test_monster_hp_negative()
        await self.test_likes_no_monster()
        await self.test_multiple_spawns()
        await self.test_gift_double_spawn()
        await self.test_xp_overflow()
        await self.test_massive_like_batch()
        await self.test_ollama_fallback()
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r['passed'])
        total = len(self.results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED!")
        else:
            print("\n⚠️ SOME TESTS FAILED - Review results above")

if __name__ == "__main__":
    tester = EdgeCaseTester()
    asyncio.run(tester.run_all_tests())
