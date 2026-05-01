"""
내주 영성팀 대시보드 서버
실행: python3 server.py
브라우저: http://localhost:5050
"""
import json, re, time, queue, threading, datetime, os
from pathlib import Path
from flask import Flask, Response, send_file, request

app = Flask(__name__)

# server.py 가 있는 폴더를 기준으로 지식베이스 경로 설정
SERVER_DIR = Path(__file__).resolve().parent
KB_BASE    = SERVER_DIR / 'knowledge-base'
TEXT_BASE  = SERVER_DIR / 'source-files' / 'text'

# 클라이언트에게 전달할 이벤트 큐
_clients: list[queue.Queue] = []
_lock = threading.Lock()

def broadcast(event: dict):
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

def agent_state(agent: str, state: str, message: str = ''):
    broadcast({'type': 'agent_state', 'agent': agent, 'state': state, 'message': message})

def log(agent: str, text: str):
    broadcast({'type': 'log', 'agent': agent, 'text': text})

def progress(value: int):
    broadcast({'type': 'progress', 'value': value})

def status(text: str, session: str = ''):
    broadcast({'type': 'status', 'text': text, 'session': session})

def result(agent: str, title: str, content: str):
    """결과물을 대시보드 결과물 패널에 표시"""
    broadcast({'type': 'result', 'agent': agent, 'title': title, 'content': content})

# ── 라우트 ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_file(SERVER_DIR / 'index.html')

@app.route('/events')
def events():
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
    data = request.get_json()
    broadcast(data)
    return {'ok': True}

@app.route('/api/result', methods=['POST'])
def api_result():
    """외부에서 결과물을 대시보드에 전송"""
    data    = request.get_json()
    agent   = data.get('agent', '영성')
    title   = data.get('title', '결과물')
    content = data.get('content', '')
    result(agent, title, content)
    return {'ok': True}

# ── 유튜브 카테고리 분류 ──────────────────────────────────────────────
CATEGORIES = {
    '영혼몸': 'spirit-soul-body',   'spirit':     'spirit-soul-body',
    '권세':   'believers-authority','authority':  'believers-authority',
    '은혜':   'grace-faith',        'grace':      'grace-faith',
    '이미':   'already-got-it',     'already':    'already-got-it',
    '노력':   'effortless-change',  'effortless': 'effortless-change',
    '제한':   'dont-limit-god',     'limit':      'dont-limit-god',
    '안식':   'sabbath',            'sabbath':    'sabbath',
    '정체성': 'identity',           'identity':   'identity',
}

def _categorize(text: str) -> str:
    t = text.lower()
    for kw, cat in CATEGORIES.items():
        if kw in t:
            return cat
    return 'general'

def _get_video_id(url: str) -> str:
    m = re.search(r'(?:v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})', url)
    return m.group(1) if m else url.strip()

def _fetch_transcript(video_id: str):
    """한국어 → 영어 → 아무 언어 순서로 자막 가져오기 (0.5.x / 0.6.x 모두 호환)"""
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    use_new = hasattr(api, 'fetch')  # 0.6.x

    def fetch_langs(langs):
        if use_new:
            return list(api.fetch(video_id, languages=langs))
        return YouTubeTranscriptApi.get_transcript(video_id, languages=langs)

    def list_all():
        if use_new:
            return api.list(video_id)
        return YouTubeTranscriptApi.list_transcripts(video_id)

    def to_dict(entry):
        if isinstance(entry, dict):
            return entry
        return {'text': entry.text, 'start': entry.start}

    for langs, label in [(['ko'], '한국어'), (['en'], '영어')]:
        try:
            raw = fetch_langs(langs)
            return label, [to_dict(e) for e in raw]
        except Exception:
            pass

    try:
        tl   = list_all()
        t    = next(iter(tl))
        raw  = list(t.fetch()) if hasattr(t, 'fetch') else list(t)
        lang = getattr(t, 'language', '알 수 없음')
        return f'{lang} (자동생성)', [to_dict(e) for e in raw]
    except Exception as e:
        raise RuntimeError(f'자막 없음: {e}')

