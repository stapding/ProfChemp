from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from fastapi.responses import JSONResponse


app = FastAPI()

# Load the trained model, scaler, and PCA
kmeans = joblib.load('kmeans_model.pkl')
scaler = joblib.load('scaler.pkl')
pca = joblib.load('pca.pkl')
le = joblib.load('label_encoder.pkl')


# Load the data
data = pd.read_csv('data.csv')

class InputData(BaseModel):
    country: str
    date: str

@app.post("/predict/")
async def predict(input_data: InputData):
    if input_data.country not in le.classes_:
        return {"Ошибка": "Такой страны нет"}

    # Encode the country
    country_encoded = le.transform([input_data.country])

    # Search for a record in the data based on the entered country and date
    record = data.loc[(data['location'] == country_encoded[0]) & (data['Date'] == input_data.date)]

    if record.empty:
        return {"Ошибка": "Не найдено записей по дню и стране"}

    # Preprocess the input data
    record_array = np.array(record.iloc[0][:-2]).reshape(1, -1)
    scaled_data = scaler.transform(record_array)
    x_pca = pca.transform(scaled_data)

    # Make a prediction
    label = kmeans.predict(x_pca)

    # Map the label to a safety level
    if label[0] == 0:
        safety = 'Безопасно'
    elif label[0] == 1:
        safety = 'Средняя опасность'
    else:
        safety = 'Опасно'

    return {"Уровень": safety}


class CurrentCountry(BaseModel):
    country: str

@app.post("/graphic/")
async def graphic(input_data: CurrentCountry):
    if input_data.country not in le.classes_:
        return {"Ошибка": "Такой страны нет"}
    # Encode the country
    country_encoded = le.transform([input_data.country])

    filtered_df = data[data['location'].isin(country_encoded)]

    return JSONResponse(content=filtered_df.to_dict(orient="records"))