"""
오드린 농업회사법인(주) — 정책자금용 사업계획서
16:9 슬라이드 형태 (PowerPoint 기준 960×540pt)
"""
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pathlib import Path
import datetime

# ── 폰트 (전부 고딕) ─────────────────────────────────────────────────
pdfmetrics.registerFont(UnicodeCIDFont('HYGothic-Medium'))
KR  = 'HYGothic-Medium'   # 본문
KRB = 'HYGothic-Medium'   # 제목·강조 (크기·색상으로 본문과 구분)

# ── 색상 ─────────────────────────────────────────────────────────────
NAVY  = colors.HexColor('#1B3A6B')
NAVY2 = colors.HexColor('#162D56')
GOLD  = colors.HexColor('#C9A84C')
BLUE  = colors.HexColor('#2E6DB4')
LBLUE = colors.HexColor('#A8C8E8')
LGRAY = colors.HexColor('#F2F4F8')
MGRAY = colors.HexColor('#CCCCCC')
GRAY  = colors.HexColor('#888888')
DGRAY = colors.HexColor('#333333')
WHITE = colors.white

# ── 슬라이드 크기 (16:9, PowerPoint 기준) ────────────────────────────
SW = 960   # 너비 (points)
SH = 540   # 높이 (points)
MX = 28    # 좌우 여백
MY = 16    # 상하 여백
CW = SW - 2 * MX   # 콘텐츠 너비 = 904

HEADER_H = 58   # 상단 헤더 바 높이 (제목 크게 → 높이 확보)
FOOTER_H = 22   # 하단 푸터 높이
CONTENT_TOP = SH - HEADER_H - 12   # 콘텐츠 시작 y
CONTENT_BOT = FOOTER_H + 4


# ══════════════════════════════════════════════════════════════════════
# 헬퍼 함수
# ══════════════════════════════════════════════════════════════════════

def wrap(c, text, max_w, font, size):
    """한글/영문 혼합 텍스트를 max_w에 맞게 줄 분리"""
    result = []
    for para in text.split('\n'):
        if not para.strip():
            result.append('')
            continue
        line = ''
        for ch in para:
            if c.stringWidth(line + ch, font, size) <= max_w:
                line += ch
            else:
                if line:
                    result.append(line)
                line = ch
        if line:
            result.append(line)
    return result


def text_block(c, text, x, y, max_w, font, size, color=DGRAY, lh=None):
    """여러 줄 텍스트 그리기. 마지막 baseline y 반환."""
    if lh is None:
        lh = size * 1.7
    c.setFont(font, size)
    c.setFillColor(color)
    for ln in wrap(c, text, max_w, font, size):
        c.drawString(x, y, ln)
        y -= lh
    return y


def slide_header(c, title, page_num):
    """슬라이드 상단 헤더 + 하단 페이지 번호"""
    c.setFillColor(NAVY)
    c.rect(0, SH - HEADER_H, SW, HEADER_H, fill=1, stroke=0)
    # 왼쪽 골드 강조 바
    c.setFillColor(GOLD)
    c.rect(0, SH - HEADER_H, 6, HEADER_H, fill=1, stroke=0)
    # 골드 하단 라인
    c.rect(0, SH - HEADER_H - 2, SW, 2, fill=1, stroke=0)
    # 페이지 제목 (크고 선명하게)
    c.setFont(KR, 20)
    c.setFillColor(WHITE)
    c.drawString(MX + 8, SH - HEADER_H + 20, title)
    # 회사명 (작게, 오른쪽)
    c.setFont(KR, 10)
    c.setFillColor(LBLUE)
    c.drawRightString(SW - MX, SH - HEADER_H + 20, '오드린 농업회사법인(주)')
    # 페이지 번호
    c.setFont(KR, 9)
    c.setFillColor(GRAY)
    c.drawCentredString(SW / 2, 8, str(page_num))


def section_label(c, x, y, text, w=None):
    """섹션 구분 레이블 박스 — 제목과 본문 구분을 위해 크게"""
    tw = c.stringWidth(text, KR, 11)
    bw = (w or tw + 20)
    bh = 22
    c.setFillColor(NAVY)
    c.roundRect(x, y - bh, bw, bh, 3, fill=1, stroke=0)
    # 왼쪽 골드 바
    c.setFillColor(GOLD)
    c.roundRect(x, y - bh, 4, bh, 2, fill=1, stroke=0)
    c.setFont(KR, 11)
    c.setFillColor(WHITE)
    c.drawString(x + 10, y - bh + 7, text)
    return bh


def divider(c, y, x1=None, x2=None, color=LGRAY):
    c.setStrokeColor(color)
    c.setLineWidth(0.6)
    c.line(x1 or MX, y, x2 or (SW - MX), y)


