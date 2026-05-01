"""
NotebookLM → 지식 베이스 추출 파이프라인
PPT, PDF, DOCX, TXT, MD → 구조화된 마크다운 변환
"""
import os, sys, re, datetime
from pathlib import Path

BASE = Path('/home/user/-/_workspace/spirituality')
SRC_PPT  = BASE / 'source-files/ppt'
SRC_PDF  = BASE / 'source-files/pdf'
SRC_DOCS = BASE / 'source-files/docs'
SRC_TEXT = BASE / 'source-files/text'
OUT = BASE / 'knowledge-base'
PROCESSED = BASE / 'processed'

# ── PPT 추출 ─────────────────────────────────────────────────────────
def extract_ppt(ppt_path: Path) -> str:
    from pptx import Presentation
    prs = Presentation(str(ppt_path))
    lines = [f'# {ppt_path.stem}\n', f'> 출처: {ppt_path.name} | 추출일: {datetime.date.today()}\n']
    for i, slide in enumerate(prs.slides, 1):
        slide_title = ''
        slide_body = []
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for j, para in enumerate(shape.text_frame.paragraphs):
                text = para.text.strip()
                if not text:
                    continue
                # 첫 텍스트 블록의 첫 줄 = 제목으로 처리
                if not slide_title and j == 0:
                    slide_title = text
                else:
                    level = para.level if para.level else 0
                    prefix = '  ' * level + '- '
                    slide_body.append(f'{prefix}{text}')
        lines.append(f'\n## 슬라이드 {i}: {slide_title or "(제목 없음)"}')
        if slide_body:
            lines.extend(slide_body)
    return '\n'.join(lines)

# ── PDF 추출 ─────────────────────────────────────────────────────────
def extract_pdf(pdf_path: Path) -> str:
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(str(pdf_path))
        lines = [f'# {pdf_path.stem}\n', f'> 출처: {pdf_path.name} | 추출일: {datetime.date.today()}\n']
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ''
            text = re.sub(r'\n{3,}', '\n\n', text.strip())
            if text:
                lines.append(f'\n## {i}페이지\n{text}')
        return '\n'.join(lines)
    except Exception as e:
        return f'# {pdf_path.stem}\n\n> 추출 오류: {e}'

# ── 카테고리 자동 분류 ────────────────────────────────────────────────
CATEGORIES = {
    '영혼몸': 'spirit-soul-body',
    'spirit': 'spirit-soul-body',
    '권세': 'believers-authority',
    'authority': 'believers-authority',
    '은혜': 'grace-faith',
    'grace': 'grace-faith',
    '이미': 'already-got-it',
    'already': 'already-got-it',
    '노력': 'effortless-change',
    'effortless': 'effortless-change',
    '제한': 'dont-limit-god',
    'limit': 'dont-limit-god',
    '안식': 'sabbath',
    'sabbath': 'sabbath',
    '정체성': 'identity',
    'identity': 'identity',
}

def categorize(filename: str) -> str:
    fn_lower = filename.lower()
    for keyword, category in CATEGORIES.items():
        if keyword in fn_lower:
            return category
    return 'general'

# ── 인덱스 업데이트 ───────────────────────────────────────────────────
def update_index(entries: list[dict]):
    index_path = OUT / 'INDEX.md'
    lines = [
        '# 천창성 영성 지식 베이스 INDEX',
        f'> 마지막 업데이트: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        f'> 총 파일 수: {len(entries)}개\n',
        '## 카테고리별 목록\n',
    ]
    by_cat: dict[str, list] = {}
    for e in entries:
        by_cat.setdefault(e['category'], []).append(e)
    
    cat_names = {
        'spirit-soul-body': '영혼몸',
        'believers-authority': '믿는 자의 권세',
        'grace-faith': '은혜와 믿음',
        'already-got-it': '당신은 이미 가졌습니다',
        'effortless-change': '노력없이 오는 변화',
        'dont-limit-god': '하나님을 제한하지 마라',
        'sabbath': '참 안식일',
        'identity': '정체성·자기발견',
        'general': '일반',
    }
    for cat, cat_label in cat_names.items():
        if cat not in by_cat:
            continue
        lines.append(f'### {cat_label}')
        for e in by_cat[cat]:
            lines.append(f'- [{e["title"]}]({e["path"]}) `{e["type"]}` {e["date"]}')
        lines.append('')
    
    index_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  → INDEX 업데이트: {len(entries)}개 항목')

