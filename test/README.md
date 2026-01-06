# Test Suite for Survivor AI

This directory contains all testing and debugging scripts for the Survivor AI project.

## Test Files

### Edge Case Testing
- **`edge_case_test.py`** - Tests boundary conditions and unusual scenarios
  - Player HP at 0
  - Monster HP negative clamping
  - Likes without active monster
  - Multiple consecutive spawns
  - Gift while monster alive (no double spawn)
  - XP overflow on level up
  - Massive like batches
  - Ollama API fallback

### Stress Testing
- **`stress_test.py`** - High-volume event simulation
  - 500 likes at once
  - 50 rapid gifts
  - 10 monster spawn/kill cycles
  - Optional long-duration test (use `--long` flag)

### Simulation Scripts
- **`test_simulation.py`** - General event simulator for development testing
  - Simulates gifts, likes, comments
  - Predefined test scenarios
  
- **`debug_simulation.py`** - Controlled monster damage testing
  - Gradual damage application for visual verification
  - Useful for testing HP bar animations

## Running Tests

```bash
# Edge case tests
python test/edge_case_test.py

# Stress tests (quick)
python test/stress_test.py

# Stress test (long duration - 5 minutes by default)
python test/stress_test.py --long 5

# Development simulation
python test/test_simulation.py

# Debug monster display
python test/debug_simulation.py
```

## Test Results Summary

### Edge Case Tests
- **7/8 tests passing (87.5%)**
- Fixed bugs:
  - Inventory TypeError (integers vs strings) ✅
  - Attribute naming issues ✅
- Known issue:
  - Ollama fallback test (timeout allows connection despite invalid URL)

### Stress Tests
- **2/3 tests passing**
- 500 likes: Slower than expected (2.3s vs 1.0s target)
- 50 rapid gifts: ✅ ~48ms per gift
- 10 monster cycles: ✅ ~2.09s per cycle

## Bug Fixes Applied

1. **Inventory Display Bug**: Fixed `TypeError` when inventory contains integers by converting all items to strings in `get_stats_text()`
2. **Attribute Names**: Corrected `current_hp` → `hp` and `current_xp` → `xp` in test scripts
3. **Gift Parameters**: Fixed `handle_gift()` calls to use correct parameter order (username, gift_name)