def _transcript_to_md(video_id, title, lang, transcript):
    lines = [
        f'# {title}', '',
        f'> 출처: https://youtu.be/{video_id}',
        f'> 언어: {lang} | 추출일: {datetime.date.today()}', '',
        '## 전체 내용', '',
    ]
    chunk, chunk_start = [], None
    for e in transcript:
        s = e['start']
        if chunk_start is None:
            chunk_start = s
        chunk.append(e['text'].strip())
        if s - chunk_start >= 30:
            mm, ss = int(chunk_start // 60), int(chunk_start % 60)
            lines.append(f'**[{mm:02d}:{ss:02d}]** {" ".join(chunk)}')
            lines.append('')
            chunk, chunk_start = [], None
    if chunk:
        lines.append(' '.join(chunk))
    return '\n'.join(lines)

# ── 유튜브 추출 API ───────────────────────────────────────────────────
@app.route('/api/youtube', methods=['POST'])
def api_youtube():
    data  = request.get_json()
    url   = (data.get('url') or '').strip()
    title = (data.get('title') or '').strip()

    if not url:
        return {'ok': False, 'error': 'URL이 없습니다.'}, 400

    try:
        vid        = _get_video_id(url)
        used_title = title or f'워맥_{vid}'
        cat        = _categorize(used_title)

        agent_state('안드레', 'thinking', '자막 가져오는 중')
        log('안드레', f'🎬 자막 추출 시작: {url}')
        progress(20)

        lang, transcript = _fetch_transcript(vid)
        progress(50)

        md = _transcript_to_md(vid, used_title, lang, transcript)

        # 지식베이스 저장
        cat_dir = KB_BASE / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        safe    = re.sub(r'[^\w가-힣\-_]', '_', used_title)[:60]
        out     = cat_dir / f'{safe}.md'
        out.write_text(md, encoding='utf-8')

        # 원본 자막 보관
        TEXT_BASE.mkdir(parents=True, exist_ok=True)
        (TEXT_BASE / f'{safe}_원본자막.txt').write_text(
            '\n'.join(e['text'] for e in transcript), encoding='utf-8')

        progress(100)
        agent_state('안드레', 'working', '지식베이스 저장 중')
        log('안드레', f'📚 저장 완료 → knowledge-base/{cat}/{out.name}')
        agent_state('안드레', 'speaking', '추출 완료!')
        status('유튜브 추출 완료 ✓')

        return {'ok': True, 'category': cat, 'file': out.name}

    except Exception as e:
        agent_state('안드레', 'idle')
        log('도마', f'⚠️ 추출 오류: {e}')
        status('추출 실패')
        return {'ok': False, 'error': str(e)}, 500

# ── 데모 시나리오 ─────────────────────────────────────────────────────
@app.route('/api/demo')
def run_demo():
    def _run():
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
            (2.5,  lambda: [agent_state('요한', 'speaking', 'Eph 2:8-9\n은혜로 구원받았으니'),
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
                             log('영성', '최종 통합 완료. 도마 피드백 반영. 저장.'),
                             result('영성', '워맥 은혜 신학 뉴스레터 1호',
"""# 은혜: 하나님의 선물, 내 것이 아닌 것이 내 것이 되는 방법

> "너희가 그 은혜를 인하여 믿음으로 말미암아 구원을 얻었으니" — 에베소서 2:8

## 📖 이번 호 핵심 메시지

은혜는 **우리의 노력으로 얻는 것이 아닙니다.**
하나님이 이미 주신 것을 믿음으로 받는 것입니다.

## 🔑 세 가지 핵심 진리

- **이미 완성됨** — 십자가에서 모든 것이 완성되었습니다
- **받는 자격** — 자격이 없어서가 아니라, 자격 없는 자에게 주시는 것이 은혜입니다
- **믿음의 통로** — 믿음은 은혜를 생산하지 않고, 은혜를 받는 통로입니다

## 💡 이번 주 실천 선언

> "나는 은혜로 구원받은 하나님의 자녀입니다.
> 내 행위가 아닌 그리스도의 완성된 사역이 나의 기초입니다."

---
*내주 영성팀 · 워맥 은혜 신학 뉴스레터*""")]),
            (2.0,  lambda: [agent_state('영성', 'idle'), status('완료 ✓')]),
        ]
        for delay, actions in steps:
            time.sleep(delay)
            actions()

    threading.Thread(target=_run, daemon=True).start()
    return {'ok': True}

if __name__ == '__main__':
    print('=' * 50)
    print('  내주 영성팀 대시보드')
    print(f'  저장 위치: {KB_BASE}')
    print('  http://localhost:5050')
    print('=' * 50)
    app.run(host='0.0.0.0', port=5050, debug=False, threaded=True)
