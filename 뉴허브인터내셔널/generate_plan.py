# -*- coding: utf-8 -*-
"""
(주)뉴허브인터내셔널 — 정책자금 사업계획서 PDF 빌더
표준 11페이지 양식 (올파이낸셜에셋 톤) / 16:9 슬라이드 / 네이비+골드
작성: 히어컴퍼니 (HearCompany) Corporate Consulting
"""
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib import colors
from pathlib import Path
import datetime

# ── 폰트 등록 ─────────────────────────────────────────
pdfmetrics.registerFont(UnicodeCIDFont('HYGothic-Medium'))
pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))
KR  = 'HYGothic-Medium'
KRB = 'HYSMyeongJo-Medium'

# ── 슬라이드 사이즈 16:9 (PowerPoint 와이드) ─────────
SW, SH = 960, 540
MX = 36         # 좌우 여백
HEADER_H = 40   # 상단 헤더 바
FOOTER_H = 22   # 하단 푸터

# ── 컬러 팔레트 ──────────────────────────────────────
NAVY      = colors.HexColor('#0F2340')
NAVY_DK   = colors.HexColor('#08182E')
NAVY_LT   = colors.HexColor('#1B3A6B')
GOLD      = colors.HexColor('#F39C12')
GOLD_LT   = colors.HexColor('#FFB343')
GOLD_PALE = colors.HexColor('#FFE6B8')
WHITE     = colors.white
BLACK     = colors.HexColor('#1A1A1A')
GRAY      = colors.HexColor('#7A7A7A')
GRAY_LT   = colors.HexColor('#D8DDE5')
BG_GRAY   = colors.HexColor('#F4F6FA')
BG_NAVY_LT= colors.HexColor('#E7ECF4')
GREEN_OK  = colors.HexColor('#2E8B57')
RED_WARN  = colors.HexColor('#C0392B')

COMPANY_KO = '(주)뉴허브인터내셔널'
COMPANY_EN = 'NewHub International Co., Ltd.'
DATE_STR   = '2026.05.08'
BRAND_LINE = '히어컴퍼니 (HearCompany) Corporate Consulting'

# ── 유틸 ─────────────────────────────────────────────
def draw_header_bar(c, page_no, total=11):
    """공통 헤더 바 (표지·맺음말 제외)"""
    c.setFillColor(NAVY)
    c.rect(0, SH - HEADER_H, SW, HEADER_H, stroke=0, fill=1)
    # 좌측 골드 액센트
    c.setFillColor(GOLD)
    c.rect(0, SH - HEADER_H, 6, HEADER_H, stroke=0, fill=1)
    # 좌측 텍스트
    c.setFillColor(WHITE)
    c.setFont(KR, 10)
    c.drawString(MX, SH - HEADER_H + 15, COMPANY_KO + ' · 정책자금 사업계획서')
    # 우측 브랜드
    c.setFont(KR, 9)
    c.setFillColor(GOLD_LT)
    c.drawRightString(SW - MX, SH - HEADER_H + 15, BRAND_LINE)
    # 페이지 번호 (작게)
    c.setFillColor(WHITE)
    c.setFont(KR, 8)
    c.drawRightString(SW - MX, SH - HEADER_H + 4, f'P. {page_no:02d} / {total:02d}')

def draw_footer_bar(c, page_no):
    """공통 푸터 (표지·맺음말 제외)"""
    c.setFillColor(NAVY)
    c.rect(0, 0, SW, FOOTER_H, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont(KR, 8)
    c.drawString(MX, 7, f'작성일 {DATE_STR} · 신용보증재단 보증신청용 (1.5억)')
    c.setFillColor(GOLD_LT)
    c.drawRightString(SW - MX, 7, BRAND_LINE)

def section_title(c, num, title, sub=''):
    """페이지 좌상단 섹션 타이틀 (번호 박스 + 제목)"""
    y = SH - HEADER_H - 38
    # 번호 박스 (네이비)
    c.setFillColor(NAVY)
    c.rect(MX, y, 36, 36, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(MX, y, 36, 4, stroke=0, fill=1)  # 골드 액센트 라인
    c.setFillColor(WHITE)
    c.setFont(KRB, 16)
    c.drawCentredString(MX + 18, y + 11, num)
    # 타이틀
    c.setFillColor(NAVY)
    c.setFont(KRB, 22)
    c.drawString(MX + 50, y + 14, title)
    if sub:
        c.setFillColor(GRAY)
        c.setFont(KR, 10)
        c.drawString(MX + 50, y - 2, sub)
    # 하단 골드 라인
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(MX, y - 12, SW - MX, y - 12)
    return y - 22  # content top y

def wrap_text(text, max_chars):
    """단순 글자수 기반 줄바꿈 (한글 폭 보정)"""
    out = []
    line = ''
    for ch in text:
        if ch == '\n':
            out.append(line)
            line = ''
            continue
        line += ch
        if len(line) >= max_chars:
            out.append(line)
            line = ''
    if line:
        out.append(line)
    return out

# =====================================================
# P1 — 표지
# =====================================================
def page_cover(c):
    # 풀 네이비 배경
    c.setFillColor(NAVY)
    c.rect(0, 0, SW, SH, stroke=0, fill=1)
    # 좌측 골드 사이드바
    c.setFillColor(GOLD)
    c.rect(0, 0, 12, SH, stroke=0, fill=1)
    # 우상단 골드 액센트 (다이아 라인)
    c.setFillColor(GOLD_LT)
    c.rect(SW - 220, SH - 80, 180, 4, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(SW - 220, SH - 95, 60, 4, stroke=0, fill=1)

    # 상단 라벨
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 11)
    c.drawString(MX + 16, SH - 70, BRAND_LINE)
    c.setFillColor(WHITE)
    c.setFont(KR, 10)
    c.drawString(MX + 16, SH - 88, 'CORPORATE BUSINESS PROPOSAL  ·  POLICY FUND')

    # 메인 타이틀
    c.setFillColor(WHITE)
    c.setFont(KRB, 56)
    c.drawString(MX + 16, SH - 200, '정책자금')
    c.setFont(KRB, 56)
    c.drawString(MX + 16, SH - 260, '사업계획서')

    # 골드 강조 박스
    c.setFillColor(GOLD)
    c.rect(MX + 16, SH - 295, 320, 4, stroke=0, fill=1)

    # 회사명 (영문 + 한글)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 13)
    c.drawString(MX + 16, SH - 325, COMPANY_EN)
    c.setFillColor(WHITE)
    c.setFont(KRB, 28)
    c.drawString(MX + 16, SH - 358, COMPANY_KO)

    # 한 줄 소개
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 13)
    c.drawString(MX + 16, SH - 390, '유럽 K-뷰티·K-푸드 B2B 수출 · Brand Curation 전문 무역회사')

    # 신청 자금 박스
    c.setFillColor(GOLD)
    c.rect(MX + 16, SH - 440, 280, 36, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KRB, 16)
    c.drawString(MX + 28, SH - 430, '신용보증재단 보증 신청  1.5억 원')

    # 하단 정보 박스 (우측 정렬)
    c.setFillColor(WHITE)
    c.setFont(KR, 10)
    info_y = 80
    c.drawRightString(SW - MX, info_y + 36, '제출처  |  신용보증재단')
    c.drawRightString(SW - MX, info_y + 22, '연락처  |  T. [회사 기재]   E. [회사 기재]')
    c.drawRightString(SW - MX, info_y + 8,  '주  소  |  서울시 강서구 마곡 중앙1로 10. 802호')
    c.setFillColor(GOLD_LT)
    c.drawRightString(SW - MX, info_y - 8,  f'작성일  |  {DATE_STR}')

    # 하단 푸터 라인
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(MX + 16, 40, SW - MX, 40)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 8)
    c.drawString(MX + 16, 26, 'Confidential — For Policy Fund Application Only')
    c.drawRightString(SW - MX, 26, 'HearCompany Corporate Consulting')

    c.showPage()

