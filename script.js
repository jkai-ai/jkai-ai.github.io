/* ============================================================
   script.js — GitHub Pages 학습용 자바스크립트
   두 가지 핵심 기능:
   1. 랜덤 명언 표시
   2. JSON 파일에서 콘텐츠 카드 불러오기
   ============================================================ */

/* ── 1. 명언 데이터 ────────────────────────────────────────────
   배열(Array): 여러 개의 데이터를 순서대로 저장하는 구조입니다.
   각 항목은 { } 중괄호로 감싼 객체(Object)이며
   text(영어), translation(한글), author(출처) 세 가지 정보를 담습니다.
   새 명언을 추가하려면 쉼표로 구분하여 객체를 하나 더 붙여넣으면 됩니다.
   ────────────────────────────────────────────────────────── */
const quotes = [
  {
    text: "The secret of getting ahead is getting started.",
    translation: "앞서 나가는 비결은 시작하는 것입니다.",
    author: "Mark Twain"
  },
  {
    text: "It does not matter how slowly you go as long as you do not stop.",
    translation: "멈추지 않는 한, 얼마나 천천히 가는지는 중요하지 않습니다.",
    author: "Confucius"
  },
  {
    text: "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    translation: "성공은 끝이 아니고, 실패는 치명적이지 않습니다. 중요한 것은 계속할 용기입니다.",
    author: "Winston Churchill"
  },
  {
    text: "Believe you can and you're halfway there.",
    translation: "할 수 있다고 믿는 순간, 이미 절반은 온 것입니다.",
    author: "Theodore Roosevelt"
  },
  {
    text: "Your time is limited, so don't waste it living someone else's life.",
    translation: "당신의 시간은 한정되어 있습니다. 다른 사람의 삶을 사는 데 낭비하지 마세요.",
    author: "Steve Jobs"
  },
  {
    text: "The only way to do great work is to love what you do.",
    translation: "위대한 일을 하는 유일한 방법은 자신이 하는 일을 사랑하는 것입니다.",
    author: "Steve Jobs"
  },
  {
    text: "In the middle of difficulty lies opportunity.",
    translation: "어려움 한가운데에 기회가 있습니다.",
    author: "Albert Einstein"
  },
  {
    text: "Life is what happens to you while you're busy making other plans.",
    translation: "인생은 다른 계획을 세우느라 바쁜 동안 일어나는 일입니다.",
    author: "John Lennon"
  },
  {
    text: "The future belongs to those who believe in the beauty of their dreams.",
    translation: "미래는 자신의 꿈의 아름다움을 믿는 사람들에게 속합니다.",
    author: "Eleanor Roosevelt"
  },
  {
    text: "It is during our darkest moments that we must focus to see the light.",
    translation: "가장 어두운 순간에 빛을 보기 위해 집중해야 합니다.",
    author: "Aristotle"
  },
  {
    text: "Do not go where the path may lead, go instead where there is no path and leave a trail.",
    translation: "길이 있는 곳으로 가지 말고, 길이 없는 곳으로 가서 흔적을 남기세요.",
    author: "Ralph Waldo Emerson"
  },
  {
    text: "You miss 100% of the shots you don't take.",
    translation: "시도하지 않으면 100% 실패합니다.",
    author: "Wayne Gretzky"
  },
  {
    text: "Whether you think you can or you think you can't, you're right.",
    translation: "할 수 있다고 생각하든 할 수 없다고 생각하든, 당신이 옳습니다.",
    author: "Henry Ford"
  },
  {
    text: "An investment in knowledge pays the best interest.",
    translation: "지식에 대한 투자가 가장 높은 이자를 냅니다.",
    author: "Benjamin Franklin"
  },
  {
    text: "The best time to plant a tree was 20 years ago. The second best time is now.",
    translation: "나무를 심기 가장 좋은 때는 20년 전이었고, 두 번째로 좋은 때는 바로 지금입니다.",
    author: "Chinese Proverb"
  },
  {
    text: "Don't watch the clock; do what it does. Keep going.",
    translation: "시계를 보지 말고, 시계처럼 행동하세요. 계속 나아가세요.",
    author: "Sam Levenson"
  },
  {
    text: "The harder I work, the luckier I get.",
    translation: "더 열심히 일할수록, 더 운이 좋아집니다.",
    author: "Samuel Goldwyn"
  },
  {
    text: "Strive not to be a success, but rather to be of value.",
    translation: "성공하려 하지 말고, 가치 있는 사람이 되려고 노력하세요.",
    author: "Albert Einstein"
  },
  {
    text: "I have not failed. I've just found 10,000 ways that won't work.",
    translation: "저는 실패한 것이 아닙니다. 작동하지 않는 10,000가지 방법을 발견했을 뿐입니다.",
    author: "Thomas Edison"
  },
  {
    text: "The only limit to our realization of tomorrow will be our doubts of today.",
    translation: "내일의 실현에 대한 유일한 한계는 오늘의 의심입니다.",
    author: "Franklin D. Roosevelt"
  }
];


/* ── 2. 랜덤 명언 표시 함수 ────────────────────────────────────
   Math.random()   : 0 이상 1 미만의 무작위 소수를 반환
   Math.floor()    : 소수점 이하를 버려서 정수로 만듦
   → 0 ~ (배열 길이 - 1) 사이의 무작위 정수 = 무작위 인덱스!
   ────────────────────────────────────────────────────────── */
