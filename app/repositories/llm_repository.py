from typing import Dict, Any, Optional
from datetime import datetime
from app.core.supabase_client import SupabaseService

class LLMRepository:
    FILLED_TABLE = "LifeSupportFormFilled"
    ANALYSIS_TABLE = "LifeSupportFormAnalysis"

    @staticmethod
    async def get_question_value(case_id: str, year: str, question_field: str) -> Optional[Any]:
        """Fetch the value of a specific question field by case_id and year"""
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
    async def save_analysis_result(filled_form_id: int, suggestions: str, summary: str, form_type: str) -> Dict[str, Any]:
        """Insert LLM analysis result into database"""
        data = {
            "filled_form_id": filled_form_id,
            "created_at": datetime.now().isoformat(),
            "suggestions": suggestions,
            "summary": summary,
            "form_type": form_type
        }
        return await SupabaseService.create(LLMRepository.ANALYSIS_TABLE, data)
