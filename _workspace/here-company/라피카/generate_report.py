import io, os, sys, re, datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, KeepTogether)
from reportlab.platypus import Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── 폰트 ─────────────────────────────────────────────────────────────
FONT = '/tmp/NanumGothic.ttf'
if not os.path.exists(FONT):
    import urllib.request
    urllib.request.urlretrieve(
        'https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf',
        FONT)
pdfmetrics.registerFont(TTFont('KR', FONT))
fm.fontManager.addfont(FONT)
plt.rcParams['font.family'] = fm.FontProperties(fname=FONT).get_name()
plt.rcParams['axes.unicode_minus'] = False

# ── 색상 ─────────────────────────────────────────────────────────────
NAVY   = colors.HexColor('#1F4E79')
BLUE   = colors.HexColor('#2E75B6')
LBLUE  = colors.HexColor('#DEEAF1')
PINK   = colors.HexColor('#F8E7F2')
GREEN  = colors.HexColor('#00B050')
ORANGE = colors.HexColor('#FF8C00')
RED    = colors.HexColor('#C00000')
FUND   = colors.HexColor('#4472C4')
WHITE  = colors.white
LGRAY  = colors.HexColor('#F5F5F5')
GRAY   = colors.HexColor('#888888')

# ── 스타일 ────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, fontName='KR', **kw)

ST = {
    'h1':  S('h1',  fontSize=22, textColor=WHITE,  spaceAfter=2, leading=28, alignment=1),
    'h2':  S('h2',  fontSize=14, textColor=NAVY,   spaceAfter=6, leading=20, spaceBefore=4),
    'h3':  S('h3',  fontSize=11, textColor=NAVY,   spaceAfter=4, leading=16),
    'bd':  S('bd',  fontSize=9,  textColor=colors.black, leading=14),
    'sm':  S('sm',  fontSize=8,  textColor=GRAY,   leading=12),
    'ctr': S('ctr', fontSize=9,  textColor=colors.black, leading=13, alignment=1),
    'lk':  S('lk',  fontSize=8,  textColor=BLUE,   leading=12, alignment=1),
    'sub': S('sub', fontSize=10, textColor=WHITE,  leading=14, alignment=1),
    'tag': S('tag', fontSize=8,  textColor=WHITE,  leading=12, alignment=1),
    'fnc': S('fnc', fontSize=7,  textColor=GRAY,   leading=11, alignment=1),
    'wht': S('wht', fontSize=9,  textColor=WHITE,  leading=13),
    'whtb':S('whtb',fontSize=11, textColor=WHITE,  leading=16, alignment=1),
    'blk': S('blk', fontSize=9,  textColor=colors.black, leading=13, alignment=1),
}

W, H = A4
M = 18*mm

# ── 기업 및 프로그램 데이터 ───────────────────────────────────────────
COMPANY = '(주)라피카'
DATE_STR = '2026-05-01'
TODAY = '20260501'

PROFILE = [
    ('기업명', '(주)라피카'),
    ('업종', '화장품 제조·도소매'),
    ('규모', '소기업 / 직원 2명'),
    ('연매출', '3억 원'),
    ('업력', '설립 2022년 (4년차)'),
    ('소재지', '서울 강남구'),
    ('수혜 이력', '없음 (정부지원 첫 신청)'),
    ('희망 분야', '자금 / 수출 / R&D / 마케팅'),
]

