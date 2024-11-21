from django.shortcuts import render
from django.conf import settings
from .models import *
from .serializers import *
import requests

from rest_framework.response import Response
from rest_framework.decorators import api_view

BASE_URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
API_KEY = settings.API_KEY_EX


@api_view(['GET'])
def load_api_data(request):
    URL = BASE_URL
    params = {
        'authkey': API_KEY,
        # 'searchdate': ,  # default: 현재일
        'data': 'AP01',
    }
    exchanges = requests.get(URL, params=params).json()
    
    for exchange in exchanges:
        if Exchange.objects.filter(cur_nm = exchange.get('cur_nm')):
            continue
        
        save_data = {
          'cur_unit': exchange.get('cur_unit'),
          'cur_nm': exchange.get('cur_nm'),
          'ttb': float(exchange.get('ttb').replace(',', '')),
          'tts': float(exchange.get('tts').replace(',', '')),
          'deal_bas_r': float(exchange.get('deal_bas_r').replace(',', '')),
          'bkpr': float(exchange.get('bkpr').replace(',', '')),
          'yy_efee_r': float(exchange.get('yy_efee_r').replace(',', '')),
          'ten_dd_efee_r': float(exchange.get('ten_dd_efee_r').replace(',', '')),
          'kftc_deal_bas_r': float(exchange.get('kftc_deal_bas_r').replace(',', '')),
          'kftc_bkpr': float(exchange.get('kftc_bkpr').replace(',', '')),
        }

        serializer = ExchangeSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
          
    return Response({"message": "환율 데이터 저장이 완료되었습니다."})
    # return Response(exchanges)


@api_view(['GET'])
def get_list(request):
    exchages = Exchange.objects.all()
    serializer = ExchangeSerializer(exchages, many=True)
    return Response(serializer.data)
