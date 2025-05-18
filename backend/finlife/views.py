from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods,require_POST
from django.http import JsonResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests

from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer

# Create your views here.

@api_view(['GET',])
def get_deposit_products(request):
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'

    params = {
        'auth': settings.FIN_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    response = requests.get(BASE_URL, params = params).json()['result']
   
    deposit_baselist = response['baseList']
    deposit_optionlist = response['optionList']

    # 상품 정보 저장 및 직렬화
    for base in deposit_baselist:
        if DepositProducts.objects.filter(fin_prdt_cd=base['fin_prdt_cd']):
            continue
        deposit_product = {
            'dcls_month' : base.get('dcls_month'),
            'fin_prdt_cd': base.get('fin_prdt_cd'),
            'fin_co_no': base.get('fin_co_no'),
            'kor_co_nm': base.get('kor_co_nm'),
            'fin_prdt_nm': base.get('fin_prdt_nm'),
            'join_way': base.get('join_way'),
            'mtrt_int': base.get('mtrt_int'),
            'spcl_cnd': base.get('spcl_cnd'),
            'join_deny': base.get('join_deny'),
            'etc_note': base.get('etc_note'),
            'max_limit': base.get('max_limit')
        }
        serializer = DepositProductsSerializer(data=deposit_product)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
        
    # deposit 옵션 정보 저장 및 직렬화
    for opt in deposit_optionlist:
        prdt_cd = opt['fin_prdt_cd']
        products = DepositProducts.objects.filter(fin_prdt_cd=prdt_cd)
        for product in products:
            deposit_option = {
                'intr_rate_type': opt.get('intr_rate_type'),
                'intr_rate_type_nm': opt.get('intr_rate_type_nm'),
                'save_trm': opt.get('save_trm'),
                'intr_rate': opt.get('intr_rate'),
                'intr_rate2': opt.get('intr_rate2'),
            }
            serializer = DepositOptionsSerializer(data=deposit_option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(deposit_product = product)
    return Response('데이터 가져오기 성공!!')

# 적금 saving ====================================
@api_view(['GET'])
def get_saving_products(request):
    
    BASE_URL ='http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'

    params = {
        'auth': settings.FIN_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    response = requests.get(BASE_URL, params = params).json()['result']
   
    saving_baselist = response['baseList']
    saving_optionlist = response['optionList']

    # 상품 정보 저장 및 직렬화
    for base in saving_baselist:
        if SavingProducts.objects.filter(fin_prdt_cd=base['fin_prdt_cd']):
            continue
        saving_product = {
            'dcls_month' : base['dcls_month'],
            'fin_co_no': base['fin_co_no'],
            'kor_co_nm': base['kor_co_nm'],
            'fin_prdt_cd': base['fin_prdt_cd'],
            'fin_prdt_nm': base['fin_prdt_nm'],
            'join_way': base['join_way'],
            'mtrt_int': base['mtrt_int'],
            'spcl_cnd': base['spcl_cnd'],
            'join_deny': base['join_deny'],
            'etc_note': base['etc_note'],
            'max_limit': base['max_limit']
        }
        serializer = SavingProductsSerializer(data=saving_product)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
        
    # saving 옵션 정보 저장 및 직렬화
    for opt in saving_optionlist:
        prdt_cd = opt['fin_prdt_cd']
        products =  SavingProducts.objects.filter(fin_prdt_cd=prdt_cd)
        for product in products:
            saving_option = {
                'intr_rate_type': opt.get('intr_rate_type'),
                'intr_rate_type_nm': opt.get('intr_rate_type_nm'),
                'rsrv_type': opt.get('rsrv_type'),
                'rsrv_type_nm': opt.get('rsrv_type_nm'),
                'save_trm': opt.get('save_trm'),
                'intr_rate': opt.get('intr_rate'),
                'intr_rate2': opt.get('intr_rate2'),  
            }
            serializer = SavingOptionsSerializer(data=saving_option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(saving_product = product)
    return Response('데이터 가져오기 성공!')

    



