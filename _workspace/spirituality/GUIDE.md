# 천창성 영성 생태계 — 사용 가이드

## NotebookLM 파일을 지식 베이스에 추가하는 법

### 1단계: 파일 복사
```
PPT 파일 → _workspace/spirituality/source-files/ppt/
PDF 파일 → _workspace/spirituality/source-files/pdf/
```

### 2단계: 추출 실행
```bash
cd _workspace/spirituality
python3 extract_to_knowledge.py
```

### 3단계: 자동 분류 확인
파일 이름에 키워드가 있으면 자동 분류됩니다:

| 파일 이름 키워드 | 분류 폴더 |
|----------------|----------|
| 영혼몸, spirit | spirit-soul-body/ |
| 권세, authority | believers-authority/ |
| 은혜, grace | grace-faith/ |
| 이미, already | already-got-it/ |
| 노력, effortless | effortless-change/ |
| 제한, limit | dont-limit-god/ |
| 안식, sabbath | sabbath/ |
| 정체성, identity | identity/ |
| (기타) | general/ |

---

## 에이전트가 지식 베이스를 쓰는 방식

에이전트가 강의안·뉴스레터·Q&A를 생성할 때:

1. `INDEX.md` 확인 → 관련 자료 목록 파악
2. `chun-changseong-profile.md` 확인 → 신학 원칙 적용
3. 해당 카테고리 `.md` 파일 읽기 → 실제 슬라이드 내용 참조
4. 워맥의 언어 + 천창성의 신학 포지션으로 콘텐츠 생성

---

## 폴더 구조

```
spirituality/
├── GUIDE.md                      ← 이 파일
├── extract_to_knowledge.py       ← 추출 스크립트
├── source-files/
│   ├── ppt/                      ← NotebookLM PPT 파일 여기에
│   └── pdf/                      ← PDF 파일 여기에
├── knowledge-base/
│   ├── INDEX.md                  ← 전체 자산 인덱스 (자동 생성)
│   ├── chun-changseong-profile.md
│   ├── spirit-soul-body/
│   ├── believers-authority/
│   ├── grace-faith/
│   ├── already-got-it/
│   ├── effortless-change/
│   ├── dont-limit-god/
│   ├── sabbath/
│   ├── identity/
│   └── general/
├── processed/                    ← 처리 완료 파일 보관
└── content-library/              ← 생성된 강의·뉴스레터 저장
```

---

## 파일 이름 권장 형식

```
워맥_[주제]_[콘텐츠유형]_[날짜].pptx
예시:
  워맥_영혼몸_요약슬라이드_20260501.pptx
  워맥_권세_강의노트_20260501.pdf
  워맥_은혜와믿음_NotebookLM요약_20260501.pdf
```
