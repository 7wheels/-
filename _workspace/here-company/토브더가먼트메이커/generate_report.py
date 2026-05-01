import io
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

FONT = '/tmp/NanumGothic.ttf'
pdfmetrics.registerFont(TTFont('KR', FONT))
fm.fontManager.addfont(FONT)
plt.rcParams['font.family'] = fm.FontProperties(fname=FONT).get_name()
plt.rcParams['axes.unicode_minus'] = False

NAVY   = colors.HexColor('#1F4E79')
BLUE   = colors.HexColor('#2E75B6')
LTBLUE = colors.HexColor('#DEEAF1')
GREEN  = colors.HexColor('#00B050')
ORANGE = colors.HexColor('#FF8C00')
WHITE  = colors.white
GRAY   = colors.HexColor('#F5F5F5')
DGRAY  = colors.HexColor('#555555')
RED    = colors.HexColor('#C00000')

def S(name, **kw):
    return ParagraphStyle(name, fontName='KR', **kw)

ST = {
    'cl': S('cl', fontSize=9,  textColor=LTBLUE, alignment=1),
    'ct': S('ct', fontSize=22, textColor=WHITE, leading=28, alignment=1),
    'cs': S('cs', fontSize=12, textColor=LTBLUE, leading=17, alignment=1),
    'cd': S('cd', fontSize=8.5,textColor=colors.HexColor('#BDD7EE'), alignment=1, spaceBefore=4),
    'h1': S('h1', fontSize=13, textColor=NAVY, leading=17, spaceBefore=8, spaceAfter=3),
    'h2': S('h2', fontSize=10, textColor=BLUE, leading=14, spaceBefore=5, spaceAfter=2),
    'h3': S('h3', fontSize=9,  textColor=NAVY, leading=13, spaceBefore=4, spaceAfter=1),
    'bd': S('bd', fontSize=8.5,textColor=colors.black, leading=14),
    'sm': S('sm', fontSize=7.5,textColor=DGRAY, leading=12),
    'rk': S('rk', fontSize=10, textColor=WHITE, leading=13, alignment=1),
    'pr': S('pr', fontSize=9.5,textColor=NAVY, leading=13),
    'am': S('am', fontSize=9,  textColor=GREEN, leading=12, alignment=2),
    'dc': S('dc', fontSize=7.5,textColor=DGRAY, leading=11),
    'lk': S('lk', fontSize=7.5,textColor=BLUE,  leading=11),
    'tg': S('tg', fontSize=8.5,textColor=WHITE, leading=12, alignment=1),
    'rd': S('rd', fontSize=8,  textColor=RED,   leading=12),
}

OUT = '/home/user/-/_workspace/here-company/토브더가먼트메이커/토브더가먼트메이커_정부지원사업리포트_20260501.pdf'
doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
story = []

# ══ 1. 표지 ══
cover = Table([[Paragraph('히어컴퍼니 정부지원사업 리포트', ST['cl'])],
               [Paragraph('(주)토브더가먼트메이커', ST['ct'])],
               [Paragraph('정부지원사업 맞춤 매칭 리포트 v3', ST['cs'])],
               [Paragraph('2026. 05. 01  |  의류제조업 택티컬 전문  |  서울 성동구', ST['cd'])]],
              colWidths=[180*mm])
cover.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
    ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story += [cover, Spacer(1,5*mm)]

