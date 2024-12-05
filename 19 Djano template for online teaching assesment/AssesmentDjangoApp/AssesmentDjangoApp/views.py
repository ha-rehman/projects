import os.path

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from all_functions.StudentAPI import StudentEvaluation
from all_functions.TeacherAPI import TeacherEvaluation


teacher_model_path = os.path.join(os.getcwd(), "all_functions/Teacher.pickle")
teacher_label_encoder_path = os.path.join(os.getcwd(), "all_functions/TeacherLe.pickle")

student_model_path = os.path.join(os.getcwd(), "all_functions/Student.pickle")
student_label_encoder_path = os.path.join(os.getcwd(), "all_functions/StudentLe.pickle")

def index(request):
    return render(request, 'index.html')


def teacher_evaluation(request):
    return render(request, 'teacher-evaluation.html')


def student_evaluation(request):
    return render(request, 'student-evaluation.html')


def teacher_prediction_score(request):
    if request.method == "POST":

        feedback = request.POST['feedback']
        online_time = request.POST['online-time']
        attendance = request.POST['attendance']
        questions = request.POST['questions']

        te = TeacherEvaluation(teacher_model_path, teacher_label_encoder_path)
        score = te.predict(feedback, online_time, attendance, questions)[0]
        score = "{:.2f}".format(score)
        return JsonResponse({'Score': score}, status=200)
    else:
        return JsonResponse(request, status=400)


def student_prediction_score(request):
    if request.method == "POST":

        feedback = request.POST['feedback']
        attendance = request.POST['attendance']
        course_access = request.POST['course-access']
        resource_visit = request.POST['resource-visit']
        submission = request.POST['submission']
        assignment1 = request.POST['assignment1']
        assignment2 = request.POST['assignment2']
        assignment3 = request.POST['assignment3']
        exam1 = request.POST['exam1']
        exam2 = request.POST['exam2']
        exam3 = request.POST['exam3']
        exam4 = request.POST['exam4']
        project = request.POST['project']

        te = StudentEvaluation(student_model_path, student_label_encoder_path)
        score = te.predict(feedback, attendance, course_access,
                           resource_visit, submission, exam1, exam2, exam3,
                           exam4, project, assignment1, assignment2, assignment3)[0]

        score = "{:.2f}".format(score)
        return JsonResponse({'Score': score}, status=200)
    else:
        return JsonResponse(request, status=400)


