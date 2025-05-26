import os
import sys
import django
import pandas as pd
from decimal import Decimal, InvalidOperation
import datetime

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))  # spot 폴더
backend_dir = os.path.dirname(current_dir)               # backend 폴더
sys.path.append(backend_dir)

# 장고 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backpjt.settings")
django.setup()

from spot.models import GoldPrice, SilverPrice

def clean_numeric_string(value):
    """숫자 변환 함수 (날짜/문자열 필터링 강화)"""
    if isinstance(value, (datetime.datetime, datetime.date)):
        return None
    
    if isinstance(value, str):
        # 23-May, 24-Feb 형식 필터링
        if any(month in value for month in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']):
            return None
        
        # 쉼표 제거 시도
        value = value.replace(",", "")
        
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None

def upload_excel_to_db(filename, model):
    file_path = os.path.join(backend_dir, filename)
    
    try:
        # 엑셀 읽기 (날짜 파싱 강제 지정)
        df = pd.read_excel(
            file_path,
            engine="openpyxl",
            parse_dates=['Date'],
            date_parser=lambda x: pd.to_datetime(x, errors='coerce')
        )
    except Exception as e:
        print(f"엑셀 파일 읽기 실패: {str(e)}")
        return

    # 컬럼명 매핑
    df.rename(columns={
        'Date': 'date',
        'Close/Last': 'close_last',
        'Volume': 'volume',
        'Open': 'open_price',
        'High': 'high',
        'Low': 'low'
    }, inplace=True)

    # 날짜 필드 유효성 검사
    df = df.dropna(subset=['date'])
    df['date'] = df['date'].dt.date  # datetime → date 변환

    # 숫자 필드 처리
    numeric_cols = ['close_last', 'volume', 'open_price', 'high', 'low']
    for col in numeric_cols:
        df[col] = df[col].apply(clean_numeric_string)
    
    # 모든 숫자 필드가 유효한 행만 필터링
    df = df.dropna(subset=numeric_cols)

    # 데이터 저장 (대량 처리)
    success_count = 0
    error_count = 0
    
    for index, row in df.iterrows():
        try:
            obj, created = model.objects.get_or_create(
                date=row['date'],
                defaults={
                    'close_last': row['close_last'],
                    'volume': row['volume'],
                    'open_price': row['open_price'],
                    'high': row['high'],
                    'low': row['low'],
                }
            )
            if created:
                success_count += 1
            else:
                print(f"중복 데이터 건너뜀: {row['date']}")
        except Exception as e:
            error_count += 1
            print(f"에러 발생 행 {index+2}: {str(e)}")
            continue

    print(f"■ 처리 결과 ■")
    print(f"파일명: {filename}")
    print(f"성공: {success_count}건")
    print(f"실패: {error_count}건")
    print(f"총 행 수: {len(df)}건")
    print("-" * 50)

if __name__ == "__main__":
    upload_excel_to_db('Gold_prices.xlsx', GoldPrice)
    upload_excel_to_db('Silver_prices.xlsx', SilverPrice)
