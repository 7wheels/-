"""
오드린 농업회사법인(주) — 정책자금용 사업계획서 PDF 생성
"""
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pathlib import Path
import datetime

# ── 폰트 ─────────────────────────────────────────────────────────────
pdfmetrics.registerFont(UnicodeCIDFont('HYGothic-Medium'))
pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))
KR  = 'HYGothic-Medium'
KRB = 'HYSMyeongJo-Medium'

# ── 색상 ─────────────────────────────────────────────────────────────
NAVY  = colors.HexColor('#1B3A6B')
GOLD  = colors.HexColor('#C9A84C')
BLUE  = colors.HexColor('#2E6DB4')
LBLUE = colors.HexColor('#A8C8E8')
LGRAY = colors.HexColor('#F2F4F8')
GRAY  = colors.HexColor('#888888')
DGRAY = colors.HexColor('#444444')
WHITE = colors.white

W, H = A4
M = 16 * mm

# ── 텍스트 래핑 헬퍼 ──────────────────────────────────────────────────
def wrap_text(c, text, max_width, font, size):
    """한국어 포함 텍스트를 max_width에 맞게 줄 분리"""
    paragraphs = text.split('\n')
    all_lines = []
    for para in paragraphs:
        if para.strip() == '':
            all_lines.append('')
            continue
        line = ''
        for ch in para:
            if c.stringWidth(line + ch, font, size) <= max_width:
                line += ch
            else:
                if line:
                    all_lines.append(line)
                line = ch
        if line:
            all_lines.append(line)
    return all_lines

def draw_text_block(c, text, x, y, max_width, font, size, color=DGRAY, line_height=None):
    """여러 줄 텍스트 그리기 — 마지막 y 반환"""
    if line_height is None:
        line_height = size * 1.65
    lines = wrap_text(c, text, max_width, font, size)
    c.setFont(font, size)
    c.setFillColor(color)
    for ln in lines:
        c.drawString(x, y, ln)
        y -= line_height
    return y

# ── 공통 컴포넌트 ──────────────────────────────────────────────────────
def page_header(c, title, sub=''):
    """상단 헤더 배너 + 히어컴퍼니 브랜딩"""
    # 배너
    c.setFillColor(NAVY)
    c.rect(0, H - 18*mm, W, 18*mm, fill=1, stroke=0)
    c.setFont(KRB, 13)
    c.setFillColor(WHITE)
    c.drawString(M, H - 12*mm, title)
    if sub:
        c.setFont(KR, 8)
        c.setFillColor(LBLUE)
        c.drawRightString(W - M, H - 12*mm, sub)
    # 브랜딩 라인
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(0, H - 18*mm, W, H - 18*mm)
    # 하단 페이지 번호 영역 라인
    c.setStrokeColor(LBLUE)
    c.setLineWidth(0.5)
    c.line(M, 10*mm, W - M, 10*mm)

def page_footer(c, page_num):
    c.setFont(KR, 8)
    c.setFillColor(GRAY)
    c.drawCentredString(W/2, 6*mm, f'{page_num}')
    c.setFont(KR, 7)
    c.drawRightString(W - M, 6*mm, '오드린 농업회사법인(주)  |  히어컴퍼니 기업컨설팅 제공')

def section_box(c, x, y, w, h, title, bg=NAVY):
    """섹션 제목 박스"""
    c.setFillColor(bg)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=0)
    c.setFont(KRB, 10)
    c.setFillColor(WHITE)
    c.drawString(x + 6, y + h/2 - 5, title)

def highlight_box(c, x, y, w, h, text, font_size=11, bg=GOLD, text_color=WHITE, radius=4):
    """강조 수치 박스"""
    c.setFillColor(bg)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=0)
    c.setFont(KRB, font_size)
    c.setFillColor(text_color)
    c.drawCentredString(x + w/2, y + h/2 - font_size*0.4, text)

