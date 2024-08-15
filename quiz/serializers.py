from rest_framework import serializers
from .models import Quiz, Question, Answer


class QuizSerializer(serializers.ModelSerializer):

    question_count = serializers.SerializerMethodField("get_question_count")

    class Meta:
        model = Quiz
        fiels = ["id", "title", "created_at"]

    def question_count(self, obj):
        return obj.question_count


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ["id", "answer_text", "is_right"]


class QuestionSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "quiz", "title", "answers"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        question = Question.objects.create(**validated_data)

        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.pop("title", instance.title)
        answers_data = validated_data.pop("answers", [])
        instance.answers.all().delete()
        for answer_data in answers_data:
            Answer.objects.create(question=instance, **answer_data)
        instance.save()
        return instance
