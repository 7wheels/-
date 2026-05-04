#!/usr/bin/env python3
"""(주)오드린 정부지원사업 PDF 인포그래픽 리포트 생성"""
import os, io, sys, subprocess, urllib.request
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image as RLImage, PageBreak, Frame,
                                KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import matplotlib.patches as mpatches

# ---------- 한국어 폰트 등록 ----------
FONT_PATH = '/tmp/NanumGothic.ttf'
FONT_BOLD_PATH = '/tmp/NanumGothicBold.ttf'

def ensure_font():
    if not os.path.exists(FONT_PATH):
        urllib.request.urlretrieve(
            'https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf',
            FONT_PATH)
    if not os.path.exists(FONT_BOLD_PATH):
        urllib.request.urlretrieve(
            'https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf',
            FONT_BOLD_PATH)

ensure_font()
pdfmetrics.registerFont(TTFont('KR', FONT_PATH))
pdfmetrics.registerFont(TTFont('KRB', FONT_BOLD_PATH))

# matplotlib 한글
fm.fontManager.addfont(FONT_PATH)
fm.fontManager.addfont(FONT_BOLD_PATH)
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# ---------- 브랜드 컬러 ----------
NAVY = HexColor('#1F4E79')
BLUE = HexColor('#2E75B6')
LIGHTBLUE = HexColor('#DEEAF1')
GREEN = HexColor('#00B050')
ORANGE = HexColor('#FF8C00')
RED = HexColor('#C00000')
GRAY = HexColor('#595959')
LIGHTGRAY = HexColor('#F2F2F2')

# ---------- 데이터 ----------
COMPANY = '(주)오드린'
TODAY = '2026-05-03'

ANNOUNCEMENTS = [
    {
        'title': '농식품 글로벌 성장패키지 지원사업',
        'agency': 'aT 한국농수산식품유통공사',
        'deadline': '2026-06-15',
        'budget': '기업당 최대 1,200만원',
        'support': '수출 마케팅, 바이어 매칭, 물류',
        'fit': '상',
        'category': 'gov',
        'difficulty': 2.0,
        'effect': 4.5,
        'amount': 12,
    },
    {
        'title': '농식품 현지화지원사업 (수입등록·검사)',
        'agency': 'aT / 농림축산식품부',
        'deadline': '2026-05-30',
        'budget': '품목당 최대 500만원',
        'support': '해외 수입등록·검사 비용',
        'fit': '상',
        'category': 'gov',
        'difficulty': 1.5,
        'effect': 3.5,
        'amount': 5,
    },
    {
        'title': '2026년 중소기업 기술개발 지원사업 (식품)',
        'agency': '중소벤처기업부 / TIPA',
        'deadline': '2026-06-30',
        'budget': '최대 2억원 (2년)',
        'support': '과실주 품질 향상·신제품 R&D',
        'fit': '상',
        'category': 'gov',
        'difficulty': 4.0,
        'effect': 5.0,
        'amount': 200,
    },
    {
        'title': '2026 부처협업형 스마트공장 구축 지원사업 (식품)',
        'agency': '중기부 / 식약처 / 스마트제조혁신추진단',
        'deadline': '2026-07-15 (2차)',
        'budget': '최대 2억원 (총 25억 한도)',
        'support': '와인 생산공정 자동화·HACCP 연계',
        'fit': '상',
        'category': 'gov',
        'difficulty': 3.5,
        'effect': 4.5,
        'amount': 200,
    },
    {
        'title': '식품융합클러스터 조성 시범사업',
        'agency': '농림축산식품부',
        'deadline': '2026-06-20',
        'budget': '컨소시엄 단위 최대 10억원',
        'support': '지역 식품기업 협업 R&D·판로',
        'fit': '중',
        'category': 'gov',
        'difficulty': 4.0,
        'effect': 4.0,
        'amount': 80,
    },
    {
        'title': '우수문화상품 지정제 활성화 사업 (식품)',
        'agency': '문화체육관광부 / 한국공예디자인문화진흥원',
        'deadline': '2026-05-25',
        'budget': '브랜딩·마케팅 패키지',
        'support': '전통주·과실주 K-브랜딩',
        'fit': '중',
        'category': 'gov',
        'difficulty': 2.0,
        'effect': 3.0,
        'amount': 30,
    },
    {
        'title': '벤처기업 확인 / 이노비즈 인증',
        'agency': '벤처기업협회 / 이노비즈협회',
        'deadline': '상시',
        'budget': '세제·금융·공공조달 가점',
        'support': '취득세 75% 감면, 정책자금 우대',
        'fit': '상',
        'category': 'cert',
        'difficulty': 2.5,
        'effect': 3.5,
        'amount': 20,
    },
    {
        'title': '수출지원기반활용사업 (수출바우처)',
        'agency': 'KOTRA / 중소벤처기업부',
        'deadline': '2026-05-31',
        'budget': '최대 8,000만원 바우처',
        'support': '해외 마케팅·인증·통번역',
        'fit': '상',
        'category': 'gov',
        'difficulty': 2.5,
        'effect': 4.0,
        'amount': 80,
    },
]