def info_row(c, x, y, label, value, label_w=40*mm, row_h=7*mm):
    """레이블:값 한 줄"""
    c.setFillColor(LGRAY)
    c.rect(x, y, label_w, row_h, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont(KRB, 9)
    c.drawString(x + 3, y + row_h/2 - 4, label)
    c.setFillColor(DGRAY)
    c.setFont(KR, 9)
    c.drawString(x + label_w + 4, y + row_h/2 - 4, value)
    c.setStrokeColor(LBLUE)
    c.setLineWidth(0.4)
    c.rect(x, y, W - 2*M, row_h, fill=0, stroke=1)

def table_header_row(c, x, y, cols, widths, row_h=8*mm):
    """표 헤더 행"""
    cx = x
    c.setFillColor(NAVY)
    c.rect(x, y, sum(widths), row_h, fill=1, stroke=0)
    c.setFont(KRB, 9)
    c.setFillColor(WHITE)
    for col, w in zip(cols, widths):
        c.drawCentredString(cx + w/2, y + row_h/2 - 4, col)
        cx += w

def table_data_row(c, x, y, vals, widths, row_h=7*mm, bg=WHITE, align='center'):
    """표 데이터 행"""
    cx = x
    c.setFillColor(bg)
    c.rect(x, y, sum(widths), row_h, fill=1, stroke=0)
    c.setStrokeColor(LBLUE)
    c.setLineWidth(0.4)
    c.rect(x, y, sum(widths), row_h, fill=0, stroke=1)
    c.setFont(KR, 9)
    c.setFillColor(DGRAY)
    for val, w in zip(vals, widths):
        if align == 'center':
            c.drawCentredString(cx + w/2, y + row_h/2 - 4, str(val))
        else:
            c.drawString(cx + 4, y + row_h/2 - 4, str(val))
        cx += w

def badge(c, x, y, text, bg=GOLD, text_color=WHITE, font_size=8):
    tw = c.stringWidth(text, KRB, font_size)
    bw = tw + 10
    bh = font_size + 6
    c.setFillColor(bg)
    c.roundRect(x, y, bw, bh, 3, fill=1, stroke=0)
    c.setFont(KRB, font_size)
    c.setFillColor(text_color)
    c.drawCentredString(x + bw/2, y + 3, text)
    return bw + 4

def divider(c, y, color=LBLUE):
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.line(M, y, W - M, y)

# ══════════════════════════════════════════════════════════════════════
# 페이지별 그리기 함수
# ══════════════════════════════════════════════════════════════════════

def draw_page1(c):
    """표지"""
    # 전체 네이비 배경
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # 골드 상단 라인
    c.setFillColor(GOLD)
    c.rect(0, H - 6*mm, W, 6*mm, fill=1, stroke=0)
    # 골드 하단 라인
    c.rect(0, 0, W, 5*mm, fill=1, stroke=0)
    # 중앙 흰색 박스
    bx, by, bw, bh = M, H*0.25, W - 2*M, H*0.5
    c.setFillColor(colors.HexColor('#162D56'))
    c.roundRect(bx, by, bw, bh, 6, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.roundRect(bx, by, bw, bh, 6, fill=0, stroke=1)
    # 회사명
    c.setFont(KRB, 22)
    c.setFillColor(WHITE)
    c.drawCentredString(W/2, by + bh - 30*mm, '오드린 농업회사법인(주)')
    # 구분선
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(W/2 - 40*mm, by + bh - 36*mm, W/2 + 40*mm, by + bh - 36*mm)
    # 부제
    c.setFont(KR, 13)
    c.setFillColor(LBLUE)
    c.drawCentredString(W/2, by + bh - 44*mm, '국내산 포도 100%  프리미엄 와인 제조 · 판매')
    # 사업계획서 타이틀
    c.setFont(KRB, 28)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, by + bh*0.45, '사  업  계  획  서')
    # 브랜드
    c.setFont(KR, 10)
    c.setFillColor(colors.HexColor('#8AADCF'))
    c.drawCentredString(W/2, by + bh*0.3, '브랜드: 월류봉  ·  베베마루')
    # 연락처
    c.setFont(KR, 10)
    c.setFillColor(GRAY)
    c.drawCentredString(W/2, by + 10*mm, f'T. 010-2466-7789     작성일: {datetime.date.today()}')
    # 히어컴퍼니
    c.setFont(KR, 8)
    c.setFillColor(colors.HexColor('#5A7FA8'))
    c.drawCentredString(W/2, 8*mm, '히어컴퍼니 기업컨설팅 제공')


def draw_page2(c):
    """주요 사업 소개"""
    page_header(c, '주요 사업 소개', '오드린 농업회사법인(주)')
    page_footer(c, 2)
    y = H - 28*mm

    # 리드 문구
    draw_text_block(c,
        '오드린 농업회사법인(주)는 3대째 포도농장을 운영해온 와인 명인이 설립한 프리미엄 와이너리입니다.\n'
        '국내산 포도를 100% 활용한 독창적인 와인을 개발·제조·판매하며, '
        '와인 명장의 고유 숙성 기술을 바탕으로 국내 와인 시장의 새로운 기준을 제시합니다.',
        M, y, W - 2*M, KR, 10, DGRAY)
    y -= 22*mm

    divider(c, y)
    y -= 8*mm

    # 브랜드 소개 박스 2개
    box_w = (W - 2*M - 8*mm) / 2
    for i, (brand, desc, prod) in enumerate([
        ('월류봉', '충북 영동 황간의 대표 명소에서 영감을 받은 프리미엄 라인.\n레드·화이트·스파클링 전 품목 생산.', '레드 · 화이트 · 스파클링'),
        ('베베마루', '가볍고 일상적인 음용을 위한 접근성 높은 라인.\n로제·화이트 중심 구성.', '로제 · 화이트'),
    ]):
        bx = M + i * (box_w + 8*mm)
        c.setFillColor(LGRAY)
        c.roundRect(bx, y - 36*mm, box_w, 38*mm, 5, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.2)
        c.line(bx, y + 2*mm, bx, y - 36*mm + 4)
        c.setFont(KRB, 14)
        c.setFillColor(NAVY)
        c.drawString(bx + 8, y - 6*mm, brand)
        draw_text_block(c, desc, bx + 8, y - 14*mm, box_w - 12, KR, 9, DGRAY)
        c.setFont(KRB, 9)
        c.setFillColor(GOLD)
        c.drawString(bx + 8, y - 33*mm, f'주요 제품: {prod}')
    y -= 46*mm

    divider(c, y)
    y -= 8*mm

    # 사업 구조
    section_box(c, M, y - 7*mm, W - 2*M, 8*mm, '사업 구조')
    y -= 16*mm

    steps = ['국내산 포도 재배·수매', '양조·발효·숙성', '병입·라벨링', '온라인 판매', 'B2B·수출']
    sw = (W - 2*M) / len(steps)
    for i, step in enumerate(steps):
        sx = M + i * sw
        c.setFillColor(NAVY if i % 2 == 0 else BLUE)
        c.roundRect(sx + 2, y - 10*mm, sw - 4, 11*mm, 3, fill=1, stroke=0)
        c.setFont(KR, 8.5)
        c.setFillColor(WHITE)
        c.drawCentredString(sx + sw/2, y - 5*mm, step)
        if i < len(steps) - 1:
            c.setFillColor(GOLD)
            c.drawCentredString(sx + sw - 2, y - 5*mm, '▶')
    y -= 20*mm

    # 키워드 배지
    kws = ['국내산 포도 100%', '와인명인 양조', 'ISO 22000', '특허 보유', '수상 와이너리']
    bx = M
    for kw in kws:
        bw = badge(c, bx, y - 8*mm, kw, NAVY)
        bx += bw + 2


def draw_page3(c):
    """핵심 강점 & 기술력"""
    page_header(c, '핵심 강점 & 기술력', '오드린 농업회사법인(주)')
    page_footer(c, 3)
    y = H - 30*mm

    strengths = [
        ('① 와인명인의 고유 숙성 기술',
         '3대째 포도농장을 운영한 와인명인의 전통적 양조 기법과 현대 기술을 결합한\n'
         '독자적 숙성 공정을 보유합니다. 동일 품종에서도 차별화된 맛과 향을 구현합니다.'),
        ('② 특허 기반 차별화 제품',
         '오미자과즙을 활용한 로제와인 제조방법(특허등록) 및 샤인머스켓 블랜딩와인\n'
         '제조방법(특허출원)으로 타 와이너리가 모방하기 어려운 독점 레시피를 보유합니다.'),
        ('③ 국내산 원재료 100% 활용',
         '수입 포도즙·농축액 의존도 제로. 국내 재배 포도만을 원료로 사용하여\n'
         '"진정한 한국 와인"의 가치를 실현하며 원가 경쟁력과 품질을 동시에 확보합니다.'),
        ('④ 검증된 품질 관리 체계',
         'ISO 22000 인증 취득, 한국식품연구원 품질인증, 한국국제소믈리에협회 와이너리 인증을\n'
         '보유하여 국내외 바이어가 신뢰할 수 있는 품질 기준을 갖추고 있습니다.'),
    ]

    box_h = 28*mm
    for i, (title, desc) in enumerate(strengths):
        by = y - i * (box_h + 5*mm)
        # 번호 원형
        c.setFillColor(GOLD if i % 2 == 0 else NAVY)
        c.circle(M + 5*mm, by - box_h/2 + 2, 5*mm, fill=1, stroke=0)
        c.setFont(KRB, 11)
        c.setFillColor(WHITE)
        c.drawCentredString(M + 5*mm, by - box_h/2 - 2, str(i+1))
        # 내용 박스
        bx = M + 13*mm
        bw = W - 2*M - 13*mm
        c.setFillColor(LGRAY)
        c.roundRect(bx, by - box_h + 2*mm, bw, box_h - 2*mm, 4, fill=1, stroke=0)
        c.setStrokeColor(GOLD if i % 2 == 0 else NAVY)
        c.setLineWidth(1)
        c.line(bx, by - box_h + 4*mm, bx, by - 2*mm)
        c.setFont(KRB, 10)
        c.setFillColor(NAVY)
        c.drawString(bx + 6, by - 8*mm, title)
        draw_text_block(c, desc, bx + 6, by - 15*mm, bw - 12, KR, 9, DGRAY, 12)

    y -= len(strengths) * (box_h + 5*mm) + 5*mm
    divider(c, y)
    y -= 8*mm

    # 경쟁 우위 요약
    c.setFillColor(colors.HexColor('#162D56'))
    c.roundRect(M, y - 14*mm, W - 2*M, 15*mm, 4, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.roundRect(M, y - 14*mm, W - 2*M, 15*mm, 4, fill=0, stroke=1)
    c.setFont(KRB, 10)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, y - 4*mm, '경쟁 우위 포인트')
    c.setFont(KR, 9)
    c.setFillColor(WHITE)
    c.drawCentredString(W/2, y - 10*mm,
        '특허 기술 × 와인명인 숙성 노하우 × 국내산 원료 × ISO 22000 — 국내 소규모 와이너리 중 유일한 4중 경쟁력')


def draw_page4(c):
    """주요 실적 & 거래처"""
    page_header(c, '주요 실적 & 인증 현황', '오드린 농업회사법인(주)')
    page_footer(c, 4)
    y = H - 30*mm

    # 특허·인증
    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '특허 / 인증 / 수상')
    y -= 16*mm

    certs = [
        ('특허등록', '오미자과즙을 이용한 로제와인 제조방법'),
        ('특허출원', '샤인머스켓을 활용한 블랜딩와인 제조방법'),
        ('국제인증', 'ISO 22000 식품안전경영시스템'),
        ('품질인증', '와이너리 품질인증서 (한국국제소믈리에협회장)'),
        ('품질인증', '품질인증서 (한국식품연구원장)'),
    ]
    widths = [28*mm, W - 2*M - 28*mm]
    table_header_row(c, M, y, ['구분', '내용'], widths, 7*mm)
    y -= 7*mm
    for i, (cat, content) in enumerate(certs):
        bg = WHITE if i % 2 == 0 else LGRAY
        table_data_row(c, M, y, [cat, content], widths, 7*mm, bg, 'left' if False else 'center')
        # 왼쪽 정렬 처리
        c.setFont(KR, 9)
        c.setFillColor(DGRAY)
        c.drawString(M + 28*mm + 4, y + 2, content)
        y -= 7*mm

    y -= 8*mm
    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '수상 내역')
    y -= 16*mm

    awards = [
        ('정부포상',  '농림축산식품부장관상 수상'),
        ('정부포상',  '신지식농업인상 수상'),
        ('국내대회',  '3년 연속 주류대상 수상'),
        ('국내대회',  '2025 K-SUUL AWARD 우수상'),
        ('국제대회',  'Asia Wine Trophy — Best Producer South Korea'),
    ]
    table_header_row(c, M, y, ['구분', '수상 내역'], widths, 7*mm)
    y -= 7*mm
    for i, (cat, award) in enumerate(awards):
        bg = WHITE if i % 2 == 0 else LGRAY
        c.setFillColor(bg)
        c.rect(M, y, sum(widths), 7*mm, fill=1, stroke=0)
        c.setStrokeColor(LBLUE)
        c.setLineWidth(0.4)
        c.rect(M, y, sum(widths), 7*mm, fill=0, stroke=1)
        c.setFont(KRB, 9)
        c.setFillColor(GOLD)
        c.drawCentredString(M + widths[0]/2, y + 2, cat)
        c.setFont(KR, 9)
        c.setFillColor(DGRAY)
        c.drawString(M + widths[0] + 4, y + 2, award)
        y -= 7*mm

    y -= 8*mm
    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '주요 거래처 및 영업망')
    y -= 16*mm
    draw_text_block(c,
        '현재 온라인 쇼핑몰 중심 판매 채널을 운영하고 있으며, 현재 거래처 20개 업체를 확보하고 있습니다.\n'
        '2026년에는 대기업 B2B 납품 10개사 수주를 진행 중이며, 해외 수출 시장 진입도 병행 추진합니다.',
        M, y, W - 2*M, KR, 9.5, DGRAY)
    y -= 16*mm

    bx = M
    for ch in ['온라인 쇼핑몰', '거래처 20개사', 'B2B 수주예정 10개사', '수출 추진 중']:
        bw = badge(c, bx, y, ch, NAVY)
        bx += bw + 3


