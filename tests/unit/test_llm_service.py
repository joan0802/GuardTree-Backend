import pytest
from unittest.mock import patch, AsyncMock

from app.services.llm_service import LLMService


@pytest.mark.asyncio
@patch('app.repositories.llm_repository.LLMRepository.get_question_value')
async def test_analyze_case_form_not_found(mock_get_question_value):
    """Test analyze_case when form data not found"""
    mock_get_question_value.return_value = None

    with pytest.raises(ValueError) as excinfo:
        await LLMService.analyze_case(case_id=1, year="2024", question_field="A")

    assert "Form not found" in str(excinfo.value)
    mock_get_question_value.assert_called_once_with(case_id=1, year="2024", question_field="A")


@pytest.mark.asyncio
@patch('app.repositories.llm_repository.LLMRepository.get_analysis_result')
@patch('app.repositories.llm_repository.LLMRepository.get_question_value')
async def test_analyze_case_existing_result(mock_get_question_value, mock_get_analysis_result):
    """Test analyze_case when analysis result already exists"""
    mock_get_question_value.return_value = {"id": 1, "case_name": "Alice", "A": "測試資料"}
    mock_get_analysis_result.return_value = {"summary": "已存在分析結果"}

    result = await LLMService.analyze_case(case_id=1, year="2024", question_field="A")

    assert result == {"summary": "已存在分析結果"}
    mock_get_question_value.assert_called_once_with(case_id=1, year="2024", question_field="A")
    mock_get_analysis_result.assert_called_once_with(filled_form_id=1, question_field="A")


@pytest.mark.asyncio
@patch('app.repositories.llm_repository.LLMRepository.save_analysis_result')
@patch('app.services.llm_service.LLMService.run_llm')
@patch('app.repositories.llm_repository.LLMRepository.get_analysis_result')
@patch('app.repositories.llm_repository.LLMRepository.get_question_value')
async def test_analyze_case_success(
    mock_get_question_value,
    mock_get_analysis_result,
    mock_run_llm,
    mock_save_analysis_result
):
    """Test analyze_case normal successful case"""

    # Mock資料
    mock_get_question_value.return_value = {
        "id": 1, "case_name": "Alice", "A": "測試資料"
    }
    mock_get_analysis_result.return_value = None

    # run_llm 模擬回傳
    mock_run_llm.return_value = "LLM回應"

    # 呼叫 function
    result = await LLMService.analyze_case(case_id=1, year="2024", question_field="A")

    # 驗證結果
    expected_result = {
        "summary": {
            "summary": "LLM回應",
            "strengths": "LLM回應",
            "concerns": "LLM回應",
            "priority_item": "LLM回應"
        },
        "suggestions": {
            "strategy": "LLM回應"
        }
    }

    assert result == expected_result

    # 驗證 mock 呼叫次數與參數
    assert mock_run_llm.call_count == 5
    mock_get_question_value.assert_called_once_with(case_id=1, year="2024", question_field="A")
    mock_get_analysis_result.assert_called_once_with(filled_form_id=1, question_field="A")
    mock_save_analysis_result.assert_called_once_with(
        filled_form_id=1,
        suggestions=expected_result["suggestions"],
        summary=expected_result["summary"],
        question_field="A"
    )


def test_build_prompt_summary():
    """Test build_prompt for summary"""
    case_data = {"case_name": "Alice", "A": "資料A", "B": "資料B"}
    prompt = LLMService.build_prompt(case_data, "summary")
    assert "以下是服務對象的日常生活功能評量資料：" in prompt
    assert "請針對上述資料進行智能摘要" in prompt


@patch('app.services.llm_service.LLMService.run_llm')
def test_run_llm(mock_pipeline):
    """Test run_llm"""
    mock_pipeline.return_value = "LLM回應"

    prompt = "請做什麼事"
    result = LLMService.run_llm(prompt)

    mock_pipeline.assert_called_once_with(prompt)
    assert result == "LLM回應"
