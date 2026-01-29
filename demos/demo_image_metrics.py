import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from metrics.image_metrics import evaluate_images

results = evaluate_images("assets/cover.png", "assets/stego.png")

print("\n=== IMAGE QUALITY METRICS ===")
for k, v in results.items():
    print(f"{k}: {v}")
