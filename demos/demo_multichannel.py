import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from multichannel.manager import run_multi_channel_qkd

result = run_multi_channel_qkd(
    n_channels=4,
    n_qubits=128,
    eve_probability=0.4,
    noise=0.02
)

print("\n=== MULTI-CHANNEL REPORT ===")

for ch in result["channels"]:
    print(ch)

if result["success"]:
    print("\nFinal key length:", result["final_key_length"])
else:
    print("\nSystem failed:", result["reason"])
