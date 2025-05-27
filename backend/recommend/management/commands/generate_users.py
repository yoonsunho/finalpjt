from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
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

        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS(
            f'✅ 완료! 유저 {total_users}명 + 예적금 찜/가입 + 카테고리별 게시글 15개씩 + 댓글/좋아요 생성'
        ))

    # 아래는 동일 (앞서 제공한 코드와 동일)
    def generate_korean_title(self, category, product=None):
        fake = Faker('ko_KR')
        title = ""
        if category == 'REVIEW' and product:
            title = f"[후기] {product.fin_prdt_nm} {fake.word(ext_word_list=['사용기', '체험기', '리뷰'])}"
        elif category == 'TIP':
            title = f"[꿀팁] {fake.word(ext_word_list=['절약', '관리', '저축'])}하는 방법 {fake.random_int(1,5)}가지"
        else:
            title = f"[자유] {self.clean_text(fake.sentence())}"
        return title[:255]

    def generate_korean_content(self, category, product):
        fake = Faker('ko_KR')
        content = []
        if category == 'REVIEW' and product:
            content.append(f"### {product.fin_prdt_nm} {fake.random_int(1,12)}개월 후기")
            content.append("\n" + self.clean_text(fake.paragraph(nb_sentences=3)))
            content.append("\n**장점**\n- " + self.clean_text(fake.sentence()))
            content.append("\n**단점**\n- " + self.clean_text(fake.sentence()))
        elif category == 'TIP':
            tip = fake.word(ext_word_list=['커피값', '통장', '할인카드','적금'])
            content.append(f"### {tip} {fake.word(ext_word_list=['절약', '관리', '활용'])} 팁")
            content.append("\n" + self.clean_text(fake.paragraph(nb_sentences=3)))
        else:
            content.append(f"### {fake.word(ext_word_list=['안녕하세요', '반갑습니다', '가입인사'])}!")
            content.append("\n" + self.clean_text(fake.paragraph(nb_sentences=3)))
        return '\n'.join(content)

    def generate_korean_comment(self, category):
        fake = Faker('ko_KR')
        comment = ""
        if category == 'REVIEW':
            comment = f"저도 이 상품 {fake.word(ext_word_list=['사용중', '관심있어요'])}! " + self.clean_text(fake.sentence())
        elif category == 'TIP':
            comment = f"이 방법 {fake.word(ext_word_list=['좋아요', '추천해요'])}! " + self.clean_text(fake.sentence())
        else:
            comment = f"{fake.word(ext_word_list=['좋은 글', '감사합니다'])}! " + self.clean_text(fake.sentence())
        return comment

    def clean_text(self, text):
        return ''.join(
            c for c in text 
            if (ord('가') <= ord(c) <= ord('힣')) or 
               (ord('0') <= ord(c) <= ord('9')) or 
               (c in [' ', '.', '!', '?', ',', '\n'])
        )
