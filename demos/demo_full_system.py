import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from multichannel.manager import run_multi_channel_qkd
from crypto.encryption import encrypt_message, decrypt_message
from stego.lsb import embed_data, extract_data

print("\n=== Quantum Secure Covert Communication Demo ===")

# Step 1: Quantum multi-channel key
result = run_multi_channel_qkd(
    n_channels=4,
    n_qubits=128,
    eve_probability=0.4,
    noise=0.02
)

if not result["success"]:
    print("System failed. No secure channel.")
    exit()

final_key = result["final_key"]
print("Quantum key established.")

# Step 2: Encrypt message
message = "Quantum + Multi-channel + Steganography = Secure Communication"
encrypted = encrypt_message(message, final_key)
payload = encrypted["iv"] + encrypted["ciphertext"]

# Step 3: Hide message
embed_data("assets/cover.png", payload, "assets/stego.png")
print("Encrypted message hidden inside image.")

# Step 4: Extract message
extracted = extract_data("assets/stego.png", len(payload))
iv = extracted[:16]
ciphertext = extracted[16:]

# Step 5: Decrypt
decrypted = decrypt_message(ciphertext, iv, final_key)
print("Recovered message:", decrypted)
