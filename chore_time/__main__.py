from flask import Flask
app = Flask(__name__)


@app.route('/')
def main():
    return 'hi'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5678, debug=True)
