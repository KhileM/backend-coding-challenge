from flask import Blueprint, request, jsonify, abort
from app.utils.crypto import encrypt_message, decrypt_message
from app.config import MESSAGE_EXPIRY_SECONDS
from debug_code import broken_decrypt, fixed_decrypt
from app.utils.auth import token_required
import time
import logging

messages_bp = Blueprint('messages', __name__)
logger = logging.getLogger(__name__)

# In-memory storage
messages_storage = {}

@messages_bp.route('/messages', methods=['POST'])
@token_required
def store_message():
    data = request.get_json()
    user_id = data.get('userId')
    message = data.get('message')

    if not user_id or not message:
        abort(400, "Missing userId or message")

    encrypted = encrypt_message(message)
    messages_storage.setdefault(user_id, []).append({
        "encrypted": encrypted,
        "timestamp": time.time()
    })

    logger.info(f"Stored encrypted message for user: {user_id}")
    return jsonify({"status": "success", "encrypted": encrypted}), 201

@messages_bp.route('/messages/<user_id>', methods=['GET'])
@token_required
def get_messages(user_id):
    messages = messages_storage.get(user_id, [])
    now = time.time()
    valid_messages = []

    for msg in messages:
        if now - msg['timestamp'] <= MESSAGE_EXPIRY_SECONDS:
            try:
                plaintext = decrypt_message(msg['encrypted'])
                valid_messages.append({
                    "message": plaintext,
                    "encrypted": msg['encrypted']
                })
            except Exception as e:
                logger.warning(f"Failed to decrypt a message for user {user_id}: {str(e)}")

    # Cleans up expired messages
    messages_storage[user_id] = [msg for msg in messages if now - msg['timestamp'] <= MESSAGE_EXPIRY_SECONDS]

    return jsonify({"userId": user_id, "messages": valid_messages})

@messages_bp.route('/debug/decrypt', methods=['POST'])
def debug_decrypt():
    data = request.get_json()
    encrypted = data.get("encrypted")
    if not encrypted:
        abort(400, "Missing 'encrypted' payload")

    test_plaintext = "Debug test message"
    test_encrypted = encrypt_message(test_plaintext)

    try:
        broken = broken_decrypt(encrypted)
    except Exception as e:
        broken = f"broken_decrypt failed: {str(e)}"

    try:
        fixed = fixed_decrypt(encrypted)
    except Exception as e:
        fixed = f"fixed_decrypt failed: {str(e)}"

    return jsonify({
        "test_plaintext": test_plaintext,
        "test_encrypted": test_encrypted,
        "broken_result": broken,
        "fixed_result": fixed,
        "explanation": "The broken_decrypt used an incorrect IV length and missed padding. The fix uses a 16-byte IV and unpads correctly."
    })