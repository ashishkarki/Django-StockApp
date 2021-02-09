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
    import requests
    import json
    from .models import Stock
    from .my_secrets import IEX_CLOUD_API_KEY

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "Stock addition successful")

            return redirect('add_stock')
    else:
        all_tickers = Stock.objects.all()
        api_resp_list = []

        for ticker in all_tickers:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker) + "/quote?token"
                                                                                                 "=" + IEX_CLOUD_API_KEY)
            try:
                api_response = json.loads(api_request.content)
                api_resp_list.append(api_response)
            except Exception:
                api_response = "Error"

        return render(request, 'add_stock.html', {
            'all_tickers': all_tickers,
            'api_resp_list': __sorter(api_resp_list),
        })


def delete(request, stock_id):
    from .models import Stock

    ticker = Stock.objects.get(pk=stock_id)
    ticker.delete()
    messages.success(request, "Stock Deleted!!")

    return redirect('delete_stock')


def delete_stock(request):
    from .models import Stock

    all_tickers = Stock.objects.all().order_by('ticker')

    return render(request, 'delete_stock.html', {
        'all_tickers': all_tickers
    })


def __get_company_name_as_key(map_obj):
    return map_obj['companyName']


def __sorter(list_of_maps):
    list_of_maps.sort(key=__get_company_name_as_key)
    return list_of_maps
