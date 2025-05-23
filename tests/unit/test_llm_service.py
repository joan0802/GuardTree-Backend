import pytest
from unittest.mock import AsyncMock, patch
from app.services.llm_service import LLMService
from app.models.llm_analysis_result import AnalysisResult, Summary, Suggestions

@pytest.mark.asyncio
async def test_analyze_case_with_existing_result():
    existing_result = AnalysisResult(
        summary=Summary(
            summary="已有摘要",
            strengths="優勢",
            concerns="困難",
            priority_item="最急迫"
        ),
        suggestions=Suggestions(strategy="已有策略")
    )

    with patch("app.repositories.llm_repository.LLMRepository.get_question_value", new=AsyncMock(return_value="form_data")), \
         patch("app.repositories.llm_repository.LLMRepository.get_analysis_result", new=AsyncMock(return_value=existing_result)):
        
        result = await LLMService.analyze_case(1, "2025", "questions_A")
        assert result["summary"]["summary"] == "已有摘要"
        assert result["summary"]["strengths"] == "優勢"
        assert result["suggestions"]["strategy"] == "已有策略"


@pytest.mark.asyncio
async def test_analyze_case_without_existing_result():
    new_result = AnalysisResult(
        summary=Summary(
            summary="新摘要",
            strengths="優勢",
            concerns="困難",
            priority_item="最急迫"
        ),
        suggestions=Suggestions(strategy="新策略")
    )

    with patch("app.repositories.llm_repository.LLMRepository.get_question_value", new=AsyncMock(side_effect=["form_data", 99])), \
         patch("app.repositories.llm_repository.LLMRepository.get_analysis_result", new=AsyncMock(return_value=None)), \
         patch("app.models.llm_prompt.LLMPrompt.generate_analysis_prompt", return_value="prompt"), \
         patch("app.services.llm_service.LLMService.run_llm", return_value="json response"), \
         patch("app.services.llm_service.LLMService.parse_response_to_json", return_value=new_result), \
         patch("app.repositories.llm_repository.LLMRepository.save_analysis_result", new=AsyncMock(return_value={"id": 1})):
        
        result = await LLMService.analyze_case(1, "2025", "questions_A")
        assert result["summary"]["summary"] == "新摘要"
        assert result["suggestions"]["strategy"] == "新策略"

@pytest.mark.asyncio
async def test_analyze_case_form_not_found():
    with patch("app.repositories.llm_repository.LLMRepository.get_question_value", new=AsyncMock(return_value=None)):
        with pytest.raises(ValueError, match="Form not found"):
            await LLMService.analyze_case(1, "2025", "questions_A")