# ══ 2. 기업 프로파일 ══
story.append(Paragraph('기업 프로파일', ST['h1']))
pdata = [['항목','내용'],
    ['기업명','(주)토브더가먼트메이커'],
    ['업종','의류제조업 (택티컬·기능성 의류 전문)'],
    ['연 매출','40억 원 (2025년)'],
    ['직원 수','8명 (소기업)'],
    ['업력','약 9년차 (2017년 설립)'],
    ['소재지','서울 성동구 (성수동 패션클러스터 인근)'],
    ['수혜 이력','없음 — 최초 신청 (신규 가점 활용 가능)'],
    ['자금 제한','중진공 신청 불가 / 기보 한도 소진 — 별도 자금 에이전트 이관'],
    ['희망 분야','수출 확대 / R&D / 자금'],
]
pt = Table(pdata, colWidths=[42*mm,138*mm])
pt.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('BACKGROUND',(0,1),(0,-1),LTBLUE),
    ('ROWBACKGROUNDS',(1,1),(-1,-1),[WHITE,GRAY]),
    ('FONTNAME',(0,0),(-1,-1),'KR'),('FONTSIZE',(0,0),(-1,-1),8.5),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),8),
    ('TEXTCOLOR',(0,8),(-1,8),RED),
]))
story += [pt, Spacer(1,5*mm)]

# ══ 3. 비융자 정부지원사업 Top 5 ══
story.append(Paragraph('비융자 정부지원사업 Top 5  (보조금·바우처·R&D 과제)', ST['h1']))
story.append(Paragraph(
    '갚지 않아도 되는 지원만 선별합니다. 정책자금(융자·보증)은 하단 자금 에이전트 이관 항목을 참고하세요.',
    ST['sm']))
story.append(Spacer(1,3*mm))

programs = [
    (1, '수출바우처 사업 2차 (수출지원기반활용사업)',
     '중기부 / 중진공', '실수혜 1,500~3,000만원', GREEN, '상',
     '의류·소비재 포함. 바이어발굴·전시회·디지털마케팅 등 14개 메뉴. 2차 모집 5~6월 예정',
     'https://www.exportvoucher.com/portal/board/boardList?bbs_id=1'),
    (2, '내수기업 수출기업화 사업 (산업부 바우처)',
     '산업통상자원부', '실수혜 500~1,500만원', GREEN, '상',
     '수출 0 기업 우선. 수출컨설팅·시장조사·인증·홍보물. 상시 신청 가능',
     'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/7/view.do?pblancId=PBLN_000000000117116'),
    (3, '성동구 중소기업육성기금 (저금리 융자)',
     '성동구청 / 기업은행', '제조업 최대 1억원 (연 1.5%)', ORANGE, '상',
     '성동구 소재 제조업 우대. 2026 상반기 70억 규모 공고. 저금리 융자로 자금 에이전트 조율 권고',
     'https://www.sijung.co.kr/news/articleView.html?idxno=425280'),
    (4, '서울시 중소기업육성자금 (저금리 융자)',
     '서울시 / 서울신용보증재단', '최대 1억원 (연 2%대)', ORANGE, '상',
     '서울 소재 상시 신청. 제조업 가점. 저금리 융자로 자금 에이전트 조율 권고',
     'https://news.seoul.go.kr/economy/rearing-funds'),
    (5, '중소기업 기술혁신개발사업 (R&D 과제)',
     '중기부 / TIPA', '실수혜 6,500~9,750만원 (65~75%)', GREEN, '중',
     '기능성·택티컬 소재 R&D 주제 설정. 하반기 2차 공고. 기업부설연구소 선행 권고 (2~3개월)',
     'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/view.do?pblancId=PBLN_000000000116943'),
]

# 헤더
hdr = Table([['순위','사업명 / 주관기관','지원규모','적합']],
            colWidths=[12*mm,104*mm,42*mm,14*mm])
hdr.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),NAVY),('TEXTCOLOR',(0,0),(-1,-1),WHITE),
    ('FONTNAME',(0,0),(-1,-1),'KR'),('FONTSIZE',(0,0),(-1,-1),8.5),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(hdr)

