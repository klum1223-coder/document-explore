from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime
import os

app = Flask(__name__)

# 데이터베이스 초기화 (학습 및 저장용)
def init_db():
    conn = sqlite3.connect('research-hub/data/knowledge.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS search_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT, timestamp DATETIME)''')
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge_base
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT, title TEXT, link TEXT, snippet TEXT, source_type TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    # 여기에 실제 검색 로직(OpenClaw의 web_search 연동)이 들어갑니다.
    # 지금은 구조를 잡기 위해 더미 데이터를 반환하거나, 검색 후 DB에 저장하는 로직을 시뮬레이션합니다.
    
    conn = sqlite3.connect('research-hub/data/knowledge.db')
    c = conn.cursor()
    c.execute("INSERT INTO search_history (query, timestamp) VALUES (?, ?)", (query, datetime.datetime.now()))
    conn.commit()
    conn.close()
    
    # 이 부분은 나중에 제가 직접 검색 결과를 넣어주는 API로 확장될 예정입니다.
    return jsonify({"status": "success", "message": f"'{query}' 주제에 대한 학습 및 검색을 시작합니다."})

@app.route('/learning-status')
def learning_status():
    # 학습된 데이터 양을 보여주는 API
    conn = sqlite3.connect('research-hub/data/knowledge.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM search_history")
    search_count = c.fetchone()[0]
    conn.close()
    return jsonify({"search_count": search_count, "level": search_count // 5 + 1})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
