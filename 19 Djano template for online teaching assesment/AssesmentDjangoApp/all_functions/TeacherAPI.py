import pickle


class TeacherEvaluation:

    def __init__(self, model_path, le_path):
        self.model = pickle.load(open(model_path, "rb"))
        self.le = pickle.load(open(le_path, "rb"))

    def predict(self, Students_feedback_for_teacher, Students_Online_Time,
                Students_Attendance, Students_Questions):
        Students_feedback_for_teacher = self.le.transform([Students_feedback_for_teacher])

        return self.model.predict([[Students_feedback_for_teacher, Students_Online_Time,
                                    Students_Attendance, Students_Questions]])

# te = TeacherEvaluation("Teacher.pickle", "TeacherLe.pickle")
# te.predict("Best", 59, 320, 85)