for rank, name, org, amt, color, fit, desc, link in programs:
    row = Table([[
        Paragraph(str(rank), ST['rk']),
        Paragraph(f'<b>{name}</b><br/><font size="7.5" color="#555555">{org}</font>', ST['pr']),
        Paragraph(amt, ST['am']),
        Paragraph(fit, ST['tg']),
    ]], colWidths=[12*mm,104*mm,42*mm,14*mm])
    row.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0),color),('BACKGROUND',(3,0),(3,0),color),
        ('BACKGROUND',(1,0),(2,0),WHITE),
        ('FONTNAME',(0,0),(-1,-1),'KR'),('FONTSIZE',(0,0),(-1,-1),8.5),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),5),
        ('BOX',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ]))
    desc_row = Table([[
        Paragraph('', ST['dc']),
        Paragraph(f'  ▶ {desc}', ST['dc']),
        Paragraph(f'공고 바로가기 >', ST['lk']),
        Paragraph('', ST['dc']),
    ]], colWidths=[12*mm,100*mm,46*mm,14*mm])
    desc_row.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),GRAY),
        ('FONTNAME',(0,0),(-1,-1),'KR'),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LEFTPADDING',(1,0),(1,0),8),
        ('LINEBELOW',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ]))
    story += [row, desc_row]

story.append(Spacer(1,4*mm))

# ══ 4. 전체 매칭표 ══
story.append(Paragraph('지원가능 사업 전체 매칭 현황', ST['h1']))
mdata = [['사업명','주관','지원규모(실수혜)','마감','성격','적합'],
    ['수출바우처 2차','중기부/중진공','1,500~3,000만원','5~6월','비융자','상'],
    ['내수기업 수출기업화','산업부','500~1,500만원','상시','비융자','상'],
    ['성동구 육성기금','성동구','최대 1억 / 연1.5%','상시','저금리융자','상'],
    ['서울시 육성자금','서울시/신보','최대 1억 / 연2%','상시','저금리융자','상'],
    ['기술혁신개발(R&D)','중기부/TIPA','6,500~9,750만원','하반기','비융자','중'],
    ['신용보증기금 보증','KODIT','→ 자금 에이전트 이관','상시','보증','검토'],
]
fit_c = {'상':GREEN,'중':ORANGE,'검토':colors.HexColor('#999999')}
mt = Table(mdata, colWidths=[48*mm,28*mm,38*mm,22*mm,22*mm,14*mm])
ms = [
    ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,-1),'KR'),('FONTSIZE',(0,0),(-1,-1),7.5),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),5),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,GRAY]),
    ('ALIGN',(2,0),(-1,-1),'CENTER'),
    ('TEXTCOLOR',(0,7),(-1,7),colors.HexColor('#888888')),
]
for i,r in enumerate(mdata[1:],1):
    c = fit_c.get(r[-1],GRAY)
    ms += [('BACKGROUND',(5,i),(5,i),c),('TEXTCOLOR',(5,i),(5,i),WHITE)]
mt.setStyle(TableStyle(ms))
story += [mt, Spacer(1,4*mm)]

# ══ 5. 버블차트 ══
story.append(Paragraph('우선순위 매트릭스 (비융자 중심)', ST['h1']))
fig,ax = plt.subplots(figsize=(8,4))
fig.patch.set_facecolor('#F8FBFF'); ax.set_facecolor('#F8FBFF')
bubbles = [
    ('수출바우처',       1.2,9.2,250,'#00B050'),
    ('내수기업수출기업화',1.0,8.4,100,'#00B050'),
    ('성동구육성기금',   1.5,8.0,100,'#FF8C00'),
    ('서울시육성자금',   1.5,7.7,100,'#FF8C00'),
    ('기술혁신개발R&D',  6.0,8.6,150,'#00B050'),
]
for name,x,y,sz,c in bubbles:
    ax.scatter(x,y,s=sz*2,color=c,alpha=0.8,edgecolors='white',linewidths=1.5)
    ax.annotate(name,(x,y),textcoords='offset points',xytext=(0,10),
                ha='center',fontsize=7.5,color='#333333')
