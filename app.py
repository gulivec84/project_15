from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import csv
from collections import Counter

app = Flask(__name__)
app.secret_key = "secret_key"
app.config["UPLOAD_FOLDER"] = "uploads"

def process_csv(file_path):
    data = []
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            director = row[6].strip()  # Индекс столбца с режиссером, удаление начальных и конечных пробелов
            if director == "Spielberg, Steven":
                data.append(row)
    return data

@app.route("/", methods=["GET", "POST"])
def index():
    data = []  # Используется заглушка для данных по умолчанию
    success_message = None
    error_message = None
    chart_data = None  # Данные для графика

    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            data = process_csv(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            success_message = "File uploaded successfully!"
            # Вычисление количества фильмов по годам
            years = [row[0] for row in data]  # Предполагается, что год находится по индексу 0
            count_by_year = dict(Counter(years))
            chart_data = {
                "labels": list(count_by_year.keys()),
                "data": list(count_by_year.values())
            }
        else:
            error_message = "Invalid file format! Please upload the CSV file."

    # Пример данных
    example_data = [
        ["1993","127","Jurassic Park","","","", "Spielberg, Steven"],
        ["1975","124","Jaws","","","","Spielberg, Steven"],
        ["1982","115","E.T. the Extra-Terrestrial","","","","Spielberg, Steven"],
        ["1998","169","Saving Private Ryan","","","","Spielberg, Steven"],
        ["1981","115","Raiders of the Lost Ark","","","","Spielberg, Steven"],
    ]

    example_chart_data = {
        "labels": ["1993", "1975", "1982", "1998", "1981"],
        "data": [1, 1, 1, 1, 1]
    }

    if not data:
        data = example_data
        chart_data = example_chart_data

    return render_template("index.html", data=data, success_message=success_message, error_message=error_message, chart_data=chart_data)

if __name__ == "__main__":
    app.run()
