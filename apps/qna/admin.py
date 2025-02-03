from django.contrib import admin, messages
from django.shortcuts import redirect, render

from .models import Answer, Category, Collection, Question, Quiz, QuizResult, Tag
from django.db.models import Prefetch
from django.utils import timezone


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("question")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question_text")
    list_display_links = ("id", "question_text")
    search_fields = ("question_text",)
    list_filter = ["categories"]
    inlines = [AnswerInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("answers", "categories")

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "import/",
                self.admin_site.admin_view(self.import_view),
                name="question_import",
            ),
        ]
        return custom_urls + urls

    def import_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            title="Import Questions",
            app_label=self.model._meta.app_label,
            opts=self.model._meta,
            has_permission=self.has_module_permission(request),
        )

        if request.method == "POST":
            if request.FILES.get("file"):
                # Your file handling logic here
                import math

                import pandas as pd

                file = request.FILES["file"]
                df = pd.read_excel(file)

                try:
                    for _, row in df.iterrows():
                        categories = row["Category"].split(",")
                        category_objs = []
                        for category in categories:
                            cleaned = category.strip()
                            category_obj = Category.objects.get_or_create(name=cleaned)[
                                0
                            ]
                            category_objs.append(category_obj)
                        question_text = row["Question"]
                        if Question.objects.filter(
                            question_text__iexact=question_text
                        ).exists():
                            continue
                        question = Question.objects.create(question_text=question_text)
                        if type(row["Hint"]) == str:
                            # import ipdb; ipdb.set_trace()
                            question.hint = row["Hint"]
                        if type(row["Difficulty"]) == str:
                            question.difficulty = row["Difficulty"]
                        question.categories.set(category_objs)
                        question.save()
                        options = [
                            row["Option A"],
                            row["Option B"],
                            row["Option C"],
                            row["Option D"],
                        ]
                        correct_answer = row["Correct Answer"]
                        for option in options:
                            is_correct = option == correct_answer
                            Answer.objects.create(
                                question=question,
                                answer_text=option,
                                is_correct=is_correct,
                            )

                    # Process file
                    messages.success(request, "Data imported successfully")
                    return redirect("admin:qna_question_changelist")
                except Exception as e:
                    messages.error(request, f"Error importing file: {str(e)}")
            else:
                messages.error(request, "Please select a file to import")

        return render(request, "admin/qna/question/import.html", context)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "question_count", "time_to_publish")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    search_fields = ("name",)
    list_filter = ("category",)
    list_per_page = 50
    autocomplete_fields = ["questions"]

    def has_add_permission(self, request):
        return False

    def time_to_publish(self, obj):

        if obj.publish_at <= timezone.now():
            return "Published"
        return obj.publish_at

    def get_queryset(self, request):
        return Quiz.objects.prefetch_related(
            "questions",
            "questions__categories",
            "questions__answers",
            "questions__tags",
        ).select_related("category")

    def question_count(self, obj):
        return obj.questions.count()

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "import/",
                self.admin_site.admin_view(self.import_view),
                name="quiz_import",
            ),
        ]
        return custom_urls + urls

    def import_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            title="Import Quiz",
            app_label=self.model._meta.app_label,
            opts=self.model._meta,
            has_permission=self.has_module_permission(request),
        )

        if request.method == "POST":
            if request.FILES.get("file"):
                import pandas as pd
                from django.utils import timezone

                file = request.FILES["file"]
                df = pd.read_excel(file)

                try:
                    names = file.name.split(".")[0].split(",")
                    quiz_name = names[0]
                    category = Category.objects.get_or_create(name=names[1].strip())[0]
                    if Quiz.objects.filter(name=quiz_name).exists():
                        quiz_name = (
                            f"{quiz_name} - {timezone.now().strftime('%Y%m%d%H%M%S')}"
                        )
                    # publish_time = timezone.now() + timezone.timedelta(minutes=1440)
                    publish_time = request.POST.get("publish")
                    quiz = Quiz.objects.create(
                        name=quiz_name, category=category, publish_at=publish_time
                    )
                    for _, row in df.iterrows():
                        categories = row["Category"].split(",")
                        category_objs = []
                        for category in categories:
                            category = Category.objects.get_or_create(
                                name=category.strip()
                            )[0]
                            category_objs.append(category)
                        question_text = row["Question"]
                        # if Question.objects.filter(
                        #     question_text__iexact=question_text
                        # ).exists():
                        #     continue
                        question = Question.objects.create(
                            question_text=question_text, publish_at=publish_time
                        )
                        if type(row["Hint"]) == str:
                            question.hint = row["Hint"]
                        if type(row["Difficulty"]) == str:
                            question.difficulty = row["Difficulty"]
                        question.categories.set(category_objs)
                        question.save()
                        options = [
                            row["Option A"],
                            row["Option B"],
                            row["Option C"],
                            row["Option D"],
                        ]
                        correct_answer = row["Correct Answer"]
                        for option in options:
                            is_correct = option == correct_answer
                            Answer.objects.create(
                                question=question,
                                answer_text=option,
                                is_correct=is_correct,
                            )
                        quiz.questions.add(question)
                    quiz.save()

                    messages.success(request, "Data imported successfully")
                    return redirect("admin:qna_quiz_changelist")
                except Exception as e:
                    messages.error(request, f"Error importing file: {str(e)}")
            else:
                messages.error(request, "Please select a file to import")

        return render(request, "admin/qna/quiz/import.html", context)


@admin.register(QuizResult)
class QuizResultAdminAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "quiz_attempted", "percentage")
    list_display_links = ("id", "user")
    search_fields = ("user__email",)

    def quiz_attempted(self, obj):
        return obj.quiz_name
