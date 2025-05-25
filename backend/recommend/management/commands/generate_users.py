from django.core.management.base import BaseCommand
from faker import Faker
import random
from accounts.models import CustomUser  
from finlife.models import DepositProducts, SavingProducts

class Command(BaseCommand):
    help = '더미 사용자 생성 및 예적금 상품 랜덤 매칭'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=250,
            help='생성할 사용자 수 (기본값: 250)'
        )

    def handle(self, *args, **kwargs):
        fake = Faker('ko_KR')
        total_users = kwargs['total']
        
        deposits = DepositProducts.objects.all()
        savings = SavingProducts.objects.all()
        
        for i in range(total_users):
            user = CustomUser.objects.create(
                email=fake.unique.email(),
                nickname=fake.unique.user_name(),
                gender=fake.random_element(['M', 'F']),
                salary=fake.random_element(['under_30m', '30m_50m', '50m_100m', 'over_100m']),
                wealth=fake.random_element(['under_10m', '10m_30m', '30m_50m', '50m_100m', 'over_100m']),
                tendency=fake.random_element(['safe', 'neutral', 'aggressive']),
                deposit_amount=fake.random_element(['under_100k', '100k_500k', '500k_1m', 'over_1m']),
                deposit_period=fake.random_element(['under_6m', '6m_12m', '1y_2y', 'over_2y'])
            )
            
            # 예금 상품 매칭 (1~3개 랜덤)
            selected_deposits = random.sample(list(deposits), k=random.randint(1,3))
            user.joined_deposits.add(*selected_deposits)
            
            # 적금 상품 매칭 (1~3개 랜덤)
            selected_savings = random.sample(list(savings), k=random.randint(1,3))
            user.joined_savings.add(*selected_savings)
            
            # 진행상황 출력
            self.stdout.write(f'{i+1}/{total_users} 생성 중...', ending='\r')
        
        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS(f'성공적으로 {total_users}명 생성 및 매칭 완료!'))
