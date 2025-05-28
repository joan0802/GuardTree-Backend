from typing import Optional
from datetime import datetime
from app.core.supabase_client import SupabaseService
from app.models.llm_analysis_result import AnalysisResult

class LLMRepository:
    FILLED_TABLE = "forms"
    ANALYSIS_TABLE = "LifeSupportFormAnalysis"

    @staticmethod
    async def get_question_value(case_id: str, year: str, question_field: str):
        filters = {
            "case_id": case_id,
            "year": year
        }
        return await SupabaseService.query_field_by_conditions(
            LLMRepository.FILLED_TABLE,
            filters,
            question_field
        )

    @staticmethod
    async def save_analysis_result(filled_form_id: int, suggestions: dict, summary: dict, question_field: str):
        data = {
            "filled_form_id": filled_form_id,
            "created_at": datetime.now().isoformat(),
            "suggestions": suggestions,
            "summary": summary,
            "question_field": question_field
        }
        return await SupabaseService.create(LLMRepository.ANALYSIS_TABLE, data)

    @staticmethod
    async def get_analysis_result(filled_form_id: int, question_field: str) -> Optional[AnalysisResult]:
        filters = {
            "filled_form_id": filled_form_id,
            "question_field": question_field
        }
        summary_result = await SupabaseService.query_field_by_conditions(
            LLMRepository.ANALYSIS_TABLE,
            filters,
            "summary"
        )
        suggestions_result = await SupabaseService.query_field_by_conditions(
            LLMRepository.ANALYSIS_TABLE,
            filters,
            "suggestions"
        )
        if not summary_result:
            return None

        return AnalysisResult(
            summary=summary_result,
            suggestions=suggestions_result
        )
