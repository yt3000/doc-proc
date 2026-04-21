from typing import List, Dict, Optional
import json
import re
from app.services.llm import LLMClient
from app.core.schemas import Correction


class CorrectorService:
    """校对服务 - 基于大模型进行智能校对"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def correct_segment(self, text: str, context: Optional[str] = None,
                       custom_rules: Optional[Dict[str, str]] = None) -> tuple[str, List[Correction]]:
        """
        校对单个段落
        
        Args:
            text: 待校对的文本
            context: 上下文信息
            custom_rules: 自定义校对规则
            
        Returns:
            (校对后的文本，修正列表)
        """
        system_prompt = self._build_system_prompt(custom_rules)
        user_prompt = self._build_user_prompt(text, context)
        
        messages = [{"role": "user", "content": user_prompt}]
        
        try:
            response = self.llm.chat(messages, system_prompt)
            return self._parse_response(response)
        except Exception as e:
            # API 调用失败，返回原文
            return text, []
    
    def _build_system_prompt(self, custom_rules: Optional[Dict[str, str]] = None) -> str:
        """构建系统提示"""
        base_prompt = """你是一个专业的文档校对助手，请仔细检查以下文本，找出并修正：
1. 语法错误
2. 拼写错误
3. 用词不当
4. 逻辑不通
5. 术语不一致
6. 风格不统一

请以 JSON 格式返回结果，格式如下：
{
    "corrected_text": "修改后的完整文本",
    "corrections": [
        {
            "original": "原文",
            "suggested": "建议",
            "reason": "修改理由",
            "type": "grammar|spelling|wording|logic|terminology|style"
        }
    ]
}

如果不需要修改，corrections 为空数组。"""
        
        if custom_rules:
            custom_prompt = "\n\n额外规则：\n"
            for key, value in custom_rules.items():
                custom_prompt += f"- {key}: {value}\n"
            base_prompt += custom_prompt
        
        return base_prompt
    
    def _build_user_prompt(self, text: str, context: Optional[str] = None) -> str:
        """构建用户提示"""
        prompt = f"请校对以下文本：\n\n{text}"
        
        if context:
            prompt = f"{context}\n\n请基于上述上下文，校对以下文本：\n\n{text}"
        
        prompt += "\n\n请返回 JSON 格式的结果。"
        
        return prompt
    
    def _parse_response(self, response: str) -> tuple[str, List[Correction]]:
        """解析模型回复"""
        try:
            # 尝试提取 JSON 部分
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
                corrected_text = result.get("corrected_text", "")
                corrections = []
                
                for corr in result.get("corrections", []):
                    correction = Correction(
                        original=corr.get("original", ""),
                        suggested=corr.get("suggested", ""),
                        reason=corr.get("reason", ""),
                        correction_type=corr.get("type", "grammar")
                    )
                    corrections.append(correction)
                
                return corrected_text, corrections
            else:
                # 如果没有 JSON 格式，直接返回原文
                return response, []
        except Exception as e:
            # 解析失败，返回原文
            return response, []
