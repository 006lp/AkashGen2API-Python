from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse, Response, StreamingResponse
import base64
import io
from typing import Dict, Any, List
import json

from app.api.auth import authenticate
from app.services.akash_service import AkashService
from app.utils.config import Config

router = APIRouter(prefix=Config.API_PREFIX)

@router.get("/")
async def root():
    return {"message": "API service is running"}

@router.get("/ping")
async def ping():
    return "pong"

@router.post("/v1/chat/completions")
async def chat_completions(request: Request, _: str = Depends(authenticate)):
    """处理聊天完成请求"""
    try:
        data = await request.json()
        messages = data.get("messages", [])
        
        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        # 获取用户消息
        user_messages = [msg for msg in messages if msg.get("role") == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message found")
        
        # 使用最后一条用户消息
        last_user_message = user_messages[-1]
        prompt = last_user_message.get("content", "")
        
        # 调用Akash服务生成图像
        result = await AkashService.generate_image(prompt)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # 构建图像URL
        image_url = f"{Config.BASE_URL}/images?id={result['job_id']}"
        
        # 构建Markdown响应
        response_text = f"<image_generation> jobId='{result['job_id']}' prompt='{result['prompt']}' negative='{result['negative']}'</image_generation>\n\n[{result['job_id']}]({image_url})"
        
        # 如果请求流式响应
        if data.get("stream", False):
            async def stream_response():
                yield f"data: {json.dumps({'content': response_text})}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(stream_response(), media_type="text/event-stream")
        
        # 非流式响应
        return {
            "id": result["job_id"],
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    }
                }
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images")
async def get_image(id: str):
    """获取生成的图像"""
    try:
        # 获取图像状态
        status_data = await AkashService.wait_for_image(id)
        
        if status_data.get("status") != "completed":
            raise HTTPException(status_code=404, detail="Image not found or not ready")
        
        # 从Base64数据中提取图像
        image_data = status_data.get("result", "")
        if not image_data or not image_data.startswith("data:image/"):
            raise HTTPException(status_code=404, detail="Image data not available")
        
        # 提取Base64部分
        _, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        
        # 返回图像
        return Response(content=image_bytes, media_type="image/webp")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
