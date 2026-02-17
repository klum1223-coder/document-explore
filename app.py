from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime
import os
import json

app = Flask(__name__)

# ZeroClaw 표준에 맞춘 데이터베이스 초기화
def init_db():
    db_path = 'research-hub/data/knowledge.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 지식 베이스 (ZeroClaw 호환 필드 추가)
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge_base
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  topic TEXT, 
                  title TEXT, 
                  link TEXT, 
                  snippet TEXT, 
                  source_type TEXT,
                  importance FLOAT DEFAULT 1.0,
                  confidence FLOAT DEFAULT 0.8,
                  tags TEXT,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # ZeroClaw 연동 로그 및 마이그레이션 상태 기록용
    c.execute('''CREATE TABLE IF NOT EXISTS system_state
                 (key TEXT PRIMARY KEY, value TEXT)''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    # ZeroClaw의 '하이브리드 검색'을 흉내낸 로직
    # 향후 zeroclaw-engine이 활성화되면 이 부분에서 직접 벡터 검색을 수행하게 됩니다.
    
    conn = sqlite3.connect('research-hub/data/knowledge.db')
    c = conn.cursor()
    # 지식 조각 생성 (추후 실시간 수집 연동)
    c.execute("INSERT INTO knowledge_base (topic, title, link, snippet, source_type, tags) VALUES (?, ?, ?, ?, ?, ?)",
              (query, f"{query}에 대한 최신 연구 동향", "#", f"'{query}' 주제를 ZeroClaw 엔진이 분석 중입니다. 심층 학습을 통해 곧 구체적인 데이터가 업데이트됩니다.", "ZeroClaw-Agent", "research,auto-evolve"))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": f"ZeroClaw 엔진이 '{query}' 주제에 대한 지식 이식을 시작했습니다."})

@app.route('/recent-knowledge')
def recent_knowledge():
    conn = sqlite3.connect('research-hub/data/knowledge.db')
    c = conn.cursor()
    c.execute("SELECT topic, title, link, snippet, confidence FROM knowledge_base ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    
    return jsonify([{"topic": r[0], "title": r[1], "link": r[2], "snippet": r[3], "confidence": r[4]} for r in rows])

@app.route('/learning-status')
def learning_status():
    conn = sqlite3.connect('research-hub/data/knowledge.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM knowledge_base")
    count = c.fetchone()[0]
    conn.close()
    
    # ZeroClaw 스타일의 진화 레벨 계산
    level = (count // 5) + 1
    return jsonify({
        "knowledge_count": count,
        "level": level,
        "engine": "ZeroClaw Hybrid Engine (Injected)",
        "evolution_stage": "Migration Ready"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
