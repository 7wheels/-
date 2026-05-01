import io, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

# ── 폰트 ──────────────────────────────────────────────────
FONT = '/tmp/NanumGothic.ttf'
pdfmetrics.registerFont(TTFont('KR', FONT))
fm.fontManager.addfont(FONT)
plt.rcParams['font.family'] = fm.FontProperties(fname=FONT).get_name()
plt.rcParams['axes.unicode_minus'] = False

# ── 색상 ──────────────────────────────────────────────────
NAVY   = colors.HexColor('#1F4E79')
BLUE   = colors.HexColor('#2E75B6')
LTBLUE = colors.HexColor('#DEEAF1')
GREEN  = colors.HexColor('#00B050')
ORANGE = colors.HexColor('#FF8C00')
WHITE  = colors.white
GRAY   = colors.HexColor('#F5F5F5')
DGRAY  = colors.HexColor('#666666')

# ── 스타일 헬퍼 ────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, fontName='KR', **kw)

ST = {
    'cover_label': S('cl', fontSize=9,  textColor=LTBLUE, alignment=1),
    'cover_title': S('ct', fontSize=24, textColor=WHITE,  leading=30, alignment=1, spaceAfter=4),
    'cover_sub':   S('cs', fontSize=13, textColor=LTBLUE, leading=18, alignment=1),
    'cover_date':  S('cd', fontSize=9,  textColor=colors.HexColor('#BDD7EE'), alignment=1, spaceBefore=6),
    'h1':  S('h1', fontSize=13, textColor=NAVY, leading=18, spaceBefore=8, spaceAfter=4),
    'h2':  S('h2', fontSize=10, textColor=BLUE, leading=15, spaceBefore=5, spaceAfter=2),
    'body': S('b',  fontSize=8.5, textColor=colors.black, leading=14),
    'small': S('sm', fontSize=7.5, textColor=DGRAY, leading=12),
    'tag_g': S('tg', fontSize=9,  textColor=WHITE, leading=12, alignment=1),
    'tag_o': S('to', fontSize=9,  textColor=WHITE, leading=12, alignment=1),
    'rank':  S('rk', fontSize=10, textColor=WHITE, leading=14, alignment=1),
    'prog':  S('pr', fontSize=9.5, textColor=NAVY, leading=14),
    'amt':   S('am', fontSize=9,  textColor=BLUE, leading=13, alignment=2),
    'desc':  S('dc', fontSize=8,  textColor=DGRAY, leading=12),
}

W, H = A4
OUT = '/home/user/-/_workspace/here-company/토브더가먼트메이커/토브더가먼트메이커_정부지원사업리포트_20260501.pdf'
doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
story = []

# ══ 1. 표지 ══════════════════════════════════════════════
cover = Table([[
    Paragraph('히어컴퍼니 정부지원사업 리포트', ST['cover_label']),
    ],[
    Paragraph('(주)토브더가먼트메이커', ST['cover_title']),
    ],[
    Paragraph('정부지원사업 맞춤 매칭 리포트', ST['cover_sub']),
    ],[
    Paragraph('2026. 05. 01  |  의류제조업 (택티컬 전문)  |  서울 성동구', ST['cover_date']),
]], colWidths=[180*mm])
cover.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), NAVY),
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
]))
story += [cover, Spacer(1,6*mm)]

# ══ 2. 기업 프로파일 ═══════════════════════════════════════
story.append(Paragraph('기업 프로파일', ST['h1']))
pdata = [
    ['항목','내용'],
    ['기업명','(주)토브더가먼트메이커'],
    ['업종','의류제조업 (택티컬·기능성 의류 전문)'],
    ['연 매출','40억 원 (2025년)'],
    ['직원 수','8명 (소기업)'],
    ['업력','약 9년차 (2017년 설립)'],
    ['소재지','서울 성동구 (성수동 패션클러스터 인근)'],
    ['수혜 이력','없음 — 최초 신청 (신규 가점 활용 가능)'],
    ['희망 분야','자금 / 수출 / R&D'],
    ['특이사항','중진공 정책자금 신청 불가 (별도 자금 경로 설계 필요)'],
]
pt = Table(pdata, colWidths=[42*mm, 138*mm])
pt.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,0),  NAVY),
    ('TEXTCOLOR',     (0,0),(-1,0),  WHITE),
    ('BACKGROUND',    (0,1),(0,-1),  LTBLUE),
    ('ROWBACKGROUNDS',(1,1),(-1,-1), [WHITE,GRAY]),
    ('FONTNAME',      (0,0),(-1,-1), 'KR'),
    ('FONTSIZE',      (0,0),(-1,-1), 8.5),
    ('GRID',          (0,0),(-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ('TEXTCOLOR',     (0,9),(-1,9),  colors.HexColor('#C00000')),
]))
story += [pt, Spacer(1,5*mm)]

