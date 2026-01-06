
import asyncio
import random
from src.game_engine import GameEngine

async def main():
    print("🧪 DEBUG MODE - Monster Damage")
    game = GameEngine()
    task = asyncio.create_task(game.start())
    await asyncio.sleep(2)

    # Ensure monster exists
    if game.current_monster_hp <= 0:
        await game.spawn_monster()
    
    print(f"👹 Monster: {game.current_monster_name} (HP: {game.current_monster_hp}/{game.current_monster_max_hp})")

    # Deal lethal damage in steps (target > 120 HP)
    damage_steps = 15
    damage_per_step = 1 # 1 like = 10 dmg (Total 150 dmg)
    
    for i in range(damage_steps):
        print(f"💥 Damage Step {i+1}/{damage_steps}...")
        await game.handle_like(damage_per_step)
        print(f"   Current HP: {game.current_monster_hp}")
        
        # Stop if dead
        if game.current_monster_hp <= 0:
            print("💀 Monster Dead!")
            break
            
        await asyncio.sleep(1.5) # Wait 1.5s between hits to see UI update

    print("🏁 Debug finished")
    game.stop()
    task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
