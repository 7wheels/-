#!/usr/bin/env bash
#
# install-claude-skills.sh
#
# 공개 GitHub 저장소 7곳에서 Claude Code 스킬을 ~/.claude/skills 에 설치한다.
# 각 저장소를 임시 디렉터리에 얕게 클론한 뒤, 스킬 폴더만 복사하고 임시본을 지운다.
#
# 사용법:
#   bash scripts/install-claude-skills.sh            # 기본 설치 (기존 폴더는 건너뜀)
#   FORCE=1 bash scripts/install-claude-skills.sh    # 같은 이름 스킬을 덮어쓰기
#   SKILLS_DIR=/경로 bash scripts/install-claude-skills.sh  # 설치 위치 변경
#
# 설치 대상 (총 49개)
#   1. coreyhaines31/marketingskills  - competitor-profiling, pricing, offers, churn-prevention (4)
#   2. stevenflanagan1/social-ai-team - 전체 (10)
#   3. mathiaschu/meta-ads-analyzer   - skill/ 폴더 (1)
#   4. AgriciDaniel/claude-seo        - 코어 25 + 이름이 겹치지 않는 확장 6 (31)
#   5. lhitches/claude-seo-skills     - google-review-handler (1)
#   6. vpodugu/startup-bookkeeper     - 저장소 루트가 곧 스킬 (1)
#   7. mvanhorn/last30days-skill      - 전체 (1)

set -euo pipefail

SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"
FORCE="${FORCE:-0}"

command -v git >/dev/null 2>&1 || { echo "git 이 필요합니다." >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$SKILLS_DIR"

installed=0
skipped=0

# 스킬 디렉터리 하나를 설치한다. $1=원본 경로, $2=설치할 이름
install_skill() {
  local src="$1" name="$2" dest="$SKILLS_DIR/$2"
  if [ -e "$dest" ] && [ "$FORCE" != "1" ]; then
    echo "  건너뜀   $name (이미 존재. 덮어쓰려면 FORCE=1)"
    skipped=$((skipped + 1))
    return
  fi
  rm -rf "$dest"
  cp -r "$src" "$dest"
  rm -rf "$dest/.git"
  echo "  설치     $name"
  installed=$((installed + 1))
}

clone() {
  local repo="$1" name="${1##*/}"
  echo "클론 중: $repo"
  git clone --depth 1 --quiet "https://github.com/$repo.git" "$TMP/$name"
}

# --- 1. marketingskills: 지정한 4개만 --------------------------------------
clone coreyhaines31/marketingskills
for s in competitor-profiling pricing offers churn-prevention; do
  install_skill "$TMP/marketingskills/skills/$s" "$s"
done

# --- 2. social-ai-team: 전체 ------------------------------------------------
clone stevenflanagan1/social-ai-team
for s in "$TMP/social-ai-team/skills"/*/; do
  install_skill "$s" "$(basename "$s")"
done

# --- 3. meta-ads-analyzer ---------------------------------------------------
# 저장소의 스킬 폴더명이 일반명사 'skill' 이라, SKILL.md frontmatter 의 name 으로 설치한다.
clone mathiaschu/meta-ads-analyzer
install_skill "$TMP/meta-ads-analyzer/skill" "meta-ads-analyzer"

# --- 4. claude-seo: 코어 전체 + 확장 중 이름이 겹치지 않는 것 ---------------
# 확장(extensions/*)의 seo-image-gen, seo-dataforseo 는 코어와 이름이 같아 건너뛴다.
# 확장 스킬은 각자 MCP 서버 설정이 있어야 동작한다 (저장소의 extensions/*/install.sh 참고).
clone AgriciDaniel/claude-seo
core_names=" "
for s in "$TMP/claude-seo/skills"/*/; do
  name="$(basename "$s")"
  core_names="$core_names$name "
  install_skill "$s" "$name"
done
for s in "$TMP/claude-seo/extensions"/*/skills/*/; do
  name="$(basename "$s")"
  # 코어에 같은 이름이 있는 확장만 건너뛴다.
  # (설치 대상 폴더에 이미 있는지가 아니라, 이번 저장소의 코어 목록과 비교해야
  #  FORCE 재실행 때 확장 스킬이 잘못 건너뛰어지지 않는다.)
  case "$core_names" in
    *" $name "*)
      echo "  건너뜀   $name (확장 버전, 코어와 이름 중복)"
      skipped=$((skipped + 1))
      ;;
    *)
      install_skill "$s" "$name"
      ;;
  esac
done

# --- 5. claude-seo-skills: google-review-handler ----------------------------
# 이 저장소는 스킬이 평면 .md 파일이라, 규격에 맞게 <이름>/SKILL.md 로 바꿔 설치한다.
clone lhitches/claude-seo-skills
if [ -e "$SKILLS_DIR/google-review-handler" ] && [ "$FORCE" != "1" ]; then
  echo "  건너뜀   google-review-handler (이미 존재. 덮어쓰려면 FORCE=1)"
  skipped=$((skipped + 1))
else
  rm -rf "$SKILLS_DIR/google-review-handler"
  mkdir -p "$SKILLS_DIR/google-review-handler"
  cp "$TMP/claude-seo-skills/skills/google-review-handler.md" \
     "$SKILLS_DIR/google-review-handler/SKILL.md"
  echo "  설치     google-review-handler"
  installed=$((installed + 1))
fi

# --- 6. startup-bookkeeper: 저장소 루트가 곧 스킬 ---------------------------
clone vpodugu/startup-bookkeeper
if [ -e "$SKILLS_DIR/startup-bookkeeper" ] && [ "$FORCE" != "1" ]; then
  echo "  건너뜀   startup-bookkeeper (이미 존재. 덮어쓰려면 FORCE=1)"
  skipped=$((skipped + 1))
else
  rm -rf "$SKILLS_DIR/startup-bookkeeper"
  mkdir -p "$SKILLS_DIR/startup-bookkeeper"
  cp "$TMP/startup-bookkeeper/SKILL.md" "$SKILLS_DIR/startup-bookkeeper/"
  cp -r "$TMP/startup-bookkeeper/references" "$TMP/startup-bookkeeper/examples" \
        "$SKILLS_DIR/startup-bookkeeper/"
  echo "  설치     startup-bookkeeper"
  installed=$((installed + 1))
fi

# --- 7. last30days-skill: 전체 ---------------------------------------------
clone mvanhorn/last30days-skill
install_skill "$TMP/last30days-skill/skills/last30days" "last30days"

# --- 검증 ------------------------------------------------------------------
echo
echo "설치 위치: $SKILLS_DIR"
echo "설치 $installed 개, 건너뜀 $skipped 개"
echo
echo "SKILL.md 검증:"
problems=0
for d in "$SKILLS_DIR"/*/; do
  name="$(basename "$d")"
  [ -f "$d/SKILL.md" ] || { echo "  SKILL.md 없음: $name"; problems=$((problems + 1)); }
done
[ "$problems" -eq 0 ] && echo "  이상 없음"
echo
echo "설치된 스킬 목록:"
ls -1 "$SKILLS_DIR" | sed 's/^/  /'
