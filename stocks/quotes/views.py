from django.shortcuts import render


# Create your views here.

def home(request):
    import requests
    import json

    ticker = 'aapl' # request.POST['ticker']
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token"
                                                                                    "=pk_062031d20883444f9ea74e2610fe2011")
    try:
        api_response = json.loads(api_request.content)
    except Exception as e:
        api_response = "Error"

    return render(request, 'home.html', {
        'api_response': api_response
    })


def about(request):
    return render(request, 'about.html', {})
