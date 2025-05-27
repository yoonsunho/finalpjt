# finalpjt

1. db 생성 명령어(순서대로)
$ python manage.py seed_products - 예적금 데이터
$ python manage.py generate_users   - 더미 유저데이터 삽입(좋아요도 랜덤으로 넣을까 고민중)
$ python spot/gold_price_upload.py - 현물데이터

# 현물 상품 비교
엑셀의 파일을 db에 넣어야 함.
1. 준비 사항
pip install pandas openpyxl

- db에 넣는 명령
python spot/gold_price_upload.py

# 공동저축 + web socket
[프론트엔드]
   |           \
[HTTP 요청]   [WebSocket 연결]
   |                |
[urls.py]        [asgi.py → routing.py]
   |                |
[views.py]       [consumers.py]
   |                |
[models.py]      [models.py]
   |                |
[DB]             [DB]

REST API: urls.py → views.py → models.py → DB

WebSocket: asgi.py + routing.py → consumers.py → models.py → DB