def card(c, x, y, w, h, title, value, sub='', title_color=LBLUE, val_color=GOLD, bg=NAVY2):
    """수치 강조 카드"""
    c.setFillColor(bg)
    c.roundRect(x, y - h, w, h, 4, fill=1, stroke=0)
    # 상단 골드 라인
    c.setFillColor(GOLD)
    c.rect(x, y - 3, w, 3, fill=1, stroke=0)
    c.setFont(KR, 9)          # 카드 제목: 9pt
    c.setFillColor(title_color)
    c.drawCentredString(x + w / 2, y - 16, title)
    c.setFont(KR, 17)         # 카드 수치: 17pt (크게)
    c.setFillColor(val_color)
    c.drawCentredString(x + w / 2, y - 36, value)
    if sub:
        c.setFont(KR, 8)
        c.setFillColor(GRAY)
        c.drawCentredString(x + w / 2, y - h + 9, sub)


def draw_table(c, x, y, headers, rows, widths,
               row_h=26, header_h=26,
               left_cols=None, bold_col=None):
    """
    완전한 표 그리기. y = 헤더 상단 기준. 최종 바닥 y 반환.
    left_cols: 왼쪽 정렬할 열 인덱스 집합
    bold_col: 굵게 처리할 열 인덱스
    """
    if left_cols is None:
        left_cols = set()
    total_w = sum(widths)

    # 헤더 — 배경 네이비, 텍스트 흰색 11pt
    c.setFillColor(NAVY)
    c.rect(x, y - header_h, total_w, header_h, fill=1, stroke=0)
    c.setFont(KR, 11)          # 표 헤더: 11pt
    c.setFillColor(WHITE)
    cx = x
    for h_txt, w in zip(headers, widths):
        c.drawCentredString(cx + w / 2, y - header_h + (header_h - 11) / 2, h_txt)
        cx += w
    y -= header_h

    # 데이터 행 — 10pt
    for ri, row in enumerate(rows):
        bg = WHITE if ri % 2 == 0 else LGRAY
        c.setFillColor(bg)
        c.rect(x, y - row_h, total_w, row_h, fill=1, stroke=0)
        c.setStrokeColor(MGRAY)
        c.setLineWidth(0.3)
        c.rect(x, y - row_h, total_w, row_h, fill=0, stroke=1)
        cx = x
        for ci, (val, w) in enumerate(zip(row, widths)):
            col = NAVY if ci == 0 else (GOLD if ci == bold_col else DGRAY)
            c.setFont(KR, 10)  # 표 데이터: 10pt
            c.setFillColor(col)
            text_y = y - row_h + (row_h - 10) / 2
            if ci in left_cols:
                c.drawString(cx + 6, text_y, str(val))
            else:
                c.drawCentredString(cx + w / 2, text_y, str(val))
            cx += w
        y -= row_h
    return y


def bullet_list(c, items, x, y, max_w, font_size=10, lh=18, bullet_color=GOLD):
    for item in items:
        c.setFillColor(bullet_color)
        c.circle(x + 5, y + 4, 3.5, fill=1, stroke=0)
        c.setFont(KR, font_size)
        c.setFillColor(DGRAY)
        lines = wrap(c, item, max_w - 16, KR, font_size)
        for li, ln in enumerate(lines):
            c.drawString(x + 14, y, ln)
            y -= lh
        y -= 3
    return y


# ══════════════════════════════════════════════════════════════════════
# 페이지 함수
# ══════════════════════════════════════════════════════════════════════

