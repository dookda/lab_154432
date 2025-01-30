def calBmi(weight, height):
    return weight / (height ** 2)


def reclassBmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24:
        return "Normal weight"
    elif bmi < 27:
        return "Overweight"
    elif bmi < 30:
        return "Obesity class 1"
    elif bmi < 35:
        return "Obesity class 2"
    else:
        return "Obesity class 3"
