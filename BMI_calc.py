from colorama import Fore, init, Style    # used to give color, style and a background to output text                         

bmi = 0
BMR = 0
LBM = 0
body_fat = 0

print("Welcome to BMI calculator !")
print("Please select the unit of calculation: \n 1> Imperial \n 2> Metric")
mode = int(input("Select option: "))                        # imperial or metric unit selection
while mode != 1 and mode != 2:
    print("Select appropriate option.")
    print("Please select the unit of calculation: \n 1> Imperial \n 2> Metric")
    mode = int(input("Select option: "))

def bmi_bar(bmi_mapped, ranges, colors, length=100):               #used to generate bar for the calculated bmi according to bmi and age
    bar = ""
    for i in range(1, length + 1):
        if i == bmi_mapped:
            bar += "█"  
        else:
            for (start, end), color in zip(ranges, colors):
                if start <= i <= end:
                    bar += color + "="
                    break
    return bar + Fore.RESET

def fat_bar(gender, fat, low, high, bar_length=100):            #used to generate bar for body fat percentage according to fat, age and gender
    bar = ""
    
    for i in range(1, bar_length + 1):
        if i == fat:
            bar += "█"  
        elif i < low or i > high:
            bar += Fore.WHITE + "="
        else:
            if gender== 1:
                bar += Fore.CYAN + "="
            else:
                bar += Fore.MAGENTA + "="
    return bar + Fore.RESET

def LBM_bar(gender, LBM, low, high, bar_length=100):        #used to generate bar for lean body mass percentage according to LBM, age and gender
    bar = ""
    
    for i in range(1, bar_length + 1):
        if i == LBM:
            bar += "█"  
        elif i < low or i > high:
            bar += Fore.WHITE + "="
        else:
            if gender== 1:
                bar += Fore.CYAN + "="
            else:
                bar += Fore.MAGENTA + "="
    return bar + Fore.RESET

def FFMI_bar(FFMI, low, high, bar_length=100):            #used to generate bar for fat free mass index percentage according to FFMI, age and gender
    bar = ""
    
    for i in range(1, bar_length + 1):
        if i == FFMI:
            bar += "█"  
        elif i < low or i > high:
            bar += Fore.WHITE + "="
        else:
            bar += Fore.GREEN + "="

    return bar + Fore.RESET

def visual(age, gender, bmi, LBM, FFMI, body_fat, BMR):   #used to provide actual output
    
    bmi_mapped = round(100*bmi/60)
    fat = round(body_fat)
    if mode == 1:
        unit = "lbs"
    else:
        unit = "kg"
    print(" ")

    #-------------------------------------------BMI---------------------------------------------------

    if age < 18:
        ranges = [(1, 5), (6, 85), (86, 95), (96, 100)]
        colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.RED]
    elif age < 65:
        ranges = [(1, 28), (29, 31), (32, 42), (43, 60), (61, 100)]
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.YELLOW, Fore.RED]
    else:
        ranges = [(1, 38), (39, 43), (44, 50), (51, 58), (59, 100)]
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.YELLOW, Fore.RED]

    disp = bmi_bar(bmi_mapped, ranges, colors)
    print(f"BMI : {bmi:.2f} kg/m^2: " + disp)

    #----------------------------------------BODY FAT PERCENTAGE-----------------------------------------------

    if gender == 1: 
        if age < 18:
            print(f"Body Fat : {body_fat:.2f} % : " + fat_bar(1, round(body_fat), 10, 20))
        elif age < 65:
            print(f"Body Fat : {body_fat:.2f} % : " + fat_bar(1, round(body_fat), 10, 25))
        else:
            print(f"Body Fat : {body_fat:.2f} % : " + fat_bar(1, round(body_fat), 12, 26))
    
    else:
        if age < 18:
            print(f"Body Fat : {body_fat:.2f} % : " + fat_bar(2, round(body_fat), 15, 25))
        elif age < 65:
            print(f"Body Fat : {body_fat:.2f} % : " + fat_bar(2, round(body_fat), 18, 30))
        else:
            print(f"Body Fat : {body_fat:.2f} % : " + fat_bar(2, round(body_fat), 20, 33))
    
    #------------------------------------------LEAN BODY MASS------------------------------------------------------

    if gender == 1: 
        if age < 18:
            print(f"Lean Body Mass : {LBM:.2f} {unit} : " + fat_bar(1, round(LBM), 65, 80))
        elif age < 65:
            print(f"Lean Body Mass : {LBM:.2f} {unit} : " + fat_bar(1, round(LBM), 70, 85))
        else:
            print(f"Lean Body Mass : {LBM:.2f} {unit} : " + fat_bar(1, round(LBM), 65, 80))
    
    else:
        if age < 18:
            print(f"Lean Body Mass : {LBM:.2f} {unit} : " + fat_bar(2, round(LBM), 75, 80))
        elif age < 65:
            print(f"Lean Body Mass : {LBM:.2f} {unit} : " + fat_bar(2, round(LBM), 60, 80))
        else:
            print(f"Lean Body Mass : {LBM:.2f} {unit} : " + fat_bar(2, round(LBM), 55, 75))

    #------------------------------------------FAT FREE MASS INDEX----------------------------------------------------

    if age < 18:
        print(f"Fat Free Mass Index : {FFMI:.2f} : " + FFMI_bar(round(LBM), 16, 21))
    elif age < 65:
        print(f"Fat Free Mass Index : {FFMI:.2f} : " + FFMI_bar(round(LBM), 18, 22))
    else:
        print(f"Fat Free Mass Index : {FFMI:.2f} : " + FFMI_bar(round(LBM), 16, 20))


def sex():                                   #gender selection
    print("Please select your gender: \n 1> Male \n 2> Female")
    gender = int(input("Select option: "))
    while gender != 1 and gender != 2 and gender != 3:
        print("Select appropriate option.")
        print("Please select your gender: \n 1> Male \n 2> Female ")
        gender = int(input("Select option: "))
    return gender

def imperial():                                 #input for when imperial unit mode is selected
    age = int(input("Enter your Age: "))
    gender = sex()
    height_feet = int(input("Enter your height in feet: "))
    height_inches = int(input("Enter your height in inches: "))
    weight = float(input("Enter your weight: "))
    height = height_feet/12 + height_inches
    bmi = (weight / (height ** 2))

    if gender == 1: 
        body_fat = (1.20 * bmi) + (0.23 * age) - 16.2
    else:
        body_fat = (1.20 * bmi) + (0.23 * age) - 5.4
    
    LBM = weight * (1- body_fat/100)
    FFMI = LBM / ((height * 0.0254) ** 2)

    visual(age, gender, bmi, LBM, FFMI, body_fat, BMR)

def metric():                                 #input for when metric unit mode is selected
    age = int(input("Enter your Age: "))
    gender = sex()
    height = int(input("Enter your height in centimeters: "))
    weight = float(input("Enter your weight: "))
    bmi = (weight / ((height/100) ** 2))

    if gender == 1: 
        body_fat = (1.20 * bmi) + (0.23 * age) - 16.2
    else:
        body_fat = (1.20 * bmi) + (0.23 * age) - 5.4

    LBM = weight * (1- body_fat/100)
    FFMI = LBM / (height ** 2)

    visual(age, gender, bmi, LBM, FFMI, body_fat, BMR)

if mode == 1:                                  #is actually to start the entire process
    imperial()
else:
    metric()