def draw_page5(c):
    """대표자 소개"""
    page_header(c, '대표자 소개', '오드린 농업회사법인(주)')
    page_footer(c, 5)
    y = H - 30*mm

    # 프로필 박스
    c.setFillColor(LGRAY)
    c.roundRect(M, y - 22*mm, W - 2*M, 23*mm, 5, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(M, y + 1*mm, M, y - 22*mm)
    c.setFont(KRB, 18)
    c.setFillColor(NAVY)
    c.drawString(M + 8*mm, y - 8*mm, '박천명  대표이사')
    c.setFont(KR, 10)
    c.setFillColor(BLUE)
    c.drawString(M + 8*mm, y - 16*mm, '오드린 농업회사법인(주)  |  와인명인  |  3대째 포도농장 운영')
    y -= 30*mm

    # 경력 타임라인
    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '주요 경력')
    y -= 16*mm

    careers = [
        ('3대째',       '포도농장 운영 — 충북 영동 황간 지역 자체 포도 재배'),
        ('와인명인',    '전통 양조 기법 계승 + 현대 양조학 접목'),
        ('2022~현재',   '오드린 농업회사법인(주) 설립 · 대표이사'),
        ('3년 연속',    '국내 주요 주류품평회 대상 수상'),
        ('2024',        'Asia Wine Trophy Best Producer South Korea 수상'),
    ]
    widths = [32*mm, W - 2*M - 32*mm]
    table_header_row(c, M, y, ['기간', '주요 경력 내용'], widths, 7*mm)
    y -= 7*mm
    for i, (period, content) in enumerate(careers):
        bg = WHITE if i % 2 == 0 else LGRAY
        c.setFillColor(bg)
        c.rect(M, y, sum(widths), 7*mm, fill=1, stroke=0)
        c.setStrokeColor(LBLUE)
        c.setLineWidth(0.4)
        c.rect(M, y, sum(widths), 7*mm, fill=0, stroke=1)
        c.setFont(KRB, 9)
        c.setFillColor(NAVY)
        c.drawCentredString(M + widths[0]/2, y + 2, period)
        c.setFont(KR, 9)
        c.setFillColor(DGRAY)
        c.drawString(M + widths[0] + 4, y + 2, content)
        y -= 7*mm

    y -= 8*mm
    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '수상 / 인정 내역')
    y -= 16*mm

    awards2 = [
        '농림축산식품부장관상 수상',
        '신지식농업인상 수상',
        '3년 연속 주류대상 수상',
        '2025 K-SUUL AWARD 우수상',
        'Asia Wine Trophy Best Producer South Korea',
    ]
    for i, aw in enumerate(awards2):
        bg = WHITE if i % 2 == 0 else LGRAY
        c.setFillColor(bg)
        c.rect(M, y, W - 2*M, 7*mm, fill=1, stroke=0)
        c.setStrokeColor(LBLUE)
        c.setLineWidth(0.4)
        c.rect(M, y, W - 2*M, 7*mm, fill=0, stroke=1)
        c.setFillColor(GOLD)
        c.circle(M + 5*mm, y + 3.5*mm, 2*mm, fill=1, stroke=0)
        c.setFont(KR, 9)
        c.setFillColor(DGRAY)
        c.drawString(M + 10*mm, y + 2, aw)
        y -= 7*mm


