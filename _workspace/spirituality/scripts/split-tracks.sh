#!/usr/bin/env bash
# 트랙 저장소 분리 마이그레이션 스크립트
# 사용자가 새 GitHub 저장소를 생성한 후 실행
#
# 사용법:
#   bash split-tracks.sh <track-code> <new-repo-url>
#
# 예:
#   bash split-tracks.sh A https://github.com/7wheels/indwelling-track-A.git
#   bash split-tracks.sh F https://github.com/7wheels/indwelling-track-F.git

set -e

TRACK_CODE="${1:-}"
NEW_REPO_URL="${2:-}"

if [ -z "$TRACK_CODE" ] || [ -z "$NEW_REPO_URL" ]; then
  cat <<EOF
사용법: bash split-tracks.sh <track-code> <new-repo-url>

예시:
  bash split-tracks.sh A https://github.com/7wheels/indwelling-track-A.git
  bash split-tracks.sh F https://github.com/7wheels/indwelling-track-F.git

지원 트랙 코드: A, B, C, D, E, F, G, H
EOF
  exit 1
fi

# 트랙 코드 → 디렉토리 매핑
case "$TRACK_CODE" in
  A) TRACK_DIR="wommack-track-A-spirit-soul-body"; TRACK_NAME="A-영혼몸" ;;
  B) TRACK_DIR="wommack-track-B-believers-authority"; TRACK_NAME="B-믿는자의권세" ;;
  C) TRACK_DIR="wommack-track-C-grace-and-faith"; TRACK_NAME="C-은혜와믿음" ;;
  D) TRACK_DIR="wommack-track-D-dont-limit-god"; TRACK_NAME="D-하나님제한금지" ;;
  E) TRACK_DIR="wommack-track-E-effortless-change"; TRACK_NAME="E-노력없는변화" ;;
  F) TRACK_DIR="wommack-track-F-already-got-it"; TRACK_NAME="F-이미가졌다" ;;
  G) TRACK_DIR="wommack-track-G-discover-gods-will"; TRACK_NAME="G-하나님의뜻" ;;
  H) TRACK_DIR="wommack-track-H-financial-stewardship"; TRACK_NAME="H-재정청지기" ;;
  *) echo "ERROR: 알 수 없는 트랙 코드: $TRACK_CODE"; exit 1 ;;
esac

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SOURCE_WEEKS="$REPO_ROOT/_workspace/spirituality/content-library/$TRACK_DIR/weeks"
TEMP_DIR="/tmp/track-$TRACK_CODE-migration-$$"

echo "════════════════════════════════════════════"
echo "  트랙 $TRACK_CODE ($TRACK_NAME) 저장소 분리"
echo "════════════════════════════════════════════"
echo ""
echo "메인 저장소: $REPO_ROOT"
echo "원본 weeks: $SOURCE_WEEKS"
echo "새 저장소 URL: $NEW_REPO_URL"
echo ""

# 1. 원본 확인
if [ ! -d "$SOURCE_WEEKS" ]; then
  echo "ERROR: $SOURCE_WEEKS 가 존재하지 않습니다."
  exit 1
fi

read -p "이 마이그레이션을 진행하시겠습니까? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
  echo "취소됨."
  exit 0
fi

# 2. 임시 디렉토리에 새 저장소 생성
echo ""
echo "[1/5] 새 저장소 초기화…"
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"
git init -b main

# 3. weeks 콘텐츠 복사
echo "[2/5] 트랙 콘텐츠 복사…"
mkdir -p weeks
cp -r "$SOURCE_WEEKS/." weeks/

# 4. 트랙 README 생성
cat > README.md <<EOF
# 트랙 $TRACK_CODE — $TRACK_NAME

> 내주(Indwelling) 영성공동체 — 트랙별 콘텐츠 저장소
> 메인 저장소: https://github.com/7wheels/-

## 구조

\`\`\`
weeks/
├── week-01/  (sermon·workbook·slides·small-group)
├── week-02/
├── …
└── week-12/
\`\`\`

## 메타·골격·신학 진술서

이 트랙의 메타급 산출물(트랙 골격·신학 진술서·레드팀 검토)은 **메인 저장소**에 있습니다:

- https://github.com/7wheels/-/tree/main/_workspace/spirituality/content-library/$TRACK_DIR/

## 사용법

회당 콘텐츠를 사용·수정하려면:

\`\`\`bash
cd ~/Desktop/Indwelling
git clone $NEW_REPO_URL track-$TRACK_CODE
cd track-$TRACK_CODE
\`\`\`

## 주의

본 저장소는 회당 풀세트만 담습니다. 메타·골격·신학 진술서는 메인 저장소를 참조하세요.
EOF

# 5. 첫 커밋
echo "[3/5] 첫 커밋 생성…"
git add -A
git commit -m "Initial migration from main repo — track $TRACK_CODE ($TRACK_NAME) weekly content"

# 6. 원격 push
echo "[4/5] 원격 저장소에 push…"
git remote add origin "$NEW_REPO_URL"
git push -u origin main

# 7. 메인 저장소에서 git rm
echo "[5/5] 메인 저장소에서 weeks/ 제거…"
cd "$REPO_ROOT"
git rm -r "_workspace/spirituality/content-library/$TRACK_DIR/weeks/"

# 8. .gitignore 갱신
GITIGNORE_LINE="_workspace/spirituality/content-library/$TRACK_DIR/weeks/"
if ! grep -qF "$GITIGNORE_LINE" "$REPO_ROOT/.gitignore" 2>/dev/null; then
  echo "$GITIGNORE_LINE" >> "$REPO_ROOT/.gitignore"
fi

# 9. 트랙 디렉토리에 분리 안내 README 생성
mkdir -p "$REPO_ROOT/_workspace/spirituality/content-library/$TRACK_DIR"
cat > "$REPO_ROOT/_workspace/spirituality/content-library/$TRACK_DIR/SPLIT-NOTICE.md" <<EOF
# 본 트랙 회당 콘텐츠는 별도 저장소로 이전됨

> 이전일: $(date '+%Y-%m-%d')

## 새 저장소

$NEW_REPO_URL

## 메인에 남은 것

- \`00_track-overview.md\` (12주 골격)
- \`theology-statement.md\` (신학 진술서)
- \`red-team-review.md\` (레드팀 검토)

## 회당 콘텐츠 (weeks/)

본 메인 저장소에는 더 이상 없습니다. 위 새 저장소에서 클론하세요.
EOF

echo ""
echo "════════════════════════════════════════════"
echo "  ✅ 트랙 $TRACK_CODE 마이그레이션 완료"
echo "════════════════════════════════════════════"
echo ""
echo "다음 단계:"
echo "  1. 메인 저장소 git status 확인"
echo "  2. 변경 사항 커밋·푸시"
echo "  3. 새 저장소 검증: $NEW_REPO_URL"
echo ""
echo "임시 디렉토리: $TEMP_DIR (수동 제거 가능)"
