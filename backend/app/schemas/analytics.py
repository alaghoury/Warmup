from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    total_users: int
    total_api_calls: int
