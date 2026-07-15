# -*- coding: utf-8 -*-
"""
(주)아꽁씨엘 — 정책자금 사업계획서 PDF 빌더 (기술보증기금 1억 신청 · v2 옵션 A)
표준 11페이지 양식 / 16:9 슬라이드 / 딥그린+골드 (ESG·업사이클 컨셉)
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

# ── 컬러 팔레트 (딥그린 · ESG·업사이클 컨셉) ──────────
# 변수명은 뉴허브 base와 호환 유지, 값만 딥그린 계열로 교체
NAVY      = colors.HexColor('#1B4332')  # deep green (base)
NAVY_DK   = colors.HexColor('#081C15')  # very dark green
NAVY_LT   = colors.HexColor('#2D6A4F')  # medium green
GOLD      = colors.HexColor('#F39C12')  # gold (accent)
GOLD_LT   = colors.HexColor('#FFB343')  # light gold
GOLD_PALE = colors.HexColor('#FFE6B8')  # pale gold
WHITE     = colors.white
BLACK     = colors.HexColor('#1A1A1A')
GRAY      = colors.HexColor('#7A7A7A')
GRAY_LT   = colors.HexColor('#D8DDE5')
BG_GRAY   = colors.HexColor('#F4F6FA')
BG_NAVY_LT= colors.HexColor('#E4EFE9')  # pale green background
GREEN_OK  = colors.HexColor('#2E8B57')
RED_WARN  = colors.HexColor('#C0392B')

COMPANY_KO = '(주)아꽁씨엘'
COMPANY_EN = 'Accongsiel Co., Ltd.'
DATE_STR   = '2026.05.13'
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
    c.drawString(MX, 7, f'작성일 {DATE_STR} · 기술보증기금 보증신청용 (1억)')
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
    c.drawString(MX + 16, SH - 390, '명품 폐원단 업사이클 프리미엄 원단 제조·유통 · ESG 순환경제 원단 전문기업')

    # 신청 자금 박스
    c.setFillColor(GOLD)
    c.rect(MX + 16, SH - 440, 280, 36, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KRB, 16)
    c.drawString(MX + 28, SH - 430, '기술보증기금 보증 신청  1억 원')

    # 하단 정보 박스 (우측 정렬)
    c.setFillColor(WHITE)
    c.setFont(KR, 10)
    info_y = 80
    c.drawRightString(SW - MX, info_y + 50, '제출처  |  신용보증재단')
    c.drawRightString(SW - MX, info_y + 36, '연락처  |  T. [회사 기재]   E. [회사 기재]')
    c.drawRightString(SW - MX, info_y + 22, '사업자등록  |  758-88-02575')
    c.drawRightString(SW - MX, info_y + 8,  '주  소  |  서울시 강남구 도산대로58길 12, 신관4층')
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
    c.drawString(box_x + 20, box_y + box_h - 92, '명품 폐원단 업사이클')
    c.drawString(box_x + 20, box_y + box_h - 112, '프리미엄 원단 제조·유통')
    c.drawString(box_x + 20, box_y + box_h - 132, 'ESG 순환경제 전문기업입니다.')

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    desc_y = box_y + box_h - 175
    desc_lines = [
        '특허 2건 출원(재생 분류·재조합 +',
        '업사이클 복합시트) 기반의 자체 재생',
        '공정과, 대표 이력에서 파생된',
        '유럽 유명 원단 독점 유통 채널로',
        '국내외 지속가능 패션 시장을',
        '공략합니다.',
        '',
        '기업부설연구소 + 벤처(혁신성장)',
        '3중 우대 요소를 확보하고 있습니다.',
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
        ('①', '명품 폐원단 재생 원단',    '등급별 재생·재조합 제조 (특허 1)'),
        ('②', '업사이클 복합시트',       '재생 TPU + 폐원단 스트립 (특허 2)'),
        ('③', '유럽 원단 독점 유통',     '프·이·영 프리미엄 원단 국내 공급'),
        ('④', '지속가능 패션 브랜드 협력','K-패션 지속가능 B2B 공급'),
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
    badges = ['유럽 원단 파트너 [기재]', '국내 지속가능 패션 브랜드 [기재]', '명품 브랜드 협력사 [기재]']
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
        ('①', '특허 2건 출원 — 원천기술 확보',
         '명품 폐원단 등급별 재생·재조합 제조방법 (특허 1)',
         '재생 TPU + 폐원단 스트립 업사이클 복합시트 (특허 2)'),
        ('②', '기업부설연구소 + 벤처(혁신성장)',
         'KOITA 인정 기업부설연구소 · 벤처확인기관 평가 통과',
         '기보 기술평가등급(T) 상향 근거 · 우대 3중 충족'),
        ('③', '유럽 원단 파트너 협의 진행',
         'Central Saint Martins 동기 네트워크 기반',
         '프·이·영 파트너 3개사와 국내 유통 협의 (2026 상반기 MOU 목표)'),
        ('④', 'ESG · 순환경제 스토리',
         '명품 브랜드 순환경제 정책 부합 · 지속가능 패션 트렌드',
         '지속가능 소재 프리미엄 단가 확보 가능'),
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
    c.drawString(MX + 20, cu_y - 42, '특허 2건 + 기업부설연구소 + 벤처(혁신성장) — 기보 우대 3중 충족 · 기술평가 T등급 상향 근거')

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
    c.drawString(chart_x + 16, chart_y + chart_h - 28, '매출 추이 — 2024→2025 약 4.7배 · 2026 상반기 진척률 [회사 기재]')
    c.setFillColor(GRAY)
    c.setFont(KR, 9)
    c.drawString(chart_x + 16, chart_y + chart_h - 44, '단위: 백만 원')

    bars = [
        ('2024',        15,  '초기',       GRAY_LT),
        ('2025',        70,  '성장',       GOLD),
        ('2026 목표',   200, '기본 시나리오', NAVY_LT),
        ('2026 공격',   250, '공격 시나리오', GREEN_OK),
    ]
    max_val = 260
    plot_x = chart_x + 50
    plot_y = chart_y + 36
    plot_h = chart_h - 90
    plot_w = chart_w - 80
    bar_w = 60
    gap = (plot_w - bar_w * 4) / 3

    # Y축 그리드
    c.setStrokeColor(GRAY_LT)
    c.setLineWidth(0.4)
    for v in [50, 100, 150, 200, 250]:
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
    c.drawString(rx + 14, y0 - 64, '16.7배')
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 11)
    c.drawString(rx + 14, y0 - 82, '2024 → 2026 예상 매출 급성장')
    c.setFillColor(WHITE)
    c.setFont(KRB, 14)
    c.drawString(rx + 14, y0 - 104, '특허 2건 출원 · 벤처(혁신성장)')

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
    c.drawString(rx + 14, cl_y - 60, '· 유럽 원단 파트너 [프·이·영]')
    c.drawString(rx + 14, cl_y - 76, '· 국내 지속가능 패션 브랜드')
    c.setFillColor(NAVY_LT)
    c.setFont(KR, 9)
    c.drawString(rx + 14, cl_y - 102, 'INSTITUTIONAL')
    c.setFillColor(BLACK)
    c.setFont(KR, 10)
    c.drawString(rx + 14, cl_y - 118, '· 기업부설연구소 (KOITA) · 벤처(혁신성장)')
    c.drawString(rx + 14, cl_y - 134, '· 임직원 2명 (대표+연구원) · 직조설비 보유')
    c.setFillColor(GOLD)
    c.setFont(KR, 9)
    c.drawString(rx + 14, cl_y - 160, '※ 특허 2건 · NICE 880점 · 차입금 0원')

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
    c.drawString(lx + 24, ly + lh - 142, '여정민 대표')
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(lx + 24, ly + lh - 158, '여 · 1984년생 · Founder & CEO')
    c.drawString(lx + 24, ly + lh - 173, '사업자등록 758-88-02575')

    # 강점 배지
    badge_y = ly + 80
    c.setFillColor(GOLD_PALE)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.roundRect(lx + 24, badge_y, lw - 48, 28, 6, stroke=1, fill=1)
    c.setFillColor(NAVY)
    c.setFont(KRB, 12)
    c.drawCentredString(lx + lw / 2, badge_y + 9, '여성 창업 · NICE 880점 · 세인트마틴 · 루이비통 우승')

    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawCentredString(lx + lw / 2, badge_y - 16, '기보 우대 3중 · 차입금 0원 · 무체납')

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
        ('학력', 'Central Saint Martins (영국) — 의류마케팅'),
        ('수상', '루이비통(Louis Vuitton) 디자인 컴피티션 우승'),
        ('인맥', '세인트마틴 동기 → 유럽 원단·의류 회사 재직'),
        ('창업', '(주)아꽁씨엘 창업 — ESG 업사이클 원단 사업'),
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
    c.drawString(rx, sec2_top - 26, '· Central Saint Martins (영국 세인트마틴 디자인스쿨) 의류마케팅')

    sec3_top = sec2_top - 56
    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(rx, sec3_top, '보유 자격증')
    c.setStrokeColor(GOLD)
    c.line(rx, sec3_top - 6, rx + 100, sec3_top - 6)
    c.setFillColor(BLACK)
    c.setFont(KR, 11)
    c.drawString(rx, sec3_top - 26, '· 루이비통 디자인 컴피티션 우승 · 유럽 원단·의류 업계 인맥')

    # 신용·재무 요약 박스 (기업 인증·매출)
    fin_top = sec3_top - 56
    c.setFillColor(NAVY)
    c.setFont(KRB, 14)
    c.drawString(rx, fin_top, '기업 인증 · 재무 요약')
    c.setStrokeColor(GOLD)
    c.line(rx, fin_top - 6, rx + 200, fin_top - 6)
    c.setFillColor(BLACK)
    c.setFont(KR, 11)
    c.drawString(rx, fin_top - 26, '· NICE 880점(1등급) · 차입금 0원 · 무체납 · 특허 2건 출원')
    c.drawString(rx, fin_top - 42, '· 2025 매출 7,000만 · R&D 집중 투자기 (매출 대비 R&D 100%+ · 영업손실 감내)')

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
        ('글로벌 지속가능 패션 시장',
         'ESG·순환경제 성장세 지속 확대',
         '명품 브랜드(버버리·구찌·에르메스 등) 순환경제 정책 강화'),
        ('업사이클 원단 시장',
         '명품 폐원단 재생 수요 급증',
         '지속가능성 소재 프리미엄 단가 형성'),
        ('K-패션 지속가능 브랜드',
         '국내 지속가능 패션 브랜드 확산',
         'B2B 원단 공급 기회 확대'),
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
    c.drawString(rx + 24, 110 + rh - 88, '2026 기본 시나리오 (메인)')
    c.setFont(KRB, 26)
    c.drawString(rx + 24, 110 + rh - 118, '2억 원')

    # 공격
    c.setStrokeColor(GOLD_LT)
    c.setLineWidth(1)
    c.rect(rx + 16, 110 + rh - 200, rw - 32, 50, stroke=1, fill=0)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 10)
    c.drawString(rx + 24, 110 + rh - 158, '2026 공격 시나리오')
    c.setFillColor(WHITE)
    c.setFont(KRB, 22)
    c.drawString(rx + 24, 110 + rh - 188, '2.5억 원')

    # 시차 안내
    c.setFillColor(GOLD_PALE)
    c.rect(rx + 16, 110 + 14, rw - 32, 50, stroke=0, fill=1)
    c.setFillColor(NAVY_DK)
    c.setFont(KRB, 10)
    c.drawString(rx + 24, 110 + 48, '※ 성장 궤도')
    c.setFillColor(NAVY)
    c.setFont(KR, 9)
    c.drawString(rx + 24, 110 + 32, '2027: 4~5억 / 2028: 7억 (혁신성장 30~40%)')
    c.drawString(rx + 24, 110 + 20, '특허 후속·유럽 채널 확장 반영')

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
        ('1', '명품 폐원단 재생 원단 (기존·특허 1)',
         '등급별 재생 원단 kg당 5만원 × 월 200kg',
         '= 월 1,000만 원 / 연 1.2억 원'),
        ('2', '업사이클 복합시트 (신규·특허 2)',
         '시트당 30만원 × 월 30개 × 6개월(2Q~)',
         '= 반기 5,400만 원'),
        ('3', '유럽 원단 독점 유통 (신규 채널)',
         '도매 마진 20% × 월 3,000만원 × 6개월',
         '= 반기 3,600만 원'),
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
        ('2024',     '15,000,000원',  '초기'),
        ('2025',     '70,000,000원',  '4.7배 증가'),
        ('2026 1Q',  '[회사 기재]',    '진행'),
        ('2026 목표', '250,000,000원', '3.6배 증가'),
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
        c.setFillColor(GREEN_OK if '증가' in tag else GRAY)
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
    c.drawString(rx + 20, pl_top - 44, '기본 시나리오 (메인)')
    c.setFont(KRB, 20)
    c.drawString(rx + 20, pl_top - 68, '2억 원')

    c.setStrokeColor(GOLD_LT)
    c.rect(rx + 12, pl_top - 122, rw - 24, 36, stroke=1, fill=0)
    c.setFillColor(GOLD_LT)
    c.setFont(KR, 9)
    c.drawString(rx + 20, pl_top - 96, '공격 시나리오')
    c.setFillColor(WHITE)
    c.setFont(KRB, 16)
    c.drawString(rx + 20, pl_top - 116, '2.5억 원')

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
            'no': '1', 'title': '명품 폐원단 재생 원단',
            'subtitle': '(기존 · 특허 1)',
            'tag': 'EXISTING',
            'calc1': '등급별 재생 원단 kg당 5만원',
            'calc2': '× 월 판매 200kg',
            'calc3': '= 월 1,000만 원',
            'calc4': '× 12개월',
            'big':   '연 1.2억 원',
            'note':  '단가·판매량 [회사 기재] 보정',
        },
        {
            'no': '2', 'title': '업사이클 복합시트',
            'subtitle': '(신규 · 특허 2 · 2Q 가동)',
            'tag': 'NEW',
            'calc1': '시트당 평균 30만 원',
            'calc2': '× 월 30개',
            'calc3': '= 월 900만 원',
            'calc4': '× 6개월 (2Q 후)',
            'big':   '반기 5,400만 원',
            'note':  '국내 지속가능 패션 브랜드 3~5곳',
        },
        {
            'no': '3', 'title': '유럽 원단 독점 유통',
            'subtitle': '(신규 채널 확대)',
            'tag': 'NEW',
            'calc1': '도매 마진 20%',
            'calc2': '× 월 도매 3,000만 원',
            'calc3': '= 월 600만 원',
            'calc4': '× 6개월',
            'big':   '반기 3,600만 원',
            'note':  '세인트마틴 동기 인맥 · 프·이·영',
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
    c.drawString(MX + 26, sum_y - 46, '기본 시나리오 (메인)')
    c.setFont(KRB, 18)
    c.drawString(MX + 26, sum_y - 64, '약 2억 원')

    c.setFillColor(WHITE)
    c.setFont(KR, 9)
    c.drawString(MX + 400, sum_y - 46, '공격 시나리오')
    c.setFillColor(GOLD_LT)
    c.setFont(KRB, 18)
    c.drawString(MX + 400, sum_y - 64, '약 2.5억 원')

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
        ('ESG·지속가능 패션 시장 성장세',
         '명품 브랜드 순환경제 정책 강화 (버버리·구찌·에르메스 등)'),
        ('2025 매출 7,000만 · 창업 2년차 시장 진입기',
         'R&D 투자로 영업손실 병행 감내 (특허 2건 확보 근거)'),
        ('특허 2건 기반 원단 프리미엄 단가',
         '재생 원단 · 업사이클 복합시트'),
        ('유럽 원단 파트너 협의 진행',
         '진입 장벽 확보 예정 (MOU·견적서 단계)'),
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
        ('여정민 대표', '세인트마틴 · 루이비통 컴피티션 우승 · 브랜딩·유럽 인맥'),
        ('나기주 연구원', '기업부설연구소 (KOITA) 소속 · 특허 R&D 인력'),
        ('직조설비 2,800만원 보유', '재생 원단 자체 직조·재조합 라인 (특허 1 구현)'),
        ('벤처(혁신성장)·특허 2건', '기보 우대 3중 · 기술평가등급 상향 근거'),
        ('유럽 원단 독점 유통', '프·이·영 세인트마틴 동기 네트워크'),
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
    y0 = section_title(c, '09', '자금 소요 계획', 'Fund Usage Plan — 기술보증기금 1억 (2트랙)')

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
    c.drawString(MX + 16, tr_top - 42, '기술보증기금 1억 · 2트랙 분리 (R&D 자금 60% + 운영자금 40%)  ·  수출자금은 실적 확보 후 별건 재신청')

    # 2개 자금 사용처 카드 (수출자금 삭제 · R&D 확대)
    cards = [
        {
            'no': '①', 'title': 'R&D 자금',
            'sub':  '특허 후속 개발 · 재생 공정 고도화 · 시제품 · 해외 인증 준비(OEKO-TEX·GRS)',
            'amt':  '6,000만 원  (60%)',
            'track':'R&D 트랙',
            'col':  NAVY,
        },
        {
            'no': '②', 'title': '운영자금',
            'sub':  '원단 매입 · 인건비 · 임차료 · 마케팅',
            'amt':  '4,000만 원  (40%)',
            'track':'운영자금 트랙',
            'col':  NAVY_LT,
        },
    ]
    n_cards = len(cards)
    cw = (SW - MX * 2 - 12 * (n_cards - 1)) / n_cards
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
    c.drawString(MX + 16, sum_y - 44, '기술보증기금 보증 요청  총 1억 원')
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
    c.drawString(MX + 16, SH - 308, 'T. [회사 기재]    E. [회사 기재]    사업자등록 758-88-02575')

    # 5대 강점 배지
    badges = ['특허 2건 출원', '벤처(혁신성장)·기업부설연구소',
              '유럽 원단 독점 유통', '세인트마틴·루이비통 우승 대표',
              'NICE 880점·차입금 0원', 'ESG 순환경제 원단']
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
                 '본 계획서는 초안이며 회사 확정 자료 반영 후 기보 심사 접수용 최종본으로 전환됩니다.')
    c.drawString(MX + 28, dis_y - 48,
                 '매출 전망은 회사 자체 추정이며 기술보증기금 심사 결과를 보장하지 않습니다.')

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
    out_dir = Path('/home/user/-/아꽁씨엘')
    out_path = out_dir / '(주)아꽁씨엘_정책자금사업계획서_20260514_v2_옵션A_1억.pdf'
    c = pdfcanvas.Canvas(str(out_path), pagesize=(SW, SH))
    c.setTitle('(주)아꽁씨엘 정책자금 사업계획서')
    c.setAuthor('히어컴퍼니 (HearCompany) Corporate Consulting')
    c.setSubject('기술보증기금 보증신청용 사업계획서 (1억 · v2 옵션 A)')

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
