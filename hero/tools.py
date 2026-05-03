"""히어로(메인 에이전트)가 호출하는 5개의 in-process MCP 도구.

각 도구는 사용자 회사 정보를 받아 공개 평가기준을 시스템 프롬프트에 임베드한
뒤 Claude API로 문서 초안을 생성합니다. 모든 평가기준은 정부 공식 출처에서
공개된 자료입니다 (criteria.py 헤더 주석 참조).
"""

from __future__ import annotations

import json
import os
from typing import Any

from anthropic import AsyncAnthropic
from claude_agent_sdk import create_sdk_mcp_server, tool

from . import criteria

DRAFTER_MODEL = os.environ.get("HERO_DRAFTER_MODEL", "claude-opus-4-7")
_anthropic = AsyncAnthropic()


def _format_rubric(rubric: list[criteria.EvalSection]) -> str:
    lines = []
    for section in rubric:
        lines.append(f"\n[{section['name']}] (가중치 {section['weight']})")
        for item in section["items"]:
            lines.append(f"  - {item}")
    return "\n".join(lines)


async def _draft(system_prompt: str, user_payload: dict[str, Any]) -> str:
    """공통 초안 생성기 — 공개 기준 + 사용자 데이터를 받아 문서 초안 반환."""
    response = await _anthropic.messages.create(
        model=DRAFTER_MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    "다음은 신청 회사의 정보입니다. 위 평가기준에 맞춰 "
                    "구체적·정량적·전문적인 초안을 작성해 주세요. "
                    "허위 정보를 만들어 채우지 말고, 정보가 부족한 항목은 "
                    "[추가 정보 필요: ...] 형식으로 명시적으로 표기하세요.\n\n"
                    f"```json\n{json.dumps(user_payload, ensure_ascii=False, indent=2)}\n```"
                ),
            }
        ],
    )
    return "".join(b.text for b in response.content if b.type == "text")


# ─────────────────────────────────────────────────────────────
# Tool 1. 벤처기업 인증 신청서 초안
# ─────────────────────────────────────────────────────────────

@tool(
    "draft_venture_certification",
    "벤처기업 인증(혁신성장유형/연구개발유형/벤처투자유형) 신청서 초안을 생성합니다. "
    "기술혁신성·사업성장성 관점에서 회사의 강점을 평가기준에 매핑한 서술형 초안을 만듭니다.",
    {
        "company_name": str,
        "venture_type": str,  # "investment" | "rnd" | "innovation"
        "industry": str,
        "founded_year": int,
        "employees": int,
        "annual_revenue_krw": int,
        "rnd_investment_krw": int,
        "ip_assets": str,  # 보유 특허·SW저작권·인증 (자유서술)
        "core_tech_summary": str,
        "target_market": str,
        "competitors": str,
        "differentiation": str,
        "growth_plan": str,
    },
)
async def draft_venture_certification(args: dict[str, Any]) -> dict[str, Any]:
    vtype = args.get("venture_type", "innovation")
    type_info = criteria.VENTURE_TYPES.get(vtype, criteria.VENTURE_TYPES["innovation"])

    system = f"""당신은 벤처기업확인 신청서 작성을 돕는 전문가입니다.
근거 법령: 「벤처기업육성에 관한 특별조치법」.

신청 유형: {type_info['label']}
유형별 충족 요건:
{chr(10).join(f"  - {r}" for r in type_info['requirements'])}
평가기관: {type_info['evaluator']}

평가표 (혁신성장유형 기준 — 다른 유형도 동일 관점 적용):
{_format_rubric(criteria.VENTURE_INNOVATION_RUBRIC)}

작성 원칙:
1. 평가표의 각 항목을 별도 소제목으로 두고, 회사 정보를 매핑하여 서술
2. 가능한 한 정량 지표(매출, R&D 비중, 특허 건수, 점유율 등) 사용
3. 보유 IP·인증·수상 실적은 구체적 명칭으로 인용
4. 시장규모는 출처 표기 권장 (예: "한국 OO 시장 [출처: 통계청 2024]")
5. 마지막에 [부족 자료 체크리스트] 섹션을 두고 보완 필요 항목 정리

출력 형식: 마크다운, 신청서 섹션 구조로 정리"""

    draft = await _draft(system, args)
    return {"content": [{"type": "text", "text": draft}]}


