class Bmi():
    def __init__(self, weight=0, height=0):
        self.weight = weight
        self.height = height
        self.bmi = 0
        self.bmiTxt = ''

    def setWeight(self, weight):
        self.weight = weight
        return self

    def setHeight(self, height):
        self.height = height
        return self

    def calculate(self):
        if self.weight == 0 or self.height == 0:
            self.bmi = 0
        else:
            self.bmi = self.weight / (self.height/100) ** 2
        return self

    def reclass(self):
        if self.bmi < 18.5:
            self.bmiTxt = "slim"
            return self
        elif self.bmi < 24.9:
            self.bmiTxt = "normal"
            return self
        elif self.bmi < 39.9:
            self.bmiTxt = "อวบ"
            return self
        else:
            self.bmiTxt = "อิ่ม"
            return self

    def __str__(self):
        return f"weight: {self.weight} height: {self.height} bmi: {self.bmi}"
