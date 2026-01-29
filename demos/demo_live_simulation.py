import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from multichannel.manager import run_multi_channel_qkd
from crypto.encryption import encrypt_message, decrypt_message
from stego.lsb import embed_data, extract_data


def slow_print(text, delay=0.7):
    print(text)
    time.sleep(delay)


print("\n" + "="*70)
print("   QUANTUM SECURE MULTI-LAYER COMMUNICATION SIMULATOR")
print("="*70)

slow_print("\n[STAGE 1] Initializing Quantum Communication Layer...")
slow_print("→ Using BB84 protocol")
slow_print("→ Enabling multi-channel transmission")
slow_print("→ Monitoring QBER for eavesdropping detection\n")

# -------------------------
# LAYER 1 + 2 : QUANTUM CORE
# -------------------------

result = run_multi_channel_qkd(
    n_channels=4,
    n_qubits=128,
    eve_probability=0.4,
    noise=0.02
)

slow_print("\n[STAGE 2] Multi-channel quantum transmission in progress...\n")

for ch in result["channels"]:
    slow_print(f"Channel {ch['channel_id']} | Eve present: {ch['eve']} | QBER: {round(float(ch['qber']),4)} | Accepted: {ch['accepted']}", 0.6)

if not result["success"]:
    slow_print("\n[SECURITY ALERT] All channels compromised.")
    slow_print("System aborted for security reasons.")
    exit()

slow_print(f"\n[STAGE 3] {result['valid_channel_count']} secure channel(s) detected.")
slow_print("→ Rejecting compromised channels")
slow_print("→ Performing XOR-based key fusion")

final_key = result["final_key"]
slow_print(f"→ Final quantum key generated (length = {len(final_key)} bits)\n")

# -------------------------
# LAYER 3A : ENCRYPTION
# -------------------------

slow_print("[STAGE 4] Classical encryption layer activated (AES-256)...")

message = "Quantum + Multi-channel + Steganography = Secure Communication"
slow_print("→ Original message:")
slow_print("  " + message)

encrypted = encrypt_message(message, final_key)
payload = encrypted["iv"] + encrypted["ciphertext"]

slow_print("→ Message encrypted using quantum-derived key")
slow_print(f"→ Ciphertext size: {len(payload)} bytes\n")

# -------------------------
# LAYER 3B : STEGANOGRAPHY
# -------------------------

slow_print("[STAGE 5] Covert communication layer activated (Steganography)...")
slow_print("→ Embedding encrypted message inside cover image")

embed_data("assets/cover.png", payload, "assets/stego.png")

slow_print("→ Stego image generated: assets/stego.png")
slow_print("→ Visually indistinguishable from original image\n")

# -------------------------
# RECEIVER SIDE
# -------------------------

slow_print("[STAGE 6] Receiver extracting hidden data from stego image...")

extracted = extract_data("assets/stego.png", len(payload))
iv = extracted[:16]
ciphertext = extracted[16:]

slow_print("→ Hidden encrypted payload successfully extracted")

decrypted = decrypt_message(ciphertext, iv, final_key)

slow_print("\n[STAGE 7] Decryption using shared quantum key...")
slow_print("→ Recovered message:")
slow_print("  " + decrypted)

print("\n" + "="*70)
print("   SIMULATION COMPLETE — SECURE COMMUNICATION ACHIEVED")
print("="*70)
