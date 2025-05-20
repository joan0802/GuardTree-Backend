from app.repositories.llm_repository import LLMRepository
from app.core.llm_pipeline import llm_pipeline

class LLMService:
    @staticmethod
    def build_prompt(case_data, analysis_type):
        """
        根據分析類型與個案資料組 prompt 字串
        """
        base_info = "以下是服務對象的日常生活功能評量資料：\n"
        for key, value in case_data.items():
            base_info += f"{key}：{value}\n"

        instruction = ""
        if analysis_type == "summary":
            instruction = "請針對上述資料進行智能摘要，條列說明服務對象整體日常生活能力狀況。"
        elif analysis_type == "strength":
            instruction = "請找出服務對象在日常生活功能中表現最好的幾項。"
        elif analysis_type == "concern":
            instruction = "請找出服務對象在日常生活功能中表現較差、需要關注的幾項。"
        elif analysis_type == "priority":
            instruction = "請依據資料內容，判斷目前最急迫、最需要改善的活動項目，並說明原因。"
        elif analysis_type == "strategy":
            instruction = "請根據上述資料，提供協助服務對象改善日常生活功能的具體策略建議。"

        return base_info + "\n" + instruction

    @staticmethod
    def run_llm(prompt: str) -> str:
        """
        對 LLM 呼叫並取得回應
        """
        response_iter = llm_pipeline(prompt)
        result = ""
        for response in response_iter:
            result += response['generated_text']
        return result

    @staticmethod
    async def analyze_case(form_id: int) -> dict:
        """
        執行所有分析項目，回傳 dict 結果，並寫回資料庫
        """
        # 撈資料
        form_data = await LLMRepository.get_form_by_id(form_id)
        if not form_data:
            raise ValueError(f"Form with id {form_id} not found")

        results = {}

        # 智能摘要
        summary_prompt = LLMService.build_prompt(form_data, "summary")
        results["summary"] = LLMService.run_llm(summary_prompt)

        # 主要優勢
        strength_prompt = LLMService.build_prompt(form_data, "strength")
        results["strengths"] = LLMService.run_llm(strength_prompt)

        # 需要關注
        concern_prompt = LLMService.build_prompt(form_data, "concern")
        results["concerns"] = LLMService.run_llm(concern_prompt)

        # 優先改善項目
        priority_prompt = LLMService.build_prompt(form_data, "priority")
        results["priority_item"] = LLMService.run_llm(priority_prompt)

        # 策略建議
        strategy_prompt = LLMService.build_prompt(form_data, "strategy")
        results["strategy"] = LLMService.run_llm(strategy_prompt)

        # 最後把分析結果寫回資料庫
        await LLMRepository.update_analysis_result(form_id, str(results))

        return results
