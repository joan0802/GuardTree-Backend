from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List

from app.services.llm_service import LLMService
from app.models.form import FormItem

router = APIRouter(prefix="/llm", tags=["llm"])

@router.post("/analyze/{case_id}/{year}/{question_field}", response_model=Dict[str, Any])
async def analyze_form_data(
    case_id: int,
    year: int,
    question_field: str,
):
    """
    使用 LLM 對指定表單資料進行分析，回傳分析結果，並將結果寫入資料庫
    """
    try:
        result = await LLMService.analyze_case(case_id, year, question_field)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")
    

@router.get("/analyze/{case_id}/{year}/{question_field}", response_model=Dict[str, Any])
async def get_analyzed_result(
    case_id: int,
    year: int,
    question_field: str,
):
    """
    取得指定表單的分析結果
    """
    try:
        result = await LLMService.get_analysis_result(case_id, year, question_field)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")