OUTPUT_DIR = '/home/user/-/_workspace/here-company/오드린'
OUT_PDF = os.path.join(OUTPUT_DIR, f'{COMPANY}_정부지원사업리포트_{datetime.now().strftime("%Y%m%d")}.pdf')

# ---------- 스타일 ----------
styles = getSampleStyleSheet()
def st(name, **kw):
    base = dict(fontName='KR', fontSize=10, leading=14, textColor=black)
    base.update(kw)
    return ParagraphStyle(name, **base)

S_TITLE = st('title', fontName='KRB', fontSize=28, textColor=white, alignment=TA_CENTER, leading=34)
S_SUB = st('sub', fontName='KR', fontSize=14, textColor=white, alignment=TA_CENTER)
S_H1 = st('h1', fontName='KRB', fontSize=18, textColor=NAVY, leading=24, spaceBefore=8, spaceAfter=8)
S_H2 = st('h2', fontName='KRB', fontSize=13, textColor=NAVY, leading=18, spaceBefore=6, spaceAfter=4)
S_BODY = st('body', fontName='KR', fontSize=10, leading=15)
S_SMALL = st('small', fontName='KR', fontSize=8, leading=11, textColor=GRAY)
S_CARD_T = st('cardt', fontName='KRB', fontSize=12, textColor=white, leading=15)
S_CARD_B = st('cardb', fontName='KR', fontSize=9, textColor=white, leading=12)
S_FOOT = st('foot', fontName='KR', fontSize=8, textColor=GRAY, alignment=TA_CENTER)

# ---------- 색상 매핑 ----------
def fit_color(fit):
    return {'상': GREEN, '중': ORANGE, '하': RED}.get(fit, GRAY)

# ---------- 페이지 데코레이터 ----------
def page_decor(canv, doc):
    canv.saveState()
    # 상단 띠
    canv.setFillColor(NAVY)
    canv.rect(0, A4[1]-15*mm, A4[0], 15*mm, fill=1, stroke=0)
    canv.setFillColor(white)
    canv.setFont('KRB', 10)
    canv.drawString(15*mm, A4[1]-10*mm, f'{COMPANY} 정부지원사업 리포트')
    canv.drawRightString(A4[0]-15*mm, A4[1]-10*mm, 'HERE COMPANY 기업컨설팅')
    # 하단
    canv.setFillColor(GRAY)
    canv.setFont('KR', 8)
    canv.drawCentredString(A4[0]/2, 8*mm,
        f'© 2026 히어컴퍼니(HERE COMPANY)  |  발행일 {TODAY}  |  Page {doc.page}')
    canv.restoreState()

