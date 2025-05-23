import pytest
from unittest.mock import patch, AsyncMock, call
from datetime import datetime
from app.repositories.llm_repository import LLMRepository


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.query_field_by_conditions', new_callable=AsyncMock)
async def test_get_question_value(mock_query_field_by_conditions):
    """Test getting a question value"""
    mock_result = {"id": 1, "questions_A": "test answer"}
    mock_query_field_by_conditions.return_value = mock_result

    result = await LLMRepository.get_question_value("case123", "2025", "questions_A")

    mock_query_field_by_conditions.assert_awaited_once_with(
        "forms",
        {"case_id": "case123", "year": "2025"},
        "questions_A"
    )
    assert result == mock_result

@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.create', new_callable=AsyncMock)
async def test_save_analysis_result(mock_create):
    """Test saving analysis result"""
    mock_result = {"id": 1}
    mock_create.return_value = mock_result

    suggestions = {"strategy": "do something"}
    summary = {
        "summary": "summary content",
        "strengths": "some strengths",
        "concerns": "concerns here",
        "priority_item": "priority item"
    }

    result = await LLMRepository.save_analysis_result(
        filled_form_id=1,
        suggestions=suggestions,
        summary=summary,
        question_field="questions_A"
    )

    mock_create.assert_awaited_once()
    args, kwargs = mock_create.call_args
    assert args[0] == "LifeSupportFormAnalysis"
    data = args[1]

    # 檢查資料內容
    assert data["filled_form_id"] == 1
    assert data["suggestions"] == suggestions
    assert data["summary"] == summary
    assert data["question_field"] == "questions_A"
    # created_at 應該是一個 ISO 格式字串
    datetime.fromisoformat(data["created_at"])

    assert result == mock_result

@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.query_field_by_conditions', new_callable=AsyncMock)
async def test_get_analysis_result(mock_query_field_by_conditions):
    """Test getting an analysis result"""
    # Simulate different results for summary and suggestions
    mock_query_field_by_conditions.side_effect = [
        {"id": 1, "summary": "some summary"},      # for summary
        {"id": 1, "suggestions": "some suggestion"}  # for suggestions
    ]

    result = await LLMRepository.get_analysis_result(1, "question_A")

    expected_summary_call = call(
        "LifeSupportFormAnalysis",
        {"filled_form_id": 1, "question_field": "question_A"},
        "summary"
    )
    expected_suggestions_call = call(
        "LifeSupportFormAnalysis",
        {"filled_form_id": 1, "question_field": "question_A"},
        "suggestions"
    )
    assert expected_summary_call in mock_query_field_by_conditions.await_args_list
    assert expected_suggestions_call in mock_query_field_by_conditions.await_args_list

    expected_result = {
        "summary": {"id": 1, "summary": "some summary"},
        "suggestions": {"id": 1, "suggestions": "some suggestion"}
    }
    assert result == expected_result