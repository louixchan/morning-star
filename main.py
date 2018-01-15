import bittrex
import autoregressive
import datetime
import time
import pandas as pd
import json
import os
import random
import numpy as np
from matplotlib import pyplot as plt

tickersList = \
[
	"BTC-XVG",
	"BTC-ETH",
	"BTC-XRP",
	"BTC-SC",
	"BTC-DOGE",
	"BTC-ADA",
	"BTC-STRAT",
	"BTC-BCC",
	"BTC-DGB",
	"BTC-XLM",
	"BTC-NEO",
	"BTC-FUN",
	"BTC-ETC",
	"BTC-QTUM",
	"BTC-MYST",
	"BTC-LTC",
	"BTC-OMG",
	"BTC-RDD",
	"BTC-SALT",
	"BTC-UKG",
	"BTC-XDN",
	"BTC-ZCL",
	"BTC-XMR",
	"BTC-BAT",
	"BTC-MANA",
	"BTC-XEM",
	"BTC-LSK",
	"BTC-REP",
	"BTC-POWR",
	"BTC-NXT",
	"BTC-VOX",
	"BTC-SNT",
	"BTC-PAY",
	"BTC-BTG",
	"BTC-WAVES",
	"BTC-ZEC",
	"BTC-BAY",
	"BTC-ARK",
	"BTC-RCN",
	"BTC-ENG",
	"BTC-PTOY",
	"BTC-NBT",
	"BTC-1ST",
	"BTC-STEEM",
	"BTC-EBST",
	"BTC-PIVX",
	"BTC-GNT",
	"BTC-EDG",
	"BTC-GAME",
	"BTC-BURST",
	"BTC-MONA",
	"BTC-DASH",
	"BTC-ADX",
	"BTC-VTC",
	"BTC-MCO",
	"BTC-STORJ",
	"BTC-SYS",
	"BTC-EMC2",
	"BTC-BRK",
	"BTC-DCT",
	"BTC-NXS",
	"BTC-GUP",
	"BTC-DNT",
	"BTC-MUSIC",
	"BTC-CFI",
	"BTC-MTL",
	"BTC-CVC",
	"BTC-SYNX",
	"BTC-HMQ",
	"BTC-VIA",
	"BTC-RISE",
	"BTC-OK",
	"BTC-KMD",
	"BTC-TRIG",
	"BTC-PKB",
	"BTC-XCP",
	"BTC-XZC",
	"BTC-SPHR",
	"BTC-THC",
	"BTC-SLR",
	"BTC-ADT",
	"BTC-AMP",
	"BTC-FCT",
	"BTC-NMR",
	"BTC-LBC",
	"BTC-GNO",
	"BTC-DCR",
	"BTC-UNB",
	"BTC-GRS",
	"BTC-GEO",
	"BTC-LMC",
	"BTC-SBD",
	"BTC-BITB",
	"BTC-SPR",
	"BTC-XMY",
	"BTC-BYC",
	"BTC-XEL",
	"BTC-NEOS",
	"BTC-WINGS",
	"BTC-QWARK",
	"BTC-BNT",
	"BTC-ANT",
	"BTC-ZEN",
	"BTC-UBQ",
	"BTC-NAV",
	"BTC-AEON",
	"BTC-VIB",
	"BTC-PINK",
	"BTC-LUN",
	"BTC-MEME",
	"BTC-CANN",
	"BTC-CLAM",
	"BTC-POT",
	"BTC-BSD",
	"BTC-NXC",
	"BTC-QRL",
	"BTC-MER",
	"BTC-DGD",
	"BTC-TIX",
	"BTC-DYN",
	"BTC-IOP",
	"BTC-CRW",
	"BTC-SHIFT",
	"BTC-TRST",
	"BTC-AGRS",
	"BTC-DTB",
	"BTC-SIB",
	"BTC-START",
	"BTC-MUE",
	"BTC-GCR",
	"BTC-MAID",
	"BTC-RADS",
	"BTC-CLUB",
	"BTC-EXP",
	"BTC-SLS",
	"BTC-FTC",
	"BTC-RLC",
	"BTC-FLDC",
	"BTC-OMNI",
	"BTC-BLK",
	"BTC-CLOAK",
	"BTC-EMC",
	"BTC-TX",
	"BTC-VRC",
	"BTC-PPC",
	"BTC-ABY",
	"BTC-DOPE",
	"BTC-GBYTE",
	"BTC-XMG",
	"BTC-IOC",
	"BTC-BLITZ",
	"BTC-COVAL",
	"BTC-EGC",
	"BTC-CPC",
	"BTC-PART",
	"BTC-CRB",
	"BTC-TKS",
	"BTC-EXCL",
	"BTC-SWT",
	"BTC-KORE",
	"USDT-BTC"
]

def fetchBittrexPrice():
	i = 0
	time.sleep(30)
	for item in tickersList:
		print("%d out of %d" % ((i + 1), len(tickersList)))
		bittrex.fetch_bittrex_data(marketName=item, tickInterval="hour", startDateTime=datetime.datetime(2017, 11, 1))
		i = i + 1
		time.sleep(60)

