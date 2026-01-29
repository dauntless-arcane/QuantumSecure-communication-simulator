# core/qkd.py

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import depolarizing_error, NoiseModel


def create_noise_model(p):
    noise_model = NoiseModel()
    error = depolarizing_error(p, 1)
    noise_model.add_all_qubit_quantum_error(error, ['x', 'h'])
    return noise_model

def prepare_qubit(bit, basis):
    qc = QuantumCircuit(1, 1)

    if bit == 1:
        qc.x(0)
    if basis == 'X':
        qc.h(0)

    return qc


def measure_qubit(qc, basis):
    if basis == 'X':
        qc.h(0)
    qc.measure(0, 0)
    return qc


def run_qkd_channel(n_qubits=64, eve=False, noise=0.0):

    backend = AerSimulator()
    noise_model = create_noise_model(noise) if noise > 0 else None

    alice_bits = np.random.randint(2, size=n_qubits)
    alice_bases = np.random.choice(['Z', 'X'], size=n_qubits)
    bob_bases = np.random.choice(['Z', 'X'], size=n_qubits)
    print("Running QKD channel simulation...")
    alice_results = []
    bob_results = []

    for i in range(n_qubits):
        qc = prepare_qubit(alice_bits[i], alice_bases[i])

        # Eve intercept-resend
        if eve:
            eve_basis = np.random.choice(['Z', 'X'])
            qc_eve = qc.copy()
            qc_eve = measure_qubit(qc_eve, eve_basis)

            compiled = transpile(qc_eve, backend)
            result = backend.run(compiled, shots=1).result().get_counts()
            eve_bit = int(list(result.keys())[0])

            qc = prepare_qubit(eve_bit, eve_basis)

        qc = measure_qubit(qc, bob_bases[i])

        compiled = transpile(qc, backend)
        job = backend.run(compiled, shots=1, noise_model=noise_model)
        result = job.result().get_counts()
        measured_bit = int(list(result.keys())[0])

        alice_results.append(alice_bits[i])
        bob_results.append(measured_bit)

    sifted_alice = []
    sifted_bob = []

    for i in range(n_qubits):
        if alice_bases[i] == bob_bases[i]:
            sifted_alice.append(alice_results[i])
            sifted_bob.append(bob_results[i])

    sifted_alice = np.array(sifted_alice)
    sifted_bob = np.array(sifted_bob)

    if len(sifted_alice) == 0:
        return None

    errors = np.sum(sifted_alice != sifted_bob)
    qber = errors / len(sifted_alice)

    return {
        "qber": qber,
        "key_length": len(sifted_alice),
        "accepted": qber < 0.11,
        "alice_key": sifted_alice,
        "bob_key": sifted_bob
    }
