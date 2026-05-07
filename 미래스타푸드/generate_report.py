#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(주)미래스타푸드 정부지원사업 리포트 PDF 생성기
- 작성: 히어컴퍼니 기업컨설팅 (HearCompany Corporate Consulting)
- 작성일: 2026-05-07
- 모드: 실시간 크롤링 기반 6공고 매칭 / D-day 컬럼 / 공고 진입 링크 클릭 가능
"""

import io
import os
import sys
import urllib.request
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage,
)


# ============================================================
# 1. 한국어 폰트 등록
# ============================================================

FONT_CANDIDATES = [
    "/tmp/NanumGothic.ttf",
    "/System/Library/Fonts/AppleGothic.ttf",
    "C:/Windows/Fonts/malgun.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]

KR_FONT_PATH = None
for fp in FONT_CANDIDATES:
    if os.path.exists(fp):
        KR_FONT_PATH = fp
        break

if KR_FONT_PATH is None:
    print("[INFO] Korean font not found - downloading NanumGothic...")
    KR_FONT_PATH = "/tmp/NanumGothic.ttf"
    urllib.request.urlretrieve(
        "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf",
        KR_FONT_PATH,
    )

pdfmetrics.registerFont(TTFont("KR", KR_FONT_PATH))
pdfmetrics.registerFont(TTFont("KR-Bold", KR_FONT_PATH))

plt.rcParams["font.family"] = "DejaVu Sans"
try:
    from matplotlib import font_manager as fm
    fm.fontManager.addfont(KR_FONT_PATH)
    plt.rcParams["font.family"] = fm.FontProperties(fname=KR_FONT_PATH).get_name()
except Exception as e:
    print(f"[WARN] matplotlib Korean font setup: {e}")
plt.rcParams["axes.unicode_minus"] = False


# ============================================================
# 2. 브랜드 컬러 / 스타일
# ============================================================

NAVY = colors.HexColor("#1F4E79")
BLUE = colors.HexColor("#2E75B6")
LIGHT_BG = colors.HexColor("#DEEAF1")
GREEN = colors.HexColor("#00B050")
ORANGE = colors.HexColor("#FF8C00")
RED = colors.HexColor("#C00000")
GRAY = colors.HexColor("#595959")
LIGHTGRAY = colors.HexColor("#D9D9D9")

styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "TitleKR", parent=styles["Title"], fontName="KR", fontSize=24,
    leading=30, textColor=colors.white, alignment=1,
)
style_subtitle = ParagraphStyle(
    "SubtitleKR", parent=styles["Title"], fontName="KR", fontSize=14,
    leading=20, textColor=colors.white, alignment=1,
)
style_h1 = ParagraphStyle(
    "H1KR", parent=styles["Heading1"], fontName="KR", fontSize=16,
    leading=22, textColor=NAVY, spaceAfter=8,
)
style_h2 = ParagraphStyle(
    "H2KR", parent=styles["Heading2"], fontName="KR", fontSize=12,
    leading=16, textColor=NAVY, spaceAfter=4,
)
style_body = ParagraphStyle(
    "BodyKR", parent=styles["BodyText"], fontName="KR", fontSize=9.5,
    leading=14, textColor=colors.black, spaceAfter=4,
)
style_small = ParagraphStyle(
    "SmallKR", parent=styles["BodyText"], fontName="KR", fontSize=8,
    leading=11, textColor=GRAY,
)
style_link = ParagraphStyle(
    "LinkKR", parent=styles["BodyText"], fontName="KR", fontSize=8,
    leading=11, textColor=BLUE,
)
style_white = ParagraphStyle(
    "WhiteKR", parent=styles["BodyText"], fontName="KR", fontSize=10,
    leading=14, textColor=colors.white, alignment=1,
)


# ============================================================
# 3. 공고 데이터 (실시간 크롤링 결과 — 2026-05-07 기준)
# ============================================================

ANNOUNCEMENTS = [
    {
        "no": "①",
        "title": "농식품 현지화지원사업 (현지 전문기관 자문)",
        "code": "PBLN_000000000118524",
        "agency": "농식품부 / aT",
        "period": "2026-01-06 ~ 2026-06-30",
        "dday": "D-54",
        "dday_color": GREEN,
        "amount": "연 5천만 원 한도",
        "fit": "★★★★★ 5/5",
        "diff": "낮음",
        "url": "https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000118524",
        "x": 2.5,
        "y": 4.5,
        "size": 500,
        "summary": "수출국 현지 전문기관 자문비 정부 90% 부담. 라벨링·할랄·HACCP 동등성 인증 자문 직결.",
    },
    {
        "no": "②",
        "title": "농식품 현지화지원사업 (수입등록·검사)",
        "code": "PBLN_000000000118527",
        "agency": "농식품부 / aT",
        "period": "2026-01-06 ~ 2026-12-31",
        "dday": "D-238",
        "dday_color": GREEN,
        "amount": "연 5천만 원 한도",
        "fit": "★★★★★ 5/5",
        "diff": "낮음",
        "url": "https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000118527",
        "x": 2.0,
        "y": 4.5,
        "size": 500,
        "summary": "FDA·중국·카타르 등 수입등록 대행비·식품검사비 환급. 영수증 기반 정산.",
    },
    {
        "no": "③",
        "title": "2026년 중소기업 정책자금 융자 (중진공)",
        "code": "PBLN_000000000116941",
        "agency": "중기부 / 중진공",
        "period": "1차 ~ 2026-05-08, 분기별 수시",
        "dday": "D-1 긴급",
        "dday_color": RED,
        "amount": "시설 60억 / 운전 5억",
        "fit": "★★★★☆ 4/5",
        "diff": "중상",
        "url": "https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/view.do?pblancId=PBLN_000000000116941",
        "x": 4.0,
        "y": 4.0,
        "size": 6000,
        "summary": "운전·시설·혁신성장·재도약 자금 통합. 5/8까지 1차 잔여분 즉시 신청 권고.",
    },
    {
        "no": "④",
        "title": "식품기업 인증 지원사업 (식품진흥원)",
        "code": "FOODPOLIS-2026",
        "agency": "농식품부 / 식품진흥원",
        "period": "2026 연중 상시",
        "dday": "상시",
        "dday_color": GREEN,
        "amount": "인증당 1~3천만 원",
        "fit": "★★★★★ 5/5",
        "diff": "낮음",
        "url": "https://www.foodpolis.kr/web/Board/3985/detailView.do",
        "x": 1.5,
        "y": 4.0,
        "size": 200,
        "summary": "HACCP·GMP·ISO 22000·FSSC 22000·KOSHER·NDI/GRAS 등 인증비 70~90% 정부 부담.",
    },
    {
        "no": "⑤",
        "title": "신용보증기금 운전·시설자금 보증 (KODIT)",
        "code": "KODIT-2026",
        "agency": "금융위 / KODIT",
        "period": "2026 연중 상시",
        "dday": "상시",
        "dday_color": ORANGE,
        "amount": "운전 매출 1/3 / 시설 100%",
        "fit": "★★★☆☆ 3/5",
        "diff": "중",
        "url": "https://www.kodit.co.kr/kodit/na/ntt/selectNttList.do?bbsId=407&mi=2518",
        "x": 3.5,
        "y": 3.0,
        "size": 3000,
        "summary": "보증료 0.5~3.0% / 식품제조업 우대. 중진공 미선정 시 백업.",
    },
    {
        "no": "⑥",
        "title": "기술보증기금 기술평가보증 (KIBO)",
        "code": "KIBO-2026",
        "agency": "중기부 / KIBO",
        "period": "2026 연중 상시",
        "dday": "상시",
        "dday_color": ORANGE,
        "amount": "일반 30억 / 우수 70억",
        "fit": "★★★☆☆ 3/5",
        "diff": "중",
        "url": "https://www.kibo.or.kr/main/work/work010101.do",
        "x": 3.8,
        "y": 3.5,
        "size": 3500,
        "summary": "기술평가 결과 자체가 R&D 가점. 벤처 우대 0.5%p.",
    },
]


# ============================================================
# 4. 페이지 헤더·푸터
# ============================================================

def header_footer(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 12 * mm, A4[0], 12 * mm, fill=1, stroke=0)
    canvas.setFont("KR", 9)
    canvas.setFillColor(colors.white)
    canvas.drawString(15 * mm, A4[1] - 8 * mm,
                      "(주)미래스타푸드  |  히어컴퍼니 기업컨설팅 (HearCompany)")
    canvas.drawRightString(A4[0] - 15 * mm, A4[1] - 8 * mm,
                           "정부지원사업 매칭 리포트  |  2026-05-07")
    # Footer bar
    canvas.setFillColor(LIGHT_BG)
    canvas.rect(0, 0, A4[0], 10 * mm, fill=1, stroke=0)
    canvas.setFont("KR", 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(15 * mm, 4 * mm,
                      "히어컴퍼니 (HearCompany) Corporate Consulting")
    canvas.drawRightString(A4[0] - 15 * mm, 4 * mm,
                           f"Page {doc.page}")
    canvas.restoreState()


# ============================================================
# 5. 차트 생성
# ============================================================

def make_priority_matrix():
    # matplotlib에서 ①②③ 글리프 누락 회피 → 1,2,3 매핑
    no_map = {"①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5", "⑥": "6"}
    fig, ax = plt.subplots(figsize=(10, 6))
    for a in ANNOUNCEMENTS:
        c = a["dday_color"].rgb()
        ax.scatter(a["x"], a["y"], s=a["size"] * 0.3, alpha=0.55,
                   color=(c[0], c[1], c[2]), edgecolors="black", linewidths=1.2)
        ax.annotate(no_map.get(a["no"], a["no"]), (a["x"], a["y"]),
                    ha="center", va="center",
                    fontsize=14, weight="bold", color="white")
        ax.annotate(a["title"][:18], (a["x"], a["y"] - 0.35),
                    ha="center", va="top", fontsize=8)

    ax.set_xlabel("신청 난이도 (1=낮음 → 5=높음)", fontsize=11)
    ax.set_ylabel("기대 효과 (1=낮음 → 5=높음)", fontsize=11)
    ax.set_title("우선순위 매트릭스 (버블 크기 = 지원 규모)",
                 fontsize=13, weight="bold", color="#1F4E79")
    ax.set_xlim(0.5, 5.0)
    ax.set_ylim(2.0, 5.5)
    ax.grid(True, alpha=0.3)
    ax.axvline(x=3.0, color="gray", linestyle="--", alpha=0.5)
    ax.axhline(y=3.5, color="gray", linestyle="--", alpha=0.5)
    ax.text(0.7, 5.3, "Quick Win\n(쉽고 효과 큼)", fontsize=9,
            color="#00B050", weight="bold")
    ax.text(4.2, 5.3, "Strategic Bet\n(어렵지만 효과 큼)", fontsize=9,
            color="#FF8C00", weight="bold")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


def make_timeline():
    no_map = {"①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5", "⑥": "6"}
    fig, ax = plt.subplots(figsize=(10, 4.5))
    today_x = 0
    timeline_data = []
    for a in ANNOUNCEMENTS:
        dday_str = a["dday"]
        if "상시" in dday_str:
            end = 240
            start = -30
        elif "긴급" in dday_str:
            end = 1
            start = -37
        elif "D-" in dday_str:
            try:
                d = int(dday_str.split("D-")[1].split(" ")[0])
                end = d
                start = -120
            except Exception:
                end = 60
                start = -30
        else:
            end = 60
            start = -30
        timeline_data.append((no_map.get(a["no"], a["no"]) + ". " + a["title"][:25], start, end, a["dday_color"]))

    for i, (label, s, e, col) in enumerate(reversed(timeline_data)):
        c = col.rgb()
        ax.barh(i, e - s, left=s, color=(c[0], c[1], c[2]),
                alpha=0.7, edgecolor="black", linewidth=0.8)
        ax.text(e + 5, i, f"~D{e:+d}", va="center", fontsize=8, color="#333")

    ax.axvline(x=today_x, color="red", linewidth=2, linestyle="--", alpha=0.8)
    ax.text(today_x, len(timeline_data) - 0.3, "오늘\n(2026-05-07)",
            ha="center", fontsize=9, color="red", weight="bold")

    ax.set_yticks(range(len(timeline_data)))
    ax.set_yticklabels([t[0] for t in reversed(timeline_data)], fontsize=8)
    ax.set_xlabel("오늘 기준 일수 (마이너스 = 과거 시작 / 플러스 = 미래 마감)", fontsize=10)
    ax.set_title("신청 타임라인 (2026-05-07 기준)",
                 fontsize=13, weight="bold", color="#1F4E79")
    ax.grid(True, alpha=0.3, axis="x")
    ax.set_xlim(-150, 280)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


# ============================================================
# 6. 페이지 빌드
# ============================================================

def build_cover(story):
    story.append(Spacer(1, 50 * mm))
    cover_data = [
        [Paragraph("정부지원사업 매칭 리포트", style_title)],
        [Spacer(1, 10 * mm)],
        [Paragraph("(주)미래스타푸드", style_title)],
        [Paragraph("육가공업 (KSIC C10120)", style_subtitle)],
        [Spacer(1, 30 * mm)],
        [Paragraph("실시간 크롤링 기반 6공고 매칭", style_white)],
        [Paragraph("작성일: 2026-05-07 (목)", style_white)],
        [Spacer(1, 30 * mm)],
        [Paragraph("히어컴퍼니 기업컨설팅", style_white)],
        [Paragraph("HearCompany Corporate Consulting", style_white)],
    ]
    cover_table = Table(cover_data, colWidths=[170 * mm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(cover_table)
    story.append(PageBreak())


def build_summary_cards(story):
    story.append(Paragraph("추천 Top 3 공고", style_h1))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "오늘(2026-05-07) 기준 마감 안 된 공고 6개 중 미래스타푸드 적합도·시너지·즉시성 기준 상위 3선.",
        style_body))
    story.append(Spacer(1, 6 * mm))

    top3 = ANNOUNCEMENTS[:3]
    for a in top3:
        cells = [
            [Paragraph(f"<b>{a['no']} {a['title']}</b>", style_white),
             Paragraph(f"<b>{a['dday']}</b>", style_white)],
            [Paragraph(f"기간: {a['period']}", style_body),
             Paragraph(f"적합도: {a['fit']}", style_body)],
            [Paragraph(f"규모: {a['amount']}", style_body),
             Paragraph(f"난이도: {a['diff']}", style_body)],
            [Paragraph(a["summary"], style_body), ""],
            [Paragraph(
                f'<link href="{a["url"]}" color="#2E75B6"><u>공고 진입: {a["url"][:75]}...</u></link>',
                style_link), ""],
        ]
        t = Table(cells, colWidths=[125 * mm, 45 * mm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), a["dday_color"]),
            ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
            ("BOX", (0, 0), (-1, -1), 1, NAVY),
            ("INNERGRID", (0, 1), (-1, -1), 0.3, LIGHTGRAY),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("SPAN", (0, 3), (1, 3)),
            ("SPAN", (0, 4), (1, 4)),
        ]))
        story.append(t)
        story.append(Spacer(1, 5 * mm))

    story.append(PageBreak())


def build_company_profile(story):
    story.append(Paragraph("기업 프로파일", style_h1))
    story.append(Spacer(1, 4 * mm))

    profile_data = [
        ["기업명", "(주)미래스타푸드"],
        ["업종", "육가공업 (한국표준산업분류 KSIC C10120 식육가공업 추정)"],
        ["추정 주력 품목", "햄 · 소시지 · 분쇄가공육 · 즉석조리식품"],
        ["매출액", "미입력 (확보 시 정밀 매칭 가능)"],
        ["인원", "미입력"],
        ["소재지", "미입력"],
        ["보유 인증", "미입력 (HACCP·ISO·벤처·이노비즈 확인 필요)"],
        ["수출 실적", "미입력"],
        ["자금 needs", "미입력 — 비융자 우선 전략 적용"],
    ]
    t = Table(profile_data, colWidths=[40 * mm, 130 * mm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (0, -1), NAVY),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("BACKGROUND", (1, 0), (1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHTGRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph("매칭 5영역 카테고리 맵", style_h2))
    cat_data = [
        ["A. 정책자금·운영자금", "중진공 융자, 기보·신보 보증", "③ ⑤ ⑥"],
        ["B. R&D·기술개발", "ipet 농림식품 R&D (1~3월 마감)", "비수기"],
        ["C. 수출·해외진출", "aT 현지화지원, 통합한국관, 수출바우처", "① ②"],
        ["D. 인증·HACCP·안전", "식품진흥원 식품기업 인증 지원사업", "④"],
        ["E. 스마트공장·시설", "부처협업형 스마트공장 (4월 종료)", "비수기"],
    ]
    t2 = Table(cat_data, colWidths=[55 * mm, 80 * mm, 35 * mm])
    t2.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (0, -1), BLUE),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("BACKGROUND", (2, 0), (2, -1), LIGHT_BG),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHTGRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t2)
    story.append(PageBreak())


def build_matching_table(story):
    story.append(Paragraph("매칭 현황표 (전체 6공고)", style_h1))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "신청기간(D-day) 컬럼 포함. 모든 공고 마감일 ≥ 2026-05-07.",
        style_small))
    story.append(Spacer(1, 5 * mm))

    header = ["No", "공고명", "기관", "신청기간 (D-day)", "지원규모", "적합도"]
    rows = [header]
    for a in ANNOUNCEMENTS:
        rows.append([
            a["no"],
            a["title"][:30],
            a["agency"],
            f"{a['period']}\n[{a['dday']}]",
            a["amount"],
            a["fit"],
        ])

    t = Table(rows, colWidths=[10 * mm, 55 * mm, 25 * mm, 42 * mm, 28 * mm, 22 * mm],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("ALIGN", (5, 1), (5, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHTGRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    for i, a in enumerate(ANNOUNCEMENTS, start=1):
        t.setStyle(TableStyle([
            ("TEXTCOLOR", (3, i), (3, i), a["dday_color"]),
            ("FONTNAME", (3, i), (3, i), "KR"),
        ]))
    story.append(t)
    story.append(Spacer(1, 6 * mm))

    # 공고 진입 링크 (전체)
    story.append(Paragraph("공고 진입 링크 (개별 공고 상세 URL)", style_h2))
    for a in ANNOUNCEMENTS:
        story.append(Paragraph(
            f'{a["no"]} <link href="{a["url"]}" color="#2E75B6"><u>{a["url"]}</u></link>',
            style_link))
        story.append(Spacer(1, 1 * mm))
    story.append(PageBreak())


def build_matrix_chart(story):
    story.append(Paragraph("우선순위 매트릭스", style_h1))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "X축: 신청 난이도 / Y축: 기대 효과 / 버블 크기: 지원 규모 / 색: D-day (초록=여유, 주황=상시, 빨강=긴급)",
        style_small))
    story.append(Spacer(1, 4 * mm))

    chart = make_priority_matrix()
    story.append(RLImage(chart, width=170 * mm, height=100 * mm))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("해석", style_h2))
    story.append(Paragraph(
        "공고 ① · ② (우상단)는 Quick Win 영역으로 즉시 신청 권고. "
        "공고 ③ (큰 빨간 버블)은 Strategic Bet — 5/8 1차 마감 임박. "
        "공고 ④는 가장 쉬운 진입로. ⑤ · ⑥은 자금 보완책.",
        style_body))
    story.append(PageBreak())


def build_timeline_chart(story):
    story.append(Paragraph("신청 타임라인 (2026-05-07 기준)", style_h1))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "빨간 점선이 오늘. 공고별 신청 가능 윈도우.",
        style_small))
    story.append(Spacer(1, 4 * mm))

    chart = make_timeline()
    story.append(RLImage(chart, width=170 * mm, height=80 * mm))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("타이밍 전략", style_h2))
    timeline_strategy = [
        ["순서", "공고", "신청 시점", "준비 일정"],
        ["1", "③ 중진공 1차", "5/7~5/8 (즉시)", "재무제표·사업계획서 24시간 내 준비"],
        ["2", "④ 식품진흥원 인증", "5/9~5/15", "현재 보유 인증 점검 → 신규 인증 선정"],
        ["3", "① 현지화 자문", "6월 초", "수출국 1순위 결정 + 바이어 컨택 증빙"],
        ["4", "② 수입등록·검사", "8~9월", "①의 자문 결과 기반으로 신청"],
        ["5", "⑤ 신보 / ⑥ 기보", "③ 미선정 시 백업", "필요시 즉시"],
    ]
    t = Table(timeline_strategy, colWidths=[12 * mm, 55 * mm, 35 * mm, 68 * mm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHTGRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(PageBreak())


def build_proposal_draft(story):
    story.append(Paragraph("제안서 초안 — 1순위: 농식품 현지화지원사업", style_h1))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "공고 ① + ② 묶음 신청 가정. 미래스타푸드 정보 미확보분은 [입력필요] 표기.",
        style_small))
    story.append(Spacer(1, 6 * mm))

    story.append(Paragraph("1. 사업 참여 필요성", style_h2))
    story.append(Paragraph(
        "(주)미래스타푸드는 KSIC C10120 식육가공업으로 추정되는 육가공 제조 기업으로, "
        "햄·소시지·분쇄가공육 등의 K-푸드 수출 잠재력을 보유하고 있다. "
        "그러나 수출 첫 진입 단계에서 발생하는 ▲수출국 식품 라벨링 규정 ▲동물성 식품 수입등록(중국 GACC, 미국 FSIS) "
        "▲할랄·할랄 동등성 인증 ▲현지 미생물·이화학 검사 비용은 중소 육가공기업 단독 부담이 어려운 수준이다. "
        "본 사업의 자문·등록·검사 지원금은 이 진입 장벽을 직접 낮추는 가장 효율적 수단이다.",
        style_body))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("2. 사업 추진 계획", style_h2))
    plan = [
        ["단계", "주요 내용", "기간", "예상 성과"],
        ["1", "수출 1순위 국가 결정 + 바이어 컨택 증빙", "2026.06", "수출 계획서 v1"],
        ["2", "현지 전문기관 자문 (라벨·식품법규)", "2026.06~08", "현지 적합 라벨 디자인"],
        ["3", "현지 수입등록 신청 (FDA/GACC)", "2026.08~11", "수입등록 완료"],
        ["4", "현지 미생물·이화학 검사", "2026.10~12", "수출 적합성 확보"],
        ["5", "첫 수출 PO 확보", "2026.12~", "수출 실적 발생"],
    ]
    t = Table(plan, colWidths=[12 * mm, 65 * mm, 28 * mm, 65 * mm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHTGRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("3. 기대 효과 및 성과 지표", style_h2))
    story.append(Paragraph(
        "<b>정량 지표</b><br/>"
        "• 수출 첫 PO 1건 이상 (사업 종료 시점)<br/>"
        "• 정부 지원 수령액 5,000만 원 ~ 1억 원 (① + ② 합산)<br/>"
        "• 수출 인증 1건 이상 신규 취득 (HACCP 동등성·할랄 등)<br/>"
        "<br/><b>정성 지표</b><br/>"
        "• 수출국 식품법규 대응 역량 내재화<br/>"
        "• 현지 바이어 네트워크 1개 이상 확보<br/>"
        "• 후속 지원사업(수출바우처 3차·통합한국관 하반기) 진입 트랙 확보",
        style_body))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("4. 사업 지속 계획", style_h2))
    story.append(Paragraph(
        "지원금 종료 후에도 자체 수출 인프라를 유지하기 위해 ▲전담 수출 담당자 1인 배치 "
        "▲공고 ④ 식품진흥원 인증 지원사업으로 인증 갱신 비용 절감 "
        "▲중진공 ③·KIBO ⑥ 기술평가보증을 활용한 수출 운전자금 확보 "
        "▲2027년 농식품글로벌성장패키지(공모형) 진입 등 후속 단계로 이어간다.",
        style_body))
    story.append(PageBreak())


def build_appendix(story):
    story.append(Paragraph("부록 1 — 추가 확인 필요 정보 5가지", style_h1))
    story.append(Spacer(1, 3 * mm))
    info_data = [
        ["1", "연 매출액 / 직전 3년 추이", "중진공·신보·기보 한도 산정 핵심"],
        ["2", "현재 보유 인증", "HACCP·ISO·벤처·이노비즈 - 가점 반영"],
        ["3", "수출 실적·계획", "①·② 신청 적격성 직결"],
        ["4", "자금 needs 우선순위", "시설 / 운영 / 수출 / R&D 중 선택"],
        ["5", "임직원 수·R&D 인력·기업부설연구소", "기보 등급 우대 + R&D 진입 트랙"],
    ]
    t = Table(info_data, colWidths=[10 * mm, 65 * mm, 95 * mm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (0, -1), NAVY),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHTGRAY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT_BG]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph("부록 2 — 검증·제외 공고 (빡빡이 트레이서빌리티)", style_h1))
    story.append(Spacer(1, 3 * mm))
    excluded = [
        ["고부가가치식품기술개발사업", "2026-02-09", "마감 경과"],
        ["농식품글로벌성장패키지(신청형)", "2026-02-06", "마감 경과"],
        ["농식품 벤처육성 지원사업(창업)", "2026-02-23", "마감 + 업력 5년 초과 가능"],
        ["식품기능성평가지원 사업", "2026-01-16", "마감 경과"],
        ["밀착형 기술사업화 지원사업", "2026-03-20", "마감 + 기술이전 전제"],
        ["국가식품클러스터 통합마케팅", "2026-03-30", "마감 + 클러스터 입주기업 우대"],
        ["글로벌 NEXT K-푸드", "2026-03-03", "마감 경과"],
        ["수출지원기반활용사업 2차(중기부)", "2026-05-06", "오늘 5/7 기준 1일 경과"],
        ["글로벌 K-푸드 페어 상반기", "2025-12-19", "마감 경과"],
        ["부처협업형 스마트공장", "2026-04-09", "마감 경과"],
    ]
    t2 = Table([["공고명", "마감일", "제외 사유"]] + excluded,
               colWidths=[75 * mm, 30 * mm, 65 * mm])
    t2.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), GRAY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.8, GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHTGRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t2)
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph(
        "본 리포트의 모든 공고 마감일은 2026-05-07 오전 시점 실시간 크롤링 결과이며, "
        "정부 사이트의 공고 변경·취소·예산 소진 발생 시 변동될 수 있다. "
        "신청 직전 반드시 공고 진입 링크에서 최신 상태를 재확인할 것.",
        style_small))


# ============================================================
# 7. 메인
# ============================================================

def main():
    out_dir = "/home/user/-/미래스타푸드"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(
        out_dir,
        "(주)미래스타푸드_정부지원사업리포트_20260507.pdf",
    )

    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=15 * mm, rightMargin=15 * mm,
        topMargin=18 * mm, bottomMargin=14 * mm,
        title="(주)미래스타푸드 정부지원사업 매칭 리포트",
        author="히어컴퍼니 기업컨설팅 (HearCompany)",
    )

    story = []
    build_cover(story)
    build_summary_cards(story)
    build_company_profile(story)
    build_matching_table(story)
    build_matrix_chart(story)
    build_timeline_chart(story)
    build_proposal_draft(story)
    build_appendix(story)

    doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=header_footer)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"[OK] PDF generated: {out_path}")
    print(f"[OK] Size: {size_kb:.1f} KB")

    try:
        if sys.platform == "darwin":
            subprocess.run(["open", out_path])
        elif sys.platform == "win32":
            os.startfile(out_path)
    except Exception:
        pass

    return out_path


if __name__ == "__main__":
    main()
