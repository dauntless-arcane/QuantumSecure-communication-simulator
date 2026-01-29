import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from multichannel.manager import run_multi_channel_qkd
from crypto.encryption import encrypt_message, decrypt_message


print("\n=== Running multi-channel QKD ===")

result = run_multi_channel_qkd(
    n_channels=4,
    n_qubits=128,
    eve_probability=0.5,
    noise=0.02
)

if not result["success"]:
    print("System failed. No secure key generated.")
    exit()

final_key = result["final_key"]
print("Final quantum key length:", len(final_key))


message = "Quantum secure communication achieved."

encrypted = encrypt_message(message, final_key)
decrypted = decrypt_message(
    encrypted["ciphertext"],
    encrypted["iv"],
    final_key
)

print("\nOriginal message :", message)
print("Decrypted message:", decrypted)
