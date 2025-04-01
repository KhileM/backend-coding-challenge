import unittest
import json
from app import create_app
from app.utils.crypto import encrypt_message, decrypt_message
from debug_code import fixed_decrypt

class MessagingApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.user_id = "user123"
        self.token = "token123"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def test_encryption_roundtrip(self):
        original = "Hello, world!"
        encrypted = encrypt_message(original)
        decrypted = decrypt_message(encrypted)
        self.assertEqual(original, decrypted)

    def test_store_and_get_message(self):
        msg = {"userId": self.user_id, "message": "Test message!"}
        post = self.app.post("/messages", headers=self.headers, data=json.dumps(msg))
        self.assertEqual(post.status_code, 201)

        get = self.app.get(f"/messages/{self.user_id}", headers=self.headers)
        self.assertEqual(get.status_code, 200)
        data = get.get_json()
        self.assertEqual(data["userId"], self.user_id)
        self.assertTrue(any(m["message"] == "Test message!" for m in data["messages"]))

    def test_debug_decrypt_endpoint(self):
        msg = {"userId": self.user_id, "message": "Decrypt test!"}
        post = self.app.post("/messages", headers=self.headers, data=json.dumps(msg))
        encrypted = post.get_json()["encrypted"]

        response = self.app.post("/debug/decrypt", headers=self.headers, data=json.dumps({
            "encrypted": encrypted
        }))
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["fixed_result"], "Decrypt test!")

if __name__ == "__main__":
    unittest
