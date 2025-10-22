# 📸 threshold_equalization_v2.py
import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import io

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Image Threshold & Equalization", page_icon="🧮", layout="wide")

st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #2F3C7E;
        text-align: center;
    }
    .sub-box {
        background-color: #F7F7F8;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 5px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stDownloadButton > button {
        background-color: #2F3C7E;
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🧮 Image Thresholding & Histogram Equalization</p>', unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def to_rgb(img: Image.Image):
    return img.convert("RGB")

def to_array(img: Image.Image):
    return np.array(img, dtype=np.uint8)

def rgb_to_gray(arr: np.ndarray):
    gray = 0.2989 * arr[..., 0] + 0.5870 * arr[..., 1] + 0.1140 * arr[..., 2]
    return gray.astype(np.uint8)

def find_peaks(hist):
    peaks = []
    for i in range(1, len(hist) - 1):
        if hist[i] > hist[i-1] and hist[i] > hist[i+1]:
            peaks.append((hist[i], i))
    peaks = sorted(peaks, key=lambda x: x[0], reverse=True)
    return sorted([p[1] for p in peaks[:2]]) if peaks else [np.argmax(hist)]

def get_threshold(peaks):
    return int(np.mean(peaks)) if len(peaks) >= 2 else peaks[0]

def binary_image(gray, t):
    return np.where(gray > t, 255, 0).astype(np.uint8)

def hist_eq(gray):
    flat = gray.flatten()
    hist, _ = np.histogram(flat, bins=256, range=(0, 255))
    cdf = hist.cumsum()
    cdf_min = cdf[cdf > 0][0]
    cdf_norm = (cdf - cdf_min) / (cdf[-1] - cdf_min) * 255
    eq = cdf_norm[flat].astype(np.uint8)
    return eq.reshape(gray.shape)

# ---------------- LAYOUT ----------------
left, right = st.columns([1, 2])

with left:
    st.markdown('<div class="sub-box">', unsafe_allow_html=True)
    st.subheader("📤 Upload Gambar")
    file = st.file_uploader("Pilih gambar (PNG/JPG)", type=["png", "jpg", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

    if file:
        st.markdown('<div class="sub-box">', unsafe_allow_html=True)
        st.subheader("📈 Info Proses")
        st.write("- Konversi ke Grayscale")
        st.write("- Deteksi Dua Puncak Histogram")
        st.write("- Thresholding → Citra Biner")
        st.write("- Histogram Equalization (Grayscale)")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Upload gambar terlebih dahulu di atas untuk memulai.")

with right:
    if file:
        try:
            img = to_rgb(Image.open(file))
            arr = to_array(img)
            gray = rgb_to_gray(arr)

            # Histogram
            hist, _ = np.histogram(gray.flatten(), bins=256, range=(0,255))
            peaks = find_peaks(hist)
            threshold = get_threshold(peaks)
            binary = binary_image(gray, threshold)
            eq = hist_eq(gray)

            # ----- DISPLAY RESULT -----
            st.subheader("🖼️ Hasil Visualisasi")
            c1, c2, c3 = st.columns(3)
            c1.image(img, caption="Gambar Asli", use_column_width=True)
            c2.image(binary, caption=f"Citra Biner (Threshold={threshold})", use_column_width=True)
            c3.image(eq, caption="Equalized Image", use_column_width=True)

            # ----- HISTOGRAM BEFORE-AFTER -----
            st.subheader("📊 Histogram Equalization - Before & After (Grayscale)")
            fig5, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            ax1.plot(hist, color='gray')
            ax1.set_title("Before")
            ax1.set_xlim(0, 255)
            ax1.set_xlabel("Intensity")
            ax1.set_ylabel("Frequency")

            hist_eq_values, _ = np.histogram(eq.flatten(), bins=256, range=(0,255))
            ax2.plot(hist_eq_values, color='blue')
            ax2.set_title("After")
            ax2.set_xlim(0, 255)
            ax2.set_xlabel("Intensity")

            st.pyplot(fig5)

            # ----- STATS -----
            mean_before = np.mean(gray)
            mean_after = np.mean(eq)
            st.markdown(f"**Mean sebelum:** {mean_before:.2f} — **Mean sesudah:** {mean_after:.2f}")

            # ----- TABLE HISTOGRAM -----
            st.subheader("📋 Tabel Nilai Intensitas & Frekuensi (Grayscale Sebelum)")
            hist_df = pd.DataFrame({
                "Intensitas": np.arange(256),
                "Frekuensi": hist
            })
            st.dataframe(hist_df)

            csv = hist_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Histogram Grayscale CSV", csv, "histogram_grayscale.csv", "text/csv")

            # ----- DOWNLOAD HASIL GAMBAR -----
            st.markdown('<div class="sub-box">', unsafe_allow_html=True)
            st.subheader("💾 Download Hasil")
            def save_img(np_arr, name):
                buf = io.BytesIO()
                Image.fromarray(np_arr).convert("RGB").save(buf, format="PNG")
                st.download_button(f"Download {name}", data=buf.getvalue(), file_name=f"{name.lower().replace(' ','_')}.png", mime="image/png")

            save_img(arr, "Original Image")
            save_img(binary, "Binary Image")
            save_img(eq, "Equalized Image")
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")
