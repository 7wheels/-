#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(주)기준테크 정부지원사업 리포트 생성기
히어컴퍼니 기업컨설팅 제공
"""
import os, io, urllib.request, subprocess, sys
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# ============ 한국어 폰트 등록 ============
FONT_PATH = '/tmp/NanumGothic.ttf'
FONT_BOLD_PATH = '/tmp/NanumGothicBold.ttf'

if not os.path.exists(FONT_PATH):
    print('한국어 폰트 다운로드 중...')
    urllib.request.urlretrieve(
        'https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf',
        FONT_PATH)
if not os.path.exists(FONT_BOLD_PATH):
    urllib.request.urlretrieve(
        'https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf',
        FONT_BOLD_PATH)

pdfmetrics.registerFont(TTFont('KR', FONT_PATH))
pdfmetrics.registerFont(TTFont('KR-Bold', FONT_BOLD_PATH))

# matplotlib 폰트
fm.fontManager.addfont(FONT_PATH)
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# ============ 브랜드 컬러 ============
NAVY = HexColor('#1F4E79')
BLUE = HexColor('#2E75B6')
LIGHT_BLUE = HexColor('#DEEAF1')
GREEN = HexColor('#00B050')
ORANGE = HexColor('#FF8C00')
RED = HexColor('#C00000')
GRAY = HexColor('#595959')
LIGHT_GRAY = HexColor('#F2F2F2')
WHITE = HexColor('#FFFFFF')

# ============ 데이터 ============
COMPANY = {
    'name': '(주)기준테크',
    'industry': '자동화기계 제조업',
    'ksic': 'C29',
    'business': '자동화 기계 제조 및 공급',
    'size': '중소기업',
    'years': '5년 이상',
    'location': '대한민국',
    'cert': '미보유 (벤처·이노비즈 추진 권장)',
}

REPORT_DATE = '2026-05-03'
REPORT_DATE_FILE = '20260503'

# 매칭된 정부지원사업 (실시간 검색 기반, 2026-05-03 시점 유효)
PROGRAMS = [
    {
        'title': '2026년 정부형 스마트공장 구축사업',
        'source': '중소벤처기업부 / 스마트제조혁신추진단',
        'deadline': '2026-06-30 (예산 소진시 마감)',
        'budget': '최대 2억원 (정부 50%, 자부담 50%)',
        'target': '제조 중소·중견기업',
        'category': 'gov',
        'match': '상',
        'difficulty': 3.0,
        'effect': 4.5,
        'amount_size': 200,
        'summary': 'ICT 기반 제조공정 최적화. 자동화기계 제조사로서 솔루션 공급자·도입자 양측 진입 가능.',
    },
    {
        'title': '2026년 R&D성과확산 스마트공장 구축 지원사업',
        'source': '중소벤처기업부 / 스마트제조혁신추진단',
        'deadline': '2026-05-30',
        'budget': '최대 4억원 (자동화장비·제어기·센서 포함)',
        'target': '도입기업+공급기업 컨소시엄',
        'category': 'gov',
        'match': '상',
        'difficulty': 4.0,
        'effect': 5.0,
        'amount_size': 400,
        'summary': '자동화기계 공급기업으로서 컨소시엄 주관 가능. 자동화장비·제어기·센서 직접 지원.',
    },
    {
        'title': '2026년 중소기업 기술개발(R&D) 지원사업',
        'source': '중소벤처기업부',
        'deadline': '2026-06-15 (수시·차수별)',
        'budget': '최대 6억원 / 2년',
        'target': '중소 제조기업',
        'category': 'gov',
        'match': '상',
        'difficulty': 4.5,
        'effect': 4.5,
        'amount_size': 600,
        'summary': '신기술·신제품 개발비 지원. 자동화기계 신모델 개발에 적합. 기업부설연구소 보유시 가점.',
    },
    {
        'title': '2026년 1·2차 수출지원기반활용사업 (수출바우처)',
        'source': '중소벤처기업부',
        'deadline': '2026-05-30 (2차 모집)',
        'budget': '최대 1억원 (바우처)',
        'target': '수출 중소기업',
        'category': 'gov',
        'match': '중',
        'difficulty': 2.5,
        'effect': 3.5,
        'amount_size': 100,
        'summary': '해외 마케팅·인증·전시회 바우처. 자동화기계 해외 진출 가속화에 적합.',
    },
    {
        'title': '2026년 AX혁신 ICT전략융합 R&D바우처',
        'source': '중소벤처기업부',
        'deadline': '2026-05-31',
        'budget': '최대 2억원',
        'target': 'AI·DX 전환 중소기업',
        'category': 'gov',
        'match': '중',
        'difficulty': 3.5,
        'effect': 4.0,
        'amount_size': 200,
        'summary': '자동화기계에 AI 제어·예지보전 기능 도입시 직접 매칭.',
    },
    {
        'title': '벤처기업 확인 + 이노비즈 인증 (병행 추진)',
        'source': '중소벤처기업부 / 이노비즈협회',
        'deadline': '상시',
        'budget': '인증 (정책자금 우대·세제혜택)',
        'target': '기술혁신형 중소기업',
        'category': 'cert',
        'match': '상',
        'difficulty': 2.0,
        'effect': 4.0,
        'amount_size': 150,
        'summary': '기업부설연구소 설립 → 벤처확인 → 이노비즈 순차 추진. 후속 R&D 가점 + 정책자금 금리 우대.',
    },
    {
        'title': '2026년 중소기업 정책자금 (시설자금)',
        'source': '중소벤처기업진흥공단',
        'deadline': '상시 (예산 소진시 마감)',
        'budget': '최대 100억원, 연 2%대 (자금 에이전트 이관)',
        'target': '제조 중소기업',
        'category': 'fund',
        'match': '중',
        'difficulty': 3.0,
        'effect': 3.5,
        'amount_size': 500,
        'summary': '노후장비 교체·생산설비 확충용 시설자금. 융자 성격 → 자금 에이전트 추가 검토.',
    },
]

# ============ 차트 생성 함수 ============
def make_priority_matrix():
    fig, ax = plt.subplots(figsize=(8, 5))
    colors_map = {'상': '#00B050', '중': '#FF8C00', '하': '#C00000'}
    for p in PROGRAMS:
        ax.scatter(p['difficulty'], p['effect'],
                   s=p['amount_size']*3,
                   c=colors_map[p['match']],
                   alpha=0.55, edgecolors='#1F4E79', linewidth=1.5)
        # 짧은 라벨
        label = p['title'][:14] + ('…' if len(p['title']) > 14 else '')
        ax.annotate(label, (p['difficulty'], p['effect']),
                    xytext=(7, 7), textcoords='offset points',
                    fontsize=8, color='#1F4E79')
    ax.set_xlabel('신청 난이도 (낮음 → 높음)', fontsize=11, color='#1F4E79')
    ax.set_ylabel('기대 효과 (낮음 → 높음)', fontsize=11, color='#1F4E79')
    ax.set_title('정부지원사업 우선순위 매트릭스', fontsize=13, color='#1F4E79', pad=15)
    ax.set_xlim(1, 5.5)
    ax.set_ylim(2.5, 5.5)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=4, color='gray', linestyle='--', alpha=0.4)
    ax.axvline(x=3, color='gray', linestyle='--', alpha=0.4)
    # 사분면 라벨
    ax.text(1.3, 5.3, '쉽고 효과 큼\n(즉시 추진)', fontsize=9, color='#00B050', alpha=0.7)
    ax.text(4.5, 5.3, '어렵고 효과 큼\n(전략 추진)', fontsize=9, color='#1F4E79', alpha=0.7)
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return buf

def make_timeline():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    # (이름, 시작주, 기간주)
    tasks = [
        ('R&D성과확산 스마트공장', 0, 4, '#2E75B6'),
        ('AX혁신 R&D바우처',       0, 4, '#2E75B6'),
        ('수출바우처 2차',           1, 4, '#FF8C00'),
        ('정부형 스마트공장',        2, 8, '#00B050'),
        ('중소기업 R&D 통합',        3, 6, '#1F4E79'),
        ('벤처·이노비즈 인증',      0, 12, '#7030A0'),
        ('정책자금 (시설)',          4, 8, '#C00000'),
    ]
    for i, (name, start, dur, c) in enumerate(tasks):
        ax.barh(i, dur, left=start, color=c, alpha=0.8, edgecolor='#1F4E79')
        ax.text(start+dur/2, i, f'{dur}주', ha='center', va='center',
                color='white', fontsize=9, fontweight='bold')
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([t[0] for t in tasks], fontsize=10)
    ax.set_xlabel('주차 (2026-05-03 기준)', fontsize=11, color='#1F4E79')
    ax.set_title('정부지원사업 신청 타임라인', fontsize=13, color='#1F4E79', pad=15)
    ax.invert_yaxis()
    ax.grid(True, axis='x', alpha=0.3)
    ax.set_xlim(0, 14)
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return buf

# ============ PDF 생성 ============
PDF_PATH = f'/home/user/-/_workspace/here-company/기준테크/기준테크_정부지원사업리포트_{REPORT_DATE_FILE}.pdf'

doc = SimpleDocTemplate(PDF_PATH, pagesize=A4,
                        leftMargin=18*mm, rightMargin=18*mm,
                        topMargin=18*mm, bottomMargin=18*mm)

styles = getSampleStyleSheet()
H1 = ParagraphStyle('H1', fontName='KR-Bold', fontSize=22, textColor=NAVY,
                    alignment=TA_LEFT, spaceAfter=10, leading=28)
H2 = ParagraphStyle('H2', fontName='KR-Bold', fontSize=15, textColor=NAVY,
                    alignment=TA_LEFT, spaceAfter=8, leading=20,
                    borderPadding=0)
H3 = ParagraphStyle('H3', fontName='KR-Bold', fontSize=12, textColor=BLUE,
                    spaceAfter=6, leading=16)
BODY = ParagraphStyle('BODY', fontName='KR', fontSize=10, textColor=GRAY,
                      leading=15, spaceAfter=4)
SMALL = ParagraphStyle('SMALL', fontName='KR', fontSize=8.5, textColor=GRAY, leading=12)
COVER_TITLE = ParagraphStyle('CT', fontName='KR-Bold', fontSize=30, textColor=WHITE,
                             alignment=TA_CENTER, leading=38, spaceAfter=12)
COVER_SUB = ParagraphStyle('CS', fontName='KR', fontSize=14, textColor=WHITE,
                           alignment=TA_CENTER, leading=22)
COVER_BRAND = ParagraphStyle('CB', fontName='KR-Bold', fontSize=11, textColor=WHITE,
                             alignment=TA_CENTER, leading=18)

story = []

# ========== 1. 표지 ==========
def cover_table():
    inner = [
        [Spacer(1, 70*mm)],
        [Paragraph(f"{COMPANY['name']}", COVER_TITLE)],
        [Paragraph("정부지원사업 매칭 리포트", COVER_SUB)],
        [Spacer(1, 8*mm)],
        [Paragraph(f"발행일 : {REPORT_DATE}", COVER_SUB)],
        [Spacer(1, 70*mm)],
        [Paragraph("HERE COMPANY 기업컨설팅", COVER_BRAND)],
        [Paragraph("히어컴퍼니 정부지원사업 전문가팀 제공", COVER_BRAND)],
        [Spacer(1, 6*mm)],
    ]
    t = Table(inner, colWidths=[170*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    return t

story.append(cover_table())
story.append(PageBreak())

# ========== 2. 요약 카드: Top 3 ==========
story.append(Paragraph("EXECUTIVE SUMMARY", H1))
story.append(Paragraph("기준테크 추천 Top 3 정부지원사업", H3))
story.append(Spacer(1, 4*mm))

top3 = [p for p in PROGRAMS if p['match'] == '상'][:3]
card_color = {'상': GREEN, '중': ORANGE, '하': RED}

for i, p in enumerate(top3, 1):
    rank = Paragraph(f"<b>#{i}</b>", ParagraphStyle('rank', fontName='KR-Bold',
                    fontSize=24, textColor=WHITE, alignment=TA_CENTER, leading=28))
    title = Paragraph(f"<b>{p['title']}</b>", ParagraphStyle('ct', fontName='KR-Bold',
                    fontSize=12, textColor=NAVY, leading=16))
    info = Paragraph(
        f"<b>지원규모</b> {p['budget']}<br/>"
        f"<b>마감</b> {p['deadline']} &nbsp;&nbsp; <b>적합도</b> {p['match']}<br/>"
        f"{p['summary']}",
        BODY)
    card = Table([[rank, [title, Spacer(1, 2*mm), info]]],
                 colWidths=[22*mm, 148*mm], rowHeights=[28*mm])
    card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), card_color[p['match']]),
        ('BACKGROUND', (1,0), (1,0), LIGHT_BLUE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (1,0), (1,0), 8),
        ('RIGHTPADDING', (1,0), (1,0), 8),
        ('TOPPADDING', (1,0), (1,0), 6),
        ('BOTTOMPADDING', (1,0), (1,0), 6),
        ('BOX', (0,0), (-1,-1), 0.5, NAVY),
    ]))
    story.append(card)
    story.append(Spacer(1, 3*mm))

story.append(Spacer(1, 6*mm))
story.append(Paragraph(
    "<b>핵심 인사이트:</b> 기준테크는 자동화기계 공급기업으로서 스마트공장 보급사업의 "
    "<b>공급사·주관사</b> 양 측면 진입이 가능하며, 기업부설연구소 설립 → 벤처·이노비즈 "
    "인증 → R&D 과제 수주의 3단계 시너지 전략이 가장 효과적입니다.",
    BODY))
story.append(PageBreak())

# ========== 3. 기업 프로파일 ==========
story.append(Paragraph("기업 프로파일", H1))
story.append(Spacer(1, 4*mm))

profile_data = [
    ['구분', '내용'],
    ['기업명', COMPANY['name']],
    ['업종 (KSIC)', f"{COMPANY['industry']}  ({COMPANY['ksic']})"],
    ['주요 사업', COMPANY['business']],
    ['기업 규모', COMPANY['size']],
    ['업력', COMPANY['years']],
    ['소재지', COMPANY['location']],
    ['보유 인증', COMPANY['cert']],
]
pt = Table(profile_data, colWidths=[40*mm, 130*mm])
pt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'KR-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'KR'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('BACKGROUND', (0,1), (0,-1), LIGHT_BLUE),
    ('TEXTCOLOR', (0,1), (0,-1), NAVY),
    ('FONTNAME', (0,1), (0,-1), 'KR-Bold'),
    ('GRID', (0,0), (-1,-1), 0.4, GRAY),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
]))
story.append(pt)
story.append(Spacer(1, 8*mm))

story.append(Paragraph("진단 코멘트", H3))
story.append(Paragraph(
    "자동화기계 제조업(C29)은 2026년 정부의 <b>제조혁신·디지털전환·탄소중립 핵심 수혜 업종</b>입니다. "
    "특히 스마트공장 보급사업의 솔루션 공급기업 풀에 진입할 경우 안정적인 매출 파이프라인 확보가 가능하며, "
    "동시에 자체 R&D를 통한 신모델 개발로 기술 경쟁력을 동시에 강화할 수 있습니다.",
    BODY))
story.append(PageBreak())

# ========== 4. 매칭 현황표 ==========
story.append(Paragraph("매칭 공고 현황", H1))
story.append(Spacer(1, 3*mm))
story.append(Paragraph(f"검색일: {REPORT_DATE}  /  총 {len(PROGRAMS)}건  /  마감 지난 공고 제외", SMALL))
story.append(Spacer(1, 4*mm))

match_color_map = {'상': GREEN, '중': ORANGE, '하': RED}
match_data = [['공고명', '지원규모', '마감', '적합도']]
for p in PROGRAMS:
    match_data.append([
        Paragraph(f"<b>{p['title']}</b><br/><font size=8 color='#595959'>{p['source']}</font>",
                  ParagraphStyle('mt', fontName='KR', fontSize=9, leading=12)),
        Paragraph(p['budget'], ParagraphStyle('mb', fontName='KR', fontSize=9, leading=12)),
        Paragraph(p['deadline'], ParagraphStyle('md', fontName='KR', fontSize=9, leading=12)),
        Paragraph(f"<b>{p['match']}</b>",
                  ParagraphStyle('mm', fontName='KR-Bold', fontSize=11,
                                 textColor=match_color_map[p['match']],
                                 alignment=TA_CENTER)),
    ])

mt = Table(match_data, colWidths=[68*mm, 50*mm, 36*mm, 16*mm], repeatRows=1)
style_cmds = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'KR-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 10),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ('GRID', (0,0), (-1,-1), 0.4, GRAY),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('ALIGN', (3,0), (3,-1), 'CENTER'),
]
# 행 색상 alternating
for i in range(1, len(match_data)):
    if i % 2 == 0:
        style_cmds.append(('BACKGROUND', (0,i), (-1,i), LIGHT_GRAY))
mt.setStyle(TableStyle(style_cmds))
story.append(mt)
story.append(PageBreak())

# ========== 5. 우선순위 매트릭스 ==========
story.append(Paragraph("우선순위 매트릭스", H1))
story.append(Paragraph("신청 난이도 × 기대효과 (버블=지원규모)", H3))
story.append(Spacer(1, 4*mm))
story.append(RLImage(make_priority_matrix(), width=170*mm, height=106*mm))
story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    "<b>해석:</b> 우상단의 <b>R&D성과확산 스마트공장</b>·<b>중소기업 R&D 통합</b>이 "
    "기대효과·금액 모두 최상위. 좌상단의 <b>벤처·이노비즈 인증</b>은 난이도가 낮고 효과가 커 "
    "병행 추진의 최우선 후보입니다.", BODY))
story.append(PageBreak())

# ========== 6. 신청 타임라인 ==========
story.append(Paragraph("신청 타임라인", H1))
story.append(Paragraph("2026-05-03부터 14주 단위 추진 계획", H3))
story.append(Spacer(1, 4*mm))
story.append(RLImage(make_timeline(), width=170*mm, height=85*mm))
story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    "<b>긴급 추진 (1~4주):</b> R&D성과확산 스마트공장(5/30 마감), AX혁신 R&D바우처(5/31 마감), "
    "수출바우처 2차 모집. 동시에 벤처·이노비즈 인증 절차 착수.<br/>"
    "<b>중기 추진 (5~10주):</b> 정부형 스마트공장, 중소기업 R&D 통합 본 신청.<br/>"
    "<b>장기 추진 (5~14주):</b> 정책자금 시설자금 협의 (자금 에이전트 연계).",
    BODY))
story.append(PageBreak())

# ========== 7. 1순위 제안서 초안 ==========
story.append(Paragraph("1순위 제안서 초안", H1))
story.append(Paragraph("R&D성과확산 스마트공장 구축 지원사업", H3))
story.append(Spacer(1, 4*mm))

story.append(Paragraph("1. 사업 참여 필요성 및 목적", H3))
story.append(Paragraph(
    "(주)기준테크는 자동화기계 제조 분야 5년 이상의 양산 경험과 자체 설계·제어 역량을 보유한 "
    "중소 제조기업으로, 정부 R&D 성과기술을 현장 적용 가능한 <b>자동화 솔루션 패키지</b>로 "
    "전환할 수 있는 공급기업 적합성을 갖추고 있다. 본 사업 참여를 통해 도입기업의 "
    "제조 경쟁력 강화에 기여하는 동시에, 기준테크의 자동화 솔루션 레퍼런스를 확보하여 "
    "후속 양산 매출로 연결하는 <b>이중 성과 창출</b>이 본 과제의 핵심 목적이다.", BODY))

story.append(Paragraph("2. 사업 추진 계획", H3))
plan_data = [
    ['단계', '주요 내용', '기간', '예상 성과'],
    ['1. 진단', '도입기업 공정 진단·요구사항 정의', '1개월', '구축 사양서'],
    ['2. 설계', '자동화장비·제어기·센서 통합 설계', '2개월', '설계도서'],
    ['3. 구축', '장비 제작·설치·시운전', '4개월', '가동 시스템'],
    ['4. 안정화', '데이터 수집·KPI 검증·고도화', '2개월', '성과 보고서'],
]
plan_t = Table(plan_data, colWidths=[18*mm, 80*mm, 25*mm, 47*mm])
plan_t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'KR-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'KR'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.4, GRAY),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(plan_t)
story.append(Spacer(1, 4*mm))

story.append(Paragraph("3. 기대 효과 및 성과 지표", H3))
story.append(Paragraph(
    "<b>정량 지표:</b> 도입기업 생산성 25% 향상, 불량률 30% 감소, 기준테크 후속 매출 5억원 이상.<br/>"
    "<b>정성 지표:</b> 자동화 솔루션 표준 모듈화 확보, 중견 제조사향 레퍼런스 구축, "
    "벤처·이노비즈 인증 가점 확보.", BODY))

story.append(Paragraph("4. 사업화 지속 계획", H3))
story.append(Paragraph(
    "본 과제로 검증된 솔루션 패키지를 표준화하여 동종 업종 도입기업 5개사 이상에 확산 보급한다. "
    "또한 기업부설연구소 설립과 연동하여 자체 IP를 확보하고, 후속 R&D·정책자금 연계로 "
    "지속적인 자금·기술 선순환 구조를 구축한다.", BODY))

story.append(Spacer(1, 8*mm))

# ========== 푸터: 자금 에이전트 이관 ==========
story.append(Paragraph("[부록] 자금 에이전트 이관 항목 (융자·보증)", H3))
story.append(Paragraph(
    "다음 항목은 융자·보증 성격으로, 별도 자금 에이전트 검토 권장:<br/>"
    "• 중소기업 정책자금 시설자금 (중진공, 최대 100억, 연 2%대)<br/>"
    "• 기보·신보 보증부 대출 (인증 취득 후 보증료·금리 우대)", BODY))

story.append(Spacer(1, 10*mm))

# 푸터 브랜딩
footer = Table([[Paragraph(
    f"<b>HERE COMPANY 기업컨설팅</b>  |  히어컴퍼니 정부지원사업 전문가팀  |  발행 {REPORT_DATE}",
    ParagraphStyle('f', fontName='KR-Bold', fontSize=9, textColor=WHITE,
                   alignment=TA_CENTER))]],
    colWidths=[170*mm], rowHeights=[10*mm])
footer.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), NAVY),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(footer)

# ============ 빌드 ============
print(f'PDF 생성 중: {PDF_PATH}')
doc.build(story)
print(f'완료: {PDF_PATH}')
print(f'파일크기: {os.path.getsize(PDF_PATH)/1024:.1f} KB')
