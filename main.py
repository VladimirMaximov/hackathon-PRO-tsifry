import streamlit as st

from user import User
from stages.stage1 import renderStage1
from stages.stage2 import renderStage2
from stages.stage3 import renderStage3
from stages.stage4 import renderStage4
from stages.stage5 import renderStage5
from OCR import for_classifier

st.set_page_config(
            page_title="СберЧек - главная",  # Отображаемый заголовок вкладки
            page_icon=":bank:",  # Необязательно: можно задать иконку (эмодзи, URL или путь к изображению)
            layout="wide"
        )

if "user" not in st.session_state:
    st.session_state.user = User()
    st.session_state.stage = 1

if st.session_state.stage == 1:
    renderStage1()
elif st.session_state.stage == 2:
    st.session_state.df = for_classifier.get_result(st.session_state.img_bgr)
    renderStage2(st.session_state.df)
elif st.session_state.stage == 3:
    renderStage3()
elif st.session_state.stage == 4:
    renderStage4()
else:
    renderStage5()