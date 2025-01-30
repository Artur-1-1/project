def fun():
        print("Such an option does not exist!")
while True:
    try:
        v = input("\nCalculator option:\nOrdinary calkulator - 1 \nPifagorean teorem - 2 \nCircle perimeter - 3\nVolume - 4\n: ")
        if v == "1":
            a = int(input("1 number: "))
            b = int(input("2 number: "))
            c = input("operation: ")
            if c == "+":
                print(f"answer: {a + b}")
            elif c == "_":
                print(f"answer: {a - b}")
            elif c == "*":
                print(f"answer: {a * b}")
            elif c == "/":
                print(f"answer: {a / b}")
            else:
                fun()
        elif v == "2":
            d = int(input("1 number: "))
            e = int(input("2 number: "))
            f = d ** 2 + e ** 2
            r = f ** 0.5
            print("hypotenuse: ")
        elif v == "3":
            y = input("Radius/Diameter:\nRadius - 1\nDiameter - 2\n: ")
            if y == "1":
                p = int(input("number: "))
                o = p * 2
                print(f"Answer: {o * 3.14}")
            elif y == "2":
                p = int(input("number: "))
                print(f"Answer: {p * 3.14}")
            else:
                fun()
        elif v == "4":
            x = input("Volume/Area:\nVolume - 1\nArea - 2\n: ")
            if x == "1":
                l = int(input("number in mm:"))
                print(f"answer: {l ** 2}")
            elif x == "2":
                l = int(input("number in mm:"))
                print(f"answer: {l ** 3}")
            else:
                fun()
        else:
            fun()
    except ValueError: 
        print("Incorrect data format!")
    except ZeroDivisionError:
        print("Cannot be divided by zero!")
    finally:
        exit = input("Do u want to exit?\n: ")
        if exit == "yes" or exit == "Yes":
            break