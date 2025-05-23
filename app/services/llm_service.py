from app.repositories.llm_repository import LLMRepository
from app.core.llm_pipeline import llm_pipeline
import json

class LLMService:

    @staticmethod
    def run_llm(prompt: str) -> str:
        """
        對 LLM 呼叫並取得回應
        """
        # response_iter = llm_pipeline(prompt)
        # result = ""
        # for response in response_iter:
        #     result += response['generated_text']
        # return result
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
    async def analyze_case(case_id: int, year: str, question_field: str) -> dict:
        """
        執行所有分析項目，回傳 dict 結果，並寫回資料庫
        """
        # 撈資料
        form_data = await LLMRepository.get_question_value(case_id=case_id, year=year, question_field=question_field)
        if not form_data:
            raise ValueError(f"Form not found")
        print(f"form_data: {form_data}")
        form_id = await LLMRepository.get_question_value(case_id=case_id, year=year, question_field="id")
        print(f"form_id: {form_id}")

        # 檢查是否已經分析過
        existing_result = await LLMRepository.get_analysis_result(
            filled_form_id=form_id,
            question_field=question_field
        )
        if existing_result:
            return existing_result

        # 建立一個總 prompt，請 LLM 直接回傳符合 JSON 格式的結果
        prompt = f"""
            你是一個繁體中文專家系統，請根據以下個案表單資料，分析並產出以下格式的 JSON 結果：

            表單資料：
            {form_data}

            其中，activity 代表活動內容，item 代表項目，subitem 代表細項（若為null 可忽略），core_area 代表這份表單所對應代的核心能力領域，
            support type 為教保員評估服務對象在這個項目的分數：4 代表需完全肢體協助；3 代表需部份身體協助； 2 代表需示範/口頭/手勢提示；1 代表須監督陪同；0 代表不須協助；null或None 代表不適用（可忽略此項評分）。

            請輸出以下 JSON 格式：
            {{
            "summary": {{
                "summary": "請針對上述資料進行智能摘要，條列說明服務對象整體日常生活能力狀況。",
                "strengths": "請找出服務對象在日常生活功能中表現最好的幾項。",
                "concerns": "請找出服務對象在日常生活功能中表現較差、需要關注的幾項。",
                "priority_item": "請依據資料內容，判斷目前最急迫、最需要改善的活動項目，並說明原因。"
            }},
            "suggestions": {{
                "strategy": "請根據上述資料，提供協助服務對象改善日常生活功能的具體策略建議。"
            }}
            }}

            注意：
            - 請完整回傳 JSON 格式
            - 不要遺漏任何欄位
            - 字串內禁止換行
            """

        response_text = LLMService.run_llm(prompt)
        print(f"response_text: {response_text}")
        # 嘗試解析成 JSON
        response_text = LLMService.clean_json_text(response_text)
        try:
            results = json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError("LLM 回傳的格式無法解析成 JSON")

        # 寫回資料庫
        await LLMRepository.save_analysis_result(
            filled_form_id=form_id,
            suggestions=results["suggestions"],
            summary=results["summary"],
            question_field=question_field
        )

        return results

