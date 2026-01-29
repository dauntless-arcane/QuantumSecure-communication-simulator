# metrics/image_metrics.py

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def compute_mse(img1, img2):
    return np.mean((img1 - img2) ** 2)


def compute_psnr(img1, img2):
    mse = compute_mse(img1, img2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))


def compute_ssim(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(gray1, gray2, full=True)
    return score


def evaluate_images(original_path, stego_path):
    original = cv2.imread(original_path)
    stego = cv2.imread(stego_path)

    return {
        "MSE": compute_mse(original, stego),
        "PSNR": compute_psnr(original, stego),
        "SSIM": compute_ssim(original, stego)
    }