# ─────────────────────────────────────────────────────────────
# Tool 2. 메인비즈 인증 신청서 초안
# ─────────────────────────────────────────────────────────────

@tool(
    "draft_mainbiz_certification",
    "메인비즈(경영혁신형 중소기업) 인증 신청서 초안을 생성합니다. "
    "경영혁신활동 5개 영역(인사·마케팅·생산·정보화·전략)과 경영성과를 평가표 구조로 작성합니다.",
    {
        "company_name": str,
        "industry": str,
        "founded_year": int,
        "employees": int,
        "revenue_history": str,  # 최근 3년 매출 추이 (자유서술)
        "hr_innovation": str,  # 인사·교육·조직 개선 활동
        "marketing_innovation": str,
        "production_innovation": str,
        "it_innovation": str,
        "strategy_innovation": str,
        "financial_metrics": str,
        "employment_metrics": str,
        "innovation_outcomes": str,
    },
)
async def draft_mainbiz_certification(args: dict[str, Any]) -> dict[str, Any]:
    system = f"""당신은 메인비즈(경영혁신형 중소기업) 인증 신청서 작성을 돕는 전문가입니다.
근거 법령: 「중소기업 인력지원 특별법」(메인비즈 운영 근거),
주관: 한국경영혁신중소기업협회.

평가표 (1000점 만점, 합격 {criteria.MAINBIZ_PASS_SCORE}점 이상):
{_format_rubric(criteria.MAINBIZ_RUBRIC)}

작성 원칙:
1. 5개 혁신 영역(인사·마케팅·생산·정보화·전략) 각각에 대해
   - 도입 시기 / 도입 배경 / 구체적 활동 / 정량 성과 4단 구조로 서술
2. 경영성과는 "Before vs After" 표로 정리 (가능하면 3년 추이)
3. 도입한 시스템·인증·교육의 명칭을 명시 (예: ERP "더존 SmartA" 도입)
4. 각 항목 끝에 평가표상 자기점수(예상)와 근거를 한 줄로 부기
5. 마지막에 [개선 권고사항] 섹션 — 점수 향상을 위한 후속 조치 제안

출력 형식: 마크다운, 평가표 순서대로 섹션 구성"""

    draft = await _draft(system, args)
    return {"content": [{"type": "text", "text": draft}]}


# ─────────────────────────────────────────────────────────────
# Tool 3. 이노비즈 인증 신청서 초안
# ─────────────────────────────────────────────────────────────

