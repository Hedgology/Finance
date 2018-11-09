
#forecast.def

from __future__ import print_function

import datetime
import numpy as np
import pandas as pd
import sklearn
import fix_yahoo_finance as yf

from pandas_datareader import data as pdr
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.svm import LinearSVC, SVC

yf.pdr_override()

def create_lagged_series(symbol, start_date, end_date, lags = 5):
    """
    This creates a pandas DataFrame that stores the
    percentage returns of the adjusted closing value of
    a stock obtained from Yahoo Finance, along with a
    number of lagged returns from the prior trading days
    (lags defaults to 5 days). Trading volume, as well as
    the Direction from the previous day, are also included.
    """

    #Obtain stock information from Yahoo Finance

    ts = pdr.get_data_yahoo(
            symbol,
            start_date-datetime.timedelta(days=365),
            end_date
    )

    #Create the new lagged DataFrame

    tslag = pd.DataFrame(index = ts.index)
    tslag['Today'] = ts['Adj Close']
    tslag['Volume'] = ts['Volume']

    # Create the shifted lag series of prior trading period close values
    for i in range(0, lags):
        tslag['lag%s' % str(i+1)] = ts['Adj Close'].shift(i+1)

    # Create the return DataFrame
    tsret = pd.DataFrame(index = tslag.index)
    tsret['Volume'] = tslag['Volume']
    tsret['Today'] = tslag['Today'].pct_change() * 100.0

    #If any of the values of percentage return equal zero, set them to
    # a small number (stops issues with QDA model in scikit-learn)
    for i, x enumerate(tsret['Today']):
        if (abs(x) < 0.0001):
            tsret['Today'][i] = 0.0001

    # Create the lagged percentage returns column
    for i in range(0, lags):
        tsret['Lag%s' % str(i+1)] = \
        tslag['Lag%s' % str(i+1)].pct_change()*100.0

    # Create the "Direction" column (+1 of -1) indicating an up/down day
    tsret['Direction'] = np.sign(tsret['Today'])
    tsret = tsret[tsret.index >= start_date]

    return tsret