# ══ 3. 추천 지원사업 Top 7 (단순 행 레이아웃) ═══════════════
story.append(Paragraph('추천 지원사업 Top 7', ST['h1']))

programs = [
    (1, '수출바우처 사업 (수출지원기반활용사업) 2차',
     '중기부 / 중진공', '최대 5,000만원', GREEN, '상',
     '의류·소비재 포함. 바이어발굴·전시회·디지털마케팅 등 14개 메뉴 자유 선택. 2차 모집 5~6월 예정'),
    (2, '내수기업 수출기업화 사업 (산업부 바우처)',
     '산업통상자원부', '최대 3,000만원', GREEN, '상',
     '수출 0 기업 우선. 수출컨설팅·시장조사·인증·온라인마케팅 지원. 상시 모집'),
    (3, '성동구 중소기업육성기금 융자',
     '성동구청 / 기업은행', '제조업 최대 1억원', GREEN, '상',
     '연 1.5% 고정금리. 성동구 소재 제조업 우대. 2026년 상반기 70억 규모 공고 완료'),
    (4, '서울시 중소기업육성자금 융자',
     '서울시 / 서울신용보증재단', '최대 1억원', GREEN, '상',
     '연 2%대. 서울 소재 중소기업 상시 신청. 제조업 가점'),
    (5, '신용보증기금 (KODIT) 일반보증',
     '신용보증기금', '최대 8억원 (보증)', ORANGE, '중',
     '보증비율 85%, 보증료 0.5~2.0%. 담보 부족 기업 금융접근성 확대. 은행 대출 연계'),
    (6, '기술보증기금 (KIBO) 기술보증',
     '기술보증기금', '최대 10억원 (보증)', ORANGE, '중',
     '택티컬 소재 기술 보유 시 기술성 평가로 우대보증 가능. 보증료 0.5~3.0%'),
    (7, '중소기업 기술혁신개발사업 (R&D)',
     '중기부 / TIPA', '최대 1.5억원', ORANGE, '중',
     '기능성·택티컬 소재 R&D. 하반기 2차 공고 예정. 기업부설연구소 선행 권고'),
]

# 헤더 행
hdr = Table([['순위','사업명','주관기관','지원규모','적합']],
            colWidths=[12*mm,72*mm,38*mm,28*mm,14*mm])
hdr.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), NAVY),
    ('TEXTCOLOR',     (0,0),(-1,-1), WHITE),
    ('FONTNAME',      (0,0),(-1,-1), 'KR'),
    ('FONTSIZE',      (0,0),(-1,-1), 8.5),
    ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
]))
story.append(hdr)

for rank, name, org, amt, color, fit, desc in programs:
    # 메인 행
    row = Table([[
        Paragraph(str(rank), ST['rank']),
        Paragraph(f'<b>{name}</b>', ST['prog']),
        Paragraph(org, ST['desc']),
        Paragraph(amt, ST['amt']),
        Paragraph(fit, ST['tag_g'] if color==GREEN else ST['tag_o']),
    ]], colWidths=[12*mm,72*mm,38*mm,28*mm,14*mm])
    row.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(0,0),  color),
        ('BACKGROUND',    (4,0),(4,0),  color),
        ('BACKGROUND',    (1,0),(3,0),  WHITE),
        ('FONTNAME',      (0,0),(-1,-1), 'KR'),
        ('FONTSIZE',      (0,0),(-1,-1), 8.5),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 5),
        ('BOX',           (0,0),(-1,-1), 0.4, colors.HexColor('#CCCCCC')),
        ('LINEBELOW',     (0,0),(-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ]))
    # 설명 행
    desc_row = Table([[
        Paragraph('', ST['desc']),
        Paragraph(f'  ▶ {desc}', ST['desc']),
    ]], colWidths=[12*mm, 152*mm])
    desc_row.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), GRAY),
        ('FONTNAME',      (0,0),(-1,-1), 'KR'),
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (1,0),(1,0),   8),
        ('LINEBELOW',     (0,0),(-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ]))
    story += [row, desc_row]

story.append(Spacer(1,5*mm))

