"""
collector.py — 자동 수집 스크립트
==================================================
실행하면 4가지 데이터를 수집해서 data/ 폴더에 JSON으로 저장합니다.

[수집 순서]
  1. 날씨 + 코디  → data/weather.json   (Open-Meteo 공개 API)
  2. 주요 뉴스    → data/news.json      (네이버뉴스 스크래핑)
  3. 시장 지수    → data/finance.json   (yfinance 라이브러리)
  4. 지원사업     → data/bizinfo.json   (기업마당 스크래핑)

[실행 방법]
  python scripts/collector.py

[필요 라이브러리]
  pip install -r requirements.txt
"""

import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ── 공통 설정 ──────────────────────────────────────────────────
# 스크래핑 시 브라우저처럼 보이도록 헤더 설정 (차단 방지)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# ── URL / CSS 선택자 모음 ───────────────────────────────────────
# 사이트 구조가 바뀌면 여기만 수정하면 됩니다
NAVER_NEWS_URL = "https://news.naver.com/section/101"
NAVER_NEWS_SELECTOR = ".sa_text_title"          # 뉴스 제목 선택자

BIZINFO_URL = (
    "https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do"
    "?schAreaDetailCodes=6110000,6410000"
)
BIZINFO_ROW_SELECTOR   = "table tbody tr"       # 테이블 행
BIZINFO_TITLE_SELECTOR = "td:nth-of-type(3) a"  # 제목 링크
BIZINFO_PERIOD_INDEX   = 4                       # 접수기간 열 번호

# 서울 좌표 (Open-Meteo 공개 API, 키 불필요)
SEOUL_LAT = 37.5665
SEOUL_LON = 126.9780
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# ── 날씨 코드 → 설명 매핑 (WMO Weather Interpretation Codes) ──
WEATHER_CODES = {
    0: "맑음",
    1: "대체로 맑음", 2: "부분적으로 흐림", 3: "흐림",
    45: "안개", 48: "결빙 안개",
    51: "가벼운 이슬비", 53: "이슬비", 55: "진한 이슬비",
    61: "약한 비", 63: "비", 65: "강한 비",
    71: "약한 눈", 73: "눈", 75: "강한 눈",
    80: "소나기", 81: "강한 소나기", 82: "폭우",
    95: "뇌우", 99: "뇌우 + 우박",
}


def get_outfit(temp_max, temp_min, rain):
    """날씨 조건에 따라 코디 문장과 참고 이미지 URL을 반환합니다."""
    is_rainy = rain != "없음"
    temp_diff = temp_max - temp_min

    if is_rainy:
        text = (
            "비 오는 날엔 방수 재킷이나 레인코트를 챙기세요. "
            "어두운 색 하의와 방수 신발로 마무리하면 실용적입니다. "
            "접이식 우산도 잊지 마세요."
        )
        img = "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=800&q=60&auto=format"
        query = "레인코트+비+코디"
    elif temp_max >= 27:
        text = (
            f"최고 {temp_max}°C의 더운 날씨입니다. "
            "반팔 티셔츠, 린넨 셔츠, 가벼운 면 팬츠를 추천합니다. "
            "자외선 차단을 위해 선크림과 가벼운 모자를 챙기세요."
        )
        img = "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800&q=60&auto=format"
        query = "여름+반팔+코디"
    elif temp_max >= 18:
        if temp_diff >= 10:
            text = (
                f"일교차가 {temp_diff}°C로 큽니다. "
                "아침저녁엔 얇은 겉옷이나 가디건을 챙기고, "
                "낮에는 가볍게 반팔 또는 얇은 긴팔 티셔츠를 입으세요."
            )
            img = "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&q=60&auto=format"
            query = "봄+가을+가디건+코디"
        else:
            text = (
                "활동하기 좋은 선선한 날씨입니다. "
                "얇은 긴팔 티셔츠나 맨투맨에 청바지 조합이 잘 어울립니다. "
                "얇은 가디건을 하나 챙기면 완벽합니다."
            )
            img = "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=800&q=60&auto=format"
            query = "봄+가을+맨투맨+코디"
    else:
        text = (
            f"최고 기온이 {temp_max}°C의 쌀쌀한 날씨입니다. "
            "니트, 코트, 머플러를 추천합니다. "
            "두꺼운 한 겹보다 얇은 레이어드 스타일이 체온 조절에 효과적입니다."
        )
        img = "https://images.unsplash.com/photo-1511401139252-f158d3209c17?w=800&q=60&auto=format"
        query = "겨울+코트+코디"

    return text, img, query


