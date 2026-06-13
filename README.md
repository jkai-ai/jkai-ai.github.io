# 📄 Daily Insights — GitHub Pages 학습 예제

GitHub Pages 배포, HTML/CSS/JS 기초, 자동화 연결을 한 번에 배울 수 있는 예제 프로젝트입니다.

---

## 📁 파일 구조

```
/
├── index.html                    # 메인 페이지 (뼈대)
├── style.css                     # 스타일 (디자인)
├── script.js                     # 기능 (명언 표시, 데이터 로드)
├── data/
│   └── contents.json             # 카드에 표시될 콘텐츠 데이터
└── .github/
    └── workflows/
        └── update-data.yml       # GitHub Actions 자동화 예제
```

---

## 🚀 GitHub Pages 배포 방법

1. 이 파일들을 GitHub 저장소에 업로드합니다
2. 저장소 **Settings → Pages** 로 이동합니다
3. Source를 **"Deploy from a branch"**, Branch를 **main** 으로 설정합니다
4. 저장 후 1~2분 뒤 `https://[아이디].github.io/[저장소명]` 으로 접속합니다

---

## 📝 콘텐츠 수정 방법

### 명언 추가/변경
`script.js` 파일 상단의 `quotes` 배열에 항목을 추가하세요:
```js
{
  text: "영어 명언",
  translation: "한글 해석",
  author: "출처"
},
```

### 카드 내용 변경
`data/contents.json` 파일을 직접 편집하세요.  
각 `items` 배열 안에 항목을 추가/수정합니다.

---

## 🤖 GitHub Actions 자동화 연결

1. `update_data.py` 파이썬 스크립트를 작성합니다  
   (뉴스 RSS, API 등에서 데이터를 수집하여 `data/contents.json`을 업데이트)
2. `.github/workflows/update-data.yml` 이 매일 자동으로 스크립트를 실행합니다
3. JSON이 업데이트되면 웹페이지도 자동으로 최신 내용을 표시합니다

---

## 🎓 학습 포인트

| 파일 | 배울 수 있는 것 |
|------|----------------|
| `index.html` | HTML 기본 구조, 시맨틱 태그, 외부 파일 연결 |
| `style.css` | CSS 변수, Flexbox/Grid, 반응형(@media), 애니메이션 |
| `script.js` | 배열/객체, fetch API, async/await, DOM 조작 |
| `contents.json` | JSON 데이터 구조 설계 |
| `update-data.yml` | GitHub Actions 스케줄 자동화 |
