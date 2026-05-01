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
RED2   = colors.HexColor('#C00000')
URGENT = colors.HexColor('#FF4444')
WHITE  = colors.white
GRAY   = colors.HexColor('#F5F5F5')
DGRAY  = colors.HexColor('#555555')

def S(name, **kw):
    return ParagraphStyle(name, fontName='KR', **kw)

ST = {
    'cl': S('cl', fontSize=9,  textColor=LTBLUE,  alignment=1),
    'ct': S('ct', fontSize=22, textColor=WHITE,   leading=28, alignment=1),
    'cs': S('cs', fontSize=12, textColor=LTBLUE,  leading=17, alignment=1),
    'cd': S('cd', fontSize=8.5,textColor=colors.HexColor('#BDD7EE'), alignment=1, spaceBefore=4),
    'h1': S('h1', fontSize=13, textColor=NAVY,    leading=17, spaceBefore=8, spaceAfter=3),
    'h2': S('h2', fontSize=10, textColor=BLUE,    leading=14, spaceBefore=5, spaceAfter=2),
    'bd': S('bd', fontSize=8.5,textColor=colors.black, leading=14),
    'sm': S('sm', fontSize=7.5,textColor=DGRAY,   leading=12),
    'ug': S('ug', fontSize=8,  textColor=URGENT,  leading=12),
    'rk': S('rk', fontSize=10, textColor=WHITE,   leading=13, alignment=1),
    'pr': S('pr', fontSize=9.5,textColor=NAVY,    leading=13),
    'am': S('am', fontSize=9,  textColor=GREEN,   leading=12, alignment=2),
    'dc': S('dc', fontSize=7.5,textColor=DGRAY,   leading=11),
    'lk': S('lk', fontSize=7.5,textColor=BLUE,    leading=11),
    'tg': S('tg', fontSize=8.5,textColor=WHITE,   leading=12, alignment=1),
    'rd': S('rd', fontSize=8,  textColor=RED2,    leading=12),
}

OUT = '/home/user/-/_workspace/here-company/로지스존/로지스존_정부지원사업리포트_20260501.pdf'
doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
story = []

# ══ 1. 표지 ══
cover = Table([
    [Paragraph('히어컴퍼니 정부지원사업 리포트', ST['cl'])],
    [Paragraph('(주)로지스존', ST['ct'])],
    [Paragraph('정부지원사업 맞춤 매칭 리포트', ST['cs'])],
    [Paragraph('2026. 05. 01  |  물류·창고업  |  경기도 군포시', ST['cd'])],
], colWidths=[180*mm])
cover.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
    ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story += [cover, Spacer(1,5*mm)]

# ══ 2. 기업 프로파일 ══
story.append(Paragraph('기업 프로파일', ST['h1']))
pdata = [['항목','내용'],
    ['기업명','(주)로지스존'],
    ['업종','물류·창고업 (3PL·물류 솔루션)'],
    ['연 매출','40억 원 (2025년)'],
    ['직원 수','24명 (소기업)'],
    ['업력','11년차 (2015년 설립)'],
    ['소재지','경기도 군포시'],
    ['수혜 이력','없음 — 최초 신청 (신규 가점 활용 가능)'],
    ['자금 현황','중진공 2억 이용 중 / 신보 한도 소진 / 시중은행 2억'],
    ['제한 항목','신보(KODIT) 한도 소진 → 제외  |  기보(KIBO) 미이용 → 자금팀 검토'],
    ['핵심 니즈','물류 자동화·WMS 시스템개발 / 창고 공간 확보 / 거래처·마케팅'],
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
    ('TEXTCOLOR',(0,9),(-1,9),RED2),
]))
story += [pt, Spacer(1,5*mm)]

# ══ 3. 비융자 정부지원사업 Top 5 ══
story.append(Paragraph('비융자 정부지원사업 Top 5  (보조금·바우처·R&D 과제)', ST['h1']))
story.append(Paragraph(
    '갚지 않아도 되는 지원만 선별. 정책자금·보증은 하단 자금 에이전트 이관 항목을 참고하세요.',
    ST['sm']))
story.append(Spacer(1,3*mm))

