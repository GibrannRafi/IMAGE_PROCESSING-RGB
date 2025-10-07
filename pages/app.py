import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(page_title="🎨 RGB Color Picker", layout="wide")
st.title("🎯 RGB Pixel Viewer dari Gambar")

# CSS biar tampilannya rapi dan mobile-friendly
st.markdown("""
    <style>
    div[data-testid="stCanvas"] {
        overflow-x: auto;
        max-width: 100%;
    }
    [data-testid="stImage"] img {
        max-width: 100%;
        height: auto;
        border-radius: 10px;
    }
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        h1 { font-size: 1.5rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📸 Upload gambar", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(img)

    # Ukuran asli gambar
    canvas_width = img.width
    canvas_height = img.height

    st.write(f"🖼️ Ukuran gambar: **{img.width} x {img.height}** px")
    st.write("🖱️ Klik di gambar untuk melihat warna pixel dan tabel sekitar 5x5")

    # Canvas interaktif
    canvas_result = st_canvas(
        fill_color="rgba(255,165,0,0.3)",
        stroke_width=1,
        background_image=img,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode="transform",
        key="canvas",
    )

    # Deteksi klik terakhir
    if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
        obj = canvas_result.json_data["objects"][-1]
        x, y = int(obj["left"]), int(obj["top"])

        if 0 <= x < img.width and 0 <= y < img.height:
            color = img_array[y, x]
            r, g, b = color
            st.markdown(
                f"### 📍 Koordinat Pixel: ({x}, {y})  \n"
                f"### 🎨 RGB: ({r}, {g}, {b})"
            )

            # Preview warna
            st.markdown(
                f"<div style='width:80px;height:80px;background-color:rgb({r},{g},{b});border:2px solid #000;border-radius:8px'></div>",
                unsafe_allow_html=True
            )

            # Ambil area 5x5 sekitar titik klik
            x_min, x_max = max(0, x - 2), min(img.width, x + 3)
            y_min, y_max = max(0, y - 2), min(img.height, y + 3)
            color_block = img_array[y_min:y_max, x_min:x_max, :]

            # Tabel warna sekitar
            html_table = "<table style='border-collapse: collapse;'>"
            for row in color_block:
                html_table += "<tr>"
                for rgb in row:
                    color_hex = "#{:02x}{:02x}{:02x}".format(*rgb)
                    html_table += f"<td style='width:30px;height:30px;background-color:{color_hex};border:1px solid #999;' title='{rgb}'></td>"
                html_table += "</tr>"
            html_table += "</table>"

            st.markdown("### 🔍 Warna sekitar pixel (5x5):")
            st.markdown(html_table, unsafe_allow_html=True)

            # Koordinat detail
            st.markdown(f"🧭 Titik yang diklik berada pada pixel **baris {y} kolom {x}** dari gambar.")
