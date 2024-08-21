from io import BytesIO

import pandas as pd
from datetime import datetime, timedelta
import calendar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

import os

from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['PYTHONIOENCODING'] = 'utf8'

from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from keras.models import load_model

def load_data(stock, seq_len):

    X_mostres = []
    y_mostres = []

    print("showing stock")
    print(stock)

    reshapingSize = int(len(stock))
    seq_len = 1

    stock1 = stock

    for i in range(seq_len, len(stock1)):
        X_mostres.append(stock1.iloc[i - seq_len: i, 0])
        y_mostres.append(stock1.iloc[i, 0])

    X_mostres = np.array(X_mostres)
    y_mostres = np.array(y_mostres)

    X_mostres = np.reshape(X_mostres, (len(X_mostres), seq_len, 1))
    return [X_mostres, y_mostres]


def plot_predictions(test, predicted, title):
    plt.figure(figsize=(16, 4))
    plt.plot(test, color='blue', label='Consum real')
    plt.plot(predicted, alpha=0.7, color='orange', label='Consum predit')
    plt.title(title)
    plt.xlabel('Temps')
    plt.ylabel('Consum d\'aigua')
    plt.legend()
    plt.show()


def utf8_encode(x):
    if isinstance(x, str):
        return x.encode('utf-8').decode('utf-8')
    else:
        return x

from keras.src.legacy.saving import legacy_h5_format

def genera_prediccio(nomexcel, numDies, horaInicial):

    directoriActual = os.path.dirname(os.path.abspath(__file__))
    save_path = (os.path.join('model', nomexcel + ".h5"))
    novaRuta = os.path.join(directoriActual, save_path)

    # guardem model LSTM

    # lstm_model = load_model(novaRuta , custom_objects={'MSE': 'mean_squared_error'})
    lstm_model = legacy_h5_format.load_model_from_hdf5(novaRuta, custom_objects={'MSE': 'MSE'})


    save_path_mostresX = (os.path.join('model', nomexcel + "Xmostres.npy"))
    novaRutaMostresX = os.path.join(directoriActual, save_path_mostresX)

    X_mostresREST = np.load(novaRutaMostresX)
    X_mostresREST.flatten().reshape(-1, 1, 1)
    print(X_mostresREST.shape)
    print(X_mostresREST)

    ## PREDICCIO --------------------

    N = 24800

    X_mostresPRED = X_mostresREST
    prediction = lstm_model.predict(X_mostresPRED[-N:], verbose=2)
    prediction_copies = np.repeat(prediction, 6, axis=-1)

    prediccio24h = prediction_copies[:0]
    # prediccio24h = []

    for i in range(1, numDies+1):
        diaSeguent = lstm_model.predict(X_mostresPRED[-N:], verbose=2)
        n = len(diaSeguent)
        i = 0
        resul = []
        while i < n:
            if i + 2 < n:  # Verifica que existan al menos 3 elementos restantes
                suma = diaSeguent[i] + diaSeguent[i + 1] + diaSeguent[i + 2]
                resul.append(suma)
                i += 3
            else:  # Si no hay suficientes elementos para formar un grupo de 3, añade los elementos restantes
                resul.extend(diaSeguent[i:])
                break
        prediction_copies = np.repeat(resul, 6, axis=-1)
        prediccio24h = np.concatenate((prediccio24h, prediction_copies[:24]))

    # predicted_consum = scaler.transform(prediction_copies)

    prediccio24h = prediccio24h[horaInicial:]

    plt.figure(figsize=(16, 4))
    plt.plot(prediccio24h, alpha=0.7, color='orange', label='Consum predit')
    plt.xlabel('Temps')
    plt.ylabel('Consum d\'aigua')
    plt.legend()
    plt.show()

    print("Predicted consum:")
    print(prediccio24h)
    return prediccio24h.tolist(), plt