programs = [
    (1,'물류 AI기술 도입 지원사업',
     '국토교통부 / 한국교통연구원',
     '실수혜 최대 5,000만원 (50%)',
     GREEN,'상',
     '물류기업 전용 AI 전환 지원. WMS·TMS·AI 최적화 솔루션 구축 비용 50% 지원. 2026년 공고',
     '⚡ 물류기업 최적 매칭',
     'https://www.koti.re.kr/user/bbs/noticeView.do?bbs_no=72729'),
    (2,'중소기업 스마트서비스 지원사업',
     '중기부 / TIPA',
     '신규 최대 5,000만원 (50%)',
     GREEN,'상',
     '서비스업 AI·디지털 전환 솔루션 구축. 물류·공급망 관리 분야 직접 해당. 신청 4/20~5/22',
     '🔴 마감 5월 22일 임박!',
     'https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000120172'),
    (3,'중소기업 마케팅지원사업',
     '중기부 (판판대로)',
     '사업별 무상 지원',
     GREEN,'상',
     '온라인판로·구매상담회·마케팅역량강화. 화주 거래처 확보 직결. 141.7억 규모 연중 운영',
     '거래처 확보 직결',
     'https://bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000117928'),
    (4,'중소기업 기술혁신개발사업 (R&D)',
     '중기부 / TIPA',
     '실수혜 6,500~9,750만원 (65~75%)',
     GREEN,'중',
     '물류시스템(WMS/TMS) 자체 개발 과제. 하반기 2차 공고 예정. 기업부설연구소 선행 권고',
     'R&D 과제로 시스템 자체개발',
     'https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000116943'),
    (5,'경기도 중소기업육성자금 (저금리융자)',
     '경기도 / 경기신용보증재단',
     '최대 5억 / 연 2.9% (이차보전)',
     ORANGE,'상',
     '창고 확장·설비 투자 자금. 1월 19일부터 소진 시까지 상시 신청. g-money.gg.go.kr',
     '창고 확대 자금 연계',
     'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/view.do?pblancId=PBLN_000000000117362'),
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

for rank, name, org, amt, color, fit, desc, badge, link in programs:
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
    badge_color = URGENT if '마감' in badge else (NAVY if '물류' in badge else BLUE)
    desc_row = Table([[
        Paragraph('', ST['dc']),
        Paragraph(f'  ▶ {desc}', ST['dc']),
        Paragraph(f'<link href="{link}">공고 바로가기 &gt;</link>', ST['lk']),
        Paragraph('', ST['dc']),
    ]], colWidths=[12*mm,100*mm,46*mm,14*mm])
    desc_row.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),GRAY),
        ('FONTNAME',(0,0),(-1,-1),'KR'),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LEFTPADDING',(1,0),(1,0),8),
        ('LINEBELOW',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ]))
    # 마감 임박 배지
    if '마감' in badge:
        badge_row = Table([[Paragraph(f'  {badge}', ST['ug'])]],
                         colWidths=[180*mm])
        badge_row.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FFF0F0')),
            ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
            ('LINEBELOW',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
        ]))
        story += [row, desc_row, badge_row]
    else:
        story += [row, desc_row]

story.append(Spacer(1,4*mm))

# ══ 4. 전체 매칭표 ══
story.append(Paragraph('지원가능 사업 전체 매칭 현황', ST['h1']))
mdata = [['사업명','주관','지원규모(실수혜)','마감','성격','적합'],
    ['물류AI기술 도입','국토부/교통연구원','최대 5,000만원','2026년','비융자','상'],
    ['스마트서비스 지원','중기부/TIPA','최대 5,000만원','5/22 마감!','비융자','상'],
    ['마케팅지원사업','중기부','무상 다양','연중','비융자','상'],
    ['기술혁신개발(R&D)','중기부/TIPA','6,500~9,750만원','하반기','비융자','중'],
    ['경기도 육성자금','경기도/경기신보','최대 5억 / 2.9%','상시','저금리융자','상'],
    ['기보(KIBO) 보증','기술보증기금','→ 자금 에이전트 이관','상시','보증','검토'],
]
fit_c = {'상':GREEN,'중':ORANGE,'검토':colors.HexColor('#999999')}
mt = Table(mdata, colWidths=[48*mm,35*mm,35*mm,22*mm,22*mm,14*mm])
ms = [
    ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,-1),'KR'),('FONTSIZE',(0,0),(-1,-1),7.5),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),5),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,GRAY]),
    ('ALIGN',(3,0),(-1,-1),'CENTER'),
    ('TEXTCOLOR',(3,2),(3,2),URGENT),
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
    ('물류AI기술도입',     1.5,9.5,250,'#00B050'),
    ('스마트서비스',       1.2,9.0,250,'#FF4444'),  # 마감 임박 강조
    ('마케팅지원',         1.0,8.0,120,'#00B050'),
    ('기술혁신R&D',        6.0,8.8,200,'#00B050'),
    ('경기도육성자금',     2.0,8.2,500,'#FF8C00'),
]
for name,x,y,sz,c in bubbles:
    ax.scatter(x,y,s=sz*2,color=c,alpha=0.8,edgecolors='white',linewidths=1.5)
    ax.annotate(name,(x,y),textcoords='offset points',xytext=(0,10),
                ha='center',fontsize=7.5,color='#333333')
