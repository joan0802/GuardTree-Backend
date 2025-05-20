from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from app.services.llm_service import LLMService
from app.core.auth import get_current_user

router = APIRouter(prefix="/llm", tags=["llm"])

@router.post("/analyze/{form_id}", response_model=Dict[str, Any])
async def analyze_form_data(
    form_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    使用 LLM 對指定表單資料進行分析，回傳分析結果，並將結果寫入資料庫
    """
    try:
        result = await LLMService.analyze_case(form_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")
