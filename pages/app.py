import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="🎨 RGB Color Picker", layout="centered")
st.title("🎨 RGB Color Picker dari Gambar")

uploaded_file = st.file_uploader("Upload gambar", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(img)

    # Tentukan ukuran canvas biar responsif
    is_mobile = st.session_state.get("is_mobile", False)
    canvas_width = 300 if is_mobile else 500
    aspect_ratio = img.height / img.width
    canvas_height = int(canvas_width * aspect_ratio)

    st.write("🖱️ Klik di gambar untuk ambil warna pixel dan lihat tabel sekitar 5x5")

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

    if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
        # Ambil titik klik terakhir
        obj = canvas_result.json_data["objects"][-1]
        x, y = int(obj["left"]), int(obj["top"])

        # Sesuaikan dengan ukuran asli gambar
        scale_x = img.width / canvas_width
        scale_y = img.height / canvas_height
        x_real, y_real = int(x * scale_x), int(y * scale_y)

        if 0 <= x_real < img.width and 0 <= y_real < img.height:
            color = img_array[y_real, x_real]
            st.markdown(
                f"**📍 Koordinat Pixel:** ({x_real}, {y_real})  \n"
                f"**🎨 RGB:** {tuple(color)}"
            )

            # Ambil area 5x5 sekitar titik
            x_min, x_max = max(0, x_real - 2), min(img.width, x_real + 3)
            y_min, y_max = max(0, y_real - 2), min(img.height, y_real + 3)
            color_block = img_array[y_min:y_max, x_min:x_max, :]

            # Buat tabel HTML berwarna
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

            # ======== Tambahan: mini zoom-in preview =========
            zoom_area = img.crop((x_min, y_min, x_max, y_max))
            zoom_size = 200  # perbesar tampilannya biar jelas
            zoom_img = zoom_area.resize((zoom_size, zoom_size), Image.NEAREST)

            st.markdown("### 🔎 Zoom-in Area (5x5 pixel diperbesar):")
            st.image(zoom_img, caption="Zoomed 5x5 Area", use_container_width=False)
else:
    st.info("📁 Silakan upload gambar dulu untuk mulai.")