def draw_page6(c):
    """시장 동향 & 매출 전망"""
    page_header(c, '시장 동향 & 매출 전망', '오드린 농업회사법인(주)')
    page_footer(c, 6)
    y = H - 30*mm

    # 시장 규모 강조 박스 3개
    metrics = [
        ('국내 와인시장 규모', '13조 원', '2024년 기준'),
        ('연평균 성장률', '3.6%', 'CAGR'),
        ('국내 생산 와인 점유율', '극히 낮음', '블루오션 시장'),
    ]
    mw = (W - 2*M - 8*mm) / 3
    for i, (label, val, sub) in enumerate(metrics):
        mx = M + i * (mw + 4*mm)
        c.setFillColor(NAVY)
        c.roundRect(mx, y - 22*mm, mw, 23*mm, 5, fill=1, stroke=0)
        c.setFont(KR, 8)
        c.setFillColor(LBLUE)
        c.drawCentredString(mx + mw/2, y - 6*mm, label)
        c.setFont(KRB, 16)
        c.setFillColor(GOLD)
        c.drawCentredString(mx + mw/2, y - 13*mm, val)
        c.setFont(KR, 7.5)
        c.setFillColor(GRAY)
        c.drawCentredString(mx + mw/2, y - 19*mm, sub)
    y -= 30*mm

    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '시장 동향 분석')
    y -= 16*mm

    draw_text_block(c,
        '국내 와인 시장은 2024년 기준 약 13조원 규모로, 1인 가구 증가·외식 문화 다양화·건강 지향 소비 트렌드에 힘입어 '
        '연평균 3.6%의 안정적 성장세를 유지하고 있습니다.\n\n'
        '그러나 현재 국내 와인 시장의 대부분은 수입 와인이 차지하고 있으며, '
        '국내산 포도를 원료로 한 순수 국내 생산 와인은 극히 드문 블루오션 영역입니다.\n\n'
        '최근 K-푸드 열풍과 함께 국산 발효·양조 제품에 대한 국내외 관심이 높아지고 있어, '
        '오드린의 "국내산 포도 100% + 와인명인 양조" 포지셔닝은 시장 차별화 요소로 강력하게 작용합니다.',
        M, y, W - 2*M, KR, 9.5, DGRAY)
    y -= 40*mm

    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '오드린 매출 추이')
    y -= 16*mm

    widths = [45*mm, 45*mm, 50*mm, W - 2*M - 140*mm]
    table_header_row(c, M, y, ['연도', '매출액', '성장률', '비고'], widths, 7*mm)
    y -= 7*mm
    rows = [
        ('2024', '134,600,000원', '—', '사업 초기 안정화'),
        ('2025', '160,620,000원', '+19.3%', '온라인 채널 확대'),
        ('2026(목표)', '250,000,000원', '+55.7%', '신제품 2라인 출시'),
        ('2027(목표)', '350,000,000원', '+40.0%', 'B2B·수출 본격화'),
    ]
    for i, row in enumerate(rows):
        bg = WHITE if i % 2 == 0 else LGRAY
        c.setFillColor(bg)
        c.rect(M, y, sum(widths), 7*mm, fill=1, stroke=0)
        c.setStrokeColor(LBLUE)
        c.setLineWidth(0.4)
        c.rect(M, y, sum(widths), 7*mm, fill=0, stroke=1)
        cx = M
        for j, (val, w) in enumerate(zip(row, widths)):
            font = KRB if j == 1 else KR
            color = GOLD if i >= 2 and j == 1 else DGRAY
            c.setFont(font, 9)
            c.setFillColor(color)
            c.drawCentredString(cx + w/2, y + 2, val)
            cx += w
        y -= 7*mm


