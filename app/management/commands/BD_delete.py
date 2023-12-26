from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):
    help = 'Очистить базу данных'

    def handle(self, *args, **options):
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        User.objects.all().delete()