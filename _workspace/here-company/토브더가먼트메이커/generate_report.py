import io, os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

# ── 폰트 등록 ──────────────────────────────────────────────
FONT_PATH = '/tmp/NanumGothic.ttf'
MPL_FONT = '/tmp/NanumGothic.ttf'
pdfmetrics.registerFont(TTFont('KR', FONT_PATH))
pdfmetrics.registerFont(TTFont('KR-Bold', FONT_PATH))

# matplotlib 한글 폰트
fm.fontManager.addfont(MPL_FONT)
plt.rcParams['font.family'] = fm.FontProperties(fname=MPL_FONT).get_name()
plt.rcParams['axes.unicode_minus'] = False

# ── 색상 ──────────────────────────────────────────────────
NAVY   = colors.HexColor('#1F4E79')
BLUE   = colors.HexColor('#2E75B6')
LTBLUE = colors.HexColor('#DEEAF1')
GREEN  = colors.HexColor('#00B050')
ORANGE = colors.HexColor('#FF8C00')
RED    = colors.HexColor('#C00000')
WHITE  = colors.white
GRAY   = colors.HexColor('#F2F2F2')

# ── 스타일 ─────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, fontName='KR', **kw)

ST_TITLE  = S('title',  fontSize=22, textColor=WHITE,   leading=28, alignment=1, spaceAfter=4)
ST_SUB    = S('sub',    fontSize=13, textColor=LTBLUE,  leading=18, alignment=1)
ST_H1     = S('h1',     fontSize=14, textColor=NAVY,    leading=18, spaceBefore=10, spaceAfter=4)
ST_H2     = S('h2',     fontSize=11, textColor=BLUE,    leading=16, spaceBefore=6,  spaceAfter=3)
ST_BODY   = S('body',   fontSize=9,  textColor=colors.black, leading=14)
ST_SMALL  = S('small',  fontSize=8,  textColor=colors.HexColor('#444444'), leading=12)
ST_WHITE  = S('white',  fontSize=9,  textColor=WHITE,   leading=13)
ST_BADGE  = S('badge',  fontSize=10, textColor=WHITE,   leading=14, alignment=1)

W, H = A4
OUT = '/home/user/-/_workspace/here-company/토브더가먼트메이커/토브더가먼트메이커_정부지원사업리포트_20260501.pdf'
doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)

story = []

# ══════════════════════════════════════════════════════
# 섹션 1: 표지
# ══════════════════════════════════════════════════════
def cover_table():
    data = [[
        Paragraph('히어컴퍼니 정부지원사업 리포트', S('ct', fontSize=10, textColor=LTBLUE, alignment=1)),
    ],[
        Paragraph('(주)토브더가먼트메이커', ST_TITLE),
    ],[
        Paragraph('정부지원사업 맞춤 매칭 리포트', ST_SUB),
    ],[
        Paragraph('2026. 05. 01 | 의류제조업 (택티컬 전문) | 서울 성동구', 
                  S('cd', fontSize=9, textColor=colors.HexColor('#BDD7EE'), alignment=1, spaceBefore=8)),
    ]]
    t = Table(data, colWidths=[180*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ROUNDEDCORNERS', [6]),
    ]))
    return t

story.append(cover_table())
story.append(Spacer(1, 6*mm))

# ══════════════════════════════════════════════════════
# 섹션 2: 기업 프로파일 카드
# ══════════════════════════════════════════════════════
story.append(Paragraph('기업 프로파일', ST_H1))

profile_data = [
    ['항목', '내용'],
    ['기업명',   '(주)토브더가먼트메이커'],
    ['업종',     '의류제조업 (택티컬·기능성 의류 전문)'],
    ['연 매출',  '40억 원 (2025년)'],
    ['직원 수',  '8명 (소기업)'],
    ['업력',     '약 9년차 (2017년 설립)'],
    ['소재지',   '서울 성동구'],
    ['수혜 이력','없음 (최초 신청 — 신규 가점 활용 가능)'],
    ['희망 분야','자금 / 수출 / R&D'],
]
pt = Table(profile_data, colWidths=[40*mm, 140*mm])
pt.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,0),  NAVY),
    ('TEXTCOLOR',    (0,0), (-1,0),  WHITE),
    ('FONTNAME',     (0,0), (-1,-1), 'KR'),
    ('FONTSIZE',     (0,0), (-1,-1), 9),
    ('BACKGROUND',   (0,1), (0,-1),  LTBLUE),
    ('ROWBACKGROUNDS',(1,1),(-1,-1), [WHITE, GRAY]),
    ('GRID',         (0,0), (-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',   (0,0), (-1,-1), 5),
    ('BOTTOMPADDING',(0,0), (-1,-1), 5),
    ('LEFTPADDING',  (0,0), (-1,-1), 8),
]))
story.append(pt)
story.append(Spacer(1, 6*mm))

