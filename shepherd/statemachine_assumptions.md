## Assumptions
### Field Control UI / LCM
  - Match number should be passed into `setup_match()`
  - Needs a 'console' (or at least a textfield) to recieve debug broadcasts from Shepherd
  - 
  
### Timer
  - `reset()` should clear any settings previously saved (including time).
  - `start(int time)` should start the timer with the amount of time passed in (`time` can be in seconds for now).
  
### Driver Stations
  - `set_mode(String mode)` function handles 3 possible modes - `'NONE'`, `'AUTO'`, and `'TELOP'`.
    - `'NONE'` refers the state in between a game (before start/after end). Driver stations should just be disabled during this mode.

### Goal
  - string `alliance` class variable should either be `'blue'` or `'gold'`
  - int `goal_value` class variable should be the current value of the goal (base score x goal multiplier)

### Alliance (?)
 - Must have the scores at the end of each state stored (in order for `reset_stage()` to be able to rollback properly)
    - Doesn't necessarily have to be implemented in Alliance, just wherever convenient is fine.

### LCM
  - `reset_lcm()` method should be implemented.

### Scoreboard
  - Scoreboard constructor should take in a Timer() `match_timer`, and update the time as it ticks down accordingly.
  - `update_scores(int blue_score, int gold_score)` should update scoreboard with new scores.

### Schedule
  - `update_scores(int blue_score, int gold_score)` should update spreadsheet with new scores.
 