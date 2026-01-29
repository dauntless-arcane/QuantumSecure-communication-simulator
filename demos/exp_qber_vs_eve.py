import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from metrics.quantum_metrics import qber_vs_eve

eve_probs = [0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
results = qber_vs_eve(eve_probs, runs=30)

print("\n=== QBER vs Eve Probability ===")
for k, v in results.items():
    print(f"Eve probability {k}: Mean QBER = {v}")
