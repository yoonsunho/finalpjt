# 엑셀파일 db로 옮겨줄 script
import os
import sys
import django
import pandas as pd

# 파이썬 경로에 backend 폴더 추가 (backpjt를 찾을 수 있도록)
current_dir = os.path.dirname(os.path.abspath(__file__))  # spot 폴더
backend_dir = os.path.dirname(current_dir)               # backend 폴더
sys.path.append(backend_dir)

# 장고 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backpjt.settings")
django.setup()

from spot.models import GoldPrice, SilverPrice

def upload_excel_to_db(filename, model):
    # 엑셀 파일 읽기
    file_path = os.path.join(backend_dir,filename)
    df = pd.read_excel(file_path, engine="openpyxl")

    # 각 행을 모델 인스턴스로 변환해서 저장
    for _, row in df.iterrows():
        model.objects.create(
            date=row['date'],
            close_last=row['close_last'],
            volume=row['volume'],
            open_price=row['open_price'],
            high=row['high'],
            low=row['low'],
        )
    print(f"{filename} 데이터 저장 완료!")

if __name__ == "__main__":
    upload_excel_to_db('Gold_prices.xlsx', GoldPrice)
    upload_excel_to_db('Silver_prices.xlsx', SilverPrice)
