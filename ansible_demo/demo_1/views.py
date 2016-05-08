from django.shortcuts import render

from rest_framework.decorators import api_view


# Create your views here.
@api_view(['GET', 'POST'])
def server_item_config(request):
    if request.method == 'GET':
        return render(request, 'server_item_config.html')

