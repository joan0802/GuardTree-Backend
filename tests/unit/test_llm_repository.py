import pytest
from unittest.mock import AsyncMock, patch
from app.repositories.llm_repository import LLMRepository

@pytest.mark.asyncio
async def test_get_question_value():
    with patch("app.core.supabase_client.SupabaseService.query_field_by_conditions", new=AsyncMock(return_value="test_value")):
        result = await LLMRepository.get_question_value("123", "2025", "questions_A")
        assert result == "test_value"

@pytest.mark.asyncio
async def test_save_analysis_result():
    with patch("app.core.supabase_client.SupabaseService.create", new=AsyncMock(return_value={"id": 1})) as mock_create:
        result = await LLMRepository.save_analysis_result(
            filled_form_id=1,
            suggestions={"strategy": "建議"},
            summary={"summary": "摘要"},
            question_field="questions_A"
        )
        assert result == {"id": 1}
        mock_create.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_analysis_result_found():
    with patch("app.core.supabase_client.SupabaseService.query_field_by_conditions", new=AsyncMock(side_effect=[
        {
            "summary": "test summary",
            "strengths": "test strengths",
            "concerns": "test concerns",
            "priority_item": "test priority"
        },  # summary_result
        {
            "strategy": "test strategy"
        }  # suggestions_result
    ])):
        result = await LLMRepository.get_analysis_result(1, "questions_A")
        assert result is not None
        assert result.summary.summary == "test summary"
        assert result.summary.strengths == "test strengths"
        assert result.suggestions.strategy == "test strategy"


@pytest.mark.asyncio
async def test_get_analysis_result_not_found():
    with patch("app.core.supabase_client.SupabaseService.query_field_by_conditions", new=AsyncMock(return_value=None)):
        result = await LLMRepository.get_analysis_result(1, "questions_A")
        assert result is None
