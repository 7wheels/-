# 프로젝트 하네스 레지스트리

이 파일은 트리거 규칙과 변경 이력만 기록한다. 실제 구조는 `.claude/` 파일시스템에 있다.

---

## 하네스: Harness Meta-Skill

**트리거:** '하네스 만들어줘', '에이전트 팀 구성해줘', '이 프로젝트에 맞는 에이전트 설계해줘', 'build a harness', 'setup agent team'
**스킬:** `.claude/skills/harness/SKILL.md`
**출처:** revfactory/harness (설치 완료)
**변경 이력:** 2026-04-30 — 초기 설치

---

## 하네스 1: 기독교 영성 + 마음챙김

**트리거:** 기독교 영성, 마음챙김, 묵상, 관상기도, 렉시오 디비나, 영성 커뮤니티, 영성 교육, 영적 성장, 기독교 마음챙김 프로그램 관련 요청
**에이전트:**
- `spiritual-orchestrator` — 총괄 오케스트레이터
- `spiritual-guide` — 기독교 영성 신학
- `mindfulness-coach` — 마음챙김 실천
- `community-manager` — 커뮤니티 운영
- `education-designer` — 교육 프로그램 설계
- `content-curator` — 콘텐츠 기획·통합

**스킬:** `.claude/skills/spirituality-mindfulness/SKILL.md`
**패턴:** Fan-out/Fan-in + Producer-Reviewer
**변경 이력:** 2026-04-30 — 최초 생성

---

## 하네스 2: 히어컴퍼니 기업컨설팅

**트리거:** S-OJT, 기업스케일업, 기업인증(벤처·이노비즈·메인비즈), 정책자금, 기업부설연구소, 법인설립, 법인전환, 자금확보, 대표 마인드셋, 컨설팅 제안서, 사업계획서 관련 요청
**에이전트:**
- `here-company-orchestrator` — 총괄 감독
- `scaleup-strategist` — 기업스케일업 전략
- `ojt-specialist` — S-OJT 재직자 훈련
- `certification-expert` — 기업인증
- `policy-fund-expert` — 정책자금·자금확보
- `legal-corporate-expert` — 법인설립·전환
- `ceo-mindset-coach` — 대표 마인드셋

**스킬:** `.claude/skills/here-company-consulting/SKILL.md`
**패턴:** Expert Pool + Supervisor
**변경 이력:** 2026-04-30 — 최초 생성
