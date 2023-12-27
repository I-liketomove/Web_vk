from django.core.management.base import BaseCommand
from app.models import Question, Answer, Tag, User, LikeQuestion, LikeAnswer
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Заполнить базу данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Количество вопросов для заполнения')

    def handle(self, *args, **options):
        ratio = options['ratio']

        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        LikeQuestion.objects.all().delete()
        LikeAnswer.objects.all().delete()
        User.objects.all().delete()

        users = []
        for i in range(ratio):
            user = User.objects.create(
                username=f'user_{i+1}',
                email=f'user_{i+1}@example.com',
                password=f'password{i+1}',
                nickname=f'nickname_{i+1}',
                photo=f'avatars/anon.png',
            )
            users.append(user)

        all_tags = [
            Tag.objects.create(name=f'Tag_{i + 1}') for i in range(ratio)
        ]

        def get_random_user(exclude_user):
            users_except_author = [user for user in users if user != exclude_user]
            return random.choice(users_except_author)

        def create_like_question(question_data, user):
            like_question_author = user
            type_value = random.choice([1, -1])

            existing_like_question = LikeQuestion.objects.filter(
                question=question_data,
                author=like_question_author,
                type=type_value
            ).first()

            if not existing_like_question:
                like_question = LikeQuestion.objects.create(
                    question=question_data,
                    author=like_question_author,
                    type=type_value,
                )
            return type_value

        def create_like_answer(answer_data, user):
            answer_author = user
            type_value = random.choice([1, -1])

            existing_like_answer = LikeAnswer.objects.filter(
                answer=answer_data,
                author=answer_author,
                type=type_value
            ).first()

            if not existing_like_answer:
                like_answer = LikeAnswer.objects.create(
                    answer=answer_data,
                    author=answer_author,
                    type=type_value,
                )
            return type_value

        for i in range(ratio * 10):
            # Создаем вопрос
            author = random.choice(users)
            question_date = timezone.now() - timezone.timedelta(days=random.randint(1, 365))
            question_data = Question.objects.create(
                title=f'Ты нашёл вопрос №{i + 1}?',
                content=f'№{i + 1} Lorem ipsum dolor sit amet, consectetur adipiscing elit,'
                        f' sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. '
                        f'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
                        f' Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                        f' Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id'
                        f' est laborum.',
                photo=f"img/fire.png",
                author=author,
                date_written=question_date,
                total_likes=1,
                total_answers=10,
            )

            selected_tags = random.sample(all_tags, random.randint(1, 5))
            question_data.tags.set(selected_tags)

            # Создаем LikeQuestion
            question_data.total_likes = create_like_question(question_data, get_random_user(author))
            question_data.save()

            for j in range(10):  # Создаем 10 ответов для каждого вопроса
                # Создаем ответ
                answer_author = get_random_user(author)
                answer_date = question_date + timezone.timedelta(days=random.randint(1, 365))
                answer_data = Answer.objects.create(
                    content=(f'Это ответ №{j + 1} на вопрос №{i + 1} '
                             f'Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
                             f'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. '
                             f'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. '
                             f'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. '
                             f'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id '
                             f'est laborum.'),
                    is_correct=random.choice([True, False]),
                    what_question=question_data,
                    author=answer_author,
                    date_written=answer_date,
                    total_likes=-3,
                )
                like_answer1 = get_random_user(answer_author)
                like_answer2 = get_random_user(like_answer1)
                # Создаем LikeAnswer
                total_likes_for_answer = 0
                total_likes_for_answer += create_like_answer(answer_data, like_answer1)
                total_likes_for_answer += create_like_answer(answer_data, like_answer2)
                answer_data.total_likes = total_likes_for_answer
                answer_data.save()

            if (i % 10 == 0):
                print(f"Создан вопрос №{i // 10 + 1}")

        self.stdout.write(self.style.SUCCESS(f'Добавлено {ratio} записей в базу данных.'))
