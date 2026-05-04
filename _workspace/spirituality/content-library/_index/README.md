# 콘텐츠 아키텍처 — 분리 운영

> 발행: 2026-05-04 | 작성: 영성
> Stage 0 후속 — 저장소·로컬 콘텐츠 분리 정책

---

## 왜 분리하는가

회당 1주분 풀세트 = 약 800줄. 1 트랙(12주) = 약 10,000줄. 8 트랙 풀가동 시 약 80,000줄. 한 저장소에 누적되면 클론·검수·이동이 모두 무거워진다.

**분리 정책:** 저장소는 **시스템(하네스·메타·골격)** 만, 로컬은 **콘텐츠(설교·교재·슬라이드·소그룹)** 만.

---

## 어디에 무엇이 사는가

### git 저장소 (가벼움 — 시스템)

```
_workspace/spirituality/
├── .claude/                     ← 에이전트·스킬 (영성·요한·… 7명)
├── CLAUDE.md / GUIDE.md         ← 하네스 레지스트리
├── 영성-작업지시.md               ← 오케스트레이션 로그
├── knowledge-base/              ← 신학·영성 지식베이스
├── source-files/                ← 워맥 원자료
├── extract_to_knowledge.py      ← 지식 추출 스크립트
├── youtube_to_knowledge.py
└── content-library/
    ├── _meta/                   ← 메타 7종 (모든 트랙 공통 기반)
    │   ├── program-portfolio.md
    │   ├── unified-theology.md
    │   ├── orthodoxy-firewall.md
    │   ├── content-template.md
    │   ├── slide-design-system.md
    │   ├── reusable-glossary.md
    │   ├── practice-template.md
    │   └── small-group-template.md
    ├── _index/                  ← 본 디렉토리 — 아키텍처·인덱스
    │   ├── README.md            ← 본 문서
    │   ├── content-manifest.md  ← 발행된 회당 인벤토리
    │   └── desktop-setup.md     ← 노트북 셋업 가이드
    └── wommack-track-{X}-{slug}/
        ├── 00_track-overview.md ← 12주 골격 (가벼움, 저장소 유지)
        ├── theology-statement.md
        ├── workbook-master.md
        └── (weeks/ 는 로컬에만 — gitignored)
```

### 노트북 바탕화면 (무거움 — 콘텐츠)

```
~/Desktop/Indwelling/
└── tracks/
    └── A-영혼몸/
        ├── week-01/
        │   ├── sermon.md
        │   ├── workbook.md
        │   ├── slides.md
        │   └── small-group.md
        ├── week-02/
        ├── …
        └── week-12/
```

회당 콘텐츠는 **여기서만 관리**. 저장소에 커밋하지 않는다.

---

## 처음 셋업 (한 번만)

노트북에서:

```bash
# 1. 저장소 클론
cd ~/Desktop
git clone https://github.com/7wheels/-.git Indwelling-repo

# 2. 콘텐츠 폴더 생성 (저장소와 별도)
mkdir -p ~/Desktop/Indwelling/tracks

# 3. 셋업 스크립트 실행 (트랙 골격을 콘텐츠 폴더에 미러링)
bash ~/Desktop/Indwelling-repo/_workspace/spirituality/scripts/setup-local.sh
```

상세: `desktop-setup.md` 참조.

---

## 작업 흐름

| 작업 | 위치 |
|------|------|
| 새 트랙 골격 작성 | 저장소 (커밋) |
| 메타 문서 갱신 | 저장소 (커밋) |
| 새 회당 콘텐츠 생성 | 노트북 `~/Desktop/Indwelling/` (커밋 안 함) |
| 회당 콘텐츠 검수·수정 | 노트북 (커밋 안 함) |
| 인벤토리 업데이트 | 저장소 `content-manifest.md` (커밋) |

---

## .gitignore 정책

저장소 루트의 `.gitignore` 가 다음을 제외한다:

```
_workspace/spirituality/content-library/**/weeks/
_workspace/spirituality/_local/
_workspace/spirituality/_drafts/
```

**즉, weeks/ 디렉토리는 git에 들어가지 않는다.** 실수로 커밋되지 않게 자동 차단.

---

## 마이그레이션 (2026-05-04 기준)

W1~W9 콘텐츠 36개 파일을 저장소에서 분리:
- 저장소에서 git rm
- `~/Desktop/Indwelling/tracks/A-영혼몸/`에 사본 보존
- 이후 W10~W12부터는 처음부터 노트북 폴더에서 작업

저장소 라인 수: 9,295 → 약 2,400 (메타 + 골격만 유지)

---

## 변경 이력

- 2026-05-04 — 분리 아키텍처 도입. 콘텐츠 라인 수 무한 증가 차단.
