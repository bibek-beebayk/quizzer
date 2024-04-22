from django.contrib import admin
from .models import Category, Collection, Question, Answer, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text')
    list_display_links = ('id', 'question_text')
    search_fields = ('question_text',)
    list_filter = ('collections', 'categories')
    inlines = [AnswerInline]
