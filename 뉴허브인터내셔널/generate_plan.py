"""
(주)뉴허브인터내셔널 — 정책자금 사업계획서 (신용보증재단 보증신청용)
16:9 슬라이드 / 인포그래픽 중심 / 11페이지

작성: 히어컴퍼니 (HearCompany) Corporate Consulting
"""
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pathlib import Path
import datetime

pdfmetrics.registerFont(UnicodeCIDFont('HYGothic-Medium'))
KR = 'HYGothic-Medium'

# ── 색상 팔레트 ───────────────────────────────────────────────────────
NAVY   = colors.HexColor('#1B3A6B')
NAVY2  = colors.HexColor('#0F2340')
BLUE   = colors.HexColor('#2563B0')
LBLUE  = colors.HexColor('#93C5FD')
GOLD   = colors.HexColor('#D4A017')
GOLD2  = colors.HexColor('#FCD34D')
LGRAY  = colors.HexColor('#F0F4F8')
MGRAY  = colors.HexColor('#CBD5E1')
DGRAY  = colors.HexColor('#1E293B')
MID    = colors.HexColor('#475569')
WHITE  = colors.white
TEAL   = colors.HexColor('#0D9488')
GREEN  = colors.HexColor('#16A34A')
ROSE   = colors.HexColor('#E11D48')
ORANGE = colors.HexColor('#EA580C')
PURPLE = colors.HexColor('#7C3AED')

# ── 슬라이드 규격 ─────────────────────────────────────────────────────
SW, SH = 960, 540
MX = 32
HDR = 62
FTR = 20
CT  = SH - HDR - 8
CB  = FTR + 6
CW  = SW - 2*MX

COMPANY    = '(주)뉴허브인터내셔널'
COMPANY_EN = 'NewHub International Co., Ltd.'
BRAND_TAG  = '히어컴퍼니 (HearCompany) Corporate Consulting'
TODAY_STR  = datetime.date.today().strftime('%Y.%m.%d')


# ══════════════════════════════════════════════════════════════════════
# 공통 헬퍼
# ══════════════════════════════════════════════════════════════════════

def W(c, text, max_w, size):
    """텍스트를 max_w에 맞게 줄 분리"""
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append('')
            continue
        ln = ''
        for ch in para:
            if c.stringWidth(ln + ch, KR, size) <= max_w:
                ln += ch
            else:
                if ln: lines.append(ln)
                ln = ch
        if ln: lines.append(ln)
    return lines

def T(c, text, x, y, max_w, size, col=None, lh=None, center=False):
    if col is None: col = DGRAY
    if lh is None: lh = size * 1.75
    c.setFont(KR, size)
    c.setFillColor(col)
    for ln in W(c, text, max_w, size):
        if center:
            c.drawCentredString(x, y, ln)
        else:
            c.drawString(x, y, ln)
        y -= lh
    return y

def hdr(c, title, pg):
    """슬라이드 공통 헤더"""
    c.setFillColor(NAVY)
    c.rect(0, SH-HDR, SW, HDR, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, SH-HDR, 8, HDR, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, SH-HDR-3, SW, 3, fill=1, stroke=0)
    c.setFont(KR, 22)
    c.setFillColor(WHITE)
    c.drawString(MX+4, SH-HDR+20, title)
    # 우측: 페이지 + 브랜드
    c.setFont(KR, 9)
    c.setFillColor(LBLUE)
    c.drawRightString(SW-MX, SH-HDR+38, BRAND_TAG)
    c.setFont(KR, 11)
    c.setFillColor(GOLD2)
    c.drawRightString(SW-MX, SH-HDR+18, f'{pg} / 11')
    # 푸터
    c.setFont(KR, 9)
    c.setFillColor(MID)
    c.drawString(MX, 7, COMPANY)
    c.drawCentredString(SW/2, 7, '신용보증재단 보증신청용 사업계획서')
    c.drawRightString(SW-MX, 7, f'작성일 {TODAY_STR}')

