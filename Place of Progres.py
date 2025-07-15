from flask import Flask, render_template,  request, redirect, session
from asteval import Interpreter
import random,datetime,csv,math
aeval = Interpreter()
def easy_math():
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    x = random.choice(['-', '+'])
    expr = (f"{a} {x} {b} ")
    result = aeval(expr)
    wrong = [result + random.randint(1, 2), result - random.randint(1, 2), result + 3]
    answers = [result] + wrong
    random.shuffle(answers)
    return expr, result, answers
def medium_math():
    a = random.randint(1, 100)
    b = random.randint(1, 10)
    x = random.choice(['/', '*'])
    expr = (f"{a} {x} {b} ")
    result = aeval(expr)
    result = round(result, 1)
    wrong = [round(result + random.choice([1, 2, 0.1, 0.2]), 1), round(result - random.choice([1, 2, 0.1, 0.2]), 1), round(result - random.choice([3, 0.3]), 1)]
    answers = [result] + wrong
    if answers in [0.3, 0.4, 0.6, 0.7, 0.8, 0.9]:
        return medium_math
    random.shuffle(answers)
    return expr, result, answers
def hard_math():
    sqrt = random.choice([True, False])
    x = random.choice(['**', math.sqrt])
    if x == '**':
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        expr = (f"{a} {x} {b} ")
        exp = (f"{a}^{b}")
    elif x == math.sqrt:
        a = random.randint(1, 20) ** 2
        b = random.randint(1, 20)
        if sqrt == True:
            v = random.choice(['-', '+'])
            expr = (f"{math.sqrt(a)} {v} {b}")
            exp = (f"√{a} {v} √{b ** 2}")
        else:
            v = random.choice(['-', '+'])
            expr = (f"{math.sqrt(a)} {v} {b}")
            exp = (f"√{a} {v} {b}")
    result = round(aeval(expr), 1)
    wrong = [result + random.choice([1, 2]), result - random.choice([1, 2]), result + 3]
    answers = [result] + wrong
    random.shuffle(answers)
    return exp, result, answers
