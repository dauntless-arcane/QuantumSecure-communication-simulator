# experiments/run_all_experiments_quick.py
# Fast version for testing - minimal runs

import sys, os, csv
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt

from metrics.quantum_metrics import qber_vs_eve, ber_vs_noise, success_rate_vs_channels
from metrics.image_metrics import evaluate_images

OUTPUT_DIR = "outputs_quick"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# 1. QBER vs Eve Probability
# -----------------------------
print("[1/4] Running QBER vs Eve probability experiment...")

eve_probs = [0, 0.5, 1.0]  # Reduced data points
qber_eve = qber_vs_eve(eve_probs, runs=3, n_qubits=32)  # Reduced runs and qubits

with open(f"{OUTPUT_DIR}/qber_vs_eve.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Eve Probability", "Mean QBER"])
    for k, v in qber_eve.items():
        writer.writerow([k, v])

plt.figure()
plt.plot(list(qber_eve.keys()), list(qber_eve.values()), marker='o')
plt.xlabel("Eve Probability")
plt.ylabel("Mean QBER")
plt.title("QBER vs Eve Probability (Quick Test)")
plt.grid()
plt.savefig(f"{OUTPUT_DIR}/qber_vs_eve.png", dpi=150)  # Lower DPI
plt.close()


# -----------------------------
# 2. QBER vs Noise
# -----------------------------
print("[2/4] Running QBER vs noise experiment...")

noise_levels = [0, 0.05, 0.1]  # Reduced data points
qber_noise = ber_vs_noise(noise_levels, runs=3, n_qubits=32)

with open(f"{OUTPUT_DIR}/qber_vs_noise.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Noise", "Mean QBER"])
    for k, v in qber_noise.items():
        writer.writerow([k, v])

plt.figure()
plt.plot(list(qber_noise.keys()), list(qber_noise.values()), marker='o')
plt.xlabel("Noise Level")
plt.ylabel("Mean QBER")
plt.title("QBER vs Noise (Quick Test)")
plt.grid()
plt.savefig(f"{OUTPUT_DIR}/qber_vs_noise.png", dpi=150)
plt.close()


# -----------------------------
# 3. Success rate vs channels
# -----------------------------
print("[3/4] Running system success vs channels experiment...")

channels = [1, 3, 5]  # Reduced data points
success_rates = success_rate_vs_channels(channels, runs=3)

with open(f"{OUTPUT_DIR}/success_vs_channels.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Channels", "Success Rate"])
    for k, v in success_rates.items():
        writer.writerow([k, v])

plt.figure()
plt.plot(list(success_rates.keys()), list(success_rates.values()), marker='o')
plt.xlabel("Number of Channels")
plt.ylabel("System Success Rate")
plt.title("System Success Rate vs Channels (Quick Test)")
plt.grid()
plt.savefig(f"{OUTPUT_DIR}/success_vs_channels.png", dpi=150)
plt.close()


# -----------------------------
# 4. Steganography image metrics
# -----------------------------
print("[4/4] Evaluating steganography quality...")

img_metrics = evaluate_images("assets/cover.png", "assets/stego.png")

with open(f"{OUTPUT_DIR}/stego_metrics.txt", "w") as f:
    for k, v in img_metrics.items():
        f.write(f"{k}: {v}\n")

print("\n=== ALL EXPERIMENTS COMPLETED (QUICK MODE) ===")
print("Results saved in /outputs folder.")
print("Note: This is a quick test version with reduced runs for faster execution.")