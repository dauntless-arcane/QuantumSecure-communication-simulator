import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.qkd import run_qkd_channel
print(run_qkd_channel(64, eve=False, noise=0.0))
print(run_qkd_channel(64, eve=True, noise=0.0))
print(run_qkd_channel(128, eve=False, noise=0.05))