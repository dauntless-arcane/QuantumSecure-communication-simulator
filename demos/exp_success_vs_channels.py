import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from metrics.quantum_metrics import success_rate_vs_channels

channels = [1, 2, 3, 4, 5, 6]
results = success_rate_vs_channels(channels, runs=30)

print("\n=== System Success Rate vs Channels ===")
for k, v in results.items():
    print(f"{k} channels: success rate = {v}")
