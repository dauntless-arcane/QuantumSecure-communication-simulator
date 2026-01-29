import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd

from multichannel.manager import run_multi_channel_qkd
from crypto.encryption import encrypt_message, decrypt_message
from stego.lsb import embed_data, extract_data
from metrics.image_metrics import evaluate_images

# ---------------- Page Config ----------------
st.set_page_config(page_title="Quantum Secure Communication Simulator", layout="wide")

st.title("🔐 Quantum Secure Multi-Layer Communication Simulator")

st.markdown("""
This simulator demonstrates a **three-layer secure communication architecture**:

**Layer 1:** Quantum Key Distribution (BB84)  
**Layer 2:** Multi-channel fault-tolerant key fusion  
**Layer 3:** AES encryption + Steganographic covert transmission  
""")

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Simulation Controls")

n_channels = st.sidebar.slider("Number of quantum channels", 1, 8, 4)
n_qubits = st.sidebar.selectbox("Qubits per channel", [32, 64, 128, 256], index=2)
eve_prob = st.sidebar.slider("Eavesdropper probability", 0.0, 1.0, 0.4)
noise = st.sidebar.slider("Quantum noise level", 0.0, 0.1, 0.02)
message = st.sidebar.text_area("Message to send", "Quantum secure communication achieved.")

run_button = st.sidebar.button("🚀 Run Simulation")

# ---------------- Log System ----------------
st.subheader("📡 System Execution Log")
log_box = st.empty()

if "logs" not in st.session_state:
    st.session_state.logs = []

def log(msg):
    st.session_state.logs.append(msg)
    log_box.markdown("\n".join(st.session_state.logs))
    time.sleep(0.4)

# ---------------- Run Simulation ----------------
if run_button:

    st.session_state.logs = []

    log("### Stage 1: Initializing quantum communication layer")
    log("- Preparing BB84 protocol")
    log("- Configuring multi-channel quantum links")
    log("- Enabling QBER-based eavesdropping detection")

    time.sleep(1)

    log("\n### Stage 2: Executing multi-channel quantum key distribution")

    with st.spinner("Running quantum channels..."):
        result = run_multi_channel_qkd(
            n_channels=n_channels,
            n_qubits=n_qubits,
            eve_probability=eve_prob,
            noise=noise
        )

    log("✔ Quantum transmission completed")

    # ---------------- Quantum Results ----------------
    st.subheader("🧪 Quantum Channel Evaluation")

    df = pd.DataFrame(result["channels"])
    st.dataframe(df, use_container_width=True)

    accepted = [c for c in result["channels"] if c["accepted"]]
    rejected = [c for c in result["channels"] if not c["accepted"]]

    log(f"\nAccepted channels: {len(accepted)}")
    log(f"Rejected channels: {len(rejected)}")

    for ch in result["channels"]:
        if ch["accepted"]:
            log(f"🟢 Channel {ch['channel_id']} accepted | QBER = {round(float(ch['qber']),4)}")
        else:
            log(f"🔴 Channel {ch['channel_id']} rejected | QBER = {round(float(ch['qber']),4)}")

    if not result["success"]:
        st.error("❌ All channels compromised. Secure communication aborted.")
        log("\n❌ SYSTEM ABORTED — No secure quantum channels available.")
        st.stop()

    final_key = result["final_key"]

    log("\n### Stage 3: Multi-channel key fusion")
    log("- Rejecting compromised channels")
    log("- Performing XOR fusion on secure keys")
    log(f"- Final quantum key generated ({len(final_key)} bits)")

    st.success(f"✅ Secure quantum key established | Length: {len(final_key)} bits")

    # ---------------- Encryption ----------------
    st.subheader("🔐 Encryption Layer")

    log("\n### Stage 4: Classical encryption layer")
    log("- Deriving AES-256 key from quantum bits")
    log("- Encrypting plaintext message")

    encrypted = encrypt_message(message, final_key)
    payload = encrypted["iv"] + encrypted["ciphertext"]

    st.code(f"Original Message:\n{message}")
    st.code(f"Encrypted Message:\n{encrypted['ciphertext'].hex()}")
    st.info(f"Encrypted payload size: {len(payload)} bytes")

    # ---------------- Steganography ----------------
    st.subheader("🕵️ Covert Communication Layer")

    log("\n### Stage 5: Steganographic embedding")
    log("- Loading cover image")
    log("- Embedding encrypted payload into image LSBs")
    log("- Generating stego image")

    cover_path = "assets/cover.png"
    stego_path = "assets/stego_ui.png"

    _ = embed_data(cover_path, payload, stego_path)

    col1, col2 = st.columns(2)
    with col1:
        st.image(cover_path, caption="Original Image")
    with col2:
        st.image(stego_path, caption="Stego Image")

    # ---------------- Receiver ----------------
    log("\n### Stage 6: Receiver-side extraction and decryption")
    log("- Extracting hidden encrypted payload")
    log("- Decrypting using shared quantum key")

    extracted = extract_data(stego_path, len(payload))
    iv = extracted[:16]
    ciphertext = extracted[16:]
    decrypted = decrypt_message(ciphertext, iv, final_key)

    st.subheader("📨 Communication Result")
    st.code("Recieved Message:\n" + encrypted['ciphertext'].hex())
    st.success("Recovered Message\n" + decrypted)

    # ---------------- Metrics ----------------
    st.subheader("📊 Steganography Quality Metrics")

    metrics = evaluate_images(cover_path, stego_path)

    c1, c2, c3 = st.columns(3)
    c1.metric("SSIM", round(metrics["SSIM"], 6))
    c2.metric("PSNR (dB)", round(metrics["PSNR"], 2))
    c3.metric("MSE", round(metrics["MSE"], 6))

    log("\n### Stage 7: System verification complete")
    log("✔ Secure multi-layer communication successfully achieved")
