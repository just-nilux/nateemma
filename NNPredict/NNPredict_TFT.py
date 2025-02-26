import operator

import numpy as np
from enum import Enum

import pywt
import talib.abstract as ta
from scipy.ndimage import gaussian_filter1d
from sklearn.preprocessing import RobustScaler, MinMaxScaler, StandardScaler

import freqtrade.vendor.qtpylib.indicators as qtpylib
import arrow

from freqtrade.exchange import timeframe_to_minutes
from freqtrade.strategy import (IStrategy, merge_informative_pair, stoploss_from_open,
                                IntParameter, DecimalParameter, CategoricalParameter)

from typing import Dict, List, Optional, Tuple, Union
from pandas import DataFrame, Series
from functools import reduce
from datetime import datetime, timedelta
from freqtrade.persistence import Trade

# Get rid of pandas warnings during backtesting
import pandas as pd
import pandas_ta as pta

pd.options.mode.chained_assignment = None  # default='warn'

# Strategy specific imports, files must reside in same folder as strategy
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import logging
import warnings

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

import custom_indicators as cta
from finta import TA as fta

#import keras
from keras import layers
from tqdm import tqdm
from tqdm.keras import TqdmCallback

import random

from NNPredict import NNPredict
from NNPredictor_TFT import NNPredictor_TFT

"""
####################################################################################
Predict_TFT - uses an TFT neural network to try and predict the future stock price
      
      This works by creating a  model that we train on the historical data, then use that model to predict 
      future values
      
      Note that this is very slow because we are training and running a neural network. 
      This strategy is likely not viable on a configuration of more than a few pairs, and even then needs
      a fast computer, preferably with a GPU
      
      In addition to the normal freqtrade packages, these strategies also require the installation of:
        finta
        keras
        tensorflow
        tqdm
        darts

####################################################################################
"""

# this inherits from NNPredict and just replaces the model used for predictions

class NNPredict_TFT(NNPredict):
    
    

    ################################

    def get_classifier(self, pair, seq_len: int, num_features: int):
        use_gpu = False # gpu issues with this model
        predictor = NNPredictor_TFT(pair, seq_len, num_features, use_gpu=use_gpu)
        name = self.__class__.__name__
        predictor.set_model_name(name, name)
        predictor.set_lookahead(self.curr_lookahead)
        predictor.set_target_column(self.target_column)
        return predictor

    ################################
