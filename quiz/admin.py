from django.contrib import admin
from .models import Question, Quiz, Answer


# Register your models here.
class QuizAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


class AnswerInlineModel(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    fields = ["title", "quiz"]
    list_display = ["title", "quiz", "created_at"]
    inlines = [AnswerInlineModel]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["answer_text", "is_right", "question"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Answer, AnswerAdmin)
