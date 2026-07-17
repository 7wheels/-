# -*- coding: utf-8 -*-
"""
태안바지락해장국 사업계획서 PDF 빌더 (정책자금 1억 · 기관명 미기재)
표준 11페이지 · 16:9 슬라이드 · 웜톤(딥레드+골드) 요식업 컨셉
작성: 히어컴퍼니 (HearCompany) Corporate Consulting
"""
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib import colors
from pathlib import Path

pdfmetrics.registerFont(UnicodeCIDFont('HYGothic-Medium'))
pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))
KR  = 'HYGothic-Medium'
KRB = 'HYSMyeongJo-Medium'

SW, SH = 960, 540
MX = 36
HEADER_H = 40
FOOTER_H = 22

# ── 웜톤 팔레트 (해장국·바지락 컨셉) ──
RED       = colors.HexColor('#8B2E1F')  # deep red-brown (base)
RED_DK    = colors.HexColor('#5E1C11')  # very dark red
RED_LT    = colors.HexColor('#B4472F')  # medium red
GOLD      = colors.HexColor('#F39C12')
GOLD_LT   = colors.HexColor('#FFB343')
GOLD_PALE = colors.HexColor('#FFE6B8')
WHITE     = colors.white
BLACK     = colors.HexColor('#1A1A1A')
GRAY      = colors.HexColor('#7A7A7A')
GRAY_LT   = colors.HexColor('#DED4CE')
BG_GRAY   = colors.HexColor('#FAF6F3')
BG_RED_LT = colors.HexColor('#F3E7E3')
GREEN_OK  = colors.HexColor('#2E8B57')

COMPANY   = '태안바지락해장국'
DATE_STR  = '2026.05.14'
BRAND     = '히어컴퍼니 (HearCompany) Corporate Consulting'


