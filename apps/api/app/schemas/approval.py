from pydantic import BaseModel, Field


class ApprovalDecisionCreate(BaseModel):
    decision: str = Field(pattern="^(approve|reject)$")