PROGRAMS = [
    {
        'rank': 1,
        'name': '서울뷰티허브\nK-뷰티 지원사업',
        'org': '서울시 / 서울산업진흥원',
        'deadline': '상시 (2026년 하반기 모집 예정)',
        'budget': '선정 기업당 최대 500만원\n(컨설팅·수출·마케팅 바우처)',
        'fit': '상',
        'summary': '뷰티 전문 지원공간, 수출·마케팅·판로 원스톱 지원. 100곳 모집. 4년차 뷰티 창업기업에 최적.',
        'link': 'https://www.bizinfo.go.kr',
        'est': '500만원 (바우처)',
    },
    {
        'rank': 2,
        'name': 'K-뷰티 수출 컨소시엄\n활성화 지원사업',
        'org': '중소벤처기업부 / 중진공',
        'deadline': '2026년 상반기 공고 예정',
        'budget': '수출 마케팅비 최대 70% 지원\n(1,000만~5,000만원)',
        'fit': '상',
        'summary': '화장품 중소기업 수출 그룹화 지원. 해외 바이어 매칭, 전시회 참가, 수출 마케팅비 보조.',
        'link': 'https://www.kosmes.or.kr',
        'est': '2,000만원 (평균 선정액)',
    },
    {
        'rank': 3,
        'name': '중소기업\n마케팅지원사업(판판대로)',
        'org': '중소벤처기업부 / 중진공',
        'deadline': '연중 상시 신청',
        'budget': '기업당 최대 1,000만원\n(판로개척 마케팅비 50% 보조)',
        'fit': '상',
        'summary': '국내외 판로 개척 마케팅 비용 지원. 총 141.7억 예산. 소기업·초기기업 우대, 서류 간소.',
        'link': 'https://www.bizinfo.go.kr',
        'est': '500~1,000만원 (50% 보조)',
    },
    {
        'rank': 4,
        'name': '초기창업패키지\n(창업도약패키지)',
        'org': '중소벤처기업부 / 창업진흥원',
        'deadline': '2026년 하반기 2차 공고 예정',
        'budget': '기업당 최대 1억원\n(사업화 자금 + 멘토링)',
        'fit': '중',
        'summary': '창업 3~7년차 기업 대상. 4년차 라피카 지원 가능. 화장품·K-뷰티 분야 심사 경쟁력 있음.',
        'link': 'https://www.k-startup.go.kr',
        'est': '3,000만~5,000만원 (평균 선정액)',
    },
    {
        'rank': 5,
        'name': 'K-뷰티 시장대응형\n기술혁신개발사업',
        'org': '중소벤처기업부 / TIPA',
        'deadline': '2026년 하반기 공고 예정',
        'budget': '과제당 최대 5억원 / 2년\n(65~75% 정부 지원)',
        'fit': '중',
        'summary': '화장품 기술혁신 R&D 전용. 성분 개발·기능성 인증 연계. 직원 2명 소규모 가능하나 외부 연구인력 활용 권장.',
        'link': 'https://www.tipa.or.kr',
        'est': '1억~1.5억원 (과제 규모 따라)',
    },
]

FUND_ITEMS = [
    ('기보 (이용 중 2억)', '추가 한도 검토 가능 여부 확인 필요', ORANGE),
    ('중진공 K-뷰티론', '미이용 → 신규 신청 가능 (화장품 특화 저리 융자)', GREEN),
    ('신보 (미이용)', '신규 신청 가능 → 자금 에이전트 설계 권장', GREEN),
]

TOTAL_EST = '약 5,000만~1억 5,000만원 (비융자 선정 기준 보수적 추정)'

# ── 버블차트 ──────────────────────────────────────────────────────────
def make_bubble():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor('#DEEAF1')
    ax.set_facecolor('#F0F6FC')
    data = [
        ('서울뷰티허브', 2, 8, 200, '#00B050'),
        ('K-뷰티수출컨소시엄', 3, 7.5, 500, '#00B050'),
        ('마케팅지원(판판대로)', 2, 7, 300, '#00B050'),
        ('창업도약패키지', 5, 6.5, 1000, '#FF8C00'),
        ('K-뷰티기술혁신R&D', 7, 8.5, 2000, '#FF8C00'),
    ]
    for name, x, y, s, c in data:
        ax.scatter(x, y, s=s, c=c, alpha=0.75, edgecolors='white', linewidths=1.5)
        ax.annotate(name, (x, y), textcoords='offset points', xytext=(0, 10),
                    ha='center', fontsize=7.5, color='#1F4E79',
                    fontproperties=fm.FontProperties(fname=FONT))
    ax.set_xlim(0, 10); ax.set_ylim(4, 11)
    ax.set_xlabel('신청 난이도 →', fontsize=9, color='#1F4E79',
                  fontproperties=fm.FontProperties(fname=FONT))
    ax.set_ylabel('기대 효과 →', fontsize=9, color='#1F4E79',
                  fontproperties=fm.FontProperties(fname=FONT))
    ax.set_title('우선순위 매트릭스 (버블 크기 = 지원 규모)', fontsize=10, color='#1F4E79',
                 fontproperties=fm.FontProperties(fname=FONT))
    ax.axvline(5, color='#aaa', linestyle='--', linewidth=0.8)
    ax.axhline(7, color='#aaa', linestyle='--', linewidth=0.8)
    ax.tick_params(labelsize=8)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontproperties(fm.FontProperties(fname=FONT))
    patches = [mpatches.Patch(color='#00B050', label='적합도 상'),
               mpatches.Patch(color='#FF8C00', label='적합도 중')]
    ax.legend(handles=patches, fontsize=8, loc='lower right',
              prop=fm.FontProperties(fname=FONT))
    fig.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=130, bbox_inches='tight')
    buf.seek(0); plt.close(fig)
    return buf

