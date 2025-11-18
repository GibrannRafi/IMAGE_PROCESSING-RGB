import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🔍 Canny Edge Detection – Step by Step")

# Normalisasi biar bisa ditampilkan di Streamlit
def norm(img):
    img = img.astype("float32")
    m = img.min()
    M = img.max()
    return (img - m) / (M - m + 1e-6)

uploaded = st.file_uploader("Upload gambar", type=["jpg", "png", "jpeg"])

if uploaded:
    # Load image
    img = Image.open(uploaded)
    img_np = np.array(img)

    # 1. Grayscale
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    # 2. Gaussian Blur
    gaussian = cv2.GaussianBlur(gray, (5, 5), 1.4)

    # 3. Sobel X & Y
    sobelx = cv2.Sobel(gaussian, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gaussian, cv2.CV_64F, 0, 1, ksize=3)

    # 4. Gradient Magnitude
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    magnitude = np.uint8((magnitude / magnitude.max()) * 255)

    # 5. Non-Max Suppression (NMS)
    angle = np.arctan2(sobely, sobelx) * 180 / np.pi
    angle[angle < 0] += 180

    nms = np.zeros_like(magnitude)
    rows, cols = magnitude.shape

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            q = r = 255

            # 0 degrees
            if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                q = magnitude[i, j+1]
                r = magnitude[i, j-1]
            # 45 degrees
            elif (22.5 <= angle[i,j] < 67.5):
                q = magnitude[i+1, j-1]
                r = magnitude[i-1, j+1]
            # 90 degrees
            elif (67.5 <= angle[i,j] < 112.5):
                q = magnitude[i+1, j]
                r = magnitude[i-1, j]
            # 135 degrees
            elif (112.5 <= angle[i,j] < 157.5):
                q = magnitude[i-1, j-1]
                r = magnitude[i+1, j+1]

            if (magnitude[i,j] >= q) and (magnitude[i,j] >= r):
                nms[i,j] = magnitude[i,j]

    # 6. Double Threshold
    high = nms.max() * 0.2
    low = high * 0.5

    strong = 255
    weak = 50

    dt = np.zeros_like(nms)
    strong_i, strong_j = np.where(nms >= high)
    weak_i, weak_j = np.where((nms <= high) & (nms >= low))

    dt[strong_i, strong_j] = strong
    dt[weak_i, weak_j] = weak

    # 7. Hysteresis
    hysteresis = dt.copy()
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if hysteresis[i, j] == weak:
                if np.any(hysteresis[i-1:i+2, j-1:j+2] == strong):
                    hysteresis[i, j] = strong
                else:
                    hysteresis[i, j] = 0

    # Show results
    st.image(img, caption="Original Image")

    st.subheader("Proses Canny:")
    st.image(gray, caption="1. Grayscale")
    st.image(gaussian, caption="2. Gaussian Blur")

    # PAKAI NORMALISASI untuk Sobel
    st.image(norm(sobelx), caption="3. Sobel Gx", clamp=True)
    st.image(norm(sobely), caption="4. Sobel Gy", clamp=True)

    st.image(magnitude, caption="5. Gradient Magnitude (Normalized)")
    st.image(nms, caption="6. Non-Max Suppression (NMS)")
    st.image(dt, caption="7. Double Threshold")
    st.image(hysteresis, caption="8. Hysteresis (Final Edge)")
