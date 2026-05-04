# 콘텐츠 아키텍처 — 정정판

> 발행: 2026-05-04 | 수정: 2026-05-04
> Stage 0 후속 — **현실에 맞게 재설계**

---

## 정정 배경

처음 설계는 "콘텐츠는 노트북 바탕화면 폴더에, 저장소는 가볍게"였다. 그러나 **AI는 사용자 노트북의 실제 바탕화면에 파일을 쓸 수 없다.** AI가 사용자에게 콘텐츠를 전달하는 유일한 통로는 **GitHub 저장소** 자체다.

따라서 아키텍처를 재설계한다 — **콘텐츠는 저장소에서 관리하되, 사용자가 노트북에 클론하면 자동으로 바탕화면 폴더가 된다.**

---

## 새 아키텍처 (현실 기반)

### 1. 모든 것은 git 저장소 안에 있다

콘텐츠·메타·골격·스크립트 모두 저장소에 commit된다. 사용자가 GitHub에서 보거나, 클론해서 노트북에서 본다.

### 2. 사용자가 클론하는 위치 = 사용자의 "바탕화면 폴더"

```bash
cd ~/Desktop
git clone https://github.com/7wheels/-.git Indwelling
```

→ `~/Desktop/Indwelling/_workspace/spirituality/content-library/.../weeks/week-01/sermon.md` 가 노트북 바탕화면에서 바로 접근 가능.

**별도 "Desktop 폴더 복사" 단계 불필요.** 클론한 폴더가 곧 작업 폴더.

### 3. 라인 수 폭증을 어떻게 막는가

저장소가 너무 커지지 않게 하는 5가지 정책:

| 정책 | 내용 |
|------|------|
| **트랙별 분리** | 트랙 8개를 모두 한 저장소에 두지 않고, 트랙 B부터는 **별도 브랜치** 또는 **별도 저장소**로 운영 |
| **회당 분량 표준** | 회당당 sermon 4천자·workbook 4쪽·slides 25매·small-group 90분 — 표준 초과 금지 |
| **메타 재사용** | 모든 트랙이 `_meta/` 7종을 공유. 트랙별로 중복 작성 X |
| **드래프트 분리** | `_drafts/`는 git 추적 안 함. 작업 중인 초안은 거기에 |
| **검수 후 발행** | 회당당 검수 한 번 통과 후 발행 — 무한 수정 방지 |

### 4. 노트북에서 작업 흐름

```bash
# 처음 한 번
cd ~/Desktop
git clone https://github.com/7wheels/-.git Indwelling
cd Indwelling
git checkout claude/load-spiritual-harness-wVfhp

# 일상
git pull                           # AI가 발행한 최신 콘텐츠 받음
# (탐색기로 바로 파일 열어서 읽음)
# (수정·메모 필요하면 _drafts/ 안에 — git 추적 안 됨)
```

---

## 디렉토리 구조 (현재)

```
~/Desktop/Indwelling/                        ← 사용자가 클론한 위치
└── _workspace/spirituality/
    ├── .claude/                             ← 하네스 (에이전트·스킬)
    ├── CLAUDE.md / GUIDE.md
    ├── 영성-작업지시.md
    ├── knowledge-base/                      ← 신학 지식베이스
    ├── source-files/                        ← 원자료
    ├── scripts/
    │   └── setup-local.sh                   (선택적 사용)
    └── content-library/
        ├── _meta/                           ← 메타 7종 (모든 트랙 공통)
        ├── _index/
        │   ├── README.md                    ← 본 문서
        │   ├── content-manifest.md
        │   └── desktop-setup.md
        └── wommack-track-A-spirit-soul-body/
            ├── 00_track-overview.md
            └── weeks/
                ├── week-01/                 (sermon·workbook·slides·small-group)
                ├── week-02/
                └── … week-12/
```

---

## 라인 수 모니터링

| 시점 | 저장소 라인 |
|------|-----------|
| W1~W6 발행 후 | 9,295 |
| W7~W9 발행 후 | 11,439 |
| W10~W12 발행 후 (예상) | 약 13,800 |

트랙 A 완주 시 약 14,000줄. 8 트랙 완주 시 약 100,000줄 — **이 시점에서는 트랙별 분리가 필요**.

### 트랙 분리 시점

다음 중 하나가 발생하면 새 트랙을 별도 저장소·브랜치로 분리:
- 저장소 라인 수 30,000줄 도달
- 클론 시간 30초 초과
- 한 트랙이 다른 트랙 콘텐츠를 참조하지 않음 확인 (메타 통해 충분)

**현재 (트랙 A 완주 시점):** 한 저장소 유지. 트랙 B 시작 시 분리 검토.

---

## 변경 이력

- 2026-05-04 — 초안: "노트북 바탕화면 폴더" 아키텍처 (실패 — AI는 사용자 노트북에 직접 쓸 수 없음)
- 2026-05-04 — **정정**: 저장소 = 작업 폴더. 클론한 위치가 곧 바탕화면. W1~W12 콘텐츠 복원.
