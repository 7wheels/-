"""
(주)라피카 — 화장품 원료 배합 및 처방 실무 향상 과정
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
COMPANY = '(주)라피카'

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
    out = Path(__file__).parent / '라피카_S-OJT_훈련계획서.pdf'
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
          Paragraph('화장품 원료 배합 및 처방 실무 향상 과정', ps(KR, 12, BLUE)),
          HRFlowable(width='100%', thickness=1.5, color=BLUE, spaceAfter=6),
          Paragraph(f'기업명: (주)라피카  |  작성일: {datetime.date.today()}  |  히어컴퍼니 기업컨설팅 제공',
                    ps(KR, 8.5, GRAY)),
          sp(3)]

    # ① 훈련과정명
    S += [sec('① 훈련과정명'), sp(0.5),
          Paragraph('화장품 원료 배합 및 처방 실무 향상 과정 (S-OJT)', h2), sp(1.5)]

    # ② 이론:실습
    S += [sec('② 이론 40% : 실습 60%'), sp(0.5)]
    S.append(tbl(
        ['교과목명', '이론(h)', '실습(h)', '합계'],
        [['원료 특성 및 분류 이해',      '4', '2', '6'],
         ['배합 비율 설계 실습',        '2', '6', '8'],
         ['처방 시험 및 안정성 테스트',  '2', '6', '8'],
         ['처방 기록 및 문서 작성',      '4', '4', '8'],
         ['합계',                      '12 (40%)', '18 (60%)', '30']],
        [90*mm, 28*mm, 28*mm, 29*mm]))
    S.append(sp(1.5))

    # ③ NCS
    S += [sec('③ NCS 분류'), sp(0.5)]
    S.append(tbl(['항목', '내용'],
        [['대분류',      '14. 화학'],
         ['중분류',      '02. 화장품'],
         ['소분류',      '01. 화장품 제조·개발'],
         ['세분류',      '03. 화장품 개발'],
         ['능력단위명',  '화장품 처방 개발'],
         ['능력단위코드','1402010301_23v1']],
        [50*mm, 125*mm]))
    S.append(sp(1.5))

    # ④ 훈련 목표
    S += [sec('④ 훈련 목표'), sp(0.5)]
    for i, g in enumerate([
        '화장품 원료(유화제·보습제·방부제·색소 등)의 특성과 역할을 설명할 수 있다',
        '제품 유형별(로션·크림·세럼) 기본 배합 비율을 설계하고 처방서를 작성할 수 있다',
        '처방 시험 절차에 따라 시제품을 제조하고 외관·점도·pH를 측정할 수 있다',
        '안정성 테스트 결과를 기준에 따라 판정할 수 있다',
        '처방 개발 결과를 내부 양식에 맞게 문서로 기록·보고할 수 있다',
    ], 1):
        S.append(Paragraph(f'{i}. {g}', bul))
    S.append(sp(1.5))

    # ⑤ 주요훈련내용
    S += [sec('⑤ 주요훈련내용'), sp(0.5)]
    S.append(Paragraph(
        '화장품 원료의 종류와 기능적 특성을 체계적으로 이해하고, 제품 유형에 따른 최적 배합 비율을 스스로 설계할 수 있는 실무 역량을 배양한다. '
        '단순 지식 전달에 그치지 않고 실험실에서 직접 처방을 시험하고, 안정성·관능 평가를 수행하며 결과를 문서화하는 전 과정을 실습한다. '
        '최종적으로 사내 처방 개발 프로세스를 독립적으로 수행할 수 있는 수준까지 역량을 향상시킨다.', body))
    S.append(sp(1.5))

    # ⑥ 훈련대상 요건
    S += [sec('⑥ 훈련대상 요건'), sp(0.5)]
    for r in ['(주)라피카 R&D·개발팀 및 생산 기술직 재직자',
              '입사 6개월 이상',
              '화학·화장품·생명과학 관련 학과 전공자 우대 (비전공자 참여 가능)',
              '기초 실험 도구(비커·저울·pH미터) 사용 경험자']:
        S.append(Paragraph(f'• {r}', bul))
    S.append(sp(1.5))

    # ⑦ 교과목/세부훈련내용
    S += [sec('⑦ 교과목 / 세부훈련내용'), sp(0.5)]
    S.append(tbl(
        ['모듈', '교과목명', '세부훈련내용', '이론', '실습', '합계'],
        [['1', '원료 특성 및 분류',
          '원료 유형 분류 / 주요 원료 역할·기준 / MSDS 확인 실습', '4', '2', '6'],
         ['2', '배합 비율 설계',
          '제품 유형별 처방 구조 / 배합 비율 계산 / 처방서 작성', '2', '6', '8'],
         ['3', '처방 시험 및 안정성',
          '유화·분산 공정 실습 / 물성 측정 / 온도·광안정성 테스트', '2', '6', '8'],
         ['4', '처방 기록 및 문서화',
          '처방 기록 양식 / 시험 성적서 작성 / 보고 실습', '4', '4', '8'],
         ['', '합계', '', '12', '18', '30']],
        [12*mm, 30*mm, 77*mm, 14*mm, 14*mm, 14*mm]))
    S.append(sp(1.5))

    # ⑧ 기업현황분석
    S += [sec('⑧ 기업현황분석'), sp(0.5)]
    S.append(Paragraph(
        '(주)라피카는 화장품 제조·판매업체로 ODM/OEM 방식의 다품종 생산 체계를 운영하고 있다. '
        '최근 자체 브랜드 제품 비중을 늘리는 방향으로 사업 전략을 전환하면서 내부 처방 개발 역량의 중요성이 높아졌다. '
        '그러나 처방 개발 실무가 일부 숙련 인력에 집중되어 신규 인력의 역량 격차가 존재하며, '
        '본 훈련을 통해 이를 해소하고자 한다.', body))
    S.append(sp(0.5))
    S.append(tbl(['항목', '내용'],
        [['업종',       '화장품 제조업 (KSIC: C20429)'],
         ['주요 사업',  '기초·색조화장품 제조, ODM/OEM'],
         ['인력 현황',  'R&D·개발팀 중심, 처방 개발 숙련자 소수 집중'],
         ['훈련 필요성','자체 처방 개발 역량 내재화 → 외주 의존 비용 절감'],
         ['기대 효과',  '재작업 건수 감소, 신제품 개발 주기 단축']],
        [45*mm, 130*mm]))
    S.append(sp(1.5))

    # ⑨ 업무 선정 및 분석
    S += [sec('⑨ 훈련대상 업무 선정 및 분석'), sp(0.5)]
    S.append(Paragraph(
        '처방 개발 업무는 제품 경쟁력의 핵심이나 체계적 교육 없이 선임자 관찰 방식으로만 전수되어 왔다. '
        '처방 오류로 인한 재작업이 월평균 3~5건 발생하고 있어 구조적 개선이 필요하다.', body))
    S.append(sp(0.5))
    S.append(tbl(['분석 항목', '내용'],
        [['대상 업무',  '원료 선정 → 배합 설계 → 시제품 제조 → 안정성 평가 → 문서화'],
         ['수행 빈도',  '신제품 기준 월 2~4건 처방 개발'],
         ['현재 수준',  '지도 없이 독립 수행 불가 (초급~중급 혼재)'],
         ['목표 수준',  '기본 처방 설계 및 시험을 독립적으로 수행 가능 (중급)'],
         ['역량 Gap',  '원료 지식 부족 / 배합 비율 계산 미숙 / 문서화 습관 부재']],
        [45*mm, 130*mm]))
    S.append(sp(1.5))

    # ⑩ 훈련환경 분석
    S += [sec('⑩ 기업훈련환경 분석'), sp(0.5)]
    S.append(tbl(['항목', '내용'],
        [['훈련 장소',    '사내 실험실 및 R&D 공간'],
         ['주요 설비',    '유화기, 균질기, pH미터, 점도계, 항온항습기'],
         ['OJT 트레이너', 'R&D팀장 (처방 개발 경력 8년) / 수석연구원 (경력 5년)'],
         ['훈련 가능 시간','주 2회, 오전 9~12시 (생산 일정 비중복)'],
         ['훈련 예산',    '총 훈련비의 60~80% 고용보험 환급 예정'],
         ['지원 제도',    '사업주 훈련 — 중소기업 우선지원 대상 기업 적용']],
        [45*mm, 130*mm]))
    S.append(sp(1.5))

    # ⑪ 평가기준
    S += [sec('⑪ 업무단원명 / 평가기준'), sp(0.5)]
    S.append(Paragraph('업무단원명: 화장품 원료 배합 및 처방 실무', h2))
    S.append(sp(0.5))
    S.append(tbl(['#', '평가기준'],
        [[str(i), c] for i, c in enumerate([
            '화장품 원료를 유성·수성·계면활성제·기능성으로 분류하고 각 역할을 설명할 수 있다',
            '원료별 MSDS를 확인하고 취급 주의사항을 준수하여 실습할 수 있다',
            '제품 유형(로션·크림·세럼)에 따른 기본 배합 구조를 설명할 수 있다',
            '처방 설계서에 원료명·함량(%)·투입 순서를 정확히 기재할 수 있다',
            '유화 공정 절차에 따라 시제품을 안전하게 제조할 수 있다',
            'pH미터·점도계를 사용하여 시제품 물성을 측정하고 기준치와 비교할 수 있다',
            '온도안정성 테스트(4℃·25℃·45℃ 4주) 절차를 수행하고 결과를 기록할 수 있다',
            '안정성 이상(분리·변색·변취) 발생 시 원인을 파악하고 트레이너에게 즉시 보고할 수 있다',
            '처방 시험 결과를 사내 양식에 맞게 문서화하고 파일로 저장할 수 있다',
            '완성된 처방 초안을 팀 검토 회의에서 구두로 설명할 수 있다',
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
