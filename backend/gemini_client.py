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
            "model": "gemini-3.1-pro-preview",
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

    async def analyze_audio(self, audio_bytes: bytes, mime_type: str) -> dict:
        """
        输入音频字节和 MIME 类型，执行 STT 转写、单词细粒度纠错、以及整句深度语法剖析。
        返回符合 AnalysisResult 结构的 dict。
        """
        import google.generativeai as genai
        from pydantic import BaseModel, Field
        from typing import List, Optional
        import json

        # 使用 gemini-3.1-pro-preview 保证高水准口语分析与纠正能力
        model_name = "gemini-3.1-pro-preview"
        
        # 1. 语音转文字 (STT)
        stt_prompt = """
        Transcribe this audio exactly as spoken. Focus on capturing every single word, 
        including all hesitation fillers (um, ah, uh, er, like, you know) and stutters. 
        Do not normalize the speech or fix any grammar during transcription. 
        The goal is 100% phonetic and lexical fidelity to the source audio.
        """
        
        model = genai.GenerativeModel(model_name=model_name)
        loop = asyncio.get_event_loop()
        
        def _sync_generate_stt():
            return model.generate_content([
                {"mime_type": mime_type, "data": audio_bytes},
                stt_prompt
            ])
            
        stt_response = await loop.run_in_executor(None, _sync_generate_stt)
        original_text = stt_response.text.strip()
        
        if not original_text:
            raise ValueError("语音转写结果为空，请确认音频录制或输入是否正常。")
            
        # 2. 单词细粒度纠正与标注
        correction_prompt = f"""
        You are a master linguistic analyst and a senior IELTS/TOEFL examiner. 
        Your task is to perform word-by-word segmentation and analysis of the provided transcript from a Chinese English learner.
        
        SEGMENTATION RULES:
        1. Break the text into INDIVIDUAL WORD segments. Each word (including punctuation attached to it) should be its own segment.
        2. Spaces between words should NOT be included in any segment's "text" field - they will be added automatically.
        3. EXACT RECONSTRUCTION: When you join all "text" fields with spaces, the result must match the original transcript.
        
        STATUS VALUES - You MUST use exactly one of these for each segment:
        - "correct": The word is spoken correctly with no issues.
        - "pronunciation": The word sounds like the speaker meant a different word (e.g., said "the" but meant "this", or "tree" but meant "three"). Provide the intended word in "correction".
        - "grammar": A grammatical error (wrong tense, wrong article, subject-verb disagreement, wrong preposition, etc.). Provide the correct form in "correction".
        - "vocabulary": Poor word choice, Chinglish, or unidiomatic expression. Provide a better alternative in "correction".
        - "deleted": A redundant or repeated word that should be removed (e.g., stuttered repetitions like "good, good" → mark the first "good," as "deleted").
        - "insertion": A word that is MISSING and should be inserted. Set "text" to the missing word and status to "insertion".
        - "filler": Hesitation sounds like "um", "uh", "ah", "er", "like", "you know".
        - "pause": An unusually long pause in speech. Set "text" to "[...]".
        - "indistinct": A word that is unclear or incomprehensible in the audio. Set "text" to the best guess or "[Indistinct]".
        
        CRITICAL ANALYSIS GUIDELINES:
        - Be STRICT and thorough. Identify every error, no matter how small.
        - For pronunciation errors: if the transcribed word doesn't match what the speaker likely intended, mark it as "pronunciation".
        - For repeated words or stutters: mark redundant instances as "deleted".
        - For missing articles, prepositions, or words: add "insertion" segments where words should be.
        - Always provide the "correction" field for pronunciation, grammar, and vocabulary errors.
        
        Transcript: {original_text}
        """

        class SegmentModel(BaseModel):
            text: str = Field(description="The exact original word or token")
            status: str = Field(description="One of: 'correct', 'pronunciation', 'grammar', 'vocabulary', 'deleted', 'insertion', 'filler', 'pause', 'indistinct'")
            correction: Optional[str] = Field(description="The corrected/improved text (required for pronunciation, grammar, vocabulary)")

        class CorrectionResponseModel(BaseModel):
            segments: List[SegmentModel]

        def _sync_generate_correction():
            return model.generate_content(
                correction_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_schema=CorrectionResponseModel
                )
            )
            
        correction_response = await loop.run_in_executor(None, _sync_generate_correction)
        correction_data = json.loads(correction_response.text)
        
        # 3. 提取纠正后的拼接文本以进行深层剖析
        corrected_words = []
        for seg in correction_data.get("segments", []):
            status = seg.get("status", "correct")
            if status == "deleted":
                continue
            elif status in ("pronunciation", "grammar", "vocabulary") and seg.get("correction"):
                corrected_words.append(seg["correction"])
            else:
                corrected_words.append(seg["text"])
        corrected_text = " ".join(corrected_words)
        
        # 4. 深度句法及英语剖析
        deep_analysis_prompt = f"""
        You are an expert English-Chinese bilingual language tutor. 
        Perform a comprehensive deep analysis of the following CORRECTED English text for a Chinese learner.
        This is the corrected version of what the speaker intended to say.
        
        Provide:
        1. **translation**: A natural, fluent Chinese translation (信达雅) of what the speaker meant.
        2. **literal_translation**: A more literal, word-by-word Chinese translation for comparison.
        3. **chunking**: Break the sentence into meaningful semantic chunks (意群). Each chunk should have the English phrase and its Chinese equivalent.
        4. **vocabulary**: Pick 1-3 key or noteworthy vocabulary words. For each, provide:
           - word: the English word
           - pos: part of speech (e.g., "n.", "v.", "adj.")
           - meaning: Chinese meaning
           - extra: synonyms, collocations, or usage notes in Chinese
        5. **syntax**: Analyze the sentence structure:
           - skeleton: The grammatical skeleton (主谓宾等) using Chinese labels
           - modifiers: Explain modifiers, clauses, and their relationships in Chinese
           - logic: Explain any notable grammatical patterns or points in Chinese
        6. **summary**: A brief mentor-style summary in Chinese, commenting on the speaker's performance, common pitfalls, and encouragement.
        
        Corrected text: {corrected_text}
        """

        class ChunkItemModel(BaseModel):
            english: str
            chinese: str

        class VocabularyItemModel(BaseModel):
            word: str
            pos: str
            meaning: str
            extra: Optional[str]

        class SyntaxAnalysisModel(BaseModel):
            skeleton: str
            modifiers: str
            logic: Optional[str]

        class DeepAnalysisResponseModel(BaseModel):
            translation: str
            literal_translation: Optional[str]
            chunking: List[ChunkItemModel]
            vocabulary: List[VocabularyItemModel]
            syntax: SyntaxAnalysisModel
            summary: str

        def _sync_generate_deep():
            return model.generate_content(
                deep_analysis_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,
                    response_mime_type="application/json",
                    response_schema=DeepAnalysisResponseModel
                )
            )
            
        deep_response = await loop.run_in_executor(None, _sync_generate_deep)
        deep_analysis_data = json.loads(deep_response.text)
        
        # 拼接分析报告
        correction_data["deep_analysis"] = deep_analysis_data
        
        return {
            "status": "success",
            "original_text": original_text,
            "analysis": correction_data
        }
