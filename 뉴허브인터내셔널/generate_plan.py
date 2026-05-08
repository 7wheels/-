"""
(주)뉴허브인터내셔널 — 정책자금 사업계획서 (신용보증재단 보증신청용)
16:9 슬라이드 / 인포그래픽 중심 / 11페이지

전면 재작성: 실제 엑셀 데이터 반영
- 2021.03.24 개업 (업력 5년)
- 2025년 매출 8.6억 흑자전환 (2024년 1.15억 결손에서 7.5배 급성장)
- 청년·여성 창업기업 / 청정 신용 / Brand Curation B2B 수출
- 자금 1.5억: K-connect hub / K-beauty4U / 자체 브랜드

작성: 히어컴퍼니 (HearCompany) Corporate Consulting
"""
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pathlib import Path
import datetime
import math

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
PINK   = colors.HexColor('#DB2777')

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
    c.drawCentredString(SW/2, 7, '신용보증재단 보증신청용 사업계획서  |  ' + BRAND_TAG)
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

def tbl(c, x, y, hdrs, rows, ws, rh=26, hh=28, lcols=None, highlight_last=False, highlight_rows=None):
    lcols = lcols or set()
    highlight_rows = highlight_rows or set()
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
        is_hl = (is_last and highlight_last) or (ri in highlight_rows)
        bg = WHITE if ri%2==0 else LGRAY
        if is_hl:
            bg = colors.HexColor('#FFF3CD')
        c.setFillColor(bg)
        c.rect(x, y-rh, tw, rh, fill=1, stroke=0)
        c.setStrokeColor(MGRAY)
        c.setLineWidth(0.4)
        c.rect(x, y-rh, tw, rh, fill=0, stroke=1)
        cx = x
        for ci, (v, w) in enumerate(zip(row, ws)):
            col = NAVY if ci==0 else (GOLD if is_hl else DGRAY)
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
    p = c.beginPath()
    a1 = math.radians(start_deg)
    a2 = math.radians(end_deg)
    p.moveTo(cx + r_out*math.cos(a1), cy + r_out*math.sin(a1))
    steps = max(2, int(abs(end_deg-start_deg)/3))
    for i in range(1, steps+1):
        ang = a1 + (a2-a1)*i/steps
        p.lineTo(cx + r_out*math.cos(ang), cy + r_out*math.sin(ang))
    p.lineTo(cx + r_in*math.cos(a2), cy + r_in*math.sin(a2))
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
    c.drawString(MX+6, SH-78, 'B2B 수출 · Brand Curation  |  화장품·식품·기계·해외 컨설팅')

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
    c.drawString(MX+6, SH-162, '청년·여성 창업기업  |  매출 7.5배 급성장 + 흑자전환')

    c.setFont(KR, 44)
    c.setFillColor(GOLD2)
    c.drawString(MX+6, SH-228, '사 업 계 획 서')

    c.setFont(KR, 13)
    c.setFillColor(WHITE)
    c.drawString(MX+6, SH-258, '신용보증재단 보증신청용  |  희망보증액 1.5억 원')

    c.setFont(KR, 12)
    c.setFillColor(MGRAY)
    c.drawString(MX+6, SH-282, '디지털 인프라 (4개 언어 사이트·B2B 편집샵) + 자체 브랜드 화장품')

    # 하단 기재 필요 표시
    c.setFont(KR, 10)
    c.setFillColor(MID)
    c.drawString(MX+6, 64, '서울시 강서구 마곡 중앙1로 10. 802호')
    c.drawString(MX+6, 50, '대표이사 [회사 기재]   |   사업자등록번호 [회사 기재]')
    c.drawString(MX+6, 36, f'개업일 2021.03.24   |   작성일 {TODAY_STR}')

    # 우측 KPI 카드 4개
    rx = int(SW*0.62)
    rw = SW - rx - MX
    kh = (SH-60)//2 - 8
    kw = (rw-8)//2

    items = [
        ('업력',          '5',  '년',     NAVY,  LBLUE, GOLD2),
        ('2025 매출',     '8.6','억 (흑자전환)', BLUE, LBLUE, GOLD2),
        ('2026 목표',     '20', '억 원',  TEAL,  LBLUE, GOLD2),
        ('일자리 창출',    '+1~2','명 예정',  ROSE, LBLUE, GOLD2),
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
    """2페이지 — 회사 개요 · 연혁 (5개 마일스톤 + 대표 정보)"""
    hdr(c, '회사 개요 · 연혁', 2)
    y = CT

    # 상단: 회사 기본 정보 표
    sec(c, MX, y, '회사 기본 정보')
    y -= 30
    info = [
        ('회사명',       COMPANY),
        ('영문명',       COMPANY_EN),
        ('개업일',       '2021.03.24  (업력 약 5년 — 청년 스타트업)'),
        ('사업장',       '서울시 강서구 마곡 중앙1로 10. 802호'),
        ('주업종',       '화장품·방향제·세제 / 무역중개·알선 / 식품·생활잡화 / 전자상거래'),
        ('대표자',       '여성 · 사업운영 7년 · 프랑스어 통역 가이드 자격 · 주식 80%'),
        ('대표 전공',     '불어불문학과 / 아프리카 지역학  →  EMEA 시장 직접 소통 역량'),
    ]
    rh = 20
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
        c.drawString(MX+10, ry-rh+5, k)
        c.setFont(KR, 10)
        c.setFillColor(DGRAY)
        c.drawString(MX+130, ry-rh+5, v)
    y -= rh*len(info) + 14

    # 청년·여성 창업기업 배지
    bx = MX
    badges = [
        ('청년·여성 창업기업', GOLD, NAVY2),
        ('매출 7.5배 급성장', ROSE, WHITE),
        ('2025 흑자전환', GREEN, WHITE),
        ('무차입 청정 신용', BLUE, WHITE),
        ('수출실적증명원 발급 가능', TEAL, WHITE),
    ]
    for t, bg, fg in badges:
        bx += badge(c, bx, y, t, bg=bg, fg=fg, size=10)
    y -= 26

    # 5개 마일스톤 타임라인
    sec(c, MX, y, '5개 마일스톤 — 2021 개업 → 2026 디지털 확장')
    y -= 30

    timeline = [
        ('2021.03', '개업\n(마곡 본사)',                  NAVY),
        ('2023',    '매출 0.75억\n사업 정착',              BLUE),
        ('2024',    '매출 1.15억\n거래선 발굴',            TEAL),
        ('2025',    '매출 8.6억\n흑자전환',               GREEN),
        ('2026',    '디지털 인프라\n+ 자체 브랜드\n+ 미국 진출', GOLD),
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
        c.setFont(KR, 14)
        c.setFillColor(GOLD2 if bg != GOLD else NAVY2)
        c.drawCentredString(tx+tw/2, CB+th-22, yr)
        c.setFont(KR, 10)
        c.setFillColor(WHITE if bg != GOLD else NAVY2)
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
    """3페이지 — 사업 모델 (Brand Curation)"""
    hdr(c, '사업 모델 — Brand Curation', 3)
    y = CT

    # 상단 메시지
    c.setFillColor(LGRAY)
    c.roundRect(MX, y-44, CW, 44, 4, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(MX, y-44, 4, 44, fill=1, stroke=0)
    c.setFont(KR, 13)
    c.setFillColor(NAVY)
    c.drawString(MX+14, y-18, 'Brand Curation — 단순 수출이 아닌, 바이어 입장의 시장 분석 기반 맞춤 제안')
    c.setFont(KR, 10)
    c.setFillColor(MID)
    c.drawString(MX+14, y-34,
        '바이어 시장·소비자 니즈 분석 → 제품·브랜드 큐레이션 → 신뢰 기반 장기 파트너십 → 반복 주문·컨설팅 마진')
    y -= 56

    # 좌측: 단순 수출 vs Brand Curation 비교
    lw = CW*0.46
    sec(c, MX, y, '비교 : 단순 수출 vs Brand Curation')
    cy = y - 30

    # 헤더
    c.setFillColor(MGRAY)
    c.rect(MX, cy-22, lw/2, 22, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(MX+lw/2, cy-22, lw/2, 22, fill=1, stroke=0)
    c.setFont(KR, 11)
    c.setFillColor(NAVY2)
    c.drawCentredString(MX+lw/4, cy-15, '단순 수출')
    c.setFillColor(GOLD2)
    c.drawCentredString(MX+lw*3/4, cy-15, 'Brand Curation (당사)')
    cy -= 22

    rows = [
        ('가격 경쟁 중심', '바이어 입장 시장 분석'),
        ('1회성 거래',     '장기 파트너십'),
        ('마진율 낮음',     '컨설팅 마진 + 안정 거래선'),
        ('범용 제품',       '맞춤 제품·브랜드 제안'),
    ]
    rrh = 26
    for i, (a, b) in enumerate(rows):
        bg = WHITE if i%2==0 else LGRAY
        c.setFillColor(bg)
        c.rect(MX, cy-rrh, lw, rrh, fill=1, stroke=0)
        c.setStrokeColor(MGRAY)
        c.setLineWidth(0.4)
        c.rect(MX, cy-rrh, lw, rrh, fill=0, stroke=1)
        c.line(MX+lw/2, cy-rrh, MX+lw/2, cy)
        c.setFont(KR, 10)
        c.setFillColor(MID)
        c.drawCentredString(MX+lw/4, cy-rrh+8, a)
        c.setFillColor(NAVY)
        c.drawCentredString(MX+lw*3/4, cy-rrh+8, b)
        cy -= rrh

    # 우측: 주력 품목 + 거래처
    rx = MX + lw + 16
    rw = CW - lw - 16
    ry = y
    sec(c, rx, ry, '주력 품목 & 거래처')
    ry -= 30

    cats = [
        ('① 화장품',      NAVY,  'K-뷰티 — 핵심 매출원\n프리미엄·자연주의 라인'),
        ('② 식품',        BLUE,  'K-푸드 — 안정 카테고리\n프랜차이즈·대형마트 입점'),
        ('③ 기계',        TEAL,  '산업·가전\n수요 기반 큐레이션'),
        ('④ 해외 컨설팅',  PURPLE,'바이어 진출 컨설팅\n부가 마진 확보'),
    ]
    cw_l = (rw-8)/2
    ch_l = 50
    for i, (t, bg, body) in enumerate(cats):
        col = i % 2
        row = i // 2
        cx = rx + col*(cw_l+8)
        cy = ry - row*(ch_l+8)
        c.setFillColor(bg)
        c.roundRect(cx, cy-ch_l, cw_l, ch_l, 4, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.rect(cx, cy-ch_l, 4, ch_l, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(GOLD2)
        c.drawString(cx+12, cy-18, t)
        c.setFont(KR, 9)
        c.setFillColor(WHITE)
        py = cy-32
        for ln in body.split('\n'):
            c.drawString(cx+12, py, ln)
            py -= 11

    # 하단: 거래처 & 확장
    c.setFillColor(GOLD)
    c.rect(MX, CB, CW, 30, fill=1, stroke=0)
    c.setFont(KR, 11)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, CB+18,
        '현재 거래처 : 유럽 Franchise Shop · 대형마트   |   확장 (2026~) : 미국 온라인 플랫폼 · 해외 인플루언서')
    c.setFont(KR, 9)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, CB+5, '* 수출실적증명원 발급 가능 → 보증재단 수출 가산점 항목 충족')


def p4(c):
    """4페이지 — 시장 환경 · SWOT"""
    hdr(c, '시장 환경 · SWOT', 4)
    y = CT

    # 좌측: K-뷰티 EMEA 시장 트렌드
    lw = CW*0.46
    sec(c, MX, y, 'K-뷰티 EMEA 시장 트렌드')
    cy = y - 30

    trends = [
        (NAVY,  'K-뷰티 글로벌 수요',  'EMEA 프리미엄·자연주의 라인 지속 확대'),
        (BLUE,  '유럽 프랜차이즈',      'K-뷰티·K-푸드 입점 적극화'),
        (TEAL,  '미국 온라인 진입',     '아마존·세포라·이커머스 진입장벽 완화'),
        (PINK,  '인플루언서 마케팅',    'SNS·인플루언서로 신생 브랜드 글로벌 진출'),
    ]
    for i, (col, t, sub) in enumerate(trends):
        iy = cy - i*42
        c.setFillColor(LGRAY)
        c.roundRect(MX, iy-38, lw, 36, 4, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(MX, iy-38, 5, 36, 2, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(col)
        c.drawString(MX+14, iy-13, t)
        c.setFont(KR, 9)
        c.setFillColor(MID)
        c.drawString(MX+14, iy-28, sub)

    # 우측: SWOT 2x2
    rx = MX + lw + 16
    rw = CW - lw - 16
    ry = CT
    sec(c, rx, ry, 'SWOT 분석')
    ry -= 30

    sw_w = (rw-8)/2
    sw_h = (CT - 30 - CB - 8)/2
    swot = [
        ('S 강점', NAVY,
         'Brand Curation 차별화\n프랑스어·EMEA 언어 역량\n매출 급성장·흑자전환\n청정 신용 + 청년·여성 대표'),
        ('W 약점', ORANGE,
         '1인 기업 (인력 한계)\n자체 브랜드·연구소·특허 부재\n자체 디지털 인프라 미구축'),
        ('O 기회', GREEN,
         'K-뷰티 글로벌 확산\n미국 온라인 진입\nEMEA 입점 가속\n청년·여성 정책 우대'),
        ('T 위협', ROSE,
         'EUR/USD 환율 변동\n경쟁 심화\n글로벌 공급·물류 리스크'),
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
            py -= 12


def p5(c):
    """5페이지 — 매출 급성장 서사 (★ 핵심)"""
    hdr(c, '매출 급성장 서사  ★', 5)

    # 골드 서브 배너
    c.setFillColor(GOLD)
    c.rect(0, SH-HDR-26, SW, 24, fill=1, stroke=0)
    c.setFont(KR, 12)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, SH-HDR-15,
        '매출 7.5배 급성장 + 흑자전환  →  2026 기본 15억 / 공격 20억')

    y = CT - 32

    # 상단 KPI 4개
    kw = (CW-24)//4
    kh = 70
    kpi(c, MX,            y, kw, kh, '2024 매출', '1.15억', '결손', NAVY2, LBLUE, GOLD2)
    kpi(c, MX+(kw+8),     y, kw, kh, '2025 매출', '8.6억',  '흑자전환',  GREEN, LBLUE, GOLD2)
    kpi(c, MX+(kw+8)*2,   y, kw, kh, '성장 배수', 'x 7.5', '24→25 매출', BLUE,  LBLUE, GOLD2)
    kpi(c, MX+(kw+8)*3,   y, kw, kh, '2026 목표', '15~20억',  '기본·공격 시나리오', ROSE,  LBLUE, GOLD2)
    y -= kh + 14

    # 매출 추이 막대 차트 (좌측)
    lw = CW*0.55
    sec(c, MX, y, '매출 추이 (단위: 억)')
    cy = y - 30

    bars_data = [
        ('2023', 0.75,  '0.75억', '결손',     MGRAY),
        ('2024', 1.15,  '1.15억', '결손',     ORANGE),
        ('2025', 8.6,   '8.6억',  '흑자전환', GREEN),
        ('26.1Q', 2.0,  '2.0억',  '진행중',   BLUE),
        ('2026목표', 20.0, '20억', '계획',    GOLD),
    ]
    max_val = 22
    chart_h = cy - CB - 70
    chart_w = lw - 60
    bar_w = chart_w / len(bars_data) - 12
    base_y = CB + 30
    for i, (label, val, vstr, status, col) in enumerate(bars_data):
        bx = MX + 50 + i*(bar_w+12)
        bh = max(8, chart_h * (val/max_val))
        c.setFillColor(col)
        c.roundRect(bx, base_y, bar_w, bh, 3, fill=1, stroke=0)
        # 값 라벨
        c.setFont(KR, 11)
        c.setFillColor(NAVY)
        c.drawCentredString(bx+bar_w/2, base_y+bh+5, vstr)
        # X축 라벨
        c.setFont(KR, 10)
        c.setFillColor(DGRAY)
        c.drawCentredString(bx+bar_w/2, base_y-14, label)
        c.setFont(KR, 8)
        c.setFillColor(MID)
        c.drawCentredString(bx+bar_w/2, base_y-26, status)
    # X축 베이스라인
    c.setStrokeColor(MGRAY)
    c.setLineWidth(0.8)
    c.line(MX+30, base_y, MX+lw-10, base_y)

    # 우측: 1년 내 20억 달성 근거
    rx = MX + lw + 16
    rw = CW - lw - 16
    ry = y
    sec(c, rx, ry, '20억 달성 근거 (3대 동력)')
    ry -= 30

    drivers = [
        ('1Q 신규+기존 거래처 주문',  '현재 2.0억 진행 중', NAVY),
        ('온라인 B2B몰 수출\n(K-beauty4U)',     '가동 후 6~9개월 시차\n분기당 2~3억 단계 진입', BLUE),
        ('자체 브랜드 출시',         '하반기 매출 기여',   TEAL),
    ]
    for i, (t, sub, col) in enumerate(drivers):
        iy = ry - i*60
        c.setFillColor(col)
        c.roundRect(rx, iy-54, rw, 52, 4, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.rect(rx, iy-54, 4, 52, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(GOLD2)
        py = iy - 14
        for ln in t.split('\n'):
            c.drawString(rx+12, py, ln)
            py -= 13
        c.setFont(KR, 10)
        c.setFillColor(LBLUE)
        c.drawString(rx+12, iy-46, sub)


def p6(c):
    """6페이지 — 자금 사용 계획 (3대 사용처)"""
    hdr(c, '자금 사용 계획 — 3대 사용처', 6)

    # 골드 서브 배너
    c.setFillColor(GOLD)
    c.rect(0, SH-HDR-26, SW, 24, fill=1, stroke=0)
    c.setFont(KR, 12)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, SH-HDR-15,
        '신용보증재단 보증 1.5억  →  운영자금 1억 + 시설·창업자금 0.5억 (트랙 분리 신청)')

    y = CT - 32

    # 자금 흐름도
    sec(c, MX, y, '자금 조달 흐름도')
    y -= 30

    flow = [
        ('신용보증재단',  '보증서 발급\n1.5억 원',     NAVY),
        ('협력 은행',     '여신 실행\n1.5억 원',       BLUE),
        ('(주)뉴허브',    '자금 수령\n3대 사용처 집행',  TEAL),
        ('사업 확장',     '디지털 인프라\n+ 자체 브랜드', GOLD),
    ]
    fw = (CW - 3*22) / 4
    fh = 56
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
        py = y-36
        for ln in sub.split('\n'):
            c.drawCentredString(fx+fw/2, py, ln)
            py -= 11
        if i < 3:
            c.setFont(KR, 18)
            c.setFillColor(GOLD)
            c.drawCentredString(fx+fw+11, y-fh/2-6, '▶')
    y -= fh + 14

    # 도넛 차트 + 3대 사용처 카드
    sec(c, MX, y, '3대 사용처 분배 (예시 — 회사 측 보정)')
    y -= 30

    # 도넛 차트 (좌측)
    cx, cy = MX + 90, CB + 78
    r_out, r_in = 64, 34
    segments = [
        ('K-connect hub',    0.30, NAVY,  '4,500만'),
        ('K-beauty4U',       0.40, BLUE,  '6,000만'),
        ('자체 브랜드',       0.30, TEAL,  '4,500만'),
    ]
    start = 90
    for lbl, pct, col, val in segments:
        end = start - pct*360
        donut_segment(c, cx, cy, r_out, r_in, start, end, col)
        start = end
    # 도넛 중앙 텍스트
    c.setFont(KR, 10)
    c.setFillColor(NAVY)
    c.drawCentredString(cx, cy+6, '총 보증액')
    c.setFont(KR, 15)
    c.setFillColor(GOLD)
    c.drawCentredString(cx, cy-12, '1.5억 원')

    # 우측 3대 카드
    lx = MX + 180
    cwx = CW - 180
    card_w = (cwx - 16)/3
    card_h = 130
    cards = [
        ('① K-connect hub', NAVY, GOLD2,
         '자사 온라인 웹사이트\n한·영·불·아랍 4개 언어\n글로벌 바이어 진입점',
         '4,500만원 (30%)', '운영자금'),
        ('② K-beauty4U', BLUE, GOLD2,
         'EMEA 화장품 Online\nB2B 편집샵 사이트 개발\n바이어 자동 주문 처리',
         '6,000만원 (40%)', '운영 + 시설성'),
        ('③ 자체 브랜드', TEAL, GOLD2,
         '자사 브랜드 화장품\n개발·생산 (기획 완료)\nOEM 우선 검토',
         '4,500만원 (30%)', '시설 + 운영자금'),
    ]
    for i, (t, bg, fg, body, amt, kind) in enumerate(cards):
        cxc = lx + i*(card_w+8)
        c.setFillColor(bg)
        c.roundRect(cxc, CB+6, card_w, card_h, 5, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(cxc, CB+6+card_h-5, card_w, 5, 2, fill=1, stroke=0)
        c.setFont(KR, 12)
        c.setFillColor(fg)
        c.drawString(cxc+10, CB+6+card_h-22, t)
        c.setStrokeColor(colors.HexColor('#FFFFFF40'))
        c.setLineWidth(0.5)
        c.line(cxc+10, CB+6+card_h-30, cxc+card_w-10, CB+6+card_h-30)
        c.setFont(KR, 9)
        c.setFillColor(WHITE)
        py = CB+6+card_h-46
        for ln in body.split('\n'):
            c.drawString(cxc+10, py, ln)
            py -= 12
        c.setFont(KR, 12)
        c.setFillColor(GOLD2)
        c.drawString(cxc+10, CB+22, amt)
        c.setFont(KR, 8)
        c.setFillColor(LBLUE)
        c.drawString(cxc+10, CB+10, kind)

    # 보정 표시
    c.setFont(KR, 8)
    c.setFillColor(MID)
    c.drawString(MX, CB-6, '* 분배 비율 30·40·30은 예시 — 회사 측 사업계획 확정 후 보정 [회사 기재]')


def p7(c):
    """7페이지 — 매출 전망·1년 20억 근거"""
    hdr(c, '매출 전망 · 20억 근거', 7)
    y = CT

    # 상단 KPI
    kw = (CW-16)//3
    kh = 68
    kpi(c, MX,          y, kw, kh, '2025 매출', '8.6억',  '흑자전환 입증', NAVY,  LBLUE, GOLD2)
    kpi(c, MX+kw+8,     y, kw, kh, '2026 목표', '15억',   '기본 (메인) — 가동 시차 반영', GREEN, LBLUE, GOLD2)
    kpi(c, MX+(kw+8)*2, y, kw, kh, '성장 배수', 'x 2.3',  '디지털+자체브랜드', BLUE,  LBLUE, GOLD2)
    y -= kh + 14

    # 분기별 매출 전망 표
    sec(c, MX, y, '2026 분기별 매출 전망')
    y -= 28
    rows = [
        ('1Q (확정)',  '2.0억',  '기존 거래처 + 신규',                  '진행중'),
        ('2Q',         '2.5억',  'K-connect hub 구축·1차 가동 (런칭 시차)',     '계획'),
        ('3Q',         '4.5억',  'K-beauty4U B2B 편집샵 트래픽 확보 단계',     '계획'),
        ('4Q',         '6.0억',  '자체 브랜드 시제품 출시 + 미국 진출 초기',     '계획'),
        ('보수 합계',   '15.0억', '기본 시나리오 (메인) — 가동 시차 반영',      '기본'),
        ('연 합계',     '20.0억', '기본 시나리오',                       '목표'),
    ]
    tbl(c, MX, y, ['분기', '매출 전망', '동력', '구분'],
        rows, [110, 130, CW-380, 140], rh=22, hh=24, highlight_last=True)
    y -= 22*5 + 24 + 14

    # 좌측: 채널별 분해 / 우측: 시나리오
    lw = CW*0.5
    sec(c, MX, y, '채널별 매출 분해 (2026)')
    cy = y - 28
    channels = [
        ('유럽 프랜차이즈·대형마트 (기존)', 0.60, '약 12억', NAVY),
        ('신규 미국 온라인·인플루언서',     0.25, '약 5억',  BLUE),
        ('자체 브랜드',                    0.15, '약 3억',  TEAL),
    ]
    for i, (lbl, pct, val, col) in enumerate(channels):
        iy = cy - i*30
        c.setFont(KR, 10)
        c.setFillColor(DGRAY)
        c.drawString(MX, iy-3, lbl)
        c.setFillColor(LGRAY)
        c.roundRect(MX, iy-22, lw-90, 12, 6, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(MX, iy-22, (lw-90)*pct, 12, 6, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(NAVY)
        c.drawString(MX+lw-86, iy-19, val)

    rx = MX + lw + 16
    rw = CW - lw - 16
    ry = y
    sec(c, rx, ry, '시나리오 분석')
    ry -= 28
    scenarios = [
        ('보수', '15억', '기존 채널 + 디지털 일부',     ORANGE),
        ('기본', '20억', '계획대로 달성',              GREEN),
        ('낙관', '25억', '자체 브랜드·미국 조기 성공', BLUE),
    ]
    for i, (lbl, val, sub, col) in enumerate(scenarios):
        iy = ry - i*30
        c.setFillColor(col)
        c.roundRect(rx, iy-26, rw, 26, 4, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(GOLD2)
        c.drawString(rx+12, iy-15, lbl)
        c.setFont(KR, 13)
        c.setFillColor(WHITE)
        c.drawString(rx+62, iy-15, val)
        c.setFont(KR, 9)
        c.setFillColor(LBLUE)
        c.drawString(rx+130, iy-15, sub)


def p8(c):
    """8페이지 — 일자리 창출 효과"""
    hdr(c, '일자리 창출 효과', 8)
    y = CT

    # 상단 메시지
    c.setFillColor(GOLD)
    c.rect(MX, y-32, CW, 32, fill=1, stroke=0)
    c.setFont(KR, 13)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, y-20,
        '1인 기업 → 6개월 이내 1~2명 채용  |  청년·여성 우대 가산점 다수 적용')
    y -= 46

    # 신규 채용 카드 2개
    sec(c, MX, y, '신규 채용 계획')
    y -= 30

    new_hires = [
        ('① 디지털 마케팅', NAVY,
         '직무: K-connect hub · K-beauty4U 운영',
         '시점: 2026년 Q2 ~ Q3',
         '대상: 청년/여성 (보증재단 우대)',
         '기대 효과: 디지털 채널 매출 견인'),
        ('② 해외 영업', BLUE,
         '직무: 유럽·미국 거래선 관리·신규 파트너 발굴',
         '시점: 2026년 Q3 ~ Q4',
         '대상: 청년/경력자 (보증재단 우대)',
         '기대 효과: 미국 진출·자체 브랜드 채널 확보'),
    ]
    cw_h = (CW-12)//2
    ch_h = 124
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

    # 하단: 보증재단 우대 가점 항목
    sec(c, MX, y, '보증재단 우대 가점 항목')
    y -= 28

    pts = [
        (GREEN,  '청년 채용 (만 39세 이하)'),
        (BLUE,   '여성 채용'),
        (GOLD,   '신규 일자리 창출 (보증한도 우대)'),
        (ROSE,   '청년·여성 창업기업'),
        (TEAL,   '수출 B2B 기업'),
    ]
    bx = MX
    for col, t in pts:
        pw = c.stringWidth(t, KR, 10) + 24
        c.setFillColor(col)
        c.roundRect(bx, y-22, pw, 22, 11, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(WHITE if col != GOLD else NAVY2)
        c.drawCentredString(bx+pw/2, y-15, t)
        bx += pw + 8


def p9(c):
    """9페이지 — 위험 요소 · 대응"""
    hdr(c, '위험 요소 · 대응 전략', 9)
    y = CT

    risks = [
        ('① EUR/USD 환율 리스크', ROSE, NAVY,
         ['결제 통화·시점 분산 (EUR/USD 혼합 결제)',
          '거래선과 가격 조정 조항 협의',
          '단가 마진 버퍼 확보 (Brand Curation 마진)',
          '환율 사이클 대응 — 7년 사업 경험']),
        ('② K-뷰티 경쟁 심화', ORANGE, NAVY,
         ['Brand Curation 차별화 — 단순 가격 경쟁 회피',
          '4개 언어 사이트로 진입장벽 차별화',
          '자체 브랜드 자산화로 장기 차별화',
          'EMEA 언어 역량 (프랑스어·아랍어 등)']),
        ('③ 디지털 마케팅 효과 불확실', GOLD, NAVY,
         ['단계적 투자 — 시범 운영 → 효과 검증 → 확대',
          '인플루언서 협업 검증 후 본격화',
          '매출 채널 다변화 (B2B + 자체몰)',
          '기존 거래처 매출 안정성 유지']),
        ('④ 자체 브랜드 진입 리스크', TEAL, NAVY,
         ['OEM 우선 검토 — 자가 설비 부담 최소화',
          '시제품 → 시장 테스트 → 본격 양산 단계',
          '실패 시에도 수입유통 기존 매출 유지',
          '단계적 자금 투입 (전체 30% 우선)']),
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
    """10페이지 — 자금 조달 · 상환 계획"""
    hdr(c, '자금 조달 · 상환 계획', 10)
    y = CT

    # 상단 상환 가정 표
    sec(c, MX, y, '상환 가정 및 부담 계산')
    y -= 28

    rows = [
        ('보증액',           '150,000,000원',  '신용보증재단 보증한도'),
        ('대출금리 (가정)',  '연 4.0%',        '협력은행 우대금리 [추정]'),
        ('상환기간',         '5년 (60개월)',   '거치 6개월 + 분할상환 4.5년 [협의]'),
        ('보증료 (연)',       '약 1,200,000원', '보증액 × 0.8% (지역신보 표준)'),
        ('월 원리금',         '약 3,580,000원', '거치 후 분할상환 [추정]'),
        ('연 상환 부담',       '약 43,000,000원','원리금 + 보증료 [추정]'),
    ]
    tbl(c, MX, y, ['항목', '금액 / 조건', '산출 근거'],
        rows, [180, 200, CW-380], rh=22, hh=24, lcols={2})
    y -= 22*6 + 24 + 14

    # DSCR 분석
    sec(c, MX, y, 'DSCR (부채상환능력) 분석 — 보수적 추정')
    y -= 28

    # 좌: 수치 박스
    lw = CW*0.42
    c.setFillColor(NAVY)
    c.roundRect(MX, y-90, lw, 90, 5, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.roundRect(MX, y-5, lw, 5, 2, fill=1, stroke=0)
    c.setFont(KR, 11)
    c.setFillColor(LBLUE)
    c.drawCentredString(MX+lw/2, y-22, 'DSCR 추정 (보수)')
    c.setFont(KR, 32)
    c.setFillColor(GOLD2)
    c.drawCentredString(MX+lw/2, y-56, '1.2 ~ 1.8 배')
    c.setFont(KR, 9)
    c.setFillColor(LBLUE)
    c.drawCentredString(MX+lw/2, y-72, '영업이익률 7~12% 가정 감도분석')
    c.drawCentredString(MX+lw/2, y-83, '2025 영업이익 [회사 기재] 확정 후 최종 산정')

    # 우: 청정 신용 + 비상 시나리오
    rx = MX + lw + 16
    rw = CW - lw - 16
    c.setFillColor(LGRAY)
    c.roundRect(rx, y-90, rw, 90, 5, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.roundRect(rx, y-5, rw, 5, 2, fill=1, stroke=0)
    c.setFont(KR, 12)
    c.setFillColor(NAVY)
    c.drawString(rx+14, y-22, '청정 신용 + 비상 상환 시나리오')
    scenarios = [
        '• 무차입 (법인 차입 0, 정책자금 기대출 0)',
        '• 무체납·무연체 (국세·지방세·4대보험)',
        '• 2025년 8.6억 매출 — 안정 현금흐름 확보',
        '• 수출 매출채권 담보 여력 + 재고 자산',
    ]
    py = y-40
    c.setFont(KR, 10)
    c.setFillColor(DGRAY)
    for s in scenarios:
        c.drawString(rx+14, py, s)
        py -= 14
    y -= 90 + 12

    # 하단 결론
    c.setFillColor(GOLD)
    c.roundRect(MX, CB, CW, 26, 4, fill=1, stroke=0)
    c.setFont(KR, 11)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, CB+8,
        'DSCR 1.2~1.8배 (보수·감도)  |  무차입 청정 신용 + 무체납  |  신용 적격성 양호 (영업이익 확정 후 최종 산정)')


def p11(c):
    """11페이지 — 사업 비전 · 요약 (Closing)"""
    c.setFillColor(NAVY2)
    c.rect(0, 0, SW, SH, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, SH-7, SW, 7, fill=1, stroke=0)
    c.rect(0, 0, SW, 6, fill=1, stroke=0)

    # 상단 비전 메시지
    c.setFont(KR, 13)
    c.setFillColor(GOLD2)
    c.drawCentredString(SW/2, SH-46, 'Vision 2026 ~ 2027')
    c.setFont(KR, 20)
    c.setFillColor(WHITE)
    c.drawCentredString(SW/2, SH-78,
        '2025 흑자전환 + 1.5억 보증  →  2026 매출 20억 + 디지털 인프라 + 자체 브랜드')

    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(SW/2-260, SH-94, SW/2+260, SH-94)

    # 핵심 요약 3박스
    cy = SH-130
    bw = (SW - 2*MX - 24) // 3
    bh = 110
    summary = [
        ('보증 활용', '1.5억 원',
         'K-connect hub\n+ K-beauty4U\n+ 자체 브랜드',
         BLUE),
        ('매출 도약', '8.6 → 20억',
         '2025 → 2026\n2.3배 성장\n흑자전환 입증',
         TEAL),
        ('일자리 창출', '+1~2명',
         '디지털 마케팅 1명\n해외 영업 1명\n청년·여성 우대',
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
        c.setFont(KR, 22)
        c.setFillColor(GOLD2)
        c.drawCentredString(bx+bw/2, cy-50, val)
        c.setFont(KR, 10)
        c.setFillColor(WHITE)
        py = cy-72
        for ln in body.split('\n'):
            c.drawCentredString(bx+bw/2, py, ln)
            py -= 12

    # 5대 강점 미니 배지
    by = cy - bh - 24
    c.setFont(KR, 12)
    c.setFillColor(GOLD2)
    c.drawCentredString(SW/2, by, '5대 강점')
    by -= 22
    badges_data = [
        ('매출 7.5배 급성장', GREEN),
        ('청년·여성 창업', PINK),
        ('청정 신용', BLUE),
        ('수출 B2B 입증', TEAL),
        ('디지털+자체브랜드', GOLD),
    ]
    total_w = sum(c.stringWidth(t, KR, 10)+22 for t, _ in badges_data) + (len(badges_data)-1)*6
    bx = (SW - total_w) / 2
    for t, col in badges_data:
        pw = c.stringWidth(t, KR, 10) + 22
        c.setFillColor(col)
        c.roundRect(bx, by-20, pw, 20, 10, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(WHITE if col != GOLD else NAVY2)
        c.drawCentredString(bx+pw/2, by-14, t)
        bx += pw + 6

    # 마무리 문구
    c.setFont(KR, 32)
    c.setFillColor(WHITE)
    c.drawCentredString(SW/2, 130, 'THANK YOU.')
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(SW/2-120, 112, SW/2+120, 112)

    c.setFont(KR, 13)
    c.setFillColor(GOLD2)
    c.drawCentredString(SW/2, 92, COMPANY)
    c.setFont(KR, 9)
    c.setFillColor(LBLUE)
    c.drawCentredString(SW/2, 78, COMPANY_EN)
    c.setFont(KR, 9)
    c.setFillColor(MGRAY)
    c.drawCentredString(SW/2, 60, '대표이사 [회사 기재]   |   T. [회사 기재]   |   E. [회사 기재]')
    c.drawCentredString(SW/2, 48, '서울시 강서구 마곡 중앙1로 10. 802호')

    c.setFont(KR, 9)
    c.setFillColor(GOLD2)
    c.drawCentredString(SW/2, 30, BRAND_TAG)

    c.setFont(KR, 8)
    c.setFillColor(MID)
    c.drawCentredString(SW/2, 14,
        '본 사업계획서는 회사 측 보정 자료(NICE 등급 · 재무제표 분기 · 대표이력) 반영 후 최종본으로 완성됩니다. 매출 전망은 회사 자체 추정이며 보증재단 심사 결과를 보장하지 않습니다.')


# ══════════════════════════════════════════════════════════════════════
def build():
    out = Path(__file__).parent / f'{COMPANY}_정책자금사업계획서_{datetime.date.today().strftime("%Y%m%d")}.pdf'
    cv = pdfcanvas.Canvas(str(out), pagesize=(SW, SH))
    cv.setTitle(f'{COMPANY} 정책자금 사업계획서')
    cv.setAuthor('히어컴퍼니 (HearCompany) Corporate Consulting')
    cv.setSubject('신용보증재단 보증신청용')
    cv.setKeywords('정책자금, 신용보증재단, 보증, K-뷰티, 수출, Brand Curation')
    for fn in [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]:
        fn(cv)
        cv.showPage()
    cv.save()
    print(f'[OK] {out}')
    print(f'     size: {out.stat().st_size:,} bytes')

if __name__ == '__main__':
    build()
