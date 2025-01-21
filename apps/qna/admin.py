from django.contrib import admin
from .models import (
    Category,
    Collection,
    Question,
    Answer,
    Quiz,
    Tag,
    UserInterest,
    UserQuiz,
)
from django.shortcuts import render, redirect
from django.contrib import messages


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
    list_filter = ("collections", "categories")
    inlines = [AnswerInline]

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
        # Get admin context
        context = dict(
            # Include the common admin context
            self.admin_site.each_context(request),
            # Add your custom context
            title="Import Questions",
            app_label=self.model._meta.app_label,
            opts=self.model._meta,
            has_permission=self.has_module_permission(request),
        )

        if request.method == "POST":
            if request.FILES.get("file"):
                # Your file handling logic here
                import pandas as pd
                import math

                file = request.FILES["file"]
                df = pd.read_excel(file)

                try:
                    for _, row in df.iterrows():
                        category = Category.objects.get_or_create(name=row["Category"])[
                            0
                        ]
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
                        question.categories.add(category)
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
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("questions",)


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category")
    list_display_links = ("id", "user", "category")
    search_fields = ("user__username", "category__name")
    list_filter = ("category",)


@admin.register(UserQuiz)
class UserQuizAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "quiz")
    list_display_links = ("id", "user")
    search_fields = ("user__email",)