def header_bar(c, page_no, total=11):
    c.setFillColor(RED)
    c.rect(0, SH - HEADER_H, SW, HEADER_H, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, SH - HEADER_H, 6, HEADER_H, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont(KR, 10)
    c.drawString(MX, SH - HEADER_H + 15, COMPANY + ' · 사업계획서')
    c.setFont(KR, 9)
    c.setFillColor(GOLD_LT)
    c.drawRightString(SW - MX, SH - HEADER_H + 15, BRAND)
    c.setFillColor(WHITE)
    c.setFont(KR, 8)
    c.drawRightString(SW - MX, SH - HEADER_H + 4, f'P. {page_no:02d} / {total:02d}')


def footer_bar(c):
    c.setFillColor(RED)
    c.rect(0, 0, SW, FOOTER_H, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont(KR, 8)
    c.drawString(MX, 7, f'작성일 {DATE_STR} · 정책자금 보증/융자 신청용 (1억)')
    c.setFillColor(GOLD_LT)
    c.drawRightString(SW - MX, 7, BRAND)


def section_title(c, num, title, sub=''):
    y = SH - HEADER_H - 38
    c.setFillColor(RED)
    c.rect(MX, y, 36, 36, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(MX, y, 36, 4, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont(KRB, 16)
    c.drawCentredString(MX + 18, y + 11, num)
    c.setFillColor(RED)
    c.setFont(KRB, 22)
    c.drawString(MX + 50, y + 14, title)
    if sub:
        c.setFillColor(GRAY)
        c.setFont(KR, 10)
        c.drawString(MX + 50, y - 2, sub)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(MX, y - 12, SW - MX, y - 12)
    return y - 22


def wrap(text, n):
    out, line = [], ''
    for ch in text:
        if ch == '\n':
            out.append(line); line = ''; continue
        line += ch
        if len(line) >= n:
            out.append(line); line = ''
    if line:
        out.append(line)
    return out


# =====================================================
# P1 표지
# =====================================================
def p1(c):
    c.setFillColor(RED)
    c.rect(0, 0, SW, SH, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, 0, 12, SH, stroke=0, fill=1)
    c.setFillColor(GOLD_LT)
    c.rect(SW - 220, SH - 80, 180, 4, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(SW - 220, SH - 95, 60, 4, stroke=0, fill=1)

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 11)
    c.drawString(MX + 16, SH - 70, BRAND)
    c.setFillColor(WHITE)
    c.setFont(KR, 10)
    c.drawString(MX + 16, SH - 88, 'BUSINESS PLAN  ·  POLICY FUND (1억)')

    c.setFillColor(WHITE)
    c.setFont(KRB, 46)
    c.drawString(MX + 16, SH - 190, '태안바지락해장국')
    c.setFont(KRB, 46)
    c.drawString(MX + 16, SH - 250, '사업계획서')

    c.setFillColor(GOLD)
    c.rect(MX + 16, SH - 285, 360, 4, stroke=0, fill=1)

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 13)
    c.drawString(MX + 16, SH - 315, '태안 특산물 바지락 해장국 전문점')
    c.setFillColor(WHITE)
    c.setFont(KR, 12)
    c.drawString(MX + 16, SH - 338, '메뉴개발 및 2호 직영점 확장 계획')

    c.setFillColor(GOLD)
    c.rect(MX + 16, SH - 390, 300, 36, stroke=0, fill=1)
    c.setFillColor(RED_DK)
    c.setFont(KRB, 16)
    c.drawString(MX + 28, SH - 380, '정책자금 보증/융자 신청  1억 원')

    c.setFillColor(WHITE)
    c.setFont(KR, 10)
    iy = 84
    c.drawRightString(SW - MX, iy + 36, '매  장  |  충남 태안군 태안읍 (본점 1호점)')
    c.drawRightString(SW - MX, iy + 22, '사업자등록 · 연락처  |  [회사 기재]')
    c.setFillColor(GOLD_LT)
    c.drawRightString(SW - MX, iy + 8, f'작성일  |  {DATE_STR}')

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(MX + 16, 40, SW - MX, 40)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 8)
    c.drawString(MX + 16, 26, 'Confidential — For Policy Fund Application Only')
    c.drawRightString(SW - MX, 26, 'HearCompany Corporate Consulting')
    c.showPage()


# =====================================================
# P2 사업 소개
# =====================================================
def p2(c):
    header_bar(c, 2); footer_bar(c)
    y0 = section_title(c, '01', '회사 주요 사업 소개', 'Business Overview')

    bx, by, bw, bh = MX, 90, 340, y0 - 110
    c.setFillColor(RED)
    c.rect(bx, by, bw, bh, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(bx, by + bh - 4, bw, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 11)
    c.drawString(bx + 20, by + bh - 32, 'CORE IDENTITY')
    c.setFillColor(WHITE)
    c.setFont(KRB, 20)
    c.drawString(bx + 20, by + bh - 62, '태안바지락해장국은')
    c.setFont(KRB, 15)
    c.drawString(bx + 20, by + bh - 88, '태안 특산물 바지락을 접목한')
    c.drawString(bx + 20, by + bh - 108, '해장국 전문점입니다.')

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    dy = by + bh - 140
    for ln in [
        '디자이너 출신 대표의 브랜딩 역량과',
        '지역 특산물 스토리를 결합하여,',
        '검증된 1호점 수익성(연 6.2억)을 기반으로',
        '메뉴개발(밀키트·신규메뉴)과',
        '2호 직영점 확장을 준비합니다.',
        '',
        '주력 메뉴: 태안바지락해장국 · 내장탕',
        '매장: 충남 태안군 태안읍 (1호점)',
    ]:
        c.drawString(bx + 20, dy, ln)
        dy -= 15

    rx = bx + bw + 24
    rw = SW - MX - rx
    cy = y0 - 8
    c.setFillColor(RED)
    c.setFont(KRB, 14)
    c.drawString(rx, cy, '4대 사업 축')
    c.setStrokeColor(GOLD)
    c.line(rx, cy - 6, rx + 120, cy - 6)

    axes = [
        ('①', '검증된 1호점 수익성', '2025년 연 6.2억 매출 검증'),
        ('②', '메뉴 개발', '밀키트·신규 메뉴 상품화'),
        ('③', '2호 직영점 확장', '태안 산단 80평·60석 · 2027 초'),
        ('④', '지역 특산물 상생', '태안 바지락 스토리 · 로컬푸드'),
    ]
    top = cy - 24
    for i, (n, t, d) in enumerate(axes):
        row = i // 2; col = i % 2
        cw = (rw - 12) / 2
        ax = rx + col * (cw + 12)
        ay = top - row * 92
        c.setFillColor(BG_GRAY)
        c.rect(ax, ay - 80, cw, 80, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(ax, ay - 4, 36, 4, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.setFont(KRB, 24)
        c.drawString(ax + 12, ay - 40, n)
        c.setFillColor(RED)
        c.setFont(KRB, 13)
        c.drawString(ax + 50, ay - 28, t)
        c.setFillColor(GRAY)
        c.setFont(KR, 9)
        for k, ln in enumerate(wrap(d, 18)):
            c.drawString(ax + 50, ay - 46 - k * 12, ln)
    c.showPage()


# =====================================================
# P3 강점 4대
# =====================================================
def p3(c):
    header_bar(c, 3); footer_bar(c)
    y0 = section_title(c, '02', '회사 장점 · 강점', 'Core Strengths')

    items = [
        ('①', '폭발적 매출 성장',
         '2024 6,300만 → 2025 6.2억 (9.8배)',
         '2026 상반기 이미 4.2억 (2025년 68%)'),
        ('②', '대표 브랜딩 역량',
         '디자이너 출신 + 요식업 컨설팅 경력',
         '매장 설계·브랜드·메뉴 기획 강점'),
        ('③', '지역 특산물 스토리',
         '태안 바지락 = 차별화·언론 소재',
         '지역 상생·로컬푸드 트렌드 부합'),
        ('④', '검증된 단일 매장 수익성',
         '1호점 연 6억+ → 2호점 확장 근거',
         'NICE 839점 · 요식업 자영업 양호 신용'),
    ]
    top = y0 - 6
    cw = (SW - MX * 2 - 16) / 2
    ch = 128
    for i, (n, t, l1, l2) in enumerate(items):
        row = i // 2; col = i % 2
        cx = MX + col * (cw + 16)
        cy = top - row * (ch + 12)
        c.setFillColor(BG_GRAY)
        c.setStrokeColor(GRAY_LT)
        c.setLineWidth(0.8)
        c.rect(cx, cy - ch, cw, ch, stroke=1, fill=1)
        c.setFillColor(GOLD)
        c.rect(cx, cy - ch, 6, ch, stroke=0, fill=1)
        c.setFillColor(RED)
        c.setFont(KRB, 34)
        c.drawString(cx + 22, cy - 50, n)
        c.setFillColor(RED)
        c.setFont(KRB, 15)
        c.drawString(cx + 78, cy - 38, t)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(cx + 78, cy - 46, cx + cw - 16, cy - 46)
        c.setFillColor(BLACK)
        c.setFont(KR, 10)
        c.drawString(cx + 78, cy - 66, l1)
        c.setFillColor(GRAY)
        c.drawString(cx + 78, cy - 84, l2)

    cu = top - 2 * (ch + 12) - 4
    c.setFillColor(RED)
    c.rect(MX, cu - 52, SW - MX * 2, 52, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(MX, cu - 4, SW - MX * 2, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(MX + 20, cu - 20, 'COMPETITIVE EDGE')
    c.setFillColor(WHITE)
    c.setFont(KRB, 13)
    c.drawString(MX + 20, cu - 40, '검증된 1호점 수익성(연 6.2억) + 디자이너 대표 브랜딩 + 태안 특산물 스토리 = 메뉴개발·2호점 확장 3중 성장 동력')
    c.showPage()


# =====================================================
# P4 매출 성장 차트
# =====================================================
def p4(c):
    header_bar(c, 4); footer_bar(c)
    y0 = section_title(c, '03', '주요 업적 · 성장', 'Track Record & Growth')

    cx0 = MX; cy0 = 110; cw = 470; chh = y0 - cy0 - 16
    c.setFillColor(BG_GRAY)
    c.rect(cx0, cy0, cw, chh, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(cx0, cy0 + chh - 4, cw, 4, stroke=0, fill=1)
    c.setFillColor(RED)
    c.setFont(KRB, 14)
    c.drawString(cx0 + 16, cy0 + chh - 28, '매출 추이 — 2024→2025 9.8배 급성장')
    c.setFillColor(GRAY)
    c.setFont(KR, 9)
    c.drawString(cx0 + 16, cy0 + chh - 44, '단위: 백만 원')

    bars = [
        ('2024',      63,  '3개월영업',   GRAY_LT),
        ('2025',      620, '월 2.5배',    GOLD),
        ('2026 상반기', 420, '68% 달성',   RED_LT),
        ('2026 목표',  900, '연간 목표',   GREEN_OK),
    ]
    maxv = 950
    px = cx0 + 54; py = cy0 + 40; ph = chh - 96; pw = cw - 84
    bw = 60; gap = (pw - bw * 4) / 3
    c.setStrokeColor(GRAY_LT); c.setLineWidth(0.4)
    for v in [200, 400, 600, 800]:
        gy = py + (v / maxv) * ph
        c.line(px - 4, gy, px + pw, gy)
        c.setFillColor(GRAY); c.setFont(KR, 8)
        c.drawRightString(px - 8, gy - 3, str(v))
    c.setStrokeColor(RED); c.setLineWidth(0.8)
    c.line(px, py, px + pw, py)
    for i, (lb, v, tag, col) in enumerate(bars):
        bx = px + i * (bw + gap)
        bh = (v / maxv) * ph
        c.setFillColor(col)
        c.rect(bx, py, bw, bh, stroke=0, fill=1)
        c.setFillColor(RED); c.setFont(KRB, 11)
        c.drawCentredString(bx + bw / 2, py + bh + 6, str(v))
        c.setFillColor(BLACK); c.setFont(KR, 10)
        c.drawCentredString(bx + bw / 2, py - 14, lb)
        c.setFillColor(GREEN_OK if tag in ('68% 달성', '연간 목표') else GRAY)
        c.setFont(KR, 8)
        c.drawCentredString(bx + bw / 2, py - 26, tag)

    rx = cx0 + cw + 16; rw = SW - MX - rx
    c.setFillColor(RED)
    c.rect(rx, y0 - 6 - 110, rw, 110, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(rx, y0 - 6 - 4, rw, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT); c.setFont(KR, 10)
    c.drawString(rx + 14, y0 - 28, 'KEY PERFORMANCE')
    c.setFillColor(WHITE); c.setFont(KRB, 30)
    c.drawString(rx + 14, y0 - 62, '월 2.5배')
    c.setFillColor(GOLD_LT); c.setFont(KR, 9)
    c.drawString(rx + 14, y0 - 79, '월평균 2,100만→5,167만 (실 성장)')
    c.drawString(rx + 14, y0 - 91, '2024.10.8 개업 · 3개월 부분영업')
    c.setFillColor(WHITE); c.setFont(KRB, 12)
    c.drawString(rx + 14, y0 - 108, '2026 상반기 이미 4.2억 (68%)')

    cl = y0 - 6 - 110 - 12
    c.setFillColor(BG_GRAY)
    c.rect(rx, cl - 180, rw, 180, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(rx, cl - 4, rw, 4, stroke=0, fill=1)
    c.setFillColor(RED); c.setFont(KRB, 13)
    c.drawString(rx + 14, cl - 22, '1호점 개요')
    c.setStrokeColor(GOLD); c.setLineWidth(0.6)
    c.line(rx + 14, cl - 28, rx + rw - 14, cl - 28)
    c.setFillColor(BLACK); c.setFont(KR, 10)
    for k, ln in enumerate([
        '· 위치: 충남 태안군 태안읍',
        '· 주력: 태안바지락해장국 · 내장탕',
        '· 디자이너 출신 대표 브랜딩',
        '· 2025년 연 6.2억 매출 검증',
    ]):
        c.drawString(rx + 14, cl - 48 - k * 18, ln)
    c.setFillColor(GOLD); c.setFont(KR, 9)
    c.drawString(rx + 14, cl - 128, '※ NICE 839점 · 2025 영업이익 4,200만(6.8%)')
    c.drawString(rx + 14, cl - 146, '※ 2024.10.8 개업 3개월 → 월평균 2.5배 실성장')
    c.showPage()


# =====================================================
# P5 대표자
# =====================================================
def p5(c):
    header_bar(c, 5); footer_bar(c)
    y0 = section_title(c, '04', '대표자 소개', 'CEO Profile')

    lx, ly, lw, lh = MX, 110, 280, y0 - 110 - 18
    c.setFillColor(RED)
    c.rect(lx, ly, lw, lh, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(lx, ly + lh - 4, lw, 4, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(lx + 24, ly + lh - 80, 60, 60, stroke=0, fill=1)
    c.setFillColor(RED_DK); c.setFont(KRB, 28)
    c.drawCentredString(lx + 54, ly + lh - 64, 'CEO')
    c.setFillColor(GOLD_LT); c.setFont(KR, 11)
    c.drawString(lx + 24, ly + lh - 110, COMPANY)
    c.setFillColor(WHITE); c.setFont(KRB, 22)
    c.drawString(lx + 24, ly + lh - 142, '김재만 대표')
    c.setFillColor(GOLD_LT); c.setFont(KR, 10)
    c.drawString(lx + 24, ly + lh - 158, 'Founder & CEO')
    c.drawString(lx + 24, ly + lh - 173, '생년월일 · 사업자등록 [회사 기재]')

    by = ly + 78
    c.setFillColor(GOLD_PALE)
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.roundRect(lx + 24, by, lw - 48, 28, 6, stroke=1, fill=1)
    c.setFillColor(RED); c.setFont(KRB, 11)
    c.drawCentredString(lx + lw / 2, by + 9, '디자이너 출신 · NICE 839점 · 브랜딩 전문')
    c.setFillColor(GOLD_LT); c.setFont(KR, 9)
    c.drawCentredString(lx + lw / 2, by - 16, '요식업 컨설팅 경력 · 태안 바지락 해장국 창업')

    rx = lx + lw + 18
    s1 = y0 - 6
    c.setFillColor(RED); c.setFont(KRB, 14)
    c.drawString(rx, s1, '주요 이력')
    c.setStrokeColor(GOLD); c.setLineWidth(1)
    c.line(rx, s1 - 6, rx + 100, s1 - 6)
    careers = [
        ('출신', '디자이너 출신 — 브랜딩·공간 설계 역량'),
        ('경력', '요식업 업체 컨설팅 다년 — 매장·메뉴 기획'),
        ('창업', '태안 특산물 바지락 접목 해장국 출시'),
        ('성과', '2025 연 6.2억·영업이익 4,200만 · 2026 상반기 4.2억'),
    ]
    cy = s1 - 22
    for yr, desc in careers:
        c.setFillColor(GOLD)
        c.rect(rx, cy - 18, 60, 22, stroke=0, fill=1)
        c.setFillColor(RED_DK); c.setFont(KRB, 11)
        c.drawCentredString(rx + 30, cy - 12, yr)
        c.setFillColor(BLACK); c.setFont(KR, 11)
        c.drawString(rx + 70, cy - 12, desc)
        cy -= 28

    s2 = cy - 6
    c.setFillColor(RED); c.setFont(KRB, 14)
    c.drawString(rx, s2, '신용 · 재무 요약')
    c.setStrokeColor(GOLD)
    c.line(rx, s2 - 6, rx + 130, s2 - 6)
    c.setFillColor(BLACK); c.setFont(KR, 11)
    c.drawString(rx, s2 - 26, '· NICE 839점 · 요식업 자영업 기준 양호 신용')
    c.drawString(rx, s2 - 44, '· 2025 매출 6.2억 · 영업이익 4,200만 (영업이익률 6.8%)')
    c.drawString(rx, s2 - 62, '· 상환재원 확보: 연 영업이익 4,200만 > 1억 5년분할 연상환 약 2천만 (DSCR 2배+)')
    c.showPage()


# =====================================================
# P6 시장 동향 + 매출 예상
# =====================================================
def p6(c):
    header_bar(c, 6); footer_bar(c)
    y0 = section_title(c, '05', '시장 동향 · 향후 매출 예상', 'Market Trend & Outlook')

    lx = MX; lw = 470; ly = y0 - 6
    c.setFillColor(RED); c.setFont(KRB, 14)
    c.drawString(lx, ly, '시장 동향')
    c.setStrokeColor(GOLD); c.line(lx, ly - 6, lx + 80, ly - 6)
    trends = [
        ('해장국·한식 외식 시장', '국물·해장 수요 꾸준', '지역 맛집 브랜드화 트렌드'),
        ('밀키트·HMR 시장 급성장', '가정간편식 확대', '메뉴개발(밀키트) 방향 정당화'),
        ('지역 특산물·로컬푸드', '로컬푸드 관심 증가', '태안 바지락 스토리 차별화'),
    ]
    ty = ly - 24
    for t, l1, l2 in trends:
        c.setFillColor(BG_GRAY)
        c.rect(lx, ty - 76, lw, 76, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(lx, ty - 4, 4, 76, stroke=0, fill=1)
        c.setFillColor(RED); c.setFont(KRB, 13)
        c.drawString(lx + 16, ty - 22, t)
        c.setFillColor(BLACK); c.setFont(KR, 10)
        c.drawString(lx + 16, ty - 42, '· ' + l1)
        c.drawString(lx + 16, ty - 60, '· ' + l2)
        ty -= 86

    rx = lx + lw + 16; rw = SW - MX - rx; rh = y0 - 6 - 110
    c.setFillColor(RED)
    c.rect(rx, 110, rw, rh, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(rx, 110 + rh - 4, rw, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT); c.setFont(KR, 10)
    c.drawString(rx + 16, 110 + rh - 26, 'REVENUE OUTLOOK')
    c.setFillColor(WHITE); c.setFont(KRB, 16)
    c.drawString(rx + 16, 110 + rh - 50, '향후 매출 예상')

    c.setFillColor(GOLD)
    c.rect(rx + 16, 110 + rh - 130, rw - 32, 60, stroke=0, fill=1)
    c.setFillColor(RED_DK); c.setFont(KR, 10)
    c.drawString(rx + 24, 110 + rh - 88, '2026 기본 시나리오')
    c.setFont(KRB, 26)
    c.drawString(rx + 24, 110 + rh - 118, '약 9억 원')

    c.setStrokeColor(GOLD_LT); c.setLineWidth(1)
    c.rect(rx + 16, 110 + rh - 200, rw - 32, 50, stroke=1, fill=0)
    c.setFillColor(GOLD_LT); c.setFont(KR, 10)
    c.drawString(rx + 24, 110 + rh - 158, '2027 공격 (2호점 반영)')
    c.setFillColor(WHITE); c.setFont(KRB, 22)
    c.drawString(rx + 24, 110 + rh - 188, '약 13억 원+')

    c.setFillColor(GOLD_PALE)
    c.rect(rx + 16, 110 + 14, rw - 32, 50, stroke=0, fill=1)
    c.setFillColor(RED_DK); c.setFont(KRB, 10)
    c.drawString(rx + 24, 110 + 48, '※ 성장 근거')
    c.setFillColor(RED); c.setFont(KR, 9)
    c.drawString(rx + 24, 110 + 32, '2026 상반기 4.2억 실증 + 밀키트 신규 매출원')
    c.drawString(rx + 24, 110 + 20, '+ 2호점(2027 초) 연 매출 기여')
    c.showPage()


# =====================================================
# P7 매출 향상 계획 (1) 매출 구조
# =====================================================
def p7(c):
    c.setFillColor(GOLD)
    c.rect(0, SH - HEADER_H, SW, HEADER_H, stroke=0, fill=1)
    c.setFillColor(RED)
    c.rect(0, SH - HEADER_H, 6, HEADER_H, stroke=0, fill=1)
    c.setFillColor(RED_DK); c.setFont(KRB, 11)
    c.drawString(MX, SH - HEADER_H + 15, '★  ' + COMPANY + ' · 사업계획서  ·  매출 향상 계획 (1)')
    c.setFont(KR, 9)
    c.drawRightString(SW - MX, SH - HEADER_H + 15, BRAND)
    c.setFont(KR, 8)
    c.drawRightString(SW - MX, SH - HEADER_H + 4, 'P. 07 / 11')
    footer_bar(c)

    y = SH - HEADER_H - 38
    c.setFillColor(GOLD)
    c.rect(MX, y, 36, 36, stroke=0, fill=1)
    c.setFillColor(RED)
    c.rect(MX, y, 36, 4, stroke=0, fill=1)
    c.setFillColor(RED_DK); c.setFont(KRB, 16)
    c.drawCentredString(MX + 18, y + 11, '06')
    c.setFillColor(RED); c.setFont(KRB, 22)
    c.drawString(MX + 50, y + 14, '매출 향상 계획 (1)  ·  매출 구조')
    c.setStrokeColor(GOLD); c.setLineWidth(1.2)
    c.line(MX, y - 12, SW - MX, y - 12)
    y0 = y - 22

    lx = MX; lw = 470; ly = y0 - 6
    c.setFillColor(RED); c.setFont(KRB, 14)
    c.drawString(lx, ly, '[ 매출 구조 ]  3대 매출 모델')
    c.setStrokeColor(GOLD); c.line(lx, ly - 6, lx + 200, ly - 6)
    models = [
        ('1', '1호점 본점 매출 (검증·연 6억+)',
         '객단가 × 일 방문객 × 영업일',
         '= 2025 실적 연 6.2억 검증'),
        ('2', '밀키트·신규 메뉴 (신규·메뉴개발)',
         '개당 단가 × 월 판매량',
         '= 메뉴개발 5,000만 투입 결과물'),
        ('3', '2호 직영점 (2027 초·연 기여)',
         '1호점 검증 모델 복제 · 80평 60석',
         '= 태안 산단 · 연 매출 기여'),
    ]
    my = ly - 22
    for n, t, calc, res in models:
        c.setFillColor(BG_GRAY)
        c.rect(lx, my - 70, lw, 70, stroke=0, fill=1)
        c.setFillColor(RED)
        c.rect(lx, my - 70, 36, 70, stroke=0, fill=1)
        c.setFillColor(GOLD); c.setFont(KRB, 22)
        c.drawCentredString(lx + 18, my - 42, n)
        c.setFillColor(RED); c.setFont(KRB, 12)
        c.drawString(lx + 50, my - 18, t)
        c.setFillColor(BLACK); c.setFont(KR, 10)
        c.drawString(lx + 50, my - 38, calc)
        c.setFillColor(GOLD); c.setFont(KRB, 12)
        c.drawString(lx + 50, my - 56, res)
        my -= 78

    rx = lx + lw + 16; rw = SW - MX - rx
    st = y0 - 6
    c.setFillColor(RED); c.setFont(KRB, 13)
    c.drawString(rx, st, '[ 매출 상황 ]')
    c.setStrokeColor(GOLD); c.line(rx, st - 6, rx + 100, st - 6)
    rows = [
        ('2024',      '63,000,000원',  '3개월영업'),
        ('2025',      '620,000,000원', '월 2.5배'),
        ('2026 상반기', '420,000,000원', '68% 달성'),
        ('2026 목표',  '900,000,000원', '연간 목표'),
    ]
    ry = st - 22
    for yr, amt, tag in rows:
        hl = yr in ('2025', '2026 상반기')
        c.setFillColor(GOLD_PALE if hl else BG_GRAY)
        c.rect(rx, ry - 22, rw, 22, stroke=0, fill=1)
        c.setFillColor(RED); c.setFont(KRB, 10)
        c.drawString(rx + 8, ry - 16, yr)
        c.setFillColor(BLACK); c.setFont(KRB if hl else KR, 9)
        c.drawString(rx + 74, ry - 16, amt)
        c.setFillColor(GREEN_OK if ('배' in tag or '달성' in tag) else GRAY)
        c.setFont(KR, 9)
        c.drawRightString(rx + rw - 8, ry - 16, tag)
        ry -= 24

    pl = ry - 14
    c.setFillColor(RED)
    c.rect(rx, pl - 110, rw, 110, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(rx, pl - 4, rw, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT); c.setFont(KR, 10)
    c.drawString(rx + 12, pl - 22, '[ 2026년 매출 계획 ]')
    c.setFillColor(GOLD)
    c.rect(rx + 12, pl - 66, rw - 24, 40, stroke=0, fill=1)
    c.setFillColor(RED_DK); c.setFont(KR, 9)
    c.drawString(rx + 20, pl - 40, '기본 시나리오')
    c.setFont(KRB, 18)
    c.drawString(rx + 20, pl - 60, '약 9억 원')
    c.setFillColor(GOLD_LT); c.setFont(KR, 9)
    c.drawString(rx + 12, pl - 84, '2호점 오픈(2027) 반영 시')
    c.setFillColor(WHITE); c.setFont(KRB, 14)
    c.drawString(rx + 12, pl - 102, '2027 약 13억 원+')
    c.showPage()


# =====================================================
# P8 매출 향상 계획 (2) 직관적 계산식
# =====================================================
def p8(c):
    c.setFillColor(GOLD)
    c.rect(0, SH - HEADER_H, SW, HEADER_H, stroke=0, fill=1)
    c.setFillColor(RED)
    c.rect(0, SH - HEADER_H, 6, HEADER_H, stroke=0, fill=1)
    c.setFillColor(RED_DK); c.setFont(KRB, 11)
    c.drawString(MX, SH - HEADER_H + 15, '★  ' + COMPANY + ' · 사업계획서  ·  매출 향상 계획 (2)')
    c.setFont(KR, 9)
    c.drawRightString(SW - MX, SH - HEADER_H + 15, BRAND)
    c.setFont(KR, 8)
    c.drawRightString(SW - MX, SH - HEADER_H + 4, 'P. 08 / 11')
    footer_bar(c)

    y = SH - HEADER_H - 38
    c.setFillColor(GOLD)
    c.rect(MX, y, 36, 36, stroke=0, fill=1)
    c.setFillColor(RED)
    c.rect(MX, y, 36, 4, stroke=0, fill=1)
    c.setFillColor(RED_DK); c.setFont(KRB, 16)
    c.drawCentredString(MX + 18, y + 11, '07')
    c.setFillColor(RED); c.setFont(KRB, 22)
    c.drawString(MX + 50, y + 14, '매출 향상 계획 (2)  ·  직관적 계산식')
    c.setStrokeColor(GOLD); c.setLineWidth(1.2)
    c.line(MX, y - 12, SW - MX, y - 12)
    y0 = y - 22

    cards = [
        {'no': '1', 'title': '1호점 본점', 'sub': '(기존 · 검증 실적)', 'tag': '검증 실적',
         'c': ['평균 객단가 1.18만 원', '× 일 방문 160명', '= 일 189만 원', '× 연 330 영업일'],
         'big': '연 6.2억 원', 'note': '2025 실적 6.2억 부합 · 좌석·회전율 [회사 기재]'},
        {'no': '2', 'title': '밀키트·신규 메뉴', 'sub': '(추정 · 미실현)', 'tag': '추정(미실현)',
         'c': ['밀키트 개당 1.2만 원', '× 월 판매 500개', '= 월 600만 원', '× 12개월'],
         'big': '연 7,200만 원', 'note': '메뉴개발 5,000만 결과물 · 채널·OEM [회사 기재]'},
        {'no': '3', 'title': '2호 직영점', 'sub': '(추정 · 2027 초 오픈)', 'tag': '추정(미실현)',
         'c': ['1호점 검증 모델 복제', '80평 · 60석 · 태안 산단', '오픈 첫해 3~4억', '안정화 후 6억'],
         'big': '첫해 3~4억', 'note': '투자 3억 별도 조달 · [회사 기재]'},
    ]
    cw = (SW - MX * 2 - 24) / 3
    ch = 268
    cy = y0 - 6
    for i, ck in enumerate(cards):
        cx = MX + i * (cw + 12)
        c.setFillColor(BG_GRAY)
        c.rect(cx, cy - ch, cw, ch, stroke=0, fill=1)
        c.setFillColor(RED)
        c.rect(cx, cy - 68, cw, 68, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(cx, cy - 4, cw, 4, stroke=0, fill=1)
        c.setFillColor(GOLD); c.setFont(KRB, 30)
        c.drawString(cx + 14, cy - 46, ck['no'])
        c.setFillColor(GOLD_LT); c.setFont(KR, 8)
        c.drawString(cx + 50, cy - 22, ck['tag'])
        c.setFillColor(WHITE); c.setFont(KRB, 14)
        c.drawString(cx + 50, cy - 40, ck['title'])
        c.setFillColor(GOLD_LT); c.setFont(KR, 9)
        c.drawString(cx + 50, cy - 56, ck['sub'])
        yy = cy - 92
        c.setFillColor(BLACK); c.setFont(KR, 10)
        for ln in ck['c']:
            c.drawString(cx + 16, yy, ln)
            yy -= 18
        c.setFillColor(RED)
        c.rect(cx + 14, cy - 214, cw - 28, 44, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(cx + 14, cy - 174, cw - 28, 4, stroke=0, fill=1)
        c.setFillColor(GOLD_LT); c.setFont(KR, 9)
        c.drawString(cx + 22, cy - 190, '예상 매출')
        c.setFillColor(WHITE); c.setFont(KRB, 17)
        c.drawString(cx + 22, cy - 210, ck['big'])
        c.setFillColor(GRAY); c.setFont(KR, 8)
        for k, ln in enumerate(wrap(ck['note'], 20)):
            c.drawString(cx + 16, cy - 232 - k * 12, ln)

    sy = cy - ch - 14
    c.setFillColor(RED)
    c.rect(MX, sy - 60, SW - MX * 2, 60, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(MX, sy - 4, SW - MX * 2, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT); c.setFont(KR, 10)
    c.drawString(MX + 16, sy - 20, '[ 합계 · 검증 실적 + 추정 병기 ]')
    c.setFillColor(GOLD)
    c.rect(MX + 16, sy - 52, 300, 26, stroke=0, fill=1)
    c.setFillColor(RED_DK); c.setFont(KRB, 13)
    c.drawString(MX + 24, sy - 44, '2026 기본  약 9억 원')
    c.setFillColor(WHITE); c.setFont(KR, 9)
    c.drawString(MX + 340, sy - 24, '2027 공격 (2호점 안정화 반영)')
    c.setFillColor(GOLD_LT); c.setFont(KRB, 14)
    c.drawString(MX + 340, sy - 42, '약 12~13억 원')
    c.setFillColor(WHITE); c.setFont(KR, 8)
    c.drawString(MX + 340, sy - 56, '※ 밀키트·2호점은 미실현 추정 · 실적 아님')
    c.showPage()


# =====================================================
# P9 매출 향상 근거 + 자금 필요성 2축
# =====================================================
def p9(c):
    header_bar(c, 9); footer_bar(c)
    y0 = section_title(c, '08', '매출 향상 근거 · 자금 필요성', 'Evidence & Fund Necessity')

    lx = MX; lw = (SW - MX * 2 - 16) / 2; ly = y0 - 6
    c.setFillColor(RED); c.setFont(KRB, 14)
    c.drawString(lx, ly, '[ 매출 향상 근거 ]')
    c.setStrokeColor(GOLD); c.line(lx, ly - 6, lx + 130, ly - 6)
    evs = [
        ('2026 상반기 4.2억 달성', '이미 2025년 68% 달성 · 성장 궤도 실증'),
        ('1호점 검증된 수익성', '연 6.2억 → 2호점 확장 타당성'),
        ('디자이너 대표 브랜딩', '태안 특산물 스토리 · 차별화'),
        ('NICE 839점', '요식업 자영업 기준 양호 신용'),
    ]
    ey = ly - 22
    for t, d in evs:
        c.setFillColor(BG_GRAY)
        c.rect(lx, ey - 50, lw, 50, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(lx, ey - 50, 4, 50, stroke=0, fill=1)
        c.setFillColor(RED); c.setFont(KRB, 11)
        c.drawString(lx + 14, ey - 22, t)
        c.setFillColor(GRAY); c.setFont(KR, 9)
        c.drawString(lx + 14, ey - 38, d)
        ey -= 56

    rx = lx + lw + 16; rw = lw
    c.setFillColor(RED); c.setFont(KRB, 14)
    c.drawString(rx, ly, '[ 자금 필요성 — 2축 ]')
    c.setStrokeColor(GOLD); c.line(rx, ly - 6, rx + 150, ly - 6)

    # 2축 강조 카드
    axis = [
        ('①', '메뉴 개발', RED,
         '밀키트·신규 메뉴로 매출 다각화',
         '2호점 상품 경쟁력 확보 (5,000만)'),
        ('②', '2호 직영점 확장', GOLD,
         '태안 산단 80평·60석 · 2027 초',
         '투자 3억 · 이번 자금은 준비 단계 조성'),
    ]
    ay = ly - 22
    for n, t, col, l1, l2 in axis:
        c.setFillColor(col)
        c.rect(rx, ay - 108, rw, 108, stroke=0, fill=1)
        c.setFillColor(GOLD if col == RED else RED)
        c.rect(rx, ay - 4, rw, 4, stroke=0, fill=1)
        c.setFillColor(WHITE if col == RED else RED_DK)
        c.setFont(KRB, 30)
        c.drawString(rx + 14, ay - 44, n)
        c.setFillColor(GOLD_LT if col == RED else RED_DK)
        c.setFont(KRB, 15)
        c.drawString(rx + 60, ay - 32, t)
        c.setFillColor(WHITE if col == RED else RED_DK)
        c.setFont(KR, 10)
        c.drawString(rx + 60, ay - 54, l1)
        c.drawString(rx + 60, ay - 72, l2)
        ay -= 116
    c.showPage()


# =====================================================
# P10 자금 소요 계획
# =====================================================
def p10(c):
    header_bar(c, 10); footer_bar(c)
    y0 = section_title(c, '09', '자금 소요 계획', 'Fund Usage Plan — 정책자금 1억')

    tr = y0 - 6
    c.setFillColor(RED)
    c.rect(MX, tr - 50, SW - MX * 2, 50, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(MX, tr - 4, SW - MX * 2, 4, stroke=0, fill=1)
    c.setFillColor(GOLD_LT); c.setFont(KR, 10)
    c.drawString(MX + 16, tr - 20, 'FUND USAGE (정책자금 1억 · 기관명 미기재)')
    c.setFillColor(WHITE); c.setFont(KRB, 14)
    c.drawString(MX + 16, tr - 40, '메뉴개발·연구 50% + 고용 30% + 운영·마케팅 20%  ·  2호점 확장 준비 단계 자금')

    cards = [
        {'no': '①', 'title': '메뉴개발·연구', 'amt': '5,000만 원 (50%)', 'col': RED,
         'sub': '밀키트·신규 메뉴 개발·상품화·시제품'},
        {'no': '②', 'title': '고용 (1명)', 'amt': '3,000만 원 (30%)', 'col': RED_LT,
         'sub': '조직 확대·다점포 운영 역량'},
        {'no': '③', 'title': '운영·마케팅', 'amt': '2,000만 원 (20%)', 'col': GOLD,
         'sub': '브랜드 확산·2호점 상권 사전 인지도'},
    ]
    n = len(cards)
    cw = (SW - MX * 2 - 12 * (n - 1)) / n
    ch = 200
    cy = tr - 60
    for i, ck in enumerate(cards):
        cx = MX + i * (cw + 12)
        c.setFillColor(BG_GRAY)
        c.rect(cx, cy - ch, cw, ch, stroke=0, fill=1)
        c.setFillColor(ck['col'])
        c.rect(cx, cy - 56, cw, 56, stroke=0, fill=1)
        c.setFillColor(WHITE if ck['col'] != GOLD else RED_DK)
        c.setFont(KRB, 26)
        c.drawString(cx + 14, cy - 42, ck['no'])
        c.setFillColor(WHITE if ck['col'] != GOLD else RED_DK)
        c.setFont(KRB, 14)
        c.drawString(cx + 54, cy - 38, ck['title'])
        c.setFillColor(BLACK); c.setFont(KR, 10)
        for k, ln in enumerate(wrap(ck['sub'], 22)):
            c.drawString(cx + 14, cy - 80 - k * 14, ln)
        c.setFillColor(RED)
        c.rect(cx + 14, cy - 168, cw - 28, 50, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(cx + 14, cy - 122, cw - 28, 4, stroke=0, fill=1)
        c.setFillColor(GOLD_LT); c.setFont(KR, 9)
        c.drawString(cx + 22, cy - 138, '소요 금액')
        c.setFillColor(WHITE); c.setFont(KRB, 16)
        c.drawString(cx + 22, cy - 160, ck['amt'])

    sy = cy - ch - 12
    c.setFillColor(GOLD)
    c.rect(MX, sy - 64, SW - MX * 2, 64, stroke=0, fill=1)
    c.setFillColor(RED)
    c.rect(MX, sy - 4, SW - MX * 2, 4, stroke=0, fill=1)
    c.setFillColor(RED_DK); c.setFont(KR, 10)
    c.drawString(MX + 16, sy - 20, 'TOTAL')
    c.setFont(KRB, 20)
    c.drawString(MX + 16, sy - 42, '총 정책자금 신청  1억 원')
    c.setFillColor(RED_DK); c.setFont(KR, 9)
    c.drawString(MX + 16, sy - 58, '※ 상환재원: 2025 영업이익 4,200만 > 1억 5년분할 연상환 약 2천만 (DSCR 2배+) · 2호점 잔여 2억 조달 [회사 기재]')
    c.drawRightString(SW - MX - 16, sy - 20, '※ 매출 6.2억 대비 16% · 보수적')
    c.showPage()


# =====================================================
# P11 맺음말
# =====================================================
def p11(c):
    c.setFillColor(RED)
    c.rect(0, 0, SW, SH, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, 0, 12, SH, stroke=0, fill=1)
    c.setFillColor(GOLD_LT)
    c.rect(SW - 220, SH - 80, 180, 4, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(SW - 220, SH - 95, 60, 4, stroke=0, fill=1)

    c.setFillColor(GOLD_LT); c.setFont(KR, 11)
    c.drawString(MX + 16, SH - 70, BRAND)
    c.setFillColor(WHITE); c.setFont(KRB, 88)
    c.drawString(MX + 16, SH - 195, 'THANK YOU.')
    c.setFillColor(GOLD)
    c.rect(MX + 16, SH - 215, 320, 4, stroke=0, fill=1)

    c.setFillColor(GOLD_LT); c.setFont(KR, 13)
    c.drawString(MX + 16, SH - 245, '태안 특산물 바지락 해장국 전문점')
    c.setFillColor(WHITE); c.setFont(KRB, 24)
    c.drawString(MX + 16, SH - 280, '태안바지락해장국')
    c.setFillColor(GOLD_LT); c.setFont(KR, 11)
    c.drawString(MX + 16, SH - 306, 'T. [회사 기재]   E. [회사 기재]   매장: 충남 태안군 태안읍')

    badges = ['매출 9.8배 급성장', '디자이너 출신 대표', '태안 특산물 스토리',
              '검증된 1호점 수익성', 'NICE 839점']
    by = 200; bx = MX + 16
    for b in badges:
        w = 14 + len(b) * 7.2
        c.setFillColor(GOLD)
        c.setStrokeColor(GOLD)
        c.roundRect(bx, by - 22, w, 24, 12, stroke=1, fill=1)
        c.setFillColor(RED_DK); c.setFont(KRB, 10)
        c.drawString(bx + 10, by - 16, b)
        bx += w + 8
        if bx + 80 > SW - MX:
            bx = MX + 16; by -= 30

    dy = 92
    c.setFillColor(RED_DK)
    c.setStrokeColor(GOLD); c.setLineWidth(0.6)
    c.rect(MX + 16, dy - 60, SW - MX * 2 - 16, 60, stroke=1, fill=1)
    c.setFillColor(GOLD_LT); c.setFont(KRB, 9)
    c.drawString(MX + 28, dy - 18, '※ 면책 문구')
    c.setFillColor(WHITE); c.setFont(KR, 9)
    c.drawString(MX + 28, dy - 34, '본 계획서는 초안이며 회사 확정 자료 반영 후 정책자금 심사 접수용 최종본으로 전환됩니다.')
    c.drawString(MX + 28, dy - 48, '매출 전망은 회사 자체 추정이며 심사 결과를 보장하지 않습니다.')

    c.setStrokeColor(GOLD); c.setLineWidth(0.6)
    c.line(MX + 16, 24, SW - MX, 24)
    c.setFillColor(GOLD_LT); c.setFont(KR, 8)
    c.drawString(MX + 16, 10, BRAND)
    c.drawRightString(SW - MX, 10, f'작성일 {DATE_STR}  ·  P. 11 / 11')
    c.showPage()


def build():
    out = Path('/home/user/-/태안바지락해장국') / '태안바지락해장국_사업계획서_20260514.pdf'
    c = pdfcanvas.Canvas(str(out), pagesize=(SW, SH))
    c.setTitle('태안바지락해장국 사업계획서')
    c.setAuthor('히어컴퍼니 (HearCompany) Corporate Consulting')
    c.setSubject('정책자금 보증/융자 신청용 사업계획서 (1억)')
    p1(c); p2(c); p3(c); p4(c); p5(c); p6(c); p7(c); p8(c); p9(c); p10(c); p11(c)
    c.save()
    size = out.stat().st_size
    print(f'OK  {out}  ({size:,} bytes)')


if __name__ == '__main__':
    build()
