# 천창성 영성 생태계 — 사용 가이드

## 자료를 넣는 곳 (한눈에 보기)

| 자료 종류 | 넣는 위치 |
|-----------|----------|
| **PPT, PPTX** — 워맥 요약 슬라이드, NotebookLM 슬라이드 | `source-files/ppt/` |
| **PDF** — NotebookLM 내보내기, 책 요약, 설교 자료 | `source-files/pdf/` |
| **DOCX, DOC** — Word 설교 노트, 강의 필기 | `source-files/docs/` |
| **TXT, MD** — 텍스트 메모, 신학 노트, 영상 요약 메모 | `source-files/text/` |

> 파일을 넣은 후 `python3 extract_to_knowledge.py` 한 번만 실행하면 자동으로 지식 베이스에 정리됩니다.

---

## 파일 추가하는 법 (3단계)

### 1단계: 파일 복사
```
PPT/PPTX  → _workspace/spirituality/source-files/ppt/
PDF       → _workspace/spirituality/source-files/pdf/
DOCX      → _workspace/spirituality/source-files/docs/
TXT/메모  → _workspace/spirituality/source-files/text/
```

### 2단계: 추출 실행
```bash
cd _workspace/spirituality
python3 extract_to_knowledge.py
```

### 3단계: 자동 분류 확인
파일 이름에 키워드가 있으면 자동으로 올바른 주제 폴더에 분류됩니다:

| 파일 이름 키워드 | 분류 폴더 |
|----------------|----------|
| `영혼몸`, `spirit` | spirit-soul-body/ |
| `권세`, `authority` | believers-authority/ |
| `은혜`, `grace` | grace-faith/ |
| `이미`, `already` | already-got-it/ |
| `노력`, `effortless` | effortless-change/ |
| `제한`, `limit` | dont-limit-god/ |
| `안식`, `sabbath` | sabbath/ |
| `정체성`, `identity` | identity/ |
| (기타) | general/ |

---

## 파일 이름 권장 형식

```
워맥_[주제]_[콘텐츠유형]_[날짜].확장자

예시:
  워맥_영혼몸_요약슬라이드_20260501.pptx
  워맥_권세_강의노트_20260501.pdf
  워맥_은혜와믿음_NotebookLM요약_20260501.pdf
  안식일신학_개인메모_20260501.txt
  정체성선언문_초안.md
```

---

## 전체 폴더 구조

```
spirituality/
├── GUIDE.md                       ← 이 파일
├── extract_to_knowledge.py        ← 추출 스크립트
│
├── source-files/                  ← 원본 파일 보관소 (여기에 넣으세요)
│   ├── ppt/                       ← PPT, PPTX
│   ├── pdf/                       ← PDF
│   ├── docs/                      ← DOCX, DOC
│   ├── text/                      ← TXT, MD
│   └── media/                     ← 영상 요약 텍스트
│
├── knowledge-base/                ← 자동 생성 (건드리지 않아도 됩니다)
│   ├── INDEX.md                   ← 전체 자산 인덱스
│   ├── chun-changseong-profile.md ← 천창성 신학 여정·원칙
│   ├── spirit-soul-body/
│   ├── believers-authority/
│   ├── grace-faith/
│   ├── already-got-it/
│   ├── effortless-change/
│   ├── dont-limit-god/
│   ├── sabbath/
│   ├── identity/
│   └── general/
│
├── processed/                     ← 처리 완료 원본 보관
└── content-library/               ← 생성된 강의·뉴스레터 저장
```

---

## 에이전트가 지식 베이스를 쓰는 방식

에이전트가 강의안·뉴스레터·Q&A를 생성할 때:

1. `INDEX.md` 확인 → 어떤 자료가 있는지 파악
2. `chun-changseong-profile.md` 확인 → 신학 원칙 적용
3. 해당 카테고리 `.md` 파일 읽기 → 실제 슬라이드·메모 내용 참조
4. 워맥의 언어 + 천창성의 신학 포지션으로 콘텐츠 생성