def p1_cover(c):
    """표지"""
    # 배경
    c.setFillColor(NAVY)
    c.rect(0, 0, SW, SH, fill=1, stroke=0)

    # 상단 골드 라인
    c.setFillColor(GOLD)
    c.rect(0, SH - 6, SW, 6, fill=1, stroke=0)
    # 하단 골드 라인
    c.rect(0, 0, SW, 5, fill=1, stroke=0)

    # 왼쪽 골드 세로 강조선
    c.setFillColor(GOLD)
    c.rect(MX, 90, 4, SH - 180, fill=1, stroke=0)

    # 회사명
    c.setFont(KRB, 28)
    c.setFillColor(WHITE)
    c.drawString(MX + 18, SH - 100, '오드린 농업회사법인(주)')

    # 부제 — 사업 소개 한 줄
    c.setFont(KR, 13)
    c.setFillColor(LBLUE)
    c.drawString(MX + 18, SH - 128, '국내산 포도 100%  |  프리미엄 와인 제조 · 판매')

    # 구분선
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(MX + 18, SH - 145, MX + 18 + 380, SH - 145)

    # 사업계획서 타이틀
    c.setFont(KRB, 38)
    c.setFillColor(GOLD)
    c.drawString(MX + 18, SH - 210, '사  업  계  획  서')

    # 브랜드
    c.setFont(KR, 11)
    c.setFillColor(colors.HexColor('#8AADCF'))
    c.drawString(MX + 18, SH - 240, '브랜드  :  월류봉  ·  베베마루')

    # 하단 정보
    c.setFont(KR, 10)
    c.setFillColor(GRAY)
    c.drawString(MX + 18, 60, f'T. 010-2466-7789')
    c.drawString(MX + 18, 42, f'작성일: {datetime.date.today()}')

    # 오른쪽 장식 박스
    c.setFillColor(colors.HexColor('#1E3F75'))
    c.roundRect(SW - MX - 220, 80, 210, SH - 175, 6, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor('#2A5199'))
    c.setLineWidth(1)
    c.roundRect(SW - MX - 220, 80, 210, SH - 175, 6, fill=0, stroke=1)

    items = [
        ('와인명인', '3대째 포도농장'),
        ('특허', '2건 보유'),
        ('ISO 22000', '품질인증'),
        ('국제수상', 'Best Producer'),
        ('매출목표', '2026년 2.5억'),
    ]
    iy = SH - 130
    for label, val in items:
        c.setFont(KR, 8)
        c.setFillColor(LBLUE)
        c.drawCentredString(SW - MX - 115, iy, label)
        c.setFont(KRB, 11)
        c.setFillColor(WHITE)
        c.drawCentredString(SW - MX - 115, iy - 14, val)
        iy -= 46


