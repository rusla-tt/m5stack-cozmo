from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/cozmomidi', methods=['GET'])
def cozmomidi():
    subprocess.call('python', 'main.py')
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)