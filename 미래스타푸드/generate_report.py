#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(주)미래스타푸드 정부지원사업 인포그래픽 리포트 생성기
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
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable

# ---------------------------------------------------------------------------
# 한국어 폰트 등록 (TTF 우선, 실패 시 UnicodeCIDFont 폴백)
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
                return ("ttf", fp)
            except Exception:
                continue
    # 다운로드 시도
    try:
        url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
        dst = "/tmp/NanumGothic.ttf"
        urllib.request.urlretrieve(url, dst)
        pdfmetrics.registerFont(TTFont("KR", dst))
        return ("ttf", dst)
    except Exception:
        # 폴백: reportlab 내장 CID 한글 폰트
        pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
        # alias 'KR' to CID font
        from reportlab.pdfbase.pdfmetrics import registerFontFamily
        # registerFont with same name to alias
        return ("cid", "HYSMyeongJo-Medium")

KR_FONT_KIND, KR_FONT_REF = register_korean_font()
KR_FONT_NAME = "KR" if KR_FONT_KIND == "ttf" else KR_FONT_REF

# matplotlib 한글 폰트
from matplotlib import font_manager as fm
if KR_FONT_KIND == "ttf":
    fm.fontManager.addfont(KR_FONT_REF)
    kr_name = fm.FontProperties(fname=KR_FONT_REF).get_name()
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
GOLD = colors.HexColor("#BF9000")

# ---------------------------------------------------------------------------
# 데이터: 미래스타푸드 매칭 공고 (추정 기반)
# ---------------------------------------------------------------------------
COMPANY = {
    "name": "(주)미래스타푸드",
    "industry": "육가공업 (KSIC C10120 추정)",
    "products": "햄·소시지·분쇄가공육·HMR(추정)",
    "cert": "HACCP 의무 보유 가정 (확인 필요)",
    "size": "중소기업 (가정)",
}

# 카테고리 맵
CATEGORY_MAP = [
    {
        "code": "A",
        "title": "정책자금·운영자금",
        "color": "#1F4E79",
        "items": "중진공·기보·신보·IBK·KDB / 농식품 진흥자금 / 농협 / 지자체",
        "note": "융자·보증 — 자금 에이전트 이관"
    },
    {
        "code": "B",
        "title": "R&D·기술개발",
        "color": "#2E75B6",
        "items": "농기평(IPET) 고부가가치식품 / 산업부 식품바이오 / 중기부 디딤돌·기술혁신 / aT 신상품",
        "note": "비융자 보조금 — 우선 공략"
    },
    {
        "code": "C",
        "title": "수출·해외진출",
        "color": "#00B050",
        "items": "aT K-Food / 코트라 / 농수산식품유통공사 / 중기부 수출바우처",
        "note": "ISO·할랄 등 인증 선결 필요"
    },
    {
        "code": "D",
        "title": "인증·HACCP·식품안전",
        "color": "#FF8C00",
        "items": "식품안전관리인증원 HACCP·스마트HACCP / 식약처 시설개선 / 이노비즈·벤처 / ISO22000",
        "note": "직접 보조금 + 간접 가점 효과"
    },
    {
        "code": "E",
        "title": "스마트공장·디지털·시설",
        "color": "#BF9000",
        "items": "중기부 스마트공장 식품제조 특화 / 농식품부 스마트팩토리 / 산업부 DX / 지자체 식품가공단지",
        "note": "HACCP과 직결 — 시너지 큼"
    },
]

