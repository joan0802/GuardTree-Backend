class LLMPrompt:
    @staticmethod
    def generate_analysis_prompt(form_data: str) -> str:
        return f"""
你是一個繁體中文專家系統，請根據以下個案表單資料，分析並產出以下格式的 JSON 結果：

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

表單資料：
{form_data}
"""
