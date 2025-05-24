from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import json
import requests
from django.conf import settings

# 1) data.json 전체 데이터 제공 (시/도, 시/군/구, 은행 목록)
@api_view(['GET'])
def map_data(request):
    data_path = os.path.join(os.path.dirname(__file__), 'data/data.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 2) 시/도에 해당하는 시/군/구만 제공 (선택)
@api_view(['GET'])
def countries(request):
    province = request.GET.get('province')
    data_path = os.path.join(os.path.dirname(__file__), 'data/data.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data['mapInfo']:
            if item['name'] == province:
                return Response(item['countries'])
        return Response([], status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 3) 카카오 API를 통한 은행 지점 검색
@api_view(['GET'])
def search_banks(request):
    print('KAKAO_API_KEY:', settings.KAKAO_API_KEY)

    province = request.GET.get('province')
    country = request.GET.get('country')
    bank = request.GET.get('bank')
    if not (province and country and bank):
        return Response({'error': '필수 파라미터 누락'}, status=status.HTTP_400_BAD_REQUEST)

    keyword = f"{province} {country} {bank}"
    kakao_api_url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {settings.KAKAO_API_KEY}",
    "KA": "sdk/1.0.0 os/python lang/ko-KR device/pc"  # os를 python으로 변경
}
    params = {"query": keyword}
    try:
        kakao_res = requests.get(kakao_api_url, headers=headers, params=params)
        kakao_res.raise_for_status()
        return Response(kakao_res.json())
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