def p2_business(c):
    """주요 사업 소개"""
    slide_header(c, '주요 사업 소개', 2)
    y = CONTENT_TOP

    # 사업 개요 텍스트 (왼쪽 60%)
    lw = CW * 0.58
    y2 = text_block(c,
        '오드린 농업회사법인(주)는 3대째 포도농장을 운영해온 와인명인이 설립한 '
        '프리미엄 와이너리입니다. 국내산 포도를 100% 활용한 고품질 와인을 개발·제조·판매하며, '
        '와인명장의 고유 숙성 기술을 바탕으로 국내 와인 시장에서 독보적인 경쟁력을 갖추고 있습니다.',
        MX, y, lw, KR, 11, DGRAY, 18)

    y2 -= 12
    divider(c, y2, MX, MX + lw)
    y2 -= 16

    # 사업 구조 흐름
    section_label(c, MX, y2, '사업 구조')
    y2 -= 28

    steps = ['국내산\n포도 재배·수매', '양조·발효\n숙성', '병입·라벨링', '온라인\n판매', 'B2B·수출']
    sw2 = lw / len(steps) - 4
    sx = MX
    for i, step in enumerate(steps):
        bg = NAVY if i % 2 == 0 else BLUE
        c.setFillColor(bg)
        c.roundRect(sx, y2 - 40, sw2, 40, 3, fill=1, stroke=0)
        c.setFont(KR, 9)
        c.setFillColor(WHITE)
        lines = step.split('\n')
        ly = y2 - 40 + (40 + len(lines) * 11) / 2 - 5
        for ln in lines:
            c.drawCentredString(sx + sw2 / 2, ly, ln)
            ly -= 13
        sx += sw2 + 4
        if i < len(steps) - 1:
            c.setFont(KR, 10)
            c.setFillColor(GOLD)
            c.drawCentredString(sx - 2, y2 - 20, '▶')

    # 오른쪽 브랜드 카드 (오른쪽 38%)
    rx = MX + lw + 20
    rw = CW - lw - 20

    for bi, (brand, desc, prods, tag_bg) in enumerate([
        ('월류봉', '충북 영동 황간의 명소에서 영감.\n프리미엄 라인.', '레드 · 화이트 · 스파클링', NAVY),
        ('베베마루', '일상적 음용을 위한 접근성 높은 라인.', '로제 · 화이트', BLUE),
    ]):
        by2 = y - bi * (SH * 0.42)
        c.setFillColor(LGRAY)
        c.roundRect(rx, by2 - 85, rw, 85, 5, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.line(rx, by2 - 8, rx, by2 - 82)
        c.setFont(KRB, 14)
        c.setFillColor(NAVY)
        c.drawString(rx + 10, by2 - 18, brand)
        text_block(c, desc, rx + 10, by2 - 34, rw - 14, KR, 8.5, DGRAY, 13)
        # 제품 배지
        c.setFillColor(tag_bg)
        tw = c.stringWidth(prods, KR, 8) + 12
        c.roundRect(rx + 10, by2 - 78, tw, 16, 3, fill=1, stroke=0)
        c.setFont(KR, 8)
        c.setFillColor(WHITE)
        c.drawString(rx + 16, by2 - 72, prods)


def p3_strengths(c):
    """핵심 강점 & 기술력"""
    slide_header(c, '핵심 강점 & 기술력', 3)
    y = CONTENT_TOP

    strengths = [
        ('① 와인명인의 고유 숙성 기술',
         '3대째 포도농장 운영의 전통 양조 기법과 현대 기술을 결합한\n'
         '독자적 숙성 공정으로 타 와이너리가 모방할 수 없는 맛을 구현합니다.'),
        ('② 특허 기반 차별화 제품',
         '오미자과즙 로제와인 제조방법(특허등록) 및 샤인머스켓\n'
         '블랜딩와인 제조방법(특허출원) — 독점 레시피 보유.'),
        ('③ 국내산 원재료 100%',
         '수입 포도즙·농축액 의존도 제로. 국내 재배 포도만을\n'
         '원료로 사용하여 "진정한 한국 와인"의 가치를 실현합니다.'),
        ('④ 검증된 품질 관리 체계',
         'ISO 22000 · 한국식품연구원 품질인증 · 한국국제소믈리에협회\n'
         '와이너리 인증 보유 — 국내외 바이어가 신뢰하는 품질 기준.'),
    ]

    # 2×2 그리드
    card_w = (CW - 12) / 2
    card_h = (CONTENT_TOP - CONTENT_BOT - 20) / 2

    for i, (title, desc) in enumerate(strengths):
        col = i % 2
        row = i // 2
        cx2 = MX + col * (card_w + 12)
        cy2 = y - row * (card_h + 10)

        c.setFillColor(LGRAY)
        c.roundRect(cx2, cy2 - card_h, card_w, card_h, 5, fill=1, stroke=0)

        bar_color = GOLD if i % 2 == 0 else NAVY
        c.setFillColor(bar_color)
        c.roundRect(cx2, cy2 - card_h, 4, card_h, 2, fill=1, stroke=0)

        c.setFont(KR, 12)        # 강점 카드 제목: 12pt
        c.setFillColor(NAVY)
        c.drawString(cx2 + 14, cy2 - 20, title)

        text_block(c, desc, cx2 + 14, cy2 - 38, card_w - 20, KR, 10, DGRAY, 16)

    # 하단 경쟁 우위 요약
    boty = CONTENT_BOT
    c.setFillColor(NAVY2)
    c.roundRect(MX, boty, CW, 22, 3, fill=1, stroke=0)
    c.setFont(KR, 10)
    c.setFillColor(GOLD)
    c.drawCentredString(SW / 2, boty + 7,
        '특허 기술  ×  와인명인 숙성  ×  국내산 원료  ×  ISO 22000  —  4중 경쟁력')


def p4_achievements(c):
    """주요 실적 & 인증"""
    slide_header(c, '주요 실적 · 인증 · 수상 현황', 4)
    y = CONTENT_TOP

    # 두 컬럼 분할
    lw = CW * 0.52
    rw = CW - lw - 16
    rx = MX + lw + 16

    # 왼쪽: 특허·인증
    section_label(c, MX, y, '특허 / 인증')
    y -= 26

    certs = [
        ('특허등록', '오미자과즙을 이용한 로제와인 제조방법'),
        ('특허출원', '샤인머스켓 블랜딩와인 제조방법'),
        ('ISO 22000', '식품안전경영시스템 인증'),
        ('와이너리인증', '한국국제소믈리에협회장'),
        ('품질인증', '한국식품연구원장 품질인증서'),
    ]
    widths_l = [72, lw - 72]
    y = draw_table(c, MX, y, ['구분', '내용'], certs, widths_l,
                   row_h=22, header_h=22, left_cols={1})

    y -= 14
    section_label(c, MX, y, '주요 거래처')
    y -= 26
    text_block(c,
        '현재 온라인 쇼핑몰 중심 판매 채널 운영.\n'
        '거래처 20개사 확보, B2B 납품 10개사 수주 협의 중.',
        MX, y, lw, KR, 9, DGRAY, 15)

    # 오른쪽: 수상 내역
    ry = CONTENT_TOP
    section_label(c, rx, ry, '수상 내역')
    ry -= 26

    awards = [
        '농림축산식품부장관상',
        '신지식농업인상',
        '3년 연속 주류대상',
        '2025 K-SUUL AWARD 우수상',
        'Asia Wine Trophy\nBest Producer South Korea',
    ]
    for aw in awards:
        c.setFillColor(LGRAY)
        c.roundRect(rx, ry - 30, rw, 28, 3, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.circle(rx + 12, ry - 15, 4, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(DGRAY)
        lines = aw.split('\n')
        ly2 = ry - 11
        for ln in lines:
            c.drawString(rx + 24, ly2, ln)
            ly2 -= 14
        ry -= 34


def p5_ceo(c):
    """대표자 소개"""
    slide_header(c, '대표자 소개', 5)
    y = CONTENT_TOP

    # 프로필 영역 (상단 배너)
    c.setFillColor(LGRAY)
    c.roundRect(MX, y - 52, CW, 52, 4, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.5)
    c.line(MX, y, MX, y - 52)

    c.setFont(KR, 22)
    c.setFillColor(NAVY)
    c.drawString(MX + 16, y - 22, '박천명  대표이사')
    c.setFont(KR, 11)
    c.setFillColor(BLUE)
    c.drawString(MX + 16, y - 42, '오드린 농업회사법인(주)  |  와인명인  |  3대째 포도농장 운영')

    y -= 62

    # 두 컬럼
    lw = CW * 0.55
    rw = CW - lw - 16
    rx = MX + lw + 16

    # 왼쪽: 경력
    section_label(c, MX, y, '주요 경력')
    y -= 26

    careers = [
        ('3대째',     '포도농장 운영 — 충북 영동 황간 지역'),
        ('와인명인', '전통 양조 기법 계승 + 현대 양조학 접목'),
        ('2022~현재', '오드린 농업회사법인(주) 설립 · 대표이사'),
        ('3년 연속', '국내 주요 주류품평회 대상 수상'),
        ('2024년',   'Asia Wine Trophy Best Producer South Korea'),
    ]
    widths_l = [70, lw - 70]
    draw_table(c, MX, y, ['기간/구분', '경력 내용'], careers, widths_l,
               row_h=22, header_h=22, left_cols={1})

    # 오른쪽: 수상
    ry = y
    section_label(c, rx, ry, '수상 / 인정')
    ry -= 26

    awards_r = [
        '농림축산식품부장관상',
        '신지식농업인상',
        '3년 연속 주류대상',
        '2025 K-SUUL AWARD 우수상',
        'Asia Wine Trophy\nBest Producer S.Korea',
    ]
    for aw in awards_r:
        c.setFillColor(LGRAY)
        c.roundRect(rx, ry - 26, rw, 24, 3, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.circle(rx + 10, ry - 13, 3.5, fill=1, stroke=0)
        lines2 = aw.split('\n')
        ly3 = ry - 10
        c.setFont(KR, 10)
        c.setFillColor(DGRAY)
        for ln in lines2:
            c.drawString(rx + 20, ly3, ln)
            ly3 -= 14
        ry -= 34


def p6_market(c):
    """시장 동향 & 매출 전망"""
    slide_header(c, '시장 동향 & 매출 전망', 6)
    y = CONTENT_TOP

    # 상단 지표 카드 3개
    mw = (CW - 16) / 3
    metrics = [
        ('국내 와인시장 규모', '13조 원', '2024년 기준'),
        ('연평균 성장률', '3.6%', 'CAGR'),
        ('국내산 와인 점유율', '극히 낮음', '블루오션'),
    ]
    for i, (lbl, val, sub) in enumerate(metrics):
        card(c, MX + i * (mw + 8), y, mw, 58, lbl, val, sub)
    y -= 68

    # 시장 분석 텍스트
    text_block(c,
        '국내 와인 시장은 1인 가구 증가·홈술 문화·건강 지향 소비 트렌드에 힘입어 연평균 3.6% 안정적 성장세를 유지합니다. '
        '수입 와인이 시장 대부분을 차지하는 가운데, "국내산 포도 100% + 와인명인 양조"는 국내 시장에서 '
        '거의 유일한 포지셔닝으로 강력한 차별화 요소가 됩니다.',
        MX, y, CW, KR, 11, DGRAY, 18)
    y -= 56

    divider(c, y)
    y -= 14

    # 매출 추이 표
    section_label(c, MX, y, '오드린 매출 추이 및 목표')
    y -= 26

    rows_m = [
        ('2024', '134,600,000원', '—', '사업 초기 안정화'),
        ('2025', '160,620,000원', '+19.3%', '온라인 채널 확대'),
        ('2026 목표', '250,000,000원', '+55.7%', '신제품 2라인 출시'),
        ('2027 목표', '350,000,000원', '+40.0%', 'B2B · 수출 본격화'),
    ]
    widths_m = [90, 160, 80, CW - 330]
    draw_table(c, MX, y, ['연도', '매출액', '성장률', '비고'], rows_m,
               widths_m, row_h=22, header_h=22)


def p7_revenue1(c):
    """매출 향상 계획 (1)"""
    slide_header(c, '매출 향상 계획  (1)  ★', 7)
    # 헤더 아래 골드 서브 배너
    c.setFillColor(GOLD)
    c.rect(0, SH - HEADER_H - 26, SW, 24, fill=1, stroke=0)
    c.setFont(KR, 13)
    c.setFillColor(NAVY)
    c.drawCentredString(SW / 2, SH - HEADER_H - 17, '오드린 농업회사법인(주)  매출 계획')

    y = CONTENT_TOP - 30

    # 매출 구조 표
    section_label(c, MX, y, '매출 구조')
    y -= 26

    rev = [
        ('와인 직판·온라인', '병당 25,000~65,000원', '자사몰 + 쇼핑몰'),
        ('B2B 납품', '건당 500만~1,500만원', '레스토랑·호텔·기업'),
        ('맞춤형·선물세트', '행사·기업선물 특화', '매년 신제품 2라인 출시'),
        ('해외 수출', '아시아·북미 진입 추진', '수상 경력 프리미엄 포지셔닝'),
    ]
    widths_r = [150, 200, CW - 350]
    y = draw_table(c, MX, y, ['매출 항목', '단가·규모', '채널 전략'], rev,
                   widths_r, row_h=22, header_h=22, left_cols={1, 2})

    y -= 16

    # 연도별 성장 카드 4개
    cw2 = (CW - 18) / 4
    milestones = [
        ('2024  실 적', '1억 3,460만', BLUE, WHITE),
        ('2025  실 적', '1억 6,062만', BLUE, WHITE),
        ('2026  목 표', '2억 5,000만', NAVY, GOLD),
        ('2027  목 표', '3억 5,000만', NAVY2, GOLD),
    ]
    card_h = y - CONTENT_BOT - 4
    cx2 = MX
    for title, val, bg, vc in milestones:
        c.setFillColor(bg)
        c.roundRect(cx2, CONTENT_BOT, cw2, card_h, 4, fill=1, stroke=0)
        c.setFont(KR, 10)
        c.setFillColor(LBLUE)
        c.drawCentredString(cx2 + cw2 / 2, CONTENT_BOT + card_h - 16, title)
        c.setFont(KR, 15)
        c.setFillColor(vc)
        c.drawCentredString(cx2 + cw2 / 2, CONTENT_BOT + card_h / 2 - 7, val)
        c.setFont(KR, 9)
        c.setFillColor(GRAY)
        c.drawCentredString(cx2 + cw2 / 2, CONTENT_BOT + 11, '원')
        cx2 += cw2 + 6


def p8_revenue2(c):
    """매출 향상 계획 (2)"""
    slide_header(c, '매출 향상 계획  (2)  ★', 8)
    c.setFillColor(GOLD)
    c.rect(0, SH - HEADER_H - 26, SW, 24, fill=1, stroke=0)
    c.setFont(KR, 13)
    c.setFillColor(NAVY)
    c.drawCentredString(SW / 2, SH - HEADER_H - 17, '채널별 세부 달성 목표')

    y = CONTENT_TOP - 30

    channels = [
        ('① 온라인 채널 확대',
         '자사몰 + 네이버스토어 + 쿠팡·마켓컬리 입점\n'
         '목표: 월 300병 → 800병  /  병당 평균 35,000원\n'
         '= 월 28,000,000원 × 12개월',
         '연 목표  336,000,000원', GOLD),
        ('② 대기업 B2B 납품',
         '수주 협의 중 10개사 계약 목표\n'
         '건당 평균 500만~1,500만원\n'
         '= 연간 B2B 납품 목표',
         '연 목표  50,000,000원+', NAVY),
        ('③ 맞춤형·선물세트 OEM',
         '기업 행사·명절 선물세트 특화 상품\n'
         '2026년 신제품 2개 라인 출시\n'
         '시즌 집중 마케팅 병행',
         '연 목표  30,000,000원', BLUE),
        ('④ 해외 수출',
         'Asia Wine Trophy 수상 실적 기반 해외 접촉\n'
         '1차 타깃: 일본·싱가포르·홍콩\n'
         '2026 시범 수출, 2027 본격 확대',
         '2026년 목표  10,000,000원', colors.HexColor('#4A90D9')),
    ]

    ch_h = (CONTENT_TOP - 30 - CONTENT_BOT - 8) / 2 - 6
    ch_w = (CW - 10) / 2

    for i, (title, body, summary, bar_col) in enumerate(channels):
        col = i % 2
        row = i // 2
        cx2 = MX + col * (ch_w + 10)
        cy2 = y - row * (ch_h + 8)

        c.setFillColor(LGRAY)
        c.roundRect(cx2, cy2 - ch_h, ch_w, ch_h, 4, fill=1, stroke=0)
        # 왼쪽 컬러 바
        c.setFillColor(bar_col)
        c.roundRect(cx2, cy2 - ch_h, 4, ch_h, 2, fill=1, stroke=0)

        c.setFont(KR, 12)
        c.setFillColor(NAVY)
        c.drawString(cx2 + 12, cy2 - 17, title)

        text_block(c, body, cx2 + 12, cy2 - 34, ch_w - 90, KR, 10, DGRAY, 15)

        # 요약 박스 (오른쪽)
        sb_w = 82
        sb_h = ch_h - 14
        c.setFillColor(bar_col)
        c.roundRect(cx2 + ch_w - sb_w - 4, cy2 - ch_h + 6, sb_w, sb_h, 3, fill=1, stroke=0)
        c.setFont(KR, 9)
        c.setFillColor(WHITE if bar_col != GOLD else NAVY)
        for li, ln in enumerate(wrap(c, summary, sb_w - 8, KR, 9)):
            c.drawCentredString(cx2 + ch_w - sb_w / 2 - 4,
                                cy2 - ch_h + sb_h - 14 - li * 13, ln)


def p9_evidence(c):
    """매출 달성 근거"""
    slide_header(c, '매출 달성 근거', 9)
    y = CONTENT_TOP

    # 두 컬럼
    lw = CW * 0.52
    rw = CW - lw - 16
    rx = MX + lw + 16

    # 왼쪽: 시장 분석
    section_label(c, MX, y, '국내 와인 시장 분석')
    y -= 26

    text_block(c,
        '통계청·한국주류산업협회 자료 기준, 국내 와인 시장은 2024년 13조원 규모이며 '
        '연평균 3.6% 성장세를 지속 중입니다.\n\n'
        '국내산 포도 100%로 제조한 와인은 전체 시장의 극히 일부에 불과하여, '
        '오드린의 시장 진입 공간은 매우 넓습니다.',
        MX, y, lw, KR, 11, DGRAY, 18)
    y -= 80

    divider(c, y, MX, MX + lw)
    y -= 16

    section_label(c, MX, y, '오드린 영업 인프라')
    y -= 26

    infra = [
        ('현재 거래처',  '20개사 확보'),
        ('수주 예정',    'B2B 10개사 협의 중'),
        ('신제품',       '2026년 2개 라인 출시'),
        ('특허',         '등록 1건 + 출원 1건'),
    ]
    widths_i = [90, lw - 90]
    draw_table(c, MX, y, ['항목', '내용'], infra,
               widths_i, row_h=22, header_h=22, left_cols={1})

    # 오른쪽: 근거 리스트
    ry = CONTENT_TOP
    section_label(c, rx, ry, '매출 목표 달성 근거')
    ry -= 26

    evidences = [
        '13조원 와인 시장, 연 3.6% 안정 성장 지속',
        '국내산 포도 100% 와인 — 시장 내 희소성 극대화',
        '와인명인 고유 숙성기술 — 동종 경쟁사 차별화',
        '수상 이력으로 품질 공신력 이미 확보',
        '특허 기술 보유 — 모방 불가 독점 레시피',
        '거래처 20개 + B2B 10개사 수주 진행 중',
        '수출 가능성 — 아시아 시장 진입 기반 갖춤',
    ]
    ry = bullet_list(c, evidences, rx, ry, rw, font_size=10, lh=19)

    # 결론 박스
    c.setFillColor(NAVY2)
    c.roundRect(MX, CONTENT_BOT, CW, 26, 3, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.roundRect(MX, CONTENT_BOT, CW, 26, 3, fill=0, stroke=1)
    c.setFont(KR, 10)
    c.setFillColor(WHITE)
    c.drawCentredString(SW / 2, CONTENT_BOT + 9,
        '13조원 시장 × 연 3.6% 성장 × 국내산 와인 희소성 × 검증된 기술력  →  충분한 매출 달성 근거 확보')


def p10_funds(c):
    """자금 소요 계획"""
    slide_header(c, '자금 소요 계획', 10)
    y = CONTENT_TOP

    section_label(c, MX, y, '항목별 자금 소요')
    y -= 26

    funds = [
        ('설비 투자',     '양조 설비 고도화 · 냉각·보관 창고 확충',
         '설비 구매·설치비 일괄',   '100,000,000원'),
        ('인건비',        '생산인력 1~2명 채용 · 6개월분',
         '월 250~300만 × 2명 × 6개월', '50,000,000원'),
        ('마케팅·박람회', '국내외 와인 박람회 참가 · 온라인 광고',
         '박람회 3회 + 디지털 마케팅', '50,000,000원'),
    ]
    widths_f = [90, 220, 200, CW - 510]
    y = draw_table(c, MX, y, ['항목', '세부 내용', '산출 근거', '금액'],
                   funds, widths_f, row_h=26, header_h=22, left_cols={1, 2})

    # 합계 행
    y -= 2
    c.setFillColor(NAVY)
    c.rect(MX, y - 28, CW, 28, fill=1, stroke=0)
    c.setFont(KR, 13)
    c.setFillColor(WHITE)
    c.drawString(MX + 12, y - 18, '총 필요 자금')
    c.setFillColor(GOLD)
    c.drawRightString(MX + CW - 12, y - 18, '200,000,000원  (2억원)')
    y -= 36

    # 타임라인
    section_label(c, MX, y, '자금 집행 타임라인')
    y -= 26

    quarters = [
        ('2026 Q1', '설비투자 착수\n5,000만원'),
        ('2026 Q2', '설비 완공\n+ 인건비\n5,000만원'),
        ('2026 Q3', '마케팅·박람회\n3,000만원'),
        ('2026 Q4', '마케팅 지속\n+ 여유자금\n2,000만원'),
    ]
    qw = (CW - 9) / 4
    qh = y - CONTENT_BOT - 4
    qx = MX
    for i, (qname, qplan) in enumerate(quarters):
        bg = [NAVY, BLUE, colors.HexColor('#4A90D9'), LGRAY][i]
        fg = WHITE if bg != LGRAY else DGRAY
        c.setFillColor(bg)
        c.roundRect(qx, CONTENT_BOT, qw, qh, 3, fill=1, stroke=0)
        c.setFont(KR, 11)
        c.setFillColor(GOLD if bg != LGRAY else NAVY)
        c.drawCentredString(qx + qw / 2, CONTENT_BOT + qh - 16, qname)
        c.setFont(KR, 10)
        c.setFillColor(fg)
        py2 = CONTENT_BOT + qh - 34
        for ln in qplan.split('\n'):
            c.drawCentredString(qx + qw / 2, py2, ln)
            py2 -= 15
        qx += qw + 3


def p11_closing(c):
    """맺음말"""
    c.setFillColor(NAVY)
    c.rect(0, 0, SW, SH, fill=1, stroke=0)

    c.setFillColor(GOLD)
    c.rect(0, SH - 6, SW, 6, fill=1, stroke=0)
    c.rect(0, 0, SW, 5, fill=1, stroke=0)

    c.setFont(KR, 52)
    c.setFillColor(WHITE)
    c.drawCentredString(SW / 2, SH * 0.60, 'THANK YOU.')

    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(SW / 2 - 160, SH * 0.54, SW / 2 + 160, SH * 0.54)

    c.setFont(KR, 18)
    c.setFillColor(GOLD)
    c.drawCentredString(SW / 2, SH * 0.47, '오드린 농업회사법인(주)')

    c.setFont(KR, 14)
    c.setFillColor(LBLUE)
    c.drawCentredString(SW / 2, SH * 0.40, '대표이사  박천명')

    c.setFont(KR, 13)
    c.setFillColor(colors.HexColor('#8AADCF'))
    c.drawCentredString(SW / 2, SH * 0.31, 'T. 010-2466-7789')
    c.drawCentredString(SW / 2, SH * 0.24, '브랜드: 월류봉  ·  베베마루')

    c.setFont(KR, 9)
    c.setFillColor(GRAY)
    c.drawCentredString(SW / 2, 18,
        '본 사업계획서는 정책자금 신청용 초안입니다. 금융기관 제출 전 전문가 검토를 권장합니다.')


# ══════════════════════════════════════════════════════════════════════
# 빌드
# ══════════════════════════════════════════════════════════════════════

def build():
    out = Path(__file__).parent / f'오드린_정책자금_사업계획서_{datetime.date.today().strftime("%Y%m%d")}.pdf'
    c = pdfcanvas.Canvas(str(out), pagesize=(SW, SH))

    pages = [
        p1_cover, p2_business, p3_strengths, p4_achievements,
        p5_ceo, p6_market, p7_revenue1, p8_revenue2,
        p9_evidence, p10_funds, p11_closing,
    ]
    for fn in pages:
        fn(c)
        c.showPage()

    c.save()
    print(f'✅ PDF 생성 완료: {out}')
    return out


if __name__ == '__main__':
    build()
