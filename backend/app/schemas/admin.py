from pydantic import BaseModel


class AdminStats(BaseModel):
    total_users: int
    active_users: int
    recent_signups: int
