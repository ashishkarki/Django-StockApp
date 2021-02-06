from django.shortcuts import render


# Create your views here.


def home(request):
    import requests
    import json
    from quotes import my_secrets

    ticker = 'aapl'  # request.POST['ticker']
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token"
                                                                                    "=" + my_secrets.IEX_CLOUD_API_KEY)
    try:
        api_response = json.loads(api_request.content)
    except Exception as e:
        api_response = "Error"

    return render(request, 'home.html', {
        'api_response': api_response
    })


def about(request):
    return render(request, 'about.html', {})
