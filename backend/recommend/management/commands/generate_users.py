from django.core.management.base import BaseCommand
from faker import Faker
import random
from accounts.models import CustomUser  
from finlife.models import DepositProducts, SavingProducts, DepositInterest, DepositJoin, SavingInterest, SavingJoin
from community.models import Article, Comment, Like

class Command(BaseCommand):
    help = '전체 더미 데이터 생성 (유저+예적금+커뮤니티)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=300,
            help='생성할 사용자 수 (기본값: 300)'
        )

    def handle(self, *args, **kwargs):
        fake = Faker('ko_KR')
        total_users = kwargs['total']
        all_users = []
        
        # 예적금 상품 미리 로드
        deposits = list(DepositProducts.objects.all())
        savings = list(SavingProducts.objects.all())

        # 1. 유저 생성 + 예적금 매칭
        for i in range(total_users):
            user = CustomUser.objects.create(
                email=fake.unique.email(),
                nickname=fake.unique.user_name(),
                gender=fake.random_element(['M', 'F']),
                salary=fake.random_element(['under_30m', '30m_50m', '50m_100m', 'over_100m']),
                wealth=fake.random_element(['under_10m', '10m_30m', '30m_50m', '50m_100m', 'over_100m']),
                tendency=fake.random_element(['safe', 'neutral', 'aggressive']),
                deposit_amount=fake.random_element(['under_100k', '100k_500k', '500k_1m', 'over_1m']),
                deposit_period=fake.random_element(['under_6m', '6m_12m', '1y_2y', 'over_2y']),
                has_completed_profile=True
            )
            
            # ✅ 예금 찜 & 가입 (0~3개 랜덤)
            for product in random.sample(deposits, k:=random.randint(0, min(3, len(deposits)))):
                DepositInterest.objects.create(user=user, product=product, created_at=fake.date_time_this_year())
            for product in random.sample(deposits, k:=random.randint(0, min(3, len(deposits)))):
                DepositJoin.objects.create(user=user, product=product, joined_at=fake.date_time_this_year())
                
            # ✅ 적금 찜 & 가입 (0~3개 랜덤)
            for product in random.sample(savings, k:=random.randint(0, min(3, len(savings)))):
                SavingInterest.objects.create(user=user, product=product, created_at=fake.date_time_this_year())
            for product in random.sample(savings, k:=random.randint(0, min(3, len(savings)))):
                SavingJoin.objects.create(user=user, product=product, joined_at=fake.date_time_this_year())
            
            all_users.append(user)
            self.stdout.write(f'[유저] {i+1}/{total_users} 생성 중...', ending='\r')
        
        # 2. 커뮤니티 데이터 생성
        self.stdout.write('\n[커뮤니티] 데이터 생성 시작...')
        for idx, user in enumerate(all_users):
            # 게시글 생성
            for _ in range(random.randint(1, 5)):
                article = Article.objects.create(
                    user=user,
                    category=random.choice(['REVIEW', 'TIP', 'FREE']),
                    title=fake.sentence().rstrip('.'),
                    content='\n'.join(fake.paragraphs(nb=3)),
                    created_at=fake.date_time_this_year()
                )
                
                # 댓글 & 답글 생성
                comments = []
                for _ in range(random.randint(2, 5)):
                    comment_author = random.choice(all_users)
                    parent = random.choice(comments) if comments and random.random() < 0.3 else None
                    comment = Comment.objects.create(
                        article=article,
                        user=comment_author,
                        parent=parent,
                        content=fake.paragraph(),
                        created_at=fake.date_time_this_year()
                    )
                    comments.append(comment)
                
                # 좋아요 생성
                for liker in random.sample(all_users, k:=random.randint(0, len(all_users))):
                    Like.objects.get_or_create(user=liker, article=article)
            
            self.stdout.write(f'[커뮤니티] {idx+1}/{total_users} 처리 중...', ending='\r')
        
        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS(
            f'✅ 완료! 유저 {total_users}명 + 예적금 찜/가입 + 게시글 {Article.objects.count()}개 + 댓글 {Comment.objects.count()}개'
        ))