# ── 간트차트 ──────────────────────────────────────────────────────────
def make_gantt():
    fig, ax = plt.subplots(figsize=(7, 3.2))
    fig.patch.set_facecolor('#DEEAF1')
    ax.set_facecolor('#F0F6FC')
    tasks = [
        ('서울뷰티허브 신청', 5, 1, '#00B050'),
        ('마케팅지원(판판대로) 신청', 5, 1, '#00B050'),
        ('K-뷰티수출컨소시엄 준비', 5, 2, '#2E75B6'),
        ('창업도약패키지 준비', 7, 2, '#FF8C00'),
        ('K-뷰티기술혁신R&D 준비', 8, 3, '#FF8C00'),
    ]
    months = ['5월','6월','7월','8월','9월','10월','11월','12월']
    colors_list = ['#00B050','#00B050','#2E75B6','#FF8C00','#FF8C00']
    for i, (name, start, dur, c) in enumerate(tasks):
        ax.barh(i, dur, left=start-5, color=c, alpha=0.8, edgecolor='white', height=0.6)
        ax.text(start-5 + dur/2, i, name, ha='center', va='center',
                fontsize=7.5, color='white',
                fontproperties=fm.FontProperties(fname=FONT))
    ax.set_xlim(0, 8); ax.set_ylim(-0.5, len(tasks)-0.5)
    ax.set_xticks(range(8)); ax.set_xticklabels(months, fontsize=8)
    ax.set_yticks([]); ax.invert_yaxis()
    ax.set_title('신청 타임라인 (2026년)', fontsize=10, color='#1F4E79',
                 fontproperties=fm.FontProperties(fname=FONT))
    for lbl in ax.get_xticklabels():
        lbl.set_fontproperties(fm.FontProperties(fname=FONT))
    fig.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=130, bbox_inches='tight')
    buf.seek(0); plt.close(fig)
    return buf

# ── PDF 생성 ──────────────────────────────────────────────────────────
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUT_DIR, f'라피카_정부지원사업리포트_{TODAY}.pdf')

doc = SimpleDocTemplate(PDF_PATH, pagesize=A4,
                        leftMargin=M, rightMargin=M,
                        topMargin=14*mm, bottomMargin=14*mm)
story = []
CW = W - 2*M

# ── 1. 표지 ───────────────────────────────────────────────────────────
cover_data = [[Paragraph('히어컴퍼니 기업컨설팅', ST['sub'])],
              [Paragraph('정부지원사업 맞춤 리포트', ST['h1'])],
              [Spacer(1, 4*mm)],
              [Paragraph(COMPANY, S('co', fontSize=18, textColor=colors.HexColor('#BDD7EE'), leading=24, alignment=1))],
              [Spacer(1, 3*mm)],
              [Paragraph(f'작성일: {DATE_STR}  |  담당: 히어컴퍼니 정부지원사업 에이전트', ST['fnc'])]]
cover = Table([cover_data], colWidths=[CW])
cover.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), NAVY),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ('ROUNDEDCORNERS', [6]),
]))
story.append(cover)
story.append(Spacer(1, 6*mm))

# ── 2. 기업 프로파일 ──────────────────────────────────────────────────
story.append(Paragraph('■ 기업 프로파일', ST['h2']))
prof_rows = [[Paragraph(k, ST['bd']), Paragraph(v, ST['bd'])] for k, v in PROFILE]
prof_tbl = Table(prof_rows, colWidths=[40*mm, CW-40*mm])
prof_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,-1), LBLUE),
    ('BACKGROUND', (1,0), (1,-1), WHITE),
    ('ROWBACKGROUNDS', (1,0), (1,-1), [WHITE, LGRAY]),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(prof_tbl)
story.append(Spacer(1, 6*mm))

# ── 3. 비융자 추천 Top 5 ──────────────────────────────────────────────
story.append(Paragraph('■ 비융자 추천 지원사업 Top 5', ST['h2']))
story.append(Paragraph('* 비융자(보조금·바우처·R&D 과제) 중심으로 선별 — 정책자금·보증은 하단 자금 에이전트 이관 박스 참조', ST['sm']))
story.append(Spacer(1, 3*mm))

