class Bmi:
    def __init__(self):
        self.weight = 0
        self.height = 0
        self.bmi = 0
        self.bmiTxt = ""

    def setWeight(self, weight):
        self.weight = weight
        return self

    def setHeight(self, height):
        self.height = height
        return self

    def calBmi(self):
        self.bmi = self.weight / self.height**2
        return self

    def reclassBmi(self):
        if self.bmi < 18.5:
            self.bmiTxt = "ต่ำกว่าเกณฑ์"
            return self
        elif self.bmi < 24:
            self.bmiTxt = "สมส่วน"
            return self
        elif self.bmi < 27:
            self.bmiTxt = "ท้วม"
            return self
        elif self.bmi < 30:
            self.bmiTxt = "อวบระยะ 1"
            return self
        elif self.bmi < 35:
            self.bmiTxt = "อวบระยะ 2"
            return self
        else:
            self.bmiTxt = "อวบระยะ 3"
            return self

    def __str__(self):
        return f"น้ำหนัก:{self.weight} สูง:{self.height} bmi:{self.bmi} {self.bmiTxt}"