@tool(
    "draft_innobiz_certification",
    "이노비즈(기술혁신형 중소기업) 인증 신청서 초안을 생성합니다. "
    "기술혁신능력·기술사업화능력·기술혁신경영성과 3대 영역을 평가지표대로 작성합니다.",
    {
        "company_name": str,
        "industry": str,
        "rnd_personnel_ratio": str,  # R&D 인력 비중 (예: "전체 30명 중 9명, 30%")
        "rnd_investment_ratio": str,  # 매출 대비 R&D 투자 비중
        "ip_portfolio": str,  # 특허·실용신안·SW·디자인 보유 현황
        "rnd_track_record": str,  # 정부 R&D·기업부설연구소 운영 실적
        "tech_management_system": str,  # 기술기획·관리 체계
        "production_capacity": str,  # 생산·서비스 인프라
        "sales_channels": str,  # 국내·해외 판로
        "new_product_revenue_ratio": str,  # 신제품·신기술 매출 기여도
        "partnerships": str,  # 산학연·공급망 협력
        "financial_performance": str,
        "employment_performance": str,
    },
)
async def draft_innobiz_certification(args: dict[str, Any]) -> dict[str, Any]:
    system = f"""당신은 이노비즈(기술혁신형 중소기업) 인증 신청서 작성을 돕는 전문가입니다.
근거 법령: 「중소기업기술혁신촉진법」 시행령.
주관: 이노비즈협회 + 중소벤처기업진흥공단.

평가지표 (1000점 만점, 합격 {criteria.INNOBIZ_PASS_SCORE}점 이상,
각 영역 60% 이상 동시 충족 필요):
{_format_rubric(criteria.INNOBIZ_RUBRIC)}

작성 원칙:
1. 3개 평가영역(기술혁신능력·기술사업화능력·기술혁신경영성과)을 1·2·3장으로 구성
2. 각 항목별로 "정의 → 회사 현황(수치) → 근거자료 → 자기점수(예상)" 4단 구조
3. R&D 인력·투자 비중은 반드시 % 수치로 명시
4. 지식재산권은 등록번호·등록일·기술분야까지 명시 (예: "특허 제10-XXXXXXX호, 2024.03 등록")
5. 기술인증·R&D 실적은 사업명·수행기간·정부지원금까지 표기
6. 모든 영역에서 60% 미만이 예상되는 항목은 [집중 개선 필요] 표시
7. 마지막에 [현장평가 대비 준비사항] 섹션 — 평가위원 질문 예상 + 답변 포인트

출력 형식: 마크다운, 평가영역 → 평가항목 → 세부지표 계층 구조"""

    draft = await _draft(system, args)
    return {"content": [{"type": "text", "text": draft}]}


# ─────────────────────────────────────────────────────────────
# Tool 4. 연구노트 초안 생성
# ─────────────────────────────────────────────────────────────

@tool(
    "draft_research_note",
    "「국가연구개발혁신법」 및 과기정통부 연구노트 작성·관리 지침에 부합하는 "
    "연구노트 한 페이지 초안을 생성합니다. 위변조 방지 요건과 필수 기재사항을 모두 반영합니다.",
    {
        "project_title": str,
        "principal_investigator": str,
        "researcher_name": str,
        "date": str,  # YYYY-MM-DD
        "page_no": str,
        "experiment_purpose": str,
        "method_and_materials": str,  # 시약·장비·조건 자유서술
        "observations": str,  # 측정값·관찰사항·이미지 캡션
        "analysis": str,  # 분석·고찰
        "next_steps": str,
        "attachments": str,  # 부착 자료 설명 (없으면 "없음")
    },
)
async def draft_research_note(args: dict[str, Any]) -> dict[str, Any]:
    required = "\n".join(f"  - {f}" for f in criteria.RESEARCH_NOTE_REQUIRED_FIELDS)
    integrity = "\n".join(f"  - {r}" for r in criteria.RESEARCH_NOTE_INTEGRITY_RULES)

    system = f"""당신은 국가 R&D 연구노트 작성을 돕는 전문가입니다.
근거: 「국가연구개발혁신법」 + 과기정통부 「연구노트 작성·관리 지침」(고시).

필수 기재사항:
{required}

위변조 방지·보존 요건:
{integrity}

작성 원칙:
1. 위 필수 항목을 모두 채운 한 페이지 분량의 노트를 작성
2. 실험 절차는 "1. 2. 3." 단계별로 명확히 — 재현 가능해야 함
3. 측정값·관찰은 단위(g, mL, ℃, % 등)와 정밀도까지 표기
4. 이미지·그래프가 있다고 가정되는 위치에는 [그림 1: 캡션] 표기 + 부착 안내
5. 끝부분에 「확인란」 — 작성자 서명 / 점검자 서명 / 확인일자 칸 배치
6. 전자노트로 가정한 경우 디지털서명 + 타임스탬프 안내 문구 포함
7. 마지막에 [감사 대비 체크리스트] 섹션 — 추후 R&D 정산 감사 시 점검 포인트

출력 형식: 마크다운, 실제 연구노트 페이지를 그대로 재현하는 레이아웃"""

    draft = await _draft(system, args)
    return {"content": [{"type": "text", "text": draft}]}


# ─────────────────────────────────────────────────────────────
# Tool 5. 사업계획서(K-Startup PSST) 초안
# ─────────────────────────────────────────────────────────────