def processa_dades(nomexcel):

    directoriActual = os.path.dirname(os.path.abspath(__file__))
    save_path = (os.path.join('model', nomexcel + ".xlsx"))
    novaRuta = os.path.join(directoriActual, save_path)

    df = pd.read_excel(novaRuta)

    try:
        df = df.applymap(utf8_encode)
    except UnicodeError:
        print("df no es UTF-8")

    index = 0
    importantData = pd.DataFrame(
        {'Year': [], 'Month': [], 'Day': [], 'Weekday': [], 'Hour': [], 'Minute': [], 'Value': []})

    while index < len(df):
        row = df.loc[index]
        readingDate = row['INF_Date']
        readingDate = readingDate[:-8]
        datetimeDate = datetime.strptime(readingDate, "%Y-%m-%d %H:%M:%S")
        newRow = {'Year': datetimeDate.year, 'Month': datetimeDate.month, 'Day': datetimeDate.day,
                  'Weekday': datetimeDate.weekday(),
                  'Hour': datetimeDate,'Value': row['INF_Value']}
        importantData.loc[index] = newRow
        index += 1

    indexHours = 0
    index = 0

    dataByHours = pd.DataFrame({'Year': [], 'Month': [], 'Day': [], 'Weekday': [], 'HourStart': [], 'Value': []})

    previousRow = None

    while index < len(importantData):
        if (previousRow != None):
            valueDiff = float(previousRow['Value']) - float(importantData.loc[index]['Value'])
        else:
            valueDiff = float(importantData.loc[index]['Value'])

        newRow = {'Year': importantData.loc[index]['Year'], 'Month': importantData.loc[index]['Month'], 'Day': importantData.loc[index]['Day'], 'Weekday': importantData.loc[index]['Weekday'],
                      'HourStart': importantData.loc[index]['Hour'], 'Value': valueDiff}

        if (previousRow != None):
            dataByHours.loc[index] = newRow

        newRow['Value'] = importantData.loc[index]['Value']
        previousRow = newRow
        index += 1


    dataForModel = dataByHours
    dataForModel = dataForModel.loc[:, ['HourStart', 'Value']]
    dataForModel = dataForModel.set_index('HourStart')

    # dataForModel = normalize_data(dataForModel)
    dataForModel.shape
    train = dataForModel
    test = dataForModel.loc[:, []]

    train.sort_index()

    train["Value"].plot(figsize=[16, 4], legend=True)

    seq_len = -1


    scaler = MinMaxScaler()

    scaler.fit_transform(dataForModel)
    X_mostres, y_mostres, = load_data(dataForModel, seq_len)

    lstm_model = Sequential()

    lstm_model.add(LSTM(250, activation="tanh", return_sequences=True, input_shape=(X_mostres.shape[1], 1)))
    lstm_model.add(Dropout(0.15))

    lstm_model.add(LSTM(250, activation="tanh", return_sequences=True))
    lstm_model.add(Dropout(0.15))

    lstm_model.add(LSTM(250, activation="tanh", return_sequences=False))
    lstm_model.add(Dropout(0.15))

    lstm_model.add(Dense(1))

    lstm_model.summary()

    lstm_model.compile(optimizer="adam", loss="MSE")

    batch_size = 64
    steps_per_epoch = int(len(X_mostres) / batch_size) * 3

    lstm_model.fit(X_mostres, y_mostres, epochs=15, batch_size=batch_size, steps_per_epoch=steps_per_epoch, verbose=2)

    directoriActual = os.path.dirname(os.path.abspath(__file__))
    save_path = (os.path.join('model', nomexcel + ".h5"))
    novaRuta = os.path.join(directoriActual, save_path)

    # guardem model LSTM
    lstm_model.save(novaRuta)

    # guardem x mostres i y mostres en un excel nou

    X_mostresFLAT = pd.DataFrame(X_mostres.flatten())
    save_path_mostresX = (os.path.join('model', nomexcel + "Xmostres.npy"))
    novaRutaMostresX = os.path.join(directoriActual, save_path_mostresX)

    np.save(novaRutaMostresX, X_mostresFLAT)
    return importantData['Hour'][0].hour
