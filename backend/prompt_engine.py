# prompt_engine.py

from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class AnalysisRequest:
    sentence: str
    trunk_text: str
    mode: str = "standard"          # standard | compact | paragraph
    context_sentences: Optional[str] = None
    custom_terms: Optional[dict] = None


class PromptEngine:
    """
    负责动态构造发送给 Gemini API 的提示词。
    系统提示词（System Prompt）固定加载，
    任务提示词（Task Prompt）根据请求参数动态渲染。
    """
    
    def __init__(self, templates_dir: str = "prompts/"):
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        # 不再在此处固定加载系统提示词，而是在请求时加载
        pass
    
    def get_system_prompt(self, mode: str = "standard") -> str:
        template_name = "system_prompt_article.j2" if mode == "article" else "system_prompt.j2"
        template = self.env.get_template(template_name)
        return template.render()
    
    def build_task_prompt(self, request: AnalysisRequest) -> str:
        # Fallback to standard if template missing
        template_name = f"task_{request.mode}.j2"
        try:
            template = self.env.get_template(template_name)
        except Exception:
            template = self.env.get_template("task_standard.j2")
            
        return template.render(
            sentence=request.sentence,
            trunk_text=request.trunk_text,
            context_sentences=request.context_sentences,
            custom_terms=request.custom_terms
        )
    
