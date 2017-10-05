<<<<<<< HEAD

=======
>>>>>>> dbc40339de7b251e8d3934e835b81747112f4ec9
import sys
import Goal


class Shepherd:

    def __init__(self): # Don't think we need the matchNumber here.
        '''
        Initializes all of the state needed to maintain the current status of elements on the field
        '''

        #The following are elements that are expected to exist in every iteration of the game
        self.UI = UI()
        self.schedule = Web()
        self.match_timer = Timer()
        self.match_number = 1
        #teams = self.schedule.getTeams(matchNumber)
        #self.alliances = {'blue': Alliance(teams[0], teams[1]), 'gold': Alliance(teams[2], teams[3])}
        self.alliances = {}
        self.current_stage = 0

        #The follwing are elements that are configured
        # specifically for the 2018 year game - Solar Scramble
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
        self.score = {'blue': 0, 
                      'gold': 0}

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

        self.scoreboard = Scoreboard(match_timer) # what even is a scoreboard
        self.driverstation = Driverstation() # Make this into a wrapper class w/ the 4 diff driverstations?
        # TODO: Create driverstation wrapper class
    # UI Commands

    def setup_match(self, matchNumber):
        #Assuming the UI/ctrl station will provide us with a match number arg
        self.match_number = matchNumber
        teams = self.schedule.getTeams(self.match_number)
        self.alliances= {'blue': Alliance(teams[0], teams[1]), 'gold': Alliance(teams[2], teams[3])}
        self.current_stage = 'NONE'
        self.timer = Timer()
        self.score = {'blue': 0, 
                      'gold': 0}
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
        self.schedule.update_scores(self.score['blue'], self.score['gold'])
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
            #self.driverstation.blue.set_mode('AUTO')
        else if mode == "TELOP":
            #self.driverstation.blue.set_mode('TELOP')
        else:
            #self.driverstation.blue.set_mode('NONE')

    # Sensors
    def goal_scored(alliance, goal):
        # Look up pt value, add it using modify_pts
        goal_value = 2
        scored_goal = goals[goal]
        if scored_goal.alliance == alliance:
            modify_points(alliance, scored_goal.goal_value)

    # Because I think we may need a seperate method for teams' permenant
    # goals and bidding changes
    def modify_points(alliance, points):
        if (alliance == 'blue' || alliance == 'gold'):
            score[alliance] += points 
        self.scoreboard.update_scores(score['blue'], score['gold'])




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

<<<<<<< HEAD
def read_from_bidding(self, alliance_name, goal_name):

    lookup current bid on goal 
    lookup next value to bid on goal
    find the previous bidder 
    if alliance_name is the same as revious bidder or alliance_name money less than bid cost 
        can not bid 
    are they allowed to bid
        check they werent the last team to bid
        check do they have enough money
    store current bid to old bid field 
    store new bid into current bid field
    give back the number that is the current bid 

    self.alliances[alliance_name] 


def main():
    while True:
        msg = read()
        msg - > fn()
    shepherd = Shepherd(sys.argv[0])
    shepherd.waitGameStart()
    shepherd.autoLoop()
    shepherd.teleopLoop()
    shepherd.gameEnd()
    shepherd.exportScore(sys.argv[0])

if __name__ == '__main__':
    main()
=======
class PowerupTimer:
    def __init__(self):
        self.steal = Timer()
        self.double = Timer()    
        self.zero = Timer()

def main():
    shepherd = Shepherd()
    #uhhh

if __name__ == '__main__':
    main()

>>>>>>> dbc40339de7b251e8d3934e835b81747112f4ec9