ax.set_xlim(0,10); ax.set_ylim(7.0,10.8)
ax.set_xlabel('신청 난이도 →',fontsize=9,color='#555555')
ax.set_ylabel('기대 효과 →',fontsize=9,color='#555555')
ax.set_title('신청 난이도 vs 기대 효과  (빨강=마감 임박)',fontsize=10,color='#1F4E79',pad=8)
ax.axvline(5,color='#CCCCCC',linestyle='--',linewidth=0.8)
ax.text(1,10.6,'즉시 신청',fontsize=8,color='#00B050',style='italic')
ax.text(6,10.6,'준비 후 신청',fontsize=8,color='#2E75B6',style='italic')
patches = [mpatches.Patch(color='#00B050',label='비융자'),
           mpatches.Patch(color='#FF8C00',label='저금리융자'),
           mpatches.Patch(color='#FF4444',label='마감임박')]
ax.legend(handles=patches,loc='lower right',fontsize=8)
ax.grid(True,alpha=0.3)
buf1=io.BytesIO(); fig.savefig(buf1,format='png',dpi=130,bbox_inches='tight'); buf1.seek(0); plt.close()
story += [RLImage(buf1,width=170*mm,height=82*mm), Spacer(1,4*mm)]

# ══ 6. 타임라인 ══
story.append(Paragraph('2026년 신청 타임라인', ST['h1']))
fig2,ax2 = plt.subplots(figsize=(8,3))
fig2.patch.set_facecolor('#F8FBFF'); ax2.set_facecolor('#F8FBFF')
tasks = [
    ('스마트서비스 지원 신청',  5,1,'#FF4444'),   # 5월 22일 마감!
    ('마케팅지원사업 신청',     5,2,'#00B050'),
    ('물류AI기술 도입 신청',    5,2,'#00B050'),
    ('경기도 육성자금 신청',    5,3,'#FF8C00'),
    ('기업부설연구소 설립',     5,3,'#2E75B6'),
    ('기술혁신개발(R&D) 신청', 9,2,'#00B050'),
]
months=['5월','6월','7월','8월','9월','10월','11월','12월']
for i,(name,start,dur,c) in enumerate(tasks):
    ax2.barh(i,dur,left=start-1,color=c,alpha=0.85,height=0.55,edgecolor='white')
    ax2.text(start-1+dur+0.1,i,name,va='center',fontsize=8,color='#333333')
ax2.set_xticks(range(8)); ax2.set_xticklabels(months,fontsize=8)
ax2.set_yticks(range(len(tasks))); ax2.set_yticklabels([t[0] for t in tasks],fontsize=8)
ax2.set_title('월별 신청 일정 (빨강 = 즉시 신청 필요)',fontsize=10,color='#1F4E79',pad=8)
ax2.set_xlim(-0.5,10); ax2.grid(axis='x',alpha=0.3); ax2.invert_yaxis()
buf2=io.BytesIO(); fig2.savefig(buf2,format='png',dpi=130,bbox_inches='tight'); buf2.seek(0); plt.close()
story += [RLImage(buf2,width=170*mm,height=75*mm), Spacer(1,4*mm)]