def cover_page(canv, doc):
    canv.saveState()
    # 풀 네이비
    canv.setFillColor(NAVY)
    canv.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # 액센트 바
    canv.setFillColor(BLUE)
    canv.rect(0, A4[1]/2 - 5*mm, A4[0], 1*mm, fill=1, stroke=0)
    # 브랜드
    canv.setFillColor(white)
    canv.setFont('KRB', 14)
    canv.drawCentredString(A4[0]/2, A4[1]-30*mm, 'HERE COMPANY')
    canv.setFont('KR', 10)
    canv.drawCentredString(A4[0]/2, A4[1]-37*mm, '기업컨설팅 · Government Funding Intelligence')
    # 메인 타이틀
    canv.setFont('KRB', 32)
    canv.drawCentredString(A4[0]/2, A4[1]/2 + 25*mm, COMPANY)
    canv.setFont('KRB', 22)
    canv.drawCentredString(A4[0]/2, A4[1]/2 + 12*mm, '정부지원사업 매칭 리포트')
    canv.setFont('KR', 12)
    canv.setFillColor(LIGHTBLUE)
    canv.drawCentredString(A4[0]/2, A4[1]/2 - 15*mm,
        '와인 제조업 (KSIC C11012 · 과실주 제조업)')
    canv.drawCentredString(A4[0]/2, A4[1]/2 - 22*mm,
        '실시간 공고 검색 · 우선순위 매트릭스 · 신청 전략')
    # 날짜
    canv.setFillColor(white)
    canv.setFont('KRB', 14)
    canv.drawCentredString(A4[0]/2, 40*mm, TODAY)
    canv.setFont('KR', 9)
    canv.setFillColor(LIGHTBLUE)
    canv.drawCentredString(A4[0]/2, 32*mm, 'Confidential · For (주)오드린 Internal Use')
    canv.restoreState()

# ---------- 차트 생성 ----------
def chart_priority_matrix():
    fig, ax = plt.subplots(figsize=(9, 5.2))
    colors = {'상': '#00B050', '중': '#FF8C00', '하': '#C00000'}
    for a in ANNOUNCEMENTS:
        ax.scatter(a['difficulty'], a['effect'],
                   s=a['amount']*15 + 100,
                   c=colors[a['fit']], alpha=0.65,
                   edgecolors='#1F4E79', linewidths=1.5)
        # 짧은 라벨
        label = a['title'][:14] + ('…' if len(a['title']) > 14 else '')
        ax.annotate(label, (a['difficulty'], a['effect']),
                    xytext=(7, 7), textcoords='offset points',
                    fontsize=8, color='#1F4E79')
    ax.set_xlabel('신청 난이도 →', fontsize=11, color='#1F4E79', fontweight='bold')
    ax.set_ylabel('기대 효과 →', fontsize=11, color='#1F4E79', fontweight='bold')
    ax.set_title('우선순위 매트릭스 (버블 크기 = 지원 규모)',
                 fontsize=13, color='#1F4E79', fontweight='bold', pad=12)
    ax.set_xlim(0, 5.5); ax.set_ylim(0, 5.8)
    ax.axhline(3, color='#CCCCCC', ls='--', lw=0.8)
    ax.axvline(3, color='#CCCCCC', ls='--', lw=0.8)
    ax.text(0.3, 5.5, 'Quick Win', fontsize=10, color='#00B050', fontweight='bold')
    ax.text(4.0, 5.5, '전략 과제', fontsize=10, color='#FF8C00', fontweight='bold')
    ax.grid(True, alpha=0.25)
    # 범례
    handles = [mpatches.Patch(color=c, label=f'적합도 {k}') for k,c in colors.items()]
    ax.legend(handles=handles, loc='lower right', fontsize=9)
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def chart_timeline():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    items = [a for a in ANNOUNCEMENTS if a['deadline'] != '상시']
    items = sorted(items, key=lambda x: x['deadline'])
    today = datetime.strptime(TODAY, '%Y-%m-%d')
    colors = {'상': '#00B050', '중': '#FF8C00', '하': '#C00000'}
    y_labels = []
    for i, a in enumerate(items):
        # 마감일 파싱 (괄호 정보 제거)
        d_raw = a['deadline'].split(' ')[0]
        d = datetime.strptime(d_raw, '%Y-%m-%d')
        days_left = (d - today).days
        ax.barh(i, days_left, left=0, color=colors[a['fit']],
                alpha=0.75, edgecolor='#1F4E79', height=0.55)
        ax.text(days_left + 1, i, f'  D-{days_left}  ({d_raw})',
                va='center', fontsize=9, color='#1F4E79')
        y_labels.append(a['title'][:30] + ('…' if len(a['title']) > 30 else ''))
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels(y_labels, fontsize=9)
    ax.set_xlabel('신청 가능 일수 (오늘 기준)', fontsize=11, color='#1F4E79', fontweight='bold')
    ax.set_title('신청 타임라인 (마감 임박 순)',
                 fontsize=13, color='#1F4E79', fontweight='bold', pad=12)
    ax.invert_yaxis()
    ax.grid(True, axis='x', alpha=0.25)
    ax.set_xlim(0, max([(datetime.strptime(a['deadline'].split(' ')[0],'%Y-%m-%d')-today).days for a in items]) + 25)
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

