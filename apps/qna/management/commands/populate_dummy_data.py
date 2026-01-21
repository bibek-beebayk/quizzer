import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from faker import Faker

from apps.qna.models import Category, Tag, Question, Answer, Quiz, QuizResult
from apps.blog.models import Blog, BlogCategory, BlogSection, Comment
from apps.analytics.models import PageVisit

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Populate the database with dummy data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating dummy data...")
        try:
            with transaction.atomic():
                self.create_users()
                self.create_qna_data()
                self.create_blog_data()
                self.create_analytics_data()
                self.stdout.write(self.style.SUCCESS("Successfully populated database with dummy data!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error populating data: {e}"))
            import traceback
            traceback.print_exc()

    def create_users(self):
        self.stdout.write("Creating Users...")
        # Create admin if not exists
        if not User.objects.filter(email="admin@example.com").exists():
            User.objects.create_superuser("admin@example.com", "password")
        
        # Create standard users
        for _ in range(10):
            email = fake.email()
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(email=email, password="password", first_name=fake.first_name(), last_name=fake.last_name())

    def create_qna_data(self):
        self.stdout.write("Creating QnA Data...")
        # Categories
        categories = ["General Knowledge", "Science", "History", "Geography", "Literature", "Sports", "Technology"]
        category_objs = []
        for name in categories:
            cat, created = Category.objects.get_or_create(name=name)
            category_objs.append(cat)

        # Tags
        tags = ["fun", "trivia", "hard", "easy", "2024", "classic"]
        tag_objs = []
        for name in tags:
            tag, created = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)

        # Questions and Answers
        users = User.objects.all()
        for _ in range(20):
            q = Question.objects.create(
                question_text=fake.sentence(nb_words=10).replace(".", "?"),
                hint=fake.sentence(),
                answer_explanation=fake.paragraph(),
                difficulty=random.choice(["Easy", "Medium", "Hard"]),
                publish_at=timezone.now()
            )
            q.categories.set(random.sample(category_objs, k=random.randint(1, 3)))
            q.tags.set(random.sample(tag_objs, k=random.randint(0, 2)))

            # Answers (1 correct, 3 wrong)
            Answer.objects.create(question=q, answer_text=fake.word(), is_correct=True)
            for _ in range(3):
                Answer.objects.create(question=q, answer_text=fake.word(), is_correct=False)
            
            # Quizzes
            if random.random() > 0.5:
                quiz_name = fake.sentence(nb_words=3).replace(".", "") + " Quiz"
                if not Quiz.objects.filter(name=quiz_name).exists():
                    quiz = Quiz.objects.create(
                        name=quiz_name,
                        category=random.choice(category_objs),
                        publish_at=timezone.now()
                    )
                    quiz.questions.add(q)
                    # Add more random questions to the quiz
                    additional_questions = Question.objects.exclude(id=q.id).order_by('?')[:4]
                    quiz.questions.add(*additional_questions)
                    
                    # Quiz Results
                    for user in random.sample(list(users), k=random.randint(0, 5)):
                        QuizResult.objects.create(
                            user=user,
                            quiz=quiz,
                            quiz_name=quiz.name,
                            total_questions=quiz.questions.count(),
                            attempted_questions=quiz.questions.count(),
                            correct_answers=random.randint(0, quiz.questions.count()),
                            category=quiz.category.name
                        )

    def create_blog_data(self):
        self.stdout.write("Creating Blog Data...")
        blog_categories = ["News", "Updates", "education", "LifeStyle"]
        blog_cat_objs = []
        for name in blog_categories:
            cat, created = BlogCategory.objects.get_or_create(name=name)
            blog_cat_objs.append(cat)

        users = User.objects.all()
        for _ in range(5):
            title = fake.sentence(nb_words=6).replace(".", "")
            slug = fake.slug()
            # Ensure unique slug
            while Blog.objects.filter(slug=slug).exists():
                slug = fake.slug() + str(random.randint(1, 1000))
            
            blog = Blog.objects.create(
                title=title,
                slug=slug,
                author=random.choice(users) if users else None,
                excerpt=fake.text(),
                publish_at=timezone.now()
            )
            blog.categories.set(random.sample(blog_cat_objs, k=random.randint(1, 2)))
            
            # Blog Sections
            for i in range(random.randint(1, 3)):
                BlogSection.objects.create(
                    blog=blog,
                    order=i,
                    title=fake.sentence(nb_words=4),
                    content=fake.paragraph()
                )

    def create_analytics_data(self):
        self.stdout.write("Creating Analytics Data...")
        users = User.objects.all()
        pages = ["Home", "Quiz", "Blog", "Profile", "Login"]
        
        for _ in range(50):
            PageVisit.objects.create(
                user=random.choice(users) if users and random.random() > 0.3 else None,
                page=random.choice(pages),
                url=fake.uri(),
                client_ip=fake.ipv4()
            )