def fetch_pm10_dust():
    """Open-Meteo Air Quality API로 서울 미세먼지(PM10) 등급을 반환합니다."""
    res = requests.get(
        OPEN_METEO_AIR_QUALITY_URL,
        params={
            "latitude": SEOUL_LAT,
            "longitude": SEOUL_LON,
            "hourly": "pm10",
            "timezone": "Asia/Seoul",
            "forecast_days": 1,
        },
        timeout=10,
    )
    res.raise_for_status()
    pm10 = res.json()["hourly"]["pm10"][12]  # 정오 기준

    if pm10 is None:
        return "데이터 없음"
    if pm10 < 30:
        return f"좋음 ({pm10:.0f}㎍/㎥)"
    if pm10 < 80:
        return f"보통 ({pm10:.0f}㎍/㎥)"
    if pm10 < 150:
        return f"나쁨 ({pm10:.0f}㎍/㎥)"
    return f"매우 나쁨 ({pm10:.0f}㎍/㎥)"


def now_str():
    """현재 시각을 '2026-06-14 06:00:00' 형식 문자열로 반환"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_json(path, data):
    """
    딕셔너리(data)를 JSON 파일로 저장합니다.
    data/ 폴더가 없으면 자동으로 생성합니다.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 저장 완료: {path}")


# ══════════════════════════════════════════════════════════════
# 1. 날씨 + 코디  →  data/weather.json
# ══════════════════════════════════════════════════════════════
def collect_weather():
    """
    Open-Meteo 공개 API로 서울 일별 날씨·공기질을 가져옵니다.
    API 키가 필요 없고 무료입니다.
    최고/최저 기온, 강수, 미세먼지를 반영해 코디를 생성합니다.
    """
    print("\n[1] 날씨 수집 중...")
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        res = requests.get(
            OPEN_METEO_FORECAST_URL,
            params={
                "latitude": SEOUL_LAT,
                "longitude": SEOUL_LON,
                "daily": (
                    "weathercode,temperature_2m_max,"
                    "temperature_2m_min,precipitation_sum"
                ),
                "timezone": "Asia/Seoul",
                "forecast_days": 1,
            },
            timeout=10,
        )
        res.raise_for_status()
        daily = res.json()["daily"]

        code     = daily["weathercode"][0]
        temp_max = round(daily["temperature_2m_max"][0])
        temp_min = round(daily["temperature_2m_min"][0])
        precip   = daily["precipitation_sum"][0]

        desc = WEATHER_CODES.get(code, "날씨 정보 없음")
        rain = f"{precip}mm 예상" if precip and precip > 0 else "없음"

        try:
            dust = fetch_pm10_dust()
        except Exception as e:
            print(f"  [경고] 공기질 수집 실패: {e}")
            dust = "정보 없음"

        outfit_text, outfit_image, outfit_query = get_outfit(temp_max, temp_min, rain)

        data = {
            # 프론트엔드 호환 필드
            "last_updated": now_str(),
            "temp":         temp_max,
            "description":  desc,
            "outfit":       outfit_text,
            "image":        outfit_image,
            "link": (
                "https://www.musinsa.com/search/musinsa/news"
                f"?q={outfit_query}"
            ),
            # 추가 수집 필드 (향후 UI 확장용)
            "date":     today,
            "region":   "서울",
            "temp_min": temp_min,
            "temp_max": temp_max,
            "rain":     rain,
            "dust":     dust,
        }
        save_json("data/weather.json", data)
        print(f"  {desc}, {temp_min}~{temp_max}°C, 미세먼지: {dust}")

    except Exception as e:
        print(f"  ✗ 날씨 수집 실패: {e}")
        save_json("data/weather.json", {
            "last_updated": now_str(),
            "temp": None, "description": "수집 실패",
            "outfit": "", "image": "", "link": "",
            "date": today, "region": "서울",
            "temp_min": None, "temp_max": None,
            "rain": "", "dust": "",
        })


