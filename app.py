import json
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>VisitLogger</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                text-align: center;
                padding-top: 100px;
            }
            h2 {
                font-size: 28px;
                margin-bottom: 20px;
            }
            button {
                font-size: 18px;
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h2>📌 출석 체크 시스템</h2>
        <p>이 버튼을 통해 출석체크를 하세요.</p>
        <button onclick="fetch('/visit').then(r => r.json()).then(d => alert('출석 완료!'))">
            출석 체크하기
        </button>
    </body>
    </html>
    '''

@app.route('/visit')
def visit():
    url = "https://vzwrszoqoj.execute-api.us-east-1.amazonaws.com/prod/click"
    response = requests.get(url)
    res_json = response.json()

    # Lambda가 body를 문자열로 주는 경우 처리
    if "body" in res_json:
        body_data = json.loads(res_json["body"])
        return jsonify(body_data)
    else:
        return jsonify(res_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
