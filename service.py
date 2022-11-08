import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import yfinance as yf
from json import dumps

def predict(company_symbol, periods):
    msft = yf.Ticker(company_symbol).history("5y")
    msft = msft[["Close"]]

    #msft["Date"] = msft.index
    msft['Date'] = pd.to_datetime(msft.index).date
    msft = msft.rename(columns = {"Date":"ds","Close":"y"}) #renaming the columns of the dataset

    msft = msft.reset_index(drop=True)

    model = Prophet(daily_seasonality=True)
    model.fit(msft[msft.columns[::-1]])

    future = model.make_future_dataframe(periods=periods) #we need to specify the number of days in future
    prediction = model.predict(future)

    result = prediction[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()

    result['actual'] = pd.Series(msft['y'].values)

    result.rename(columns = {'yhat':'predicted'}, inplace = True)
    result.rename(columns = {'yhat_lower':'predicted_lower'}, inplace = True)
    result.rename(columns = {'yhat_upper':'predicted_upper'}, inplace = True)

    return result 