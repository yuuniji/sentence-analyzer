# gemini_client.py

import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from typing import AsyncGenerator
import asyncio
import os
from dotenv import load_dotenv

# 加载上级目录的 .env 文件并覆盖系统变量
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path, override=True)


class GeminiClient:
    """
    封装 Gemini API 调用，支持流式和非流式两种模式。
    内置重试机制和错误处理。
    """
    
    MODEL_CONFIGS = {
        "standard": {
            "model": "gemini-2.5-flash",
            "temperature": 0.3,
            "top_p": 0.9,
            "max_output_tokens": 8192,
        },
        "pro": {
            "model": "gemini-2.5-pro",
            "temperature": 0.3,
            "top_p": 0.9,
            "max_output_tokens": 8192,
        },
        "compact": {
            "model": "gemini-2.5-flash",
            "temperature": 0.2,
            "top_p": 0.85,
            "max_output_tokens": 3000,
        }
    }
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
    
    async def stream_analyze(
        self,
        system_prompt: str,
        task_prompt: str,
        mode: str = "standard"
    ) -> AsyncGenerator[str, None]:
        """
        流式生成解析结果，通过 AsyncGenerator 逐块推送文本。
        """
        if mode.startswith("gemini-"):
            # 如果直接传了模型名，就直接使用
            model_name = mode
            gen_config = GenerationConfig(
                temperature=0.3, top_p=0.9, max_output_tokens=8192
            )
        else:
            config = self.MODEL_CONFIGS.get(mode, self.MODEL_CONFIGS["standard"])
            model_name = config["model"]
            gen_config = GenerationConfig(
                temperature=config["temperature"],
                top_p=config["top_p"],
                max_output_tokens=config["max_output_tokens"],
            )
            
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt,
            generation_config=gen_config
        )
        
        # 使用线程池运行同步的流式调用
        loop = asyncio.get_event_loop()
        
        def _sync_stream():
            return model.generate_content(task_prompt, stream=True)
        
        response = await loop.run_in_executor(None, _sync_stream)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
    
    async def analyze(
        self,
        system_prompt: str,
        task_prompt: str,
        mode: str = "standard"
    ) -> str:
        """
        非流式调用，返回完整结果字符串。
        用于格式校验和修复场景。
        """
        full_text = ""
        async for chunk in self.stream_analyze(system_prompt, task_prompt, mode):
            full_text += chunk
        return full_text
