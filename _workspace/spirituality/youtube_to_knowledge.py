"""
유튜브 영상 → 지식 베이스 추출 스크립트
자막(한국어/영어)을 추출하여 마크다운으로 저장
"""
import re, os, datetime
from pathlib import Path

# 이 스크립트가 spirituality/ 안에 있으면 그 폴더를 BASE로,
# dashboard/ 같은 하위 폴더에서 실행될 경우 부모 폴더를 BASE로 사용
_here = Path(__file__).resolve().parent
if (_here / 'knowledge-base').exists() or (_here / 'source-files').exists():
    BASE = _here
elif (_here.parent / 'knowledge-base').exists() or (_here.parent / 'source-files').exists():
    BASE = _here.parent
else:
    # 어디서 실행해도 스크립트 옆에 폴더 생성
    BASE = _here

OUT_TEXT = BASE / 'source-files/text'
OUT_KB   = BASE / 'knowledge-base'

# ── 키워드 → 카테고리 (extract_to_knowledge.py와 동일) ──────────────
CATEGORIES = {
    '영혼몸': 'spirit-soul-body',   'spirit': 'spirit-soul-body',
    '권세':   'believers-authority','authority': 'believers-authority',
    '은혜':   'grace-faith',        'grace': 'grace-faith',
    '이미':   'already-got-it',     'already': 'already-got-it',
    '노력':   'effortless-change',  'effortless': 'effortless-change',
    '제한':   'dont-limit-god',     'limit': 'dont-limit-god',
    '안식':   'sabbath',            'sabbath': 'sabbath',
    '정체성': 'identity',           'identity': 'identity',
}

def categorize(text: str) -> str:
    t = text.lower()
    for kw, cat in CATEGORIES.items():
        if kw in t:
            return cat
    return 'general'

