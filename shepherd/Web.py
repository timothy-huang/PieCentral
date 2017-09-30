import gspread
from oauth2client.service_account import ServiceAccountCredentials
from Team import Team

class Web:
    '''
    Handles communication between Shepherd and the match Schedule
    '''
    def __init__(self):
        scoresheet_key = '15Ia6zIaYzzqpMw2kJRVD4cBPnOgXPfzFNd4GYrzIShU'
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        print('Authenticating')
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        print('Opening spreadsheet ' + scoresheet_key)
        self.client = gspread.authorize(creds)
        self.match_schedule = self.client.open_by_key(scoresheet_key)
        self.qual_matches = self.match_schedule.get_worksheet(0)
        self.elim_matches = self.match_schedule.get_worksheet(1)

    def get_value_from_title(self, worksheet, rowNumber, columnName):
        '''
        Helper method that returns the value of a cell specified by match number
        and column name.
        '''
        if (type(rowNumber) is str): # Convert letter to number
            rowNumber = ord(rowNumber.lower()) - 96

        row = worksheet.get_all_records()[rowNumber - 1]
        try:
            return row[columnName]
        except:
            print('Could not find ' + columnName + ", returning null")
            return None


    def get_teams(self, matchNumber, isElim = False):
        '''
        Returns a list where the first two elements are Team objects 
        which correspond to the blue alliance the the next two elements are
        Team objects corresponding to the gold alliance
        (Returns [Blue1, Blue2, Gold1, Gold2])
        INPUTS: matchNumber, isElim (toggles between qual (false) and elim (true) matches)
        '''
        ref_sheet = self.elim_matches if isElim else self.qual_matches
        blue1 = (Team(self.get_value_from_title(ref_sheet, matchNumber, 'Blue1Name'), 
                      self.get_value_from_title(ref_sheet, matchNumber, 'Blue1Number')))
        blue2 = (Team(self.get_value_from_title(ref_sheet, matchNumber, 'Blue2Name'), 
                      self.get_value_from_title(ref_sheet, matchNumber, 'Blue2Number')))
        gold1 = (Team(self.get_value_from_title(ref_sheet, matchNumber, 'Gold1Name'), 
                      self.get_value_from_title(ref_sheet, matchNumber, 'Gold1Number')))
        gold2 = (Team(self.get_value_from_title(ref_sheet, matchNumber, 'Gold2Name'), 
                      self.get_value_from_title(ref_sheet, matchNumber, 'Gold2Number')))
        if (isElim):
            blue3 = (Team(self.get_value_from_title(ref_sheet, matchNumber, 'Blue3Name'), 
                          self.get_value_from_title(ref_sheet, matchNumber, 'Blue3Number')))
            gold3 = (Team(self.get_value_from_title(ref_sheet, matchNumber, 'Gold3Name'), 
                          self.get_value_from_title(ref_sheet, matchNumber, 'Gold3Number')))

        return [blue1, blue2, blue3, gold1, gold2, gold3] if isElim else [blue1, blue2, gold1, gold2]

    def record_score(self, matchNumber, blueScore, goldScore, isElim = False):
        '''
        Records the spreadsheet to reflect the scores of the blue and gold alliance.
        Will be called once at the end of a match
        '''
        # In qual_matches, Blue and Gold score are cols 11 and 12 respectively.
        # In elim_matches, Blue and Gold score are cols 17 and 18 respectively.
        # It's jank but works I guess...
        if (isElim):
            ref_sheet = self.elim_matches
            blue_score_col = 17
            gold_score_col = 18
        else:
            ref_sheet = self.qual_matches
            blue_score_col = 11
            gold_score_col = 12

        if (type(matchNumber) is str): # Convert letter to number
            matchNumber = ord(matchNumber.lower()) - 96

        ref_sheet.update_cell(matchNumber + 1, blue_score_col, blueScore)
        ref_sheet.update_cell(matchNumber + 1, gold_score_col, goldScore)




