"""Debug script to test API key encryption and usage"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from utils.auth_manager import AuthManager
from utils.rag_manager import RAGManager
from openai import OpenAI

# Your new API key
test_api_key = "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"

print("=" * 60)
print("TESTING API KEY ENCRYPTION/DECRYPTION")
print("=" * 60)

# Initialize managers
rag_manager = RAGManager()
auth_manager = AuthManager(rag_manager)

# Test encryption
print(f"\n1. Original API key: {test_api_key[:20]}...")
encrypted = auth_manager.encrypt_api_key(test_api_key)
print(f"2. Encrypted: {encrypted[:30]}...")

# Test decryption
decrypted = auth_manager.decrypt_api_key(encrypted)
print(f"3. Decrypted: {decrypted[:20]}...")

if decrypted == test_api_key:
    print("✅ Encryption/Decryption works correctly!")
else:
    print("❌ Encryption/Decryption FAILED!")
    sys.exit(1)

# Test API key with OpenRouter
print("\n" + "=" * 60)
print("TESTING API KEY WITH OPENROUTER")
print("=" * 60)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=decrypted
)

try:
    response = client.chat.completions.create(
        model="anthropic/claude-3-haiku",
        messages=[
            {"role": "user", "content": "Say 'API key works!' if you can read this"}
        ],
        max_tokens=50
    )
    
    print(f"✅ API Key Works!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ API Key Failed: {str(e)}")
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED! ✅")
print("=" * 60)
