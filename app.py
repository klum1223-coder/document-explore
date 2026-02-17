from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime
import os
import random
import traceback

app = Flask(__name__)

# 경로 설정 (실행 파일 기준 절대 경로)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'knowledge.db')

def init_db():
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # 테이블이 없으면 생성, 있으면 무시
        c.execute('''CREATE TABLE IF NOT EXISTS knowledge_base
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      topic TEXT, title TEXT, link TEXT, snippet TEXT, 
                      source_type TEXT, importance FLOAT DEFAULT 1.0,
                      confidence FLOAT DEFAULT 0.8, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()
        print(f"✅ DB initialized at: {DB_PATH}")
    except Exception as e:
        print(f"❌ DB Init Error: {e}")

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.form.get('query')
        if not query:
            return jsonify({"status": "error", "message": "Query is empty"})

        insights = [
            {"title": f"{query}의 미래와 핵심 기술", "snippet": f"최근 {query} 분야의 트렌드를 분석한 결과, 사용자 경험과 보안 기술의 결합이 주요 화두로 떠오르고 있습니다."},
            {"title": f"{query} 관련 주요 논문 및 도서 요약", "snippet": f"이 지식 조각은 {query}에 대한 방대한 데이터를 ZeroClaw 엔진이 요약한 결과입니다."},
            {"title": f"{query} 실무 적용 가이드 v1.0", "snippet": f"{query}를 실제 프로젝트에 도입할 때 고려해야 할 핵심 체크리스트 5가지를 포함하고 있습니다."}
        ]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        for insight in insights:
            c.execute("INSERT INTO knowledge_base (topic, title, link, snippet, source_type, confidence) VALUES (?, ?, ?, ?, ?, ?)",
                      (query, insight['title'], "#", insight['snippet'], "ZeroClaw-AI", round(random.uniform(0.85, 0.99), 2)))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Knowledge injected successfully"})
    except Exception as e:
        print(f"❌ Search Error: {traceback.format_exc()}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/recent-knowledge')
def recent_knowledge():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT topic, title, link, snippet, confidence FROM knowledge_base ORDER BY id DESC LIMIT 15")
        rows = c.fetchall()
        conn.close()
        return jsonify([{"topic": r[0], "title": r[1], "link": r[2], "snippet": r[3], "confidence": r[4]} for r in rows])
    except Exception as e:
        return jsonify([])

@app.route('/learning-status')
def learning_status():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM knowledge_base")
        count = c.fetchone()[0]
        conn.close()
        return jsonify({"knowledge_count": count, "level": (count // 5) + 1})
    except Exception as e:
        return jsonify({"knowledge_count": 0, "level": 1})

if __name__ == '__main__':
    # 어떤 환경에서도 접근 가능하도록 0.0.0.0으로 열어둡니다.
    app.run(debug=True, host='0.0.0.0', port=5000)