@tool(
    "draft_business_plan",
    "K-Startup 표준양식(PSST: Problem-Solution-Scale up-Team) 사업계획서 초안을 생성합니다. "
    "예비창업패키지·초기창업패키지·창업도약패키지 등 정부지원사업 공통 양식입니다.",
    {
        "company_name": str,
        "founder_profile": str,  # 대표 학력·경력·창업 이력
        "team_members": str,  # 핵심 구성원 역할·전문성
        "problem_definition": str,  # 해결하려는 문제 + 타겟 고객
        "market_analysis": str,  # 시장규모·성장률 (출처 포함 권장)
        "product_summary": str,  # 제품/서비스 핵심
        "tech_differentiation": str,  # 기술·기능·UX 차별성
        "ip_strategy": str,  # 특허·상표·영업비밀 보호 전략
        "revenue_model": str,  # 수익구조·단가·마진
        "go_to_market": str,  # 시장 진입 전략
        "milestones_36months": str,  # 36개월 마일스톤
        "funding_plan": str,  # 자금 운용 계획
        "risk_and_mitigation": str,  # 리스크 + 대응
    },
)
async def draft_business_plan(args: dict[str, Any]) -> dict[str, Any]:
    sections = []
    for s in criteria.PSST_SECTIONS:
        hints = "\n".join(f"      • {h}" for h in s["drafting_hints"])
        subs = "\n".join(f"    - {sub}" for sub in s["subsections"])
        sections.append(
            f"\n[{s['code']}] {s['name']}\n  소절:\n{subs}\n  작성 가이드:\n{hints}"
        )

    system = f"""당신은 K-Startup 사업계획서(PSST 구조) 작성을 돕는 전문가입니다.
이 양식은 예비창업패키지/초기창업패키지/창업도약패키지/혁신창업스쿨 등
중기부·창업진흥원 정부지원사업의 공통 표준양식입니다.

PSST 구조:{''.join(sections)}

작성 원칙:
1. 각 소절은 본문 1~2페이지 분량, 도표/표가 들어갈 자리는 [표 X], [그림 X]로 표기
2. Problem 섹션: 정량 데이터로 시장 문제를 입증 (출처 표기 — 통계청·KISTI·시장조사기관)
3. Solution 섹션: 기술/서비스 흐름도를 텍스트로 묘사 + 경쟁사 비교표 포함
4. Scale-up 섹션: 3년 매출·이익 추정 표 + 자금 사용 계획 표
5. Team 섹션: 대표·핵심 구성원의 도메인 경력을 정량적으로 (예: "OO 분야 12년")
6. 평가위원 시각으로 "왜 이 팀이, 이 시점에, 이 시장에서 성공할 수 있는가"를
   각 섹션에서 답할 수 있도록 작성
7. 마지막에 [심사평 예상 Q&A] — 평가위원이 던질 만한 질문 5개 + 답변 포인트
8. 사실 확인이 필요한 수치/주장은 [확인 필요: ...] 표기로 사용자가 보완하게 함

출력 형식: 마크다운, PSST 4개 대단원 + 각 소절 번호(1-1, 1-2, 2-1 ...)"""

    draft = await _draft(system, args)
    return {"content": [{"type": "text", "text": draft}]}


# ─────────────────────────────────────────────────────────────
# MCP 서버 — 위 5개 도구를 묶어 히어로에게 노출
# ─────────────────────────────────────────────────────────────

HERO_DOCS_SERVER = create_sdk_mcp_server(
    name="hero-docs",
    version="0.1.0",
    tools=[
        draft_venture_certification,
        draft_mainbiz_certification,
        draft_innobiz_certification,
        draft_research_note,
        draft_business_plan,
    ],
)

ALLOWED_TOOLS = [
    "mcp__hero-docs__draft_venture_certification",
    "mcp__hero-docs__draft_mainbiz_certification",
    "mcp__hero-docs__draft_innobiz_certification",
    "mcp__hero-docs__draft_research_note",
    "mcp__hero-docs__draft_business_plan",
]