# =====================================================
# P2 — 회사 주요 사업 소개
# =====================================================
def page_business_intro(c):
    draw_header_bar(c, 2)
    draw_footer_bar(c, 2)
    y0 = section_title(c, '01', '회사 주요 사업 소개', 'Main Business Overview')

    # 좌측 컬러 박스 (네이비)
    box_x, box_y, box_w, box_h = MX, 90, 320, y0 - 110
    c.setFillColor(NAVY)
    c.rect(box_x, box_y, box_w, box_h, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(box_x, box_y + box_h - 4, box_w, 4, stroke=0, fill=1)

    # 좌측 박스 콘텐츠
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 11)
    c.drawString(box_x + 20, box_y + box_h - 32, 'CORE IDENTITY')
    c.setFillColor(WHITE)
    c.setFont(KRB, 22)
    c.drawString(box_x + 20, box_y + box_h - 64, COMPANY_KO + '은')
    c.setFont(KRB, 16)
    c.drawString(box_x + 20, box_y + box_h - 92, '유럽 K-뷰티·K-푸드')
    c.drawString(box_x + 20, box_y + box_h - 112, 'B2B 수출 + Brand Curation')
    c.drawString(box_x + 20, box_y + box_h - 132, '전문 무역회사입니다.')

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    desc_y = box_y + box_h - 175
    desc_lines = [
        '단순 수출이 아닌 — 상담을 통한',
        '바이어 입장 맞춤 제품·브랜드 제안으로',
        '신뢰 기반 Brand Curation을 진행합니다.',
        '',
        '유럽 프랜차이즈·대형마트 거래선과',
        '장기 파트너십 기반 신뢰 거래를 형성하며,',
        '4개 국어(한·영·불·아랍) 시장 대응 인프라를',
        '갖추어 EMEA·MENA 동시 공략이 가능합니다.',
    ]
    for ln in desc_lines:
        c.drawString(box_x + 20, desc_y, ln)
        desc_y -= 14

    # 우측 — 4대 카테고리 카드
    right_x = box_x + box_w + 24
    right_w = SW - MX - right_x
    cat_y = y0 - 8
    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(right_x, cat_y, '주력 품목 4대 카테고리')
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(right_x, cat_y - 6, right_x + 200, cat_y - 6)

    cats = [
        ('①', '화장품 (K-뷰티)', '유럽 인디 브랜드 수요 대응'),
        ('②', '식품 (K-푸드)', '한류 효과 시장 진입 가속'),
        ('③', '기계',           '산업재 수출 확대'),
        ('④', '해외 업무 컨설팅','거래선 매칭·시장 진입 자문'),
    ]
    card_top = cat_y - 24
    for i, (n, t, d) in enumerate(cats):
        row = i // 2
        col = i % 2
        cw = (right_w - 12) / 2
        cx = right_x + col * (cw + 12)
        cy = card_top - row * 88
        c.setFillColor(BG_GRAY)
        c.rect(cx, cy - 76, cw, 76, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(cx, cy - 4, 36, 4, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.setFont(KRB, 26)
        c.drawString(cx + 12, cy - 38, n)
        c.setFillColor(NAVY)
        c.setFont(KRB, 13)
        c.drawString(cx + 50, cy - 26, t)
        c.setFillColor(GRAY)
        c.setFont(KR, 9)
        c.drawString(cx + 50, cy - 44, d)
        c.setFillColor(NAVY_LT)
        c.setFont(KR, 8)
        c.drawString(cx + 12, cy - 66, 'CATEGORY')

    # 하단 거래처 배지
    bx = right_x
    by = card_top - 2 * 88 - 14
    c.setFillColor(NAVY)
    c.setFont(KRB, 12)
    c.drawString(bx, by, '주요 거래처')
    by -= 24
    badges = ['유럽 Franchise Shop', '유럽 대형마트', '미국 온라인 (예정)', '해외 인플루언서 (예정)']
    bx_cur = bx
    for b in badges:
        w = 8 + len(b) * 6.2
        c.setFillColor(GOLD_PALE)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.roundRect(bx_cur, by - 16, w, 18, 9, stroke=1, fill=1)
        c.setFillColor(NAVY)
        c.setFont(KR, 9)
        c.drawString(bx_cur + 8, by - 12, b)
        bx_cur += w + 6
        if bx_cur + 80 > SW - MX:
            bx_cur = bx
            by -= 22

    c.showPage()

# =====================================================
# P3 — 회사 장점·기술력
# =====================================================
def page_strengths(c):
    draw_header_bar(c, 3)
    draw_footer_bar(c, 3)
    y0 = section_title(c, '02', '회사 장점 · 기술력', 'Core Strengths & Capabilities')

    items = [
        ('①', 'Brand Curation 차별화',
         '단순 수출이 아닌 바이어 입장 분석을 통한',
         '맞춤 제품·브랜드 제안. 장기 파트너십 기반 신뢰 거래.'),
        ('②', '다국어 4개 국어 역량',
         '한·영·불·아랍어 4개 국어 K-connect hub 구축 예정.',
         'EMEA·MENA 시장 동시 공략 가능 인프라.'),
        ('③', '해외 트렌드 대응 속도',
         '해외 시장 트렌드 빠른 접수 → 대응 제품 빠른 선정.',
         '바이어 요청 → 소싱 → 제안 평균 1~2주 소요.'),
        ('④', '수출실적증명원 발급 가능 B2B',
         '유럽 다거래선 B2B 실거래 입증 가능.',
         '수출 가산점 적격 요건 충족 — 정책자금 우대.'),
    ]

    card_top = y0 - 6
    cw = (SW - MX * 2 - 16) / 2
    ch = 130
    for i, (n, t, l1, l2) in enumerate(items):
        row = i // 2
        col = i % 2
        cx = MX + col * (cw + 16)
        cy = card_top - row * (ch + 12)

        c.setFillColor(BG_GRAY)
        c.setStrokeColor(GRAY_LT)
        c.setLineWidth(0.8)
        c.rect(cx, cy - ch, cw, ch, stroke=1, fill=1)
        c.setFillColor(GOLD)
        c.rect(cx, cy - ch, 6, ch, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont(KRB, 36)
        c.drawString(cx + 22, cy - 50, n)
        c.setFillColor(NAVY)
        c.setFont(KRB, 15)
        c.drawString(cx + 80, cy - 38, t)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(cx + 80, cy - 46, cx + cw - 16, cy - 46)
        c.setFillColor(BLACK)
        c.setFont(KR, 10)
        c.drawString(cx + 80, cy - 66, l1)
        c.setFillColor(GRAY)
        c.setFont(KR, 10)
        c.drawString(cx + 80, cy - 84, l2)
        c.setFillColor(NAVY_LT)
        c.setFont(KR, 8)
        c.drawString(cx + 22, cy - ch + 12, 'STRENGTH')

    # 하단 — 경쟁 우위 포인트 강조 박스
    cu_y = card_top - 2 * (ch + 12) - 6
    c.setFillColor(NAVY)
    c.rect(MX, cu_y - 56, SW - MX * 2, 56, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(MX, cu_y - 4, SW - MX * 2, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(MX + 20, cu_y - 22, 'COMPETITIVE EDGE')
    c.setFillColor(WHITE)
    c.setFont(KRB, 14)
    c.drawString(MX + 20, cu_y - 42, '청년·여성 창업기업 + 매출 7.5배 급성장 + 무차입 청정 신용 — 보증재단 우대 가산 3중 충족')

    c.showPage()

# =====================================================
# P4 — 주요 업적·거래처
# =====================================================
def page_achievements(c):
    draw_header_bar(c, 4)
    draw_footer_bar(c, 4)
    y0 = section_title(c, '03', '주요 업적 · 거래처', 'Track Record & Clients')

    # 좌측 — 매출 막대그래프
    chart_x = MX
    chart_y = 110
    chart_w = 470
    chart_h = y0 - chart_y - 16

    c.setFillColor(BG_GRAY)
    c.rect(chart_x, chart_y, chart_w, chart_h, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(chart_x, chart_y + chart_h - 4, chart_w, 4, stroke=0, fill=1)

    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(chart_x + 16, chart_y + chart_h - 28, '매출 추이 — 7.5배 급성장 + 흑자전환')
    c.setFillColor(GRAY)
    c.setFont(KR, 9)
    c.drawString(chart_x + 16, chart_y + chart_h - 44, '단위: 백만 원')

    bars = [
        ('2023',    75, '결손', GRAY_LT),
        ('2024',   115, '결손', GRAY),
        ('2025',   860, '흑자전환', GOLD),
        ('2026 1Q',200, '진행중', NAVY_LT),
    ]
    max_val = 900
    plot_x = chart_x + 50
    plot_y = chart_y + 36
    plot_h = chart_h - 90
    plot_w = chart_w - 80
    bar_w = 60
    gap = (plot_w - bar_w * 4) / 3

    # Y축 그리드
    c.setStrokeColor(GRAY_LT)
    c.setLineWidth(0.4)
    for v in [200, 400, 600, 800]:
        gy = plot_y + (v / max_val) * plot_h
        c.line(plot_x - 4, gy, plot_x + plot_w, gy)
        c.setFillColor(GRAY)
        c.setFont(KR, 8)
        c.drawRightString(plot_x - 8, gy - 3, str(v))

    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(plot_x, plot_y, plot_x + plot_w, plot_y)

    for i, (label, v, tag, col) in enumerate(bars):
        bx = plot_x + i * (bar_w + gap)
        bh = (v / max_val) * plot_h
        c.setFillColor(col)
        c.rect(bx, plot_y, bar_w, bh, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont(KRB, 11)
        c.drawCentredString(bx + bar_w / 2, plot_y + bh + 6, str(v))
        c.setFillColor(BLACK)
        c.setFont(KR, 10)
        c.drawCentredString(bx + bar_w / 2, plot_y - 14, label)
        c.setFillColor(GREEN_OK if tag == '흑자전환' else (GRAY if tag != '진행중' else NAVY_LT))
        c.setFont(KR, 8)
        c.drawCentredString(bx + bar_w / 2, plot_y - 26, tag)

    # 우측 — 거래처 + 성과 박스
    rx = chart_x + chart_w + 16
    rw = SW - MX - rx

    # 성과 수치 강조 박스
    c.setFillColor(NAVY)
    c.rect(rx, y0 - 6 - 110, rw, 110, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(rx, y0 - 6 - 4, rw, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(rx + 14, y0 - 28, 'KEY PERFORMANCE')
    c.setFillColor(WHITE)
    c.setFont(KRB, 30)
    c.drawString(rx + 14, y0 - 64, '7.5배')
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 11)
    c.drawString(rx + 14, y0 - 82, '2024 → 2025 매출 급성장')
    c.setFillColor(WHITE)
    c.setFont(KRB, 14)
    c.drawString(rx + 14, y0 - 104, '흑자전환 (2025)')

    # 거래처 박스
    cl_y = y0 - 6 - 110 - 12
    c.setFillColor(BG_GRAY)
    c.rect(rx, cl_y - 180, rw, 180, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(rx, cl_y - 4, rw, 4, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont(KRB, 13)
    c.drawString(rx + 14, cl_y - 22, '거래처')
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(rx + 14, cl_y - 28, rx + rw - 14, cl_y - 28)
    c.setFillColor(NAVY_LT)
    c.setFont(KR, 9)
    c.drawString(rx + 14, cl_y - 44, 'CURRENT')
    c.setFillColor(BLACK)
    c.setFont(KR, 10)
    c.drawString(rx + 14, cl_y - 60, '· 유럽 Franchise Shop (다수)')
    c.drawString(rx + 14, cl_y - 76, '· 유럽 대형마트')
    c.setFillColor(NAVY_LT)
    c.setFont(KR, 9)
    c.drawString(rx + 14, cl_y - 102, 'EXPECTED')
    c.setFillColor(BLACK)
    c.setFont(KR, 10)
    c.drawString(rx + 14, cl_y - 118, '· 미국 온라인 플랫폼')
    c.drawString(rx + 14, cl_y - 134, '· 해외 인플루언서 마케팅')
    c.setFillColor(GOLD)
    c.setFont(KR, 9)
    c.drawString(rx + 14, cl_y - 160, '※ 수출실적증명원 발급 가능')

    c.showPage()

# =====================================================
# P5 — 대표자 경력·학력·자격증
# =====================================================
def page_ceo(c):
    draw_header_bar(c, 5)
    draw_footer_bar(c, 5)
    y0 = section_title(c, '04', '대표자 소개', 'CEO Profile')

    # 좌측 — 대표 카드 (네이비)
    lx, ly, lw, lh = MX, 110, 280, y0 - 110 - 18
    c.setFillColor(NAVY)
    c.rect(lx, ly, lw, lh, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(lx, ly + lh - 4, lw, 4, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(lx + 24, ly + lh - 80, 60, 60, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KRB, 28)
    c.drawCentredString(lx + 54, ly + lh - 64, 'CEO')

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 11)
    c.drawString(lx + 24, ly + lh - 110, COMPANY_KO)
    c.setFillColor(WHITE)
    c.setFont(KRB, 22)
    c.drawString(lx + 24, ly + lh - 142, '[대표자명] 대표')
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(lx + 24, ly + lh - 158, '※ 회사 기재')

    # 강점 배지
    badge_y = ly + 80
    c.setFillColor(GOLD_PALE)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.roundRect(lx + 24, badge_y, lw - 48, 28, 6, stroke=1, fill=1)
    c.setFillColor(NAVY)
    c.setFont(KRB, 12)
    c.drawCentredString(lx + lw / 2, badge_y + 9, '여성 청년 창업기업 대표')

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawCentredString(lx + lw / 2, badge_y - 16, '보증재단 우대 가산점 · 주식 80% 보유')

    # 우측 — 경력·학력·자격
    rx = lx + lw + 18
    rw = SW - MX - rx

    sec1_top = y0 - 6
    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(rx, sec1_top, '주요 경력')
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(rx, sec1_top - 6, rx + 100, sec1_top - 6)

    careers = [
        ('7년',     '사업 운영 경력'),
        ('2021.03', '(주)뉴허브인터내셔널 창업'),
        ('2025',    '유럽 본격 진입 — 매출 8.6억 흑자전환'),
        ('2026',    '디지털 인프라 + 자체 브랜드 추진'),
    ]
    cy = sec1_top - 22
    for yr, desc in careers:
        c.setFillColor(GOLD)
        c.rect(rx, cy - 18, 70, 22, stroke=0, fill=1)
        c.setFillColor(NAVY_DK)
        c.setFont(KRB, 11)
        c.drawCentredString(rx + 35, cy - 12, yr)
        c.setFillColor(BLACK)
        c.setFont(KR, 11)
        c.drawString(rx + 80, cy - 12, desc)
        cy -= 28

    sec2_top = cy - 6
    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(rx, sec2_top, '주요 학력')
    c.setStrokeColor(GOLD)
    c.line(rx, sec2_top - 6, rx + 100, sec2_top - 6)
    c.setFillColor(BLACK)
    c.setFont(KR, 11)
    c.drawString(rx, sec2_top - 26, '· 불어불문학과 / 아프리카 지역학 전공')

    sec3_top = sec2_top - 56
    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(rx, sec3_top, '보유 자격증')
    c.setStrokeColor(GOLD)
    c.line(rx, sec3_top - 6, rx + 100, sec3_top - 6)
    c.setFillColor(BLACK)
    c.setFont(KR, 11)
    c.drawString(rx, sec3_top - 26, '· 프랑스어 통역 가이드')

    c.showPage()

# =====================================================
# P6 — 시장 동향 + 향후 매출 예상
# =====================================================
def page_market(c):
    draw_header_bar(c, 6)
    draw_footer_bar(c, 6)
    y0 = section_title(c, '05', '시장 동향 · 향후 매출 예상', 'Market Trend & Revenue Outlook')

    # 좌측 — 시장 동향 3개 박스
    lx = MX
    lw = 470
    ly = y0 - 6
    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(lx, ly, '시장 동향')
    c.setStrokeColor(GOLD)
    c.line(lx, ly - 6, lx + 80, ly - 6)

    trends = [
        ('K-뷰티 EMEA 시장',
         'K-뷰티 글로벌 확장세 / 유럽 인디 브랜드 수요 증가',
         '유럽 프랜차이즈·대형마트 입점 가속'),
        ('K-푸드 EMEA 시장',
         'K-푸드 한류 효과 / 유럽 식품 시장 진입 가속',
         '아시안 식품 카테고리 성장'),
        ('디지털 채널',
         'B2B 온라인 편집샵 수요 확대',
         '인플루언서 채널 효과 확산'),
    ]
    ty = ly - 24
    for t, l1, l2 in trends:
        c.setFillColor(BG_GRAY)
        c.rect(lx, ty - 76, lw, 76, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(lx, ty - 4, 4, 76, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont(KRB, 13)
        c.drawString(lx + 16, ty - 22, t)
        c.setFillColor(BLACK)
        c.setFont(KR, 10)
        c.drawString(lx + 16, ty - 42, '· ' + l1)
        c.drawString(lx + 16, ty - 60, '· ' + l2)
        ty -= 86

    # 우측 — 향후 매출 시나리오 박스
    rx = lx + lw + 16
    rw = SW - MX - rx
    rh = y0 - 6 - 110

    c.setFillColor(NAVY)
    c.rect(rx, 110, rw, rh, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(rx, 110 + rh - 4, rw, 4, stroke=0, fill=1)

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(rx + 16, 110 + rh - 26, '2026 REVENUE OUTLOOK')
    c.setFillColor(WHITE)
    c.setFont(KRB, 16)
    c.drawString(rx + 16, 110 + rh - 50, '향후 매출 예상')

    # 보수 (메인)
    c.setFillColor(GOLD)
    c.rect(rx + 16, 110 + rh - 130, rw - 32, 60, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KR, 10)
    c.drawString(rx + 24, 110 + rh - 88, '보수 시나리오 (메인)')
    c.setFont(KRB, 26)
    c.drawString(rx + 24, 110 + rh - 118, '15억 원')

    # 공격
    c.setStrokeColor(GOLD_LT)
    c.setLineWidth(1)
    c.rect(rx + 16, 110 + rh - 200, rw - 32, 50, stroke=1, fill=0)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(rx + 24, 110 + rh - 158, '공격 시나리오')
    c.setFillColor(WHITE)
    c.setFont(KRB, 22)
    c.drawString(rx + 24, 110 + rh - 188, '20억 원')

    # 시차 안내
    c.setFillColor(GOLD_PALE)
    c.rect(rx + 16, 110 + 14, rw - 32, 50, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KRB, 10)
    c.drawString(rx + 24, 110 + 48, '※ 시차 반영')
    c.setFillColor(NAVY)
    c.setFont(KR, 9)
    c.drawString(rx + 24, 110 + 32, 'K-beauty4U·자체 브랜드 가동 후')
    c.drawString(rx + 24, 110 + 20, '6~9개월 시차 보수 반영 — 보수 메인')

    c.showPage()

# =====================================================
# P7 ★ 매출 향상 계획 (1) — 매출 구조
# =====================================================
def page_sales_plan_1(c):
    # 골드 헤더 (★)
    c.setFillColor(GOLD)
    c.rect(0, SH - HEADER_H, SW, HEADER_H, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.rect(0, SH - HEADER_H, 6, HEADER_H, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KRB, 11)
    c.drawString(MX, SH - HEADER_H + 15, '★  ' + COMPANY_KO + ' · 정책자금 사업계획서  ·  매출 향상 계획 (1)')
    c.setFont(KR, 9)
    c.drawRightString(SW - MX, SH - HEADER_H + 15, BRAND_LINE)
    c.setFont(KR, 8)
    c.drawRightString(SW - MX, SH - HEADER_H + 4, 'P. 07 / 11')

    draw_footer_bar(c, 7)

    # 섹션 타이틀
    y = SH - HEADER_H - 38
    c.setFillColor(GOLD)
    c.rect(MX, y, 36, 36, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.rect(MX, y, 36, 4, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KRB, 16)
    c.drawCentredString(MX + 18, y + 11, '06')
    c.setFillColor(NAVY)
    c.setFont(KRB, 22)
    c.drawString(MX + 50, y + 14, '매출 향상 계획 (1)  ·  매출 구조')
    c.setFillColor(GOLD)
    c.setFont(KR, 10)
    c.drawString(MX + 50, y - 2, 'Revenue Plan (1) — Sales Structure')
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(MX, y - 12, SW - MX, y - 12)
    y0 = y - 22

    # 좌측 — 매출 구조 3대 모델
    lx = MX
    lw = 470
    ly = y0 - 6
    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(lx, ly, '[ 매출 구조 ]  3대 매출 모델')
    c.setStrokeColor(GOLD)
    c.line(lx, ly - 6, lx + 200, ly - 6)

    models = [
        ('1', '유럽 B2B 직수출 (기존 안정)',
         '거래당 평균 1,000만 원 × 월 7건',
         '= 월 7,000만 원'),
        ('2', 'K-beauty4U 온라인 B2B 편집샵 (신규·3Q)',
         '가입 바이어 100개사 × 월 평균 50만 원',
         '= 월 5,000만 원'),
        ('3', '자체 브랜드 화장품 (신규·4Q)',
         '거래선당 5,000만 원 × 4개 거래선',
         '= 분기 2억 원'),
    ]
    my = ly - 22
    for n, t, calc, result in models:
        c.setFillColor(BG_GRAY)
        c.rect(lx, my - 70, lw, 70, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.rect(lx, my - 70, 36, 70, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.setFont(KRB, 22)
        c.drawCentredString(lx + 18, my - 42, n)
        c.setFillColor(NAVY)
        c.setFont(KRB, 12)
        c.drawString(lx + 50, my - 18, t)
        c.setFillColor(BLACK)
        c.setFont(KR, 10)
        c.drawString(lx + 50, my - 38, calc)
        c.setFillColor(GOLD)
        c.setFont(KRB, 12)
        c.drawString(lx + 50, my - 56, result)
        my -= 78

    # 우측 — 매출 상황 + 12월 매출 계획
    rx = lx + lw + 16
    rw = SW - MX - rx

    s_top = y0 - 6
    c.setFillColor(NAVY)
    c.setFont(KRB, 13)
    c.drawString(rx, s_top, '[ 매출 상황 ]')
    c.setStrokeColor(GOLD)
    c.line(rx, s_top - 6, rx + 100, s_top - 6)

    rows = [
        ('2023',     '75,000,000원',  '결손'),
        ('2024',     '115,000,000원', '결손'),
        ('2025',     '860,000,000원', '흑자전환'),
        ('2026 1Q',  '200,000,000원', '진행'),
    ]
    ry = s_top - 22
    for yr, amt, tag in rows:
        if yr == '2025':
            c.setFillColor(GOLD_PALE)
            c.rect(rx, ry - 22, rw, 22, stroke=0, fill=1)
        else:
            c.setFillColor(BG_GRAY)
            c.rect(rx, ry - 22, rw, 22, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont(KRB, 10)
        c.drawString(rx + 8, ry - 16, yr)
        c.setFillColor(BLACK)
        c.setFont(KR if yr != '2025' else KRB, 10)
        c.drawString(rx + 70, ry - 16, amt)
        c.setFillColor(GREEN_OK if tag == '흑자전환' else GRAY)
        c.setFont(KR, 9)
        c.drawRightString(rx + rw - 8, ry - 16, tag)
        ry -= 24

    # 12월 매출 계획 박스
    pl_top = ry - 14
    c.setFillColor(NAVY)
    c.rect(rx, pl_top - 130, rw, 130, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(rx, pl_top - 4, rw, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(rx + 12, pl_top - 22, '[ 2026년 12월 매출 계획 ]')

    c.setFillColor(GOLD)
    c.rect(rx + 12, pl_top - 76, rw - 24, 46, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KR, 9)
    c.drawString(rx + 20, pl_top - 44, '보수 시나리오 (메인)')
    c.setFont(KRB, 20)
    c.drawString(rx + 20, pl_top - 68, '15억 원')

    c.setStrokeColor(GOLD_LT)
    c.rect(rx + 12, pl_top - 122, rw - 24, 36, stroke=1, fill=0)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 9)
    c.drawString(rx + 20, pl_top - 96, '공격 시나리오')
    c.setFillColor(WHITE)
    c.setFont(KRB, 16)
    c.drawString(rx + 20, pl_top - 116, '20억 원')

    c.showPage()

# =====================================================
# P8 ★ 매출 향상 계획 (2) — 매출 달성 목표 (직관적 계산식)
# =====================================================
def page_sales_plan_2(c):
    c.setFillColor(GOLD)
    c.rect(0, SH - HEADER_H, SW, HEADER_H, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.rect(0, SH - HEADER_H, 6, HEADER_H, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KRB, 11)
    c.drawString(MX, SH - HEADER_H + 15, '★  ' + COMPANY_KO + ' · 정책자금 사업계획서  ·  매출 향상 계획 (2)')
    c.setFont(KR, 9)
    c.drawRightString(SW - MX, SH - HEADER_H + 15, BRAND_LINE)
    c.setFont(KR, 8)
    c.drawRightString(SW - MX, SH - HEADER_H + 4, 'P. 08 / 11')

    draw_footer_bar(c, 8)

    y = SH - HEADER_H - 38
    c.setFillColor(GOLD)
    c.rect(MX, y, 36, 36, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.rect(MX, y, 36, 4, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KRB, 16)
    c.drawCentredString(MX + 18, y + 11, '07')
    c.setFillColor(NAVY)
    c.setFont(KRB, 22)
    c.drawString(MX + 50, y + 14, '매출 향상 계획 (2)  ·  매출 달성 목표')
    c.setFillColor(GOLD)
    c.setFont(KR, 10)
    c.drawString(MX + 50, y - 2, 'Revenue Plan (2) — Achievement Targets (직관적 계산식)')
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(MX, y - 12, SW - MX, y - 12)
    y0 = y - 22

    cards = [
        {
            'no': '1', 'title': '유럽 B2B 직수출',
            'subtitle': '(기존 사업 안정)',
            'tag': 'EXISTING',
            'calc1': '거래당 평균 1,000만 원',
            'calc2': '× 월 7건',
            'calc3': '= 월 7,000만 원',
            'calc4': '× 12개월',
            'big':   '연 8.4억 원',
            'note':  '거래선 수·거래액 [회사 기재] 보정',
        },
        {
            'no': '2', 'title': 'K-beauty4U B2B 편집샵',
            'subtitle': '(신규 — 3Q 가동)',
            'tag': 'NEW',
            'calc1': '가입 바이어 100개사',
            'calc2': '× 월 평균 50만 원',
            'calc3': '= 월 5,000만 원',
            'calc4': '× 6개월 (3Q 후)',
            'big':   '반기 3억 원',
            'note':  '가동 후 6~9개월 시차 반영',
        },
        {
            'no': '3', 'title': '자체 브랜드 화장품',
            'subtitle': '(신규 — 4Q 출시)',
            'tag': 'NEW',
            'calc1': '거래선당 5,000만 원',
            'calc2': '× 4개 거래선',
            'calc3': '× Q4 진입',
            'calc4': '',
            'big':   '분기 2억 원',
            'note':  '본격 양산은 후속 자금 확보 후',
        },
    ]
    cw = (SW - MX * 2 - 24) / 3
    ch = 270
    cy = y0 - 6
    for i, ck in enumerate(cards):
        cx = MX + i * (cw + 12)
        c.setFillColor(BG_GRAY)
        c.rect(cx, cy - ch, cw, ch, stroke=0, fill=1)
        # 상단 네이비 헤더
        c.setFillColor(NAVY)
        c.rect(cx, cy - 70, cw, 70, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(cx, cy - 4, cw, 4, stroke=0, fill=1)
        # 번호
        c.setFillColor(GOLD)
        c.setFont(KRB, 32)
        c.drawString(cx + 14, cy - 48, ck['no'])
        # 태그
        c.setFillColor(GOLD_LT)
        c.setFont(KR, 8)
        c.drawString(cx + 50, cy - 22, ck['tag'])
        # 타이틀
        c.setFillColor(WHITE)
        c.setFont(KRB, 13)
        c.drawString(cx + 50, cy - 40, ck['title'])
        c.setFillColor(GOLD_LT)
        c.setFont(KR, 10)
        c.drawString(cx + 50, cy - 56, ck['subtitle'])

        # 계산식 (라인별)
        c.setFillColor(GRAY)
        c.setFont(KR, 9)
        c.drawString(cx + 14, cy - 90, '계산식')
        c.setFillColor(BLACK)
        c.setFont(KR, 11)
        ly_calc = cy - 110
        for line in [ck['calc1'], ck['calc2'], ck['calc3'], ck['calc4']]:
            if line:
                c.drawString(cx + 18, ly_calc, line)
                ly_calc -= 16

        # 큰 숫자 박스
        c.setFillColor(GOLD)
        c.rect(cx + 14, cy - 220, cw - 28, 44, stroke=0, fill=1)
        c.setFillColor(NAVY_DK)
        c.setFont(KRB, 20)
        c.drawCentredString(cx + cw / 2, cy - 206, ck['big'])

        # 노트
        c.setFillColor(GRAY)
        c.setFont(KR, 8)
        c.drawString(cx + 14, cy - 240, '※ ' + ck['note'])

    # 합계 박스
    sum_y = cy - ch - 14
    c.setFillColor(NAVY)
    c.rect(MX, sum_y - 80, SW - MX * 2, 80, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(MX, sum_y - 4, SW - MX * 2, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(MX + 16, sum_y - 22, '[ 2026년 매출 합계 ]')

    c.setFillColor(GOLD)
    c.rect(MX + 16, sum_y - 70, 360, 36, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KR, 9)
    c.drawString(MX + 26, sum_y - 46, '보수 시나리오 (메인)')
    c.setFont(KRB, 18)
    c.drawString(MX + 26, sum_y - 64, '약 13~15억 원')

    c.setFillColor(WHITE)
    c.setFont(KR, 9)
    c.drawString(MX + 400, sum_y - 46, '공격 시나리오')
    c.setFillColor(GOLD_LT)
    c.setFont(KRB, 18)
    c.drawString(MX + 400, sum_y - 64, '약 20억 원')

    c.showPage()

# =====================================================
# P9 — 매출 향상 근거 + 영업 인프라
# =====================================================
def page_evidence(c):
    draw_header_bar(c, 9)
    draw_footer_bar(c, 9)
    y0 = section_title(c, '08', '매출 향상 근거 · 영업 인프라', 'Sales Evidence & Infrastructure')

    lx = MX
    lw = (SW - MX * 2 - 16) / 2
    ly = y0 - 6
    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(lx, ly, '[ 매출 향상 근거 ]')
    c.setStrokeColor(GOLD)
    c.line(lx, ly - 6, lx + 130, ly - 6)

    evidences = [
        ('K-뷰티 EMEA 시장 규모',
         '글로벌 확장세 (구체 수치 — 회사 보정)'),
        ('2025 매출 8.6억 = 월평균 7,200만 원',
         '안정 운영 입증 — 흑자전환 달성'),
        ('2026 1Q 2억 = 월평균 6,700만 원',
         '안정 정착 단계 — 분기 진행 중'),
        ('유럽 신뢰 거래선 보유',
         '프랜차이즈·대형마트 다거래선'),
    ]
    ey = ly - 22
    for t, d in evidences:
        c.setFillColor(BG_GRAY)
        c.rect(lx, ey - 50, lw, 50, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(lx, ey - 50, 4, 50, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont(KRB, 11)
        c.drawString(lx + 14, ey - 22, t)
        c.setFillColor(GRAY)
        c.setFont(KR, 9)
        c.drawString(lx + 14, ey - 38, d)
        ey -= 56

    rx = lx + lw + 16
    rw = lw
    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(rx, ly, '[ 영업 인프라 ]')
    c.setStrokeColor(GOLD)
    c.line(rx, ly - 6, rx + 130, ly - 6)

    infras = [
        ('Brand Curation', '차별화 사업 모델'),
        ('다국어 4개 국어', '한·영·불·아랍어 시장 진입 역량'),
        ('프랑스어 통역 가이드', '대표 보유 자격'),
        ('무차입 청정 신용', '개인 1,800만 외 부채 없음·무체납'),
        ('6개월 내 1~2명 채용', '청년·여성 우대 가산'),
    ]
    iy = ly - 22
    for t, d in infras:
        c.setFillColor(BG_NAVY_LT)
        c.rect(rx, iy - 38, rw, 38, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.rect(rx, iy - 38, 4, 38, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont(KRB, 11)
        c.drawString(rx + 14, iy - 18, t)
        c.setFillColor(GRAY)
        c.setFont(KR, 9)
        c.drawString(rx + 14, iy - 30, d)
        iy -= 44

    c.showPage()

# =====================================================
# P10 — 자금 소요 계획
# =====================================================
def page_fund_plan(c):
    draw_header_bar(c, 10)
    draw_footer_bar(c, 10)
    y0 = section_title(c, '09', '자금 소요 계획', 'Fund Usage Plan — 1.5억')

    # 트랙 분리 안내 박스
    tr_top = y0 - 6
    c.setFillColor(NAVY)
    c.rect(MX, tr_top - 50, SW - MX * 2, 50, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(MX, tr_top - 4, SW - MX * 2, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(MX + 16, tr_top - 22, 'TRACK SEPARATION')
    c.setFillColor(WHITE)
    c.setFont(KRB, 14)
    c.drawString(MX + 16, tr_top - 42, '운영자금 1억 + 시설·창업자금 0.5억  ·  트랙 분리 신청 권고')

    # 3개 자금 사용처 카드
    cards = [
        {
            'no': '①', 'title': 'K-connect hub 자사 웹사이트',
            'sub':  '한·영·불·아랍어 4개 언어 디자인·개발',
            'amt':  '4,500만 원',
            'track':'운영자금',
            'col':  NAVY,
        },
        {
            'no': '②', 'title': 'K-beauty4U EMEA B2B 편집샵',
            'sub':  '플랫폼 개발·콘텐츠·마케팅',
            'amt':  '6,000만 원',
            'track':'운영자금 + 일부 시설',
            'col':  NAVY_LT,
        },
        {
            'no': '③', 'title': '자체 브랜드 화장품 개발·생산',
            'sub':  '시제품·인증·초도 생산 (별도 트랙)',
            'amt':  '4,500만 원',
            'track':'시설·창업자금 (별도 트랙 권고)',
            'col':  GOLD,
        },
    ]
    cw = (SW - MX * 2 - 24) / 3
    ch = 200
    cy = tr_top - 60
    for i, ck in enumerate(cards):
        cx = MX + i * (cw + 12)
        c.setFillColor(BG_GRAY)
        c.rect(cx, cy - ch, cw, ch, stroke=0, fill=1)
        c.setFillColor(ck['col'])
        c.rect(cx, cy - 56, cw, 56, stroke=0, fill=1)
        # 번호
        c.setFillColor(WHITE if ck['col'] != GOLD else NAVY_DK)
        c.setFont(KRB, 26)
        c.drawString(cx + 14, cy - 42, ck['no'])
        # 트랙 라벨
        c.setFillColor(GOLD_LT if ck['col'] != GOLD else NAVY)
        c.setFont(KR, 9)
        c.drawString(cx + 50, cy - 24, ck['track'])
        # 타이틀
        c.setFillColor(WHITE if ck['col'] != GOLD else NAVY_DK)
        c.setFont(KRB, 12)
        for k, ln in enumerate(wrap_text(ck['title'], 18)):
            c.drawString(cx + 50, cy - 40 - k * 14, ln)
        # 본문
        c.setFillColor(BLACK)
        c.setFont(KR, 10)
        for k, ln in enumerate(wrap_text(ck['sub'], 22)):
            c.drawString(cx + 14, cy - 80 - k * 14, ln)
        # 금액
        c.setFillColor(NAVY)
        c.rect(cx + 14, cy - 168, cw - 28, 50, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(cx + 14, cy - 122, cw - 28, 4, stroke=0, fill=1)
        c.setFillColor(GOLD_LT)
        c.setFont(KR, 9)
        c.drawString(cx + 22, cy - 138, '소요 금액')
        c.setFillColor(WHITE)
        c.setFont(KRB, 18)
        c.drawString(cx + 22, cy - 160, ck['amt'])

    # 총 합계 박스
    sum_y = cy - ch - 12
    c.setFillColor(GOLD)
    c.rect(MX, sum_y - 50, SW - MX * 2, 50, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.rect(MX, sum_y - 4, SW - MX * 2, 4, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KR, 10)
    c.drawString(MX + 16, sum_y - 22, 'TOTAL FUND REQUIRED')
    c.setFont(KRB, 22)
    c.drawString(MX + 16, sum_y - 44, '총 사업비  약 1억 5천만 원')
    c.setFillColor(NAVY_DK)
    c.setFont(KR, 9)
    c.drawRightString(SW - MX - 16, sum_y - 22, '※ 분배 비율 예시 — 회사 측 정확 사업계획에 따라 조정 [회사 기재]')

    c.showPage()

# =====================================================
# P11 — 맺음말 (THANK YOU)
# =====================================================
def page_closing(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, SW, SH, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, 0, 12, SH, stroke=0, fill=1)
    c.setFillColor(GOLD_LT)
    c.rect(SW - 220, SH - 80, 180, 4, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(SW - 220, SH - 95, 60, 4, stroke=0, fill=1)

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 11)
    c.drawString(MX + 16, SH - 70, BRAND_LINE)

    c.setFillColor(WHITE)
    c.setFont(KRB, 92)
    c.drawString(MX + 16, SH - 200, 'THANK YOU.')

    c.setFillColor(GOLD)
    c.rect(MX + 16, SH - 220, 320, 4, stroke=0, fill=1)

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 13)
    c.drawString(MX + 16, SH - 250, COMPANY_EN)
    c.setFillColor(WHITE)
    c.setFont(KRB, 22)
    c.drawString(MX + 16, SH - 282, COMPANY_KO)

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 11)
    c.drawString(MX + 16, SH - 308, 'T. [회사 기재]    E. [회사 기재]')

    # 5대 강점 배지
    badges = ['청년·여성 창업', '매출 7.5배 급성장', '무차입 청정 신용',
              'Brand Curation 차별화', '디지털 인프라 사용처']
    by = 200
    bx_cur = MX + 16
    for b in badges:
        w = 14 + len(b) * 7.2
        c.setFillColor(GOLD)
        c.setStrokeColor(GOLD)
        c.roundRect(bx_cur, by - 22, w, 24, 12, stroke=1, fill=1)
        c.setFillColor(NAVY_DK)
        c.setFont(KRB, 10)
        c.drawString(bx_cur + 10, by - 16, b)
        bx_cur += w + 8
        if bx_cur + 80 > SW - MX:
            bx_cur = MX + 16
            by -= 30

    # 면책 박스
    dis_y = 90
    c.setFillColor(NAVY_DK)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.rect(MX + 16, dis_y - 60, SW - MX * 2 - 16, 60, stroke=1, fill=1)
    c.setFillColor(GOLD_LT)
    c.setFont(KRB, 9)
    c.drawString(MX + 28, dis_y - 18, '※ 면책 문구')
    c.setFillColor(WHITE)
    c.setFont(KR, 9)
    c.drawString(MX + 28, dis_y - 34,
                 '본 사업계획서는 회사 측 보정 자료(NICE 등급·재무제표·대표 이력) 반영 후 최종본으로 완성됩니다.')
    c.drawString(MX + 28, dis_y - 48,
                 '매출 전망은 회사 자체 추정이며 보증재단 심사 결과를 보장하지 않습니다.')

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(MX + 16, 24, SW - MX, 24)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 8)
    c.drawString(MX + 16, 10, BRAND_LINE)
    c.drawRightString(SW - MX, 10, f'작성일 {DATE_STR}  ·  P. 11 / 11')

    c.showPage()

# =====================================================
# 빌드
# =====================================================
def build_pdf():
    out_dir = Path('/home/user/-/뉴허브인터내셔널')
    out_path = out_dir / '(주)뉴허브인터내셔널_정책자금사업계획서_20260508.pdf'
    c = pdfcanvas.Canvas(str(out_path), pagesize=(SW, SH))
    c.setTitle('(주)뉴허브인터내셔널 정책자금 사업계획서')
    c.setAuthor('히어컴퍼니 (HearCompany) Corporate Consulting')
    c.setSubject('신용보증재단 보증신청용 사업계획서 (1.5억)')

    page_cover(c)
    page_business_intro(c)
    page_strengths(c)
    page_achievements(c)
    page_ceo(c)
    page_market(c)
    page_sales_plan_1(c)
    page_sales_plan_2(c)
    page_evidence(c)
    page_fund_plan(c)
    page_closing(c)

    c.save()
    return out_path

if __name__ == '__main__':
    p = build_pdf()
    sz = p.stat().st_size
    print(f'OK  {p}  ({sz:,} bytes)')
