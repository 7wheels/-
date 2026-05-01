"""
내주 영성팀 대시보드 서버
실행: python3 server.py
브라우저: http://localhost:5050
"""
import json, time, queue, threading
from pathlib import Path
from flask import Flask, Response, send_file, request

app = Flask(__name__)
BASE = Path(__file__).parent

# 클라이언트에게 전달할 이벤트 큐
_clients: list[queue.Queue] = []
_lock = threading.Lock()

def broadcast(event: dict):
    """모든 연결된 브라우저에 이벤트 전송"""
    data = json.dumps(event, ensure_ascii=False)
    with _lock:
        dead = []
        for q in _clients:
            try:
                q.put_nowait(data)
            except queue.Full:
                dead.append(q)
        for q in dead:
            _clients.remove(q)

# ── 대시보드 상태 업데이트 헬퍼 ──────────────────────────────────────
def agent_state(agent: str, state: str, message: str = ''):
    """에이전트 상태 변경 (idle / thinking / working / speaking)"""
    broadcast({'type': 'agent_state', 'agent': agent, 'state': state, 'message': message})

def log(agent: str, text: str):
    """사이드 로그에 메시지 추가"""
    broadcast({'type': 'log', 'agent': agent, 'text': text})

def progress(value: int):
    """진행률 0~100"""
    broadcast({'type': 'progress', 'value': value})

def status(text: str, session: str = ''):
    """전체 상태 텍스트"""
    broadcast({'type': 'status', 'text': text, 'session': session})

# ── 라우트 ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_file(BASE / 'index.html')

@app.route('/events')
def events():
    """Server-Sent Events 스트림"""
    q: queue.Queue = queue.Queue(maxsize=50)
    with _lock:
        _clients.append(q)

    def stream():
        yield 'data: {"type":"ping"}\n\n'
        try:
            while True:
                try:
                    data = q.get(timeout=30)
                    yield f'data: {data}\n\n'
                except queue.Empty:
                    yield ': keepalive\n\n'
        except GeneratorExit:
            with _lock:
                if q in _clients:
                    _clients.remove(q)

    return Response(stream(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

@app.route('/api/broadcast', methods=['POST'])
def api_broadcast():
    """외부 스크립트에서 이벤트를 전송하는 API"""
    data = request.get_json()
    broadcast(data)
    return {'ok': True}

# ── 데모 시나리오 (서버 측) ───────────────────────────────────────────
@app.route('/api/demo')
def run_demo():
    def _run():
        import time
        steps = [
            (0.5,  lambda: [status('회의 진행 중...', '워맥 은혜 신학 뉴스레터 작성'),
                             agent_state('영성', 'speaking', '팀을 소집합니다.')]),
            (1.5,  lambda: [agent_state('영성', 'working'),
                             log('영성', '요한·마태·안드레에게 임무를 부여합니다.')]),
            (1.0,  lambda: [agent_state('요한', 'thinking'),
                             agent_state('마태', 'thinking'),
                             agent_state('안드레', 'thinking'),
                             progress(15),
                             log('요한', '워맥 은혜 신학 성경 근거 분석 시작.'),
                             log('마태', '뉴스레터 구조 설계 시작.'),
                             log('안드레', '독자 공감 포인트 기획 시작.')]),
            (2.5,  lambda: [agent_state('요한', 'speaking', 'elp 2:8-9\n은혜로 구원받았으니'),
                             progress(40)]),
            (1.5,  lambda: [agent_state('마태', 'speaking', '훅→본문→선언문\n→실천 과제'),
                             progress(55)]),
            (1.5,  lambda: [agent_state('안드레', 'speaking', '"은혜는 노력이\n아닙니다"'),
                             progress(70)]),
            (1.5,  lambda: [agent_state('요한', 'idle'), agent_state('마태', 'idle'),
                             agent_state('안드레', 'idle'),
                             agent_state('도마', 'thinking'),
                             log('도마', '초안 검토 — 번영신학 혼합 위험 점검 중...')]),
            (2.0,  lambda: [agent_state('도마', 'speaking', '⚠️ "원하면 이루어진다"\n표현 수정 필요'),
                             log('도마', '수정 권고: 끌어당김 언어 → 성경 언어로 재번역.')]),
            (1.5,  lambda: [agent_state('도마', 'idle'),
                             agent_state('영성', 'speaking', '통합 완료!\n뉴스레터 1호 완성'),
                             progress(100),
                             log('영성', '최종 통합 완료. 도마 피드백 반영. 저장.')]),
            (2.0,  lambda: [agent_state('영성', 'idle'), status('완료 ✓')]),
        ]
        for delay, actions in steps:
            time.sleep(delay)
            result = actions()
            if isinstance(result, list):
                for r in result:
                    pass  # 이미 broadcast 완료

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return {'ok': True}

if __name__ == '__main__':
    print('=' * 50)
    print('  내주 영성팀 대시보드')
    print('  http://localhost:5050')
    print('=' * 50)
    app.run(host='0.0.0.0', port=5050, debug=False, threaded=True)
