from django.shortcuts import render
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt 
import dcf_algo as dcf
import scraper
import django

def index(request):
	return render(request, 'dcf_app/index.html')

def results(request):
	if request.method == 'POST':
		ticker = request.POST.get("ticker")
		company_name = scraper.getCompanyNameFromTicker(ticker)
		model_data = dcf.revenue_growth_model(ticker)
		x = model_data['x']
		y = model_data['y']
		best_model = model_data['max_cv']
		predicted = model_data['predicted']


		plt.scatter(x, y)  # scatterplot of points
		plt.plot(x, predicted, color='blue', linewidth=3) # plot the linear fit

		canvas = FigureCanvas(plt.figure(1))
		response=django.http.HttpResponse(content_type='image/png')
		canvas.print_png(response)
		return response
	#return render(request, 'dcf_app/results.html', {'company_name' : company_name })