def compileData():

	with open("data/tickers.txt", "r") as f:

		tickers = f.readlines()

	tickers = [str(x).rstrip("\n") for x in tickers]
	mainDfBTC = pd.DataFrame()

	for count, ticker in enumerate(tickers):
		with open("data/{}.json".format(ticker), "r") as f:
			data = json.load(f)["result"]
			df = pd.DataFrame(data)

			df.rename(columns={"C":ticker}, inplace=True)
			df["T"] = pd.to_datetime(df["T"].str.replace('T', ' '))
			df.set_index("T", inplace=True)
			df.drop(["O", "H", "L", "V", "BV"], 1, inplace=True)

			if mainDfBTC.empty:
				mainDf = df
			else:
				mainDf = mainDf.join(df, how="outer")

			if count % 10 == 0:
				print(count)

	print(mainDfBTC.head())

	mainDfBTC.to_csv("bittrex_joined_closes.csv")

	return mainDfBTC

def loadCompiledData():

	if os.path.isfile("bittrex_joined_closes.csv"):

		data = pd.read_csv("bittrex_joined_closes.csv")
		data.set_index("T", inplace=True)
		return data

	else:

		return compileData()

def visualiseCorrelation(df):
	df_corr = df.corr()

	data = df_corr.values
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	heatmap = ax.pcolor(data, cmap=plt.cm.RdGy)
	fig.colorbar(heatmap)
	ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
	ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
	ax.invert_yaxis()
	ax.xaxis.tick_top()

	column_labels = df_corr.columns
	row_labels = df_corr.columns

	ax.set_xticklabels(column_labels)
	ax.set_yticklabels(row_labels)
	plt.xticks(rotation=90)
	heatmap.set_clim(-1, 1)
	plt.tight_layout()
	plt.show()

	# Neutral ones (BTC):
	# POT, BSD, CLUB, UKG

	# Neutral ones (USD):
	# UKG, NBT, NXT, MONA, VTC, EMC2, CLUB, TX, IOC
	# Negative ones (USD):
	# BTG

def loadUSD(df):

	if not("USDT-BTC" in list(df.columns)):

		with open("data/USDT-BTC.json", "r") as f:
			data = json.load(f)["result"]
			temp = pd.DataFrame(data)

			temp.rename(columns={"C": "USDT-BTC"}, inplace=True)
			temp["T"] = pd.to_datetime(temp["T"].str.replace('T', ' '))
			temp.set_index("T", inplace=True)
			temp.drop(["O", "H", "L", "V", "BV"], 1, inplace=True)

			df = df.join(temp, how="inner")

	for ticker in list(df.columns):

		if ticker != "USDT-BTC":
			df[ticker] = df[ticker] * df["USDT-BTC"]

	return df

def getReturnRate(df, dayCount):
	# dayCount = 7
	df.fillna(0, inplace=True)

	for ticker in list(df.columns):
		for i in range(1, dayCount + 1):

			df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i * 24) / df[ticker]) - 1

	df.fillna(0, inplace=True)
	return df

def main():
	# autoregressive.test()
	# compileData()
	df = loadCompiledData()
	#
	# i = 0
	# tickers = list(df)
	# while i < 10:
	# 	portfolio = df[random.sample(tickers, 10)]
	# 	print(portfolio.columns)
	# 	i = i + 1

	portfolio = df[random.sample(list(df), 10)]
	# print(portfolio.head())

	ticker = list(portfolio)[0]

	portfolioCumReturnRate = pd.DataFrame()
	portfolio3DReturnRate = pd.DataFrame()
	portfolio2DReturnRate = pd.DataFrame()
	portfolio1DReturnRate = pd.DataFrame()

	for ticker in list(portfolio):
		asset = pd.DataFrame()
		asset = portfolio[ticker].to_frame()
		asset["return"] = asset[ticker] - asset.shift(1)[ticker]
		asset["2Dreturn"] = asset[ticker] - asset.shift(2)[ticker]
		asset["3Dreturn"] = asset[ticker] - asset.shift(3)[ticker]
		asset["cumReturn"] = asset["return"].cumsum()

		portfolioCumReturnRate[ticker] = asset[ticker] / (asset[ticker] - asset["cumReturn"])
		portfolio3DReturnRate[ticker] = asset[ticker] / (asset[ticker] - asset["3Dreturn"])
		portfolio2DReturnRate[ticker] = asset[ticker] / (asset[ticker] - asset["2Dreturn"])
		portfolio1DReturnRate[ticker] = asset[ticker] / (asset[ticker] - asset["return"])

	# Assume every day is an end to a iteration

	evalutaion = pd.DataFrame()
	for ticker in list(portfolio):

		evalutaion[ticker] = (portfolio3DReturnRate[ticker] ** 2) * portfolio2DReturnRate[ticker] * \
		                     (portfolio1DReturnRate[ticker] ** 0.5) / portfolioCumReturnRate[ticker]

	print(portfolioCumReturnRate.tail())
	# firstAsset = portfolio[ticker].to_frame()
	# print(firstAsset)

	# visualiseCorrelation(df)

	# dfUSD = loadUSD(df)

	# visualiseCorrelation(dfUSD)

	# dfUSDReturn = getReturnRate(dfUSD, 3)

	# visualiseCorrelation(dfUSDReturn)


if __name__ == "__main__":
	main()