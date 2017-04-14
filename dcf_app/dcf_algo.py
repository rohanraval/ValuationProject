# Algorithm for DCF Analysis developed by Rohan Raval and Amar Singh
import scraper
import numpy as np
import pandas as pd
from scipy import sparse
from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import cross_val_score

# FREE CASH FLOW
def free_cash_flow(revenue, cogs, sga, da, capex, nwc):
	return


def revenue_growth_model(ticker):
	financial_data = scraper.getFinancialData(ticker)

	revenue = financial_data["Revenue"]
	df = pd.DataFrame.from_dict(revenue.items())
	x = df[0].to_frame() # x-values are the years
	y = df[1].to_frame() # y-values are revenue values (given)

	### linear modeling ###

	""" make the models """
	ols_reg = linear_model.LinearRegression() #ordinary least squares
	ridge_reg = linear_model.Ridge() #ridge regression
	lasso_reg = linear_model.Lasso() #lasso regression
	LARS_reg = linear_model.LassoLars() #least angle regression (on lasso)
	b_ridge_reg = linear_model.BayesianRidge() #bayesian ridge regression
	ard_reg = linear_model.ARDRegression() #bayesian ARD regression
	sgd_reg =  linear_model.SGDRegressor() #stochastic gradient descent regression
	ransac_model = linear_model.RANSACRegressor(ols_reg) #fit linear model with RANdom SAmple Consensus algorithm


	""" fit the models to a regression function based on data """
	ols_reg.fit(x,y)
	ridge_reg.fit(x,y)
	lasso_reg.fit(x,y)
	LARS_reg.fit(x,y)
	b_ridge_reg.fit(x,y)
	ard_reg.fit(x,y)
	sgd_reg.fit(x,y)
	ransac_model.fit(x,y)

	### k-cross validation ### 

	cv_scores= {
		'ols_scores' : ols_reg.score(x,y),
		'ridge_scores' : ridge_reg.score(x,y),
		'lasso_scores' : lasso_reg.score(x,y),
		'LARS_scores' : LARS_reg.score(x,y),
		'b_ridge_scores' : b_ridge_reg.score(x,y),
		'ard_scores' : ard_reg.score(x,y),
		'sgd_scores' : sgd_reg.score(x,y),
		'ransac_scores' : ransac_model.score(x,y)
	}
	vals = list(cv_scores.values())
	keys = list(cv_scores.keys())

	max_cv = keys[vals.index(max(vals))]
	print vals
	print max_cv

	predicted = []
	if max_cv == 'ols_scores':
		predicted = ols_reg.predict(x)
	elif max_cv == 'ridge_scores':
		predicted = ridge_reg.predict(x)
	elif max_cv == 'lasso_scores':
		predicted = lasso_reg.predict(x)
	elif max_cv == 'LARS_scores':
		predicted = LARS_reg.predict(x)
	elif max_cv == 'b_ridge_scores':
		predicted = b_ridge_reg.predict(x)
	elif max_cv == 'ard_scores':
		predicted = ard_reg.predict(x)
	elif max_cv == 'sgd_scores':
		predicted = sgd_reg.predict(x)
	else:
		predicted = ransac_model.predict(x)

	return {
		'x': x, 'y': y, 
		'max_cv': max_cv, 'predicted': predicted 
	}

# algorithm
"""
reg = linear_model.LinearRegression() # do the linear regression
reg.fit(x, y) # get the linear fit, using x and y(revenues from df)
m = reg.coef_[0][0] # slope of fitted line
b = reg.intercept_[0] # intercept of fitted line

predicted = reg.predict(x)
"""
#print m, b

# plt.scatter(x, y)  # scatterplot of points
# plt.plot(x, predicted, color='blue', linewidth=3) # plot the linear fit
# plt.show()
