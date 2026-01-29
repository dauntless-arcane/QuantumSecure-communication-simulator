import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from metrics.quantum_metrics import ber_vs_noise

noise_levels = [0, 0.01, 0.02, 0.05, 0.1]
results = ber_vs_noise(noise_levels, runs=30)

print("\n=== BER (QBER) vs Noise ===")
for k, v in results.items():
    print(f"Noise {k}: Mean QBER = {v}")
