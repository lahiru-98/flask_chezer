from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Your App is Working'

if __name__ == "__main__":
    app.run()
