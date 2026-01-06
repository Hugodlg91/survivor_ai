"""
Stress Testing for Survivor AI
High-volume event simulation to test system stability
"""

import asyncio
import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game_engine import GameEngine

class StressTester:
    def __init__(self):
        self.game_engine = GameEngine()
        
    def get_resource_usage(self):
        """Get current resource info (simplified without psutil)"""
        return {
            "timestamp": time.time()
        }
    
    async def stress_test_likes(self, count=500):
        """Stress test: Process many likes"""
        print(f"\n🔥 Stress Test: {count} likes at once")
        
        start_time = time.time()
        
        await self.game_engine.spawn_monster()
        initial_hp = self.game_engine.current_monster_hp
        
        # Send massive like count
        await self.game_engine.handle_like(count)
        
        end_time = time.time()
        
        duration = end_time - start_time
        final_hp = self.game_engine.current_monster_hp
        
        print(f"  ⏱️  Duration: {duration:.3f}s")
        print(f"  ❤️  HP: {initial_hp} → {final_hp}")
        
        return duration < 1.0  # Should complete in under 1 second
    
    async def stress_test_gifts(self, count=50):
        """Stress test: Rapid gift processing"""
        print(f"\n🎁 Stress Test: {count} rapid gifts")
        
        start_time = time.time()
        
        for i in range(count):
            await self.game_engine.handle_gift("Rose", 1)
            if i % 10 == 0:
                print(f"  Progress: {i}/{count}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"  ⏱️  Total Duration: {duration:.2f}s")
        print(f"  ⚡ Avg per gift: {(duration/count*1000):.1f}ms")
        
        return True
    
    async def stress_test_monster_cycle(self, cycles=10):
        """Stress test: Rapid spawn/kill cycles"""
        print(f"\n👹 Stress Test: {cycles} spawn/kill cycles")
        
        start_time = time.time()
        
        for i in range(cycles):
            await self.game_engine.spawn_monster()
            damage = self.game_engine.current_monster_max_hp
            await self.game_engine.damage_monster(damage)
            
            if i % 5 == 0:
                print(f"  Cycle {i}/{cycles} complete")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"  ⏱️  Total Duration: {duration:.2f}s")
        print(f"  ⚡ Avg per cycle: {(duration/cycles):.2f}s")
        
        return True
    
    async def stress_test_long_duration(self, duration_minutes=5):
        """Stress test: Run for extended period"""
        print(f"\n⏰ Long Duration Test: {duration_minutes} minute(s)")
        print("  Processing random events continuously...")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        event_count = 0
        
        while time.time() < end_time:
            # Random event simulation
            import random
            event_type = random.choice(['like', 'gift', 'spawn'])
            
            if event_type == 'like':
                await self.game_engine.handle_like(random.randint(1, 20))
            elif event_type == 'gift':
                await self.game_engine.handle_gift("TestUser", "Rose")
            elif event_type == 'spawn':
                if self.game_engine.current_monster_hp <= 0:
                    await self.game_engine.spawn_monster()
            
            event_count += 1
            
            # Progress update every 100 events
            if event_count % 100 == 0:
                elapsed = time.time() - start_time
                remaining = end_time - time.time()
                print(f"  Events: {event_count} | Elapsed: {elapsed:.0f}s | Remaining: {remaining:.0f}s")
            
            await asyncio.sleep(0.1)  # Small delay
        
        print(f"\n  ✅ Test Complete!")
        print(f"  📊 Total Events Processed: {event_count}")
        
        return True
    
    async def run_all_stress_tests(self):
        """Run all stress tests"""
        print("=" * 60)
        print("🔥 STRESS TESTING - Survivor AI")
        print("=" * 60)
        
        results = []
        
        # Test 1: Massive likes
        result1 = await self.stress_test_likes(500)
        results.append(("500 Likes", result1))
        
        await asyncio.sleep(2)
        
        # Test 2: Rapid gifts
        result2 = await self.stress_test_gifts(50)
        results.append(("50 Rapid Gifts", result2))
        
        await asyncio.sleep(2)
        
        # Test 3: Monster cycles
        result3 = await self.stress_test_monster_cycle(10)
        results.append(("10 Monster Cycles", result3))
        
        print("\n" + "=" * 60)
        print("📊 STRESS TEST SUMMARY")
        print("=" * 60)
        
        for test_name, passed in results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} | {test_name}")
        
        passed_count = sum(1 for _, p in results if p)
        total_count = len(results)
        
        print(f"\nPassed: {passed_count}/{total_count}")
        
        if passed_count == total_count:
            print("\n🎉 ALL STRESS TESTS PASSED!")
        else:
            print("\n⚠️ SOME STRESS TESTS FAILED")

if __name__ == "__main__":
    tester = StressTester()
    
    # Check if long duration test is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--long":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        asyncio.run(tester.stress_test_long_duration(duration))
    else:
        asyncio.run(tester.run_all_stress_tests())
