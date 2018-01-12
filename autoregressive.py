from pandas import Series
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
from  datetime import datetime
import pandas as pd
import json
import matplotlib.dates as mdates

style.use("ggplot")

def test():
	data = {}
	usdtbtc = {}

	with open("data/BTC-ARK.json") as f:

		data = json.load(f)["result"]

	raw = pd.DataFrame(data)

	data={}
	with open("data/USDT-BTC.json") as f:

		data = json.load(f)["result"]

	usdtbtc = pd.DataFrame(data)
	# print(usdtbtc.C)

	raw = pd.merge(usdtbtc.rename(index=str, columns={"C": "USDT"})[["T", "USDT"]], raw, on=["T"])
	# closeBTCPriceSeries = raw.iloc[:,1]
	# closeUSDTPriceSeries = closeBTCPriceSeries.multiply(usdtbtc.iloc[:,1])

	# CONVERT to datetime
	# CALCULATE closing usd value
	raw["C_USDT"] = raw["C"] * raw["USDT"]
	raw["T"] = pd.to_datetime(raw["T"].str.replace('T', ' '))

	# print(raw.columns)
	raw = raw.set_index("T")
	# raw.plot()
	# plt.show()

	raw["100ma"] = raw["C_USDT"].rolling(window=100).mean()

	# df = raw.dropna()

	df_ohlc = raw.C_USDT.resample("1D").ohlc()
	df_volume = raw.C_USDT.resample("1D").sum()

	df_ohlc.reset_index(inplace=True)
	df_ohlc["T"] = df_ohlc["T"].map(mdates.date2num)

	ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
	ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

	ax1.xaxis_date()

	candlestick_ohlc(ax1, df_ohlc.values, width=0.5)
	ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

	# ax1.plot(df.index, df.C_USDT)
	# ax1.plot(df.index, df["100ma"])
	# ax2.bar(df.index, df["V"])

	plt.show()