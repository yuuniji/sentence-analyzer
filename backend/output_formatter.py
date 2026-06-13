# output_formatter.py

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    is_valid: bool
    issues: list[str]
    fixed_output: Optional[str] = None


class OutputFormatter:
    """
    验证 Gemini 输出是否符合 VitePress Tabs 格式规范，
    并尝试自动修复常见格式问题。
    """
    
    REQUIRED_TABS = [
        "== 完整翻译",
        "== 语义/意群拆分",
        "== 关键词汇与短语",
        "== 重难点与语法分析",
        "== 导师小结"
    ]
    
    def validate(self, output: str, mode: str = "standard") -> ValidationResult:
        issues = []
        
        required_tabs = self.REQUIRED_TABS
        if mode == "article":
            required_tabs = [
                "== 核心主旨",
                "== 情绪与文风",
                "== 高频生词本",
                "== 长难句雷达"
            ]
        
        # 检查 <details> 包裹
        if not output.strip().startswith("<details>"):
            issues.append("缺少 <details> 开始标签")
        if not output.strip().endswith("</details>"):
            issues.append("缺少 </details> 结束标签")
        
        # 检查 <summary> 标签
        if "<summary>" not in output or "</summary>" not in output:
            issues.append("缺少 <summary> 标签")
        
        # 检查 ::: tabs 语法
        if "::: tabs" not in output:
            issues.append("缺少 ::: tabs 声明")
        if ":::" not in output[output.rfind("::: tabs"):]:
            issues.append("缺少 ::: 结束标记")
        
        # 检查大标签页
        for tab in required_tabs:
            if tab not in output:
                issues.append(f"缺少标签页：{tab}")
        
        # 检查 Emoji（Unicode 范围检测）
        emoji_pattern = re.compile(
            "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+"
        )
        if emoji_pattern.search(output):
            issues.append("输出中包含 Emoji 字符")
        
        if not issues:
            return ValidationResult(is_valid=True, issues=[])
        
        # 尝试自动修复
        fixed = self._attempt_fix(output, issues)
        return ValidationResult(is_valid=False, issues=issues, fixed_output=fixed)
    
    def _attempt_fix(self, output: str, issues: list[str]) -> Optional[str]:
        fixed = output.strip()
        
        # 修复首尾标签
        if not fixed.startswith("<details>"):
            fixed = "<details>\n<summary>句子解析</summary>\n" + fixed
        if not fixed.endswith("</details>"):
            fixed = fixed + "\n</details>"
        
        # 移除 Emoji
        emoji_pattern = re.compile(
            "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+"
        )
        fixed = emoji_pattern.sub("", fixed)
        
        return fixed
