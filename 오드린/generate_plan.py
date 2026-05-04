"""
오드린 농업회사법인(주) — 정책자금용 사업계획서
16:9 슬라이드 / 인포그래픽 중심 / 전체 고딕 폰트
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
ROSE   = colors.HexColor('#E11D48')

# ── 슬라이드 규격 ─────────────────────────────────────────────────────
SW, SH = 960, 540
MX = 32          # 좌우 여백
HDR = 62         # 헤더 높이
FTR = 20         # 푸터 높이
CT  = SH - HDR - 8   # 콘텐츠 최상단 y
CB  = FTR + 6        # 콘텐츠 최하단 y
CW  = SW - 2*MX      # 콘텐츠 폭 = 896


# ══════════════════════════════════════════════════════════════════════
# 공통 헬퍼
# ══════════════════════════════════════════════════════════════════════

def W(c, text, max_w, size):
    """텍스트를 max_w에 맞게 줄 분리 (한국어 character-wrap)"""
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
    """텍스트 블록 그리기. 마지막 y 반환."""
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
    # 좌측 GOLD 강조바
    c.setFillColor(GOLD)
    c.rect(0, SH-HDR, 8, HDR, fill=1, stroke=0)
    # 하단 구분선
    c.setFillColor(GOLD)
    c.rect(0, SH-HDR-3, SW, 3, fill=1, stroke=0)
    # 제목 텍스트
    c.setFont(KR, 22)
    c.setFillColor(WHITE)
    c.drawString(MX+4, SH-HDR+20, title)
    # 페이지 번호 (우측 상단)
    c.setFont(KR, 11)
    c.setFillColor(LBLUE)
    c.drawRightString(SW-MX, SH-HDR+22, f'{pg} / 11')
    # 하단 footer
    c.setFont(KR, 9)
    c.setFillColor(MID)
    c.drawCentredString(SW/2, 7, '오드린 농업회사법인(주)')

def sec(c, x, y, text, w=None, bg=NAVY, fg=WHITE, size=13):
    """섹션 레이블 박스. 높이 반환."""
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
    """KPI 카드 — 대형 수치 강조"""
    # 그림자 효과
    c.setFillColor(colors.HexColor('#0A1929'))
    c.roundRect(x+3, y-h-2, w, h, 6, fill=1, stroke=0)
    # 본체
    c.setFillColor(bg)
    c.roundRect(x, y-h, w, h, 6, fill=1, stroke=0)
    # 상단 골드 라인
    c.setFillColor(GOLD)
    c.roundRect(x, y-4, w, 4, 2, fill=1, stroke=0)
    # 레이블
    c.setFont(KR, 10)
    c.setFillColor(label_col)
    c.drawCentredString(x+w/2, y-18, label)
    # 수치 (매우 크게)
    c.setFont(KR, 26)
    c.setFillColor(val_col)
    c.drawCentredString(x+w/2, y-h/2-2, value)
    # 서브
    if sub:
        c.setFont(KR, 9)
        c.setFillColor(sub_col)
        c.drawCentredString(x+w/2, y-h+10, sub)

def tbl(c, x, y, hdrs, rows, ws, rh=26, hh=28, lcols=None):
    """표. y = 헤더 상단. 바닥 y 반환."""
    lcols = lcols or set()
    tw = sum(ws)
    # 헤더
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
        bg = WHITE if ri%2==0 else LGRAY
        c.setFillColor(bg)
        c.rect(x, y-rh, tw, rh, fill=1, stroke=0)
        c.setStrokeColor(MGRAY)
        c.setLineWidth(0.4)
        c.rect(x, y-rh, tw, rh, fill=0, stroke=1)
        cx = x
        for ci, (v, w) in enumerate(zip(row, ws)):
            col = NAVY if ci==0 else (GOLD if ri==len(rows)-1 and ci==len(ws)-1 else DGRAY)
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
    """가로 진행률 바"""
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
    """배지 (태그)"""
    pw = c.stringWidth(text, KR, size)+16
    ph = size+10
    c.setFillColor(bg)
    c.roundRect(x, y-ph, pw, ph, ph//2, fill=1, stroke=0)
    c.setFont(KR, size)
    c.setFillColor(fg)
    c.drawCentredString(x+pw/2, y-ph+5, text)
    return pw+5

def num_circle(c, cx, cy, r, num, bg=GOLD, fg=NAVY, size=16):
    """번호 원"""
    c.setFillColor(bg)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFont(KR, size)
    c.setFillColor(fg)
    c.drawCentredString(cx, cy-size*0.38, str(num))

def div(c, y, x1=None, x2=None):
    c.setStrokeColor(MGRAY)
    c.setLineWidth(0.7)
    c.line(x1 or MX, y, x2 or SW-MX, y)


# ══════════════════════════════════════════════════════════════════════
# 페이지 함수
# ══════════════════════════════════════════════════════════════════════

def p1(c):
    # ── 배경 ──────────────────────────────────────────────────────────
    c.setFillColor(NAVY2)
    c.rect(0, 0, SW, SH, fill=1, stroke=0)
    # 상단/하단 골드 바
    c.setFillColor(GOLD)
    c.rect(0, SH-7, SW, 7, fill=1, stroke=0)
    c.rect(0, 0, SW, 6, fill=1, stroke=0)
    # 왼쪽 콘텐츠 영역 배경
    c.setFillColor(colors.HexColor('#142858'))
    c.roundRect(MX-10, 30, SW*0.55, SH-60, 8, fill=1, stroke=0)

    # ── 왼쪽 텍스트 ───────────────────────────────────────────────────
    c.setFont(KR, 13)
    c.setFillColor(LBLUE)
    c.drawString(MX+6, SH-60, '농업회사법인')

    c.setFont(KR, 32)
    c.setFillColor(WHITE)
    c.drawString(MX+6, SH-98, '오드린(주)')

    c.setFillColor(GOLD)
    c.rect(MX+6, SH-110, 200, 3, fill=1, stroke=0)

    c.setFont(KR, 13)
    c.setFillColor(LBLUE)
    c.drawString(MX+6, SH-128, '국내산 포도 100%  프리미엄 와인 제조 · 판매')

    c.setFont(KR, 44)
    c.setFillColor(GOLD2)
    c.drawString(MX+6, SH-195, '사 업 계 획 서')

    c.setFont(KR, 12)
    c.setFillColor(MGRAY)
    c.drawString(MX+6, SH-222, f'브랜드  월류봉 · 베베마루     {datetime.date.today()}')

    c.setFont(KR, 12)
    c.setFillColor(MID)
    c.drawString(MX+6, 36, 'T. 010-2466-7789')

    # ── 오른쪽 KPI 박스 4개 ───────────────────────────────────────────
    rx = int(SW*0.60)
    rw = SW - rx - MX
    kh = (SH-60)//2 - 8
    kw = (rw-8)//2

    items = [
        ('설립 연도',   '2022', '년', NAVY,  LBLUE, GOLD2),
        ('와인 브랜드', '2',    '개', BLUE,  LBLUE, GOLD2),
        ('특허',        '2',    '건', TEAL,  LBLUE, GOLD2),
        ('수상 이력',   '5+',   '회', ROSE,  LBLUE, GOLD2),
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
    hdr(c, '주요 사업 소개', 2)
    y = CT

    # ── 상단: 핵심 메시지 배너 ────────────────────────────────────────
    c.setFillColor(LGRAY)
    c.roundRect(MX, y-42, CW, 42, 4, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(MX, y, MX, y-42)
    c.setFont(KR, 13)
    c.setFillColor(NAVY)
    c.drawString(MX+14, y-17,
        '3대째 포도농장 운영의 전통과 현대 양조학을 결합한 프리미엄 와이너리')
    c.setFont(KR, 11)
    c.setFillColor(MID)
    c.drawString(MX+14, y-34, '국내산 포도 100% 사용  |  와인명인 양조  |  특허 기술 보유')
    y -= 52

    # ── 중간: 사업 구조 플로우 ─────────────────────────────────────────
    sec(c, MX, y, '사업 구조')
    y -= 30

    steps = [
        ('🌿', '포도 재배\n& 수매'),
        ('🍷', '양조·발효\n숙성'),
        ('🏷', '병입\n라벨링'),
        ('🛒', '온라인\n판매'),
        ('🤝', 'B2B\n수출'),
    ]
    sw = (CW - (len(steps)-1)*6) / len(steps)
    sx = MX
    for i, (icon, txt) in enumerate(steps):
        bg = NAVY if i % 2 == 0 else BLUE
        c.setFillColor(bg)
        c.roundRect(sx, y-52, sw, 52, 5, fill=1, stroke=0)
        # 상단 GOLD 라인
        c.setFillColor(GOLD)
        c.rect(sx, y-3, sw, 3, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(WHITE)
        for li, ln in enumerate(txt.split('\n')):
            c.drawCentredString(sx+sw/2, y-24-li*15, ln)
        sx += sw+6
        if i < len(steps)-1:
            c.setFont(KR, 14)
            c.setFillColor(GOLD)
            c.drawCentredString(sx-3, y-26, '▶')
    y -= 62

    # ── 하단: 브랜드 2개 + 핵심 키워드 ──────────────────────────────
    bw = (CW-12)//2
    for i, (brand, sub, prods, clr) in enumerate([
        ('월류봉', '프리미엄 라인 — 충북 영동 황간',  '레드 · 화이트 · 스파클링', NAVY),
        ('베베마루', '접근성 높은 일상 와인 라인', '로제 · 화이트', BLUE),
    ]):
        bx = MX + i*(bw+12)
        c.setFillColor(LGRAY)
        c.roundRect(bx, y-58, bw, 58, 5, fill=1, stroke=0)
        c.setFillColor(clr)
        c.roundRect(bx, y-5, bw, 5, 2, fill=1, stroke=0)
        c.setFont(KR, 17)
        c.setFillColor(clr)
        c.drawString(bx+14, y-24, brand)
        c.setFont(KR, 11)
        c.setFillColor(MID)
        c.drawString(bx+14, y-40, sub)
        # 제품 배지
        c.setFillColor(clr)
        pw = c.stringWidth(prods, KR, 10)+16
        c.roundRect(bx+14, y-56, pw, 16, 8, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(WHITE)
        c.drawCentredString(bx+14+pw/2, y-50, prods)


def p3(c):
    hdr(c, '핵심 강점 & 기술력', 3)
    y = CT

    # ── 4개 강점 카드 (2×2 그리드) ───────────────────────────────────
    cw = (CW-12)//2
    ch = (CT - CB - 34)//2

    data = [
        (1, '와인명인 고유 숙성 기술',
         '3대째 포도농장 운영으로 축적된\n전통 양조 기법 + 현대 양조학 결합\n타 와이너리 모방 불가',
         NAVY, GOLD2),
        (2, '특허 기반 독점 레시피',
         '오미자과즙 로제와인 (특허등록)\n샤인머스켓 블랜딩와인 (특허출원)\n독점 레시피 2종 보유',
         BLUE, GOLD2),
        (3, '국내산 포도 100% 원료',
         '수입 포도즙·농축액 ZERO\n충북 영동 자체 재배 포도 사용\n진정한 한국 와인 가치 실현',
         TEAL, GOLD2),
        (4, '검증된 품질 인증 체계',
         'ISO 22000 인증\n한국식품연구원 품질인증\n아시아 와인트로피 수상',
         colors.HexColor('#7C3AED'), GOLD2),
    ]

    for i, (num, title, body, bg, nc) in enumerate(data):
        col = i % 2
        row = i // 2
        cx = MX + col*(cw+12)
        cy = y - row*(ch+10)

        # 카드 배경
        c.setFillColor(bg)
        c.roundRect(cx, cy-ch, cw, ch, 6, fill=1, stroke=0)
        # 상단 라인
        c.setFillColor(GOLD)
        c.roundRect(cx, cy-4, cw, 4, 2, fill=1, stroke=0)

        # 번호 원
        num_circle(c, cx+26, cy-28, 18, num, GOLD, NAVY, 15)

        # 제목
        c.setFont(KR, 14)
        c.setFillColor(WHITE)
        c.drawString(cx+54, cy-26, title)

        # 구분선
        c.setStrokeColor(colors.HexColor('#FFFFFF30'))
        c.setLineWidth(0.5)
        c.line(cx+12, cy-44, cx+cw-12, cy-44)

        # 본문
        T(c, body, cx+16, cy-60, cw-24, 11, LBLUE, 17)

    # ── 하단 요약 배너 ────────────────────────────────────────────────
    c.setFillColor(GOLD)
    c.rect(MX, CB, CW, 22, fill=1, stroke=0)
    c.setFont(KR, 11)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, CB+7,
        '특허 기술  ×  와인명인 숙성  ×  국내산 원료  ×  ISO 22000  —  4중 경쟁력')


def p4(c):
    hdr(c, '주요 실적 · 인증 · 수상', 4)
    y = CT

    lw = CW*0.50 - 8
    rw = CW - lw - 16
    rx = MX + lw + 16

    # ── 왼쪽: 특허·인증 ──────────────────────────────────────────────
    sec(c, MX, y, '특허 / 인증')
    y -= 30

    cert_items = [
        (TEAL,  '특허등록',   '오미자과즙 로제와인 제조방법'),
        (BLUE,  '특허출원',   '샤인머스켓 블랜딩와인 제조방법'),
        (NAVY,  'ISO 22000', '식품안전경영시스템'),
        (NAVY,  '와이너리인증','한국국제소믈리에협회장'),
        (NAVY,  '품질인증',   '한국식품연구원장'),
    ]
    for i, (clr, cat, cont) in enumerate(cert_items):
        iy = y - i*34
        c.setFillColor(LGRAY)
        c.roundRect(MX, iy-30, lw, 28, 4, fill=1, stroke=0)
        c.setFillColor(clr)
        c.roundRect(MX, iy-30, 5, 28, 2, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(clr)
        c.drawString(MX+14, iy-11, cat)
        c.setFont(KR, 11)
        c.setFillColor(DGRAY)
        c.drawString(MX+14+c.stringWidth(cat,KR,10)+8, iy-11, cont)

    # ── 오른쪽: 수상 ─────────────────────────────────────────────────
    ry = CT
    sec(c, rx, ry, '수상 내역')
    ry -= 30

    awards = [
        (GOLD,  '농림축산식품부장관상'),
        (GOLD,  '신지식농업인상'),
        (GOLD,  '3년 연속 주류대상'),
        (GOLD,  '2025 K-SUUL AWARD 우수상'),
        (GOLD,  'Asia Wine Trophy  Best Producer South Korea'),
    ]
    for i, (clr, aw) in enumerate(awards):
        ay = ry - i*34
        c.setFillColor(LGRAY)
        c.roundRect(rx, ay-30, rw, 28, 4, fill=1, stroke=0)
        c.setFillColor(clr)
        c.circle(rx+16, ay-16, 6, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(DGRAY)
        c.drawString(rx+28, ay-20, aw)

    # ── 하단 KPI 3개 ─────────────────────────────────────────────────
    kw = (CW-16)//3
    kh = 38
    bottom_y = CB + kh + 4
    for i, (lbl, val, bg) in enumerate([
        ('보유 특허', '2건', NAVY),
        ('품질 인증', '3건', BLUE),
        ('수상 횟수', '5회+', TEAL),
    ]):
        kx = MX + i*(kw+8)
        c.setFillColor(bg)
        c.roundRect(kx, CB, kw, kh, 4, fill=1, stroke=0)
        c.setFont(KR, 9)
        c.setFillColor(LBLUE)
        c.drawCentredString(kx+kw/2, CB+kh-12, lbl)
        c.setFont(KR, 18)
        c.setFillColor(GOLD2)
        c.drawCentredString(kx+kw/2, CB+8, val)


def p5(c):
    hdr(c, '대표자 소개', 5)
    y = CT

    # ── 프로필 배너 ───────────────────────────────────────────────────
    c.setFillColor(NAVY)
    c.roundRect(MX, y-60, CW, 60, 5, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(MX, y-60, 5, 60, fill=1, stroke=0)
    # 이름·직함
    c.setFont(KR, 28)
    c.setFillColor(WHITE)
    c.drawString(MX+18, y-30, '박천명  대표이사')
    c.setFont(KR, 12)
    c.setFillColor(LBLUE)
    c.drawString(MX+18, y-50, '오드린 농업회사법인(주)  |  와인명인  |  3대째 포도농장 운영')
    # 우측 뱃지
    bx = SW - MX - 3
    for tag in reversed(['와인명인', 'ISO 22000', '특허보유']):
        bw = c.stringWidth(tag, KR, 10) + 18
        bx -= bw
        c.setFillColor(BLUE)
        c.roundRect(bx, y-46, bw, 18, 9, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(WHITE)
        c.drawCentredString(bx+bw/2, y-38, tag)
        bx -= 6
    y -= 70

    # ── 경력 타임라인 (왼쪽) ─────────────────────────────────────────
    lw = CW*0.56
    sec(c, MX, y, '주요 경력')
    y -= 30

    careers = [
        ('3대째',     '포도농장 운영 — 충북 영동 황간 지역'),
        ('와인명인',  '전통 양조 기법 계승 + 현대 양조학 접목'),
        ('2022~현재', '오드린 농업회사법인(주) 설립 · 대표이사'),
        ('3년 연속',  '국내 주요 주류품평회 대상 수상'),
        ('2024',      'Asia Wine Trophy Best Producer South Korea'),
    ]
    for i, (period, content) in enumerate(careers):
        iy = y - i*30
        # 타임라인 점
        c.setFillColor(GOLD if i==0 or i==2 else BLUE)
        c.circle(MX+12, iy-11, 6, fill=1, stroke=0)
        # 연결선
        if i < len(careers)-1:
            c.setStrokeColor(MGRAY)
            c.setLineWidth(1.5)
            c.line(MX+12, iy-17, MX+12, iy-35)
        # 기간 레이블
        c.setFont(KR, 10)
        c.setFillColor(NAVY)
        c.drawString(MX+24, iy-15, period)
        pw = c.stringWidth(period, KR, 10)
        # 내용
        c.setFont(KR, 11)
        c.setFillColor(DGRAY)
        c.drawString(MX+24+pw+10, iy-15, content)

    # ── 오른쪽: 수상 배지 ────────────────────────────────────────────
    rx = MX + lw + 16
    rw = CW - lw - 16
    ry = CT - 70
    sec(c, rx, ry, '수상 / 인정')
    ry -= 30

    awards = [
        (GOLD,  '농림축산식품부장관상'),
        (GOLD,  '신지식농업인상'),
        (GOLD,  '3년 연속 주류대상'),
        (TEAL,  '2025 K-SUUL AWARD 우수상'),
        (ROSE,  'Asia Wine Trophy\nBest Producer S.Korea'),
    ]
    for lbl_col, aw in awards:
        c.setFillColor(LGRAY)
        c.roundRect(rx, ry-28, rw, 26, 4, fill=1, stroke=0)
        c.setFillColor(lbl_col)
        c.circle(rx+12, ry-15, 5, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(DGRAY)
        for li, ln in enumerate(aw.split('\n')):
            c.drawString(rx+24, ry-12-li*13, ln)
        ry -= 33


def p6(c):
    hdr(c, '시장 동향 & 매출 전망', 6)
    y = CT

    # ── 상단: 대형 KPI 3개 ───────────────────────────────────────────
    kw = (CW-16)//3
    kh = 90
    kpi(c, MX,          y, kw, kh, '국내 와인시장 규모', '13조 원', '2024년 기준', NAVY,  LBLUE, GOLD2)
    kpi(c, MX+kw+8,     y, kw, kh, '연평균 성장률',      '3.6 %',   'CAGR',        BLUE,  LBLUE, GOLD2)
    kpi(c, MX+(kw+8)*2, y, kw, kh, '국내산 와인 점유율', '극히 낮음','블루오션 시장', TEAL, LBLUE, GOLD2)
    y -= kh + 14

    # ── 시장 분석 요약 ────────────────────────────────────────────────
    c.setFillColor(LGRAY)
    c.roundRect(MX, y-38, CW, 38, 4, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(MX, y-38, 4, 38, fill=1, stroke=0)
    c.setFont(KR, 12)
    c.setFillColor(DGRAY)
    c.drawString(MX+14, y-14,
        '수입 와인 중심 시장에서 "국내산 포도 100% + 와인명인 양조"는 국내 거의 유일한 포지셔닝')
    c.setFont(KR, 11)
    c.setFillColor(MID)
    c.drawString(MX+14, y-30,
        'K-푸드 열풍 + 홈술 문화 정착 + 건강 지향 소비 → 프리미엄 국내산 와인 수요 성장 기대')
    y -= 48

    # ── 매출 추이 표 ─────────────────────────────────────────────────
    sec(c, MX, y, '오드린 매출 추이 및 목표')
    y -= 30

    rows = [
        ('2024 실적', '134,600,000원', '—',     '사업 초기 안정화'),
        ('2025 실적', '160,620,000원', '+19.3%', '온라인 채널 확대'),
        ('2026 목표', '250,000,000원', '+55.7%', '신제품 2라인 출시'),
        ('2027 목표', '350,000,000원', '+40.0%', 'B2B · 수출 본격화'),
    ]
    tbl(c, MX, y, ['연도', '매출액', '증감률', '비고'],
        rows, [120, 200, 90, CW-410], rh=26, hh=28)


def p7(c):
    hdr(c, '매출 향상 계획 (1)  ★', 7)

    # 서브 배너
    c.setFillColor(GOLD)
    c.rect(0, SH-HDR-28, SW, 26, fill=1, stroke=0)
    c.setFont(KR, 13)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, SH-HDR-16, '오드린 농업회사법인(주)  —  연도별 매출 목표')

    y = CT - 32

    # ── 상단: 매출 구조 표 ────────────────────────────────────────────
    sec(c, MX, y, '매출 구조')
    y -= 30

    rev = [
        ('와인 직판·온라인', '병당 25,000~65,000원', '자사몰 + 쇼핑몰'),
        ('B2B 납품',         '건당 500만~1,500만원', '레스토랑·호텔·기업'),
        ('맞춤형·선물세트', '행사·기업선물 특화',    '매년 신제품 2라인'),
        ('해외 수출',         '아시아·북미 진입 추진', '수상 경력 프리미엄'),
    ]
    tbl(c, MX, y, ['매출 항목', '단가 · 규모', '채널 전략'],
        rev, [180, 230, CW-410], rh=24, hh=26, lcols={0,1,2})
    y -= 26*4 + 28 + 14

    # ── 하단: 연도별 대형 수치 카드 4개 ──────────────────────────────
    kw2 = (CW-18)//4
    kh2 = y - CB - 4
    for i, (lbl, val, bg) in enumerate([
        ('2024  실 적', '1억 3,460만', NAVY),
        ('2025  실 적', '1억 6,062만', BLUE),
        ('2026  목 표', '2억 5,000만', TEAL),
        ('2027  목 표', '3억 5,000만', ROSE),
    ]):
        kx = MX + i*(kw2+6)
        c.setFillColor(bg)
        c.roundRect(kx, CB, kw2, kh2, 5, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(kx, CB+kh2-4, kw2, 4, 2, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(LBLUE)
        c.drawCentredString(kx+kw2/2, CB+kh2-16, lbl)
        c.setFont(KR, 18)
        c.setFillColor(GOLD2)
        c.drawCentredString(kx+kw2/2, CB+kh2/2-4, val)
        c.setFont(KR, 10)
        c.setFillColor(MGRAY)
        c.drawCentredString(kx+kw2/2, CB+10, '원')


def p8(c):
    hdr(c, '매출 향상 계획 (2)  ★', 8)

    c.setFillColor(GOLD)
    c.rect(0, SH-HDR-28, SW, 26, fill=1, stroke=0)
    c.setFont(KR, 13)
    c.setFillColor(NAVY2)
    c.drawCentredString(SW/2, SH-HDR-16, '채널별 세부 달성 목표')

    y = CT - 32
    ch_h = (y - CB - 10)//2
    ch_w = (CW-12)//2

    channels = [
        ('① 온라인 채널 확대', NAVY,
         '자사몰 + 네이버 + 쿠팡·마켓컬리',
         '월 300병 → 800병 × 35,000원',
         '연 목표  3억 3,600만 원'),
        ('② 대기업 B2B 납품', BLUE,
         '수주 협의 중 10개사 목표',
         '건당 500만~1,500만원',
         '연 목표  5,000만 원+'),
        ('③ 맞춤형 · 선물세트', TEAL,
         '기업행사·명절 특화 상품',
         '2026년 신제품 2라인 출시',
         '연 목표  3,000만 원'),
        ('④ 해외 수출', ROSE,
         '아시아·북미 진입 (수상 기반)',
         '1차 : 일본·싱가포르·홍콩',
         '2026년 시범 1,000만 원'),
    ]

    for i, (title, bg, l1, l2, summary) in enumerate(channels):
        col = i % 2
        row = i // 2
        cx = MX + col*(ch_w+12)
        cy = y - row*(ch_h+10)

        c.setFillColor(LGRAY)
        c.roundRect(cx, cy-ch_h, ch_w, ch_h, 5, fill=1, stroke=0)
        # 상단 컬러 바
        c.setFillColor(bg)
        c.roundRect(cx, cy-5, ch_w, 5, 2, fill=1, stroke=0)
        # 좌측 컬러 바
        c.setFillColor(bg)
        c.rect(cx, cy-ch_h, 4, ch_h, fill=1, stroke=0)

        # 제목
        c.setFont(KR, 14)
        c.setFillColor(NAVY)
        c.drawString(cx+14, cy-22, title)

        # 내용
        c.setFont(KR, 11)
        c.setFillColor(MID)
        c.drawString(cx+14, cy-40, l1)
        c.drawString(cx+14, cy-56, l2)

        # 목표 수치 박스
        sw2 = ch_w-20
        c.setFillColor(bg)
        c.roundRect(cx+10, cy-ch_h+8, sw2, 24, 4, fill=1, stroke=0)
        c.setFont(KR, 12)
        c.setFillColor(WHITE if bg != GOLD else NAVY)
        c.drawCentredString(cx+10+sw2/2, cy-ch_h+16, summary)


def p9(c):
    hdr(c, '매출 달성 근거', 9)
    y = CT

    lw = CW*0.46
    rw = CW - lw - 16
    rx = MX + lw + 16

    # ── 왼쪽: 시장 인포그래픽 ────────────────────────────────────────
    sec(c, MX, y, '국내 와인 시장 분석')
    y -= 32

    # 대형 수치 강조
    c.setFillColor(LGRAY)
    c.roundRect(MX, y-58, lw, 58, 5, fill=1, stroke=0)
    c.setFont(KR, 38)
    c.setFillColor(NAVY)
    c.drawCentredString(MX+lw/2, y-34, '13조 원')
    c.setFont(KR, 11)
    c.setFillColor(MID)
    c.drawCentredString(MX+lw/2, y-52, '2024년 국내 와인 시장 규모')
    y -= 66

    # 성장률 바
    c.setFont(KR, 12)
    c.setFillColor(DGRAY)
    c.drawString(MX, y, '연평균 성장률 (CAGR)')
    y -= 16
    bar_h(c, MX, y, lw, 18, 0.36, label='', val='3.6%')
    y -= 26

    # 텍스트 요약
    T(c, '수입 와인 중심 시장에서 국내산 포도 100%\n와인은 극히 드문 블루오션 영역.',
      MX, y, lw, 11, MID, 18)
    y -= 50

    div(c, y, MX, MX+lw)
    y -= 14

    sec(c, MX, y, '오드린 영업 인프라')
    y -= 30

    infra = [('현재 거래처', '20개사'), ('B2B 수주예정', '10개사'), ('신제품', '2라인 (2026)'), ('특허', '2건')]
    tbl(c, MX, y, ['항목', '현황'], infra, [lw*0.45, lw*0.55], rh=22, hh=24)

    # ── 오른쪽: 달성 근거 체크리스트 ─────────────────────────────────
    ry = CT
    sec(c, rx, ry, '매출 목표 달성 근거')
    ry -= 32

    items = [
        (GOLD,  '13조원 시장, 연 3.6% 안정 성장 지속'),
        (GOLD,  '국내산 포도 100% — 시장 내 희소성 극대화'),
        (TEAL,  '와인명인 고유 숙성기술 — 동종 경쟁사 無'),
        (TEAL,  '수상 이력 5건+ — 품질 공신력 이미 확보'),
        (BLUE,  '특허 2건 — 모방 불가 독점 레시피'),
        (BLUE,  '거래처 20개 + B2B 10개사 수주 진행'),
        (ROSE,  '아시아 와인트로피 수상 — 수출 기반 확보'),
    ]
    for col, txt in items:
        c.setFillColor(col)
        c.circle(rx+10, ry-10, 6, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(DGRAY)
        c.drawString(rx+22, ry-14, txt)
        ry -= 26

    # 결론 배너
    c.setFillColor(NAVY2)
    c.roundRect(MX, CB, CW, 24, 3, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.roundRect(MX, CB, CW, 24, 3, fill=0, stroke=1)
    c.setFont(KR, 11)
    c.setFillColor(GOLD2)
    c.drawCentredString(SW/2, CB+8,
        '13조원 성장 시장 × 국내산 희소성 × 검증된 기술력  →  매출 목표 달성 근거 충분')


def p10(c):
    hdr(c, '자금 소요 계획', 10)
    y = CT

    # ── 상단: 항목별 카드 3개 ─────────────────────────────────────────
    kw = (CW-16)//3
    kh = 80
    fund_cards = [
        ('설비 투자', '1억 원', '양조 설비 고도화\n냉각·보관 창고 확충', NAVY),
        ('인건비',    '5천만 원', '생산인력 1~2명\n6개월분 급여', BLUE),
        ('마케팅·박람회', '5천만 원', '국내외 와인 박람회\n온라인 광고', TEAL),
    ]
    for i, (lbl, amt, detail, bg) in enumerate(fund_cards):
        kx = MX + i*(kw+8)
        c.setFillColor(bg)
        c.roundRect(kx, y-kh, kw, kh, 6, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(kx, y-4, kw, 4, 2, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(LBLUE)
        c.drawCentredString(kx+kw/2, y-18, lbl)
        c.setFont(KR, 22)
        c.setFillColor(GOLD2)
        c.drawCentredString(kx+kw/2, y-46, amt)
        c.setFont(KR, 10)
        c.setFillColor(LGRAY)
        for li, ln in enumerate(detail.split('\n')):
            c.drawCentredString(kx+kw/2, y-62-li*12, ln)
    y -= kh + 12

    # ── 총액 강조 ────────────────────────────────────────────────────
    c.setFillColor(GOLD)
    c.roundRect(MX, y-36, CW, 36, 4, fill=1, stroke=0)
    c.setFont(KR, 14)
    c.setFillColor(NAVY2)
    c.drawString(MX+20, y-21, '총 필요 자금')
    c.setFont(KR, 22)
    c.setFillColor(NAVY2)
    c.drawRightString(MX+CW-20, y-21, '200,000,000원   (2억 원)')
    y -= 46

    # ── 분기별 집행 타임라인 ─────────────────────────────────────────
    sec(c, MX, y, '분기별 집행 타임라인')
    y -= 30

    quarters = [
        ('2026 Q1', '설비투자 착수\n5,000만원', NAVY),
        ('2026 Q2', '설비 완공\n+ 인건비\n5,000만원', BLUE),
        ('2026 Q3', '박람회·마케팅\n3,000만원', TEAL),
        ('2026 Q4', '마케팅 지속\n여유자금\n2,000만원', colors.HexColor('#4A90D9')),
    ]
    qw = (CW-9)//4
    qh = y - CB - 4
    qx = MX
    for qname, qbody, bg in quarters:
        c.setFillColor(bg)
        c.roundRect(qx, CB, qw, qh, 4, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(qx, CB+qh-4, qw, 4, 2, fill=1, stroke=0)
        c.setFont(KR, 12)
        c.setFillColor(GOLD2)
        c.drawCentredString(qx+qw/2, CB+qh-18, qname)
        c.setFont(KR, 10)
        c.setFillColor(WHITE)
        py = CB+qh-36
        for ln in qbody.split('\n'):
            c.drawCentredString(qx+qw/2, py, ln)
            py -= 14
        qx += qw+3


def p11(c):
    c.setFillColor(NAVY2)
    c.rect(0, 0, SW, SH, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, SH-7, SW, 7, fill=1, stroke=0)
    c.rect(0, 0, SW, 6, fill=1, stroke=0)

    # 세로 중앙 정렬
    c.setFont(KR, 54)
    c.setFillColor(WHITE)
    c.drawCentredString(SW/2, SH*0.60, 'THANK YOU.')

    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(SW/2-180, SH*0.54, SW/2+180, SH*0.54)

    c.setFont(KR, 20)
    c.setFillColor(GOLD2)
    c.drawCentredString(SW/2, SH*0.46, '오드린 농업회사법인(주)')
    c.setFont(KR, 14)
    c.setFillColor(LBLUE)
    c.drawCentredString(SW/2, SH*0.38, '대표이사  박천명')
    c.setFont(KR, 13)
    c.setFillColor(colors.HexColor('#8AADCF'))
    c.drawCentredString(SW/2, SH*0.30, 'T. 010-2466-7789')
    c.drawCentredString(SW/2, SH*0.23, '브랜드: 월류봉 · 베베마루')
    c.setFont(KR, 9)
    c.setFillColor(MID)
    c.drawCentredString(SW/2, 16,
        '본 사업계획서는 정책자금 신청용 초안입니다. 금융기관 제출 전 전문가 검토를 권장합니다.')


# ══════════════════════════════════════════════════════════════════════
def build():
    out = Path(__file__).parent / f'오드린_정책자금_사업계획서_{datetime.date.today().strftime("%Y%m%d")}.pdf'
    cv = pdfcanvas.Canvas(str(out), pagesize=(SW, SH))
    for fn in [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]:
        fn(cv)
        cv.showPage()
    cv.save()
    print(f'✅ {out}')

if __name__ == '__main__':
    build()
