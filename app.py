import streamlit as st
import yt_dlp
import os
import glob

st.set_page_config(page_title="YouTube MP3 Downloader", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #FF0000;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎵 Descargador MP3")
st.write("Convierte videos de YouTube a audio en alta calidad (320kbps).")

url = st.text_input("Enlace del video de YouTube", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Convertir a MP3"):
    if not url:
        st.warning("Por favor, ingresa una URL válida.")
    else:
        with st.spinner("Procesando y convirtiendo audio..."):
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio')

                list_of_files = glob.glob('downloads/*.mp3')
                latest_file = max(list_of_files, key=os.path.getctime)

                with open(latest_file, "rb") as file:
                    st.success("¡Conversión completada!")
                    st.download_button(
                        label="📥 Descargar archivo MP3",
                        data=file,
                        file_name=os.path.basename(latest_file),
                        mime="audio/mpeg"
                    )

            except Exception as e:
                st.error(f"Error al procesar el enlace: {str(e)}")