FIT_COLOR = {'상': GREEN, '중': ORANGE, '하': RED}
for p in PROGRAMS:
    fc = FIT_COLOR.get(p['fit'], GRAY)
    fit_badge = Table([[Paragraph(f"적합도 {p['fit']}", ST['tag'])]], colWidths=[22*mm])
    fit_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), fc),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROUNDEDCORNERS', [4]),
    ]))
    rank_cell = Paragraph(f'<b>0{p["rank"]}</b>', S('rk', fontSize=18, textColor=NAVY, leading=24, alignment=1))
    name_cell = Paragraph(f'<b>{p["name"]}</b><br/><font size="8" color="#555555">{p["org"]}</font>', ST['bd'])
    budget_cell = Paragraph(p['budget'], ST['ctr'])
    link_cell = Paragraph(f'<link href="{p["link"]}">공고 바로가기 &gt;</link>', ST['lk'])

    main_row = [[rank_cell, name_cell, budget_cell, fit_badge]]
    main_tbl = Table(main_row, colWidths=[14*mm, CW-14*mm-38*mm-26*mm, 38*mm, 26*mm])
    main_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LBLUE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#BBCCDD')),
    ]))

    desc_row = [[Paragraph('마감', ST['sm']), Paragraph(p['deadline'], ST['bd']),
                 Paragraph('요약', ST['sm']), Paragraph(p['summary'], ST['bd'])]]
    desc_tbl = Table(desc_row, colWidths=[12*mm, 55*mm, 12*mm, CW-12*mm-55*mm-12*mm])
    desc_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BACKGROUND', (0,0), (0,0), LGRAY),
        ('BACKGROUND', (2,0), (2,0), LGRAY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#DDDDDD')),
    ]))

    link_row = [[Paragraph('', ST['sm']), link_cell]]
    link_tbl = Table(link_row, colWidths=[14*mm, CW-14*mm])
    link_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LGRAY),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))

    story.append(KeepTogether([main_tbl, desc_tbl, link_tbl, Spacer(1, 3*mm)]))

story.append(Spacer(1, 4*mm))

# ── 4. 매칭 현황표 ────────────────────────────────────────────────────
story.append(Paragraph('■ 매칭 현황표', ST['h2']))
hdr = [Paragraph(t, ST['wht']) for t in ['순위', '사업명', '주관기관', '마감일', '지원규모', '적합도']]
tbl_data = [hdr]
for p in PROGRAMS:
    fc = FIT_COLOR.get(p['fit'], GRAY)
    tbl_data.append([
        Paragraph(f'0{p["rank"]}', ST['ctr']),
        Paragraph(p['name'].replace('\n', ' '), ST['bd']),
        Paragraph(p['org'], ST['sm']),
        Paragraph(p['deadline'].split('(')[0].strip(), ST['sm']),
        Paragraph(p['budget'].replace('\n', ' '), ST['sm']),
        Table([[Paragraph(p['fit'], ST['tag'])]], colWidths=[12*mm],
              style=[('BACKGROUND',(0,0),(-1,-1),fc),
                     ('ALIGN',(0,0),(-1,-1),'CENTER'),
                     ('TOPPADDING',(0,0),(-1,-1),2),
                     ('BOTTOMPADDING',(0,0),(-1,-1),2)]),
    ])
match_tbl = Table(tbl_data, colWidths=[13*mm, 45*mm, 35*mm, 30*mm, 40*mm, 16*mm])
ts = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
])
match_tbl.setStyle(ts)
story.append(match_tbl)
story.append(Spacer(1, 6*mm))

# ── 5. 예상 수혜금액 ──────────────────────────────────────────────────
story.append(Paragraph('■ 예상 총 수혜금액 (보수적 추정)', ST['h2']))
est_data = [
    [Paragraph('사업명', ST['wht']), Paragraph('예상 수혜액 (보수적)', ST['wht']), Paragraph('비고', ST['wht'])],
]
for p in PROGRAMS:
    est_data.append([
        Paragraph(p['name'].replace('\n', ' '), ST['bd']),
        Paragraph(p['est'], ST['bd']),
        Paragraph('비융자 (보조금·바우처·R&D)', ST['sm']),
    ])
est_data.append([
    Paragraph('합계 (보수적 시나리오)', S('tot', fontSize=9, textColor=NAVY, leading=13)),
    Paragraph(TOTAL_EST, S('tot2', fontSize=9, textColor=RED, leading=13)),
    Paragraph('중복 신청 가능 항목 합산', ST['sm']),
])
est_tbl = Table(est_data, colWidths=[60*mm, 70*mm, CW-130*mm])
est_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('BACKGROUND', (0,-1), (-1,-1), LBLUE),
    ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, LGRAY]),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(est_tbl)
story.append(Spacer(1, 6*mm))

# ── 6. 버블차트 ───────────────────────────────────────────────────────
story.append(Paragraph('■ 우선순위 매트릭스', ST['h2']))
story.append(RLImage(make_bubble(), width=170*mm, height=82*mm))
story.append(Spacer(1, 4*mm))

