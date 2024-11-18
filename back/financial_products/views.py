from django.shortcuts import render
from django.conf import settings
from .models import *
from .serializers import *
import requests

from rest_framework.response import Response
from rest_framework.decorators import api_view

BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
API_KEY = settings.API_KEY

topFinGrpNo = ['030200', '030300', '050000', '060000']

@api_view(['GET'])
def load_api_data(request):
    for type in topFinGrpNo:
        for i in range(1, 11):
            # 예금
            deposit_URL = BASE_URL + 'depositProductsSearch.json'
            deposit_params = {
                'auth': API_KEY,
                'topFinGrpNo': type,
                'pageNo' : f'{i}',
            }
            deposits = requests.get(deposit_URL, params=deposit_params).json()
            
            print(f'deposit {type}/{i}', deposits.get('result').get('max_page_no'))
            
            for deposit in deposits.get('result').get('baseList'):
                if Deposit.objects.filter(fin_prdt_cd = deposit.get('fin_prdt_cd')):
                    continue
                
                save_data = {
                    'fin_prdt_cd': deposit.get('fin_prdt_cd'),
                    'fin_prdt_nm': deposit.get('fin_prdt_nm'),
                    'fin_co_no': deposit.get('fin_co_no'),
                    'kor_co_nm': deposit.get('kor_co_nm'),
                    'etc_note': deposit.get('etc_note'),
                    'join_deny': deposit.get('join_deny'),
                    'join_member': deposit.get('join_member'),
                    'join_way': deposit.get('join_way'),
                    'spcl_cnd': deposit.get('spcl_cnd'),
                    'max_limit': deposit.get('max_limit'),
                }

                serializer = DepositSerializer(data=save_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            
            for option in deposits.get('result').get('optionList'):
                deposit = Deposit.objects.get(fin_prdt_cd = option.get('fin_prdt_cd'))
                
                save_option = {
                    'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                    'intr_rate': option.get('intr_rate', -1),
                    'intr_rate2': option.get('intr_rate2', -1),
                    'save_trm': option.get('save_trm', -1),
                }

                serializer = DepositOptionSerializer(data=save_option)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(deposit=deposit)
                  
            # 적금
            saving_URL = BASE_URL + 'savingProductsSearch.json'
            saving_params = {
                'auth': API_KEY,
                'topFinGrpNo': type,
                'pageNo' : f'{i}',
            }

            savings = requests.get(saving_URL, params=saving_params).json()

            print(f'saving {type}/{i}', savings.get('result').get('max_page_no'))

            for saving in savings.get('result').get('baseList'):
                if Saving.objects.filter(fin_prdt_cd = saving.get('fin_prdt_cd')):
                    continue
                
                save_data = {
                    'fin_prdt_cd': saving.get('fin_prdt_cd'),
                    'fin_prdt_nm': saving.get('fin_prdt_nm'),
                    'fin_co_no': saving.get('fin_co_no'),
                    'kor_co_nm': saving.get('kor_co_nm'),
                    'etc_note': saving.get('etc_note'),
                    'join_deny': saving.get('join_deny'),
                    'join_member': saving.get('join_member'),
                    'join_way': saving.get('join_way'),
                    'spcl_cnd': saving.get('spcl_cnd'),
                    'max_limit': saving.get('max_limit'),
                }

                serializer = SavingSerializer(data=save_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            
            for option in savings.get('result').get('optionList'):
                saving = Saving.objects.get(fin_prdt_cd = option.get('fin_prdt_cd'))
                
                save_option = {
                    'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                    'rsrv_type_nm': option.get('rsrv_type_nm'),
                    'intr_rate': option.get('intr_rate', -1),
                    'intr_rate2': option.get('intr_rate2', -1),
                    'save_trm': option.get('save_trm', -1),
                }

                serializer = SavingOptionSerializer(data=save_option)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(saving=saving)
          
    return Response({"message": "금융 데이터 저장이 완료되었습니다."})


@api_view(['GET'])
def deposit_list(request):
    deposits = Deposit.objects.all()
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def deposit_option_list(request):
    deposit_options = DepositOption.objects.all()
    serializer = DepositOptionSerializer(deposit_options, many=True)

    return Response(serializer.data)