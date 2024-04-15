from django.urls import path
from .views import test_generate, generate_longanswer_questions, generate_mcqquestions
# predict_score_view
# course_suggestion_view



urlpatterns = [
    path('questiongenerate/',test_generate,name='generate_questions'),
    # path('mcqquestiongenerate/',mcq,name='mcqgenerate_questions'),
     path('longanswergenerate/',generate_longanswer_questions,name='longanswergenerate_questions'), 
    path('mcq/',generate_mcqquestions,name='generate_questionsse'),
    # path('predictscore/',predict_score_view,name='predict_score_view'),
    # path('coursesuggestion/',course_suggestion_view,name='course_suggestion_view'),

]
