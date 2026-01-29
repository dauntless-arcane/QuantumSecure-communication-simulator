# multichannel/manager.py

import numpy as np
import random
from core.qkd import run_qkd_channel

print("Multi-channel QKD manager module loaded.")
print("You can run multi-channel QKD simulations with specified parameters.")
def xor_keys(keys):
    """
    XOR all valid keys (trim to shortest length)
    """
    min_len = min(len(k) for k in keys)
    trimmed = [k[:min_len] for k in keys]

    final_key = trimmed[0].copy()
    for k in trimmed[1:]:
        final_key = np.bitwise_xor(final_key, k)

    return final_key

print("XOR keys function is ready.")
print("You can combine multiple keys using XOR operation.")
def run_multi_channel_qkd(
        n_channels=3,
        n_qubits=128,
        eve_probability=0.7,
        noise=0.01,
        qber_threshold=0.110000000000000000000000
    ):
    print("Starting multi-channel QKD simulation...")
    channels = []
    valid_keys = []

    for i in range(n_channels):
        print(f"Evaluating Channel {i+1}...")
        eve = random.random() < eve_probability
        result = run_qkd_channel(
            n_qubits=n_qubits,
            eve=eve,
            noise=noise
        )
        
        channel_data = {
            "channel_id": i,
            "eve": eve,
            "qber": result["qber"],
            "key_length": result["key_length"],
            "accepted": result["qber"] < qber_threshold
        }

        channels.append(channel_data)

        if channel_data["accepted"]:
            valid_keys.append(result["alice_key"])
        print(f"Quantum Channel {i+1} evaluated and reported QBER: {round(result['qber'],4)}")
    if len(valid_keys) == 0:
        return {
            "success": False,
            "reason": "All channels compromised",
            "channels": channels,
            "final_key": None
        }
    
    final_key = xor_keys(valid_keys)
    
    return {
        "success": True,
        "channels": channels,
        "valid_channel_count": len(valid_keys),
        "final_key": final_key,
        "final_key_length": len(final_key)
    }
