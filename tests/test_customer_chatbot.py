import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot_app import TrainTicketChatbotWithBooking

class TestCustomerChatbot(unittest.TestCase):
    def setUp(self):
        self.bot = TrainTicketChatbotWithBooking()

    def test_welcome_and_booking_intent(self):
        msg = "I want to book a train"
        response = self.bot.generate_response(msg)
        self.assertTrue("where are you travelling from" in response.lower() or "origin station" in response.lower())

    def test_unknown_intent(self):
        msg = "Do you believe in aliens?"
        response = self.bot.generate_response(msg)
        self.assertIn("sorry", response.lower())

    def test_delay_prediction_flow(self):
        msg = "Is there a delay from Norwich to London?"
        response = self.bot.generate_response(msg)
        self.assertTrue("delay" in response.lower() or "prediction" in response.lower() or "estimate" in response.lower())

    def test_station_fuzzy_matching(self):
        msg = "I want to go to Norw"
        response = self.bot.generate_response(msg)
        self.assertIn("did you mean", response.lower())

    def test_exit_intent(self):
        msg = "Thanks, bye"
        response = self.bot.generate_response(msg)
        self.assertIn("goodbye", response.lower())

if __name__ == '__main__':
    unittest.main()
