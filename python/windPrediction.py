import json
import math
from flask import Flask, request

import pandas as pd
import numpy as np
from pandas import json_normalize
import matplotlib.pyplot as plt

from sklearn import model_selection
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)


@app.route("/windPrediction", methods=['POST'])
def windData():

    try:

        data = request.get_json()
        data = data['data']['data']

        df = json_normalize(data)
        df = df[["datetime", "min_temp", "max_temp", "temp",
                "wind_spd", "max_wind_spd", "wind_gust_spd", "wind_dir"]]

        df.columns = ["datetime", "min_temp", "max_temp", "mean_temp",
                      "min_speed", "mean_speed", "max_speed", "direction"]

        # print(df.head(5))

        x = df[["min_temp", "max_temp", "mean_temp",
                "min_speed", "max_speed", "direction"]]
        y = df[["mean_speed"]]

        x_train, x_test, y_train, y_test = model_selection.train_test_split(
            x, y, test_size=0.1, random_state=4)

        xnorm = StandardScaler()
        ynorm = StandardScaler()

        x_train = xnorm.fit_transform(x_train)
        x_test = xnorm.transform(x_test)

        y_train = ynorm.fit_transform(np.array(y_train).reshape(-1, 1))
        y_test = ynorm.transform(np.array(y_test).reshape(-1, 1))

        model = Sequential()
        model.add(Dense(512, input_shape=(6,), activation='relu'))
        model.add(Dense(256, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam')
        # print(model.summary())

        model.fit(x_train, y_train, epochs=30, batch_size=32)

        # trainPredict = model.predict(x_train)
        testPredict = model.predict(x_test)

        # plt.plot(range(0, y_train.shape[0]), ynorm.inverse_transform(y_train), label='y_train')
        # plt.plot(range(y_train.shape[0], y_train.shape[0] + y_test.shape[0]), ynorm.inverse_transform(y_test), label='y_test')
        # plt.xlabel('Day')
        # plt.ylabel('Mean Speed')
        # plt.title('Wind Speed Prediction')
        # plt.legend()
        # plt.show()

        # plt.plot(range(0, y_train.shape[0]), ynorm.inverse_transform(y_train), label='y_train')
        # plt.plot(range(y_train.shape[0], y_train.shape[0] + y_test.shape[0]), ynorm.inverse_transform(testPredict), label='testPredict2')
        # plt.xlabel('Day')
        # plt.ylabel('Mean Speed')
        # plt.title('Wind Speed Prediction')
        # plt.legend()
        # plt.show()

        trainingScore = model.evaluate(x_train, y_train)
        testingScore = model.evaluate(x_test, y_test)

        plot_1x = list(range(0, y_train.shape[0]))
        
        plot_1y = (ynorm.inverse_transform(y_train)).tolist()
        plot_1y = [dat[0] for dat in plot_1y]
        
        plot_2x = list(range(y_train.shape[0], y_train.shape[0] + y_test.shape[0]))
        
        plot_2test_y = (ynorm.inverse_transform(y_test)).tolist()
        plot_2test_y = [dat[0] for dat in plot_2test_y]

        plot_2predict_y = (ynorm.inverse_transform(testPredict)).tolist()
        plot_2predict_y = [dat[0] for dat in plot_2predict_y]

        arr_res = np.array([ plot_1x + plot_2x, plot_1y + [0 for _ in plot_2test_y], [0 for _ in plot_1y] + plot_2test_y, [0 for _ in plot_1y] + plot_2predict_y ])

        arr_res = arr_res.transpose()
        # print(arr_res)

            # "plot_1x": plot_1x,
            # "plot_1y": plot_1y,
            # "plot_2x": plot_2x,

            # "plot_2test_y": plot_2test_y,
            # "plot_2predict_y": plot_2predict_y,

        data = {
            "response": arr_res.tolist(),
            "trainingScore": trainingScore, 
            "RMS_trainingScore": math.sqrt(trainingScore), 
            "testingScore": testingScore, 
            "RMS_testingScore": math.sqrt(testingScore), 
        }


        # train = y_train.tolist()
        # train = [dat[0] for dat in train]

        # test = y_test.tolist()
        # test = [dat[0] for dat in test]
        
        # predict = testPredict.tolist()
        # predict = [dat[0] for dat in predict]
        # 'y_train': train, 
        # 'y_test': test, 
        # 'testPredict': predict

        return json.dumps({"result": "ok", "data": data})

    except Exception as e:
        print(e)
        return json.dumps({"error": "Error Occured"})


if __name__ == "__main__":
    app.run(port=5001)
