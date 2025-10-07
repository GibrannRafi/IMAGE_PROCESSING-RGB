import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(page_title="🎨 RGB Color Picker", layout="wide")
st.title("🎨 RGB Color Picker dari Gambar (Akurat 1:1 Pixel)")

# CSS biar bisa discroll di mobile
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
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📸 Upload gambar", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(img)

    # Pakai ukuran asli gambar (biar pixel klik sesuai)
    canvas_width = img.width
    canvas_height = img.height

    st.write(f"🖼️ Ukuran gambar: **{img.width} x {img.height} px**")
    st.write("🖱️ Klik di gambar untuk ambil warna pixel dan lihat tabel sekitar 5x5")

    # Gambar langsung di-canvas dengan ukuran asli
    canvas_result = st_canvas(
    fill_color="rgba(255,165,0,0.3)",
    stroke_width=2,
    stroke_color="blue",
    background_image=Image.open(uploaded_image) if uploaded_image else None,
    update_streamlit=True,
    height=img.height if uploaded_image else 300,
    width=img.width if uploaded_image else 300,
    drawing_mode="rect",
    key="canvas",
)

    if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
        obj = canvas_result.json_data["objects"][-1]
        x, y = int(obj["left"]), int(obj["top"])

        if 0 <= x < img.width and 0 <= y < img.height:
            color = img_array[y, x]
            st.markdown(
                f"**📍 Koordinat Pixel:** ({x}, {y})  \n"
                f"**🎨 RGB:** {tuple(color)}"
            )

            # Ambil area sekitar (5x5)
            x_min, x_max = max(0, x - 2), min(img.width, x + 3)
            y_min, y_max = max(0, y - 2), min(img.height, y + 3)
            color_block = img_array[y_min:y_max, x_min:x_max, :]

            # Tabel warna
            html_table = "<table style='border-collapse: collapse;'>"
            for row in color_block:
                html_table += "<tr>"
                for rgb in row:
                    color_hex = "#{:02x}{:02x}{:02x}".format(*rgb)
                    html_table += f"<td style='width:30px;height:30px;background-color:{color_hex};border:1px solid #aaa;' title='{rgb}'></td>"
                html_table += "</tr>"
            html_table += "</table>"

            st.markdown("### 🔍 Warna sekitar pixel (5x5):")
            st.markdown(html_table, unsafe_allow_html=True)

            # Zoom preview
            zoom_area = img.crop((x_min, y_min, x_max, y_max))
            zoom_img = zoom_area.resize((200, 200), Image.NEAREST)
            st.markdown("### 🔎 Zoom-in Area (5x5 pixel diperbesar):")
            st.image(zoom_img, caption="Zoomed 5x5 Area", use_container_width=False)
else:
    st.info("📁 Silakan upload gambar dulu untuk mulai.")
