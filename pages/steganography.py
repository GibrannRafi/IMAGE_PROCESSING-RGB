import cv2
import numpy as np
from PIL import Image
import sys

# ============================
#   1️⃣ LSB METHOD 
# ============================
def encode_lsb(image_path, message, output_path):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size

    msg_bin = ''.join(format(ord(char), '08b') for char in message) + '00000000'
    idx = 0

    for y in range(height):
        for x in range(width):
            if idx < len(msg_bin):
                r, g, b = img.getpixel((x, y))
                r = (r & ~1) | int(msg_bin[idx]); idx += 1
                if idx < len(msg_bin):
                    g = (g & ~1) | int(msg_bin[idx]); idx += 1
                if idx < len(msg_bin):
                    b = (b & ~1) | int(msg_bin[idx]); idx += 1
                encoded.putpixel((x, y), (r, g, b))
            else:
                img.save(output_path)
                return

def decode_lsb(image_path):
    img = Image.open(image_path)
    width, height = img.size
    bits = ""

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ""
    for c in chars:
        if c == "00000000":
            break
        message += chr(int(c, 2))
    return message

# ============================
#   2️⃣ HISTOGRAM SHIFTING
# ============================
def encode_histogram(image_path, message, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    hist = cv2.calcHist([img], [0], None, [256], [0,256])
    peak = np.argmax(hist)
    zero = np.where(hist == 0)[0][0]

    msg_bin = ''.join(format(ord(i),'08b') for i in message) + '00000000'
    idx = 0
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] == peak and idx < len(msg_bin):
                img[i,j] = peak + int(msg_bin[idx])
                idx += 1
            elif peak < img[i,j] < zero:
                img[i,j] += 1

    cv2.imwrite(output_path, img)

def decode_histogram(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    bits = ""
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] == 128 or img[i,j] == 129:
                bits += str(img[i,j] - 128)
    
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ""
    for c in chars:
        if c == "00000000":
            break
        message += chr(int(c,2))
    return message

# ============================
#   3️⃣ PVD METHOD
# ============================
def encode_pvd(image_path, message, output_path):
    img = cv2.imread(image_path)
    msg_bin = ''.join(format(ord(i),'08b') for i in message) + '00000000'
    idx = 0

    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]-1, 2):
            if idx >= len(msg_bin):
                cv2.imwrite(output_path, img)
                return
            p1 = img[i,j,0]
            p2 = img[i,j+1,0]
            diff = abs(p1-p2)

            if diff < 16:
                bits = 1
            elif diff < 32:
                bits = 2
            elif diff < 64:
                bits = 3
            else:
                bits = 4

            segment = msg_bin[idx:idx+bits]
            idx += bits
            new_diff = int(segment,2)

            if p1 > p2:
                if p1 - new_diff < 0:
                    p1 = new_diff + p2
                else:
                    p2 = p1 - new_diff
            else:
                if p2 - new_diff < 0:
                    p2 = new_diff + p1
                else:
                    p1 = p2 - new_diff

            img[i,j,0] = p1
            img[i,j+1,0] = p2

def decode_pvd(image_path):
    img = cv2.imread(image_path)
    bits = ""

    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]-1, 2):
            p1 = img[i,j,0]
            p2 = img[i,j+1,0]
            diff = abs(p1-p2)

            if diff < 16:
                n = 1
            elif diff < 32:
                n = 2
            elif diff < 64:
                n = 3
            else:
                n = 4

            bits += format(diff, f'0{n}b')

    chars = [bits[i:i+8] for i in range(0,len(bits),8)]
    message = ""
    for c in chars:
        if c == "00000000":
            break
        message += chr(int(c, 2))
    return message

# ============================
#   📌 MAIN PROGRAM MENU
# ============================
def main():
    print("\n🔐 Steganography Program (3 Methods)")
    print("1. Encode LSB")
    print("2. Decode LSB")
    print("3. Encode Histogram Shifting")
    print("4. Decode Histogram Shifting")
    print("5. Encode PVD")
    print("6. Decode PVD")
    
    choice = int(input("\n⚙️ Pilih Menu: "))

    if choice in [1,3,5]:
        img = input("Masukkan path gambar input: ")
        msg = input("Masukkan pesan: ")
        out = input("Masukkan nama file output: ")

    if choice == 1:
        encode_lsb(img, msg, out)
        print("✔ Selesai Encode LSB")
    elif choice == 2:
        print("Pesan:", decode_lsb(input("Path gambar: ")))

    elif choice == 3:
        encode_histogram(img, msg, out)
        print("✔ Selesai Encode Histogram Shifting")
    elif choice == 4:
        print("Pesan:", decode_histogram(input("Path gambar: ")))

    elif choice == 5:
        encode_pvd(img, msg, out)
        print("✔ Selesai Encode PVD")
    elif choice == 6:
        print("Pesan:", decode_pvd(input("Path gambar: ")))
    else:
        print("❌ Invalid!")

if __name__ == "__main__":
    main()