def load_facts():
    with open('facts.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row['fact'] for row in reader]
notes = []
books = []
app = Flask(__name__)
app.secret_key = "PoP"
FACTS = load_facts()
@app.route("/", methods=["GET", "POST"])
def home():
    fact = random.choice(FACTS)
    current_day = datetime.datetime.now().strftime('%A')
    uk_days = {
        "Monday": "Понеділок", "Tuesday": "Вівторок", "Wednesday": "Середа",
        "Thursday": "Четвер", "Friday": "Пʼятниця", "Saturday": "Субота", "Sunday": "Неділя"
    }

    schedule = session.get("schedule_data", {})
    return render_template("Main_Project.html", Main_Project="home", title="Place of Progres", fact=fact, current_day=uk_days[current_day], schedule=schedule)
@app.route("/math", methods=["GET"])
def math_page():
    return render_template("Main_Project.html", Main_Project="math_page", title="PoP Math")
@app.route("/calculator", methods=["GET", "POST"])
def calculator_page():
    result = None
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
                elif op == "**":
                    result = a ** b
                elif op == "sq":
                    result = math.sqrt(a)
                else:
                    result = "Невідома операція"
            except Exception as e:
                result = "Помилка: " + str(e)
    return render_template("Main_Project.html", Main_Project="calculator_page", title="PoP Calculator", result=result)
@app.route("/mathtest", methods=["GET", "POST"])
def math_test():
    if request.method == "POST":
        # Старт тесту
        if "start_test" in request.form:
            session["total_questions"] = int(request.form["num_questions"])
            session["difficulty"] = request.form["difficulty"]
            session["current"] = 0
            session["score"] = 0
            session["math_results"] = []
            return redirect("/mathtest")

        # Обробка відповіді
        selected = request.form.get("answer")
        correct = session.get("correct")
        question_text = session.get("question_text")  # Вираз

        if selected:
            # Збереження результату
            session["math_results"].append({
                "question": question_text,
                "user": selected,
                "correct": correct
            })

            # Оцінювання
            if float(selected) == float(correct):
                session["score"] += 1

        session["current"] += 1

        if session["current"] >= session["total_questions"]:
            score = session.pop("score", 0)
            total = session.pop("total_questions", 0)
            results = session.pop("math_results", [])
            session.pop("current", None)
            session.pop("correct", None)
            session.pop("question_text", None)
            session.pop("difficulty", None)
            return render_template("Main_Project.html", Main_Project="math_test_result",
                                   score=score, total=total, results=results)

    # Генерація нового запитання
    if "current" in session:
        difficulty = session.get("difficulty", "easy")
        if difficulty == "medium":
            expr, result, answers = medium_math()
        elif difficulty == "hard":
            expr, result, answers = hard_math()
        else:
            expr, result, answers = easy_math()

        session["correct"] = result
        session["question_text"] = expr

        return render_template("Main_Project.html", Main_Project="math_question", title="Тест",
                               expr=expr, answers=answers,
                               current=session["current"] + 1,
                               total=session["total_questions"])

    # Початковий екран
    return render_template("Main_Project.html", Main_Project="math_start", title="PoP MathT")
@app.route("/notes", methods=["GET", "POST"])
def notes():
    if "notes" not in session:
        session["notes"] = []
    error = None
    if request.method == "POST":
        if "delete_title" in request.form:
            # Видалення за заголовком
            title_to_delete = request.form["delete_title"]
            session["notes"] = [note for note in session["notes"] if note["title"] != title_to_delete]
            session.modified = True
        else:
            # Додавання нової нотатки
            title = request.form.get("title")
            content = request.form.get("content")
            if title and content:
                for note in session["notes"]:
                    if note["title"] == title:
                        error = "❗ Нотатка з таким заголовком вже існує"
                        break
                else:
                    session["notes"].append({"title": title, "content": content})
                    session.modified = True
    return render_template("Main_Project.html", Main_Project="notes_page", title="PoP Notes", notes=session["notes"], error=error)
@app.route("/schedule", methods=["GET", "POST"])
def schedule_page():
    if "schedule_data" not in session:
        session["schedule_data"] = {
            "Понеділок": ["Математика", "Українська"],
            "Вівторок": ["Фізика", "Історія"],
            "Середа": ["Біологія", "Англійська"],
            "Четвер": ["Хімія", "Мистецтво"],
            "П’ятниця": ["Географія", "Фізкультура"],
            "Розклад дзвінків": [
                "1. 08:30 - 09:15",
                "2. 09:25 - 10:10",
                "3. 10:20 - 11:05",
                "4. 11:15 - 12:00",
                "5. 12:10 - 12:55",
                "6. 13:05 - 13:50"
            ]
        }

    schedule_data = session["schedule_data"]

    if request.method == "POST":
        for day in schedule_data:
            new_lessons = request.form.get(day)
            if new_lessons is not None:
                session["schedule_data"][day] = [line.strip() for line in new_lessons.split('\n') if line.strip()]
        session.modified = True
        return redirect("/schedule")
        
    return render_template("Main_Project.html", Main_Project="schedule_edit", title="PoP Schedule", schedule=schedule_data)
@app.route("/library", methods=["GET", "POST"])
def library():
    if "books" not in session:
        session["books"] = []
    error = None
    if request.method == "POST":
        if "delete_title" in request.form:
            # Видалення за заголовком
            title_to_delete = request.form["delete_title"]
            session["books"] = [book for book in session["books"] if book["name"] != title_to_delete]
            session.modified = True
        else:
            # Додавання нової книги
            name = request.form.get("name")
            author = request.form.get("author")
            if name and author:
                for book in session["books"]:
                    if book["name"] == name:
                        error = "❗ Нотатка з таким заголовком вже існує"
                        break
                else:
                    session["books"].append({"name": name, "author": author})
                    session.modified = True
    return render_template("Main_Project.html", Main_Project="library", title="Pop Library", books=session["books"], error=error)
@app.route("/words", methods=["GET"])
def words_menu():
    return render_template("Main_Project.html", Main_Project="words_menu", title="PoP Words")
@app.route("/word_test", methods=["GET", "POST"])
def word_test():
    if "word_dict" not in session or len(session["word_dict"]) == 0:
        return "⚠️ Словник порожній!"

    if request.method == "POST":
        user_answer = request.form.get("answer")
        correct_answer = session.get("current_word_correct")
        current_question = session.get("current_word_question")
        if user_answer == correct_answer:
            session["word_test_score"] += 1
        session["word_test_answers"].append({
            "question": current_question,
            "correct": correct_answer,
            "user": user_answer
        })
        session["word_test_current"] += 1
        if session["word_test_current"] >= session["word_test_total"]:
            score = session.pop("word_test_score", 0)
            total = session.pop("word_test_total", 0)
            results = session.pop("word_test_answers", [])
            session.pop("word_dict", None)
            return render_template("Main_Project.html", Main_Project="word_test_result", title="PoP WordsT", score=score, total=total, results=results)

    # Генеруємо нове питання
    word_list = session["word_dict"]
    current = word_list[session["word_test_current"]]
    direction = random.choice(["forward", "reverse"])
    if direction == "forward":
        question = current["word"]
        correct = current["translation"]
    else:
        question = current["translation"]
        correct = current["word"]

    options = [correct]
    while len(options) < 4:
        opt = random.choice(word_list)
        val = opt["translation"] if direction == "forward" else opt["word"]
        if val not in options:
            options.append(val)
    random.shuffle(options)

    session["current_word_question"] = question
    session["current_word_correct"] = correct

    return render_template("Main_Project.html", Main_Project="word_question", title="PoP WordsT", question=question, options=options,current=session["word_test_current"] + 1,total=session["word_test_total"])
@app.route("/words_dict", methods=["GET", "POST"])
def words_dict():
    if "words" not in session:
        session["words"] = []
    error = None
    if request.method == "POST":
        if "delete_title" in request.form:
            title_to_delete = request.form["delete_title"]
            session["words"] = [entry for entry in session["words"] if entry["word"] != title_to_delete]
            session.modified = True
        else:
            word = request.form.get("word", "").strip()
            translation = request.form.get("translation", "").strip()
            note = request.form.get("note", "").strip()
            if word and translation:
                for entry in session["words"]:
                    if entry["word"] == word:
                        error = "❗️Таке слово вже існує у словнику"
                        break
                else:
                    session["words"].append({
                        "word": word,
                        "translation": translation,
                        "note": note
                    })
                    session.modified = True
            else:
                error = "❗️Заповніть обов'язкові поля"
    return render_template("Main_Project.html", Main_Project="words_dict", title="PoP Dict", words=session["words"], error=error)
@app.route("/word_test_setup", methods=["GET", "POST"])
def word_test_setup():
    if "words" not in session or len(session["words"]) == 0:
        return "⚠️ Словник порожній!"

    if request.method == "POST":
        total = int(request.form.get("num_questions", 5))
        if len(session["words"]) < total:
            return "⚠️ Недостатньо слів для тесту."
        session["word_dict"] = session["words"].copy()
        random.shuffle(session["word_dict"])
        session["word_test_total"] = total
        session["word_test_score"] = 0
        session["word_test_current"] = 0
        session["word_test_answers"] = []
        return redirect("/word_test")
    
    return render_template("Main_Project.html", Main_Project="word_test_setup", title="PoP WordsT")


if __name__ == "__main__":
    app.run(debug=True)
