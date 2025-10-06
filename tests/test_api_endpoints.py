import unittest
import requests

class TestChatbotAPIs(unittest.TestCase):

    def test_customer_chat_api(self):
        msg = {"message": "I want to book a ticket"}
        response = requests.post("http://localhost:5001/chat", json=msg)
        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", response.json())
        print("Customer Bot:", response.json()["reply"])

    def test_staff_chat_api(self):
        msg = {"message": "Is there a blockage at Stratford?"}
        response = requests.post("http://localhost:5002/chat", json=msg)
        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", response.json())
        print("Staff Bot:", response.json()["reply"])

if __name__ == "__main__":
    unittest.main()