# ── 메인 실행 ─────────────────────────────────────────────────────────
def main():
    entries = []
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PROCESSED, exist_ok=True)

    # 기존 처리된 항목 로드
    for existing in OUT.glob('**/*.md'):
        if existing.name == 'INDEX.md':
            continue

    total_ppt  = list(SRC_PPT.glob('*.pptx'))  + list(SRC_PPT.glob('*.ppt'))
    total_pdf  = list(SRC_PDF.glob('*.pdf'))
    total_docs = list(SRC_DOCS.glob('*.docx')) + list(SRC_DOCS.glob('*.doc'))
    total_text = list(SRC_TEXT.glob('*.txt'))  + list(SRC_TEXT.glob('*.md'))

    if not total_ppt and not total_pdf and not total_docs and not total_text:
        print('⚠  소스 파일이 없습니다.')
        print(f'   PPT  → {SRC_PPT}/')
        print(f'   PDF  → {SRC_PDF}/')
        print(f'   DOCX → {SRC_DOCS}/')
        print(f'   TXT  → {SRC_TEXT}/')
        print('\n데모용 샘플 파일을 생성합니다...')
        _create_demo()
        return

    print(f'처리 시작: PPT {len(total_ppt)}개 | PDF {len(total_pdf)}개 | DOCX {len(total_docs)}개 | TXT {len(total_text)}개\n')

    for ppt_file in total_ppt:
        print(f'[PPT] {ppt_file.name}')
        try:
            content = extract_ppt(ppt_file)
            cat = categorize(ppt_file.stem)
            cat_dir = OUT / cat
            cat_dir.mkdir(exist_ok=True)
            out_file = cat_dir / f'{ppt_file.stem}.md'
            out_file.write_text(content, encoding='utf-8')
            entries.append({
                'title': ppt_file.stem,
                'path': str(out_file.relative_to(OUT)),
                'category': cat,
                'type': 'PPT',
                'date': datetime.date.today().isoformat(),
            })
            print(f'  → 저장: {out_file.relative_to(BASE)}')
        except Exception as e:
            print(f'  ✗ 오류: {e}')

    for pdf_file in total_pdf:
        print(f'[PDF] {pdf_file.name}')
        try:
            content = extract_pdf(pdf_file)
            cat = categorize(pdf_file.stem)
            cat_dir = OUT / cat
            cat_dir.mkdir(exist_ok=True)
            out_file = cat_dir / f'{pdf_file.stem}.md'
            out_file.write_text(content, encoding='utf-8')
            entries.append({
                'title': pdf_file.stem,
                'path': str(out_file.relative_to(OUT)),
                'category': cat,
                'type': 'PDF',
                'date': datetime.date.today().isoformat(),
            })
            print(f'  → 저장: {out_file.relative_to(BASE)}')
        except Exception as e:
            print(f'  ✗ 오류: {e}')

    # DOCX 처리
    for doc_file in total_docs:
        print(f'[DOCX] {doc_file.name}')
        try:
            import docx
            doc = docx.Document(str(doc_file))
            lines = [f'# {doc_file.stem}\n', f'> 출처: {doc_file.name} | 추출일: {datetime.date.today()}\n']
            for para in doc.paragraphs:
                text = para.text.strip()
                if not text:
                    continue
                style = para.style.name.lower()
                if 'heading 1' in style:
                    lines.append(f'\n## {text}')
                elif 'heading 2' in style:
                    lines.append(f'\n### {text}')
                else:
                    lines.append(text)
            content = '\n'.join(lines)
            cat = categorize(doc_file.stem)
            cat_dir = OUT / cat
            cat_dir.mkdir(exist_ok=True)
            out_file = cat_dir / f'{doc_file.stem}.md'
            out_file.write_text(content, encoding='utf-8')
            entries.append({'title': doc_file.stem, 'path': str(out_file.relative_to(OUT)),
                            'category': cat, 'type': 'DOCX', 'date': datetime.date.today().isoformat()})
            print(f'  → 저장: {out_file.relative_to(BASE)}')
        except ImportError:
            print('  ⚠ python-docx 필요: pip install python-docx')
        except Exception as e:
            print(f'  ✗ 오류: {e}')

    # TXT / MD 처리
    for txt_file in total_text:
        print(f'[TXT] {txt_file.name}')
        try:
            raw = txt_file.read_text(encoding='utf-8', errors='ignore')
            header = f'# {txt_file.stem}\n\n> 출처: {txt_file.name} | 추출일: {datetime.date.today()}\n\n'
            content = header + raw
            cat = categorize(txt_file.stem)
            cat_dir = OUT / cat
            cat_dir.mkdir(exist_ok=True)
            out_file = cat_dir / f'{txt_file.stem}.md'
            out_file.write_text(content, encoding='utf-8')
            entries.append({'title': txt_file.stem, 'path': str(out_file.relative_to(OUT)),
                            'category': cat, 'type': 'TXT', 'date': datetime.date.today().isoformat()})
            print(f'  → 저장: {out_file.relative_to(BASE)}')
        except Exception as e:
            print(f'  ✗ 오류: {e}')

    if entries:
        update_index(entries)
    print(f'\n완료. 지식 베이스: {OUT}')

