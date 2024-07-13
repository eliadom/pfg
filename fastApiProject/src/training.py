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


def processa_dades(nomexcel, numDies):
    scaler = MinMaxScaler()
    directoriActual = os.path.dirname(os.path.abspath(__file__))
    save_path = (os.path.join('model', nomexcel + ".xlsx"))
    novaRuta = os.path.join(directoriActual, save_path)

    df = pd.read_excel(novaRuta)

    try:
        df = df.applymap(utf8_encode)
        print("df is UTF-8, length %d bytes" % len(df))
    except UnicodeError:
        print("df is not UTF-8")

    index = 0
    importantData = pd.DataFrame(
        {'Year': [], 'Month': [], 'Day': [], 'Weekday': [], 'Hour': [], 'Minute': [], 'Value': []})

    while index < len(df):
        row = df.loc[index]
        readingDate = row['INF_Date']
        readingDate = readingDate[:-8]
        datetimeDate = datetime.strptime(readingDate, "%Y-%m-%d %H:%M:%S")
        # newRow = {'Year': datetimeDate.year, 'Month': datetimeDate.month, 'Day': datetimeDate.day,
        #           'Weekday': datetimeDate.weekday(),
        #           'Hour': datetimeDate.hour, 'Minute': datetimeDate.minute, 'Value': row['INF_Value']}
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



        # lastRegisterFromHour = importantData.loc[index]
        #
        # varYear = lastRegisterFromHour['Year']
        # varMonth = lastRegisterFromHour['Month']
        # varDay = lastRegisterFromHour['Day']
        # varWeekday = lastRegisterFromHour['Weekday']
        # varHour = lastRegisterFromHour['Hour']
        # varMinute = lastRegisterFromHour['Minute']
        # currentTime = str(int(varYear)) + '-' + str(int(varMonth)).zfill(2) + '-' + str(int(varDay)).zfill(
        #     2) + " " + str(int(varHour)).zfill(2) + ':' + str(int(varMinute)).zfill(2)
        # currentRowDatetime = datetime.strptime(currentTime, "%Y-%m-%d %H:%M")
        # previousRowDatetime = currentRowDatetime - timedelta(hours=1)
        # nextRowDatetime = currentRowDatetime + timedelta(hours=1)
        #
        # varYearPrev = previousRowDatetime.year
        # varMonthPrev = previousRowDatetime.month
        # varDayPrev = previousRowDatetime.day
        # varWeekdayPrev = previousRowDatetime.weekday()
        # varHourPrev = previousRowDatetime.hour
        # varMinutePrev = previousRowDatetime.minute
        #
        # # intentem buscar un registre del qual faci exactament 1h
        # firstOfCurrentHour = importantData.loc[(importantData['Year'] == varYear) & (importantData['Month'] == varMonth)
        #                                        & (importantData['Day'] == varDay) & (
        #                                                    importantData['Hour'] == varHour)].tail(1)
        #
        # firstOfPreviousHour = importantData.loc[
        #     (importantData['Year'] == varYearPrev) & (importantData['Month'] == varMonthPrev)
        #     & (importantData['Day'] == varDayPrev) & (importantData['Hour'] == varHourPrev)].tail(1)
        #
        # multiplier = 1
        #
        # # si no existeix, fem el calcul manualment
        # if (not (firstOfCurrentHour.empty) | firstOfPreviousHour.empty):
        #     if (float(firstOfCurrentHour['Minute']) != float(firstOfPreviousHour['Minute'])):
        #         # si no ha passat exactament 1h, farem els calculs manualment
        #
        #         minDiff = float(firstOfCurrentHour['Minute']) - float(firstOfPreviousHour['Minute'])
        #         if (minDiff != 0):
        #             multiplier = (60 / minDiff)
        #
        #     valueCreated = (float(firstOfCurrentHour['Value']) - float(firstOfPreviousHour['Value'])) * multiplier
        #     fullStringDate = str(int(varYearPrev)) + '-' + str(int(varMonthPrev)).zfill(2) + '-' + str(
        #         int(varDayPrev)).zfill(2) + ' ' + str(int(firstOfPreviousHour['Hour'])).zfill(2) + ':' + str(
        #         int(firstOfPreviousHour['Minute'])).zfill(2)
        #     fullStringDate = datetime.strptime(fullStringDate, '%Y-%m-%d %H:%M')
        #     newRow = {'Year': varYear, 'Month': varMonth, 'Day': varDay, 'Weekday': varWeekday,
        #               'HourStart': fullStringDate, 'Value': valueCreated}
        #
        #     dataByHours.loc[indexHours] = newRow
        #     indexHours += 1
        #     index += 1
        #     nextRow = importantData.loc[index]
        #     while ((index < len(importantData)) & (nextRow['Hour'] == varHour)):
        #         index += 1
        #         if ((index < len(importantData))):
        #             nextRow = importantData.loc[index]
        # else:
        #     break;

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

    print("dataForModel:")
    print(dataForModel)

    scaler.fit_transform(dataForModel)
    X_mostres, y_mostres, = load_data(dataForModel, seq_len)
    print("x mostres::")
    print(X_mostres)
    print("y mostres::")
    print(y_mostres)

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
    # batch_size = 800
    steps_per_epoch = int(len(X_mostres) / batch_size) * 3

    # lstm_model.fit(X_mostres, y_mostres, epochs=700, batch_size=batch_size, steps_per_epoch=steps_per_epock, verbose=2)
    lstm_model.fit(X_mostres, y_mostres, epochs=15, batch_size=batch_size, steps_per_epoch=steps_per_epoch, verbose=2)

    print("model generated:")
    print(lstm_model.summary)
    print("guardant model...")

    directoriActual = os.path.dirname(os.path.abspath(__file__))
    save_path = (os.path.join('model', nomexcel + ".h5"))
    novaRuta = os.path.join(directoriActual, save_path)

    lstm_model.save(novaRuta)

    ## PREDICCIO --------------------

    primeres24h = X_mostres
    resulPrimeres24h = y_mostres

    N = 24800


    prediction = lstm_model.predict(X_mostres[-N:], verbose=2)
    prediction_copies = np.repeat(prediction, 6, axis=-1)

    prediccio24h = prediction_copies[:0]
    # prediccio24h = []

    for i in range(2, numDies):
        diaSeguent = lstm_model.predict(X_mostres[-N:], verbose=2)
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

    plt.figure(figsize=(16, 4))
    plt.plot(prediccio24h, alpha=0.7, color='orange', label='Consum predit')
    plt.xlabel('Temps')
    plt.ylabel('Consum d\'aigua')
    plt.legend()
    plt.show()

    print("Predicted consum:")
    print(prediccio24h)

    # Generem prediccio dels 3 propers dies:
    #
    # Primerament, generem les properes 24h.

    # lstm_predictions = lstm_model.predict(X_mostres, verbose=2)
    # print(lstm_predictions)

# no les primeres 24h
#     lstm_predictions = lstm_model.predict(X_mostres[-N:], verbose=2)
#
#     lstm_score = r2_score(X_mostres, lstm_predictions)
#     print("R^2 Score of LSTM model = ",lstm_score)
#     plot_predictions(y_mostres, lstm_predictions, "Predictions fetes pel model LSTM")
#     print("LSTM predictions:")
#     print(lstm_predictions)

# funcio per preparar els 3 seguents dies
# def prepara_prediccions(stock):
#   X_mostres = []
#
#   print("showing stock")
#   print(stock)
#
#   seq_len = 1
#
#   stock1 = stock
#
#
#
#   for i in range(seq_len, len(stock1)):
#     X_mostres.append(stock1.iloc[i-seq_len : i, 0])
#
#
#   X_mostres = np.array(X_mostres)
#
#   X_mostres = np.reshape(X_mostres,(len(X_mostres), seq_len, 1))
#   return X_mostres
