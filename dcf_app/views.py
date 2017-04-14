from django.shortcuts import render
from django.http import HttpResponse
import scraper

def index(request):
	return render(request, 'dcf_app/index.html')

def results(request):
	if request.method == 'POST':
		ticker = request.POST.get("ticker")
		company_name = scraper.getCompanyNameFromTicker(ticker)
	else:
		return
	return render(request, 'dcf_app/results.html', {'company_name' : company_name })