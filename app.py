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
    </head>
    <body>
        <h2>🚪 방문 버튼</h2>
        <button onclick="fetch('/visit').then(r => r.json()).then(d => alert(d.message))">
            방문 기록 남기기
        </button>
    </body>
    </html>
    '''

@app.route('/visit')
def visit():
    # 아래 URL을 본인의 API Gateway /click 주소로 바꿔주세요
    url = "https://vzwrszoqoj.execute-api.us-east-1.amazonaws.com/prod/click"
    response = requests.get(url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
