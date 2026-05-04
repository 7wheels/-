#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(주)미르스타푸드 정부지원사업 인포그래픽 리포트 생성기
Powered by 히어컴퍼니 기업컨설팅
"""

import os
import io
import sys
import urllib.request
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable

# ---------------------------------------------------------------------------
# 한국어 폰트 등록
# ---------------------------------------------------------------------------
def register_korean_font():
    candidates = [
        "/System/Library/Fonts/AppleGothic.ttf",
        "C:/Windows/Fonts/malgun.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/opentype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/tmp/NanumGothic.ttf",
    ]
    for fp in candidates:
        if os.path.exists(fp):
            try:
                pdfmetrics.registerFont(TTFont("KR", fp))
                return fp
            except Exception:
                continue
    url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    dst = "/tmp/NanumGothic.ttf"
    urllib.request.urlretrieve(url, dst)
    pdfmetrics.registerFont(TTFont("KR", dst))
    return dst

KR_FONT_PATH = register_korean_font()

# matplotlib 한글 폰트
from matplotlib import font_manager as fm
fm.fontManager.addfont(KR_FONT_PATH)
kr_name = fm.FontProperties(fname=KR_FONT_PATH).get_name()
plt.rcParams["font.family"] = kr_name
plt.rcParams["axes.unicode_minus"] = False

# ---------------------------------------------------------------------------
# 브랜드 컬러
# ---------------------------------------------------------------------------
NAVY = colors.HexColor("#1F4E79")
BLUE = colors.HexColor("#2E75B6")
LIGHT_BLUE = colors.HexColor("#DEEAF1")
GREEN = colors.HexColor("#00B050")
ORANGE = colors.HexColor("#FF8C00")
RED = colors.HexColor("#C00000")
GRAY = colors.HexColor("#595959")
LIGHT_GRAY = colors.HexColor("#F2F2F2")

# ---------------------------------------------------------------------------
# 데이터: 미르스타푸드 매칭 공고
# ---------------------------------------------------------------------------
COMPANY = {
    "name": "(주)미르스타푸드",
    "industry": "식육가공업 (KSIC C10120)",
    "products": "햄 · 소시지 · 분쇄가공육",
    "cert": "HACCP 인증 운영 중",
    "size": "중소기업 (우선지원 대상)",
}

ANNOUNCEMENTS = [
    {
        "title": "2026년 스마트공장 지원사업\n(식품제조업·육가공업 특화 트랙)",
        "source": "중기부·식약처·삼성전자",
        "deadline": "2026-05-30",
        "budget": "최대 2억원",
        "fit": "상",
        "category": "설비/DX",
        "summary": "HACCP 인증 식품기업 대상 스마트HACCP 고도화·MES 구축·디지털전환 지원. 5월 식품업 특화 30개사 추가 모집.",
        "difficulty": 2.5,
        "effect": 4.5,
        "size_num": 200,
        "start_day": 0,
        "duration": 30,
    },
    {
        "title": "2026년 고부가가치식품기술개발사업",
        "source": "농림축산식품부 / 농기평",
        "deadline": "2026-06-15",
        "budget": "총 115억원 (과제당 3-7억)",
        "fit": "상",
        "category": "R&D",
        "summary": "미래대응식품·식품 품질안전·차세대 식품가공 분야 R&D. 식육가공 신제품·공정혁신 과제 적합.",
        "difficulty": 4.0,
        "effect": 5.0,
        "size_num": 500,
        "start_day": 5,
        "duration": 45,
    },
    {
        "title": "2026년 식품기업 인증 지원사업",
        "source": "식품안전관리인증원 (foodpolis)",
        "deadline": "상시",
        "budget": "인증 컨설팅·심사비 지원",
        "fit": "상",
        "category": "인증",
        "summary": "HACCP 고도화·스마트HACCP·ISO22000·FSSC22000 등 국제인증 취득 지원. 미르스타푸드 HACCP 자산 확장에 최적.",
        "difficulty": 1.5,
        "effect": 3.5,
        "size_num": 50,
        "start_day": 0,
        "duration": 200,
    },
    {
        "title": "2026년 체계적 현장훈련(S-OJT)\n참여기업 모집",
        "source": "한국산업인력공단",
        "deadline": "2026-10-30 (상시)",
        "budget": "훈련비·과정운영비 전액 지원",
        "fit": "상",
        "category": "훈련",
        "summary": "우선지원대상기업 대상. 현재 작성 중인 식육가공품 제조 공정 운영 실무 향상 과정(40h)과 즉시 연계.",
        "difficulty": 1.5,
        "effect": 3.0,
        "size_num": 80,
        "start_day": 0,
        "duration": 180,
    },
    {
        "title": "2026년 중소기업 기술개발 지원사업\n(창업성장기술개발 디딤돌)",
        "source": "중기부 / TIPA",
        "deadline": "2026-05-20",
        "budget": "최대 1.2억원 (1년)",
        "fit": "중",
        "category": "R&D",
        "summary": "창업 7년 이내 기술혁신형 중소기업 대상. 식육가공 공정·품질·HMR 신제품 개발에 활용 가능.",
        "difficulty": 3.5,
        "effect": 4.0,
        "size_num": 120,
        "start_day": 2,
        "duration": 17,
    },
    {
        "title": "이노비즈(Inno-Biz) 인증 신청",
        "source": "이노비즈협회 (innobiz.net)",
        "deadline": "상시",
        "budget": "세제·금융·R&D 가점 혜택",
        "fit": "중",
        "category": "인증",
        "summary": "업력 3년 이상 기술혁신 중소기업 인증. 정책자금·R&D 신청 시 가점, 보증료 우대 효과.",
        "difficulty": 2.5,
        "effect": 3.5,
        "size_num": 30,
        "start_day": 10,
        "duration": 90,
    },
    {
        "title": "2026년 중소기업 정책자금 융자\n(혁신성장유형)",
        "source": "중소벤처기업진흥공단",
        "deadline": "2026-12-31 (소진시)",
        "budget": "운전 5억 / 시설 60억",
        "fit": "중",
        "category": "정책자금(융자)",
        "summary": "혁신성장 분야 시설·운전자금 저리 융자. 자금 에이전트 추가 분석 권고 항목.",
        "difficulty": 3.0,
        "effect": 3.5,
        "size_num": 600,
        "start_day": 15,
        "duration": 60,
    },
]

# ---------------------------------------------------------------------------
# 차트 생성
# ---------------------------------------------------------------------------
def make_priority_matrix():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
    fig.patch.set_facecolor("white")

    color_map = {"상": "#00B050", "중": "#FF8C00", "하": "#C00000"}
    for a in ANNOUNCEMENTS:
        ax.scatter(a["difficulty"], a["effect"],
                   s=a["size_num"] * 3,
                   c=color_map[a["fit"]],
                   alpha=0.55, edgecolors="#1F4E79", linewidth=1.5)

    labels = ["스마트공장(식품)", "고부가가치 식품 R&D", "식품인증 지원",
              "S-OJT", "디딤돌 R&D", "이노비즈", "정책자금 융자"]
    for a, lab in zip(ANNOUNCEMENTS, labels):
        ax.annotate(lab,
                    (a["difficulty"], a["effect"]),
                    xytext=(8, 8), textcoords="offset points",
                    fontsize=9, color="#1F4E79", fontweight="bold")

    ax.axhline(3.0, color="#BFBFBF", linestyle="--", linewidth=0.8)
    ax.axvline(3.0, color="#BFBFBF", linestyle="--", linewidth=0.8)
    ax.set_xlim(0.5, 5)
    ax.set_ylim(2, 5.5)
    ax.set_xlabel("신청 난이도 (낮음 ← → 높음)", fontsize=11, color="#1F4E79", fontweight="bold")
    ax.set_ylabel("기대 효과 (낮음 ← → 높음)", fontsize=11, color="#1F4E79", fontweight="bold")
    ax.set_title("우선순위 매트릭스 (버블 크기 = 지원 규모)",
                 fontsize=13, color="#1F4E79", fontweight="bold", pad=12)
    ax.grid(True, alpha=0.2)
    for spine in ax.spines.values():
        spine.set_color("#BFBFBF")

    ax.text(1.2, 5.2, "Quick Win", fontsize=10, color="#00B050", fontweight="bold")
    ax.text(4.2, 5.2, "전략과제", fontsize=10, color="#1F4E79", fontweight="bold")
    ax.text(1.2, 2.2, "기본 정비", fontsize=10, color="#595959")
    ax.text(4.2, 2.2, "재검토", fontsize=10, color="#C00000")

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

def make_timeline():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    fig.patch.set_facecolor("white")

    color_map = {"상": "#00B050", "중": "#FF8C00", "하": "#C00000"}
    titles = ["스마트공장(식품)", "고부가가치 R&D", "식품인증 지원",
              "S-OJT", "디딤돌 R&D", "이노비즈", "정책자금"]
    y_pos = np.arange(len(ANNOUNCEMENTS))

    for i, a in enumerate(ANNOUNCEMENTS):
        ax.barh(i, a["duration"], left=a["start_day"],
                color=color_map[a["fit"]], alpha=0.75,
                edgecolor="#1F4E79", linewidth=1)
        ax.text(a["start_day"] + a["duration"] + 2, i,
                a["deadline"], va="center", fontsize=8.5, color="#1F4E79")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(titles, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("오늘로부터 경과일 (단위: 일)", fontsize=11, color="#1F4E79", fontweight="bold")
    ax.set_title("신청 타임라인 (2026-05-03 기준)",
                 fontsize=13, color="#1F4E79", fontweight="bold", pad=12)
    ax.grid(True, alpha=0.2, axis="x")
    ax.set_xlim(0, 230)
    for spine in ax.spines.values():
        spine.set_color("#BFBFBF")

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

# ---------------------------------------------------------------------------
# PDF 빌드
# ---------------------------------------------------------------------------
def build_pdf(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm,
        title="미르스타푸드 정부지원사업 리포트",
        author="히어컴퍼니 기업컨설팅",
    )

    styles = getSampleStyleSheet()
    H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="KR",
                        fontSize=20, textColor=NAVY, spaceAfter=10, leading=26)
    H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="KR",
                        fontSize=14, textColor=NAVY, spaceBefore=10, spaceAfter=8, leading=20)
    H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="KR",
                        fontSize=11, textColor=BLUE, spaceBefore=6, spaceAfter=4, leading=16)
    BODY = ParagraphStyle("BODY", parent=styles["BodyText"], fontName="KR",
                          fontSize=10, textColor=colors.black, leading=15)
    SMALL = ParagraphStyle("SMALL", parent=styles["BodyText"], fontName="KR",
                           fontSize=8.5, textColor=GRAY, leading=12)
    COVER_TITLE = ParagraphStyle("COVERT", parent=styles["Title"], fontName="KR",
                                 fontSize=30, textColor=colors.white, alignment=TA_CENTER, leading=40)
    COVER_SUB = ParagraphStyle("COVERS", parent=styles["Title"], fontName="KR",
                               fontSize=16, textColor=LIGHT_BLUE, alignment=TA_CENTER, leading=24)
    COVER_BR = ParagraphStyle("COVERB", parent=styles["BodyText"], fontName="KR",
                              fontSize=11, textColor=colors.white, alignment=TA_CENTER, leading=16)

    story = []

    # -------- 표지 --------
    cover_tbl = Table(
        [
            [Spacer(1, 60*mm)],
            [Paragraph("정부지원사업<br/>매칭 리포트", COVER_TITLE)],
            [Spacer(1, 14*mm)],
            [Paragraph("(주)미르스타푸드", COVER_SUB)],
            [Spacer(1, 6*mm)],
            [Paragraph("식육가공업 · HACCP 인증기업", COVER_BR)],
            [Spacer(1, 70*mm)],
            [Paragraph(f"발행일 : {datetime.now().strftime('%Y년 %m월 %d일')}", COVER_BR)],
            [Spacer(1, 6*mm)],
            [Paragraph("Powered by <b>히어컴퍼니 기업컨설팅</b>", COVER_BR)],
            [Paragraph("HereCompany Consulting", COVER_BR)],
        ],
        colWidths=[180*mm],
    )
    cover_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(cover_tbl)
    story.append(PageBreak())

    # -------- 요약 카드 (Top 3) --------
    story.append(Paragraph("01. 추천 Top 3 프로그램", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))

    top3 = ANNOUNCEMENTS[:3]
    fit_color = {"상": GREEN, "중": ORANGE, "하": RED}
    cards = []
    for a in top3:
        card = Table([
            [Paragraph(f'<b>{a["category"]}</b>', ParagraphStyle("c", fontName="KR", fontSize=9, textColor=colors.white, alignment=TA_CENTER))],
            [Paragraph(f'<b>{a["title"]}</b>', ParagraphStyle("t", fontName="KR", fontSize=10, textColor=NAVY, leading=14))],
            [Paragraph(f'출처 : {a["source"]}', SMALL)],
            [Paragraph(f'<b>지원 규모</b>  {a["budget"]}', BODY)],
            [Paragraph(f'<b>마감</b>  {a["deadline"]}', BODY)],
            [Paragraph(f'적합도 <b>{a["fit"]}</b>', ParagraphStyle("f", fontName="KR", fontSize=10, textColor=colors.white, alignment=TA_CENTER))],
        ], colWidths=[55*mm], rowHeights=[8*mm, 22*mm, 7*mm, 9*mm, 9*mm, 8*mm])
        card.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), NAVY),
            ("BACKGROUND", (0, 5), (0, 5), fit_color[a["fit"]]),
            ("BACKGROUND", (0, 1), (0, 4), LIGHT_BLUE),
            ("BOX", (0, 0), (-1, -1), 0.6, NAVY),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        cards.append(card)

    cards_row = Table([cards], colWidths=[58*mm, 58*mm, 58*mm])
    cards_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(cards_row)
    story.append(Spacer(1, 6*mm))

    # 핵심 메시지
    msg = Table([[Paragraph(
        "<b>핵심 메시지</b><br/>"
        "미르스타푸드는 HACCP 인증 보유 식육가공업체로, <b>식품업 특화 스마트공장 사업</b>과 "
        "<b>고부가가치식품기술개발 R&D</b> 두 축을 우선 공략하는 것이 가장 효율적입니다. "
        "동시에 작성 중인 S-OJT 훈련계획서를 산업인력공단 지원 트랙으로 연계하면 즉시 인건비·훈련비를 회수할 수 있습니다.",
        BODY)]], colWidths=[180*mm])
    msg.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
        ("BOX", (0, 0), (-1, -1), 0.5, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(msg)
    story.append(PageBreak())

    # -------- 기업 프로파일 --------
    story.append(Paragraph("02. 기업 프로파일", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))

    prof_data = [
        ["기업명", COMPANY["name"], "업종", COMPANY["industry"]],
        ["주요 제품", COMPANY["products"], "보유 인증", COMPANY["cert"]],
        ["기업 규모", COMPANY["size"], "현재 이슈", "S-OJT 40h 훈련계획서 작성 중"],
        ["관심 분야", "정책자금 · 인증(벤처/이노비즈) · R&D · 정부지원사업", "", ""],
    ]
    prof = Table(prof_data, colWidths=[28*mm, 62*mm, 28*mm, 62*mm])
    prof.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BACKGROUND", (0, 0), (0, -1), NAVY),
        ("BACKGROUND", (2, 0), (2, -1), NAVY),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.white),
        ("BACKGROUND", (1, 0), (1, -1), LIGHT_GRAY),
        ("BACKGROUND", (3, 0), (3, -1), LIGHT_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.white),
        ("SPAN", (1, 3), (3, 3)),
    ]))
    story.append(prof)
    story.append(Spacer(1, 8*mm))

    # 강점 박스
    strength = Table([
        [Paragraph("<b>강점</b>", H3),
         Paragraph("<b>기회</b>", H3),
         Paragraph("<b>리스크</b>", H3)],
        [Paragraph("· HACCP 운영 실적<br/>· 식육가공 전문성<br/>· 우선지원 대상", BODY),
         Paragraph("· 식품 특화 스마트공장<br/>· 고부가가치 R&D 11.5억<br/>· S-OJT 즉시 연계", BODY),
         Paragraph("· R&D 사업계획서 부담<br/>· 자체부담금 매칭<br/>· 단기 마감 다수", BODY)],
    ], colWidths=[60*mm, 60*mm, 60*mm])
    strength.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE),
        ("BOX", (0, 0), (-1, -1), 0.5, BLUE),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(strength)
    story.append(PageBreak())

    # -------- 매칭 현황표 --------
    story.append(Paragraph("03. 매칭 공고 종합표", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))

    header = ["#", "공고명", "출처", "지원 규모", "마감", "적합도"]
    rows = [header]
    for i, a in enumerate(ANNOUNCEMENTS, 1):
        rows.append([
            str(i),
            Paragraph(a["title"].replace("\n", " "), ParagraphStyle("p", fontName="KR", fontSize=8.5, leading=11)),
            Paragraph(a["source"], ParagraphStyle("p", fontName="KR", fontSize=8, leading=10)),
            a["budget"],
            a["deadline"],
            a["fit"],
        ])
    tbl = Table(rows, colWidths=[8*mm, 56*mm, 32*mm, 35*mm, 27*mm, 14*mm])
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, 0), 9.5),
        ("FONTSIZE", (0, 1), (-1, -1), 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("ALIGN", (-1, 1), (-1, -1), "CENTER"),
        ("ALIGN", (-2, 1), (-2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BFBFBF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for i, a in enumerate(ANNOUNCEMENTS, 1):
        style.append(("BACKGROUND", (-1, i), (-1, i), fit_color[a["fit"]]))
        style.append(("TEXTCOLOR", (-1, i), (-1, i), colors.white))
        style.append(("FONTSIZE", (-1, i), (-1, i), 10))
    tbl.setStyle(TableStyle(style))
    story.append(tbl)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "주: 융자 성격 항목(7번 정책자금)은 자금 에이전트에 추가 분석 요청 권고. "
        "예상 수혜 금액은 평균 선정 규모 기준 보수적 추정치.", SMALL))
    story.append(PageBreak())

    # -------- 우선순위 매트릭스 --------
    story.append(Paragraph("04. 우선순위 매트릭스", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
    story.append(Paragraph(
        "X축은 신청 난이도, Y축은 기대 효과, 버블 크기는 지원 규모를 의미합니다. "
        "<b>우상단(전략과제)</b>의 고부가가치 R&D, <b>중상단(Quick Win)</b>의 스마트공장·식품인증을 "
        "병행 추진하는 포트폴리오가 권고됩니다.", BODY))
    story.append(Spacer(1, 4*mm))
    story.append(RLImage(make_priority_matrix(), width=180*mm, height=110*mm))
    story.append(PageBreak())

    # -------- 타임라인 --------
    story.append(Paragraph("05. 신청 타임라인", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
    story.append(Paragraph(
        "오늘(2026-05-03) 기준 각 공고의 준비~마감 구간을 시각화했습니다. "
        "5월 내 마감되는 <b>스마트공장(식품)</b>과 <b>디딤돌 R&D</b>를 최우선 착수하십시오.", BODY))
    story.append(Spacer(1, 4*mm))
    story.append(RLImage(make_timeline(), width=180*mm, height=100*mm))
    story.append(PageBreak())

    # -------- 제안서 초안 --------
    story.append(Paragraph("06. 1순위 공고 제안서 초안", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
    story.append(Paragraph("미르스타푸드 × 2026년 스마트공장 지원사업 (식품제조업·육가공업)", H2))

    story.append(Paragraph("사업 참여 필요성", H3))
    story.append(Paragraph(
        "미르스타푸드는 햄·소시지·분쇄가공육을 생산하는 식육가공 전문기업으로, "
        "현행 HACCP 운영 체계를 보유하고 있으나 일일 점검·온도 모니터링·원료 추적이 수기 의존도가 높습니다. "
        "본 사업을 통해 <b>스마트HACCP(센서 기반 CCP 자동 모니터링)</b>과 <b>MES(생산실행시스템)</b>를 구축함으로써, "
        "위해요소 실시간 통제·로트 추적성·생산성을 동시에 확보하고자 합니다.", BODY))

    story.append(Paragraph("추진 계획", H3))
    plan = Table([
        ["단계", "주요 내용", "기간", "예상 성과"],
        ["1단계", "현황 진단 · CCP 매핑 · 시스템 설계", "1-2개월", "스마트HACCP 설계서"],
        ["2단계", "센서·IoT 게이트웨이 설치 / MES 모듈 도입", "3-5개월", "온도·pH 자동기록"],
        ["3단계", "데이터 통합 · 운영자 교육 · 시범 가동", "6-8개월", "로트 추적 100%"],
        ["4단계", "성과 측정 · 표준화 · 인증 갱신 연계", "9-10개월", "불량률 30% 감축"],
    ], colWidths=[18*mm, 78*mm, 24*mm, 50*mm])
    plan.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("ALIGN", (2, 1), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BFBFBF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(plan)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("기대 효과 및 성과 지표", H3))
    kpi = Table([
        ["구분", "측정 지표", "현재", "목표(1년 내)"],
        ["품질", "위해요소 일탈 건수", "월 평균 4건", "월 1건 이하 (75%↓)"],
        ["생산성", "라인당 시간당 생산량", "기준치 100", "120 (20%↑)"],
        ["추적성", "로트 추적 소요시간", "평균 4시간", "5분 이내"],
        ["인력", "수기 점검 인력 시간", "주 40h", "주 10h (재배치)"],
        ["매출", "신규 거래처 확보(B2B)", "-", "신규 5개사 / +12%"],
    ], colWidths=[22*mm, 60*mm, 38*mm, 50*mm])
    kpi.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BFBFBF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(kpi)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("지속 추진 계획", H3))
    story.append(Paragraph(
        "사업 종료 후에도 자체 IT예산을 전체 매출의 1.0% 이상으로 편성하여 시스템 고도화를 지속하며, "
        "획득한 데이터 자산을 활용해 <b>고부가가치식품기술개발 R&D</b>의 후속 과제로 연계 신청합니다. "
        "동시에 <b>이노비즈 인증</b> 취득을 추진하여 정책자금 가점·세제혜택을 확보, 투자 회수 사이클을 단축합니다.", BODY))

    story.append(PageBreak())

    # -------- 액션 플랜 + 푸터 --------
    story.append(Paragraph("07. 30일 즉시 실행 플랜", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
    action = Table([
        ["기간", "Action", "담당"],
        ["D+0~3일", "스마트공장 사업 공고문 정독 · 신청서 양식 다운로드", "대표이사"],
        ["D+3~7일", "현황 진단 자료 수집 (생산실적·CCP 점검표·인력현황)", "품질팀"],
        ["D+7~14일", "벤더 사전 미팅 (스마트HACCP 솔루션 3개사 견적)", "생산팀"],
        ["D+14~21일", "사업계획서 초안 작성 (히어컴퍼니 컨설팅 연계 권고)", "대표 + 컨설팅"],
        ["D+21~28일", "내부 검토 · 수정 · 자체부담금 자금 계획 확정", "재무팀"],
        ["D+28~30일", "온라인 신청 · 첨부서류 최종 점검 · 제출", "대표이사"],
    ], colWidths=[26*mm, 110*mm, 34*mm])
    action.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "KR"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("ALIGN", (2, 1), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BFBFBF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(action)
    story.append(Spacer(1, 12*mm))

    # 푸터 박스
    footer = Table([
        [Paragraph("<b>본 리포트는 히어컴퍼니 기업컨설팅이 제공합니다</b>", COVER_BR)],
        [Paragraph("HereCompany Consulting · 정부지원사업 매칭 · 사업계획서 컨설팅 · 인증·정책자금 통합 솔루션", COVER_BR)],
        [Spacer(1, 3*mm)],
        [Paragraph(f"발행일 {datetime.now().strftime('%Y-%m-%d')} · 본 자료는 공개 공고 기반 추정으로 실제 신청 전 공고문 원문을 반드시 확인하십시오.", COVER_BR)],
    ], colWidths=[180*mm])
    footer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(footer)

    doc.build(story)


def main():
    out_dir = "/home/user/-/_workspace/here-company/미르스타푸드"
    os.makedirs(out_dir, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    pdf_path = os.path.join(out_dir, f"미르스타푸드_정부지원사업리포트_{today}.pdf")
    build_pdf(pdf_path)
    print(f"OK: {pdf_path}")
    print(f"Size: {os.path.getsize(pdf_path)} bytes")

if __name__ == "__main__":
    main()