def get_video_id(url: str) -> str:
    """유튜브 URL에서 video ID 추출"""
    patterns = [
        r'(?:v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return url.strip()  # ID 직접 입력한 경우

def fetch_transcript(video_id: str) -> tuple[str, list]:
    """자막 가져오기 — 한국어 우선, 없으면 영어, 없으면 아무 언어"""
    from youtube_transcript_api import YouTubeTranscriptApi

    # 0.6.x 새 API (인스턴스 방식) vs 0.5.x 정적 메서드 자동 감지
    _api = YouTubeTranscriptApi() if callable(getattr(YouTubeTranscriptApi, '__init__', None)) else None

    def _fetch(langs):
        if _api and hasattr(_api, 'fetch'):
            return _api.fetch(video_id, languages=langs)
        return YouTubeTranscriptApi.get_transcript(video_id, languages=langs)

    def _list():
        if _api and hasattr(_api, 'list'):
            return _api.list(video_id)
        return YouTubeTranscriptApi.list_transcripts(video_id)

    try:
        return '한국어', _fetch(['ko'])
    except Exception:
        pass
    try:
        return '영어', _fetch(['en'])
    except Exception:
        pass
    try:
        tl = _list()
        t = next(iter(tl))
        data = t.fetch() if hasattr(t, 'fetch') else list(t)
        # 0.6.x FetchedTranscript → list of dicts
        if hasattr(data, '__iter__') and not isinstance(data, list):
            data = [{'text': s.text, 'start': s.start} for s in data]
        return f'{t.language} (자동생성)', data
    except Exception as e:
        raise RuntimeError(f'자막 없음: {e}')

def transcript_to_markdown(video_id: str, title: str, lang: str, 
                             transcript: list, url: str) -> str:
    """자막 리스트 → 마크다운 변환"""
    lines = [
        f'# {title}',
        f'',
        f'> 출처: https://youtu.be/{video_id}',
        f'> 언어: {lang} | 추출일: {datetime.date.today()}',
        f'',
        f'## 전체 내용',
        f'',
    ]
    
    # 자막을 문단으로 묶기 (30초 단위)
    # 0.6.x는 객체, 0.5.x는 dict — 둘 다 처리
    def _text(e): return (e['text'] if isinstance(e, dict) else e.text).strip()
    def _start(e): return e['start'] if isinstance(e, dict) else e.start

    chunk, chunk_start = [], None
    for entry in transcript:
        if chunk_start is None:
            chunk_start = _start(entry)
        chunk.append(_text(entry))
        if _start(entry) - chunk_start >= 30:
            text = ' '.join(chunk)
            minutes = int(chunk_start // 60)
            seconds = int(chunk_start % 60)
            lines.append(f'**[{minutes:02d}:{seconds:02d}]** {text}')
            lines.append('')
            chunk, chunk_start = [], None
    
    # 남은 내용
    if chunk:
        text = ' '.join(chunk)
        lines.append(text)
    
    return '\n'.join(lines)

def process_video(url_or_id: str, title: str = ''):
    """단일 영상 처리"""
    video_id = get_video_id(url_or_id)
    url = f'https://youtu.be/{video_id}'
    
    print(f'\n[영상] {url}')
    
    # 자막 가져오기
    lang, transcript = fetch_transcript(video_id)
    print(f'  → 자막 언어: {lang} ({len(transcript)}개 세그먼트)')
    
    # 제목이 없으면 video_id 사용
    if not title:
        title = f'워맥_{video_id}'
    
    # 마크다운 변환
    md = transcript_to_markdown(video_id, title, lang, transcript, url)
    
    # 카테고리 분류 및 저장
    cat = categorize(title)
    cat_dir = OUT_KB / cat
    cat_dir.mkdir(parents=True, exist_ok=True)
    
    safe_title = re.sub(r'[^\w가-힣\-_]', '_', title)[:60]
    out_file = cat_dir / f'{safe_title}.md'
    out_file.write_text(md, encoding='utf-8')
    print(f'  → 저장: {out_file.relative_to(BASE)}')
    
    # 원본 텍스트도 source-files/text 에 보관
    OUT_TEXT.mkdir(parents=True, exist_ok=True)
    src_file = OUT_TEXT / f'{safe_title}_원본자막.txt'
    raw = '\n'.join(e['text'] if isinstance(e, dict) else e.text for e in transcript)
    src_file.write_text(raw, encoding='utf-8')
    
    return out_file

def process_playlist_or_list(urls: list[tuple[str, str]]):
    """여러 영상 일괄 처리. urls = [(url, title), ...]"""
    results = []
    for url, title in urls:
        try:
            f = process_video(url, title)
            results.append((url, title, '✓'))
        except Exception as e:
            print(f'  ✗ 오류: {e}')
            results.append((url, title, f'✗ {e}'))
    
    print('\n\n=== 처리 결과 ===')
    for url, title, status in results:
        print(f'  {status}  {title or url}')

# ── 실행 ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print('사용법:')
        print('  단일 영상:  python3 youtube_to_knowledge.py <URL> <제목(선택)>')
        print('  예시:')
        print('  python3 youtube_to_knowledge.py https://youtu.be/xxxx "워맥_영혼몸_1강"')
        print('')
        print('  목록 파일:  python3 youtube_to_knowledge.py --list videos.txt')
        print('  videos.txt 형식: URL<탭>제목 (한 줄에 하나)')
        sys.exit(0)
    
    if sys.argv[1] == '--list':
        # 파일에서 목록 읽기
        list_file = Path(sys.argv[2])
        urls = []
        for line in list_file.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t', 1)
            url = parts[0].strip()
            title = parts[1].strip() if len(parts) > 1 else ''
            urls.append((url, title))
        process_playlist_or_list(urls)
    else:
        url   = sys.argv[1]
        title = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ''
        process_video(url, title)
    
    # 인덱스 업데이트 (extract_to_knowledge.py가 같은 폴더에 있을 때만)
    extract_script = BASE / 'extract_to_knowledge.py'
    if extract_script.exists():
        os.system(f'python3 "{extract_script}"')
