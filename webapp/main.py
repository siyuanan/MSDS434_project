efrom flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Welcome to the new app!"

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port = 8080, debug = True)