function showRandomQuote() {
  // 무작위 인덱스 생성
  const randomIndex = Math.floor(Math.random() * quotes.length);

  // 해당 인덱스의 명언 객체를 가져옴
  const quote = quotes[randomIndex];

  // HTML 요소를 찾아서 내용을 업데이트
  // document.getElementById('아이디') : HTML에서 해당 id를 가진 요소를 찾음
  document.getElementById('quote-text').textContent = quote.text;
  document.getElementById('quote-translation').textContent = quote.translation;
  document.getElementById('quote-author').textContent = '— ' + quote.author;
}


/* ── 3. JSON 데이터 로드 & 카드 렌더링 ────────────────────────
   fetch() : 외부 파일이나 API에서 데이터를 가져오는 함수
   async/await : 데이터를 가져오는 동안 기다리는 비동기 처리 방식

   [GitHub Actions 자동화 연결 방법]
   - GitHub Actions 스크립트가 data/contents.json 을 생성/업데이트하면
     이 함수가 자동으로 최신 데이터를 읽어서 카드로 표시합니다.
   - .github/workflows/update-data.yml 파일을 만들어 자동화하세요.
   ────────────────────────────────────────────────────────── */
async function loadContents() {
  const container = document.getElementById('sections-container');

  // 로딩 중 메시지 표시
  container.innerHTML = `
    <div class="status-msg">
      <div class="spinner"></div>
      <p>콘텐츠를 불러오는 중...</p>
    </div>
  `;

  try {
    // data/contents.json 파일을 가져옴
    const response = await fetch('data/contents.json');

    // 응답이 실패했을 경우 에러 처리
    if (!response.ok) {
      throw new Error('파일을 불러올 수 없습니다.');
    }

    // JSON 형식으로 파싱 (텍스트 → 자바스크립트 객체)
    const data = await response.json();

    // 마지막 업데이트 날짜 표시
    if (data.last_updated) {
      const dateEl = document.getElementById('last-updated');
      if (dateEl) dateEl.textContent = '업데이트: ' + data.last_updated;
    }

    // 섹션이 없을 경우
    if (!data.sections || data.sections.length === 0) {
      container.innerHTML = '<div class="status-msg"><p>표시할 콘텐츠가 없습니다.</p></div>';
      return;
    }

    // 각 섹션을 HTML로 변환하여 추가
    container.innerHTML = data.sections.map(section => buildSection(section)).join('');

  } catch (error) {
    // 에러 발생 시 메시지 표시
    console.error('데이터 로드 실패:', error);
    container.innerHTML = `
      <div class="status-msg">
        <p>⚠️ 데이터를 불러오지 못했습니다.<br>
        <small>data/contents.json 파일을 확인해 주세요.</small></p>
      </div>
    `;
  }
}


/* ── 4. 섹션 HTML 생성 함수 ────────────────────────────────────
   템플릿 리터럴(Template Literal): 백틱(``)으로 감싼 문자열.
   ${변수} 형태로 변수 값을 문자열 안에 직접 넣을 수 있습니다.
   ────────────────────────────────────────────────────────── */
function buildSection(section) {
  // 섹션 안의 카드들을 HTML로 변환
  const cardsHtml = section.items.map(item => buildCard(item)).join('');

  return `
    <section class="content-section">
      <div class="section-header">
        <h2 class="section-title">${section.title}</h2>
      </div>
      <div class="card-grid">
        ${cardsHtml}
      </div>
    </section>
  `;
}


/* ── 5. 카드 HTML 생성 함수 ──────────────────────────────────── */
function buildCard(item) {
  // 날짜를 보기 좋게 포맷 (예: "2026-06-13" → "2026년 6월 13일")
  const date = formatDate(item.date);

  // url이 없을 경우 버튼 비활성화
  const linkHtml = item.url
    ? `<a href="${item.url}" target="_blank" rel="noopener" class="card-link">
         자세히 보기 →
       </a>`
    : '';

  return `
    <article class="card">
      <div class="card-meta">
        <span class="card-category">${item.category || ''}</span>
        <span class="card-date">${date}</span>
      </div>
      <h3 class="card-title">${item.title}</h3>
      <p class="card-summary">${item.summary}</p>
      ${item.source ? `<p class="card-source">출처: ${item.source}</p>` : ''}
      ${linkHtml}
    </article>
  `;
}


/* ── 6. 날짜 포맷 함수 ──────────────────────────────────────────
   "2026-06-13" 형태의 문자열을 "2026년 6월 13일" 로 변환합니다.
   ────────────────────────────────────────────────────────── */
function formatDate(dateStr) {
  if (!dateStr) return '';
  try {
    // split('-')으로 '-' 기준 분리 → ["2026", "06", "13"]
    const [year, month, day] = dateStr.split('-');
    return `${year}년 ${parseInt(month)}월 ${parseInt(day)}일`;
  } catch (e) {
    return dateStr;  // 변환 실패 시 원본 그대로 반환
  }
}


/* ── 7. 페이지 로드 시 실행 ─────────────────────────────────────
   DOMContentLoaded : HTML 파싱이 완료되면 실행되는 이벤트.
   이 안에 초기화 코드를 넣으면 안전하게 실행됩니다.
   ────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', function () {

  // 랜덤 명언 표시
  showRandomQuote();

  // JSON 데이터 로드 & 카드 렌더링
  loadContents();

  // "다른 명언 보기" 버튼 클릭 이벤트
  const quoteBtn = document.getElementById('quote-btn');
  if (quoteBtn) {
    quoteBtn.addEventListener('click', showRandomQuote);
  }

});
