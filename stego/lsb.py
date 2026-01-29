# stego/lsb.py

import cv2
import numpy as np


def bytes_to_bits(data):
    bits = []
    for byte in data:
        bits.extend([int(b) for b in format(byte, '08b')])
    return bits


def bits_to_bytes(bits):
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        bytes_list.append(int("".join(map(str, byte)), 2))
    return bytes(bytes_list)


def embed_data(image_path, data, output_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found")

    flat = image.flatten()
    bits = bytes_to_bits(data)

    if len(bits) > len(flat):
        raise ValueError("Data too large to embed")

    for i in range(len(bits)):
        flat[i] = (flat[i] & 0b11111110) | bits[i]

    stego = flat.reshape(image.shape)
    cv2.imwrite(output_path, stego)
    return output_path


def extract_data(image_path, data_length):
    image = cv2.imread(image_path)
    flat = image.flatten()

    bits = []
    for i in range(data_length * 8):
        bits.append(flat[i] & 1)

    return bits_to_bytes(bits)