# ---------- 카드 빌더 ----------
def top3_cards():
    """추천 Top 3 프로그램 카드 (3열 테이블)"""
    top3 = [a for a in ANNOUNCEMENTS if a['fit'] == '상'][:3]
    cells = []
    for a in top3:
        c = fit_color(a['fit'])
        inner = [
            [Paragraph(f"<b>적합도 {a['fit']}</b>", S_CARD_B)],
            [Paragraph(a['title'], S_CARD_T)],
            [Paragraph(f"<b>주관:</b> {a['agency']}", S_CARD_B)],
            [Paragraph(f"<b>마감:</b> {a['deadline']}", S_CARD_B)],
            [Paragraph(f"<b>규모:</b> {a['budget']}", S_CARD_B)],
        ]
        t = Table(inner, colWidths=[55*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        cells.append(t)
    while len(cells) < 3:
        cells.append('')
    outer = Table([cells], colWidths=[60*mm]*3)
    outer.setStyle(TableStyle([
        ('LEFTPADDING',(0,0),(-1,-1),2),
        ('RIGHTPADDING',(0,0),(-1,-1),2),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    return outer

def profile_block():
    rows = [
        ['업종', '와인 제조업 (과실주, KSIC C11012)'],
        ['주요 사업', '와인 제조 및 판매'],
        ['규모', '중소기업'],
        ['업력 / 단계', '성장기 (와이너리 운영)'],
        ['핵심 키워드', '과실주 · 우리술 · 프리미엄 · K-와인 수출'],
        ['추천 트랙', '농식품 R&D · 수출 · 스마트공장 · 인증'],
    ]
    t = Table(rows, colWidths=[35*mm, 135*mm])
    t.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'KR',10),
        ('FONT',(0,0),(0,-1),'KRB',10),
        ('BACKGROUND',(0,0),(0,-1),LIGHTBLUE),
        ('TEXTCOLOR',(0,0),(0,-1),NAVY),
        ('GRID',(0,0),(-1,-1),0.4,HexColor('#BFBFBF')),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
    ]))
    return t

def matching_table():
    header = ['공고명', '주관', '마감일', '지원규모', '적합도']
    data = [header]
    for a in ANNOUNCEMENTS:
        data.append([
            Paragraph(a['title'], S_BODY),
            Paragraph(a['agency'], S_SMALL),
            a['deadline'],
            Paragraph(a['budget'], S_SMALL),
            a['fit'],
        ])
    t = Table(data, colWidths=[55*mm, 38*mm, 25*mm, 35*mm, 12*mm], repeatRows=1)
    style = TableStyle([
        ('FONT',(0,0),(-1,0),'KRB',10),
        ('FONT',(0,1),(-1,-1),'KR',9),
        ('BACKGROUND',(0,0),(-1,0),NAVY),
        ('TEXTCOLOR',(0,0),(-1,0),white),
        ('ALIGN',(2,0),(2,-1),'CENTER'),
        ('ALIGN',(4,0),(4,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('GRID',(0,0),(-1,-1),0.3,HexColor('#BFBFBF')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white, LIGHTGRAY]),
        ('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ])
    # 적합도 색상
    for i, a in enumerate(ANNOUNCEMENTS, start=1):
        style.add('BACKGROUND', (4,i), (4,i), fit_color(a['fit']))
        style.add('TEXTCOLOR', (4,i), (4,i), white)
        style.add('FONT', (4,i), (4,i), 'KRB', 10)
    t.setStyle(style)
    return t

def proposal_block():
    text = """
    <b>1. 사업 참여 필요성</b><br/>
    (주)오드린은 국내 과실주 시장의 프리미엄화 흐름과 K-푸드 글로벌 확산기에 위치한
    와인 제조 중소기업으로, 농식품 글로벌 성장패키지 사업의 정책 목표(우리술 수출 확대)와
    높은 정합성을 보유한다. 본 사업 참여를 통해 해외 바이어 매칭, 현지 마케팅, 물류·통관
    지원 패키지를 활용하여 단기간 내 수출 매출 가시화가 가능하다.
    <br/><br/>
    <b>2. 사업 추진 계획</b><br/>
    • 1단계 (M1~M2): 타깃 시장 선정 (일본·미국·홍콩) + 제품 라인업 정비<br/>
    • 2단계 (M3~M5): aT 바이어 매칭 행사 참가, 현지 인증·라벨링 정비<br/>
    • 3단계 (M6~M9): 시범 수출 + 현지 시음회·B2B 프로모션 실행<br/>
    • 4단계 (M10~M12): 정기 발주 계약 체결 + 차년도 채널 확장 계획 수립
    <br/><br/>
    <b>3. 기대 효과 및 성과 지표</b><br/>
    • 정량: 신규 수출국 2개국 확보 / 수출 매출 +30% / 해외 거래선 5사 신규 발굴<br/>
    • 정성: 우리술 카테고리 내 프리미엄 브랜드 포지셔닝, 후속 R&D·인증 연계 기반 마련
    <br/><br/>
    <b>4. 사업화 지속 계획</b><br/>
    1차년도 수출 실적을 기반으로 수출바우처(KOTRA) → 벤처/이노비즈 인증 →
    스마트공장 구축 → 식품 R&D 지원사업으로 이어지는 4개년 정부지원 로드맵을 통해
    자생적 글로벌 와이너리 모델을 구축한다.
    """
    return Paragraph(text, S_BODY)

def fund_referral():
    text = """
    아래 항목은 융자·보증 성격으로, <b>자금 에이전트 후속 분석</b> 대상입니다.<br/>
    • 중소벤처기업진흥공단 청년창업·신성장기반자금 (식품 제조업 우대)<br/>
    • 기술보증기금 우리술 산업 특화 보증 상품<br/>
    • 농업정책보험금융원 농식품 모태펀드 연계 투자유치
    """
    return Paragraph(text, S_SMALL)

# ---------- 빌드 ----------
doc = SimpleDocTemplate(OUT_PDF, pagesize=A4,
                        leftMargin=15*mm, rightMargin=15*mm,
                        topMargin=22*mm, bottomMargin=15*mm)

story = []

# Section 1: 표지 (PageBreak로 본문 시작)
story.append(PageBreak())

# Section 2: 요약 카드
story.append(Paragraph('Executive Summary · 추천 Top 3', S_H1))
story.append(Paragraph(
    f'(주)오드린에 즉시 신청 권장되는 핵심 정부지원사업 3선. 발행일 {TODAY} 기준 모두 신청 가능.',
    S_BODY))
story.append(Spacer(1, 4*mm))
story.append(top3_cards())
story.append(Spacer(1, 6*mm))

# 핵심 인사이트 박스
insight = Table([[Paragraph(
    "<b>핵심 인사이트</b>  ·  와인 제조업은 농식품부·중기부·문체부의 3개 부처 지원이 "
    "교차하는 영역. 수출 트랙(aT) → 인증 트랙(벤처/이노비즈) → R&D·스마트공장(중기부) "
    "순으로 신청해 자금 갭을 메우는 4단계 로드맵을 권장한다.",
    S_BODY)]], colWidths=[180*mm])
insight.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),LIGHTBLUE),
    ('LEFTPADDING',(0,0),(-1,-1),10),
    ('RIGHTPADDING',(0,0),(-1,-1),10),
    ('TOPPADDING',(0,0),(-1,-1),8),
    ('BOTTOMPADDING',(0,0),(-1,-1),8),
    ('LINEBEFORE',(0,0),(0,-1),3,NAVY),
]))
story.append(insight)
story.append(PageBreak())

