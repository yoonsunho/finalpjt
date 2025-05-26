from django.core.management.base import BaseCommand
from finlife.views import (
    fetch_deposit_products, save_deposit_data,
    fetch_saving_products, save_saving_data
)

class Command(BaseCommand):
    help = 'Seed deposit and saving products from external API'

    def handle(self, *args, **options):
        # 예금 데이터 처리
        deposit_base, deposit_options = fetch_deposit_products()
        save_deposit_data(deposit_base, deposit_options)
        self.stdout.write(f'예금 {len(deposit_base)}개 저장 완료')

        # 적금 데이터 처리
        saving_base, saving_options = fetch_saving_products()
        save_saving_data(saving_base, saving_options)
        self.stdout.write(f'적금 {len(saving_base)}개 저장 완료')

        self.stdout.write(self.style.SUCCESS('모든 데이터 저장 성공!'))
