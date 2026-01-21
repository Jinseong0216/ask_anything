from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        problem = request.form.get("problem").strip()

        if not name:
            name = "익명"

        print("질문 도착")
        print("이름:", name)
        print("문제 번호:", problem)
        print("시간:", datetime.now())
        print("-" * 30)

        return render_template("index.html", success=True)

    return render_template("index.html", success=False)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
