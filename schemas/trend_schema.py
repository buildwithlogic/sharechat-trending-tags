from pydantic import BaseModel


class TrendingTag(BaseModel):
    tag: str
    description: str
    category: str
    heat_score: int
    source: str
    approx_traffic: str
