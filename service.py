import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
import yfinance as yf
from sklearn.metrics import mean_absolute_error

def predict(company_symbol, periods):
    data_set = yf.Ticker(company_symbol).history("5y")
    data_set = data_set[["Close"]]

    #msft["Date"] = msft.index
    data_set['Date'] = pd.to_datetime(data_set.index).date
    data_set = data_set.rename(columns = {"Date":"ds","Close":"y"}) #renaming the columns of the dataset

    data_set = data_set.reset_index(drop=True)

    model = Prophet(daily_seasonality=True)
    model.fit(data_set[data_set.columns[::-1]])

    future = model.make_future_dataframe(periods=periods) #we need to specify the number of days in future
    prediction = model.predict(future)

    result = prediction[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()

    result['actual'] = pd.Series(data_set['y'].values)


    result.rename(columns = {'yhat':'predicted'}, inplace = True)
    result.rename(columns = {'yhat_lower':'predicted_lower'}, inplace = True)
    result.rename(columns = {'yhat_upper':'predicted_upper'}, inplace = True)

    y_actual = data_set['y']
    y_predicted = prediction['yhat']
    y_predicted = y_predicted.astype(int)
    error = mean_absolute_error(y_actual, y_predicted.head(len(y_predicted) - periods))


    return result, error