# Shepherd API

## Constants
#### shepherd.py
  * `GOAL_SCORE`: string `goal` (?)
  * `GOAL_BID`: string `goal`, Alliance `alliance`, int `bid`
  * `CODE_INPUT`:  string `input`

  * Shepherd will receive certain headers from the UI, setting off certain events in the game:
     * `SETUP_MATCH`: int `match_number`
     * `SETUP_MATCH_MANUAL`: int `match_number`, string `team_blue_1`, string `team_blue_2`, string `team_gold_1`, string `team_gold_1`
     * `START_MATCH`
       * (just fires `START_AUTO` ¯\_(ツ)_/¯)
       * `START_AUTO`
       * `START_TELOP`
       * `END_MATCH`
     * `START_NEXT_STAGE`: string `current_stage` 
       * (in the form of AUTO, TELOP, END)
     * `RESET_CURRENT_STAGE`
     * `RESET_MATCH` 
       * (just calls ‘END_MATCH’, then  ‘START_MATCH’)
  
  * `BID_TIMER_END` string `goal`
  * `STAGE_TIMER_END`

#### sensors.py
  * `CODE_RESULT`
  * `FAILED_POWERUP`
  * `CURRENT_BID`: int `bid_value`


#### scoreboard
  * `SCORE`: int `blue_score`, int `gold_score`
  * `TEAMS`: string `blue_team_1`, string `blue_team_2`, string `gold_team_1`, string `gold_team_2`
  * `BID_TIMER_START` string `goal`
  * `BID_AMOUNT` string `goal`, string `alliance_name`, int `bid`
  * `BID_WIN`: string `goal`, string `winning_alliance`
  * `STAGE`: string `current_stage`
     * (in the form of AUTO, TELOP, END)
  * `STAGE_TIMER_START`
  * `POWERUPS`: string `goal` string `alliance` 
  * `ALLIANCE_MULTIPLIER`: int ‘multiplier’

## Methods
`todo`