# ══ 4. 매칭 현황 상세표 ══════════════════════════════════════
story.append(Paragraph('지원가능 사업 전체 매칭 현황', ST['h1']))
mdata = [
    ['사업명','주관기관','지원규모','마감','적합도'],
    ['수출바우처 2차','중기부/중진공','최대 5,000만원','5~6월 예정','상'],
    ['내수기업 수출기업화','산업부','최대 3,000만원','상시','상'],
    ['성동구 육성기금','성동구/기업은행','최대 1억원','상시','상'],
    ['서울시 육성자금','서울시/신보','최대 1억원','상시','상'],
    ['신용보증기금 보증','KODIT','최대 8억원(보증)','상시','중'],
    ['기술보증기금 보증','KIBO','최대 10억원(보증)','상시','중'],
    ['기술혁신개발(R&D)','중기부/TIPA','최대 1.5억원','하반기 예정','중'],
]
fit_colors = {'상': GREEN, '중': ORANGE}
mt = Table(mdata, colWidths=[52*mm,35*mm,35*mm,28*mm,16*mm])
ms = [
    ('BACKGROUND',    (0,0),(-1,0),  NAVY),
    ('TEXTCOLOR',     (0,0),(-1,0),  WHITE),
    ('FONTNAME',      (0,0),(-1,-1), 'KR'),
    ('FONTSIZE',      (0,0),(-1,-1), 8),
    ('GRID',          (0,0),(-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING',   (0,0),(-1,-1), 6),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [WHITE,GRAY]),
    ('ALIGN',         (2,0),(-1,-1), 'CENTER'),
]
for i, r in enumerate(mdata[1:], 1):
    c = fit_colors.get(r[-1], GRAY)
    ms += [('BACKGROUND',(4,i),(4,i),c),('TEXTCOLOR',(4,i),(4,i),WHITE)]
mt.setStyle(TableStyle(ms))
story += [mt, Spacer(1,5*mm)]

# ══ 5. 버블차트 (우선순위 매트릭스) ═══════════════════════════
story.append(Paragraph('우선순위 매트릭스', ST['h1']))
fig, ax = plt.subplots(figsize=(8,4))
fig.patch.set_facecolor('#F8FBFF')
ax.set_facecolor('#F8FBFF')
bubbles = [
    ('수출바우처',     1.5, 9.2, 500, '#00B050'),
    ('내수기업수출기업화',1.2, 8.5, 300, '#00B050'),
    ('성동구육성기금', 1.0, 8.0, 100, '#00B050'),
    ('서울시육성자금', 1.2, 7.8, 100, '#00B050'),
    ('신용보증',       2.0, 7.5, 800, '#FF8C00'),
    ('기술보증',       3.0, 7.2, 1000,'#FF8C00'),
    ('기술혁신개발',   6.0, 8.5, 150, '#FF8C00'),
]
for name,x,y,sz,c in bubbles:
    ax.scatter(x,y,s=sz*1.8,color=c,alpha=0.75,edgecolors='white',linewidths=1.5)
    ax.annotate(name,(x,y),textcoords='offset points',xytext=(0,10),
                ha='center',fontsize=7.5,color='#333333')
ax.set_xlim(0,10); ax.set_ylim(6.5,10.5)
ax.set_xlabel('신청 난이도 →',fontsize=9,color='#555555')
ax.set_ylabel('기대 효과 →',fontsize=9,color='#555555')
ax.set_title('신청 난이도 vs 기대 효과  (버블 크기 = 지원 규모)',fontsize=10,color='#1F4E79',pad=8)
ax.axvline(5,color='#CCCCCC',linestyle='--',linewidth=0.8)
ax.axhline(8,color='#CCCCCC',linestyle='--',linewidth=0.8)
ax.text(1,10.3,'즉시 신청',fontsize=8,color='#00B050',style='italic')
ax.text(6,10.3,'준비 후 신청',fontsize=8,color='#FF8C00',style='italic')
patches = [mpatches.Patch(color='#00B050',label='적합도 상'),
           mpatches.Patch(color='#FF8C00',label='적합도 중')]
ax.legend(handles=patches,loc='lower right',fontsize=8)
ax.grid(True,alpha=0.3)
buf1=io.BytesIO(); fig.savefig(buf1,format='png',dpi=130,bbox_inches='tight'); buf1.seek(0); plt.close()
story += [RLImage(buf1,width=170*mm,height=82*mm), Spacer(1,5*mm)]

# ══ 6. 타임라인 간트차트 ═══════════════════════════════════
story.append(Paragraph('2026년 신청 타임라인', ST['h1']))
fig2, ax2 = plt.subplots(figsize=(8,3.5))
fig2.patch.set_facecolor('#F8FBFF'); ax2.set_facecolor('#F8FBFF')
tasks = [
    ('성동구 육성기금',     5,1,'#00B050'),
    ('서울시 육성자금',     5,2,'#00B050'),
    ('내수기업 수출기업화', 5,2,'#00B050'),
    ('수출바우처 2차',      6,1,'#00B050'),
    ('신용보증/기술보증',   5,4,'#FF8C00'),
    ('기술혁신개발(R&D)',   9,2,'#FF8C00'),
]
months=['5월','6월','7월','8월','9월','10월','11월','12월']
for i,(name,start,dur,c) in enumerate(tasks):
    ax2.barh(i,dur,left=start-1,color=c,alpha=0.8,height=0.55,edgecolor='white')
    ax2.text(start-1+dur+0.1,i,name,va='center',fontsize=8,color='#333333')
ax2.set_xticks(range(8)); ax2.set_xticklabels(months,fontsize=8)
ax2.set_yticks(range(len(tasks))); ax2.set_yticklabels([t[0] for t in tasks],fontsize=8)
ax2.set_title('월별 신청·진행 일정 (2026년)',fontsize=10,color='#1F4E79',pad=8)
ax2.set_xlim(-0.5,10); ax2.grid(axis='x',alpha=0.3); ax2.invert_yaxis()
buf2=io.BytesIO(); fig2.savefig(buf2,format='png',dpi=130,bbox_inches='tight'); buf2.seek(0); plt.close()
story += [RLImage(buf2,width=170*mm,height=80*mm), Spacer(1,5*mm)]

# ══ 7. 제안서 초안 (수출바우처) ════════════════════════════
story.append(Paragraph('1순위 제안서 초안 — 수출바우처 사업', ST['h1']))
for title, content in [
    ('사업 참여 필요성',
     '국내 택티컬 의류 시장이 포화 단계에 진입하는 반면, 글로벌 밀리터리·아웃도어 시장은 연 7~12% 성장 중이다. '
     '9년간 내수에서 쌓은 제조 전문성과 고기능성 소재 가공 기술을 보유하고 있으나 '
     '수출 채널과 해외 마케팅 인프라가 전무하다. 수출바우처를 활용해 바이어 발굴·전시회 참가·디지털 마케팅에 '
     '집중 투자하여 첫 수출 성과(50만 달러)를 조기 달성한다.'),
    ('추진 계획 (3단계)',
     '1단계(1~2개월): 영문 카탈로그·온라인 쇼룸 제작, 수출 인증 검토 | '
     '2단계(3~5개월): KOTRA·무역협회 활용 미국·유럽 바이어 매칭 5개사, B2B 마케팅 실행 | '
     '3단계(6~10개월): 유럽 ISPO 또는 미국 SHOT Show 참가, 첫 FOB 계약 1건 이상 체결'),
    ('기대 효과',
     '수출액 5억원 이상 달성(1년) · 해외 바이어 5개사 계약 · 수출 비중 매출의 10% 이상 · '
     '수출 실적 기반 2027년 이노비즈·벤처인증 연계 · 국내 경기 의존도 분산'),
]:
    story.append(Paragraph(title, ST['h2']))
    story.append(Paragraph(content, ST['body']))
    story.append(Spacer(1,3*mm))

# ══ 8. 예상 총 수혜 규모 ════════════════════════════════════
story.append(Paragraph('예상 총 수혜 규모', ST['h2']))
tdata = [
    ['사업명','예상 수혜액','성격'],
    ['수출바우처 + 내수기업 수출기업화','5,000만~8,000만원','비융자'],
    ['성동구 + 서울시 육성자금','1억~2억원','저금리 융자'],
    ['신용보증/기술보증 연계 대출','3억~10억원','보증 연계'],
    ['R&D 기술혁신개발','1억~1.5억원','비융자'],
    ['합  계','약 4.5억~22억원+','복합'],
]
tt = Table(tdata, colWidths=[72*mm,56*mm,36*mm])
ts = [
    ('BACKGROUND',    (0,0),(-1,0),  NAVY),
    ('TEXTCOLOR',     (0,0),(-1,0),  WHITE),
    ('BACKGROUND',    (0,-1),(-1,-1),LTBLUE),
    ('FONTNAME',      (0,0),(-1,-1), 'KR'),
    ('FONTSIZE',      (0,0),(-1,-1), 8.5),
    ('GRID',          (0,0),(-1,-1), 0.4, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ('ROWBACKGROUNDS',(0,1),(-1,-2), [WHITE,GRAY]),
]
tt.setStyle(TableStyle(ts))
story += [tt, Spacer(1,4*mm)]

story.append(Paragraph(
    '본 리포트는 히어컴퍼니 정부지원사업팀이 2026-05-01 기준 공개 공고를 바탕으로 작성하였습니다. '
    '실제 신청 전 최신 공고문을 반드시 재확인하시기 바랍니다.  |  히어컴퍼니 대표상담 1:1 문의',
    ST['small']))

doc.build(story)
print(f'PDF generated: {OUT}')
