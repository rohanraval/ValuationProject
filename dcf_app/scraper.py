# Rohan S Raval
from bs4 import BeautifulSoup
from yahoo_finance import Share
import requests
import re

"""
	- Inputs: Stock Ticker of the public company.
	- Return: Registered name of the company that has that ticker.
"""
def getCompanyNameFromTicker(ticker):
	company = Share(ticker).get_name()
	if company is not None:
		return company
	else:
		return None

"""
	- Helper function for getIncomeStatement, getBalanceSheet, and getCashFlowStatement function
	- Inputs: The name of the data to be extracted from the API
		output, e.g. "EBITDA", and the API output HTML.
	- Return: A dictionary { year : value } that represents the values
		of the data_name in the available years (currently, 2012->2016 and TTM).
"""
def getDataDictFromHTML(data_name, html_soup):
 	data = {}
 	data_html = re.search("^" + data_name + ",(.*)$", str(html_soup), re.MULTILINE) #regex search through html_soup
 	if data_html:
 		data_output = data_html.group(1)
 		data_array = data_output.split(',') #split data on ',' for year
 		for i in range(0,5):
 			if data_array[i] != '':
 				data[int("20"+str(i+12))] = int(data_array[i])
		#if len(data_array) > 5:
		#	data["TTM"] = int(data_array[5]) #TTM data only exists for I/S and CFS
	return data


"""
	- Inputs: Stock Ticker of the public company.
	- Function: With Morningstar API to retreive I/S data using BS4.
	Using the helper function getDataDictFromHTML, orgainizes retrieved data into dictionaries representing relevant facets of the I/S over time.
	- Returns: Dict containing revenues, cogs, sga and ebitda dicts
"""
def getIncomeStatement(ticker):
	url = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="+ticker+"&reportType=is&period=12&dataType=A&order=asc&columnYear=10&number=3"
	soup = BeautifulSoup(requests.get(url).text, "lxml")
	data = soup.find("p").get_text() # this contains the API output with all the data as HTML
	#print data

 	revenues = getDataDictFromHTML("Revenue", data)
 	cogs = getDataDictFromHTML("Cost of revenue", data)
 	sga = getDataDictFromHTML("\"Sales, General and administrative\"", data)
 	operating_income = getDataDictFromHTML("Operating income", data)
 	interest_expense = getDataDictFromHTML("Interest Expense", data)
 	ebitda = getDataDictFromHTML("EBITDA", data)

 	return { "Revenue" : revenues,
 			"COGS" : cogs,
 			"SG&A" : sga,
 			"Operating Income" : operating_income,
 			"Interest Expense" : interest_expense,
 			"EBITDA" : ebitda }

"""
	- Inputs: Stock Ticker of the public company.
	- Function: With Morningstar API to retreive B/S data using BS4.
	Using the helper function getDataDictFromHTML, orgainizes retrieved data into dictionaries representing relevant facets of the B/S over time.
	- Returns: Dict containing revenues, cogs, sga and ebitda dicts
"""
def getBalanceSheet(ticker):
	url = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="+ticker+"&reportType=bs&period=12&dataType=A&order=asc&columnYear=10&number=3"
	soup = BeautifulSoup(requests.get(url).text, "lxml")
	data = soup.find("p").get_text()

	total_liab = getDataDictFromHTML("Total liabilities", data)

	total_current_assets = getDataDictFromHTML("Total current assets", data)
	if total_current_assets is None:
		total_current_assets = getDataDictFromHTML("Total assets", data)

	total_current_liab = getDataDictFromHTML("Total current liabilities", data)
	if total_current_liab is None:
		total_current_liab = total_liab

	working_capital = {}
	for i in range(len(total_current_assets.keys())):
		working_capital[total_current_assets.keys()[i]] = total_current_assets[total_current_assets.keys()[i]] - total_current_liab[total_current_assets.keys()[i]]

	return { "Working Capital" : working_capital,
			"Total Liabilities" : total_liab }

"""
	- Inputs: Stock Ticker of the public company.
	- Function: With Morningstar API to retreive CFS data using BS4.
	Using the helper function getDataDictFromHTML, orgainizes retrieved data into dictionaries representing relevant facets of the CFS over time.
	- Returns: Dict containing D&A and CAPEX dicts
"""
def getCashFlowStatement(ticker):
 	url = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="+ticker+"&reportType=cf&period=12&dataType=A&order=asc&columnYear=10&number=3"
	soup = BeautifulSoup(requests.get(url).text, "lxml")
	data = soup.find("p").get_text()
	#print str(data)

	depamort = getDataDictFromHTML("Depreciation & amortization", data)
	capex = getDataDictFromHTML("Capital expenditure", data)

	return { "D&A" : depamort,
			"CAPEX" : capex }

def getFinancialData(ticker):
	company_name = getCompanyNameFromTicker(ticker)
	income_statement = getIncomeStatement(ticker)
	balance_sheet = getBalanceSheet(ticker)
	cash_flow_statement = getCashFlowStatement(ticker)

	financial_data = dict(income_statement)
	financial_data.update(balance_sheet)
	financial_data.update(cash_flow_statement)

	return financial_data


############# MAIN METHOD #############
# ticker = raw_input("enter ticker: ")

# if ticker is not None or getCompanyNameFromTicker(ticker) is not None:

# 	company_name = getCompanyNameFromTicker(ticker)
# 	income_statement = getIncomeStatement(ticker)
# 	balance_sheet = getBalanceSheet(ticker)
# 	cash_flow_statement = getCashFlowStatement(ticker)

# 	financial_data = dict(income_statement)
# 	financial_data.update(balance_sheet)
# 	financial_data.update(cash_flow_statement)

# 	print financial_data

# else:
# 	print "INVALID TICKER! TERMINATING PROGRAM..."
