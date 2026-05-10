import requests
import xml.etree.ElementTree as ET
from schemas.trend_schema import TrendingTag
from utils.normalizer import normalize_to_tag
from utils.categorizer import categorize_trend

HT_NS = {"ht": "https://trends.google.com/trending/rss"}


def fetch_google_trends():
    url = "https://trends.google.com/trending/rss?geo=IN"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def extract_trend_items(rss_text: str) -> list[dict]:
    root = ET.fromstring(rss_text)
    items = []

    for item in root.findall("./channel/item"):
        title = ""
        approx_traffic = ""
        news_title = ""
        news_source = ""

        title_element = item.find("title")
        if title_element is not None and title_element.text:
            title = title_element.text.strip()

        traffic_element = item.find("ht:approx_traffic", HT_NS)
        if traffic_element is not None and traffic_element.text:
            approx_traffic = traffic_element.text.strip()

        news_item = item.find("ht:news_item", HT_NS)
        if news_item is not None:
            news_title_element = news_item.find("ht:news_item_title", HT_NS)
            if news_title_element is not None and news_title_element.text:
                news_title = news_title_element.text.strip()

            news_source_element = news_item.find("ht:news_item_source", HT_NS)
            if news_source_element is not None and news_source_element.text:
                news_source = news_source_element.text.strip()

        if title:
            items.append(
                {
                    "title": title,
                    "approx_traffic": approx_traffic,
                    "news_title": news_title,
                    "news_source": news_source,
                }
            )

    return items


def generate_description(title: str, category: str, approx_traffic: str, news_title: str, news_source: str) -> str:
    if news_title and news_source:
        return f"{title} is trending with {approx_traffic or 'rising'} searches. Related coverage: {news_title} — {news_source}."

    if news_title:
        return f"{title} is trending with {approx_traffic or 'rising'} searches. Related topic in the news: {news_title}."

    if category == "sports":
        return f"Sports conversation around {title} is gaining traction across India{f' with {approx_traffic} searches' if approx_traffic else ''}."

    if category == "entertainment":
        return f"Entertainment buzz around {title} is rising quickly{f' with {approx_traffic} searches' if approx_traffic else ''}."

    if category == "politics":
        return f"Political discussion related to {title} is picking up{f' with {approx_traffic} searches' if approx_traffic else ''}."

    if category == "astrology":
        return f"Astrology and horoscope interest around {title} is trending{f' with {approx_traffic} searches' if approx_traffic else ''}."

    if category == "weather":
        return f"Weather-related attention around {title} is increasing{f' with {approx_traffic} searches' if approx_traffic else ''}."

    if category == "local":
        return f"Local interest around {title} is rising{f' with {approx_traffic} searches' if approx_traffic else ''}."

    if category == "news":
        return f"News interest around {title} is trending right now{f' with {approx_traffic} searches' if approx_traffic else ''}."

    if category == "people":
        return f"People are actively searching for {title}{f' with {approx_traffic} searches' if approx_traffic else ''}."

    return f"{title} is seeing strong search interest in India right now{f' with {approx_traffic} searches' if approx_traffic else ''}."


def traffic_bucket_bonus(approx_traffic: str) -> int:
    cleaned = approx_traffic.replace("+", "").replace(",", "").strip().upper()

    if not cleaned:
        return 0

    if cleaned.endswith("M"):
        try:
            value = float(cleaned[:-1])
            if value >= 10:
                return 18
            if value >= 5:
                return 16
            if value >= 2:
                return 14
            if value >= 1:
                return 12
            return 10
        except ValueError:
            return 0

    if cleaned.endswith("K"):
        try:
            value = float(cleaned[:-1])
            if value >= 500:
                return 16
            if value >= 200:
                return 14
            if value >= 100:
                return 12
            if value >= 50:
                return 10
            if value >= 20:
                return 8
            if value >= 10:
                return 6
            if value >= 5:
                return 4
            if value >= 2:
                return 2
            return 1
        except ValueError:
            return 0

    try:
        value = int(cleaned)
        if value >= 500000:
            return 16
        if value >= 200000:
            return 14
        if value >= 100000:
            return 12
        if value >= 50000:
            return 10
        if value >= 20000:
            return 8
        if value >= 10000:
            return 6
        if value >= 5000:
            return 4
        if value >= 2000:
            return 2
        return 1
    except ValueError:
        return 0


def compute_heat_score(rank_index: int, approx_traffic: str) -> int:
    rank_score = max(35, 100 - (rank_index * 2))
    bonus = traffic_bucket_bonus(approx_traffic)
    return min(100, rank_score + bonus)


def build_trending_tags(items: list[dict]) -> list[TrendingTag]:
    trending_tags = []

    for index, item in enumerate(items[:10]):
        title = item["title"]
        category = categorize_trend(title)

        trending_tags.append(
            TrendingTag(
                tag=normalize_to_tag(title),
                description=generate_description(
                    title=title,
                    category=category,
                    approx_traffic=item["approx_traffic"],
                    news_title=item["news_title"],
                    news_source=item["news_source"],
                ),
                category=category,
                heat_score=compute_heat_score(index, item["approx_traffic"]),
                source="Google Trends RSS",
                approx_traffic=item["approx_traffic"],
            )
        )

    return trending_tags


def get_trending_tags_service() -> list[TrendingTag]:
    rss_text = fetch_google_trends()
    items = extract_trend_items(rss_text)
    return build_trending_tags(items)