ANNOUNCEMENTS = [
    {
        "no": "①",
        "title": "고부가가치식품기술개발 R&D",
        "source": "농림축산식품부 / 농기평(IPET)",
        "deadline": "연 1~2회 공모 (4~6월 추정)",
        "budget": "과제당 3~7억원 (2~3년)",
        "fit": "상",
        "category": "R&D",
        "summary": "미래대응식품·식품 품질안전 분야 R&D. 식육 신제품·공정혁신·발효육·고령친화 식육 적합.",
        "difficulty": 4.5,
        "effect": 5.0,
        "size_num": 500,
        "start_day": 10,
        "duration": 60,
    },
    {
        "no": "②",
        "title": "식품 특화 스마트공장 보급",
        "source": "중기부·식약처·삼성전자",
        "deadline": "상·하반기 분할 모집",
        "budget": "고도화1: 1억 / 고도화2: 최대 2~4억",
        "fit": "상",
        "category": "시설/DX",
        "summary": "HACCP 보유 식품기업 우대. 스마트HACCP·MES 도입으로 CCP 자동화·로트추적성 확보.",
        "difficulty": 2.8,
        "effect": 4.5,
        "size_num": 250,
        "start_day": 0,
        "duration": 45,
    },
    {
        "no": "③",
        "title": "HACCP 고도화·스마트HACCP 지원",
        "source": "식품안전관리인증원",
        "deadline": "상시 (예산 소진 시까지)",
        "budget": "컨설팅·심사비 + 시설 3천만~1억",
        "fit": "상",
        "category": "인증",
        "summary": "HACCP 운영 식품기업 대상 디지털화 지원. 스마트공장과 연동 시 시너지 극대화.",
        "difficulty": 1.8,
        "effect": 3.5,
        "size_num": 80,
        "start_day": 0,
        "duration": 200,
    },
    {
        "no": "④",
        "title": "aT 농식품 수출 지원",
        "source": "한국농수산식품유통공사",
        "deadline": "연중 분기별 공모",
        "budget": "수출물류비·해외마케팅·박람회 지원",
        "fit": "중",
        "category": "수출",
        "summary": "K-Food 글로벌 진출. 식육 가공품 ISO·할랄 선결 필요. K-바비큐·스낵 라인 시장 확대.",
        "difficulty": 3.0,
        "effect": 4.0,
        "size_num": 150,
        "start_day": 30,
        "duration": 60,
    },
    {
        "no": "⑤",
        "title": "창업성장기술개발·기술혁신개발",
        "source": "중기부 / TIPA",
        "deadline": "연 2~3회 공모",
        "budget": "디딤돌 1.2억 / 기술혁신 6억 (1~3년)",
        "fit": "중",
        "category": "R&D",
        "summary": "업력별 트랙(창업 7년 vs 일반). 농기평 R&D와 중복 지원 제한 확인 필요.",
        "difficulty": 3.8,
        "effect": 4.0,
        "size_num": 200,
        "start_day": 15,
        "duration": 45,
    },
    {
        "no": "⑥",
        "title": "이노비즈 인증 + 벤처기업 확인",
        "source": "이노비즈협회·기보·중기부",
        "deadline": "상시 (평가형)",
        "budget": "직접 자금 X — 세제·정책자금 가점·보증료 우대",
        "fit": "중",
        "category": "인증",
        "summary": "정책자금 가점·세액공제 50%·보증료 0.5%p 우대. 다른 공고 ROI를 1.3~1.5배 증대.",
        "difficulty": 2.8,
        "effect": 3.5,
        "size_num": 60,
        "start_day": 20,
        "duration": 90,
    },
    {
        "no": "⑦",
        "title": "중진공 신성장기반자금 융자",
        "source": "중소벤처기업진흥공단",
        "deadline": "연중 (예산 소진 시)",
        "budget": "시설 60억 / 운전 5억 한도 (저금리)",
        "fit": "중",
        "category": "정책자금(융자)",
        "summary": "융자 성격 — 자금 에이전트 이관 권고. 시설 투자 임박 시 동시 신청 검토.",
        "difficulty": 3.2,
        "effect": 3.5,
        "size_num": 600,
        "start_day": 30,
        "duration": 90,
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

    short_labels = ["고부가 R&D", "스마트공장(식품)", "HACCP 고도화",
                    "aT 수출", "중기부 R&D", "이노비즈/벤처", "중진공 융자"]
    for a, lab in zip(ANNOUNCEMENTS, short_labels):
        ax.annotate(lab,
                    (a["difficulty"], a["effect"]),
                    xytext=(10, 8), textcoords="offset points",
                    fontsize=9, color="#1F4E79", fontweight="bold")

    ax.axhline(3.0, color="#BFBFBF", linestyle="--", linewidth=0.8)
    ax.axvline(3.0, color="#BFBFBF", linestyle="--", linewidth=0.8)
    ax.set_xlim(0.5, 5.2)
    ax.set_ylim(2, 5.5)
    ax.set_xlabel("신청 난이도 (낮음 ← → 높음)", fontsize=11, color="#1F4E79", fontweight="bold")
    ax.set_ylabel("기대 효과 (낮음 ← → 높음)", fontsize=11, color="#1F4E79", fontweight="bold")
    ax.set_title("미래스타푸드 우선순위 매트릭스 (버블 = 지원 규모)",
                 fontsize=13, color="#1F4E79", fontweight="bold", pad=12)
    ax.grid(True, alpha=0.2)
    for spine in ax.spines.values():
        spine.set_color("#BFBFBF")

    ax.text(1.0, 5.25, "Quick Win", fontsize=10, color="#00B050", fontweight="bold")
    ax.text(4.2, 5.25, "전략과제", fontsize=10, color="#1F4E79", fontweight="bold")
    ax.text(1.0, 2.15, "기본 정비", fontsize=10, color="#595959")
    ax.text(4.2, 2.15, "재검토", fontsize=10, color="#C00000")

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
    titles = ["고부가 R&D", "스마트공장(식품)", "HACCP 고도화",
              "aT 수출", "중기부 R&D", "이노비즈/벤처", "중진공 융자"]
    y_pos = np.arange(len(ANNOUNCEMENTS))

    for i, a in enumerate(ANNOUNCEMENTS):
        ax.barh(i, a["duration"], left=a["start_day"],
                color=color_map[a["fit"]], alpha=0.75,
                edgecolor="#1F4E79", linewidth=1)
        ax.text(a["start_day"] + a["duration"] + 3, i,
                a["deadline"], va="center", fontsize=8.5, color="#1F4E79")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(titles, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("오늘로부터 경과일 (단위: 일)  ※ 추정 일정", fontsize=11, color="#1F4E79", fontweight="bold")
    ax.set_title("신청 준비~마감 타임라인 (2026-05-07 기준 추정)",
                 fontsize=13, color="#1F4E79", fontweight="bold", pad=12)
    ax.grid(True, alpha=0.2, axis="x")
    ax.set_xlim(0, 280)
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
def _on_page(canvas, doc):
    """헤더·푸터 그리기"""
    canvas.saveState()
    # 헤더 라인
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(0.5)
    canvas.line(15*mm, A4[1] - 12*mm, A4[0] - 15*mm, A4[1] - 12*mm)
    # 헤더 텍스트
    canvas.setFont(KR_FONT_NAME, 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(15*mm, A4[1] - 10*mm, "(주)미래스타푸드 — 정부지원사업 매칭 리포트")
    canvas.drawRightString(A4[0] - 15*mm, A4[1] - 10*mm, "히어컴퍼니 기업컨설팅 제공")
    # 푸터 라인
    canvas.line(15*mm, 12*mm, A4[0] - 15*mm, 12*mm)
    canvas.setFillColor(GRAY)
    canvas.setFont(KR_FONT_NAME, 8)
    canvas.drawString(15*mm, 8*mm, f"발행일 {datetime.now().strftime('%Y-%m-%d')}  ·  추정 기반 — 실제 신청 전 공고문 원문 재확인 필수")
    canvas.drawRightString(A4[0] - 15*mm, 8*mm, f"- {doc.page} -")
    canvas.restoreState()

def build_pdf(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title="(주)미래스타푸드 정부지원사업 리포트",
        author="히어컴퍼니 기업컨설팅",
    )

    styles = getSampleStyleSheet()
    H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName=KR_FONT_NAME,
                        fontSize=20, textColor=NAVY, spaceAfter=10, leading=26)
    H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName=KR_FONT_NAME,
                        fontSize=14, textColor=NAVY, spaceBefore=10, spaceAfter=8, leading=20)
    H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName=KR_FONT_NAME,
                        fontSize=11, textColor=BLUE, spaceBefore=6, spaceAfter=4, leading=16)
    BODY = ParagraphStyle("BODY", parent=styles["BodyText"], fontName=KR_FONT_NAME,
                          fontSize=10, textColor=colors.black, leading=15)
    SMALL = ParagraphStyle("SMALL", parent=styles["BodyText"], fontName=KR_FONT_NAME,
                           fontSize=8.5, textColor=GRAY, leading=12)
    COVER_TITLE = ParagraphStyle("COVERT", parent=styles["Title"], fontName=KR_FONT_NAME,
                                 fontSize=30, textColor=colors.white, alignment=TA_CENTER, leading=40)
    COVER_SUB = ParagraphStyle("COVERS", parent=styles["Title"], fontName=KR_FONT_NAME,
                               fontSize=16, textColor=LIGHT_BLUE, alignment=TA_CENTER, leading=24)
    COVER_BR = ParagraphStyle("COVERB", parent=styles["BodyText"], fontName=KR_FONT_NAME,
                              fontSize=11, textColor=colors.white, alignment=TA_CENTER, leading=16)
    CARD_CAT = ParagraphStyle("CCAT", fontName=KR_FONT_NAME, fontSize=9, textColor=colors.white, alignment=TA_CENTER, leading=11)
    CARD_TITLE = ParagraphStyle("CTITLE", fontName=KR_FONT_NAME, fontSize=10, textColor=NAVY, leading=14)
    CARD_FIT = ParagraphStyle("CFIT", fontName=KR_FONT_NAME, fontSize=10, textColor=colors.white, alignment=TA_CENTER, leading=12)

    story = []

    # ====================================================================
    # 표지
    # ====================================================================
    cover_tbl = Table(
        [
            [Spacer(1, 50*mm)],
            [Paragraph("정부지원사업<br/>매칭 리포트", COVER_TITLE)],
            [Spacer(1, 14*mm)],
            [Paragraph("(주)미래스타푸드", COVER_SUB)],
            [Spacer(1, 6*mm)],
            [Paragraph("육가공업 (KSIC C10120 추정) · HACCP 보유 가정", COVER_BR)],
            [Spacer(1, 70*mm)],
            [Paragraph(f"발행일 : {datetime.now().strftime('%Y년 %m월 %d일')}", COVER_BR)],
            [Spacer(1, 6*mm)],
            [Paragraph("Powered by <b>히어컴퍼니 기업컨설팅</b>", COVER_BR)],
            [Paragraph("HereCompany Consulting", COVER_BR)],
            [Spacer(1, 4*mm)],
            [Paragraph("본 자료는 공개정보 기반 추정 매칭 — 실제 신청 전 공고문 원문 재확인 필수", COVER_BR)],
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

    # ====================================================================
    # 01. 헤드라인 요약 + Top 3 카드
    # ====================================================================
    story.append(Paragraph("01. 헤드라인 요약 — 추천 Top 3", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))

    top3 = ANNOUNCEMENTS[:3]
    fit_color = {"상": GREEN, "중": ORANGE, "하": RED}
    cards = []
    for a in top3:
        card = Table([
            [Paragraph(f'<b>{a["category"]}</b>', CARD_CAT)],
            [Paragraph(f'<b>{a["no"]} {a["title"]}</b>', CARD_TITLE)],
            [Paragraph(f'출처 : {a["source"]}', SMALL)],
            [Paragraph(f'<b>지원 규모</b>  {a["budget"]}', BODY)],
            [Paragraph(f'<b>마감</b>  {a["deadline"]}', BODY)],
            [Paragraph(f'적합도 <b>{a["fit"]}</b>', CARD_FIT)],
        ], colWidths=[55*mm], rowHeights=[8*mm, 22*mm, 7*mm, 11*mm, 11*mm, 8*mm])
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
        "(주)미래스타푸드는 육가공(C10120 추정) 분야 중소기업으로, HACCP 의무 업종 특성에 맞춰 "
        "<b>① 농기평 고부가가치식품 R&D + ② 식품 특화 스마트공장 + ③ HACCP 고도화 지원</b> "
        "3개 공고를 우선 공략하는 것이 효율적입니다. 셋은 단순 병렬이 아니라 "
        "<b>HACCP 고도화 → 스마트공장 → R&D 데이터 기반 신제품</b>의 연쇄 시너지가 성립합니다. "
        "단, 공고 일정·금액·자격은 매년 변경되므로 신청 직전 원문 확인이 필수입니다.",
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

    # ====================================================================
    # 02. 기업 프로파일
    # ====================================================================
    story.append(Paragraph("02. 기업 프로파일 (추정)", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))

    prof_data = [
        ["기업명", COMPANY["name"], "업종", COMPANY["industry"]],
        ["주요 제품(추정)", COMPANY["products"], "보유 인증", COMPANY["cert"]],
        ["기업 규모", COMPANY["size"], "리포트 일자", datetime.now().strftime("%Y-%m-%d")],
        ["관심 분야", "정책자금 · 인증 · R&D · 수출 · 스마트공장", "", ""],
    ]
    prof = Table(prof_data, colWidths=[28*mm, 62*mm, 28*mm, 62*mm])
    prof.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), KR_FONT_NAME),
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
    story.append(Spacer(1, 6*mm))

    # 미입력 항목 경고
    warn = Table([[Paragraph(
        "<b>주의 — 미입력 항목</b>  매출·임직원 수·업력·정확한 제품군·보유 인증·자금 needs 등 "
        "핵심 정보가 미입력 상태입니다. 본 리포트는 업계 평균 가설로 작성되었으며, "
        "실제 컨설팅에서는 인터뷰 후 정밀 매칭 버전으로 갱신됩니다.",
        BODY)]], colWidths=[180*mm])
    warn.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF4E5")),
        ("BOX", (0, 0), (-1, -1), 0.6, ORANGE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(warn)
    story.append(Spacer(1, 6*mm))

    # 강점·기회·리스크
    strength = Table([
        [Paragraph("<b>강점 (추정)</b>", H3),
         Paragraph("<b>기회</b>", H3),
         Paragraph("<b>리스크</b>", H3)],
        [Paragraph("· HACCP 의무 운영 경험<br/>· 식육 가공 전문성<br/>· 우선지원대상 가능성", BODY),
         Paragraph("· 식품 특화 스마트공장<br/>· 농기평 고부가 R&D<br/>· K-Food 수출 확대", BODY),
         Paragraph("· R&D 사업계획서 부담<br/>· 자체부담금 25~50%<br/>· 중복지원 제한 점검", BODY)],
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

    # ====================================================================
    # 03. 카테고리 맵
    # ====================================================================
    story.append(Paragraph("03. 육가공업 정부지원사업 카테고리 맵", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
    story.append(Paragraph(
        "식육가공업(C10120 추정)에 적용 가능한 정부지원사업을 5개 영역으로 정리합니다. "
        "각 영역의 주관기관·핵심 사업·전략 포인트를 한눈에 파악하실 수 있습니다.", BODY))
    story.append(Spacer(1, 4*mm))

    map_rows = [["코드", "영역", "주관기관·핵심 사업", "전략 포인트"]]
    for c in CATEGORY_MAP:
        map_rows.append([
            c["code"],
            Paragraph(f'<b>{c["title"]}</b>', BODY),
            Paragraph(c["items"], BODY),
            Paragraph(c["note"], BODY),
        ])
    cat_tbl = Table(map_rows, colWidths=[12*mm, 38*mm, 80*mm, 50*mm])
    style = [
        ("FONTNAME", (0, 0), (-1, -1), KR_FONT_NAME),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BFBFBF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]
    # 코드 셀에 카테고리 컬러
    for i, c in enumerate(CATEGORY_MAP, 1):
        style.append(("BACKGROUND", (0, i), (0, i), colors.HexColor(c["color"])))
        style.append(("TEXTCOLOR", (0, i), (0, i), colors.white))
        style.append(("FONTSIZE", (0, i), (0, i), 12))
    cat_tbl.setStyle(TableStyle(style))
    story.append(cat_tbl)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "주: A 영역(융자·보증)은 자금 에이전트로 별도 이관, "
        "본 리포트의 메인은 B~E 영역의 비융자 보조금·인증·시설 지원입니다.", SMALL))
    story.append(PageBreak())

    # ====================================================================
    # 04. 매칭 공고 종합표
    # ====================================================================
    story.append(Paragraph("04. 추천 매칭 공고 7개", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))

    header = ["#", "공고명", "출처", "지원 규모", "마감(추정)", "적합도"]
    rows = [header]
    for a in ANNOUNCEMENTS:
        rows.append([
            a["no"],
            Paragraph(a["title"], ParagraphStyle("p", fontName=KR_FONT_NAME, fontSize=8.5, leading=11)),
            Paragraph(a["source"], ParagraphStyle("p", fontName=KR_FONT_NAME, fontSize=8, leading=10)),
            Paragraph(a["budget"], ParagraphStyle("p", fontName=KR_FONT_NAME, fontSize=8.5, leading=11)),
            Paragraph(a["deadline"], ParagraphStyle("p", fontName=KR_FONT_NAME, fontSize=8.5, leading=11)),
            a["fit"],
        ])
    tbl = Table(rows, colWidths=[8*mm, 50*mm, 35*mm, 38*mm, 31*mm, 14*mm])
    style = [
        ("FONTNAME", (0, 0), (-1, -1), KR_FONT_NAME),
        ("FONTSIZE", (0, 0), (-1, 0), 9.5),
        ("FONTSIZE", (0, 1), (-1, -1), 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("ALIGN", (-1, 1), (-1, -1), "CENTER"),
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
        "주: 모든 금액·일정은 작년 기준 추정. ⑦번 정책자금 융자는 자금 에이전트 이관 권고. "
        "예상 수혜 금액은 평균 선정 규모 기준 보수적 추정치.", SMALL))
    story.append(Spacer(1, 5*mm))

    # 공고 요약 카드 (4~7번)
    story.append(Paragraph("공고별 요약 메모", H3))
    for a in ANNOUNCEMENTS:
        memo = Table([[Paragraph(
            f'<b>{a["no"]} {a["title"]}</b>  ({a["category"]})  <font color="#595959">— {a["source"]}</font><br/>'
            f'{a["summary"]}',
            BODY)]], colWidths=[180*mm])
        memo.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
            ("BOX", (0, 0), (-1, -1), 0.3, GRAY),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(memo)
        story.append(Spacer(1, 2*mm))
    story.append(PageBreak())

    # ====================================================================
    # 05. 우선순위 매트릭스
    # ====================================================================
    story.append(Paragraph("05. 우선순위 매트릭스", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
    story.append(Paragraph(
        "X축은 신청 난이도, Y축은 기대 효과, 버블 크기는 지원 규모를 의미합니다. "
        "<b>우상단(전략과제)</b>의 고부가 R&D는 사업계획서 부담이 크지만 임팩트가 가장 큽니다. "
        "<b>중상단(Quick Win)</b>의 스마트공장·HACCP 고도화를 먼저 잡고 그 데이터를 R&D로 연결하는 "
        "포트폴리오가 효율적입니다.", BODY))
    story.append(Spacer(1, 4*mm))
    story.append(RLImage(make_priority_matrix(), width=180*mm, height=110*mm))
    story.append(PageBreak())

    # ====================================================================
    # 06. 신청 타임라인
    # ====================================================================
    story.append(Paragraph("06. 신청 타임라인", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
    story.append(Paragraph(
        "오늘(2026-05-07) 기준 각 공고의 준비~마감 추정 구간을 시각화했습니다. "
        "<b>HACCP 고도화·스마트공장은 즉시 착수</b>가 가능하며, "
        "<b>고부가 R&D는 10일 후부터 60일간 집중 준비</b>해야 마감 대응이 가능합니다.", BODY))
    story.append(Spacer(1, 4*mm))
    story.append(RLImage(make_timeline(), width=180*mm, height=100*mm))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("※ 일정은 작년 공고 패턴 기반 추정. 실제 공고 확정 시 재배치 필요.", SMALL))
    story.append(PageBreak())

    # ====================================================================
    # 07. 시너지 패키지 전략
    # ====================================================================
    story.append(Paragraph("07. 육가공업 특화 시너지 전략", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
    story.append(Paragraph(
        "공고를 따로따로 신청하지 않고 <b>3개 패키지</b>로 묶어서 연쇄 효과를 만드는 것이 핵심입니다.",
        BODY))
    story.append(Spacer(1, 4*mm))

    # 패키지 A
    pa_data = [
        ["패키지 A", "시설 현대화 패키지 (3단계 연쇄)"],
        ["1단계", "HACCP 고도화·스마트HACCP 컨설팅 (식품안전관리인증원)"],
        ["2단계", "식품 특화 스마트공장 보급 (중기부·식약처)"],
        ["3단계", "고부가가치식품 R&D — 데이터 기반 신제품 (농기평)"],
        ["누적 수혜", "보조금 합산 약 3~7억원 + 정책자금 가점·세제혜택 (보수적 추정)"],
    ]
    pa = Table(pa_data, colWidths=[26*mm, 154*mm])
    pa.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), KR_FONT_NAME),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("BACKGROUND", (0, 1), (0, -1), LIGHT_BLUE),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#FFF4E5")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BFBFBF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(pa)
    story.append(Spacer(1, 5*mm))

    # 패키지 B
    pb_data = [
        ["패키지 B", "수출 확장 패키지"],
        ["1단계", "HACCP + ISO22000 / FSSC22000 국제 인증 취득"],
        ["2단계", "aT 수출 + 코트라·중기부 수출바우처 (중복 가능 여부 확인)"],
        ["3단계", "K-Food 박람회·해외 안테나숍 입점 → B2B 거래 확보"],
        ["기대 효과", "내수 의존도 축소, 매출 다각화, 18~24개월 단위 로드맵"],
    ]
    pb = Table(pb_data, colWidths=[26*mm, 154*mm])
    pb.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), KR_FONT_NAME),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#E2F0DC")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#FFF4E5")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BFBFBF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(pb)
    story.append(Spacer(1, 5*mm))

    # 패키지 C
    pc_data = [
        ["패키지 C", "인증 포트폴리오로 ROI 극대화"],
        ["기반", "HACCP (이미 보유 가정)"],
        ["추가", "이노비즈 → 벤처기업 확인 → 기업부설연구소 설립"],
        ["시너지", "정책자금 가점 / 세액공제 50% / 보증료 0.5%p 우대 / 인력 채용 우대"],
        ["기대 효과", "직접 자금 X, 다른 모든 공고의 ROI를 1.3~1.5배 증대"],
    ]
    pc = Table(pc_data, colWidths=[26*mm, 154*mm])
    pc.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), KR_FONT_NAME),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), ORANGE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#FCE7CC")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#FFF4E5")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BFBFBF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(pc)
    story.append(PageBreak())

    # ====================================================================
    # 08. 추가 정보 요청 + 다음 액션
    # ====================================================================
    story.append(Paragraph("08. 추가 확인 필요 정보 — 사용자 답변 요청", H1))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
    story.append(Paragraph(
        "본 리포트의 정밀도를 60% → 90%로 끌어올리기 위해 다음 정보가 필요합니다.", BODY))
    story.append(Spacer(1, 3*mm))

    info_rows = [
        ["#", "확인 필요 항목", "영향"],
        ["1", "매출 규모 (최근 3개년)·임직원 수·업력",
         "정책자금 한도, 창업기업 R&D 트랙 분기, 우선지원 대상 확정"],
        ["2", "주력 제품군과 주요 거래처 (B2B/B2C)",
         "수출·R&D·신제품 매칭의 정밀도 결정"],
        ["3", "보유 인증 현황 (HACCP·ISO22000·할랄·벤처·이노비즈 등)",
         "인증 패키지 진입 단계 결정"],
        ["4", "자금 needs 우선순위 (시설 / 운영 / R&D / 수출 / 인증)",
         "7개 공고의 1~3순위 재배치"],
        ["5", "신청 목표 시점 (3개월 / 6개월 / 1년 계획)",
         "마감 임박 vs 상시 공고 우선순위 결정"],
        ["6 (선택)", "기존 정부지원 이력",
         "동일 사업 중복 지원 제한 점검"],
        ["7 (선택)", "소재지 (시·도 단위)",
         "지자체 공고 추가 매칭"],
    ]
    info_tbl = Table(info_rows, colWidths=[18*mm, 76*mm, 86*mm])
    info_tbl.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), KR_FONT_NAME),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BFBFBF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(info_tbl)
    story.append(Spacer(1, 8*mm))

    # 다음 액션
    story.append(Paragraph("다음 액션 — 5단계 즉시 실행 플랜", H2))
    action = Table([
        ["기간", "Action", "담당"],
        ["즉시", "위 5가지 정보 회신 → 정밀 매칭 버전으로 업데이트", "대표·실무"],
        ["1주 내", "농기평 ATIS / smart-factory.kr / haccp.or.kr 공고 모니터링 등록", "대표·기획"],
        ["2주 내", "HACCP 고도화 사전 진단 신청 (가장 진입장벽 낮음)", "품질팀"],
        ["1개월 내", "사업계획서 컨설팅 착수 (스마트공장 또는 R&D 1순위 선택)", "대표 + 컨설팅"],
        ["3개월 내", "이노비즈·벤처 자가진단 → 미달 영역 보완 계획 수립", "대표 + 컨설팅"],
    ], colWidths=[26*mm, 110*mm, 34*mm])
    action.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), KR_FONT_NAME),
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
        [Paragraph(
            f"발행일 {datetime.now().strftime('%Y-%m-%d')} · 본 자료는 공개 공고 기반 추정으로 "
            f"실제 신청 전 공고문 원문을 반드시 확인하십시오.", COVER_BR)],
    ], colWidths=[180*mm])
    footer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(footer)

    doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=_on_page)


def main():
    out_dir = "/home/user/-/미래스타푸드"
    os.makedirs(out_dir, exist_ok=True)
    # 사용자 지정 파일명: 20260504
    pdf_path = os.path.join(out_dir, "(주)미래스타푸드_정부지원사업리포트_20260504.pdf")
    build_pdf(pdf_path)
    print(f"OK: {pdf_path}")
    print(f"Size: {os.path.getsize(pdf_path)} bytes")


if __name__ == "__main__":
    main()