def draw_page7(c):
    """매출 향상 계획 (1)"""
    page_header(c, '매출 향상 계획 (1)  ★', '오드린 농업회사법인(주)')
    page_footer(c, 7)
    y = H - 30*mm

    # 골드 강조 타이틀
    c.setFillColor(GOLD)
    c.roundRect(M, y - 10*mm, W - 2*M, 11*mm, 4, fill=1, stroke=0)
    c.setFont(KRB, 12)
    c.setFillColor(NAVY)
    c.drawCentredString(W/2, y - 5*mm, '오드린 농업회사법인(주)  매출 계획')
    y -= 18*mm

    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '매출 구조')
    y -= 16*mm

    rev_items = [
        ('와인 판매 (직판·온라인)', '병당 평균 25,000~65,000원', '온라인 쇼핑몰 + 자사몰'),
        ('B2B 납품 (레스토랑·호텔)', '케이스 단위 납품, 건당 500만~1,500만원', '대기업 거래처 발굴 중'),
        ('맞춤형 와인 OEM·선물세트', '행사·기업선물 특화 상품', '매년 신제품 2라인 출시'),
        ('수출 (해외 시장)', '아시아·북미 시장 진입 추진', '수상 경력 활용 프리미엄 포지셔닝'),
    ]
    widths = [52*mm, 72*mm, W - 2*M - 124*mm]
    table_header_row(c, M, y, ['매출 항목', '단가 / 규모', '채널 전략'], widths, 7*mm)
    y -= 7*mm
    for i, row in enumerate(rev_items):
        bg = WHITE if i % 2 == 0 else LGRAY
        c.setFillColor(bg)
        c.rect(M, y, sum(widths), 7*mm, fill=1, stroke=0)
        c.setStrokeColor(LBLUE)
        c.setLineWidth(0.4)
        c.rect(M, y, sum(widths), 7*mm, fill=0, stroke=1)
        cx = M
        for val, w in zip(row, widths):
            c.setFont(KR, 8.5)
            c.setFillColor(DGRAY)
            c.drawCentredString(cx + w/2, y + 2, val)
            cx += w
        y -= 7*mm

    y -= 8*mm
    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '연도별 매출 실적 및 목표')
    y -= 16*mm

    # 수치 강조 카드
    cards = [
        ('2024\n실적', '134,600,000원', BLUE),
        ('2025\n실적', '160,620,000원', BLUE),
        ('2026\n목표', '250,000,000원', NAVY),
        ('2027\n목표', '350,000,000원', GOLD),
    ]
    cw = (W - 2*M - 9*mm) / 4
    cx = M
    for label, val, bg in cards:
        c.setFillColor(bg)
        c.roundRect(cx, y - 26*mm, cw, 27*mm, 5, fill=1, stroke=0)
        c.setFont(KR, 8)
        c.setFillColor(WHITE if bg != GOLD else NAVY)
        # label에 줄바꿈 처리
        for li, ln in enumerate(label.split('\n')):
            c.drawCentredString(cx + cw/2, y - 7*mm - li*10, ln)
        c.setFont(KRB, 10)
        c.setFillColor(GOLD if bg == NAVY else (WHITE if bg != GOLD else NAVY))
        # 값 줄바꿈
        val_lines = ['₩ ' + val.replace('원', ''), '원']
        c.drawCentredString(cx + cw/2, y - 18*mm, '₩ ' + val.replace('원',''))
        c.setFont(KRB, 8)
        c.drawCentredString(cx + cw/2, y - 23*mm, '원')
        cx += cw + 3*mm
    y -= 34*mm

    # 핵심 목표 강조
    c.setFillColor(colors.HexColor('#162D56'))
    c.roundRect(M, y - 14*mm, W - 2*M, 15*mm, 4, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.roundRect(M, y - 14*mm, W - 2*M, 15*mm, 4, fill=0, stroke=1)
    c.setFont(KRB, 12)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, y - 5*mm, '2026년 목표  ₩ 250,000,000원  →  2027년 목표  ₩ 350,000,000원')
    c.setFont(KR, 9)
    c.setFillColor(LBLUE)
    c.drawCentredString(W/2, y - 11*mm, '2024년 대비 2년 내 2.6배 성장  |  연평균 성장률 +61%')


