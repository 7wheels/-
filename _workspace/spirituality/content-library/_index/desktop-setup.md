# 노트북 셋업 가이드

> 처음 한 번만 실행. 이후는 일상 동기화만.

---

## 1. 처음 셋업

### macOS / Linux

```bash
# 1. 저장소 클론 (시스템·메타·골격)
cd ~/Desktop
git clone https://github.com/7wheels/-.git Indwelling-repo

# 2. 콘텐츠 폴더 생성 (저장소와 분리)
mkdir -p ~/Desktop/Indwelling/tracks

# 3. 셋업 스크립트 실행
bash ~/Desktop/Indwelling-repo/_workspace/spirituality/scripts/setup-local.sh
```

### Windows (PowerShell)

```powershell
cd ~\Desktop
git clone https://github.com/7wheels/-.git Indwelling-repo
New-Item -ItemType Directory -Force -Path "~\Desktop\Indwelling\tracks"
bash "~\Desktop\Indwelling-repo\_workspace\spirituality\scripts\setup-local.sh"
```

(WSL 또는 Git Bash 권장)

---

## 2. 폴더 구조 (셋업 완료 후)

```
~/Desktop/
├── Indwelling-repo/             ← git 저장소 (가벼움)
│   └── _workspace/spirituality/
│       └── content-library/
│           ├── _meta/           ← 메타 7종
│           └── wommack-track-A-spirit-soul-body/
│               └── 00_track-overview.md
│
└── Indwelling/                  ← 콘텐츠 (무거움, git 추적 X)
    └── tracks/
        └── A-영혼몸/
            ├── week-01/
            ├── week-02/
            └── …
```

두 폴더가 **나란히** 있다. Indwelling-repo는 `git pull` 로 업데이트, Indwelling은 자유롭게 편집.

---

## 3. 일상 작업 흐름

### 새 회당 작성 시

1. 저장소에서 골격·메타 확인 (`Indwelling-repo/.../00_track-overview.md`)
2. 콘텐츠 4종 작성 → `~/Desktop/Indwelling/tracks/A-영혼몸/week-{NN}/`
3. 매니페스트 갱신: `Indwelling-repo/.../content-manifest.md`
4. 매니페스트만 커밋·푸시 (콘텐츠는 자동 제외)

### 메타·골격 변경 시

1. `Indwelling-repo/`에서 편집
2. 평소처럼 git 커밋·푸시

### 다른 디바이스에서 작업할 때

1. 저장소: `git pull` 로 동기화
2. 콘텐츠: 별도 동기화 필요 (드롭박스/iCloud/구글드라이브 권장)

---

## 4. 콘텐츠 백업 (권장)

회당 콘텐츠는 git에 들어가지 않으므로 별도 백업이 필수.

| 옵션 | 비고 |
|------|------|
| **iCloud Drive** (Mac) | `~/Desktop/Indwelling/`을 iCloud Drive 안에 두면 자동 동기화 |
| **드롭박스 / 구글드라이브** | 마찬가지로 동기화 폴더 안에 배치 |
| **별도 git 저장소** (private) | `Indwelling/` 폴더를 별도 private repo로 — 가장 안전 |
| **로컬 외장하드** | 주 1회 수동 백업 |

---

## 5. 자주 묻는 질문

### Q. 왜 한 저장소에서 다 관리하지 않는가?
A. 회당 1주분이 약 800줄. 트랙 8개 × 12주 = 약 80,000줄. 한 저장소에 누적되면 클론·검수·동기화 모두 무거워진다.

### Q. 콘텐츠가 git에 안 들어가면 협업은?
A. 협업이 필요하면 **별도 private 저장소**를 권장한다. 또는 드롭박스 공유 폴더.

### Q. 저장소에서 weeks/ 디렉토리가 안 보인다
A. 정상. `.gitignore`로 제외되어 있다. 콘텐츠는 `~/Desktop/Indwelling/`에 있다.

### Q. 실수로 콘텐츠를 저장소 폴더에 만들면?
A. `.gitignore`가 자동으로 차단한다. `git status`에 안 나타난다. 안전.
