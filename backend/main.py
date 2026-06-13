# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
import asyncio
import json
import os
from dotenv import load_dotenv

from typing import Optional
from prompt_engine import PromptEngine, AnalysisRequest
from gemini_client import GeminiClient
from output_formatter import OutputFormatter
from database import HistoryDB
from utils import extract_trunk, detect_language

# 加载环境变量
load_dotenv(dotenv_path="../.env", override=True)

app = FastAPI(title="英语长难句解析系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖注入
prompt_engine = PromptEngine()
api_key = os.environ.get("GEMINI_API_KEY", "")
gemini_client = GeminiClient(api_key=api_key)
formatter = OutputFormatter()
db = HistoryDB()


class AnalyzeRequest(BaseModel):
    sentence: str
    mode: str = "standard"
    model: str = "standard"
    context: Optional[str] = None


@app.post("/analyze")
async def analyze_sentence(request: AnalyzeRequest):
    """
    主解析接口，返回 SSE 流式响应。
    """
    # 输入验证
    if not request.sentence.strip():
        raise HTTPException(status_code=400, detail="输入句子不能为空")
    
    if detect_language(request.sentence) != "en":
        raise HTTPException(status_code=400, detail="请输入英文句子")
    
    # 提取主干
    trunk = extract_trunk(request.sentence)
    
    # 构造解析请求
    analysis_request = AnalysisRequest(
        sentence=request.sentence,
        trunk_text=trunk,
        mode=request.mode,
        context_sentences=request.context
    )
    
    # 构造提示词
    task_prompt = prompt_engine.build_task_prompt(analysis_request)
    
    async def event_generator():
        full_output = ""
        
        yield {"event": "start", "data": json.dumps({"trunk": trunk})}
        
        try:
            async for chunk in gemini_client.stream_analyze(
                system_prompt=prompt_engine.system_prompt,
                task_prompt=task_prompt,
                mode=request.model
            ):
                full_output += chunk
                yield {"event": "chunk", "data": json.dumps({"text": chunk})}
            
            # 格式验证
            validation = formatter.validate(full_output)
            if not validation.is_valid and validation.fixed_output:
                full_output = validation.fixed_output
                yield {"event": "fixed", "data": json.dumps({
                    "issues": validation.issues
                })}
            
            # 持久化
            record_id = await db.save(
                sentence=request.sentence,
                output=full_output,
                mode=request.mode,
                context=request.context
            )
            
            yield {"event": "done", "data": json.dumps({
                "record_id": record_id,
                "is_valid": validation.is_valid
            })}
            
        except Exception as e:
            yield {"event": "error", "data": json.dumps({"message": str(e)})}
    
    return EventSourceResponse(event_generator())


@app.get("/history")
async def get_history(page: int = 1, page_size: int = 20):
    return await db.list_records(page=page, page_size=page_size)

@app.delete("/history/{record_id}")
async def delete_history(record_id: int):
    await db.delete_record(record_id)
    return {"status": "ok"}

@app.get("/models")
async def get_models():
    import google.generativeai as genai
    models = []
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            # 去除前缀 'models/'
            name = m.name.replace('models/', '')
            models.append({
                "name": name,
                "display_name": getattr(m, 'display_name', name)
            })
    return {"models": models}

@app.get("/health")
async def health():
    return {"status": "ok"}
