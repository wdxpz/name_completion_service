import json
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework import status
from rest_framework.response import Response
#from rest_framework.decorators import JSONParser

from elastic.completionapiwrapper import query_completion, create_name_index
from utils.logger import getLogger
logger = getLogger(__name__)
logger.propagate = False

@api_view(['GET'])
#@parser_classes([parser_classes.JSONParser])
def query(request):
    if 'term' not in request.query_params.keys():
        return Response(('key-value ?term=* required'), status=status.HTTP_400_BAD_REQUEST)
    
    q = request.query_params['term']  
    if q != '':
        logger.info('user query: {}'.format(q))
        results = query_completion(q)
        logger.info(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
    #suggestion = query_completion(request.query_params['term'])
    #return Response(suggestion, status=status.HTTP_200_OK)


@api_view(['POST'])
def index(request):   
    if request.method == 'POST':
        all_data = request.data  
        try:
            create_name_index(all_data) 
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("Index created!", status=status.HTTP_200_OK)