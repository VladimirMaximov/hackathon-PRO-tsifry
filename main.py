import joblib
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer

from user import User
from stages.stage1 import renderStage1
from stages.stage2 import renderStage2
from stages.stage3 import renderStage3
from stages.stage4 import renderStage4


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
    data = pd.DataFrame({"Наименование": ["Картошка фри", "Гамбургер", "Кола"],
                         "Количество": [2, 1, 1],
                         "Цена за 1 шт.": [100, 150, 120],
                         "Цена": [200, 150, 120]})
    renderStage2(data)
elif st.session_state.stage == 3:
    renderStage3()
elif st.session_state.stage == 4:
    renderStage4()

