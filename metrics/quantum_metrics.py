# metrics/quantum_metrics.py

import numpy as np
from core.qkd import run_qkd_channel
from multichannel.manager import run_multi_channel_qkd


def qber_vs_eve(eve_probs, runs=20, n_qubits=128, noise=0.0):
    results = {}

    for p in eve_probs:
        qbers = []
        for _ in range(runs):
            res = run_qkd_channel(
                n_qubits=n_qubits,
                eve=(np.random.rand() < p),
                noise=noise
            )
            qbers.append(res["qber"])

        results[p] = np.mean(qbers)

    return results


def ber_vs_noise(noise_levels, runs=20, n_qubits=128):
    results = {}

    for noise in noise_levels:
        qbers = []
        for _ in range(runs):
            res = run_qkd_channel(
                n_qubits=n_qubits,
                eve=False,
                noise=noise
            )
            qbers.append(res["qber"])

        results[noise] = np.mean(qbers)

    return results


def success_rate_vs_channels(channel_counts, runs=20, eve_probability=0.4, noise=0.02):
    results = {}

    for n in channel_counts:
        success = 0
        for _ in range(runs):
            res = run_multi_channel_qkd(
                n_channels=n,
                eve_probability=eve_probability,
                noise=noise
            )
            if res["success"]:
                success += 1

        results[n] = success / runs

    return results
