# 히어로 (Hero) — 중소·벤처 기업 문서 자동화 에이전트

Claude Agent SDK 기반의 한국 중소·벤처 기업 컨설팅 에이전트입니다.
공개된 정부 평가기준·표준양식만을 사용해 다음 5가지 문서 초안을
자연어 대화로 생성합니다.

| # | 문서                                      | 도구                                |
|---|-------------------------------------------|-------------------------------------|
| 1 | 벤처기업 인증 신청서                      | `draft_venture_certification`       |
| 2 | 메인비즈(경영혁신형) 인증 신청서          | `draft_mainbiz_certification`       |
| 3 | 이노비즈(기술혁신형) 인증 신청서          | `draft_innobiz_certification`       |
| 4 | 연구노트 (국가 R&D 과제용)                | `draft_research_note`               |
| 5 | 사업계획서 (K-Startup PSST)               | `draft_business_plan`               |

---

## 구조

```
hero/
├── __init__.py
├── criteria.py   # 공개 평가기준·양식 데이터 (출처 명시)
├── tools.py      # 5개 in-process MCP 도구 + 서버
├── hero.py       # 메인 에이전트 시스템 프롬프트 + 옵션
└── cli.py        # 대화형 CLI
```

**역할 분담**
- `criteria.py`: law.go.kr·mss.go.kr·k-startup.go.kr 등 정부 공식 사이트의
  공개 자료를 Python 데이터 구조로 정리
- `tools.py`: 각 도구는 사용자 회사 정보를 받아 공개 기준을 시스템 프롬프트에
  임베드한 뒤 Claude API(`claude-opus-4-7`)로 초안 생성
- `hero.py`: Claude Agent SDK의 `ClaudeSDKClient` 옵션 정의 — 히어로가 5개
  도구를 적절히 라우팅하도록 시스템 프롬프트 설계
- `cli.py`: 터미널 대화 루프

---

## 설치 및 실행

```bash
# 1) 의존성 설치
pip install -r requirements.txt

# 2) API 키 설정
cp .env.example .env
# .env 파일에서 ANTHROPIC_API_KEY 채우기
export $(cat .env | xargs)

# 3) Claude Code CLI 설치 (Agent SDK 동작 전제)
#    https://docs.anthropic.com/en/docs/claude-code/quickstart
npm install -g @anthropic-ai/claude-code

# 4) 히어로 실행
python -m hero.cli
```

실행 예시:

```
============================================================
히어로 (Hero) — 중소·벤처 기업 문서 에이전트
============================================================
작성 가능: 벤처인증 / 메인비즈 / 이노비즈 / 연구노트 / 사업계획서
종료: 빈 줄 + Enter, 또는 Ctrl+D

안녕하세요! 다음 5가지 문서 작성을 도와드릴 수 있습니다 ...

> 우리 회사 이노비즈 인증 신청서 초안 만들어줘
```

히어로가 입력 항목을 한 번에 묶어 질문하면, 답변 후 도구가 호출되고
Claude가 평가지표 구조에 맞춰 초안을 생성합니다.

---

## 도구 직접 호출 (테스트용)

CLI 없이 도구를 직접 시험할 수 있습니다.

```python
import asyncio
from hero.tools import draft_innobiz_certification

async def main():
    result = await draft_innobiz_certification({
        "company_name": "주식회사 예시",
        "industry": "AI 소프트웨어",
        "rnd_personnel_ratio": "전체 24명 중 10명 (41.7%)",
        "rnd_investment_ratio": "매출 15억 중 R&D 4억 (26.7%)",
        "ip_portfolio": "특허 등록 3건, 출원 5건, SW저작권 7건",
        "rnd_track_record": "중기부 TIPS 1단계 수행 중 (2023~)",
        "tech_management_system": "기업부설연구소 보유, 분기별 기술기획회의",
        "production_capacity": "AWS 기반 SaaS, 월 활성사용자 1.2만명",
        "sales_channels": "국내 B2B 직판 + 일본 파트너 1사",
        "new_product_revenue_ratio": "최근 2년 신제품 매출 비중 78%",
        "partnerships": "OO대학 산학협력단 + KISTI 데이터 협약",
        "financial_performance": "매출 CAGR 130%, 영업이익률 12%",
        "employment_performance": "정규직 비율 95%, 청년 고용 65%",
    })
    print(result["content"][0]["text"])

asyncio.run(main())
```

---

## 데이터 출처

이 시스템에 임베드된 평가기준·양식은 모두 정부 공식 사이트에서 누구나
열람 가능한 공개 자료입니다.

| 문서          | 근거 / 출처                                                   |
|---------------|---------------------------------------------------------------|
| 벤처기업 인증 | 「벤처기업육성에 관한 특별조치법」 (law.go.kr) + 벤처기업확인기관 평가표 |
| 메인비즈      | 한국경영혁신중소기업협회 평가표 (mainbiz.go.kr 또는 mainbiz.or.kr) |
| 이노비즈      | 「중소기업기술혁신촉진법 시행령」 별표 + 이노비즈협회 평가지표 (innobiz.or.kr) |
| 연구노트      | 「국가연구개발혁신법」 + 과기정통부 「연구노트 작성·관리 지침」(고시) |
| 사업계획서    | K-Startup 표준양식 (k-startup.go.kr 공고별 첨부파일) |

특정 기업의 영업비밀·내부 평가 노하우·유료 서비스의 코드는 일절
사용하지 않았습니다.

---

## 한계 및 면책

- 본 시스템이 생성하는 초안은 **참고용**이며 실제 평가기관의 합격을
  보장하지 않습니다.
- 정량 데이터(매출·인력·특허 등)는 사용자가 정확히 입력해야 하며,
  히어로는 정보가 부족한 항목을 `[추가 정보 필요: ...]` 로 명시합니다.
- 실적 부풀리기·허위 기재 요청에는 응답하지 않습니다 — 정직한 서술
  기반에서 보완할 수 있는 후속 활동을 제안합니다.
- 평가기준은 매년 개정될 수 있으므로 신청 직전 협회·기관 공고를 다시
  확인하세요.
