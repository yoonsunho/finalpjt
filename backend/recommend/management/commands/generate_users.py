from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
from accounts.models import CustomUser  
from finlife.models import DepositProducts, SavingProducts, DepositInterest, DepositJoin, SavingInterest, SavingJoin
from community.models import Article, Comment, Like
from savingroom.models import SavingRoom, SavingParticipant, SavingDeposit

class Command(BaseCommand):
    help = '전체 더미 데이터 생성 (유저+예적금+커뮤니티)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=250,
            help='생성할 사용자 수 (기본값: 250)'
        )
        
    def clean_text(self, text):
        return ''.join(
            c for c in text 
            if (ord('가') <= ord(c) <= ord('힣')) or 
               (ord('0') <= ord(c) <= ord('9')) or 
               (c in [' ', '.', '!', '?', ',', '\n'])
        )

    def handle(self, *args, **kwargs):
        fake = Faker('ko_KR')
        total_users = kwargs['total']
        all_users = []

        # 예적금 상품 미리 로드
        deposits = list(DepositProducts.objects.all())
        savings = list(SavingProducts.objects.all())
        if not deposits and not savings:
            self.stdout.write(self.style.ERROR('❌ 예적금/적금 상품이 없습니다. 먼저 상품 데이터를 로드해주세요.'))
            return

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

            def get_aware_datetime():
                naive_dt = fake.date_time_this_year()
                return timezone.make_aware(naive_dt, timezone.get_current_timezone())

            # 예금 찜 & 가입
            for product in random.sample(deposits, k:=random.randint(0, min(3, len(deposits)))):
                DepositInterest.objects.create(user=user, product=product, created_at=get_aware_datetime())
            for product in random.sample(deposits, k:=random.randint(0, min(3, len(deposits)))):
                DepositJoin.objects.create(user=user, product=product, joined_at=get_aware_datetime())

            # 적금 찜 & 가입
            for product in random.sample(savings, k:=random.randint(0, min(3, len(savings)))):
                SavingInterest.objects.create(user=user, product=product, created_at=get_aware_datetime())
            for product in random.sample(savings, k:=random.randint(0, min(3, len(savings)))):
                SavingJoin.objects.create(user=user, product=product, joined_at=get_aware_datetime())

            all_users.append(user)
            self.stdout.write(f'[유저] {i+1}/{total_users} 생성 중...', ending='\r')

        # 2. 카테고리별 15개 게시글만 생성
        self.stdout.write('\n[커뮤니티] 데이터 생성 시작...')
        categories = ['REVIEW', 'TIP', 'FREE']
        articles = []

        for category in categories:
            for i in range(15):
                # REVIEW는 상품 랜덤 연결, 나머지는 None
                product = None
                if category == 'REVIEW':
                    products = deposits + savings
                    product = random.choice(products) if products else None

                article = Article.objects.create(
                    user=random.choice(all_users),
                    category=category,
                    title=self.generate_korean_title(category, product),
                    content=self.generate_korean_content(category, product),
                    created_at=get_aware_datetime()
                )
                articles.append((article, category))
                self.stdout.write(f'[{category}] {i+1}/15 생성 중...', ending='\r')

        # 3. 각 게시글에 댓글, 좋아요 생성
        for idx, (article, category) in enumerate(articles):
            comments = []
            for _ in range(random.randint(2, 5)):
                comment_author = random.choice(all_users)
                parent = random.choice(comments) if comments and random.random() < 0.3 else None
                comment = Comment.objects.create(
                    article=article,
                    user=comment_author,
                    parent=parent,
                    content=self.generate_korean_comment(category),
                    created_at=get_aware_datetime()
                )
                comments.append(comment)

            likers = random.sample(all_users, k=random.randint(0, len(all_users)))
            for liker in likers:
                Like.objects.get_or_create(user=liker, article=article)

            self.stdout.write(f'[댓글/좋아요] {idx+1}/{len(articles)} 처리 중...', ending='\r')
            
        # 3. SavingRoom, SavingParticipant, SavingDeposit 더미 생성 추가
        self.stdout.write('\n[저축방] 데이터 생성 시작...')
        for room_num in range(20):
            creator = random.choice(all_users)
            goal_amount = random.randint(10, 100) * 100000  # 10만원 단위
            
            room = SavingRoom.objects.create(
                name=f"{creator.nickname}의 저축방 {room_num+1}",
                description=f"{creator.nickname}님과 함께 목표를 향해 저축하는 방입니다.",
                goal_amount=goal_amount,
                deadline=fake.date_between(start_date='+30d', end_date='+1y'),
                created_by=creator,
                created_at=timezone.now()
            )

            participants = random.sample(all_users, k=random.randint(2, 10))
            if creator not in participants:
                participants.append(creator)
                
            # ✅ 방 전체 입금 총액 추적 (목표금액을 넘지 않도록)
            total_deposited = 0

            for user in participants:
                participant = SavingParticipant.objects.create(
                    room=room,
                    user=user,
                    joined_at=timezone.now()
                )
                
                # 입금 횟수 (1~5회) & 금액 제한
                for _ in range(random.randint(1, 5)):
                    
                    # 남은 금액 계산
                    remaining = goal_amount - total_deposited
                    if remaining <= 0:
                        break
                    # 1만원 ~ min(50만원, 남은 금액)
                    max_amount = min(500000, remaining)
                    amount = random.randrange(10000, max_amount + 1, 10000)  # 1만원 단위
                    
                    SavingDeposit.objects.create(
                        participant=participant,
                        amount=amount,
                        memo=fake.word(ext_word_list=['월급', '용돈', '절약', '보너스', '용돈저축']),
                        created_at=timezone.now()
                    )
                    total_deposited += amount
                    
            self.stdout.write(f'[저축방] {room_num+1}/20 생성 (목표: {goal_amount:,}원, 모금: {total_deposited:,}원)', ending='\r')

        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS(
            f'✅ 완료! 유저 {total_users}명 + 예적금 찜/가입 + 커뮤니티 게시글 + 저축방 20개 생성'
        ))

    # 커뮤니티 게시글
    def generate_korean_title(self, category, product=None):
        fake = Faker('ko_KR')
        title = ""
        if category == 'REVIEW' and product:
            review_types = [
                f"{product.fin_prdt_nm} {fake.random_int(1, 12)}개월 사용 후기",
                f"{product.kor_co_nm} {product.fin_prdt_nm} 실사용 체험기",
                f"[{product.fin_prdt_nm}] 이 상품의 숨은 장점은?"
            ]
            title = random.choice(review_types)
        elif category == 'TIP':
            tip_keywords = ["재테크", "절약", "신용관리", "목표금액"]
            title = f"[{random.choice(tip_keywords)}] {fake.random_int(1,5)}가지 실천 방법"
        else:
            free_keywords = ["가입인사", "자유주제", "고민상담", "정보공유"]
            title = f"[{random.choice(free_keywords)}] {self.clean_text(fake.sentence())}"
        return title[:255]


    def generate_korean_content(self, category, product):
        fake = Faker('ko_KR')
        content = []
        
        if category == 'REVIEW' and product:
            # 상품 특성 반영
            features = ["금리", "유연한 인출", "가입 절차", "고객 서비스"]
            pros = random.sample(features, 2)
            cons = list(set(features) - set(pros))[:1]
            
            content.append(f"### {product.fin_prdt_nm} {fake.random_int(1,12)}개월 후기")
            content.append("\n" + self.clean_text(fake.paragraph(nb_sentences=3)))
            content.append("\n** 만족한 점**")
            for p in pros:
                content.append(f"- {p} 부분이 {fake.word(ext_word_list=['훌륭해요', '만족스러웠어요', '편리했어요'])}")
            content.append("\n** 아쉬운 점**")
            for c in cons:
                content.append(f"- {c} 측면에서 {fake.word(ext_word_list=['개선이 필요해요', '아쉬웠어요', '불편했어요'])}")
            content.append("\n" + fake.sentence() + " 다른 분들도 한번 고려해보세요!")

        elif category == 'TIP':
            steps = [
                "매월 급여의 10% 자동 이체",
                "카드 사용 내역 주간 점검",
                "복리 효과를 위한 장기 적금"
            ]
            content.append(f"### {fake.random_int(1,5)}년 차 직장인이 알려주는 {fake.word(ext_word_list=['절약', '저축', '투자'])} 비법")
            content.append("\n" + self.clean_text(fake.paragraph(nb_sentences=2)))
            content.append("\n** 실천 단계**")
            for idx, step in enumerate(random.sample(steps, 3), 1):
                content.append(f"{idx}. {step}")
            content.append("\n" + fake.sentence() + " 꾸준함이 중요합니다!")

        else:
            content.append(f"### {fake.word(ext_word_list=['안녕하세요', '반갑습니다'])}! {fake.name()}입니다")
            content.append("\n" + self.clean_text(fake.paragraph(nb_sentences=3)))
            content.append("\n** 함께 이야기 나누고 싶은 주제**")
            content.append(f"- {fake.sentence()}")
            content.append(f"- {fake.sentence()}")
            content.append("\n잘 부탁드립니다~ ")

        return '\n'.join(content)

    def generate_korean_comment(self, category):
        fake = Faker('ko_KR')
        
        if category == 'REVIEW':
            comments = [
                f"저도 이 상품 {fake.random_int(1,3)}년째 사용중인데요, {fake.word(ext_word_list=['금리', '유연성'])} 부분이 정말 좋아요!",
                f"{fake.random_int(1,5)}% 금리라니... 다음 달에 가입해봐야겠네요!",
                "고객센터 응대가 좀 느리다는 점이 아쉽다고 생각해요"
            ]
        elif category == 'TIP':
            comments = [
                f"이 방법 {fake.random_int(1,6)}개월째 실천중인데 효과 확실히 있어요!",
                "추가로 추천할만한 방법이 있을까요?",
                "예산 관리 앱과 함께 사용하면 더 효과적이에요!"
            ]
        else:
            comments = [
                "안녕하세요! 좋은 정보 감사합니다 ",
                "비슷한 고민을 겪은 분들 계신가요?",
                "오늘도 화이팅하세요 "
            ]
        
        return self.clean_text(random.choice(comments))