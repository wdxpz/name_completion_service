from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework import status
from rest_framework.response import Response
#from rest_framework.decorators import JSONParser

@api_view(['GET'])
#@parser_classes([parser_classes.JSONParser])
def query(request):
    return Response("hello", status=status.HTTP_200_OK)


@api_view(['POST'])
def index(request):      
    return Response("Command Accepted!", status=status.HTTP_202_ACCEPTED)