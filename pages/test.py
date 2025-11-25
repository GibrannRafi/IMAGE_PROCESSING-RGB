import streamlit as st
from PIL import Image
import numpy as np
import io
import base64

# --- Fungsi Inti Steganografi (LSB) ---

def encode_text(image, text):
    """Menyematkan teks ke dalam gambar menggunakan LSB."""
    text += "#####"
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    data_index = 0
    data_len = len(binary_text)
    img_array = np.array(image)

    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(img_array.shape[2]):
                if data_index < data_len:
                    pixel_value = img_array[i, j, k]
                    new_pixel_value = np.bitwise_and(pixel_value, 254) | int(binary_text[data_index])
                    img_array[i, j, k] = new_pixel_value
                    data_index += 1
        if data_index >= data_len:
            break

    encoded_image = Image.fromarray(img_array)
    return encoded_image, data_index


def decode_text(image):
    """Mengungkap teks dari gambar menggunakan LSB."""
    img_array = np.array(image)
    binary_data = ""

    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(img_array.shape[2]):
                binary_data += str(img_array[i, j, k] & 1)

    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
    decoded_text = ""

    for byte in all_bytes:
        if len(byte) == 8:
            decoded_text += chr(int(byte, 2))
            if decoded_text.endswith("#####"):
                return decoded_text[:-5]

    return "Tidak ada teks rahasia terdeteksi atau gambar bukan merupakan hasil encoding."


# --- Fungsi Streamlit ---

def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">**Klik di sini untuk mengunduh {text}**</a>'
    return href


def main():
    st.set_page_config(
        page_title="Aplikasi Steganografi Teks (LSB)",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.title("🔐 Aplikasi Steganografi Teks dengan Streamlit")
    st.markdown("Aplikasi untuk menyembunyikan teks ke dalam gambar dan mengungkapkannya kembali menggunakan teknik **LSB (Least Significant Bit)**.")
    
    st.sidebar.header("Pilih Aksi")
    operation = st.sidebar.radio("Apa yang ingin Anda lakukan?", 
                                 ("Sembunyikan Teks (Encode)", "Ungkap Teks (Decode)"))
    
    st.markdown("---")
    
    # ====== ENCODE ======
    if operation == "Sembunyikan Teks (Encode)":
        st.header("🖼️ Sembunyikan Teks ke dalam Gambar")
        
        uploaded_file = st.file_uploader("Pilih gambar yang akan digunakan (PNG/JPG)", 
                                         type=["png", "jpg", "jpeg"])
        secret_text = st.text_area("Masukkan teks rahasia yang ingin disembunyikan:", 
                                   max_chars=500, height=150)
        
        if uploaded_file and secret_text:
            try:
                original_image = Image.open(uploaded_file).convert("RGB")
                max_chars_possible = (original_image.width * original_image.height * 3) // 8
                
                if (len(secret_text) + 5) * 8 > (original_image.width * original_image.height * 3):
                    st.error(f"❌ **Kesalahan:** Teks terlalu panjang! Gambar ini hanya dapat menampung sekitar {max_chars_possible - 5} karakter.")
                else:
                    st.success("✅ Gambar dan Teks siap disematkan.")
                    
                    if st.button("Lakukan Encoding"):
                        st.info("Sedang memproses penyematan teks...")
                        encoded_image, bits_used = encode_text(original_image, secret_text)
                        
                        st.subheader("Hasil Steganografi")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.image(original_image, caption="Citra Awal", use_column_width=True)
                            
                        with col2:
                            st.image(encoded_image, caption="Citra Hasil Stegano", use_column_width=True)
                            
                        st.markdown(f"**Pesan:** '{secret_text}' telah berhasil disematkan ke dalam gambar!")
                        st.markdown(get_image_download_link(encoded_image, "stegano_result.png", "Citra Hasil Stegano"), 
                                    unsafe_allow_html=True)
                        
                        st.markdown("---")
                        st.caption(f"Keterangan: Digunakan {bits_used} bit untuk menyematkan teks.")
                        
            except Exception as e:
                st.error(f"Terjadi kesalahan saat pemrosesan: {e}")

    # ====== DECODE ======
    elif operation == "Ungkap Teks (Decode)":
        st.header("🔍 Ungkap Teks dari Gambar")
        
        uploaded_stegano = st.file_uploader("Pilih Citra Hasil Stegano (PNG direkomendasikan)", 
                                            type=["png", "jpg", "jpeg"])
        
        if uploaded_stegano:
            try:
                stegano_image = Image.open(uploaded_stegano).convert("RGB")
                st.image(stegano_image, caption="Citra Stegano yang Diunggah", use_column_width=True)
                
                if st.button("Lakukan Decoding"):
                    st.info("Sedang mencoba mengungkap teks rahasia...")
                    decoded_text = decode_text(stegano_image)

                    st.subheader("Teks yang Diungkap")

                    if decoded_text.startswith("Tidak ada teks"):
                        st.error("❌ Tidak ditemukan pesan dalam gambar ini.")
                    else:
                        st.success("✅ Pesan berhasil ditemukan di dalam gambar!")
                        st.code(decoded_text, language='text')

            except Exception as e:
                st.error(f"Terjadi kesalahan saat pemrosesan: {e}")

if __name__ == "__main__":
    main()
