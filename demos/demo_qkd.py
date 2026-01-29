import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.qkd import run_qkd_channel


print("=== Normal channel ===")
res = run_qkd_channel(n_qubits=128, eve=False, noise=0.01)
print(res)

print("\n=== Eve present ===")
res = run_qkd_channel(n_qubits=128, eve=True, noise=0.01)
print(res)
