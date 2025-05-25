# recommend/utils/recommend.py
from django.db.models import Count  
from django.contrib.auth import get_user_model
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

User = get_user_model()

def get_user_vector(user):
    """사용자 프로필을 숫자 벡터로 변환"""
    # 각 필드의 가능한 모든 선택지 (모델 정의와 일치해야 함)
    vector = []
    
    # 성별 (M:0, F:1)
    vector.append(0 if user.gender == 'M' else 1)
    
    # 연봉 (under_30m → 0, 30m_50m → 1, ...)
    salary_map = {'under_30m':0, '30m_50m':1, '50m_100m':2, 'over_100m':3}
    vector.append(salary_map[user.salary])
    
    # 재산 (under_10m → 0, 10m_30m →1, ...)
    wealth_map = {'under_10m':0, '10m_30m':1, '30m_50m':2, '50m_100m':3, 'over_100m':4}
    vector.append(wealth_map[user.wealth])
    
    # 투자성향 (safe:0, neutral:1, aggressive:2)
    tendency_map = {'safe':0, 'neutral':1, 'aggressive':2}
    vector.append(tendency_map[user.tendency])
    
    # 예치금액 (under_100k:0, ..., over_1m:3)
    deposit_amount_map = {'under_100k':0, '100k_500k':1, '500k_1m':2, 'over_1m':3}
    vector.append(deposit_amount_map[user.deposit_amount])
    
    # 예치기간 (under_6m:0, ..., over_2y:3)
    deposit_period_map = {'under_6m':0, '6m_12m':1, '1y_2y':2, 'over_2y':3}
    vector.append(deposit_period_map[user.deposit_period])
    
    return np.array(vector)

def get_similar_users(target_user, n=5):
    """유사한 사용자 상위 n명 반환"""
    all_users = User.objects.exclude(id=target_user.id)
    
    # 벡터 변환
    target_vector = get_user_vector(target_user).reshape(1, -1)
    user_vectors = [get_user_vector(user) for user in all_users]
    
    # 코사인 유사도 계산
    similarities = cosine_similarity(target_vector, user_vectors)[0]
    
    # 상위 n개 인덱스 추출 (numpy int64 → Python int 변환)
    top_indices = similarities.argsort()[-n:][::-1]
    top_indices = [int(i) for i in top_indices]  # 변환 추가s


    return [all_users[i] for i in top_indices]

def recommend_products(target_user, n=3):
    """추천 상품 반환"""
    similar_users = get_similar_users(target_user)
    
    # 유사 사용자들이 가입한 상품 수집
    deposit_ids = []
    saving_ids = []
    
    for user in similar_users:
        deposit_ids += list(user.joined_deposits.values_list('id', flat=True))
        saving_ids += list(user.joined_savings.values_list('id', flat=True))
    
    # 상품 조회 및 정렬 (가입자 많은 순)
    from finlife.models import DepositProducts, SavingProducts
    
    deposits = DepositProducts.objects.filter(id__in=deposit_ids)
    savings = SavingProducts.objects.filter(id__in=saving_ids)
    
    # 상위 n개 추출 (가입자 수 기준)
    top_deposits = deposits.annotate(joined_count=Count('joined_users')).order_by('-joined_count')[:n]
    top_savings = savings.annotate(joined_count=Count('joined_users')).order_by('-joined_count')[:n]
    
    return {
        'deposits': top_deposits,
        'savings': top_savings
    }
