# 저장소 분리 결정 — A1 (트랙별 별도 저장소)

> 발행: 2026-05-04 | 결정: 사용자 (옵션 A1)
> 트랙 A·F 완마감 시점 — 라인 24,515줄, 임계 30,000 임박

---

## 1. 결정 내용

### A1: 트랙별 별도 GitHub 저장소

각 트랙이 독립된 GitHub 저장소에 살게 한다. 메인 저장소(`7wheels/-`)는 **하네스·메타·인덱스만** 가벼운 상태로 유지.

### 저장소 구조 (목표)

```
GitHub:
├── 7wheels/-                          ← 메인 (하네스·메타·인덱스)
│   └── _workspace/spirituality/
│       ├── .claude/                   (에이전트·스킬)
│       ├── content-library/
│       │   ├── _meta/                 (메타 7종)
│       │   ├── _index/                (인덱스·매니페스트)
│       │   └── tracks-readonly/       (각 트랙 골격·신학 진술서·레드팀만)
│       ├── knowledge-base/
│       └── source-files/
│
├── 7wheels/indwelling-track-A         ← 트랙 A 콘텐츠 (별도)
│   └── weeks/                         (12회당 4종 = 48 파일)
│
├── 7wheels/indwelling-track-F         ← 트랙 F 콘텐츠 (별도)
│   └── weeks/
│
└── 7wheels/indwelling-track-C         ← 다음 트랙 (생성 예정)
    └── weeks/
```

---

## 2. 무엇이 어디로

### 메인 저장소 `7wheels/-`에 유지

- `.claude/` (에이전트 7명 + 스킬)
- `content-library/_meta/` (메타 7종)
- `content-library/_index/` (인덱스·매니페스트·아키텍처)
- 각 트랙의 메타급 산출물 (작아서 메인에 둠):
  - `00_track-overview.md` (12주 골격)
  - `theology-statement.md`
  - `red-team-review.md`
- `knowledge-base/`
- `source-files/`
- `scripts/`

**예상 라인 수 (분리 후 메인):** 약 5,000줄 — **임계 한참 아래**

### 트랙별 저장소로 이동

각 트랙의 `weeks/` 폴더만 별도 저장소로:
- `7wheels/indwelling-track-A` ← 현재 `wommack-track-A-spirit-soul-body/weeks/`
- `7wheels/indwelling-track-F` ← 현재 `wommack-track-F-already-got-it/weeks/`

**각 트랙 저장소 라인 수:** 약 9,000줄 — 가벼움

---

## 3. 마이그레이션 단계 (사용자 액션 필요)

### Step 1: 사용자가 GitHub에 새 저장소 생성

```
1. https://github.com/new 에서 두 개 생성:
   - 이름: indwelling-track-A
   - 이름: indwelling-track-F
   - 둘 다 private (또는 public — 선택)
   - 빈 저장소로 (README·gitignore 자동 생성 X)
```

### Step 2: 영성에게 저장소 생성 완료 알림

저장소 URL을 공유해주시면, 마이그레이션 스크립트가 자동으로:
- 메인에서 `weeks/` 콘텐츠를 새 저장소로 push
- 메인에서 `weeks/` 폴더 git rm
- `.gitignore`로 향후 재추적 차단
- 인덱스·매니페스트 갱신 (각 트랙의 새 저장소 URL 명시)

### Step 3: 검증

마이그레이션 후:
- 메인 저장소 라인 수 ~5,000줄 확인
- 트랙 A·F 새 저장소에서 콘텐츠 접근 확인
- 노트북에서 각 저장소 클론·작업

---

## 4. 노트북 작업 흐름 변경

### 처음 셋업 (분리 후)

```bash
cd ~/Desktop
mkdir Indwelling
cd Indwelling

# 메인 (하네스·메타)
git clone https://github.com/7wheels/-.git core

# 트랙별 (필요한 트랙만 클론)
git clone https://github.com/7wheels/indwelling-track-A.git track-A
git clone https://github.com/7wheels/indwelling-track-F.git track-F
```

### 일상 작업

| 작업 | 위치 |
|------|------|
| 메타·골격·신학 진술서 변경 | `~/Desktop/Indwelling/core/` (메인) |
| 트랙 A 회당 콘텐츠 변경 | `~/Desktop/Indwelling/track-A/` |
| 트랙 F 회당 콘텐츠 변경 | `~/Desktop/Indwelling/track-F/` |
| 새 트랙 생성 | 새 GitHub 저장소 + 클론 |

---

## 5. 다음 트랙 (C 등) 시작 시

### Step 1: 트랙 C 골격 작성 (메인 저장소)

영성이 메인 저장소에 트랙 C의 다음을 작성:
- `00_track-overview.md`
- (이후 종료 시) `theology-statement.md`·`red-team-review.md`

### Step 2: 사용자가 트랙 C 저장소 생성

```
GitHub: indwelling-track-C
```

### Step 3: 영성이 회당 콘텐츠를 트랙 C 저장소에 작성

W1~W12 회당 콘텐츠 모두 새 저장소에서.

---

## 6. 임시 대안 (사용자 GitHub 저장소 생성 전)

새 저장소가 만들어지기 전까지는 **현재 구조 유지**. 즉:
- 트랙 A·F 회당 콘텐츠는 메인에 그대로 유지
- 트랙 C는 시작하지 않음
- 메인 라인 수는 24,515 → 임계 미초과 상태로 유지

**트랙 C 시작 = 분리 마이그레이션 완료 시점.**

---

## 7. 마이그레이션 자동화 스크립트

`_workspace/spirituality/scripts/split-tracks.sh` (다음 커밋에 포함)이 다음을 자동화:

1. 새 저장소 URL 입력 받음
2. 메인에서 트랙 콘텐츠를 새 저장소로 push
3. 메인에서 git rm (히스토리 보존)
4. .gitignore 갱신
5. 매니페스트 갱신
6. 검증

사용자는 새 저장소 URL만 공유하면 됨.

---

## 8. 결정 영향 요약

| 항목 | 분리 전 | 분리 후 |
|------|--------|--------|
| 메인 저장소 라인 | 24,515 | ~5,000 |
| 클론 무게 | 무거움 (트랙 8개 시 100k+) | 트랙별 가벼움 |
| 트랙 추가 | 메인 부담 | 새 저장소만 |
| 메타·골격 검색 | 한 곳 | 메인에 한 곳 (변동 없음) |
| 사용자 클론 | 1개 | 메인 + 필요 트랙만 (선택적) |
| 협업 | 한 저장소 권한 | 트랙별 권한 (세분화 가능) |

---

## 9. 변경 이력

- 2026-05-04 — A1 결정 (트랙별 별도 저장소)
- 2026-05-04 — 본 문서 발행
- 향후 — 사용자 GitHub 저장소 생성 후 실제 마이그레이션 진행
