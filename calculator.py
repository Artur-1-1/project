from flask import Flask, session, render_template, request
app = Flask(__name__)
app.secret_key = "секретний_ключ"

@app.route("/", methods=["GET", "POST"])
def index():
    result = session.get("last_result")  # Отримаємо результат з сесії

    if request.method == "POST":
        user_input = request.form.get("user_input")  # назва має збігатись з name="user_input"
        if user_input:
            try:
                parts = user_input.split()
                a = int(parts[0])
                op = parts[1]
                b = int(parts[2])

                if op == "+":
                    result = a + b
                elif op == "-":
                    result = a - b
                elif op == "*":
                    result = a * b
                elif op == "/":
                    result = a / b
                else:
                    result = "Невідома операція"

                session["last_result"] = result  # Зберігаємо в сесію
            except Exception as e:
                result = "Помилка: " + str(e)

    return render_template("calculator.html", result=result)