# Section 3: 기업 프로파일
story.append(Paragraph('1. 기업 프로파일', S_H1))
story.append(profile_block())
story.append(Spacer(1, 8*mm))

# Section 4: 매칭 현황표
story.append(Paragraph('2. 매칭 공고 전체 현황 (8건)', S_H1))
story.append(matching_table())
story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    '※ 적합도는 업종·규모·정책목적 정합성을 기준으로 한 히어컴퍼니 자체 평가입니다.',
    S_SMALL))
story.append(PageBreak())

# Section 5: 우선순위 매트릭스
story.append(Paragraph('3. 우선순위 매트릭스', S_H1))
story.append(Paragraph(
    'X축은 신청 난이도, Y축은 기대 효과, 버블 크기는 지원 규모(억원)를 의미합니다. '
    '우상단(전략 과제)은 장기 준비, 좌상단(Quick Win)은 즉시 착수 권장.', S_BODY))
story.append(Spacer(1, 4*mm))
story.append(RLImage(chart_priority_matrix(), width=175*mm, height=100*mm))
story.append(PageBreak())

# Section 6: 신청 타임라인
story.append(Paragraph('4. 신청 타임라인', S_H1))
story.append(Paragraph(
    f'오늘({TODAY}) 기준 마감 임박 순. 마감 30일 이내 공고는 즉시 서류 준비 착수 필요.',
    S_BODY))
