#!/usr/bin/env python
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

df = pd.read_csv("container_meta-half.csv", usecols=[6] , sep=",", header=None)
X=df.values
size = int(len(X) * 0.85)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
	model = ARIMA(history, order= (7,1,0)) # (3,0,1) (5,0,1)  (7,0,1)**  (3,1,0) (5,1,0) (7,1,0) (1,1,0)*
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
	#print('predicted=%f, expected=%f' % (yhat, obs))

def rotate(arr,n):
	return arr[n:] + arr[:n]

predictions=rotate(predictions,1)
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)

pyplot.plot(test, color='blue', label='Actual Demand')
pyplot.plot(predictions, color='red', label='Predicted Demand')
pyplot.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',ncol=2, mode="expand", borderaxespad=0.)
pyplot.ylabel('CPU Demand')
pyplot.xlabel('Samples')
pyplot.show()

arrpredict=np.asarray(predictions)

df = pd.DataFrame({"actual" : test[:, 0], "predicted" : arrpredict[:, 0]})
df.to_csv("results-C6-half.csv", index=False)
