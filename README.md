# finalpjt
# 프로 젝트 소개 
(밑줄)
이 프로젝트는 사용자가 다양한 예적금 상품을 쉽고 빠르게 조회하고, AI 기반 필터링을 통해 개인의 금융 성향에 맞는 맞춤형 상품을 추천받을 수 있는 금융 플랫폼입니다. 또한, 여러 사용자가 함께 참여할 수 있는 공동 저축방 기능을 제공하여 목표 금액을 함께 모으는 경험을 지원합니다. 금/은 등 현물 시세 확인과, 주변 은행 위치를 지도로 검색하는 기능도 포함되어 있어, 사용자에게 종합적인 금융 정보를 제공합니다.


1. 팀원 정보 및 업무 분담 내역
윤선호 : Back-end 개발, AI 상품 추천 알고리즘 구현, 현물 시세 조회 시스템, Google 로그인 회원가입
서지원: Front-end 개발, UI/UX디자인, 

2. 설계 내용(아키텍처 등) 및 실제 구현 정도

3. 데이터베이스 모델링

4. 금융 상품 추천 알고리즘에 대한 기술적 설명

5. 서비스 대표 기능들에 대한 설명

6. 생성형 AI 를 활용한 부분

7. 기타(느낀 점, 후기 등)


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