# ── 데모 샘플 생성 ────────────────────────────────────────────────────
def _create_demo():
    """소스 파일이 없을 때 구조 확인용 샘플 생성"""
    from pptx import Presentation
    from pptx.util import Inches, Pt
    
    demo_dir = SRC_PPT
    os.makedirs(demo_dir, exist_ok=True)
    
    prs = Presentation()
    slides_data = [
        ('영혼몸 - 워맥 요약', ['인간은 세 부분으로 구성', '영(Spirit) - 이미 완전', '혼(Soul) - 갱신 중', '몸(Body) - 마지막에 따라옴']),
        ('거듭난 영의 완전성', ['고후 5:17 - 새로운 피조물', '엡 4:24 - 하나님을 따라 창조', '이미 완전한 내 영', '혼이 영을 따라야 한다']),
        ('은혜와 믿음의 관계', ['은혜 = 하나님의 공급', '믿음 = 받는 통로', '행위로 얻는 것이 아님', '엡 2:8-9']),
    ]
    blank_layout = prs.slide_layouts[1]
    for title_text, bullets in slides_data:
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.title.text = title_text
        tf = slide.placeholders[1].text_frame
        for i, bullet in enumerate(bullets):
            if i == 0:
                tf.text = bullet
            else:
                p = tf.add_paragraph()
                p.text = bullet
                p.level = 1
    
    demo_path = demo_dir / '워맥_영혼몸_요약슬라이드_DEMO.pptx'
    prs.save(str(demo_path))
    print(f'  샘플 PPT 생성: {demo_path}')
    
    # 이제 실제로 추출
    content = extract_ppt(demo_path)
    cat_dir = OUT / 'spirit-soul-body'
    cat_dir.mkdir(exist_ok=True)
    out_file = cat_dir / '워맥_영혼몸_요약슬라이드_DEMO.md'
    out_file.write_text(content, encoding='utf-8')
    
    update_index([{
        'title': '워맥_영혼몸_요약슬라이드_DEMO',
        'path': 'spirit-soul-body/워맥_영혼몸_요약슬라이드_DEMO.md',
        'category': 'spirit-soul-body',
        'type': 'PPT(DEMO)',
        'date': datetime.date.today().isoformat(),
    }])
    print(f'  샘플 마크다운 생성: {out_file}')
    print('\n실제 파일을 넣고 다시 실행하세요.')

if __name__ == '__main__':
    main()