def draw_page8(c):
    """매출 향상 계획 (2)"""
    page_header(c, '매출 향상 계획 (2)  ★', '오드린 농업회사법인(주)')
    page_footer(c, 8)
    y = H - 30*mm

    c.setFillColor(GOLD)
    c.roundRect(M, y - 10*mm, W - 2*M, 11*mm, 4, fill=1, stroke=0)
    c.setFont(KRB, 12)
    c.setFillColor(NAVY)
    c.drawCentredString(W/2, y - 5*mm, '매출 달성 목표 — 채널별 세부 계획')
    y -= 18*mm

    channels = [
        ('① 온라인 채널 확대',
         '자사몰 + 네이버스토어 + 쿠팡·마켓컬리 입점\n'
         '월 평균 판매 목표: 300병 → 800병 (2026년)\n'
         '병당 평균 단가: 35,000원\n'
         '= 월 매출 28,000,000원  ×  12개월  =  연 336,000,000원',
         '→ 온라인 연 매출 목표  ₩ 3억 3,600만원'),
        ('② 대기업 B2B 납품',
         '현재 수주 협의 중 10개사 계약 목표\n'
         '건당 평균 계약 규모: 500만~1,500만원\n'
         '= 연간 B2B 납품 목표  ₩ 5,000만원~1억원',
         '→ B2B 연 매출 목표  ₩ 5,000만원 이상'),
        ('③ 맞춤형·선물세트 OEM',
         '기업 행사·기념품·명절 선물세트 특화 상품 출시\n'
         '2026년 신제품 2개 라인 출시 예정\n'
         '= 연간 OEM·선물세트 목표  ₩ 3,000만원',
         '→ 시즌 집중 마케팅 병행'),
        ('④ 해외 수출',
         'Asia Wine Trophy 수상 실적 기반 해외 바이어 접촉\n'
         '1차 타깃: 일본·싱가포르·홍콩 와인 시장\n'
         '= 2026년 수출 시범 목표  ₩ 1,000만원',
         '→ 수출 성과 달성 시 2027년 본격 확대'),
    ]

    ch_h = 32*mm
    for i, (title, body, summary) in enumerate(channels):
        by = y - i * (ch_h + 4*mm)
        # 채널 박스
        c.setFillColor(LGRAY)
        c.roundRect(M, by - ch_h + 4*mm, W - 2*M, ch_h - 3*mm, 4, fill=1, stroke=0)
        # 왼쪽 컬러 바
        bar_color = [GOLD, NAVY, BLUE, colors.HexColor('#4A90D9')][i]
        c.setFillColor(bar_color)
        c.roundRect(M, by - ch_h + 4*mm, 3*mm, ch_h - 3*mm, 2, fill=1, stroke=0)
        # 제목
        c.setFont(KRB, 10)
        c.setFillColor(NAVY)
        c.drawString(M + 7*mm, by - 7*mm, title)
        # 본문
        draw_text_block(c, body, M + 7*mm, by - 14*mm, W - 2*M - 75*mm, KR, 8.5, DGRAY, 11)
        # 요약 강조
        c.setFillColor(bar_color)
        c.roundRect(W - M - 65*mm, by - ch_h + 8*mm, 63*mm, 14*mm, 3, fill=1, stroke=0)
        c.setFont(KRB, 8)
        c.setFillColor(WHITE if bar_color != GOLD else NAVY)
        # 요약 줄바꿈
        for li, ln in enumerate(wrap_text(c, summary, 58*mm, KRB, 8)):
            c.drawCentredString(W - M - 33.5*mm, by - ch_h + 18*mm - li*10, ln)


