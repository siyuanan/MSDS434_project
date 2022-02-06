from flask import Flask

app = Flask(__name__)

def welcome():
    return "Welcome to the new app!"

def title_line():
    return "This is for mobile price prediction"

@app.route("/")
def main_func(): 
    print(welcome)
    print('\n')
    print(title_line)

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port = 8080, debug = True)
