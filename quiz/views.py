from rest_framework import generics, status
from rest_framework.response import Response
from .models import Quiz, Question
from .serializers import QuestionSerializer, AnswerSerializer, QuizSerializer
from rest_framework.views import APIView
from django.http import Http404


class ListCreateQuiz(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class RetrieveUpdateDestroyQuiz(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizQuestion(APIView):
    def get(self, request, format="None", **kwargs):
        question = Question.objects.filter(quiz_id=kwargs.get("quiz_id", None))
        serilaizer = QuestionSerializer(question=question, many=True)

        return Response(serilaizer.data, status=status.HTTP_200_OK)

    def post(self, request, format="None", **kwargs):
        quiz = Question.objects.get(id=kwargs.get("quiz_id"))
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(quiz=quiz)
            return Response(
                {"message": "Question created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizQuestionDetail(APIView):
    def get_object(self, pk=None):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format="None"):
        question = self.get_object(pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None, format="None"):
        question = self.get_object(pk=pk)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format="None"):
        question = self.get_object(pk=pk)
        question.delete()
        return Response(
            {"message": "Question Deleted successfully", "data": serializer.data},
            status=status.HTTP_204_NO_CONTENT,
        )