def draw_page9(c):
    """매출 달성 근거"""
    page_header(c, '매출 달성 근거', '오드린 농업회사법인(주)')
    page_footer(c, 9)
    y = H - 30*mm

    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '국내 와인 시장 분석')
    y -= 16*mm

    draw_text_block(c,
        '통계청·한국주류산업협회 자료에 따르면 국내 와인 시장 규모는 2024년 기준 약 13조원으로 집계됩니다. '
        '동 시장은 1인 가구 증가, 홈술 문화 정착, 건강 지향 음주 트렌드에 힘입어 연평균 3.6%의 성장세를 지속하고 있습니다.\n\n'
        '특히 국내산 포도를 원료로 한 순수 국내 생산 와인은 전체 시장의 극히 일부에 불과하여, '
        '"국산 포도 100%"를 내세운 오드린의 시장 진입 공간은 매우 넓은 상황입니다.',
        M, y, W - 2*M, KR, 9.5, DGRAY)
    y -= 30*mm

    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '오드린 영업 인프라 및 근거')
    y -= 16*mm

    evidence = [
        ('현재 거래처',     '20개 업체 확보 (온라인 채널 중심)'),
        ('수주 예정',       '10개사 B2B 납품 계약 협의 진행 중'),
        ('신제품 계획',     '2026년 2개 라인 신제품 출시 예정'),
        ('수상 경력',       '3년 연속 주류대상 · Asia Wine Trophy 수상으로 품질 공신력 확보'),
        ('특허 기술',       '오미자 로제(등록) + 샤인머스켓 블랜딩(출원) — 독점 레시피 보유'),
        ('시장 차별성',     '국내산 포도 100% + 와인명인 숙성 — 국내 동종 경쟁사 전무'),
    ]
    widths = [35*mm, W - 2*M - 35*mm]
    table_header_row(c, M, y, ['근거 항목', '내용'], widths, 7*mm)
    y -= 7*mm
    for i, row in enumerate(evidence):
        bg = WHITE if i % 2 == 0 else LGRAY
        c.setFillColor(bg)
        c.rect(M, y, sum(widths), 7*mm, fill=1, stroke=0)
        c.setStrokeColor(LBLUE)
        c.setLineWidth(0.4)
        c.rect(M, y, sum(widths), 7*mm, fill=0, stroke=1)
        c.setFont(KRB, 9)
        c.setFillColor(NAVY)
        c.drawCentredString(M + widths[0]/2, y + 2, row[0])
        c.setFont(KR, 9)
        c.setFillColor(DGRAY)
        c.drawString(M + widths[0] + 4, y + 2, row[1])
        y -= 7*mm

    y -= 8*mm
    # 결론 강조 박스
    c.setFillColor(colors.HexColor('#162D56'))
    c.roundRect(M, y - 16*mm, W - 2*M, 17*mm, 4, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.roundRect(M, y - 16*mm, W - 2*M, 17*mm, 4, fill=0, stroke=1)
    c.setFont(KRB, 10)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, y - 5*mm, '결론')
    c.setFont(KR, 9)
    c.setFillColor(WHITE)
    c.drawCentredString(W/2, y - 11*mm,
        '13조원 시장 + 연 3.6% 성장 + 국내산 와인 희소성 + 검증된 기술력 = 충분한 매출 달성 근거 확보')


