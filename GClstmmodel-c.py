#!/usr/bin/env python
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)

# fix random seed for reproducibility
numpy.random.seed(7)
dataframe =  pd.read_csv("GC-EDGE-CMD.csv", usecols=[1] , sep=",", header=None) #pd.read_csv("/home/ecrm/arima/DS6-trace.csv", usecols=[4] , sep=",", header=None) #pd.read_csv("/home/ecrm/arima/DS1-trace.csv", usecols=[4] , sep=",", header=None) #pd.read_csv("/home/ecrm/arima/cnewcountdata10Min.csv", usecols=[11] , sep=",", header=None)
dataset = dataframe.values
dataset = dataset.astype('float32')

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# split into train and test sets
train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

# reshape into X=t and Y=t+1
look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(4, input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)

# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))  #math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0])) # numpy.mean(numpy.abs((trainY - trainPredict) / trainY)) * 100
#trainScore = numpy.mean(numpy.abs((trainY - trainPredict) / trainY)) * 100
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0])) #math.sqrt(mean_squared_error(testY[0], testPredict[:,0])) # numpy.mean(numpy.abs((testY - testPredict) / testY)) * 100 
#testScore = numpy.mean(numpy.abs((testY - testPredict) / testY)) * 100 
print('Test Score: %.2f RMSE' % (testScore))


# shift train predictions for plotting
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict
"""
# plot baseline and predictions
plt.plot(testY[0], color='blue', label='Actual Demand')
#plt.plot(trainPredictPlot)
plt.plot(testPredict[:,0], color='red', label='Predicted Demand')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',ncol=2, mode="expand", borderaxespad=0.)
plt.ylabel('CPU Demand')
plt.xlabel('Samples')
plt.show()
"""
df = pd.DataFrame({"actual" : testY[0], "predicted" : testPredict[:,0]})
df.to_csv("GClstmresults-EDGE-c.csv", index=False)

