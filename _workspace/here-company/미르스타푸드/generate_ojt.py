"""
(주)미르스타푸드 — 식육가공품 제조 공정 운영 실무 향상 과정
S-OJT 훈련계획서 PDF 생성
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
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
WHITE = colors.white

W, H = A4
M = 18 * mm
COMPANY = '(주)미르스타푸드'

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
    kw.setdefault('leading', size * 1.6)
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

def tbl(headers, rows, widths=None):
    """데이터 표"""
    if not widths:
        widths = [(W - 2*M) / len(headers)] * len(headers)
    th = ps(KRB, 9, WHITE, leading=13)
    td = ps(KR,  9, colors.black, leading=13)
    cells = [[Paragraph(h, th) for h in headers]]
    for row in rows:
        cells.append([Paragraph(str(c), td) for c in row])
    return Table(cells, colWidths=widths, repeatRows=1,
                 style=TableStyle([
                     ('BACKGROUND',    (0,0), (-1,0),  NAVY),
                     ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LGRAY]),
                     ('GRID',          (0,0), (-1,-1), 0.4, LBLUE),
                     ('TOPPADDING',    (0,0), (-1,-1), 5),
                     ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                     ('LEFTPADDING',   (0,0), (-1,-1), 6),
                     ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
                     ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
                     ('ALIGN',         (0,1), (0,-1),  'LEFT'),
                 ]))

# ── 본문 빌드 ─────────────────────────────────────────────────────────
def build():
    out = Path(__file__).parent / '미르스타푸드_S-OJT_훈련계획서.pdf'
    doc = SimpleDocTemplate(str(out), pagesize=A4,
                            topMargin=18*mm, bottomMargin=14*mm,
                            leftMargin=M, rightMargin=M)
    body = ps(KR, 9.5)
    h2   = ps(KRB, 11, NAVY)
    bul  = ps(KR, 9.5, leftIndent=12)
    note = ps(KR, 8.5, GRAY, leftIndent=6)

    S = []

    # 표지
    S += [sp(5),
          Paragraph('S-OJT 훈련계획서', ps(KRB, 22, NAVY)),
          Paragraph('식육가공품 제조 공정 운영 실무 향상 과정', ps(KR, 12, BLUE)),
          HRFlowable(width='100%', thickness=1.5, color=BLUE, spaceAfter=6),
          Paragraph(f'기업명: (주)미르스타푸드  |  작성일: {datetime.date.today()}  |  히어컴퍼니 기업컨설팅 제공',
                    ps(KR, 8.5, GRAY)),
          sp(3)]

    # ① 훈련과정명
    S += [sec('① 훈련과정명'), sp(0.5),
          Paragraph('식육가공품 제조 공정 운영 실무 향상 과정 (S-OJT)', h2), sp(1.5)]

    # ② 이론:실습
    S += [sec('② 이론 40% : 실습 60%'), sp(0.5)]
    S.append(tbl(
        ['교과목명', '이론(h)', '실습(h)', '합계'],
        [['원료육 선별 및 전처리',    '4', '2', '6'],
         ['배합·성형·충전 공정 실습', '2', '6', '8'],
         ['가열·냉각 공정 실습',      '2', '6', '8'],
         ['공정 이상 대응 및 HACCP 기록', '4', '4', '8'],
         ['합계',                    '12 (40%)', '18 (60%)', '30']],
        [90*mm, 28*mm, 28*mm, 29*mm]))
    S.append(sp(1.5))

    # ③ NCS
    S += [sec('③ NCS 분류'), sp(0.5)]
    S.append(tbl(['항목', '내용'],
        [['대분류',      '13. 음식서비스'],
         ['중분류',      '02. 식품가공'],
         ['소분류',      '03. 식육가공'],
         ['세분류',      '01. 식육가공품제조'],
         ['능력단위명',  '식육가공품 제조'],
         ['능력단위코드','1302030101_23v1']],
        [50*mm, 125*mm]))
    S.append(sp(1.5))

    # ④ 훈련 목표
    S += [sec('④ 훈련 목표'), sp(0.5)]
    for i, g in enumerate([
        '원료육의 신선도·등급을 기준에 따라 선별하고 이상육을 격리할 수 있다',
        'SOP에 따라 배합·성형·충전 공정을 순서대로 수행할 수 있다',
        '가열 공정에서 중심온도 75℃ 이상 달성 여부를 확인하고 기록할 수 있다',
        '공정 이상(온도이탈·이물혼입·중량편차) 발생 시 즉시 라인을 정지하고 보고할 수 있다',
        'HACCP CCP 모니터링 기록지를 정확히 작성하고 보관할 수 있다',
    ], 1):
        S.append(Paragraph(f'{i}. {g}', bul))
    S.append(sp(1.5))

    # ⑤ 주요훈련내용
    S += [sec('⑤ 주요훈련내용'), sp(0.5)]
    S.append(Paragraph(
        '식육가공품 제조의 전 공정(원료육 선별·전처리 → 배합·성형·충전 → 가열·냉각)을 SOP 기반으로 체계적으로 습득한다. '
        '단순 기능 습득에 그치지 않고 HACCP CCP 기준을 적용하여 위해요소를 식별하고, '
        '공정 이상 발생 시 표준 절차에 따라 신속히 대응하는 역량을 현장 실습 중심으로 훈련한다. '
        '최종적으로 생산라인에서 독립적으로 각 공정을 수행하고 관련 기록을 정확히 작성할 수 있는 수준을 목표로 한다.', body))
    S.append(sp(1.5))

    # ⑥ 훈련대상 요건
    S += [sec('⑥ 훈련대상 요건'), sp(0.5)]
    for r in ['(주)미르스타푸드 생산라인 재직자',
              '입사 6개월 이상',
              'HACCP 기본 교육 이수 완료자',
              '식품위생 관련 법령 이해자 우대']:
        S.append(Paragraph(f'• {r}', bul))
    S.append(sp(1.5))

    # ⑦ 교과목/세부훈련내용
    S += [sec('⑦ 교과목 / 세부훈련내용'), sp(0.5)]
    S.append(tbl(
        ['모듈', '교과목명', '세부훈련내용', '이론', '실습', '합계'],
        [['1', '원료육 선별 및 전처리',
          '원료육 등급·신선도 판정 기준 / 이상육 격리 절차 / 전처리 SOP 실습', '4', '2', '6'],
         ['2', '배합·성형·충전 공정',
          '배합 비율표 적용 실습 / 성형기·충전기 조작 / 중량 편차 관리', '2', '6', '8'],
         ['3', '가열·냉각 공정',
          '가열 온도 설정 및 중심온도 75℃ 확인 / 냉각 기준 준수 / 이탈 대응', '2', '6', '8'],
         ['4', '공정 이상 대응 및 HACCP 기록',
          'CCP 모니터링 기준 / 이상 발생 보고 절차 / HACCP 기록지 작성 실습', '4', '4', '8'],
         ['', '합계', '', '12', '18', '30']],
        [12*mm, 30*mm, 77*mm, 14*mm, 14*mm, 14*mm]))
    S.append(sp(1.5))

    # ⑧ 기업현황분석
    S += [sec('⑧ 기업현황분석'), sp(0.5)]
    S.append(Paragraph(
        '(주)미르스타푸드는 식육가공업체로 햄·소시지·분쇄가공육 등을 제조하여 납품하고 있다. '
        'HACCP 인증을 취득한 위생 관리 체계를 운영 중이나, 생산라인 재직자의 공정 숙련도 차이로 인해 '
        '온도이탈 등 공정 이상이 월 2~3건 발생하고 있다. '
        '본 훈련을 통해 전 공정에 대한 SOP 기반 실무 역량을 강화하고 품질 사고를 예방하고자 한다.', body))
    S.append(sp(0.5))
    S.append(tbl(['항목', '내용'],
        [['업종',       '식육가공업 (KSIC: C10120)'],
         ['주요 제품',  '햄, 소시지, 분쇄가공육'],
         ['인증 현황',  'HACCP 인증 취득·운영 중'],
         ['훈련 필요성','공정 이상(온도이탈) 월 2~3건 → SOP 기반 실무 역량 강화'],
         ['기대 효과',  '공정 이상 건수 감소, 제품 불량률 저감, HACCP 기록 정확성 향상']],
        [45*mm, 130*mm]))
    S.append(sp(1.5))

    # ⑨ 업무 선정 및 분석
    S += [sec('⑨ 훈련대상 업무 선정 및 분석'), sp(0.5)]
    S.append(Paragraph(
        '생산라인의 핵심 공정인 가열·냉각 단계에서 온도이탈이 반복 발생하고 있으며, '
        '이는 온도 관리 기준 미숙·이상 판단력 부족·기록 오류가 복합적으로 작용한 결과이다. '
        '전처리부터 가열냉각까지 전 공정을 대상으로 역량 Gap을 해소한다.', body))
    S.append(sp(0.5))
    S.append(tbl(['분석 항목', '내용'],
        [['대상 업무',  '원료육 선별 → 배합·성형·충전 → 가열·냉각 → HACCP 기록'],
         ['수행 빈도',  '매일 생산 라인 운영 (교대 근무 포함)'],
         ['현재 수준',  '공정 이상 월 2~3건 (온도이탈 중심), 기록 오류 산발적 발생'],
         ['목표 수준',  'SOP 독립 수행 가능, 이상 발생 즉시 대응 및 정확한 기록'],
         ['역량 Gap',  '온도 관리 기준 미숙 / 이상 판단력 부족 / HACCP 기록 오류']],
        [45*mm, 130*mm]))
    S.append(sp(1.5))

    # ⑩ 훈련환경 분석
    S += [sec('⑩ 기업훈련환경 분석'), sp(0.5)]
    S.append(tbl(['항목', '내용'],
        [['훈련 장소',    '사내 생산라인 및 HACCP 관리 구역'],
         ['주요 설비',    '가열기, 냉각기, 성형기, 충전기, 중심온도계, HACCP 기록판'],
         ['OJT 트레이너', '생산팀장 (식육가공 경력 10년) / 생산반장 (경력 6년)'],
         ['훈련 가능 시간','주 3회, 오후 2~5시 (오전 생산 종료 후)'],
         ['훈련 예산',    '총 훈련비의 60~80% 고용보험 환급 예정'],
         ['지원 제도',    '사업주 훈련 — 중소기업 우선지원 대상 기업 적용']],
        [45*mm, 130*mm]))
    S.append(sp(1.5))

    # ⑪ 평가기준
    S += [sec('⑪ 업무단원명 / 평가기준'), sp(0.5)]
    S.append(Paragraph('업무단원명: 식육가공품 제조 공정 운영', h2))
    S.append(sp(0.5))
    S.append(tbl(['#', '평가기준'],
        [[str(i), c] for i, c in enumerate([
            '원료육을 신선도·등급 기준에 따라 선별하고 이상육을 격리할 수 있다',
            '전처리 SOP(해동·세척·트리밍)를 순서대로 수행할 수 있다',
            '배합 비율표에 따라 원료를 정확히 계량하고 배합기에 투입할 수 있다',
            '성형기·충전기를 조작하여 규격(중량·형태) 내 제품을 생산할 수 있다',
            '가열 공정에서 제품 중심온도가 75℃ 이상임을 온도계로 확인하고 기록할 수 있다',
            '냉각 기준(10℃ 이하)을 준수하고 냉각 시간을 기록할 수 있다',
            '온도이탈 발생 시 라인을 즉시 정지하고 트레이너에게 보고하는 절차를 수행할 수 있다',
            'HACCP CCP 모니터링 기록지를 빠짐없이 정확하게 작성할 수 있다',
            '이물 혼입 의심 시 해당 로트를 격리하고 보고 절차를 따를 수 있다',
            '일일 생산 종료 후 설비 세척·소독 기준을 준수하고 점검 결과를 기록할 수 있다',
        ], 1)],
        [12*mm, 163*mm]))
    S.append(sp(0.5))
    S.append(Paragraph('합격 기준: 10개 항목 중 8개 이상 "수행 가능" 판정', h2))
    S.append(sp(2))

    # 안내
    S.append(HRFlowable(width='100%', thickness=0.5, color=LBLUE, spaceAfter=4))
    S.append(Paragraph(
        '본 훈련계획서는 고용보험 사업주 훈련 환급 기준을 충족하여 작성되었습니다. '
        'HRD-Net 등록 및 노무사 최종 검토 후 제출을 권장합니다.', note))

    doc.build(S, onFirstPage=on_page, onLaterPages=on_page)
    print(f'✅ PDF 생성 완료: {out}')
    return out

if __name__ == '__main__':
    build()
