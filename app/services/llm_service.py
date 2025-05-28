import json
from app.repositories.llm_repository import LLMRepository
from app.models.llm_prompt import LLMPrompt
from app.core.llm_pipeline import llm_pipeline
from app.models.llm_analysis_result import AnalysisResult

class LLMService:
    @staticmethod
    def run_llm(prompt: str) -> str:
        response = llm_pipeline(prompt)
        return response

    @staticmethod
    def clean_json_text(response_text: str) -> str:
        if response_text.startswith("```json"):
            response_text = response_text[len("```json"):].strip()
        if response_text.endswith("```"):
            response_text = response_text[:-3].strip()
        return response_text

    @staticmethod
    def parse_response_to_json(response_text: str) -> AnalysisResult:
        cleaned_text = LLMService.clean_json_text(response_text)
        try:
            result_dict = json.loads(cleaned_text)
        except json.JSONDecodeError:
            raise ValueError("LLM 回傳的格式無法解析成 JSON")
        return AnalysisResult(**result_dict)
    
    @staticmethod
    async def analyze_case(case_id: int, year: str, question_field: str):
        form_data = await LLMRepository.get_question_value(case_id, year, question_field)
        if not form_data:
            raise ValueError("Form not found")

        form_id = await LLMRepository.get_question_value(case_id, year, "id")
        existing_result = await LLMService.get_analysis_result(case_id, year, question_field)
        if existing_result:
            return existing_result

        prompt = LLMPrompt.generate_analysis_prompt(form_data)
        response_text = LLMService.run_llm(prompt)
        analysis_result = LLMService.parse_response_to_json(response_text)

        await LLMRepository.save_analysis_result(
            filled_form_id=form_id,
            suggestions=analysis_result.suggestions.dict(),
            summary=analysis_result.summary.dict(),
            question_field=question_field
        )

        return analysis_result.dict()
    
    @staticmethod
    async def get_analysis_result(case_id: int, year: str, question_field: str):
        form_data = await LLMRepository.get_question_value(case_id, year, question_field)
        if not form_data:
            raise ValueError("Form not found")

        form_id = await LLMRepository.get_question_value(case_id, year, "id")

        existing_result = await LLMRepository.get_analysis_result(
            filled_form_id=form_id,
            question_field=question_field
        )
        if existing_result:
            return existing_result.dict()

        return None