# ══ 7. 예상 수혜 규모 ══
story.append(Paragraph('예상 수혜 규모 (보수적 산정)', ST['h1']))
story.append(Paragraph('최대치가 아닌 실제 평균 선정 규모 기준. 미선정 리스크 반영.', ST['sm']))
story.append(Spacer(1,2*mm))
tdata = [['사업명','보수적 예상 수혜','성격','시기'],
    ['물류AI기술 도입','2,000~5,000만원','비융자','5~6월'],
    ['스마트서비스 지원','1,500~5,000만원','비융자','5월 즉시'],
    ['마케팅지원사업','500~2,000만원 상당','비융자','연중'],
    ['기술혁신개발(R&D)','6,500~9,750만원','비융자','하반기'],
    ['경기도 육성자금','1억~3억원','저금리융자 2.9%','즉시'],
    ['합  계 (비융자만)','약 1억~2.2억원','비융자 합산','—'],
    ['합  계 (융자 포함)','약 2억~5.2억원','전체 합산','—'],
]
tt = Table(tdata, colWidths=[55*mm,50*mm,38*mm,21*mm])
ts = [
    ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('BACKGROUND',(0,6),(-1,6),LTBLUE),
    ('BACKGROUND',(0,7),(-1,7),colors.HexColor('#EBF3FB')),
    ('FONTNAME',(0,0),(-1,-1),'KR'),('FONTSIZE',(0,0),(-1,-1),8.5),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),8),
    ('ROWBACKGROUNDS',(0,1),(-1,5),[WHITE,GRAY]),
    ('TEXTCOLOR',(3,2),(3,2),URGENT),
]
tt.setStyle(TableStyle(ts))
story += [tt, Spacer(1,4*mm)]

# ══ 8. 자금 에이전트 이관 ══
story.append(Paragraph('정책자금 이관 — 자금 에이전트 담당', ST['h1']))
fa_data = [['이관 항목','현황','자금 에이전트 검토 방향'],
    ['기보(KIBO) 기술보증','미이용 → 신규 가능','물류시스템 기술성 평가 후 보증 한도 진단'],
    ['중진공 추가 한도','2억 이용 중','운전·시설자금 추가 한도 여부 상담 권고'],
    ['신보(KODIT) 보증','한도 소진 → 제외','대환·보증기관 교체 가능성 중장기 검토'],
]
ft = Table(fa_data, colWidths=[42*mm,42*mm,80*mm])
ft.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#4472C4')),
    ('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,-1),'KR'),('FONTSIZE',(0,0),(-1,-1),8),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),7),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EEF3FB'),WHITE]),
    ('BOX',(0,0),(-1,-1),1,colors.HexColor('#4472C4')),
    ('TEXTCOLOR',(0,3),(-1,3),RED2),
]))
story += [ft, Spacer(1,4*mm)]

# ══ 9. 1순위 제안서 초안 ══
story.append(Paragraph('1순위 제안서 초안 — 물류 AI기술 도입 지원사업', ST['h1']))
story.append(Paragraph(
    '공고 바로가기: koti.re.kr → 연구원 소식 → 공지사항', ST['lk']))
story.append(Spacer(1,2*mm))
for title, content in [
    ('사업 참여 필요성',
     '국내 물류 시장은 e커머스 급성장에 따라 신속·정확한 재고관리와 배송 최적화 수요가 폭증하고 있다. '
     '(주)로지스존은 11년간 물류·창고 운영으로 현장 노하우를 보유하고 있으나, '
     'AI 기반 입출고 예측·최적 경로 배정·재고 자동화 시스템이 부재하여 처리 속도와 운영 효율에 한계가 있다. '
     '물류AI기술 도입 지원사업을 통해 WMS(창고관리시스템) AI화를 구현하고, '
     '처리 물동량 30% 확대 및 운영 인력 효율 개선을 달성한다.'),
    ('3단계 추진 계획',
     '1단계(1~2개월): AI 기반 WMS 도입 설계, 현행 물류 프로세스 분석 및 구축 사양 확정 | '
     '2단계(3~6개월): AI 입출고 예측 모듈·재고 자동화·배송 경로 최적화 시스템 구축 및 시범 운영 | '
     '3단계(7~10개월): 전체 창고 적용, 고객사 연동 인터페이스 개발, 성과 측정 및 고도화'),
    ('기대 효과',
     '물동량 처리 속도 30% 향상(보수적) · 재고 오류율 80% 감소 · 운영 인건비 15% 절감 · '
     '신규 화주 거래처 3개사 이상 추가 확보 · 2027년 이노비즈 인증 연계'),
]:
    story.append(Paragraph(title, ST['h2']))
    story.append(Paragraph(content, ST['bd']))
    story.append(Spacer(1,3*mm))

story.append(Spacer(1,3*mm))
story.append(Paragraph(
    '본 리포트는 히어컴퍼니 정부지원사업팀이 2026-05-01 기준 공개 공고를 바탕으로 작성하였습니다. '
    '실제 신청 전 각 기관 공고문을 반드시 재확인하시기 바랍니다.  |  정책자금 상담 → 자금 에이전트 이관',
    ST['sm']))

doc.build(story)
print(f'PDF generated: {OUT}')
