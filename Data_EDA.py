import pandas as pd

import os
import glob

from read_csv import read_multiple_csv

path = r'D:/MarketReport/inbound'
df=read_multiple_csv(path)

df.drop(['BizDt', 'Sgmt', 'Src', 'FinInstrmTp', 'FinInstrmId', 'ISIN','XpryDt', 'FininstrmActlXpryDt', 'StrkPric','OptnTp','FinInstrmNm','LastPric','PrvsClsgPric', 'UndrlygPric', 'SttlmPric', 'OpnIntrst','ChngInOpnIntrst', 'TtlTradgVol', 'TtlTrfVal', 'TtlNbOfTxsExctd',
       'SsnId', 'NewBrdLotQty', 'Rmks', 'Rsvd1', 'Rsvd2', 'Rsvd3', 'Rsvd4'],axis=1,inplace=True)

final_df=df[df['SctySrs'].isin(['BE', 'EQ'])]


final_df.drop(['SctySrs'], axis=1, inplace=True)

final_df.rename(columns={"TradDt": "date", 
                         "TckrSymb": "ticker", 
                         "OpnPric": "open", 
                         "HghPric": "high", 
                         "LwPric": "low", 
                         "ClsPric": "close"}, inplace=True)