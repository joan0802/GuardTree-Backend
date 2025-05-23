from pydantic import BaseModel

class Summary(BaseModel):
    summary: str
    strengths: str
    concerns: str
    priority_item: str

class Suggestions(BaseModel):
    strategy: str

class AnalysisResult(BaseModel):
    summary: Summary
    suggestions: Suggestions
