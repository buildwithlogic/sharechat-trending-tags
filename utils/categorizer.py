def categorize_trend(title: str) -> str:
    lowered = title.lower().strip()

    sports_keywords = [
        "vs", "ipl", "cricket", "match", "football", "csk", "rcb", "mi",
        "ipl final", "bcci", "icc", "t20", "odi", "test match", "kabaddi"
    ]

    entertainment_keywords = [
        "bollywood", "movie", "film", "actor", "actress", "song", "trailer",
        "celebrity", "ott", "web series", "cinema", "release",
        "sai pallavi", "celina jaitly", "salman", "shah rukh", "srk",
        "deepika", "ranbir", "allu arjun", "prabhas", "ntr", "rajinikanth",
        "पल्लवी", "சினிமா", "திரைப்படம்"
    ]

    politics_keywords = [
        "election", "minister", "government", "politics", "parliament",
        "bjp", "congress", "cm", "pm", "modi", "rahul gandhi",
        "राजनीति", "सरकार", "चुनाव", "মন্ত্রী", "সরকার", "রাজনীতি",
        "రాజకీయాలు", "அரசியல்", "રાજકારણ"
    ]

    astrology_keywords = [
        "rashifal", "rashi", "horoscope", "zodiac",
        "राशि", "राशिफल", "ஜாதகம்", "రాశి", "રાશિ", "রাশিফল"
    ]

    weather_keywords = [
        "rain", "rains", "storm", "cyclone", "weather", "heatwave",
        "monsoon", "flood", "temperature",
        "बारिश", "मौसम", "বর্ষা", "বৃষ্টি", "কালবৈশাখী",
        "వర్షం", "மழை", "હવામાન"
    ]

    city_keywords = [
        "delhi", "mumbai", "bengaluru", "bangalore", "kolkata", "chennai",
        "hyderabad", "pune", "lucknow", "patna", "jaipur", "surat",
        "ahmedabad", "bhopal"
    ]

    news_keywords = [
        "news", "breaking", "update", "live", "today"
    ]

    if any(keyword in lowered for keyword in sports_keywords):
        return "sports"

    if any(keyword in lowered for keyword in entertainment_keywords):
        return "entertainment"

    if any(keyword in lowered for keyword in politics_keywords):
        return "politics"

    if any(keyword in lowered for keyword in astrology_keywords):
        return "astrology"

    if any(keyword in lowered for keyword in weather_keywords):
        return "weather"

    if any(keyword in lowered for keyword in city_keywords):
        return "local"

    if any(keyword in lowered for keyword in news_keywords):
        return "news"

    words = lowered.split()

    if len(words) == 2 and all(word.isalpha() for word in words):
        return "people"

    if len(words) == 1 and lowered[0:1].isalpha() and len(lowered) > 3:
        return "general"

    return "general"
