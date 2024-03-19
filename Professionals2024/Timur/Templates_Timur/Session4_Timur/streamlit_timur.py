import joblib
import pandas as pd
import streamlit as st
import requests
import json
import os

os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

def send_request(date, area):
    response = requests.post(
        "http://localhost:8000/predict/",
        json={"date": date, "country": area}
    )

    return response.json()

def send_request_graphic(area):
    response = requests.post(
        "http://localhost:8000/graphic/",
        json={"country": area}
    )

    return response.json()



# Add the About window
with st.expander("О программе"):
    st.write("""
    Эта программа предсказывает уровень опасности COVID-19 в конкретном регионе в конкретную дату.

    - Введите дату: введите дату, для которой хотите предсказать уровень опасности.
    - Введите регион: введите регион (страну), для которого хотите предсказать уровень опасности.
    - Выявить уровень опасности в текущую дату: нажмите эту кнопку, чтобы предсказать уровень опасности для введенной даты и региона.
    - Вывод графика заболеваний по стране за весь период времени: нажмите эту кнопку, чтобы отобразить график новых случаев COVID-19 в введенном регионе за весь период времени.
    """)

st.title("Covid")

date = st.date_input("Enter date")
area = st.text_input("Enter area")

if st.button("Выявить уровень опасности в текущую дату"):
    result = send_request(date.strftime("%Y-%m-%d"), area)
    print(result)

    if 'Ошибка' in result:
        danger_level = result["Ошибка"]
    elif 'Уровень' in result:
        danger_level = result["Уровень"]
    else:
        pass

    if danger_level == "Безопасно":
        color = "green"
    elif danger_level == "Средняя опасность":
        color = "purple"
    else:
        color = "red"

    st.markdown(f'<p style="color: {color};">Результат: {danger_level.capitalize()}</p>', unsafe_allow_html=True)

if st.button("Вывод графика заболеваний по стране за весь период времени"):
    result = send_request_graphic(area)
    st.line_chart(result, x='Date', y='new_cases')