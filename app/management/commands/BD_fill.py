from django.core.management.base import BaseCommand
from app.models import Question, Answer, Tag, User
import random

class Command(BaseCommand):
    help = 'Заполнить базу данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Количество вопросов для заполнения')

    def handle(self, *args, **options):
        ratio = options['ratio']

        answers_data_to_insert = []

        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()

        users = []
        for i in range(ratio * 2):
            user = User.objects.create(
                username=f'user_{i+1}',
                email=f'user_{i+1}@example.com',
                password=f'password{i+1}',
                nickname=f'nickname_{i+1}',
                photo=f'avatars/anon.png',
            )
            users.append(user)

        all_tags = [
            Tag.objects.create(name=f'Tag_{i + 1}') for i in range(ratio * 2)
        ]

        def get_random_user(exclude_user):
            users_except_author = [user for user in users if user != exclude_user]
            return random.choice(users_except_author)

        for i in range(ratio):
            # Создаем вопрос
            author = random.choice(users)
            question_data = Question.objects.create(
                title=f'Ты нашёл вопрос №{i + 1}?',
                content=f'№{i + 1} Lorem ipsum dolor sit amet, consectetur adipiscing elit,'
                       f' sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. '
                       f'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
                       f' Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                       f' Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id'
                       f' est laborum.',
                photo=f"img/fire.png",
                like=random.randint(-1000, 1000),
                author=author,
            )

            # Выбираем случайное количество тэгов (от 1 до 5)
            selected_tags = random.sample(all_tags, random.randint(1, 5))
            question_data.tags.set(selected_tags)

            for j in range(10):  # Создаем 10 ответов для каждого вопроса
                # Создаем ответ
                answer_author = get_random_user(author)
                answer_data = Answer.objects.create(
                    content=f'Это ответ №{j+1} на вопрос №{i + 1}',
                    is_correct=random.choice([True, False]),
                    what_question=question_data,  # Передаем экземпляр Question
                    like=random.randint(0, 1000),
                    author=answer_author,
                )
                answers_data_to_insert.append(answer_data)

            print("Создан вопрос №", i + 1)

        self.stdout.write(self.style.SUCCESS(f'Добавлено {ratio} записей в базу данных.'))