def draw_page10(c):
    """자금 소요 계획"""
    page_header(c, '자금 소요 계획', '오드린 농업회사법인(주)')
    page_footer(c, 10)
    y = H - 30*mm

    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '항목별 자금 소요')
    y -= 16*mm

    funds = [
        ('설비 투자',     '양조 설비 고도화 · 냉각·보관 창고 확충',   '1억원',    '100,000,000'),
        ('인건비',        '생산인력 채용 (1~2명) × 6개월',              '5천만원',  '50,000,000'),
        ('마케팅·박람회', '국내외 와인 박람회 참가 · SNS·온라인 광고', '5천만원',  '50,000,000'),
    ]
    total = '2억원 (200,000,000원)'

    widths = [30*mm, 72*mm, 28*mm, 45*mm]
    table_header_row(c, M, y, ['항목', '세부 내용', '금액', '산출 근거'], widths, 7*mm)
    y -= 7*mm
    for i, (cat, detail, amt, calc) in enumerate(funds):
        bg = WHITE if i % 2 == 0 else LGRAY
        c.setFillColor(bg)
        c.rect(M, y, sum(widths), 8*mm, fill=1, stroke=0)
        c.setStrokeColor(LBLUE)
        c.setLineWidth(0.4)
        c.rect(M, y, sum(widths), 8*mm, fill=0, stroke=1)
        cx = M
        for j, (val, w) in enumerate(zip([cat, detail, amt, calc], widths)):
            font = KRB if j in (0, 2) else KR
            color = NAVY if j == 0 else (GOLD if j == 2 else DGRAY)
            c.setFont(font, 9)
            c.setFillColor(color)
            c.drawCentredString(cx + w/2, y + 2.5, val)
            cx += w
        y -= 8*mm

    # 합계 행
    c.setFillColor(NAVY)
    c.rect(M, y, sum(widths), 9*mm, fill=1, stroke=0)
    c.setFont(KRB, 11)
    c.setFillColor(WHITE)
    c.drawString(M + 6, y + 2.5, '총 필요 자금')
    c.setFillColor(GOLD)
    c.drawRightString(M + sum(widths) - 6, y + 2.5, total)
    y -= 18*mm

    section_box(c, M, y - 7*mm, W - 2*M, 7*mm, '자금 집행 타임라인')
    y -= 16*mm

    # 타임라인 바
    quarters = ['2026 Q1\n(1~3월)', '2026 Q2\n(4~6월)', '2026 Q3\n(7~9월)', '2026 Q4\n(10~12월)']
    q_plans = [
        ['설비투자 착수\n(5천만원)'],
        ['설비 완공\n+ 인건비 집행\n(5천만원)'],
        ['마케팅·박람회\n참가 (3천만원)'],
        ['마케팅 지속\n+ 여유자금\n(2천만원)'],
    ]
    qw = (W - 2*M) / 4
    for i, (q, plans) in enumerate(zip(quarters, q_plans)):
        qx = M + i * qw
        bg = [NAVY, BLUE, colors.HexColor('#4A90D9'), LGRAY][i]
        fg = WHITE if bg != LGRAY else DGRAY
        c.setFillColor(bg)
        c.rect(qx, y - 24*mm, qw - 1, 25*mm, fill=1, stroke=0)
        c.setFont(KR, 8)
        c.setFillColor(fg)
        for li, ln in enumerate(q.split('\n')):
            c.drawCentredString(qx + qw/2, y - 6*mm - li*9, ln)
        c.setFont(KR, 7.5)
        for li, ln in enumerate(plans[0].split('\n')):
            c.drawCentredString(qx + qw/2, y - 16*mm - li*9, ln)
    y -= 32*mm

    # 총액 강조
    c.setFillColor(colors.HexColor('#162D56'))
    c.roundRect(M, y - 12*mm, W - 2*M, 13*mm, 4, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.roundRect(M, y - 12*mm, W - 2*M, 13*mm, 4, fill=0, stroke=1)
    c.setFont(KRB, 13)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, y - 4*mm, '총 사업비 필요 금액  :  2억원  (200,000,000원)')
    c.setFont(KR, 9)
    c.setFillColor(LBLUE)
    c.drawCentredString(W/2, y - 10*mm, '설비투자 1억 + 인건비 5천만 + 마케팅·박람회 5천만')


def draw_page11(c):
    """맺음말"""
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 6*mm, W, 6*mm, fill=1, stroke=0)
    c.rect(0, 0, W, 5*mm, fill=1, stroke=0)

    c.setFont(KRB, 46)
    c.setFillColor(WHITE)
    c.drawCentredString(W/2, H*0.62, 'THANK YOU.')

    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(W/2 - 50*mm, H*0.57, W/2 + 50*mm, H*0.57)

    c.setFont(KRB, 14)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, H*0.52, '오드린 농업회사법인(주)')

    c.setFont(KR, 11)
    c.setFillColor(LBLUE)
    c.drawCentredString(W/2, H*0.47, '대표이사  박천명')

    c.setFont(KR, 11)
    c.setFillColor(colors.HexColor('#8AADCF'))
    c.drawCentredString(W/2, H*0.4, 'T. 010-2466-7789')
    c.drawCentredString(W/2, H*0.36, '브랜드: 월류봉  ·  베베마루')

    c.setStrokeColor(colors.HexColor('#2A4A7A'))
    c.setLineWidth(0.5)
    c.line(W/2 - 50*mm, H*0.31, W/2 + 50*mm, H*0.31)

    c.setFont(KR, 9)
    c.setFillColor(GRAY)
    c.drawCentredString(W/2, H*0.26,
        '본 사업계획서는 정책자금 신청용 초안입니다. 금융기관 제출 전 전문가 검토를 권장합니다.')
    c.setFont(KR, 8)
    c.setFillColor(colors.HexColor('#5A7FA8'))
    c.drawCentredString(W/2, 8*mm, '히어컴퍼니 기업컨설팅 제공')


# ── 빌드 ─────────────────────────────────────────────────────────────
def build():
    out = Path(__file__).parent / f'오드린_정책자금_사업계획서_{datetime.date.today().strftime("%Y%m%d")}.pdf'
    c = pdfcanvas.Canvas(str(out), pagesize=A4)

    draw_page1(c);  c.showPage()
    draw_page2(c);  c.showPage()
    draw_page3(c);  c.showPage()
    draw_page4(c);  c.showPage()
    draw_page5(c);  c.showPage()
    draw_page6(c);  c.showPage()
    draw_page7(c);  c.showPage()
    draw_page8(c);  c.showPage()
    draw_page9(c);  c.showPage()
    draw_page10(c); c.showPage()
    draw_page11(c); c.showPage()

    c.save()
    print(f'✅ PDF 생성 완료: {out}')
    return out

if __name__ == '__main__':
    build()
