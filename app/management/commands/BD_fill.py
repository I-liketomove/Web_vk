from django.core.management.base import BaseCommand
from app.models import Question, Answer, Tag
import random

class Command(BaseCommand):
    help = 'Заполнить базу данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Количество ячеек для заполнения')

    def handle(self, *args, **options):
        ratio = options['ratio']

        questions_data_to_insert = []
        answers_data_to_insert = []
        tags_data_to_insert = []

        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()

        for i in range(ratio):
            tag_data = Tag(name=f'Tag №{i+1}')
            tags_data_to_insert.append(tag_data)

        Tag.objects.bulk_create(tags_data_to_insert)

        for i in range(ratio * 10):
            question_data = Question.objects.create(
                title=f'Ты нашёл вопрос №{i + 1}?',
                content=f'№{i} Lorem ipsum dolor sit amet, consectetur adipiscing elit,'
                       f' sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. '
                       f'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
                       f' Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                       f' Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id'
                       f' est laborum.',
                photo="../../media/img/fire.png",
                like=random.randint(-1000, 1000),
            )

            tags = [
                Tag.objects.get(name=f'Tag №{random.randint(1, ratio)}'),
                Tag.objects.get(name=f'Tag №{random.randint(1, ratio)}'),
            ]

            question_data.tags.set(tags)
            questions_data_to_insert.append(question_data)

            for j in range(10):  # Создаем 10 ответов для каждого вопроса
                answer_data = Answer.objects.create(
                    content=f'Это ответ №{j+1} на вопрос №{i + 1}',
                    is_correct=random.choice([True, False]),
                    what_question=question_data,  # Передаем экземпляр Question
                    like=random.randint(0, 1000)
                )
                answers_data_to_insert.append(answer_data)

            print("Создан вопрос №", i)

        self.stdout.write(self.style.SUCCESS(f'Добавлено {ratio} записей в базу данных.'))
