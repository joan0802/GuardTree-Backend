import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.llm_service import LLMService
from app.models.llm_analysis_result import AnalysisResult


@pytest.mark.asyncio
async def test_analyze_case_with_existing_result():
    # 模擬資料
    fake_form_data = {"some": "data"}
    fake_form_id = 123
    fake_existing_result = AnalysisResult(
        summary={
            "summary": "已有摘要",
            "strengths": "已有優勢",
            "concerns": "已有困難",
            "priority_item": "已有優先項目"
        },
        suggestions={"strategy": "已有策略"}
    )

    with patch("app.repositories.llm_repository.LLMRepository.get_question_value", new=AsyncMock(side_effect=[fake_form_data, fake_form_id])):
        with patch("app.services.llm_service.LLMService.get_analysis_result", new=AsyncMock(return_value=fake_existing_result)):
            result = await LLMService.analyze_case(1, "2025", "questions_A")

            assert result.summary.strengths == "已有優勢"
            assert result.suggestions.strategy == "已有策略"


@pytest.mark.asyncio
async def test_analyze_case_without_existing_result():
    fake_form_data = {"some": "data"}
    fake_form_id = 123
    fake_prompt = "這是 prompt"
    fake_llm_response = """```json
    {
        "summary": {
            "summary": "測試摘要",
            "strengths": "測試優勢",
            "concerns": "測試困難",
            "priority_item": "測試優先項目"
        },
        "suggestions": {
            "strategy": "測試策略"
        }
    }
    ```"""

    with patch("app.repositories.llm_repository.LLMRepository.get_question_value", new=AsyncMock(side_effect=[fake_form_data, fake_form_id])):
        with patch("app.services.llm_service.LLMService.get_analysis_result", new=AsyncMock(return_value=None)):
            with patch("app.models.llm_prompt.LLMPrompt.generate_analysis_prompt", return_value=fake_prompt):
                with patch("app.services.llm_service.LLMService.run_llm", return_value=fake_llm_response):
                    with patch("app.repositories.llm_repository.LLMRepository.save_analysis_result", new=AsyncMock()) as mock_save:
                        result = await LLMService.analyze_case(1, "2025", "questions_A")

                        assert result.summary.strengths == "測試優勢"
                        assert result.suggestions.strategy == "測試策略"
                        mock_save.assert_awaited_once()


@pytest.mark.asyncio
async def test_analyze_case_form_not_found():
    with patch("app.repositories.llm_repository.LLMRepository.get_question_value", new=AsyncMock(return_value=None)):
        with pytest.raises(ValueError, match="Form not found"):
            await LLMService.analyze_case(1, "2025", "questions_A")


@pytest.mark.asyncio
async def test_parse_response_to_json_success():
    response_text = """```json
    {
        "summary": {
            "summary": "摘要",
            "strengths": "優勢",
            "concerns": "困難",
            "priority_item": "優先項目"
        },
        "suggestions": {
            "strategy": "策略"
        }
    }
    ```"""
    result = LLMService.parse_response_to_json(response_text)
    assert result.summary.strengths == "優勢"
    assert result.suggestions.strategy == "策略"


def test_clean_json_text():
    raw_text = """```json
    {"a": 1}
    ```"""
    cleaned = LLMService.clean_json_text(raw_text)
    assert cleaned == '{"a": 1}'