ax.set_xlim(0,10); ax.set_ylim(6.5,10.5)
ax.set_xlabel('신청 난이도 →',fontsize=9,color='#555555')
ax.set_ylabel('기대 효과 →',fontsize=9,color='#555555')
ax.set_title('신청 난이도 vs 기대 효과  (비융자·저금리 분류)',fontsize=10,color='#1F4E79',pad=8)
ax.axvline(5,color='#CCCCCC',linestyle='--',linewidth=0.8)
ax.text(1,10.3,'즉시 신청',fontsize=8,color='#00B050',style='italic')
ax.text(6,10.3,'준비 후 신청',fontsize=8,color='#00B050',style='italic')
ax.text(1,6.65,'● 비융자',fontsize=8,color='#00B050')
ax.text(2.5,6.65,'● 저금리융자',fontsize=8,color='#FF8C00')
ax.grid(True,alpha=0.3)
buf1=io.BytesIO(); fig.savefig(buf1,format='png',dpi=130,bbox_inches='tight'); buf1.seek(0); plt.close()
story += [RLImage(buf1,width=170*mm,height=80*mm), Spacer(1,4*mm)]

# ══ 6. 타임라인 ══
story.append(Paragraph('2026년 신청 타임라인', ST['h1']))
fig2,ax2 = plt.subplots(figsize=(8,3))
fig2.patch.set_facecolor('#F8FBFF'); ax2.set_facecolor('#F8FBFF')
tasks = [
    ('성동구 육성기금 상담',   5,1,'#00B050'),
    ('서울시 육성자금 신청',   5,2,'#00B050'),
    ('내수기업 수출기업화',    5,2,'#00B050'),
    ('수출바우처 2차 신청',    6,1,'#00B050'),
    ('R&D 연구소 설립 준비',  5,3,'#2E75B6'),
    ('기술혁신개발 신청',      9,2,'#FF8C00'),
]
months=['5월','6월','7월','8월','9월','10월','11월','12월']
for i,(name,start,dur,c) in enumerate(tasks):
    ax2.barh(i,dur,left=start-1,color=c,alpha=0.8,height=0.55,edgecolor='white')
    ax2.text(start-1+dur+0.1,i,name,va='center',fontsize=8,color='#333333')
ax2.set_xticks(range(8)); ax2.set_xticklabels(months,fontsize=8)
ax2.set_yticks(range(len(tasks))); ax2.set_yticklabels([t[0] for t in tasks],fontsize=8)
ax2.set_title('월별 신청 일정',fontsize=10,color='#1F4E79',pad=8)
ax2.set_xlim(-0.5,10); ax2.grid(axis='x',alpha=0.3); ax2.invert_yaxis()
buf2=io.BytesIO(); fig2.savefig(buf2,format='png',dpi=130,bbox_inches='tight'); buf2.seek(0); plt.close()
story += [RLImage(buf2,width=170*mm,height=75*mm), Spacer(1,4*mm)]

# ══ 7. 예상 수혜 규모 (보수적) ══
story.append(Paragraph('예상 수혜 규모 (보수적 산정)', ST['h1']))
story.append(Paragraph(
    '최대치가 아닌 실제 평균 선정 규모 기준. 미선정 리스크 반영.',
    ST['sm']))
story.append(Spacer(1,2*mm))
tdata = [['사업명','보수적 예상 수혜','성격','신청 시기'],
    ['수출바우처 2차','1,500~3,000만원','비융자 (갚지 않음)','5~6월'],
    ['내수기업 수출기업화','500~1,500만원','비융자 (갚지 않음)','즉시'],
    ['성동구 + 서울시 융자','5,000만~1억원','저금리 융자 (상환)','즉시'],
    ['기술혁신개발 R&D','6,500~9,750만원','비융자 (갚지 않음)','하반기'],
    ['합  계 (비융자만)','약 2,000만~1.4억원','비융자 합산','—'],
    ['합  계 (융자 포함)','약 7,000만~2.5억원','전체 합산','—'],
]
tt = Table(tdata, colWidths=[55*mm,45*mm,38*mm,26*mm])
ts = [
    ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('BACKGROUND',(0,5),(-1,5),LTBLUE),
    ('BACKGROUND',(0,6),(-1,6),colors.HexColor('#EBF3FB')),
    ('FONTNAME',(0,0),(-1,-1),'KR'),('FONTSIZE',(0,0),(-1,-1),8.5),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),8),
    ('ROWBACKGROUNDS',(0,1),(-1,4),[WHITE,GRAY]),
]
tt.setStyle(TableStyle(ts))
story += [tt, Spacer(1,4*mm)]

