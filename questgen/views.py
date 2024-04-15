from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .prep import *
from . import your_script_file
from . import multipleqa
from .subjective import SubjectiveTest
# from sklearn.linear_model import LinearRegression
import numpy as np
# from transformers import pipeline
from rest_framework import status


@api_view(['POST'])
def test_generate(request):
    if request.method == 'POST':
        input_text = request.data.get('itext', '')
        
        no_of_ques = request.data.get('noq', '')

        
        objective_generator = SubjectiveTest(input_text, no_of_ques)
        question_list, answer_list = objective_generator.generate_test()
        response_data = [{'question': q, 'answer': a} for q, a in zip(question_list, answer_list)]
        return Response(response_data)
    
    
@api_view(['POST'])
def mcq(request):
    if request.method == 'POST':
        input_text = request.data.get('text', '')
        
        # Generate questions from input text
        text_object = Text(input_text)
        questions = text_object.generate_questions()
        
        # Serialize questions
        serialized_questions = []
        for question in questions:
            serialized_question = {
                'question': question.question,
                'answer': question.ans,
                'options': question.options
            }
            serialized_questions.append(serialized_question)
        
        return Response({'questions': serialized_questions})

@api_view(['POST'])
def generate_longanswer_questions(request):
    try:
        context_data = request.data.get('context')  
        no_of_ques = int(request.data.get('noq', ''))# Assuming the context is sent as 'context' in the request body
        if not context_data:
            return Response({"error": "Context data is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming the context data is already in JSON format, no need for additional parsing
        # Call your function from the script file with the context data
        questions = your_script_file.generate_questions(context_data,no_of_ques)
        
        return Response(questions, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def generate_mcqquestions(request):
    try:
        context_data = request.data.get('context')  
        no_of_ques = int(request.data.get('noq', ''))# Assuming the context is sent as 'context' in the request body
        if not context_data:
            return Response({"error": "Context data is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming the context data is already in JSON format, no need for additional parsing
        # Call your function from the script file with the context data
        questions = multipleqa.generate_questions(context_data,no_of_ques)
        
        return Response(questions, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    

# @api_view(['POST'])
# def predict_score_view(request):
#     if request.method == 'POST':
#         # Extract scores from request data
#         scores = request.data.get('scores', [])

#         # Ensure that scores for exactly 7 exams are provided
#         if len(scores) != 7:
#             return Response({'error': 'Please provide scores for exactly 7 exams'}, status=400)

#         # Reshape scores into numpy array for regression
#         X_train = np.array(range(1, 8)).reshape(-1, 1)  # Previous 7 exams as X values
#         y_train = np.array(scores).reshape(-1, 1)  # Corresponding scores as y values

#         # Fit linear regression model
#         model = LinearRegression()
#         model.fit(X_train, y_train)

#         # Predict scores for upcoming exams (next 3 exams)
#         X_test = np.array(range(8, 11)).reshape(-1, 1)  # Next 3 exams
#         predicted_scores = model.predict(X_test)

#         # Prepare data for graph construction
#         exam_numbers = list(range(1, 11))  # Exam numbers from 1 to 10 (7 previous + 3 upcoming)
#         exam_scores = list(scores) + list(predicted_scores.flatten())

#         # Construct response data
#         response_data = {
#             'exam_numbers': exam_numbers,
#             'exam_scores': exam_scores
#         }

#         return Response(response_data)
    
    

# @api_view(['POST'])
# def course_suggestion_view(request):
#     if request.method == 'POST':
#         data = request.data
#         subject_marks = data.get('subject_marks', {})

#         suggested_course = suggest_course(subject_marks)
        
#         return Response({"course": suggested_course}, status=status.HTTP_200_OK)

# def suggest_course(subject_marks):
#     input_text = _preprocess_input(subject_marks)
#     classifier = pipeline("zero-shot-classification", model="distilbert-base-uncased")
#     candidate_labels = ["Engineering", "Medicine", "Arts"]
#     result = classifier(input_text, candidate_labels, return_all_scores=True)
#     label_scores = result['scores']
#     label_index = label_scores.index(max(label_scores))
#     return candidate_labels[label_index]

# def _preprocess_input(subject_marks):
#     input_text = " ".join([f"{subject}: {marks}" for subject, marks in subject_marks.items()])
#     return input_text.strip()