def sec(c, x, y, text, w=None, bg=NAVY, fg=WHITE, size=13):
    h = size + 14
    tw = c.stringWidth(text, KR, size)
    bw = w or (tw + 22)
    c.setFillColor(bg)
    c.roundRect(x, y-h, bw, h, 3, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(x, y-h, 4, h, fill=1, stroke=0)
    c.setFont(KR, size)
    c.setFillColor(fg)
    c.drawString(x+10, y-h+6, text)
    return h

def kpi(c, x, y, w, h, label, value, sub='',
        bg=NAVY, label_col=LBLUE, val_col=GOLD2, sub_col=MID):
    c.setFillColor(colors.HexColor('#0A1929'))
    c.roundRect(x+3, y-h-2, w, h, 6, fill=1, stroke=0)
    c.setFillColor(bg)
    c.roundRect(x, y-h, w, h, 6, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.roundRect(x, y-4, w, 4, 2, fill=1, stroke=0)
    c.setFont(KR, 10)
    c.setFillColor(label_col)
    c.drawCentredString(x+w/2, y-18, label)
    c.setFont(KR, 26)
    c.setFillColor(val_col)
    c.drawCentredString(x+w/2, y-h/2-2, value)
    if sub:
        c.setFont(KR, 9)
        c.setFillColor(sub_col)
        c.drawCentredString(x+w/2, y-h+10, sub)

def tbl(c, x, y, hdrs, rows, ws, rh=26, hh=28, lcols=None, highlight_last=False):
    lcols = lcols or set()
    tw = sum(ws)
    c.setFillColor(NAVY)
    c.rect(x, y-hh, tw, hh, fill=1, stroke=0)
    c.setFont(KR, 12)
    c.setFillColor(WHITE)
    cx = x
    for h, w in zip(hdrs, ws):
        c.drawCentredString(cx+w/2, y-hh+(hh-12)/2, h)
        cx += w
    y -= hh
    for ri, row in enumerate(rows):
        is_last = ri == len(rows)-1
        bg = LGRAY if is_last and highlight_last else (WHITE if ri%2==0 else LGRAY)
        if is_last and highlight_last:
            bg = colors.HexColor('#FFF3CD')
        c.setFillColor(bg)
        c.rect(x, y-rh, tw, rh, fill=1, stroke=0)
        c.setStrokeColor(MGRAY)
        c.setLineWidth(0.4)
        c.rect(x, y-rh, tw, rh, fill=0, stroke=1)
        cx = x
        for ci, (v, w) in enumerate(zip(row, ws)):
            col = NAVY if ci==0 else (GOLD if is_last and highlight_last else DGRAY)
            c.setFont(KR, 11)
            c.setFillColor(col)
            ty = y-rh+(rh-11)/2
            if ci in lcols:
                c.drawString(cx+6, ty, str(v))
            else:
                c.drawCentredString(cx+w/2, ty, str(v))
            cx += w
        y -= rh
    return y

def bar_h(c, x, y, w, h, pct, bg=LGRAY, fg=BLUE, label='', val=''):
    c.setFillColor(bg)
    c.roundRect(x, y-h, w, h, h//2, fill=1, stroke=0)
    fw = max(h, w*pct)
    c.setFillColor(fg)
    c.roundRect(x, y-h, fw, h, h//2, fill=1, stroke=0)
    if label:
        c.setFont(KR, 10)
        c.setFillColor(DGRAY)
        c.drawString(x, y+3, label)
    if val:
        c.setFont(KR, 10)
        c.setFillColor(WHITE if pct>0.25 else DGRAY)
        c.drawString(x+fw-c.stringWidth(val,KR,10)-4, y-h+(h-10)/2, val)

def badge(c, x, y, text, bg=NAVY, fg=WHITE, size=10):
    pw = c.stringWidth(text, KR, size)+16
    ph = size+10
    c.setFillColor(bg)
    c.roundRect(x, y-ph, pw, ph, ph//2, fill=1, stroke=0)
    c.setFont(KR, size)
    c.setFillColor(fg)
    c.drawCentredString(x+pw/2, y-ph+5, text)
    return pw+5

def num_circle(c, cx, cy, r, num, bg=GOLD, fg=NAVY, size=16):
    c.setFillColor(bg)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFont(KR, size)
    c.setFillColor(fg)
    c.drawCentredString(cx, cy-size*0.38, str(num))

def div(c, y, x1=None, x2=None):
    c.setStrokeColor(MGRAY)
    c.setLineWidth(0.7)
    c.line(x1 or MX, y, x2 or SW-MX, y)

def donut_segment(c, cx, cy, r_out, r_in, start_deg, end_deg, fill_color):
    """도넛 차트 한 조각을 path로 그린다"""
    import math
    p = c.beginPath()
    a1 = math.radians(start_deg)
    a2 = math.radians(end_deg)
    # 외곽 시작점
    p.moveTo(cx + r_out*math.cos(a1), cy + r_out*math.sin(a1))
    # 외곽 호 — 작은 스텝으로 근사
    steps = max(2, int(abs(end_deg-start_deg)/3))
    for i in range(1, steps+1):
        ang = a1 + (a2-a1)*i/steps
        p.lineTo(cx + r_out*math.cos(ang), cy + r_out*math.sin(ang))
    # 내곽으로 이동
    p.lineTo(cx + r_in*math.cos(a2), cy + r_in*math.sin(a2))
    # 내곽 호 (반대 방향)
    for i in range(1, steps+1):
        ang = a2 - (a2-a1)*i/steps
        p.lineTo(cx + r_in*math.cos(ang), cy + r_in*math.sin(ang))
    p.close()
    c.setFillColor(fill_color)
    c.setStrokeColor(WHITE)
    c.setLineWidth(1.2)
    c.drawPath(p, fill=1, stroke=1)


# ══════════════════════════════════════════════════════════════════════
# 페이지 함수
# ══════════════════════════════════════════════════════════════════════

def p1(c):
    """1페이지 — 표지"""
    c.setFillColor(NAVY2)
    c.rect(0, 0, SW, SH, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, SH-7, SW, 7, fill=1, stroke=0)
    c.rect(0, 0, SW, 6, fill=1, stroke=0)

    # 좌측 콘텐츠 영역
    c.setFillColor(colors.HexColor('#142858'))
    c.roundRect(MX-10, 30, SW*0.58, SH-60, 8, fill=1, stroke=0)

    # 컨설팅 브랜드 헤더
    c.setFont(KR, 11)
    c.setFillColor(GOLD2)
    c.drawString(MX+6, SH-50, BRAND_TAG)

    c.setFont(KR, 11)
    c.setFillColor(LBLUE)
    c.drawString(MX+6, SH-78, '수입유통 · 무역업  |  유럽 3국 (프랑스 · 스페인 · 이탈리아)')

    c.setFont(KR, 32)
    c.setFillColor(WHITE)
    c.drawString(MX+6, SH-112, COMPANY)

    c.setFont(KR, 11)
    c.setFillColor(MGRAY)
    c.drawString(MX+6, SH-130, COMPANY_EN)

    c.setFillColor(GOLD)
    c.rect(MX+6, SH-142, 220, 3, fill=1, stroke=0)

    c.setFont(KR, 13)
    c.setFillColor(LBLUE)
    c.drawString(MX+6, SH-162, '21년 안정 영업의 다국·다품목 수입유통 전문기업')

    c.setFont(KR, 44)
    c.setFillColor(GOLD2)
    c.drawString(MX+6, SH-228, '사 업 계 획 서')

    c.setFont(KR, 13)
    c.setFillColor(WHITE)
    c.drawString(MX+6, SH-258, '신용보증재단 보증신청용  |  희망보증액 1.5억 원')

    c.setFont(KR, 12)
    c.setFillColor(MGRAY)
    c.drawString(MX+6, SH-282, f'화장품 · 식품 · 전자제품  |  제조업 신규 추가 추진')

    # 하단 기재 필요 표시
    c.setFont(KR, 10)
    c.setFillColor(MID)
    c.drawString(MX+6, 50, '대표이사 [회사 기재]   |   사업자등록번호 [회사 기재]')
    c.drawString(MX+6, 36, f'작성일  {TODAY_STR}')

    # 우측 KPI 카드 4개
    rx = int(SW*0.62)
    rw = SW - rx - MX
    kh = (SH-60)//2 - 8
    kw = (rw-8)//2

    items = [
        ('업력',          '21', '년',   NAVY,  LBLUE, GOLD2),
        ('주요 거래국',    '3',  '국',   BLUE,  LBLUE, GOLD2),
        ('연 매출(2025)', '8',  '억 원', TEAL,  LBLUE, GOLD2),
        ('일자리 창출',    '+2', '명 예정', ROSE, LBLUE, GOLD2),
    ]
    for i, (lbl, val, unit, bg, lc, vc) in enumerate(items):
        col = i % 2
        row = i // 2
        kx = rx + col*(kw+8)
        ky = SH-35 - row*(kh+10)
        c.setFillColor(bg)
        c.roundRect(kx, ky-kh, kw, kh, 6, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(kx, ky-4, kw, 4, 2, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(lc)
        c.drawCentredString(kx+kw/2, ky-18, lbl)
        c.setFont(KR, 30)
        c.setFillColor(vc)
        c.drawCentredString(kx+kw/2, ky-kh/2-4, val)
        c.setFont(KR, 11)
        c.setFillColor(LBLUE)
        c.drawCentredString(kx+kw/2, ky-kh+11, unit)


def p2(c):
    """2페이지 — 회사 개요 · 연혁"""
    hdr(c, '회사 개요 · 연혁', 2)
    y = CT

    # 상단: 회사 기본 정보 표
    sec(c, MX, y, '회사 기본 정보')
    y -= 30
    info = [
        ('회사명',       COMPANY),
        ('영문명',       COMPANY_EN),
        ('대표이사',     '[회사 기재]'),
        ('업종',         '수입유통업 (제조업 신규 추가 예정)'),
        ('업력',         '21년 (2005년경 설립 — 정확한 설립일 [회사 기재])'),
        ('주요 거래국',  '프랑스 · 스페인 · 이탈리아 (유럽 3국)'),
        ('주요 품목',    '화장품 · 식품 · 전자제품'),
    ]
    rh = 22
    for i, (k, v) in enumerate(info):
        ry = y - i*rh
        bg = WHITE if i%2==0 else LGRAY
        c.setFillColor(bg)
        c.rect(MX, ry-rh, CW, rh, fill=1, stroke=0)
        c.setStrokeColor(MGRAY)
        c.setLineWidth(0.4)
        c.rect(MX, ry-rh, CW, rh, fill=0, stroke=1)
        c.setFont(KR, 10)
        c.setFillColor(NAVY)
        c.drawString(MX+10, ry-rh+6, k)
        c.setFont(KR, 11)
        c.setFillColor(DGRAY)
        c.drawString(MX+150, ry-rh+6, v)
    y -= rh*len(info) + 16

    # 연혁 타임라인
    sec(c, MX, y, '21년 연혁 타임라인')
    y -= 32

    timeline = [
        ('2005',    '설립\n(추정)', NAVY),
        ('2010s',   '유럽 거래선\n다변화', BLUE),
        ('2020s',   '다품목\n포트폴리오\n구축', TEAL),
        ('2025',    '연매출\n8억 달성', GREEN),
        ('2026',    '제조업\n신규 추가\n+ 일자리 2명', GOLD),
        ('2027~',   '종합 무역\n· 제조 기업\n도약', ROSE),
    ]
    n = len(timeline)
    tw = (CW - (n-1)*8) / n
    th = y - CB - 4
    for i, (yr, body, bg) in enumerate(timeline):
        tx = MX + i*(tw+8)
        c.setFillColor(bg)
        c.roundRect(tx, CB, tw, th, 5, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(tx, CB+th-5, tw, 5, 2, fill=1, stroke=0)
        # 연도
        c.setFont(KR, 14)
        c.setFillColor(GOLD2)
        c.drawCentredString(tx+tw/2, CB+th-22, yr)
        # 본문
        c.setFont(KR, 10)
        c.setFillColor(WHITE)
        py = CB+th-44
        for ln in body.split('\n'):
            c.drawCentredString(tx+tw/2, py, ln)
            py -= 13
        # 화살표
        if i < n-1:
            c.setFont(KR, 14)
            c.setFillColor(GOLD)
            c.drawCentredString(tx+tw+4, CB+th/2, '▶')


def p3(c):
    """3페이지 — 사업 현황 (수입유통)"""
    hdr(c, '사업 현황 — 수입유통 매트릭스', 3)
    y = CT

    # 상단 메시지
    c.setFillColor(LGRAY)
    c.roundRect(MX, y-38, CW, 38, 4, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(MX, y-38, 4, 38, fill=1, stroke=0)
    c.setFont(KR, 12)
    c.setFillColor(DGRAY)
    c.drawString(MX+14, y-15,
        '유럽 3국 × 3품목 — 9개 카테고리의 분산형 포트폴리오로 안정적 매출 구조 확보')
    c.setFont(KR, 10)
    c.setFillColor(MID)
    c.drawString(MX+14, y-30,
        '단일 거래국·단일 품목 의존도 ZERO — 환율·시장 리스크 자연 분산')
    y -= 50

    # 3 × 3 매트릭스
    sec(c, MX, y, '국가 × 품목 매트릭스')
    y -= 30

    countries = ['프랑스', '스페인', '이탈리아']
    products = ['화장품', '식품', '전자제품']
    cell_w = (CW - 100) / 3
    cell_h = 50
    head_h = 26
    # 헤더 행
    c.setFillColor(NAVY)
    c.rect(MX, y-head_h, 100, head_h, fill=1, stroke=0)
    for i, ct in enumerate(countries):
        c.setFillColor(NAVY)
        c.rect(MX+100+i*cell_w, y-head_h, cell_w, head_h, fill=1, stroke=0)
        c.setFont(KR, 12)
        c.setFillColor(WHITE)
        c.drawCentredString(MX+100+i*cell_w+cell_w/2, y-head_h+8, ct)
    y -= head_h
    # 셀 데이터
    cell_data = {
        ('화장품', '프랑스'):   '프리미엄 스킨케어\n향수',
        ('화장품', '스페인'):   '오가닉 라인\n색조',
        ('화장품', '이탈리아'): '럭셔리 브랜드\n고급 화장품',
        ('식품', '프랑스'):     '와인·치즈\n제과',
        ('식품', '스페인'):     '올리브유·하몽\n와인',
        ('식품', '이탈리아'):   '파스타·올리브유\n치즈·와인',
        ('전자제품', '프랑스'): '소형가전\n주방가전',
        ('전자제품', '스페인'): '디자인 가전\n소형 IT',
        ('전자제품', '이탈리아'): '명품 주방가전\n프리미엄 IT',
    }
    cell_colors = [LGRAY, WHITE, LGRAY]
    for ri, prod in enumerate(products):
        # 품목 레이블
        c.setFillColor(BLUE if ri%2==0 else TEAL)
        c.rect(MX, y-cell_h, 100, cell_h, fill=1, stroke=0)
        c.setFont(KR, 12)
        c.setFillColor(WHITE)
        c.drawCentredString(MX+50, y-cell_h/2-4, prod)
        for ci, ct in enumerate(countries):
            cx = MX+100+ci*cell_w
            c.setFillColor(cell_colors[(ri+ci)%2])
            c.rect(cx, y-cell_h, cell_w, cell_h, fill=1, stroke=0)
            c.setStrokeColor(MGRAY)
            c.setLineWidth(0.4)
            c.rect(cx, y-cell_h, cell_w, cell_h, fill=0, stroke=1)
            txt = cell_data.get((prod, ct), '')
            c.setFont(KR, 9)
            c.setFillColor(DGRAY)
            for li, ln in enumerate(txt.split('\n')):
                c.drawCentredString(cx+cell_w/2, y-18-li*12, ln)
        y -= cell_h
    y -= 16

    # 매출 8억 비중 추정
    sec(c, MX, y, '2025년 매출 8억원 — 품목별 비중 [추정]')
    y -= 28
    bars = [
        ('화장품',    0.45, '약 3.6억', NAVY),
        ('식품',      0.35, '약 2.8억', BLUE),
        ('전자제품',  0.20, '약 1.6억', TEAL),
    ]
    bar_w = CW - 200
    for lbl, pct, val, col in bars:
        c.setFont(KR, 11)
        c.setFillColor(DGRAY)
        c.drawString(MX, y-3, lbl)
        c.setFillColor(LGRAY)
        c.roundRect(MX+80, y-14, bar_w, 12, 6, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(MX+80, y-14, bar_w*pct, 12, 6, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(NAVY)
        c.drawString(MX+90+bar_w, y-3, val)
        y -= 20

    # 보정 안내
    c.setFont(KR, 8)
    c.setFillColor(MID)
    c.drawString(MX, CB-2, '* 품목별 비중은 추정치 — 회사 측 정확한 매출 분기 데이터로 보정 필요')


def p4(c):
    """4페이지 — 시장 환경 · 경쟁력 · SWOT"""
    hdr(c, '시장 환경 · 경쟁력 · SWOT', 4)
    y = CT

    # 좌측: 시장 트렌드
    lw = CW*0.46
    sec(c, MX, y, '유럽 수입 시장 트렌드')
    y -= 30

    trends = [
        (NAVY,  '프리미엄 화장품',  'K-뷰티 역수입·럭셔리 라인 성장'),
        (BLUE,  '유럽 식품 프리미엄', '와인·올리브유·치즈 수요 안정'),
        (TEAL,  '소형·디자인 가전', '주방·생활가전 시장 연 5%+ 성장'),
        (GREEN, '환율 안정 국면',   'EUR/KRW 안정 — 수입 환경 우호적'),
    ]
    for i, (col, t, sub) in enumerate(trends):
        iy = y - i*38
        c.setFillColor(LGRAY)
        c.roundRect(MX, iy-34, lw, 32, 4, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(MX, iy-34, 5, 32, 2, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(col)
        c.drawString(MX+14, iy-13, t)
        c.setFont(KR, 9)
        c.setFillColor(MID)
        c.drawString(MX+14, iy-26, sub)

    # 우측: SWOT 2x2
    rx = MX + lw + 16
    rw = CW - lw - 16
    ry = CT
    sec(c, rx, ry, 'SWOT 분석')
    ry -= 30

    sw_w = (rw-8)/2
    sw_h = (CT - 30 - CB - 8)/2
    swot = [
        ('S 강점', NAVY,  '21년 업력 신뢰자산\n다국·다품목 분산\n검증된 거래선'),
        ('W 약점', ORANGE,'제조 기반 미보유\n자체 브랜드 부재\n환율 노출도'),
        ('O 기회', GREEN, 'K-푸드/뷰티 글로벌\n프리미엄 수요 성장\n제조 다각화'),
        ('T 위협', ROSE,  'EUR 환율 변동\n경쟁사 직수입 증가\n글로벌 공급 리스크'),
    ]
    for i, (t, bg, body) in enumerate(swot):
        col = i % 2
        row = i // 2
        sx = rx + col*(sw_w+8)
        sy = ry - row*(sw_h+8)
        c.setFillColor(bg)
        c.roundRect(sx, sy-sw_h, sw_w, sw_h, 4, fill=1, stroke=0)
        c.setFont(KR, 12)
        c.setFillColor(GOLD2)
        c.drawString(sx+10, sy-18, t)
        c.setFont(KR, 9)
        c.setFillColor(WHITE)
        py = sy-34
        for ln in body.split('\n'):
            c.drawString(sx+10, py, ln)
            py -= 13


def p5(c):
    """5페이지 — 신규 사업 (제조업 추가)"""
    hdr(c, '신규 사업 — 제조업 추가 추진', 5)
    y = CT

    # 명분 배너
    c.setFillColor(NAVY)
    c.roundRect(MX, y-50, CW, 50, 5, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(MX, y-50, 5, 50, fill=1, stroke=0)
    c.setFont(KR, 14)
    c.setFillColor(GOLD2)
    c.drawString(MX+18, y-22, '"수입유통 + 자체 제조" 결합으로 부가가치 향상 및 매출 안정화')
    c.setFont(KR, 11)
    c.setFillColor(LBLUE)
    c.drawString(MX+18, y-40, '21년 유통 경험으로 시장 수요를 읽고, 자체 제조로 마진율·브랜드 자산을 동시에 확보')
    y -= 62

    # 좌측: 카테고리 후보 3개
    lw = CW*0.42
    sec(c, MX, y, '제조 카테고리 후보 [회사 확정]')
    ly = y - 30

    cats = [
        ('① 화장품 OEM',  NAVY,  'K-뷰티 역수입 노하우\n+ 자체 브랜드 OEM'),
        ('② 식품 가공',    BLUE,  '유럽 원료 수입 +\n국내 가공·재포장'),
        ('③ 전자제품 조립', TEAL,  '수입 부품·완제품\n+ 국내 조립·SI'),
    ]
    cw_l = lw
    ch_l = 56
    for i, (t, bg, body) in enumerate(cats):
        cy = ly - i*(ch_l+6)
        c.setFillColor(bg)
        c.roundRect(MX, cy-ch_l, cw_l, ch_l, 4, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.rect(MX, cy-ch_l, 4, ch_l, fill=1, stroke=0)
        c.setFont(KR, 13)
        c.setFillColor(GOLD2)
        c.drawString(MX+14, cy-22, t)
        c.setFont(KR, 10)
        c.setFillColor(WHITE)
        py = cy-38
        for ln in body.split('\n'):
            c.drawString(MX+14, py, ln)
            py -= 13

    # 우측: 추진 로드맵
    rx = MX + lw + 16
    rw = CW - lw - 16
    ry = y
    sec(c, rx, ry, '6~12개월 추진 로드맵')
    ry -= 30

    roadmap = [
        ('1~2개월',  '카테고리 확정 · 제조 파트너 선정', GOLD),
        ('3~4개월',  '소요 자금 집행 · 시설·계약',        BLUE),
        ('5~7개월',  '시제품 제작 · 인증 · 시장 테스트',   TEAL),
        ('8~10개월', '본격 양산 · 마케팅 런칭',            GREEN),
        ('11~12개월','매출 발생 · 채널 확장',              ROSE),
    ]
    for i, (period, content, col) in enumerate(roadmap):
        iy = ry - i*30
        c.setFillColor(col)
        c.circle(rx+10, iy-10, 6, fill=1, stroke=0)
        if i < len(roadmap)-1:
            c.setStrokeColor(MGRAY)
            c.setLineWidth(1.5)
            c.line(rx+10, iy-16, rx+10, iy-34)
        c.setFont(KR, 10)
        c.setFillColor(NAVY)
        c.drawString(rx+24, iy-14, period)
        c.setFont(KR, 10)
        c.setFillColor(DGRAY)
        c.drawString(rx+90, iy-14, content)

    # 하단: 예상 효과
    c.setFillColor(GOLD)
    c.rect(MX, CB, CW, 26, fill=1, stroke=0)
    c.setFont(KR, 12)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, CB+8,
        '예상 효과  —  제조업 추가 → 마진율 5~8%p 향상 + 자체 브랜드 자산 + 일자리 2명 창출')


def p6(c):
    """6페이지 — 자금 조달 · 사용 계획 (★ 핵심)"""
    hdr(c, '자금 조달 · 사용 계획  ★', 6)

    # 골드 서브 배너
    c.setFillColor(GOLD)
    c.rect(0, SH-HDR-26, SW, 24, fill=1, stroke=0)
    c.setFont(KR, 12)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, SH-HDR-15, '신용보증재단 보증 1.5억 → 협력은행 융자 1.5억 실행')

    y = CT - 32

    # 자금 흐름도
    sec(c, MX, y, '자금 조달 흐름도')
    y -= 30

    flow = [
        ('신용보증재단',  '보증서 발급\n1.5억 원',     NAVY),
        ('협력 은행',     '여신 실행\n1.5억 원',       BLUE),
        ('(주)뉴허브',    '자금 수령\n사업 집행',       TEAL),
        ('자금 사용',     '운영 / 결제\n/ 제조',         GOLD),
    ]
    fw = (CW - 3*22) / 4
    fh = 60
    for i, (name, sub, col) in enumerate(flow):
        fx = MX + i*(fw+22)
        c.setFillColor(col)
        c.roundRect(fx, y-fh, fw, fh, 5, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(fx, y-4, fw, 4, 2, fill=1, stroke=0)
        c.setFont(KR, 12)
        c.setFillColor(WHITE if col != GOLD else NAVY2)
        c.drawCentredString(fx+fw/2, y-22, name)
        c.setFont(KR, 9)
        c.setFillColor(LBLUE if col != GOLD else NAVY)
        py = y-38
        for ln in sub.split('\n'):
            c.drawCentredString(fx+fw/2, py, ln)
            py -= 11
        if i < 3:
            c.setFont(KR, 18)
            c.setFillColor(GOLD)
            c.drawCentredString(fx+fw+11, y-fh/2-6, '▶')
    y -= fh + 16

    # 하단: 도넛 차트 (자금 사용처)
    sec(c, MX, y, '자금 사용처 분배')
    y -= 30

    # 도넛 차트 (좌측)
    cx, cy = MX + 100, CB + 80
    r_out, r_in = 70, 38
    segments = [
        ('운영자금',   0.40, NAVY,  '6,000만원'),
        ('수입결제',   0.40, BLUE,  '6,000만원'),
        ('제조업 추가', 0.20, TEAL,  '3,000만원'),
    ]
    start = 90
    for lbl, pct, col, val in segments:
        end = start - pct*360
        donut_segment(c, cx, cy, r_out, r_in, start, end, col)
        start = end
    # 도넛 중앙 텍스트
    c.setFont(KR, 11)
    c.setFillColor(NAVY)
    c.drawCentredString(cx, cy+8, '총 보증액')
    c.setFont(KR, 16)
    c.setFillColor(GOLD)
    c.drawCentredString(cx, cy-12, '1.5억 원')

    # 우측 범례 + 표
    lx = MX + 200
    lw = CW - 200
    legend_y = y - 8
    for i, (lbl, pct, col, val) in enumerate(segments):
        ly = legend_y - i*36
        c.setFillColor(col)
        c.roundRect(lx, ly-22, 16, 16, 2, fill=1, stroke=0)
        c.setFont(KR, 12)
        c.setFillColor(NAVY)
        c.drawString(lx+24, ly-14, f'{lbl}  {int(pct*100)}%')
        c.setFont(KR, 10)
        c.setFillColor(MID)
        c.drawString(lx+24, ly-28, f'{val}  —  ' + {
            '운영자금':   '인건비 · 임차료 · 관리비 · 광고비',
            '수입결제':   'L/C 개설 · T/T 송금 · 통관 · 운송',
            '제조업 추가': '시설 · 초도 운영 · 시제품 · 인증',
        }[lbl])

    # 보정 표시
    c.setFont(KR, 8)
    c.setFillColor(MID)
    c.drawRightString(SW-MX, CB-2, '* 비율은 기본 예시 — 회사 측 정확한 사업계획에 따라 조정 [회사 기재]')


def p7(c):
    """7페이지 — 매출·재무 추이 및 전망"""
    hdr(c, '매출 · 재무 추이 및 전망', 7)
    y = CT

    # 상단 KPI
    kw = (CW-16)//3
    kh = 80
    kpi(c, MX,          y, kw, kh, '2025 매출 실적', '8.0억',  '21년 안정 영업', NAVY,  LBLUE, GOLD2)
    kpi(c, MX+kw+8,     y, kw, kh, '2027 매출 목표', '11.0억', '제조업 효과 반영', BLUE, LBLUE, GOLD2)
    kpi(c, MX+(kw+8)*2, y, kw, kh, '3년 누적 성장률', '+50%',   '연평균 +14.5%',  TEAL, LBLUE, GOLD2)
    y -= kh + 14

    # 매출 추이 표
    sec(c, MX, y, '매출 추이 및 전망')
    y -= 30
    rows = [
        ('2023 실적', '6.5억 원',  '—',     '수입유통 기반 안정', '[추정]'),
        ('2024 실적', '7.2억 원',  '+10.8%', '거래선 확대',        '[추정]'),
        ('2025 실적', '8.0억 원',  '+11.1%', '다품목 포트폴리오',  '확정'),
        ('2026 목표', '9.5억 원',  '+18.8%', '제조업 추가 초기 효과', '계획'),
        ('2027 목표', '11.0억 원', '+15.8%', '제조 본격화 + 일자리 2명', '계획'),
        ('2028 목표', '12.0억 원', '+9.1%',  '종합 무역·제조 기업 도약', '계획'),
    ]
    tbl(c, MX, y, ['연도', '매출액', '증감률', '비고', '구분'],
        rows, [100, 130, 90, CW-460, 140], rh=24, hh=26, highlight_last=True)

    # 하단 안내
    c.setFillColor(LGRAY)
    c.roundRect(MX, CB, CW, 20, 3, fill=1, stroke=0)
    c.setFont(KR, 9)
    c.setFillColor(MID)
    c.drawString(MX+10, CB+6,
        '* 2023~2024 실적 및 2026~2028 전망은 추정치 — 회사 측 엑셀 원본 자료 기반 보정 필요')


def p8(c):
    """8페이지 — 일자리 창출 효과"""
    hdr(c, '일자리 창출 효과', 8)
    y = CT

    # 상단 메시지
    c.setFillColor(GOLD)
    c.rect(MX, y-32, CW, 32, fill=1, stroke=0)
    c.setFont(KR, 14)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, y-20,
        '21년 안정 고용 + 신규 채용 2명 = 보증재단 일자리 창출 가산점 항목 충족')
    y -= 46

    # 신규 채용 카드 2개
    sec(c, MX, y, '신규 채용 계획')
    y -= 30

    new_hires = [
        ('① 제조·품질관리 1명', NAVY,
         '직무: 신규 제조사업 품질관리·제조 공정 관리',
         '시점: 2026년 Q2 ~ Q3',
         '대상: 청년/경력자 (보증재단 우대)',
         '연봉: 약 3,800만 원 (4대보험 포함)'),
        ('② 영업·해외협력 1명', BLUE,
         '직무: 유럽 거래선 영업·신규 파트너 발굴',
         '시점: 2026년 Q3 ~ Q4',
         '대상: 청년/여성/경력자 (보증재단 우대)',
         '연봉: 약 3,500만 원 (4대보험 포함)'),
    ]
    cw_h = (CW-12)//2
    ch_h = 130
    for i, (t, bg, l1, l2, l3, l4) in enumerate(new_hires):
        cx = MX + i*(cw_h+12)
        c.setFillColor(bg)
        c.roundRect(cx, y-ch_h, cw_h, ch_h, 5, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(cx, y-5, cw_h, 5, 2, fill=1, stroke=0)
        c.setFont(KR, 14)
        c.setFillColor(GOLD2)
        c.drawString(cx+14, y-26, t)
        c.setStrokeColor(colors.HexColor('#FFFFFF40'))
        c.setLineWidth(0.5)
        c.line(cx+14, y-36, cx+cw_h-14, y-36)
        c.setFont(KR, 11)
        c.setFillColor(WHITE)
        py = y-54
        for ln in [l1, l2, l3, l4]:
            c.drawString(cx+14, py, ln)
            py -= 17
    y -= ch_h + 14

    # 하단: 보증재단 우대 가점 안내
    sec(c, MX, y, '보증재단 우대 가점 항목')
    y -= 28

    pts = [
        (GREEN,  '청년 채용 (만 39세 이하)'),
        (BLUE,   '여성 채용'),
        (TEAL,   '중장년 채용 (만 50세 이상)'),
        (GOLD,   '신규 일자리 창출 (보증한도 우대)'),
        (ROSE,   '21년 장기 고용 안정 기업'),
    ]
    bx = MX
    for col, t in pts:
        pw = c.stringWidth(t, KR, 10) + 24
        c.setFillColor(col)
        c.roundRect(bx, y-22, pw, 22, 11, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(WHITE)
        c.drawCentredString(bx+pw/2, y-15, t)
        bx += pw + 8


def p9(c):
    """9페이지 — 위험 요소 · 대응"""
    hdr(c, '위험 요소 · 대응 전략', 9)
    y = CT

    risks = [
        ('① 환율 리스크 (EUR/KRW 변동)', ROSE, NAVY,
         ['선물환·통화옵션 헷지 도입',
          '결제 통화·시점 분산',
          '거래선과 가격 조정 조항 협의',
          '21년 거래 노하우로 환율 사이클 대응']),
        ('② 글로벌 공급·물류 리스크', ORANGE, NAVY,
         ['3개국 거래선 분산 — 단일 공급 의존도 낮음',
          '주요 품목별 복수 거래선 보유',
          '재고 안전수준 운영 (3~4개월분)',
          'L/C 보험·운송 보험 가입']),
        ('③ 경쟁사 직수입 증가', GOLD, NAVY,
         ['21년 누적 신뢰자산 — 거래선 독점성',
          '제조업 추가로 차별화 (자체 브랜드)',
          '다품목 포트폴리오로 경쟁 분산',
          '프리미엄·소량 다품종 전략 강화']),
        ('④ 제조업 진입 초기 리스크', TEAL, NAVY,
         ['단계적 투자 (전체 자금의 20%만 우선 투입)',
          '시제품 → 시장 테스트 → 본격 양산',
          'OEM/위탁 우선 검토 — 자가 설비 부담 최소화',
          '실패 시 수입유통 기존 매출 유지']),
    ]
    cw_r = (CW-12)//2
    ch_r = (CT - CB - 6)//2

    for i, (title, accent, bg, items) in enumerate(risks):
        col = i % 2
        row = i // 2
        cx = MX + col*(cw_r+12)
        cy = y - row*(ch_r+6)
        c.setFillColor(LGRAY)
        c.roundRect(cx, cy-ch_r, cw_r, ch_r, 5, fill=1, stroke=0)
        c.setFillColor(accent)
        c.roundRect(cx, cy-5, cw_r, 5, 2, fill=1, stroke=0)
        c.setFillColor(accent)
        c.rect(cx, cy-ch_r, 4, ch_r, fill=1, stroke=0)
        c.setFont(KR, 13)
        c.setFillColor(NAVY)
        c.drawString(cx+14, cy-22, title)
        c.setStrokeColor(MGRAY)
        c.setLineWidth(0.4)
        c.line(cx+14, cy-30, cx+cw_r-14, cy-30)
        py = cy-46
        c.setFont(KR, 10)
        c.setFillColor(DGRAY)
        for it in items:
            c.setFillColor(accent)
            c.circle(cx+18, py+3, 2.5, fill=1, stroke=0)
            c.setFillColor(DGRAY)
            c.drawString(cx+26, py, it)
            py -= 16


def p10(c):
    """10페이지 — 자금 상환 계획"""
    hdr(c, '자금 상환 계획', 10)
    y = CT

    # 상단 상환 가정
    sec(c, MX, y, '상환 가정 및 부담 계산')
    y -= 30

    rows = [
        ('보증액',           '150,000,000원',  '신용보증재단 보증한도'),
        ('대출금리 (가정)',  '연 4.0%',        '협력은행 우대금리 [추정]'),
        ('상환기간',         '5년 (60개월)',   '거치 1년 + 분할상환 4년 [추정]'),
        ('월 이자(거치기간)', '500,000원',     '150,000,000 × 4% ÷ 12'),
        ('월 원리금(분할상환)','3,440,000원',  '원금 분할 + 이자 합계 [추정]'),
        ('연간 상환 부담',    '약 41,300,000원','12개월 × 3,440,000 [추정]'),
    ]
    tbl(c, MX, y, ['항목', '금액 / 조건', '산출 근거'],
        rows, [180, 200, CW-380], rh=22, hh=24, lcols={2})
    y -= 22*6 + 24 + 14

    # DSCR 분석
    sec(c, MX, y, 'DSCR (부채상환능력) 분석')
    y -= 30

    # 좌: 수치 박스
    lw = CW*0.42
    c.setFillColor(NAVY)
    c.roundRect(MX, y-90, lw, 90, 5, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.roundRect(MX, y-5, lw, 5, 2, fill=1, stroke=0)
    c.setFont(KR, 11)
    c.setFillColor(LBLUE)
    c.drawCentredString(MX+lw/2, y-22, 'DSCR 추정')
    c.setFont(KR, 36)
    c.setFillColor(GOLD2)
    c.drawCentredString(MX+lw/2, y-58, '2.4 배')
    c.setFont(KR, 10)
    c.setFillColor(LBLUE)
    c.drawCentredString(MX+lw/2, y-78, '연 영업이익 약 1억 ÷ 연 상환부담 4,130만')

    # 우: 시나리오
    rx = MX + lw + 16
    rw = CW - lw - 16
    c.setFillColor(LGRAY)
    c.roundRect(rx, y-90, rw, 90, 5, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.roundRect(rx, y-5, rw, 5, 2, fill=1, stroke=0)
    c.setFont(KR, 12)
    c.setFillColor(NAVY)
    c.drawString(rx+14, y-22, '비상 상환 시나리오')
    scenarios = [
        '• 수입유통 기존 매출 8억 — 안정 현금흐름 유지',
        '• 제조업 진입 지연 시에도 기존 사업 매출 영향 없음',
        '• 21년 거래선 신뢰 — 매출 급락 가능성 낮음',
        '• 재고 자산·매출채권 담보 여력 보유',
    ]
    py = y-40
    c.setFont(KR, 10)
    c.setFillColor(DGRAY)
    for s in scenarios:
        c.drawString(rx+14, py, s)
        py -= 14
    y -= 90 + 14

    # 하단 결론
    c.setFillColor(GOLD)
    c.roundRect(MX, CB, CW, 26, 4, fill=1, stroke=0)
    c.setFont(KR, 12)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, CB+8,
        'DSCR 2.4배 — 안정적 상환 능력 확보  |  매출 8억 기반 + 제조업 추가 효과 = 상환 위험 낮음')


def p11(c):
    """11페이지 — 사업 비전 · 요약 (Closing)"""
    c.setFillColor(NAVY2)
    c.rect(0, 0, SW, SH, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, SH-7, SW, 7, fill=1, stroke=0)
    c.rect(0, 0, SW, 6, fill=1, stroke=0)

    # 상단 비전 메시지
    c.setFont(KR, 14)
    c.setFillColor(GOLD2)
    c.drawCentredString(SW/2, SH-50, 'Vision 2028')
    c.setFont(KR, 24)
    c.setFillColor(WHITE)
    c.drawCentredString(SW/2, SH-90, '21년 안정 영업 + 신규 제조 = 종합 무역·제조 기업 도약')

    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(SW/2-220, SH-110, SW/2+220, SH-110)

    # 핵심 요약 3박스
    cy = SH-160
    bw = (SW - 2*MX - 24) // 3
    bh = 110
    summary = [
        ('보증 활용', '1.5억 원',
         '신용보증재단 보증\n→ 협력은행 융자\n→ 운영·결제·제조',
         BLUE),
        ('매출 도약', '8억 → 12억',
         '2025 → 2028\n+50% 성장\n연평균 +14.5%',
         TEAL),
        ('일자리 창출', '+ 2명',
         '제조·품질관리 1명\n영업·해외협력 1명\n청년·여성 우대',
         ROSE),
    ]
    for i, (lbl, val, body, bg) in enumerate(summary):
        bx = MX + i*(bw+12)
        c.setFillColor(bg)
        c.roundRect(bx, cy-bh, bw, bh, 6, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(bx, cy-4, bw, 4, 2, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(LBLUE)
        c.drawCentredString(bx+bw/2, cy-22, lbl)
        c.setFont(KR, 24)
        c.setFillColor(GOLD2)
        c.drawCentredString(bx+bw/2, cy-52, val)
        c.setFont(KR, 10)
        c.setFillColor(WHITE)
        py = cy-72
        for ln in body.split('\n'):
            c.drawCentredString(bx+bw/2, py, ln)
            py -= 12

    # 마무리 문구
    c.setFont(KR, 36)
    c.setFillColor(WHITE)
    c.drawCentredString(SW/2, 150, 'THANK YOU.')
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(SW/2-120, 130, SW/2+120, 130)

    c.setFont(KR, 14)
    c.setFillColor(GOLD2)
    c.drawCentredString(SW/2, 105, COMPANY)
    c.setFont(KR, 10)
    c.setFillColor(LBLUE)
    c.drawCentredString(SW/2, 88, COMPANY_EN)
    c.setFont(KR, 10)
    c.setFillColor(MGRAY)
    c.drawCentredString(SW/2, 68, '대표이사 [회사 기재]   |   T. [회사 기재]   |   E. [회사 기재]')

    c.setFont(KR, 9)
    c.setFillColor(GOLD2)
    c.drawCentredString(SW/2, 44, BRAND_TAG)

    c.setFont(KR, 8)
    c.setFillColor(MID)
    c.drawCentredString(SW/2, 16,
        '본 사업계획서는 정책자금 신청용 초안입니다. 신용보증재단 제출 전 전문가 검토를 권장합니다.')


# ══════════════════════════════════════════════════════════════════════
def build():
    out = Path(__file__).parent / f'{COMPANY}_정책자금사업계획서_{datetime.date.today().strftime("%Y%m%d")}.pdf'
    cv = pdfcanvas.Canvas(str(out), pagesize=(SW, SH))
    cv.setTitle(f'{COMPANY} 정책자금 사업계획서')
    cv.setAuthor('히어컴퍼니 (HearCompany) Corporate Consulting')
    cv.setSubject('신용보증재단 보증신청용')
    for fn in [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]:
        fn(cv)
        cv.showPage()
    cv.save()
    print(f'[OK] {out}')
    print(f'     size: {out.stat().st_size:,} bytes')

if __name__ == '__main__':
    build()