story.append(Spacer(1, 4*mm))
story.append(RLImage(chart_timeline(), width=175*mm, height=105*mm))
story.append(PageBreak())

# Section 7: 제안서 초안
story.append(Paragraph('5. 1순위 공고 제안서 초안', S_H1))
story.append(Paragraph(
    '<b>대상 사업:</b> 농식품 글로벌 성장패키지 지원사업 (aT)', S_H2))
story.append(proposal_block())
story.append(Spacer(1, 6*mm))

story.append(Paragraph('자금 에이전트 이관 항목 (융자·보증)', S_H2))
story.append(fund_referral())
story.append(Spacer(1, 6*mm))

# 마지막 CTA
cta = Table([[Paragraph(
    "<b>HERE COMPANY</b>가 (주)오드린의 정부지원사업 신청부터 사업계획서 작성, "
    "선정 후 사후관리까지 풀 사이클을 함께합니다.<br/>"
    "<font color='#DEEAF1'>무료상담 · herecompany.kr</font>",
    ParagraphStyle('cta', fontName='KR', fontSize=10, textColor=white, leading=14))]],
    colWidths=[180*mm])
cta.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),NAVY),
    ('LEFTPADDING',(0,0),(-1,-1),12),
    ('RIGHTPADDING',(0,0),(-1,-1),12),
    ('TOPPADDING',(0,0),(-1,-1),12),
    ('BOTTOMPADDING',(0,0),(-1,-1),12),
]))
story.append(cta)

# ---------- onFirstPage / onLaterPages ----------
doc.build(story, onFirstPage=cover_page, onLaterPages=page_decor)
print(f'생성 완료: {OUT_PDF}')
print(f'파일 크기: {os.path.getsize(OUT_PDF)/1024:.1f} KB')
