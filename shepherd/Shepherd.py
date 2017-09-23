import sys
import Goal


class Shepherd:

    def __init__(self, matchNumber):
        '''
        Initializes all of the state needed to maintain the current status of elements on the field
        '''

        #The following are elements that are expected to exist in every iteration of the game
        self.UI = UI()
        self.schedule = Web()
        self.match_timer = Timer()
        self.match_number = 1
        teams = self.schedule.getTeams(matchNumber)
        self.alliances= {'blue': Alliance(teams[0], teams[1]), 'gold': Alliance(teams[2], teams[3])}
        self.current_stage = 0

        #The follwing are elements that are configured
        specifically for the 2018 year game - Solar Scramble
        self.goals = {'a': Goal(),'b': Goal(),'c': Goal(),'d': Goal(),'e': Goal()}

        self.blue_powerup_timers = {'a': PowerupTimer(),
                                    'b': PowerupTimer(),
                                    'c': PowerupTimer(),
                                    'd': PowerupTimer(),
                                    'e': PowerupTimer()}
        self.gold_powerup_timers = {'a': PowerupTimer(),
                                    'b': PowerupTimer(),
                                    'c': PowerupTimer(),
                                    'd': PowerupTimer(),
                                    'e': PowerupTimer()}
        self.blue_decode_timers = PowerupTimer()
        self.gold_decode_timers = PowerupTimer()
        self.sensors = Sensors()

        self.event_mapping = {
            "setup_match": setup_match,
            "start_auto": start_auto,
            "start_telop": start_telop,
            "start_next_stage": start_next_stage,
            "reset_match": reset_match,
            "reset_stage": reset_stage,
            "reset_lcm": reset_lcm,
            "end_match": end_match,
        }

    def setup_match(self, matchNumber):
        #Assuming the UI/ctrl station will provide us with a match number arg
        self.match_number = matchNumber
        teams = self.schedule.getTeams(self.match_number)
        self.alliances= {'blue': Alliance(teams[0], teams[1]), 'gold': Alliance(teams[2], teams[3])}
        self.current_stage = 'NONE'
        self.timer = Timer()
        broadcast_status("Set up match #" + str(self.match_number))

    def start_auto(self):
        self.current_stage = 'AUTO'
        self.match_timer.reset()
        self.set_driver_stations_mode("AUTO")
        # assuming autonomous means we operate independently of the driver station
        broadcast_status("Starting autonomous")
        self.match_timer.start("AUTO_TIME")

    def start_telop(self):
        self.current_stage = 'TELOP'
        self.match_timer.reset()
        self.set_driver_stations_mode("TELOP")
        broadcast_status("Starting teleop")
        self.match_timer.start("TELOP_TIME")

    def start_next_stage(self):
        if self.current_stage == 'NONE':
            self.start_auto()
        else if self.current_stage == 'AUTO':
            self.start_telop()
        else:
            self.end_match()

    def end_match(self):
        self.current_stage = 'NONE'
        self.set_driver_stations_mode("NONE")
        broadcast_status("Ending match")
        # what else do we do?

    def reset_match(self):
        self.end_match()
        self.setup_match()

    def reset_stage(self):
        # probably need to reset score to prev state as well (rollback), something for the alliance to handle?
        # where do we even start

    def reset_lcm(self):
        # what happens here? can't we just force the lcm to do this itself?
        

    def set_driver_stations_mode(self, mode):
        if mode == "AUTO":
            
        else if mode == "TELOP":
            
        else:


    Things to receive:
        UI_Commands from field control:
            Setup_Match
            Start_Auto
            Start_Telop
            Start_Next_Stage #added
            Reset_Match
            Reset_Stage
            reset_lcm (optional)
            End_Match #added
        Button_Commands from bidding station:
            Bid on [Goal X] from [Alliance A]
        FromSensors:
            Ball scored in [Goal X] on [Alliance A]
            Code received from [Goal X] on [Alliance A]
        FromTimers:
            WhatTimerItIs, CurrentTimeReamining
            ChangeMatchState (for MatchTimers)
            ChangeGoalState (for GoalTimers)
            ChangeMultiplierState (for GoalMultipliers)
        FromDriverStation:
            Robot State (connected, disconnected, teleop, auto)

class PowerupTimer:
    def __init__(self):
        self.steal = Timer()
        self.double = Timer()    
        self.zero = Timer()

def main():
    shepherd = Shepherd()
    while True:




if __name__ == '__main__':
    main()

