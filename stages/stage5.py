import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from menu import menu

def renderStage5():
    """
    Этап 5: итоговая сводная таблица с колонками:
      - Гость №
      - Потратил (ProgressColumn)
      - Цена в % (NumberColumn)
      - Круговая диаграмма (ImageColumn)
      - Оплатил (CheckboxColumn)
    """
    st.markdown("# Итог")
    st.markdown("---")

    # 1) Собираем суммы по каждому гостю и общий итог
    totals = [float(df["Цена"].sum()) for df in st.session_state.dfs]
    total_all = sum(totals)

    # Вспомогательная функция: строит pie‑chart и возвращает data URI
    def make_pie_data_uri(value: float, total: float, size_px: int = 100) -> str:
        fig, ax = plt.subplots(
            figsize=(size_px / 100, size_px / 100),
            dpi=100
        )
        ax.pie(
            [value, max(total - value, 0.0)],
            colors=["#1CAF5E", "#D0FFD1"],
            startangle=90,
            wedgeprops={"linewidth": 0},
        )
        ax.axis("equal")
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode()
        return f"data:image/png;base64,{b64}"

    # 2) Формируем список строк
    rows = []
    for i, spent in enumerate(totals, start=1):
        pct = (spent / total_all * 100) if total_all > 0 else 0.0
        rows.append({
            "Гость №":   f"№{i}",
            "Потратил":   spent,
            "Цена в %":  round(pct, 1),
            "Диаграмма":  make_pie_data_uri(spent, total_all),
            "Оплатил":    False
        })
    summary_df = pd.DataFrame(rows)

    # 3) Рендерим data_editor с новыми столбцами
    edited = st.data_editor(
        summary_df,
        key="stage5_summary",
        hide_index=True,
        use_container_width=True,
        column_config={
            "Потратил": st.column_config.ProgressColumn(
                label="Потратил, ₽",
                format="%.2f ₽",
                min_value=0.0,
                max_value=float(total_all)
            ),
            "Цена в %": st.column_config.NumberColumn(
                label="Потратил, %",
                format="%.1f%%",
                width="small"
            ),
            "Диаграмма": st.column_config.ImageColumn(
                label="Диаграмма",
                width="small"
            ),
            "Оплатил": st.column_config.CheckboxColumn(
                label="Оплатил",
                width="small"
            )
        },
        disabled=True
    )

    # 4) Сохраняем состояние чекбоксов
    st.session_state.payment_done = edited["Оплатил"].tolist()

    st.markdown("# Введите номер телефона для генерации QR-кода")
    st.markdown("---")

    # 5) Поле для телефона и кнопка QR
    phone = st.text_input(
        label="",
        value="+7",
        max_chars=12,
        help="В формате +7XXXXXXXXXX",
        label_visibility="collapsed"
    )
    if st.button("Сгенерировать QR‑код для оплаты", use_container_width=True):
        if len(phone) != 12 or not phone.startswith("+7") or not phone[2:].isdigit():
            st.error("Неверный формат. Должно быть +7 и 10 цифр.")
        else:
            st.success(f"QR‑код для {phone} сгенерирован.")

    menu()

