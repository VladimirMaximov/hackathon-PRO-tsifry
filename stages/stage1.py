import cv2
import numpy as np
import streamlit as st
from menu import menu


def renderStage1():
    st.markdown("# СберЧек - разделение счета по фотографии чека")
    with st.columns(1)[0]:
        st.image("preview.png")
        uploaded_file = st.file_uploader(label="", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        if uploaded_file is not None:
            # Открываем изображение с помощью Pillow
            file_bytes = uploaded_file.read()  # bytes
            st.session_state.image = file_bytes

            # 2. Делаем из них numpy-массив uint8
            np_arr = np.frombuffer(file_bytes, dtype=np.uint8)

            # 3. Декодируем этот буфер в BGR-изображение OpenCV
            st.session_state.img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            st.session_state.stage = 2

            st.rerun()


    menu()