from django.shortcuts import render,redirect
from .models import Stock   
from .forms import StockForm
from django.contrib import messages


# home page
def home(request):
	import requests # both imports are needed 
	import json		# in order to make an api call

	if request.method == 'POST':
		ticker = request.POST['ticker']
		# pk_062031d20883444f9ea74e2610fe2011
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_062031d20883444f9ea74e2610fe2011")

		try:
			api = json.loads(api_request.content)
		except	Exception as e:
			api = "Error..."
		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': "Enter a ticker symbol above"})

# about page
def about(request):
	return render(request, 'about.html', {})

# add_stock page
def add_stock(request):
	import requests # both imports are needed 
	import json		# in order to make an api call

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added"))
			return redirect('add_stock')
	else:
		ticker = Stock.objects.all()
		output = []
		for tickerItem in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(tickerItem) + "/quote?token=pk_062031d20883444f9ea74e2610fe2011")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except	Exception as e:
				api = "Error..."
			
		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock has been deleted"))
	return redirect(delete_stock)


# delete_stock page
def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})



