# ══ 8. 자금 에이전트 이관 박스 ══
story.append(Paragraph('정책자금 이관 — 자금 에이전트 담당', ST['h1']))
fa_data = [['이관 항목','이유','자금 에이전트 검토 방향'],
    ['기보 (KIBO) 추가 보증','현재 한도 소진','타 보증기관 또는 대환 구조 검토'],
    ['신용보증기금 (KODIT)','중진공 불가 공백 대체','KODIT 신규 보증 한도 가능 여부 진단'],
    ['IBK·KDB 등 정책금융','보증 연계 대출','보증서 활용 은행 대출 포트폴리오 재설계'],
]
ft = Table(fa_data, colWidths=[45*mm,45*mm,75*mm])
ft.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#4472C4')),
    ('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,-1),'KR'),('FONTSIZE',(0,0),(-1,-1),8),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),7),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EEF3FB'),WHITE]),
    ('BOX',(0,0),(-1,-1),1,colors.HexColor('#4472C4')),
]))
story += [ft, Spacer(1,4*mm)]

# ══ 9. 제안서 초안 ══
story.append(Paragraph('1순위 제안서 초안 — 수출바우처 사업', ST['h1']))
story.append(Paragraph(
    '공고 바로가기: www.exportvoucher.com → 공지사항 → 2026년 2차 모집공고', ST['lk']))
story.append(Spacer(1,2*mm))
for title, content in [
    ('사업 참여 필요성',
     '글로벌 밀리터리·아웃도어 시장은 연 7~12% 성장 중이며, 국내 택티컬 의류 제조 경쟁력은 이미 세계 수준이다. '
     '9년간 내수 시장에서 검증된 제조 역량과 고기능성 소재 가공 기술을 보유하고 있으나, '
     '수출 채널과 해외 바이어 네트워크가 전무하다. 수출바우처를 통해 '
     '초기 수출 인프라(영문카탈로그·바이어발굴·전시회)를 단기 구축하여 첫 수출 성과를 조기 달성한다.'),
    ('3단계 추진 계획',
     '1단계(1~2개월): 영문 카탈로그·수출용 홈페이지 제작, CE/UL 인증 검토 | '
     '2단계(3~5개월): KOTRA 해외지사 활용 미국·유럽 바이어 5개사 매칭, B2B 플랫폼 등록 | '
     '3단계(6~10개월): 유럽 ISPO 전시회 참가, 첫 FOB 계약 1건 이상 체결'),
    ('기대 효과',
     '수출액 2억원 이상 달성(1년, 보수적) · 해외 바이어 3개사 계약 · '
     '수출 실적 확보 후 2027년 이노비즈·벤처인증 연계 · 국내 매출 의존도 분산'),
]:
    story.append(Paragraph(title, ST['h2']))
    story.append(Paragraph(content, ST['bd']))
    story.append(Spacer(1,3*mm))

story.append(Spacer(1,3*mm))
story.append(Paragraph(
    '본 리포트는 히어컴퍼니 정부지원사업팀이 2026-05-01 기준 공개 공고를 바탕으로 작성하였습니다. '
    '실제 신청 전 각 기관 공고문을 반드시 재확인하시기 바랍니다.  |  정책자금 상담은 자금 에이전트에게 이관합니다.',
    ST['sm']))

doc.build(story)
print(f'PDF generated: {OUT}')
