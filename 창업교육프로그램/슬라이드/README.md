# 강의 슬라이드 (Marp)

5주 강의 덱입니다. 소스는 **Marp 마크다운**이고, 렌더링된 **PDF**와 **PPTX**가 함께 들어 있습니다.

## 파일 구성

| 주차 | 소스(.md) | PDF | PPTX |
|---|---|---|---|
| 1주 | `1주차_마인드셋_성향진단.md` | `pdf/` | `pptx/` |
| 2주 | `2주차_아이템발굴_검증설계.md` | `pdf/` | `pptx/` |
| 3주 | `3주차_검증게이트_구조화.md` | `pdf/` | `pptx/` |
| 4주 | `4주차_특허전략_출원준비.md` | `pdf/` | `pptx/` |
| 5주 | `5주차_사업계획서_데모데이.md` | `pdf/` | `pptx/` |

- **PDF**: 그대로 화면에 띄워 강의하거나 인쇄
- **PPTX**: 파워포인트에서 열어 로고·색·내용 수정 (각 슬라이드는 이미지로 들어갑니다 → 텍스트 편집은 소스 .md에서)

## 다시 렌더링하는 법

소스(.md)를 수정한 뒤 아래로 다시 변환합니다. (Node.js 필요)

```bash
# PDF
npx @marp-team/marp-cli@latest 1주차_마인드셋_성향진단.md --pdf -o pdf/1주차_마인드셋_성향진단.pdf

# PPTX
npx @marp-team/marp-cli@latest 1주차_마인드셋_성향진단.md --pptx -o pptx/1주차_마인드셋_성향진단.pptx

# 편집하며 미리보기 (브라우저 자동 새로고침)
npx @marp-team/marp-cli@latest -s .
```

> PDF/PPTX 변환에는 Chromium이 필요합니다. 없으면 `npx puppeteer browsers install chrome` 후
> 환경변수 `CHROME_PATH`에 설치 경로를 지정하세요.
> VS Code를 쓴다면 **Marp for VS Code** 확장으로 미리보기·내보내기가 더 편합니다.

## 디자인 수정

각 .md 상단 `style:` 블록에서 글꼴·색을 바꿉니다.
- 제목색 `h1/h2` = `#1D4ED8`(파랑), 강조 `strong` = `#B45309`(주황)
- 한글 글꼴: `Noto Sans CJK KR` → 없으면 시스템 고딕으로 대체됨
