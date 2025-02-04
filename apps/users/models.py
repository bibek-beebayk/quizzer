from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    interests = models.ManyToManyField("qna.Category", related_name="users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def total_quizzes_taken(self):
        return self.quizzes.count()

    @property
    def average_score(self):
        if self.total_questions_answered == 0:
            return 0
        return round(
            (self.total_correct_answers / self.total_questions_answered) * 100, 2
        )

    @property
    def highest_score(self):
        if self.total_quizzes_taken == 0:
            return 0
        return max(quiz.percentage for quiz in self.quizzes.all())

    @property
    def highest_score_quiz(self):
        if self.highest_score == 0:
            return None
        return self.quizzes.filter(percentage=self.highest_score).first().quiz_name

    @property
    def lowest_score(self):
        if self.total_quizzes_taken == 0:
            return 0
        return min(quiz.percentage for quiz in self.quizzes.all())

    @property
    def lowest_score_quiz(self):
        if self.lowest_score == 0:
            return None
        return self.quizzes.filter(percentage=self.lowest_score).first().quiz_name

    @property
    def total_questions_answered(self):
        return sum(quiz.total_questions for quiz in self.quizzes.all())

    @property
    def total_correct_answers(self):
        return sum(quiz.correct_answers for quiz in self.quizzes.all())

    @property
    def most_active_category(self):
        categories = {}
        for quiz in self.quizzes.all():
            if quiz.category in categories:
                categories[quiz.category] += 1
            else:
                categories[quiz.category] = 1
        if not categories:
            return None
        return max(categories, key=categories.get)

    @property
    def quizzes_this_month(self):
        return self.quizzes.filter(created_at__month=timezone.now().month).count()
    
    def send_password_reset_email(self, code):
        from django.core.mail import send_mail
        subject = "Password Reset Request"
        # message = render_to_string(
        #     "password_reset_email.html",
        #     {
        #         "user": self,
        #         "uid": self.id,
        #         "token": self.password_reset_token,
        #     },
        # )
        message = f"Your OTP for password reset is {code}."
        from_email = "beebayk63478@gmail.com"
        recipient_list = [self.email]
        send_mail(subject, message, from_email, recipient_list)

    def generate_otp(self, type):
        import random
        if self.otps.exists():
            Otp.objects.filter(user=self).delete()
        otp_string = str(random.randint(100000, 999999))
        otp = Otp.objects.create(user=self, code=otp_string, type=type)
        self.send_password_reset_email(otp_string)
        # send_mail(subject, message, from_email, recipient_list)

    @classmethod
    def get_registration_data(cls):
        # pages_vivits_coo = cls.objects.all().values('page').annotate(count=models.Count('page'))
        response_data = {}
        response_data["total_registration"] = cls.objects.count()
        response_data["registrations_today"] = cls.objects.filter(
            date_joined__date=timezone.now().date()
        ).count()
        response_data["registrations_last_7_days"] = cls.objects.filter(
            date_joined__gte=timezone.now() - timezone.timedelta(days=7)
        ).count()
        response_data["registrations_last_30_days"] = cls.objects.filter(
            date_joined__gte=timezone.now() - timezone.timedelta(days=30)
        ).count()
        return response_data


class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    type = models.CharField(max_length=32, default="password_reset")

    def __str__(self):
        return self.code
    
    @property
    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 300


class RequestLog(models.Model):
    endpoint = models.CharField(max_length=1000, null=True)
    user = models.CharField(max_length=255)
    response_code = models.PositiveSmallIntegerField()
    method = models.CharField(max_length=10, null=True)
    remote_address = models.CharField(max_length=1000, null=True)
    exec_time = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now=True)
    body_response = models.TextField(null=True)
    body_request = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