# ══════════════════════════════════════════════════════════════
# 2. 네이버 뉴스  →  data/news.json
# ══════════════════════════════════════════════════════════════
def collect_naver_news():
    """
    네이버 뉴스 경제 섹션을 직접 스크래핑합니다.
    requests로 HTML을 받아 BeautifulSoup으로 파싱합니다.
    """
    print("\n[2] 네이버 뉴스 수집 중...")
    try:
        res = requests.get(NAVER_NEWS_URL, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        items = []
        # CSS 선택자로 뉴스 제목 링크 요소들을 가져옴
        for tag in soup.select(NAVER_NEWS_SELECTOR)[:10]:
            title = tag.get_text(strip=True)        # 태그 안의 텍스트
            link  = tag.get("href", "")             # href 속성값
            if title and link:
                items.append({"title": title, "link": link})

        data = {"last_updated": now_str(), "news": items}
        save_json("data/news.json", data)
        print(f"  수집된 뉴스: {len(items)}건")

    except Exception as e:
        print(f"  ✗ 뉴스 수집 실패: {e}")
        save_json("data/news.json", {"last_updated": now_str(), "news": []})


# ══════════════════════════════════════════════════════════════
# 3. 주요 시장 지수  →  data/finance.json
# ══════════════════════════════════════════════════════════════
def collect_finance():
    """
    yfinance 라이브러리로 주요 지수의 현재가와 등락을 가져옵니다.
    최근 2거래일 데이터로 전일 대비 변동률을 계산합니다.
    """
    print("\n[3] 시장 지수 수집 중...")
    try:
        import yfinance as yf

        # 수집할 지수 목록 (이름: Yahoo Finance 심볼)
        targets = {
            "KOSPI":       "^KS11",
            "S&P 500":     "^GSPC",
            "반도체(SOX)": "^SOX",
            "금(Gold)":    "GC=F",
        }

        items = []
        for name, symbol in targets.items():
            try:
                # 최근 5일치 데이터를 가져와서 마지막 2개 사용
                hist = yf.Ticker(symbol).history(period="5d")
                if len(hist) < 2:
                    continue

                prev_close = float(hist["Close"].iloc[-2])  # 전일 종가
                last_close = float(hist["Close"].iloc[-1])  # 당일 종가
                change     = last_close - prev_close        # 절대 변동
                percent    = (change / prev_close) * 100    # 퍼센트 변동

                items.append({
                    "name":    name,
                    "price":   round(last_close, 2),
                    "change":  round(change, 2),
                    "percent": round(percent, 2),
                })
                print(f"  {name}: {last_close:.2f} ({percent:+.2f}%)")

            except Exception as e:
                print(f"  ✗ {name} 수집 실패: {e}")

        save_json("data/finance.json", {"last_updated": now_str(), "items": items})

    except ImportError:
        print("  ✗ yfinance 미설치. pip install yfinance 실행 후 재시도하세요.")
        save_json("data/finance.json", {"last_updated": now_str(), "items": []})
    except Exception as e:
        print(f"  ✗ 금융 수집 실패: {e}")
        save_json("data/finance.json", {"last_updated": now_str(), "items": []})


# ══════════════════════════════════════════════════════════════
# 4. 기업마당 지원사업  →  data/bizinfo.json
# ══════════════════════════════════════════════════════════════
def collect_bizinfo_news():
    """
    기업마당(bizinfo.go.kr)에서 서울·경기 지원사업을 스크래핑합니다.
    테이블 구조를 파싱해 제목, 링크, 접수기간을 저장합니다.
    """
    print("\n[4] 지원사업 수집 중...")
    try:
        res = requests.get(BIZINFO_URL, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        items = []
        rows = soup.select(BIZINFO_ROW_SELECTOR)

        for row in rows[:10]:
            # 제목 링크 추출
            title_tag = row.select_one(BIZINFO_TITLE_SELECTOR)
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            href  = title_tag.get("href", "")

            # 상대경로 → 절대경로 변환
            if href.startswith("/"):
                href = "https://www.bizinfo.go.kr" + href

            # 접수기간 열 추출 (0번 인덱스부터 시작하므로 -1)
            cells  = row.find_all("td")
            period = ""
            if len(cells) > BIZINFO_PERIOD_INDEX - 1:
                period = cells[BIZINFO_PERIOD_INDEX - 1].get_text(strip=True)

            if title:
                items.append({"title": title, "link": href, "period": period})

        data = {"last_updated": now_str(), "items": items}
        save_json("data/bizinfo.json", data)
        print(f"  수집된 지원사업: {len(items)}건")

    except Exception as e:
        print(f"  ✗ 지원사업 수집 실패: {e}")
        save_json("data/bizinfo.json", {"last_updated": now_str(), "items": []})


# ══════════════════════════════════════════════════════════════
# 실행 진입점
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 50)
    print("  데이터 수집 시작:", now_str())
    print("=" * 50)

    collect_weather()           # 1. 날씨
    collect_naver_news()        # 2. 뉴스
    collect_finance()           # 3. 시장 지수
    collect_bizinfo_news()      # 4. 지원사업

    print("\n" + "=" * 50)
    print("  모든 수집 완료:", now_str())
    print("=" * 50)
