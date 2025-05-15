from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html.j2', title="# My Flask App", message="This is a message for my Jinja template example!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)