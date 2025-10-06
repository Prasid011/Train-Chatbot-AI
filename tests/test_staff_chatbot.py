import unittest         # Build in modules for writing unit tests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #add to the system path so we can import staff_chatbot.py

from staff_chatbot import StaffChatbot

class TestStaffChatbot(unittest.TestCase):

    def setUp(self):
        self.bot = StaffChatbot()

    def test_end_intent(self):
        msg = "Thanks for your help!"
        response = self.bot.generate_response(msg)
        self.assertIn("Goodbye", response)

    def test_unknown_intent(self):
        msg = "Do you like pizza?"
        response = self.bot.generate_response(msg)
        self.assertIn("I’m here to help with train service disruptions", response)

    def test_blockage_intent_known_location(self):
        msg = "There's a disruption in Stratford"
        response = self.bot.generate_response(msg)
        self.assertTrue("Stratford" in response or "blockage" in response)

    def test_blockage_intent_unknown_location(self):
        msg = "There's an issue in Diss"
        response = self.bot.generate_response(msg)
        self.assertIn("Where is the disruption", response)

    def test_multiple_entries_needs_blockage_type(self):
        msg = "There’s a problem in Liverpool Street"
        response = self.bot.generate_response(msg)
        self.assertIn("partial", response.lower() or "full" in response.lower())

    def test_blockage_type_flow(self):
        self.bot.awaiting_blockage_type = True
        self.bot.last_entry_candidates = self.bot.extract_location("Norwich")
        response = self.bot.generate_response("partial")
        self.assertIn("Disruption at", response)

if __name__ == '__main__':
    unittest.main()
