# backend/recommend/utils/ai.py
from openai import OpenAI
from django.conf import settings

def generate_recommend_reason(user, product):

    """추천 이유 생성"""
    client = OpenAI(api_key = settings.OPENAI_API_KEY)  # 클라이언트 초기화
    max_rate = product.max_rate() or 0  # None 대신 0 사용

    prompt = f"""
    [역할] 금융 상품 추천 전문가
    [사용자 정보]
    - 닉네임: {user.nickname}
   - 투자 성향: {user.get_tendency_display()}
    - 예치 기간: {user.get_deposit_period_display()}
    - 예치 금액: {user.get_deposit_amount_display()}
    
    [상품 정보]
    - 이름: {product.fin_prdt_nm}
    - 은행: {product.kor_co_nm}
    - 최대 금리: {max_rate}%
    
    [요청사항]
    위 사용자에게 이 상품을 추천하는 이유를 3문장 이내로 작성해주세요.
    금리, 기간, 사용자 성향을 반드시 언급해야 합니다.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 전문 금융 어드바이저입니다. 친절하고 명확한 설명을 부탁드립니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    return response.choices[0].message.content.strip()