# ══════════════════════════════════════════════════════
# 섹션 3: 추천 Top 5 요약 카드
# ══════════════════════════════════════════════════════
story.append(Paragraph('추천 지원사업 Top 5', ST_H1))

programs = [
    ('1순위', '수출바우처 사업', '최대 5,000만원', '★★★ 상', GREEN,   '수출 채널 구축 · 해외 바이어 발굴 직결'),
    ('2순위', '중진공 정책자금 운영자금', '최대 5억원', '★★★ 상', GREEN, '저금리 2~3%대 · 즉시 유동성 확보'),
    ('3순위', '서울시 중소기업 육성자금', '최대 1억원', '★★★ 상', GREEN, '성동구 소재 우대 · 연 1.5% 고정금리'),
    ('4순위', '기술혁신개발사업(R&D)', '최대 1.5억원', '★★  중', ORANGE,'기능성 소재 R&D · 하반기 공고 준비'),
    ('5순위', '소재부품기술개발사업', '3~5억원', '★★  중', ORANGE, '대규모 R&D · 2027년 목표 사전 준비'),
]

for rank, name, amount, fit, color, desc in programs:
    row = Table([[
        Table([[Paragraph(rank, ST_BADGE)]], colWidths=[18*mm],
              style=[('BACKGROUND',(0,0),(-1,-1),color),
                     ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]),
        Table([[Paragraph(f'<b>{name}</b>', S('cn', fontSize=10, textColor=NAVY)),
                Paragraph(desc, ST_SMALL)]],
              colWidths=[120*mm],
              style=[('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
                     ('LEFTPADDING',(0,0),(-1,-1),8)]),
        Table([[Paragraph(amount, S('ca', fontSize=9, textColor=NAVY, alignment=1)),
                Paragraph(fit,    S('cf', fontSize=8, textColor=color,  alignment=1))]],
              colWidths=[40*mm],
              style=[('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]),
    ]], colWidths=[18*mm, 120*mm, 42*mm])
    row.setStyle(TableStyle([
        ('BOX',        (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('LEFTPADDING',(0,0),(-1,-1),0),
        ('RIGHTPADDING',(0,0),(-1,-1),0),
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[WHITE]),
    ]))
    story.append(row)
    story.append(Spacer(1, 2*mm))

story.append(Spacer(1, 4*mm))

# ══════════════════════════════════════════════════════
# 섹션 4: 매칭 현황표
# ══════════════════════════════════════════════════════
story.append(Paragraph('매칭 현황 상세표', ST_H1))

match_data = [
    ['사업명', '주관기관', '지원규모', '마감', '적합도'],
    ['수출바우처 2차', '중기부/중진공', '최대 5,000만원', '5~6월 예정', '상'],
    ['중진공 운영자금', '중소기업진흥공단', '최대 5억원', '상시 신청', '상'],
    ['서울시 육성자금', '서울시/신보', '최대 1억원', '상시 신청', '상'],
    ['기술혁신개발(R&D)', '중기부/TIPA', '최대 1.5억원', '하반기 예정', '중'],
    ['소재부품기술개발', '산업부/KEIT', '3~5억원', '하반기 예정', '중'],
]
mt = Table(match_data, colWidths=[55*mm, 38*mm, 32*mm, 28*mm, 17*mm])
fit_colors = {'상': GREEN, '중': ORANGE}
mt_style = [
    ('BACKGROUND',   (0,0), (-1,0),  NAVY),
    ('TEXTCOLOR',    (0,0), (-1,0),  WHITE),
    ('FONTNAME',     (0,0), (-1,-1), 'KR'),
    ('FONTSIZE',     (0,0), (-1,-1), 8.5),
    ('GRID',         (0,0), (-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',   (0,0), (-1,-1), 5),
    ('BOTTOMPADDING',(0,0), (-1,-1), 5),
    ('LEFTPADDING',  (0,0), (-1,-1), 6),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [WHITE, GRAY]),
    ('ALIGN', (2,0), (-1,-1), 'CENTER'),
]
for i, row in enumerate(match_data[1:], 1):
    c = fit_colors.get(row[-1], GRAY)
    mt_style += [
        ('BACKGROUND', (4,i), (4,i), c),
        ('TEXTCOLOR',  (4,i), (4,i), WHITE),
        ('FONTNAME',   (4,i), (4,i), 'KR-Bold'),
    ]
mt.setStyle(TableStyle(mt_style))
story.append(mt)
story.append(Spacer(1, 6*mm))

# ══════════════════════════════════════════════════════
# 섹션 5: 우선순위 매트릭스 (버블차트)
# ══════════════════════════════════════════════════════
story.append(Paragraph('우선순위 매트릭스', ST_H1))

fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor('#F8FBFF')
ax.set_facecolor('#F8FBFF')

bubbles = [
    ('수출바우처',    2, 9, 500,  '#00B050'),
    ('중진공 운영자금', 2, 8, 500, '#00B050'),
    ('서울시 육성자금', 1, 7, 100, '#00B050'),
    ('기술혁신개발',  6, 8, 150,  '#FF8C00'),
    ('소재부품기술',  8, 9, 400,  '#FF8C00'),
]
for name, x, y, size, c in bubbles:
    ax.scatter(x, y, s=size*2, color=c, alpha=0.7, edgecolors='white', linewidths=1.5)
    ax.annotate(name, (x, y), textcoords='offset points', xytext=(0, 10),
                ha='center', fontsize=8, color='#333333')

ax.set_xlim(0, 10); ax.set_ylim(5, 10.5)
ax.set_xlabel('신청 난이도 →', fontsize=9, color='#555555')
ax.set_ylabel('기대 효과 →',  fontsize=9, color='#555555')
ax.set_title('신청 난이도 vs 기대 효과 (버블 크기 = 지원 규모)', fontsize=10, color='#1F4E79', pad=10)
ax.axvline(5, color='#CCCCCC', linestyle='--', linewidth=0.8)
ax.axhline(7.5, color='#CCCCCC', linestyle='--', linewidth=0.8)
ax.text(1, 10.3, '즉시 신청', fontsize=8, color='#00B050', style='italic')
ax.text(6, 10.3, '준비 후 신청', fontsize=8, color='#FF8C00', style='italic')

patches = [mpatches.Patch(color='#00B050', label='적합도 상'),
           mpatches.Patch(color='#FF8C00', label='적합도 중')]
ax.legend(handles=patches, loc='lower right', fontsize=8)
ax.grid(True, alpha=0.3)

buf1 = io.BytesIO()
fig.savefig(buf1, format='png', dpi=130, bbox_inches='tight')
buf1.seek(0)
plt.close()
story.append(RLImage(buf1, width=170*mm, height=85*mm))
story.append(Spacer(1, 6*mm))

# ══════════════════════════════════════════════════════
# 섹션 6: 신청 타임라인 (간트차트)
# ══════════════════════════════════════════════════════
story.append(Paragraph('2026년 신청 타임라인', ST_H1))

fig2, ax2 = plt.subplots(figsize=(8, 3.5))
fig2.patch.set_facecolor('#F8FBFF')
ax2.set_facecolor('#F8FBFF')

tasks = [
    ('수출바우처',    5, 1, '#00B050'),
    ('중진공 운영자금', 5, 1, '#00B050'),
    ('서울시 육성자금', 5, 2, '#00B050'),
    ('기술혁신개발', 9, 2, '#FF8C00'),
    ('소재부품기술', 10, 3, '#FF8C00'),
]
for i, (name, start, dur, c) in enumerate(tasks):
    ax2.barh(i, dur, left=start-1, color=c, alpha=0.8, height=0.6, edgecolor='white')
    ax2.text(start-1+dur+0.1, i, name, va='center', fontsize=8, color='#333333')

months = ['5월','6월','7월','8월','9월','10월','11월','12월']
ax2.set_xticks(range(8))
ax2.set_xticklabels(months, fontsize=8)
ax2.set_yticks(range(len(tasks)))
ax2.set_yticklabels([t[0] for t in tasks], fontsize=8)
ax2.set_title('월별 신청·선정 일정 (2026년)', fontsize=10, color='#1F4E79', pad=8)
ax2.set_xlim(-0.5, 10)
ax2.grid(axis='x', alpha=0.3)
ax2.invert_yaxis()

buf2 = io.BytesIO()
fig2.savefig(buf2, format='png', dpi=130, bbox_inches='tight')
buf2.seek(0)
plt.close()
story.append(RLImage(buf2, width=170*mm, height=80*mm))
story.append(Spacer(1, 6*mm))

# ══════════════════════════════════════════════════════
# 섹션 7: 제안서 초안 (수출바우처)
# ══════════════════════════════════════════════════════
story.append(Paragraph('1순위 제안서 초안 — 수출바우처', ST_H1))

proposal = [
    ('사업 참여 필요성',
     '국내 택티컬 의류 시장이 포화되는 반면, 글로벌 밀리터리·아웃도어 시장은 연 7~12% 성장 중이다. '
     '9년간 쌓은 제조 전문성과 고기능성 소재 가공 기술을 보유하고 있으나, 수출 채널과 해외 마케팅 인프라가 없다. '
     '수출바우처로 바이어 발굴·전시회 참가·디지털 마케팅에 집중 투자하여 첫 수출 성과(50만 달러)를 달성한다.'),
    ('추진 계획',
     '1단계(1~2개월): 영문 카탈로그·온라인 쇼룸 제작, 수출 인증 검토 | '
     '2단계(3~5개월): KOTRA 활용 미국·유럽 바이어 매칭 5개사, B2B 마케팅 실행 | '
     '3단계(6~10개월): 유럽 ISPO 전시회 참가, 첫 FOB 계약 1건 이상 체결'),
    ('기대 효과',
     '수출액 5억원 이상 달성 (1년) · 해외 바이어 5개사 · 수출 비중 10% 이상 · '
     '2027년 이노비즈·벤처 인증 연계 · 국내 경기 의존도 분산'),
]
for title, content in proposal:
    story.append(Paragraph(title, ST_H2))
    story.append(Paragraph(content, ST_BODY))
    story.append(Spacer(1, 3*mm))

# 예상 수혜 합계
total_data = [
    ['사업명', '예상 수혜액', '성격'],
    ['수출바우처',     '3,000~5,000만원', '비융자'],
    ['중진공 운영자금','3억~5억원',       '융자'],
    ['서울시 육성자금','1,000~1억원',     '융자'],
    ['R&D 과제',      '1억~1.5억원',     '비융자'],
    ['합  계',        '약 5억~8억원+',   '복합'],
]
tt = Table(total_data, colWidths=[65*mm, 55*mm, 50*mm])
tt_style = [
    ('BACKGROUND',   (0,0), (-1,0),  NAVY),
    ('TEXTCOLOR',    (0,0), (-1,0),  WHITE),
    ('BACKGROUND',   (0,-1),(-1,-1), LTBLUE),
    ('FONTNAME',     (0,0), (-1,-1), 'KR'),
    ('FONTNAME',     (0,-1),(-1,-1), 'KR-Bold'),
    ('FONTSIZE',     (0,0), (-1,-1), 9),
    ('GRID',         (0,0), (-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',   (0,0), (-1,-1), 5),
    ('BOTTOMPADDING',(0,0), (-1,-1), 5),
    ('LEFTPADDING',  (0,0), (-1,-1), 8),
    ('ROWBACKGROUNDS',(0,1),(-1,-2), [WHITE, GRAY]),
]
tt.setStyle(TableStyle(tt_style))
story.append(Spacer(1, 3*mm))
story.append(Paragraph('예상 총 수혜 규모', ST_H2))
story.append(tt)

story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    '본 리포트는 히어컴퍼니 정부지원사업팀이 2026-05-01 기준 공개 공고를 바탕으로 작성하였습니다. '
    '실제 신청 전 최신 공고문을 반드시 재확인하시기 바랍니다. | 히어컴퍼니 대표상담 1:1 문의',
    ST_SMALL))

# ── 빌드 ──────────────────────────────────────────────
doc.build(story)
print(f'PDF generated: {OUT}')
