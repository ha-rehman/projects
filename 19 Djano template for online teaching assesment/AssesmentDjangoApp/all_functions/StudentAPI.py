import pickle


# For Checking
class StudentEvaluation:

    def __init__(self, model_path, le_path):
        self.model = pickle.load(open(model_path, "rb"))
        self.le = pickle.load(open(le_path, "rb"))

    def predict(self, Teacher_Remarks, Attendance_in_course, Course_Access,
                Resourse_Visit, On_Time_Submission, Exam_1, Exam_2, Exam_3,
                Exam_4, Project, Assignment_1, Assignment_2, Assignment_3):
        Teacher_Remarks = self.le.transform([Teacher_Remarks])

        return self.model.predict([[Teacher_Remarks, Attendance_in_course, Course_Access,
                                    Resourse_Visit, On_Time_Submission, Exam_1, Exam_2, Exam_3,
                                    Exam_4, Project, Assignment_1, Assignment_2, Assignment_3]])
