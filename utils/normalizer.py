import re


def normalize_to_tag(title: str) -> str:
    cleaned = title.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)

    words = cleaned.split(" ")
    capitalized_words = [word.capitalize() for word in words if word]

    return "#" + "".join(capitalized_words)