# ── 7. 간트차트 ───────────────────────────────────────────────────────
story.append(Paragraph('■ 신청 타임라인', ST['h2']))
story.append(RLImage(make_gantt(), width=170*mm, height=78*mm))
story.append(Spacer(1, 6*mm))

# ── 8. 자금 에이전트 이관 박스 ────────────────────────────────────────
story.append(Paragraph('■ 자금 에이전트 이관 항목 (정책자금·보증)', ST['h2']))
story.append(Paragraph('* 아래 항목은 융자·보증 성격으로 자금 에이전트가 별도 설계합니다.', ST['sm']))
story.append(Spacer(1, 2*mm))
fund_hdr = [[Paragraph(t, ST['wht']) for t in ['구분', '현황', '비고']]]
fund_rows = [[Paragraph(name, ST['bd']), Paragraph(memo, ST['bd']),
              Table([[Paragraph('이관' if c==ORANGE else '신규가능', ST['tag'])]], colWidths=[18*mm],
                    style=[('BACKGROUND',(0,0),(-1,-1),c),
                           ('ALIGN',(0,0),(-1,-1),'CENTER'),
                           ('TOPPADDING',(0,0),(-1,-1),2),
                           ('BOTTOMPADDING',(0,0),(-1,-1),2)])]
             for name, memo, c in FUND_ITEMS]
fund_tbl = Table(fund_hdr + fund_rows, colWidths=[50*mm, CW-50*mm-22*mm, 22*mm])
fund_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), FUND),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(fund_tbl)
story.append(Spacer(1, 6*mm))

# ── 9. 제안서 초안 ────────────────────────────────────────────────────
story.append(Paragraph('■ Top 1 제안서 초안: 서울뷰티허브 K-뷰티 지원사업', ST['h2']))
proposal_items = [
    ('사업 개요', '서울산업진흥원이 운영하는 K-뷰티 전문 지원공간으로, 화장품 기업에 수출·마케팅·판로 개척 원스톱 지원 서비스를 제공합니다. 2026년 100개 기업 모집 예정.'),
    ('신청 요건', '① 서울시 소재 화장품 제조·도소매 기업\n② 중소기업기본법 상 소기업 해당\n③ 수출 또는 마케팅 계획 보유\n④ 사업자등록증 및 최근 재무제표'),
    ('사업 필요성',
     '(주)라피카는 2022년 설립 이후 4년간 화장품 제조·도소매 역량을 축적해 왔습니다. '
     'K-뷰티에 대한 글로벌 관심이 최고조에 달한 현재, 해외 바이어 발굴과 수출 인프라 구축이 '
     '성장의 핵심 과제입니다. 서울뷰티허브는 수출·마케팅·판로를 한 곳에서 지원하는 최적의 '
     '플랫폼으로, 초기 수출 비용 부담 없이 글로벌 시장 진입을 가속화할 수 있습니다.'),
    ('추진 계획',
     '1단계 (선정 후 1~2개월): 영문 제품 카탈로그 및 온라인 쇼룸 제작, 수출 타겟 시장 선정 (동남아·일본·중동 우선)\n'
     '2단계 (3~5개월): K-뷰티 수출 컨소시엄 참여, 해외 B2B 박람회 참가 (서비스 바우처 활용)\n'
     '3단계 (6개월~): 첫 수출 계약 성사, 2027년 수출바우처 자동 자격 확보'),
    ('기대 효과',
     '• 1년 내 수출 거래처 2~3곳 발굴 목표\n'
     '• 수출 매출 5,000만원 이상 달성 목표\n'
     '• 수출 실적 기반으로 2027년 이노비즈·벤처 인증 연계\n'
     '• K-뷰티 글로벌 브랜딩 강화로 국내 매출 병행 성장'),
]
for title, body in proposal_items:
    story.append(Paragraph(f'▸ {title}', ST['h3']))
    story.append(Paragraph(body, ST['bd']))
    story.append(Spacer(1, 3*mm))

# ── 꼬리말 ────────────────────────────────────────────────────────────
story.append(HRFlowable(width=CW, thickness=0.5, color=GRAY))
story.append(Spacer(1, 2*mm))
story.append(Paragraph(
    f'본 리포트는 히어컴퍼니 정부지원사업 에이전트가 {DATE_STR} 기준 공개된 공고 정보를 바탕으로 작성하였습니다. '
    '실제 신청 전 최신 공고문을 반드시 재확인하시기 바랍니다.',
    ST['sm']))

doc.build(story)
print(f'PDF 생성 완료: {PDF_PATH}')
