from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockForm

# Create your views here.


def home(request):
    import requests
    import json
    from .my_secrets import IEX_CLOUD_API_KEY

    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token"
                                                                                        "=" + IEX_CLOUD_API_KEY)
        try:
            api_response = json.loads(api_request.content)
        except Exception:
            api_response = "Error"

        return render(request, 'home.html', {
            'api_response': api_response
        })
    else:
        return render(request, 'home.html', {
            'info': 'Please enter a ticker symbol above..'
        })


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    from .models import Stock

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "Stock addition successful")

            return redirect('add_stock')
    else:
        all_tickers = Stock.objects.all()

        return render(request, 'add_stock.html', {
            'all_tickers': all_tickers
        })
