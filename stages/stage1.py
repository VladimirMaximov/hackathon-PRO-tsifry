import streamlit as st
from menu import menu


def renderStage1():
    st.markdown("# СберЧек - разделение счета по фотографии чека")
    st.image("test_photo2.jpg",)
    uploaded_file = st.file_uploader(label="", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Открываем изображение с помощью Pillow
        st.session_state.image = uploaded_file
        st.session_state.stage = 2
        st.rerun()

    menu()