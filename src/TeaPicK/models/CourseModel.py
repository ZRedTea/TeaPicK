class CourseModel:
    def __init__(self, courseName : str, courseNo : str):
        self.courseName = courseName
        self.courseNo = courseNo
        self.courseId = None

        self.isSelected = False

    def getCourseName(self):
        return self.courseName
    def setCourseName(self, courseName):
        self.courseName = courseName

    def getCourseNo(self):
        return self.courseNo
    def setCourseNo(self, courseNo):
        self.courseNo = courseNo

    def isSelected(self):
        return self.isSelected
    def Selected(self):
        self.isSelected = True

    def getCourseId(self):
        return self.courseId
    def setCourseId(self, courseId):
        self.courseId = courseId


    def __str__(self):
        return f'{self.courseName}[{self.courseNo}]'