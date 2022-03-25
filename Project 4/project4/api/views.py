from urllib import response
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET'])
def new_post(request):
    data = request.data
    print(type(data))
    return Response(data)