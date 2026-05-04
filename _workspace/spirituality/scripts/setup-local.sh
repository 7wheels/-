#!/usr/bin/env bash
# 내주(Indwelling) 영성공동체 — 로컬 콘텐츠 폴더 셋업
# 처음 한 번만 실행

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SPIR="$REPO_ROOT/_workspace/spirituality"
LOCAL="$HOME/Desktop/Indwelling"

echo "════════════════════════════════════════════"
echo "  내주(Indwelling) — 로컬 콘텐츠 셋업"
echo "════════════════════════════════════════════"
echo ""
echo "저장소 위치: $REPO_ROOT"
echo "로컬 콘텐츠 위치: $LOCAL"
echo ""

# 1. 콘텐츠 폴더 생성
echo "[1/4] 폴더 구조 생성…"
mkdir -p "$LOCAL/tracks"
mkdir -p "$LOCAL/_meta-readonly-mirror"

# 2. 트랙 골격 미러링 (읽기 전용 참조용)
echo "[2/4] 트랙 골격 미러링…"
for track in "$SPIR/content-library"/wommack-track-*; do
  if [ -d "$track" ]; then
    name=$(basename "$track")
    # 코드명 추출 (wommack-track-A-spirit-soul-body → A-영혼몸 등 매핑)
    case "$name" in
      *track-A*) display="A-영혼몸" ;;
      *track-B*) display="B-믿는자의권세" ;;
      *track-C*) display="C-은혜와믿음" ;;
      *track-D*) display="D-하나님제한금지" ;;
      *track-E*) display="E-노력없는변화" ;;
      *track-F*) display="F-이미가졌다" ;;
      *track-G*) display="G-하나님의뜻" ;;
      *track-H*) display="H-재정청지기" ;;
      *) display="$name" ;;
    esac
    mkdir -p "$LOCAL/tracks/$display"
    if [ -f "$track/00_track-overview.md" ]; then
      cp "$track/00_track-overview.md" "$LOCAL/tracks/$display/_track-overview.md"
    fi
  fi
done

# 3. 메타 미러링 (참조용 — 편집은 저장소에서)
echo "[3/4] 메타 7종 미러링 (참조용)…"
if [ -d "$SPIR/content-library/_meta" ]; then
  cp -r "$SPIR/content-library/_meta/." "$LOCAL/_meta-readonly-mirror/"
fi

# 4. 안내 파일
echo "[4/4] 안내 파일 생성…"
cat > "$LOCAL/00_시작하세요.md" <<'EOF'
# 내주(Indwelling) — 로컬 콘텐츠 폴더

## 폴더 구조

- `tracks/` — 회당 콘텐츠 (설교·교재·슬라이드·소그룹)
- `_meta-readonly-mirror/` — 메타 7종 참조용 (편집 금지, 저장소에서 수정)

## 새 회당 작성 시

1. `tracks/A-영혼몸/week-NN/` 폴더 만들기
2. 4종 파일 작성: sermon.md / workbook.md / slides.md / small-group.md
3. 저장소의 `content-manifest.md` 갱신
4. 콘텐츠는 저장소에 커밋하지 않음

## 동기화

- 저장소: `cd ~/Desktop/Indwelling-repo && git pull`
- 콘텐츠: iCloud / 드롭박스 / 별도 private repo 권장

## 주의

- 이 폴더 (`~/Desktop/Indwelling/`)는 **git에 들어가지 않는다**
- 콘텐츠 백업은 본인 책임
- 저장소(`~/Desktop/Indwelling-repo/`)와는 별개
EOF

echo ""
echo "════════════════════════════════════════════"
echo "  ✅ 셋업 완료"
echo "════════════════════════════════════════════"
echo ""
echo "다음 단계:"
echo "  1. cd $LOCAL"
echo "  2. cat 00_시작하세요.md"
echo "  3. tracks/ 안에서 회당 콘텐츠 작성"
echo ""
echo "저장소 변경 시: cd $REPO_ROOT && git pull"
