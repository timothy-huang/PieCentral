import unittest
import gspread, random
from Web import Web

test_client = Web()

class WebTests(unittest.TestCase):
    """
    (Pretty basic) unit tests for Web.py
    """

    def test_gspread(self):
        '''
        Tests gspread's built in get_all_records() function on our sheet
        '''
        print("Testing gspread")
        self.assertEqual(len(test_client.qual_matches.get_all_records()), 24)

    def test_getValueFromTitle(self):
        '''
        Tests for getValueFromTitle helper function.
        '''
        print("Testing getValueFromTitle")
        self.assertEqual(test_client.getValueFromTitle(test_client.qual_matches, "A", 'Blue2Name'), "De Anza HS")
        self.assertEqual(test_client.getValueFromTitle(test_client.qual_matches, 10, 'Gold1Name'), "De Anza HS")
        self.assertEqual(test_client.getValueFromTitle(test_client.elim_matches, "M", 'Gold2Name'), "Lighthouse Community")

    def test_getTeams(self):
        '''
        Tests for getTeams function.
        '''
        print("Testing getTeams")
        self.assertEqual([str(t) for t in test_client.getTeams(1)],
            ["Team 13: Head-Royce", "Team 3: De Anza HS", "Team 18: Aspire Cal Prep", "Team 27: San Lorenzo"])
        self.assertEqual([str(t) for t in test_client.getTeams('F', True)],
            ['Team 17: ACLC', 'Team 1: Albany HS', 'Team 18: Aspire Cal Prep', 'Team 15: Pinole Valley', 'Team 9: Hercules HS', 'Team 27: San Lorenzo'])

    def test_recordScore(self):
        '''
        Tests for recordScore function.
        '''
        print("Testing recordScore")

        test_b_score = random.randrange(0, 10)
        test_g_score = random.randrange(0, 10)

        # Store scores for Qual Match 2
        test_client.recordScore(2, test_b_score, test_g_score)
        self.assertEqual(test_client.getValueFromTitle(test_client.qual_matches, 2, 'BlueScore'), test_b_score)
        self.assertEqual(test_client.getValueFromTitle(test_client.qual_matches, 2, 'GoldScore'), test_g_score)

        # Store scores for Elim Match C
        test_client.recordScore('C', test_b_score, test_g_score, True)
        self.assertEqual(test_client.getValueFromTitle(test_client.elim_matches, 'C', 'BlueScore'), test_b_score)
        self.assertEqual(test_client.getValueFromTitle(test_client.elim_matches, 'C', 'GoldScore'), test_g_score)





if __name__ == '__main__':
    unittest.main()

