# app.py v1.0.0.0.4

from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ AIKO LINE Bot 起動中", 200

if __name__ == "__main__":
    app.run(debug=True)