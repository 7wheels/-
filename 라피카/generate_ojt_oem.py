"""
(주)라피카 — 화장품 OEM 생산관리 및 생산성 향상 실무 과정 (S-OJT)
5일 × 8시간 집중형 (총 40시간) 훈련계획서 PDF 생성
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
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
BLUE  = colors.HexColor('#2E6DB4')
LBLUE = colors.HexColor('#A8C8E8')
LGRAY = colors.HexColor('#F5F7FA')
GRAY  = colors.HexColor('#888888')
GREEN = colors.HexColor('#1E8449')
ORANGE= colors.HexColor('#D35400')
WHITE = colors.white

W, H = A4
M = 18 * mm
COMPANY = '(주)라피카'
TITLE   = '화장품 OEM 생산관리 및 생산성 향상 실무 과정 (S-OJT)'
SUBTITLE= '5일 × 8시간 집중형 (총 40시간) — 사무실 기반 실습 — 2026년 재직자 직무능력향상훈련'

# ── 페이지 헤더/푸터 ──────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(KR, 7.5)
    canvas.setFillColor(NAVY)
    canvas.drawString(M, H - 10*mm, COMPANY)
    w = canvas.stringWidth(COMPANY, KR, 7.5)
    canvas.setFillColor(BLUE)
    canvas.drawString(M + w, H - 10*mm, '  |  히어컴퍼니 기업컨설팅 제공')
    canvas.setStrokeColor(LBLUE)
    canvas.setLineWidth(0.6)
    canvas.line(M, H - 11.5*mm, W - M, H - 11.5*mm)
    canvas.setFont(KR, 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, 8*mm, f'{doc.page}')
    canvas.restoreState()

# ── 스타일 헬퍼 ───────────────────────────────────────────────────────
def ps(font, size, color=colors.black, **kw):
    kw.setdefault('leading', size * 1.5)
    return ParagraphStyle('_', fontName=font, fontSize=size,
                          textColor=color, **kw)

def sp(n=1):
    return Spacer(1, n * 4 * mm)

def sec(text):
    """진한 파란 배경 섹션 헤더"""
    style = ps(KRB, 12, WHITE, leftIndent=6, spaceAfter=0)
    return Table([[Paragraph(text, style)]],
                 colWidths=[W - 2*M],
                 style=TableStyle([
                     ('BACKGROUND',    (0,0), (-1,-1), NAVY),
                     ('TOPPADDING',    (0,0), (-1,-1), 7),
                     ('BOTTOMPADDING', (0,0), (-1,-1), 7),
                     ('LEFTPADDING',   (0,0), (-1,-1), 10),
                 ]))

def subsec(text, color=BLUE):
    """소섹션 헤더 (색 라벨)"""
    style = ps(KRB, 10.5, color, spaceAfter=0)
    return Table([[Paragraph(text, style)]],
                 colWidths=[W - 2*M],
                 style=TableStyle([
                     ('LEFTPADDING',   (0,0), (-1,-1), 0),
                     ('TOPPADDING',    (0,0), (-1,-1), 4),
                     ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                     ('LINEBELOW',     (0,0), (-1,-1), 0.6, color),
                 ]))

def tbl(headers, rows, widths=None, header_color=NAVY, font_size=8.5):
    """데이터 표"""
    if not widths:
        widths = [(W - 2*M) / len(headers)] * len(headers)
    th = ps(KRB, font_size, WHITE, leading=font_size*1.5, alignment=1)
    td = ps(KR,  font_size, colors.black, leading=font_size*1.5)
    cells = [[Paragraph(str(h), th) for h in headers]]
    for row in rows:
        cells.append([Paragraph(str(c), td) for c in row])
    style = TableStyle([
        ('BACKGROUND',     (0,0), (-1,0),  header_color),
        ('GRID',           (0,0), (-1,-1), 0.4, GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
        ('VALIGN',         (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',    (0,0), (-1,-1), 5),
        ('RIGHTPADDING',   (0,0), (-1,-1), 5),
        ('TOPPADDING',     (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',  (0,0), (-1,-1), 4),
    ])
    return Table(cells, colWidths=widths, repeatRows=1, style=style)

def para(text, size=9.5, font=KR, color=colors.black, **kw):
    return Paragraph(text, ps(font, size, color, **kw))

def bullet(items, size=9.5):
    style = ps(KR, size, colors.black, leftIndent=10, bulletIndent=2,
               leading=size*1.6)
    return [Paragraph(f'• {t}', style) for t in items]

# ── 본문 빌드 ─────────────────────────────────────────────────────────
def build():
    out = Path(__file__).parent / '라피카_S-OJT_훈련계획서_OEM생산관리.pdf'
    doc = SimpleDocTemplate(
        str(out), pagesize=A4,
        leftMargin=M, rightMargin=M,
        topMargin=18*mm, bottomMargin=14*mm,
        title='라피카 S-OJT 훈련계획서 — OEM 생산관리',
        author='히어컴퍼니 기업컨설팅',
    )
    s = []

    # ── 표지 ───────────────────────────────────────────────────────
    s.append(Spacer(1, 25*mm))
    s.append(para('히어컴퍼니 기업컨설팅', 11, KRB, BLUE, alignment=1))
    s.append(sp(0.5))
    s.append(HRFlowable(width=80*mm, thickness=1.2, color=BLUE,
                        hAlign='CENTER'))
    s.append(sp(2.5))
    s.append(para('S-OJT 훈련계획서', 24, KRB, NAVY, alignment=1, leading=30))
    s.append(sp(2))
    s.append(para(TITLE, 15, KRB, colors.black, alignment=1, leading=22))
    s.append(sp(2))
    s.append(para(SUBTITLE, 11, KR, GRAY, alignment=1))
    s.append(sp(6))
    info_widths = [40*mm, 130*mm]
    s.append(Table([
        [Paragraph('<b>훈련기관</b>', ps(KRB, 10, NAVY)),
         Paragraph(COMPANY + '  (화장품 OEM 제조)', ps(KR, 10, colors.black))],
        [Paragraph('<b>총 훈련시간</b>', ps(KRB, 10, NAVY)),
         Paragraph('40시간 (이론 16h : 실습 24h = 40 : 60)',
                   ps(KR, 10, colors.black))],
        [Paragraph('<b>운영 방식</b>', ps(KRB, 10, NAVY)),
         Paragraph('5일 × 8시간 집중형 (월~금 1주 완성)',
                   ps(KR, 10, colors.black))],
        [Paragraph('<b>대상</b>', ps(KRB, 10, NAVY)),
         Paragraph('라피카 생산관리·공정관리 담당자 (협력공장 관리자 포함 가능)',
                   ps(KR, 10, colors.black))],
        [Paragraph('<b>작성일</b>', ps(KRB, 10, NAVY)),
         Paragraph(datetime.date.today().strftime('%Y년 %m월 %d일'),
                   ps(KR, 10, colors.black))],
    ], colWidths=info_widths, style=TableStyle([
        ('GRID', (0,0), (-1,-1), 0.4, LBLUE),
        ('BACKGROUND', (0,0), (0,-1), LGRAY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ])))
    s.append(PageBreak())

    # ── 1. 과정 개요 ────────────────────────────────────────────────
    s.append(sec('1. 과정 개요'))
    s.append(sp(1))
    s.append(subsec('1.1 기본 정보'))
    s.append(sp(0.5))
    s.append(tbl(
        ['항목', '내용'],
        [
            ['과정명', '화장품 OEM 생산관리 및 생산성 향상 실무 과정 (S-OJT)'],
            ['훈련 형태', '사업주 직업능력개발훈련 — 자체훈련(S-OJT)'],
            ['총 훈련시간', '<b>40시간 (이론 16h : 실습 24h = 40:60)</b>'],
            ['운영 방식', '<b>5일 × 8시간 집중형 (월~금 1주 완성)</b>'],
            ['훈련 대상', '라피카 생산관리·공정관리 담당자 (협력공장 관리자 포함 가능)'],
            ['훈련 장소', '<b>(주)라피카 자사 사업장 회의실 (사무실 기반)</b>'],
            ['훈련 방법', '<b>사무실 기반 S-OJT</b> — 사전 녹화 작업영상 분석 / 과거 실측 데이터·표본 자료 분석 / 양식 작성 실습 / 사례 토의·피드백 + 부분 집체이론'],
        ],
        widths=[35*mm, W - 2*M - 35*mm]))
    s.append(sp(2))

    s.append(subsec('1.2 훈련 목표 (정량 KPI 포함)'))
    s.append(sp(0.5))
    s.append(para('훈련 종료 시점에 훈련생은 다음을 수행할 수 있다.', 9.5))
    s.append(sp(0.5))
    s.extend(bullet([
        '수주 정보(품목·수량·납기)를 기반으로 <b>월간 기준생산계획(MPS)을 1시간 이내</b>에 작성하고, 자사·협력공장 라인 부하를 ±10% 오차 이내로 산출할 수 있다.',
        '사전 녹화된 충진·포장 작업 영상을 분석하여 <b>공정별 사이클타임을 분 단위 소수점 1자리</b>까지 산출하고, 라인 밸런싱 효율을 % 단위로 계산할 수 있다.',
        '표본 생산 데이터를 활용하여 일일 생산일보를 작성하고 <b>계획 대비 실적률·불량률·시간당 생산량(UPH)</b> 3대 KPI를 정확히 산출할 수 있다.',
        '<b>Excel/Google Sheets 기반 KPI 대시보드를 직접 구축</b>하고 일별·주별 추이를 시각화하여 이상치를 식별할 수 있다.',
        '개선 전·후 KPI 비교 분석을 통해 <b>생산성 향상률(%)·불량률 감소(%)·납기준수율(%)</b> 변화를 정량 보고서로 작성하고 발표할 수 있다.',
    ]))
    s.append(PageBreak())

    # ── 2. 단원별 상세 ─────────────────────────────────────────────
    s.append(sec('2. 단원별 상세 (5단원 × 8시간 = 40시간)'))
    s.append(sp(1))

    units = [
        {
            'no': 1,
            'day': 'Day 1 (월요일) — 09:00~18:00',
            'title': '수주 기반 생산계획(MPS) 수립 및 협력공장 일정 조율',
            'time': '8h: 이론 3.5h + 실습 4.5h',
            'goals': [
                '수주 정보(품목·수량·납기·고객사)를 분석하여 월간 기준생산계획(MPS)을 1시간 이내 작성할 수 있다.',
                '자사·협력공장 capacity를 합산하여 부하율을 산출하고 ±10% 오차 이내로 일정을 배분할 수 있다.',
                '협력공장에 발주서·납기관리표를 표준 양식으로 발행하고 변경 사유를 기록할 수 있다.',
            ],
            'rows': [
                ['1-1', '화장품 OEM 수주 흐름과 다품종 소량생산 특성', '1.0', '0', '수주서·BOM·처방코드·로트관리 / 다품종 소량 OEM 특성'],
                ['1-2', 'MPS 개념·구성요소·작성 절차', '1.5', '0', '수요예측·가용재고·ATP·라인 capacity·납기 계산식'],
                ['1-3', '수주서 표본 분석 → 월간 MPS 작성 실습', '0', '2.0', '사전 제공 표본 수주서 5건으로 MPS 시트 작성'],
                ['1-4', '자사 vs 협력공장 부하 분배 실습', '0', '1.5', '사전 측정된 capacity 자료(자사·외주)로 부하 분배'],
                ['1-5', '협력공장 발주서·납기관리표 작성', '1.0', '1.0', '발주번호·로트·납기일·검수기준 양식'],
                ['<b>합계</b>', '', '<b>3.5</b>', '<b>4.5</b>', '<b>8.0</b>'],
            ],
            'practice': [
                '사전 제공 표본 수주서 5건(라피카 과거 실수주 가공·개인정보 마스킹)으로 월간 MPS 시트 작성',
                '사전 측정·정리된 자사 라인 capacity 자료와 협력공장 capacity 자료를 활용해 부하 분배 시뮬레이션',
                '협력공장 2개사(가명 A사·B사)에 대한 발주서·납기관리표를 Excel 템플릿으로 작성',
                '페이퍼 케이스: 일정 변경 1건 발생 가정 → 변경관리대장 기록',
            ],
        },
        {
            'no': 2,
            'day': 'Day 2 (화요일) — 09:00~18:00',
            'title': '작업영상 기반 표준시간 측정과 라인 밸런싱',
            'time': '8h: 이론 3h + 실습 5h',
            'goals': [
                '표준시간(ST)의 정의와 산출 공식을 이해하고 영상 기반 스톱워치법으로 공정별 ST를 측정할 수 있다.',
                '사전 녹화된 충진·포장 작업 영상에서 사이클타임을 분 단위 소수점 1자리까지 측정·기록할 수 있다.',
                '라인 밸런싱 효율(%)을 계산하고 영상 분석을 통해 병목공정을 식별하여 개선안을 제시할 수 있다.',
            ],
            'rows': [
                ['2-1', '표준시간(ST) 개념·공식·여유율', '1.0', '0', 'ST = 정미시간 × (1+여유율) / 여유율 산정 기준'],
                ['2-2', '영상 분석법·작업분석 기법', '1.0', '0', '영상 재생속도·구간 표시·관측 횟수·이상치 처리'],
                ['2-3', '충진·포장 작업 영상 분석 실습', '0', '2.5', '사전 녹화 영상에서 공정별 10회 사이클타임 측정'],
                ['2-4', '라인 밸런싱 효율 계산식', '1.0', '1.0', '효율(%) = (Σ공정시간 / (공정수×최대공정시간)) × 100'],
                ['2-5', '병목공정 식별·개선안 도출', '0', '1.5', '영상·데이터 기반 병목 식별 → 개선안 1건'],
                ['<b>합계</b>', '', '<b>3.0</b>', '<b>5.0</b>', '<b>8.0</b>'],
            ],
            'practice': [
                '사전 녹화된 충진라인·포장라인 작업 영상(각 30분 분량)을 노트북·태블릿으로 재생',
                '영상 위 스톱워치 또는 동영상 플레이어 구간 표시 기능으로 각 공정 사이클타임 10회 측정',
                '측정값을 표준시간 측정표에 분 단위 소수점 1자리로 기록 → 평균·표준편차 산출',
                '라인 밸런싱 분석 시트(Excel)로 효율(%)·병목공정 식별 → 개선안 1건 작성',
            ],
        },
        {
            'no': 3,
            'day': 'Day 3 (수요일) — 09:00~18:00',
            'title': '표본 데이터 기반 일일 생산일보 작성 실무',
            'time': '8h: 이론 3h + 실습 5h',
            'goals': [
                '일일 생산일보의 표준 양식과 항목을 이해하고 표본 데이터로 정확히 작성할 수 있다.',
                '계획 대비 실적률·불량률·시간당 생산량(UPH)을 정확한 산출식으로 계산할 수 있다.',
                '자재 수율(%)을 산출하여 일일 생산일보에 기록할 수 있다.',
            ],
            'rows': [
                ['3-1', '일일 생산일보 양식·항목·작성 절차', '1.0', '0', '라인·품목·계획수량·실적수량·불량수량·작업시간'],
                ['3-2', '계획 대비 실적률·불량률·UPH 산출식', '1.5', '0', '산출식·단위·예제 풀이'],
                ['3-3', '자재 수율(%) 산출 실무', '0.5', '1.0', '투입·산출·loss율 / 원료·용기·박스'],
                ['3-4', '일일 생산일보 작성 실습 (1·2·3일차분)', '0', '2.5', '사전 제공 표본 데이터로 일보 3장 작성'],
                ['3-5', '일보 검토·이상치 분석', '0', '1.5', '이상치 식별 / 사유 분석 / 보고 절차'],
                ['<b>합계</b>', '', '<b>3.0</b>', '<b>5.0</b>', '<b>8.0</b>'],
            ],
            'practice': [
                '사전 제공 5일치 표본 생산 데이터 세트(라피카 과거 실데이터 가공)를 입력원으로 활용',
                'Day 3 실습 시간에 표본 데이터 1·2·3일차분으로 일일 생산일보 3장 작성',
                '자재 수율(원료·용기·박스) 계산표 작성',
                '이상치 사례 3건 식별 → 사유 추정·보고 절차 토의',
            ],
        },
        {
            'no': 4,
            'day': 'Day 4 (목요일) — 09:00~18:00',
            'title': '생산성 KPI 대시보드 설계·운영',
            'time': '8h: 이론 3h + 실습 5h',
            'goals': [
                'KPI 정의와 데이터 흐름을 설계하여 Excel/Google Sheets 기반 대시보드를 구축할 수 있다.',
                '일별·주별 KPI 추이를 시각화(차트·피벗)하여 의사결정 자료로 활용할 수 있다.',
                '이상치 알림과 관리 한계선을 설정하여 즉시 대응 가능한 운영체계를 만들 수 있다.',
            ],
            'rows': [
                ['4-1', 'KPI 정의·데이터 흐름 설계', '1.5', '0', '입력→집계→시각화 / 단일 진실원본(SSOT)'],
                ['4-2', 'Excel/Sheets 함수·피벗·차트 활용', '1.5', '0', 'SUMIFS·QUERY·피벗·조건부서식·스파크라인'],
                ['4-3', 'KPI 대시보드 템플릿 구축 실습', '0', '2.5', '일일 생산일보 → 자동 집계 대시보드 1부'],
                ['4-4', '일별·주별 KPI 추이 시각화', '0', '1.5', '라인차트·바차트·이중축 / Day 1~4 데이터'],
                ['4-5', '이상치 알림·관리 한계선 설정', '0', '1.0', 'UCL/LCL·조건부서식 색상·메일 알림'],
                ['<b>합계</b>', '', '<b>3.0</b>', '<b>5.0</b>', '<b>8.0</b>'],
            ],
            'practice': [
                'Day 3에서 작성한 일보 3장 + 표본 데이터 4일차분으로 누적 4일치 데이터 확보',
                '누적 데이터를 입력원으로 Excel/Sheets KPI 대시보드 1부 직접 구축',
                '실적률·불량률·UPH·납기준수율 4종 KPI를 일별·주별 차트로 시각화',
                '조건부서식·UCL/LCL 알림 설정 시연·실습',
            ],
        },
        {
            'no': 5,
            'day': 'Day 5 (금요일) — 09:00~18:00',
            'title': '개선 전·후 비교 분석 및 보고서 작성·발표',
            'time': '8h: 이론 3.5h + 실습 4.5h',
            'goals': [
                '개선 활동 우선순위를 결정하고 baseline·after 측정 절차를 수행할 수 있다.',
                '향상률·감소율을 정량 계산하고 A4 5페이지 비교 분석 보고서를 작성할 수 있다.',
                '발표 자료를 준비하여 경영진·트레이너 앞에서 5분 내 핵심을 전달할 수 있다.',
            ],
            'rows': [
                ['5-1', '개선 활동 선정 기준·우선순위 매트릭스', '1.0', '0', '영향도·실행가능성 2×2 매트릭스'],
                ['5-2', 'Baseline·After 측정 절차', '1.5', '0', '측정 기간·표본·동일 조건 통제'],
                ['5-3', '향상률·감소율 정량 계산 방법', '1.0', '0', '향상률(%) = (After-Before)/Before × 100'],
                ['5-4', '개선 전·후 비교 분석 보고서 작성', '0', '3.0', 'A4 5페이지 / 표·차트 / 단원 1~4 산출물 종합'],
                ['5-5', '발표 자료 준비 및 발표', '0', '1.5', '슬라이드 5장 + 5분 발표 + 표본 5일차 일보 1장'],
                ['<b>합계</b>', '', '<b>3.5</b>', '<b>4.5</b>', '<b>8.0</b>'],
            ],
            'practice': [
                '표본 데이터 5일차분으로 일일 생산일보 1장 추가 작성 → 누적 5일치 완성',
                '단원 2 라인 밸런싱 개선안을 표본 데이터에 반영한 가상 시나리오 적용 → after 데이터 시뮬레이션',
                '개선 전·후 비교 분석 보고서(A4 5p) + 발표 슬라이드 작성·발표',
            ],
        },
    ]

    for u in units:
        block = []
        block.append(subsec(f'단원 {u["no"]}. {u["title"]}  ({u["time"]})', BLUE))
        block.append(sp(0.3))
        block.append(para(u['day'], 9, KRB, NAVY))
        block.append(sp(0.3))
        block.append(para('<b>학습목표</b>', 9.5, KRB, GREEN))
        block.extend(bullet(u['goals'], 9))
        block.append(sp(0.5))
        block.append(para('<b>세부 학습내용</b>', 9.5, KRB, GREEN))
        block.append(sp(0.3))
        block.append(tbl(
            ['No', '소단원명', '이론(h)', '실습(h)', '핵심 내용'],
            u['rows'],
            widths=[12*mm, 55*mm, 16*mm, 16*mm, W - 2*M - 99*mm],
            font_size=8))
        block.append(sp(0.5))
        block.append(para('<b>실습 활동 (자사 현장 수행)</b>', 9.5, KRB, GREEN))
        block.extend(bullet(u['practice'], 9))
        block.append(sp(2))
        s.append(KeepTogether(block))

    s.append(PageBreak())

    # ── 3. 평가 ────────────────────────────────────────────────────
    s.append(sec('3. 평가'))
    s.append(sp(1))
    s.append(subsec('3.1 평가기준 10개 (이론 4 + 실습 6)'))
    s.append(sp(0.5))
    eval_rows = [
        ['1', '이론', '1', '기준생산계획(MPS) 구성요소 5가지(수요예측·가용재고·ATP·라인 capacity·납기)를 모두 나열한다', '서술형 시험'],
        ['2', '이론', '2', '표준시간(ST) = 정미시간 × (1+여유율) 공식을 적용해 ST를 계산한다', '객관식·계산'],
        ['3', '이론', '2', '라인 밸런싱 효율(%) 계산식을 적고 예제 1건(공정 5개)을 풀이한다', '서술형·계산'],
        ['4', '이론', '3', '생산성 3대 KPI(실적률·불량률·UPH) 산출식·단위·계산 예제를 정확히 작성한다', '객관식·서술'],
        ['5', '실습', '1', '표본 수주서 3건 기반 월간 MPS 시트를 1시간 이내에 작성한다', '산출물(MPS)'],
        ['6', '실습', '2', '사전 녹화 충진라인 영상에서 사이클타임을 10회 측정하여 분 단위 소수점 1자리로 표에 기록하고 평균·표준편차를 산출한다', '실기 체크리스트'],
        ['7', '실습', '2', '영상 분석 결과로 포장라인 밸런싱 효율(%)을 계산하고 병목공정 1개 식별 후 개선안 1건을 제시한다', '산출물(분석시트)'],
        ['8', '실습', '3', '표본 데이터 기반 일일 생산일보 3일치를 작성하고 실적률·불량률·UPH를 정확히 입력한다', '산출물(일보)'],
        ['9', '실습', '4', 'Excel/Sheets 기반 생산성 KPI 대시보드 1부를 직접 구축하고 일별·주별 추이를 시각화한다', '산출물(대시보드)'],
        ['10','실습', '5', '개선 전·후 KPI 비교 분석 보고서(A4 5p)를 작성하고 향상률·감소율을 정량 표시하여 5분 내 발표한다', '산출물+발표평가'],
    ]
    s.append(tbl(
        ['No', '구분', '단원', '평가기준', '측정 방법'],
        eval_rows,
        widths=[10*mm, 14*mm, 12*mm, W - 2*M - 66*mm, 30*mm],
        font_size=8))
    s.append(sp(2))

    s.append(subsec('3.2 평가방법'))
    s.append(sp(0.5))
    s.append(tbl(
        ['평가 영역', '배점', '평가 도구'],
        [
            ['지식평가 (이론)', '30점', '서술형 + 객관식 시험 (40문항, 60분, Day 5 오전 종료시점)'],
            ['실기평가 (사무실 수행)', '40점', '트레이너 관찰 체크리스트 (단원별 8점)'],
            ['산출물 평가', '20점', 'MPS·표준시간표·일보·대시보드·보고서 7종 평가'],
            ['출석·태도', '10점', '출석률 80% 이상 + 트레이너 관찰'],
            ['<b>합계</b>', '<b>100점</b>', ''],
        ],
        widths=[40*mm, 22*mm, W - 2*M - 62*mm]))
    s.append(sp(2))

    s.append(subsec('3.3 합격 기준'))
    s.extend(bullet([
        '<b>총점 80점 이상</b> AND <b>각 영역별 60% 이상</b>',
        '출석률 80% 미만 시 불합격 (정부 환급 기준 준수)',
        '산출물 7종 중 1건 이상 미제출 시 재훈련',
    ]))
    s.append(PageBreak())

    # ── 4. 산출물 ──────────────────────────────────────────────────
    s.append(sec('4. 훈련 산출물 (총 7종)'))
    s.append(sp(1))
    s.append(para(
        '훈련 종료 시 훈련생은 다음 7종 산출물을 제출한다. 모든 산출물은 환급 신청 시 증빙으로 보관한다.',
        9.5))
    s.append(sp(0.8))
    s.append(tbl(
        ['No', '산출물명', '분량/형식', '작성 단원'],
        [
            ['1', '월간 기준생산계획(MPS) 시트', 'Excel 1부 (3개월분)', '단원 1 (Day 1)'],
            ['2', '협력공장 발주·납기 관리대장 (협력사명 가명: A사·B사)', 'Excel 1부 (5건 이상)', '단원 1 (Day 1)'],
            ['3', '충진/포장 라인 표준시간 측정표 (영상 분석 기반)', 'Excel 1부 (각 라인 10회 측정)', '단원 2 (Day 2)'],
            ['4', '라인 밸런싱 분석 시트', 'Excel 1부 (효율%·병목·개선안)', '단원 2 (Day 2)'],
            ['5', '일일 생산일보 5일치 (표본 데이터 기반)', 'Excel 5장', '단원 3·4·5 (Day 3·4·5)'],
            ['6', '생산성 KPI 대시보드', 'Excel 또는 Google Sheets 1부', '단원 4 (Day 4)'],
            ['7', '개선 전·후 비교 분석 보고서 + 발표 슬라이드', 'A4 5페이지 + 슬라이드 5장', '단원 5 (Day 5)'],
        ],
        widths=[10*mm, 70*mm, 50*mm, W - 2*M - 130*mm]))
    s.append(sp(2.5))

    # ── 5. 트레이너 ────────────────────────────────────────────────
    s.append(sec('5. OJT 트레이너 요건'))
    s.append(sp(1))
    s.append(subsec('5.1 자격 요건'))
    s.extend(bullet([
        '화장품 OEM 또는 제조업 <b>생산관리·공정관리 직무 5년 이상</b> 경력자',
        '다음 중 1개 이상 보유 권장: 품질경영기사·산업기사 / 생산관리 NCS 능력단위 이수 또는 직업훈련교사 자격 / 사내 생산관리 부서장·팀장 경력 3년 이상',
        'Excel/Google Sheets 활용 능력 필수 (피벗·함수·차트)',
    ]))
    s.append(sp(1))
    s.append(subsec('5.2 트레이너 사전 교육'))
    s.extend(bullet([
        '사전 교육 시간: <b>8시간</b> (1일 집중)',
        '내용: S-OJT 운영 매뉴얼·평가 체크리스트 활용법 / 단원별 실습 활동 시연 (영상 분석법·표본 데이터 활용법 포함) / 산출물 평가 기준·합격선 / 사무실 환경 안전교육·이상상황 대응',
    ]))
    s.append(sp(1))
    s.append(subsec('5.3 1인당 지도 가능 훈련생 수'))
    s.extend(bullet([
        '<b>트레이너 1인당 최대 8명</b> (S-OJT 적정 비율 1:8)',
        '단원 4(KPI 대시보드 구축)는 1:1 코칭 비중 높음 → 보조 트레이너 1명 권장',
    ]))
    s.append(PageBreak())

    # ── 6. 일정 ────────────────────────────────────────────────────
    s.append(sec('6. 훈련 일정'))
    s.append(sp(1))
    s.append(subsec('6.1 5일 집중형 일정표 (월~금)'))
    s.append(sp(0.5))
    s.append(tbl(
        ['일자', '시간', '단원', '시간배분', '핵심 산출물'],
        [
            ['Day 1<br/>(월)', '09:00–18:00<br/>(8h)', '단원 1<br/>MPS·협력공장', '이론 3.5<br/>+ 실습 4.5', 'MPS 시트<br/>발주·납기 관리대장'],
            ['Day 2<br/>(화)', '09:00–18:00<br/>(8h)', '단원 2<br/>영상 분석·라인밸런싱', '이론 3.0<br/>+ 실습 5.0', '표준시간 측정표<br/>라인밸런싱 분석시트'],
            ['Day 3<br/>(수)', '09:00–18:00<br/>(8h)', '단원 3<br/>일일 생산일보', '이론 3.0<br/>+ 실습 5.0', '일일 생산일보<br/>(1·2·3일차)'],
            ['Day 4<br/>(목)', '09:00–18:00<br/>(8h)', '단원 4<br/>KPI 대시보드', '이론 3.0<br/>+ 실습 5.0', 'KPI 대시보드<br/>일보 4일차'],
            ['Day 5<br/>(금)', '09:00–18:00<br/>(8h)', '단원 5<br/>개선 비교·발표', '이론 3.5<br/>+ 실습 4.5', '개선 보고서·슬라이드<br/>일보 5일차'],
            ['<b>합계</b>', '<b>40h</b>', '<b>5단원</b>', '<b>이론 16h<br/>+ 실습 24h</b>', '<b>7종</b>'],
        ],
        widths=[18*mm, 28*mm, 38*mm, 28*mm, W - 2*M - 112*mm],
        font_size=8.5))
    s.append(sp(2))

    s.append(subsec('6.2 일일 운영 표준 시간표'))
    s.append(sp(0.5))
    s.append(tbl(
        ['시간', '활동', '비고'],
        [
            ['09:00–10:30', '이론 강의 / 시연', '회의실'],
            ['10:30–10:40', '휴식', ''],
            ['10:40–12:00', '이론 강의 / 시연 / 실습 도입', '회의실'],
            ['12:00–13:00', '중식 (훈련시간 미포함)', ''],
            ['13:00–14:30', '사무실 실습 (영상 분석·데이터 작성·양식 작성)', '회의실'],
            ['14:30–14:40', '휴식', ''],
            ['14:40–16:00', '사무실 실습', '회의실'],
            ['16:00–16:10', '휴식', ''],
            ['16:10–17:00', '산출물 작성 / 일일 생산일보 마감', '회의실'],
            ['17:00–18:00', '트레이너 피드백 / 일일 정리', '회의실'],
        ],
        widths=[35*mm, 90*mm, W - 2*M - 125*mm]))
    s.append(sp(2))

    s.append(subsec('6.3 운영 원칙'))
    s.extend(bullet([
        '<b>1주 집중형(월~금)</b> — 학습 몰입도·KPI 데이터 연속성 확보',
        '<b>사무실 기반 실습</b> — 회의실에 노트북·프로젝터·동영상 자료·표본 데이터 세트 사전 비치',
        '5일치 일일 생산일보를 <b>표본 데이터로 훈련 5일간 매일 1장씩 훈련시간 내 작성</b>',
        '사업장 라인 가동에 영향을 주지 않음 (훈련생 전원이 사무실 회의실에서 학습)',
        '분할 운영 옵션: 사업장 사정 시 "월화수 + 다음주 월화" 또는 "월화 + 다음주 수목금" 분할 가능',
    ]))
    s.append(PageBreak())

    # ── 부록 ──────────────────────────────────────────────────────
    s.append(sec('부록 A. 사용 도구·자료'))
    s.append(sp(1))
    s.append(tbl(
        ['분류', '도구 / 자료', '단원'],
        [
            ['영상 자료', '사전 녹화된 충진라인·포장라인 작업 영상 (각 30분, MP4 또는 사내 공유 링크)', '2'],
            ['측정 보조', '동영상 플레이어 구간 표시 기능 또는 디지털 스톱워치 (영상 위 측정용)', '2'],
            ['SW', 'Microsoft Excel 또는 Google Sheets (훈련생 1인 1대 노트북)', '1·2·3·4·5'],
            ['디스플레이', '회의실 빔프로젝터·대형 모니터 (집체이론·시연·발표용)', '전 단원'],
            ['템플릿', 'MPS 시트, 발주·납기 관리대장, 표준시간 측정표, 라인 밸런싱 분석 시트, 일일 생산일보, KPI 대시보드, 비교 분석 보고서 (총 7종 — 사전 제공)', '1·2·3·4·5'],
            ['표본 자료', '라피카 표본 수주서 5건, 자사·협력공장 capacity 자료, 5일치 표본 생산 데이터 세트 (모두 개인정보·기밀 마스킹)', '1·2·3·4·5'],
            ['출력', '발주서·일일 생산일보 출력용 양식 (A4)', '1·3'],
        ],
        widths=[22*mm, W - 2*M - 54*mm, 32*mm]))
    s.append(sp(3))

    s.append(sec('부록 B. 작년 품질관리(QC) 과정과의 차별점'))
    s.append(sp(1))
    s.append(tbl(
        ['비교 항목', '작년 QC 과정', '올해 OEM 생산관리 과정'],
        [
            ['직무 영역', '품질관리 (불량 저감·검사 표준)', '생산관리 (계획·일정·생산성)'],
            ['핵심 산출물', '검사 표준서·불량 분석 보고서', 'MPS·표준시간표·KPI 대시보드·개선 보고서'],
            ['측정 지표', '불량률·합격률', '실적률·UPH·향상률·납기준수율'],
            ['실습 도구', '검사 장비·표준품', '노트북·Excel·작업영상·표본 데이터'],
            ['훈련 환경', '현장 검사실', '사무실 회의실 (사무실 기반)'],
        ],
        widths=[35*mm, 70*mm, W - 2*M - 105*mm]))
    s.append(sp(1.5))
    s.append(para(
        '→ 직무 영역·산출물·측정 지표·훈련 환경이 전면 차별화되어 작년 QC 과정과 중복되지 않음.',
        9.5, KRB, GREEN))

    # ── 푸터 ──────────────────────────────────────────────────────
    s.append(sp(5))
    s.append(HRFlowable(width=W - 2*M, thickness=0.5, color=LBLUE))
    s.append(sp(0.5))
    s.append(para(
        f'(주)라피카 — S-OJT 훈련계획서 · 화장품 OEM 생산관리 및 생산성 향상 실무 과정 · '
        f'작성일 {datetime.date.today().strftime("%Y.%m.%d")} · 히어컴퍼니 기업컨설팅',
        7.5, KR, GRAY, alignment=1))

    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)
    print(f'✅ PDF 생성 완료: {out}')
    return out


if __name__ == '__main__':
    build()
