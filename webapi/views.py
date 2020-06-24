from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework import status
from rest_framework.response import Response
#from rest_framework.decorators import JSONParser

from elastic.completionapiwrapper import query_completion, create_name_index

@api_view(['GET'])
#@parser_classes([parser_classes.JSONParser])
def query(request):
    return Response("hello", status=status.HTTP_200_OK)


@api_view(['POST'])
def index(request):   
    if request.method == 'POST':
        all_data = request.data  
        try:
            create_name_index(all_data) 
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("Index created!", status=status.HTTP_200_OK)