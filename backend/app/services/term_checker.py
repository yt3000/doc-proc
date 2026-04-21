from typing import List, Dict, Set
import re


class TermConsistencyChecker:
    """术语一致性检查器"""
    
    def __init__(self):
        self.terms: Dict[str, str] = {}  # 术语 -> 标准形式
        self.seen_terms: Dict[str, List[str]] = {}  # 术语概念 -> 所有出现的形式
    
    def extract_terms(self, text: str, min_length: int = 4) -> List[str]:
        """
        从文本中提取潜在术语
        
        Args:
            text: 文本内容
            min_length: 最小长度
            
        Returns:
            术语列表
        """
        # 提取中文词汇（简单实现）
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        
        # 提取英文词汇
        english_words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        
        # 提取数字 + 中文组合
        mixed_terms = re.findall(r'\d+[\u4e00-\u9fa5]+|[\u4e00-\u9fa5]+\d+', text)
        
        all_terms = chinese_words + english_words + mixed_terms
        
        # 过滤短词
        return [term for term in all_terms if len(term) >= min_length]
    
    def analyze_document(self, text: str) -> Dict[str, List[str]]:
        """
        分析文档中的术语使用情况
        
        Args:
            text: 文档文本
            
        Returns:
            术语变体映射
        """
        terms = self.extract_terms(text)
        
        # 统计术语出现形式
        term_variants: Dict[str, Set[str]] = {}
        
        for term in terms:
            # 规范化术语（转为小写等）
            normalized = self._normalize_term(term)
            
            if normalized not in term_variants:
                term_variants[normalized] = set()
            
            term_variants[normalized].add(term)
        
        # 过滤出有多个变体的术语
        inconsistent_terms = {
            k: list(v) for k, v in term_variants.items()
            if len(v) > 1
        }
        
        return inconsistent_terms
    
    def _normalize_term(self, term: str) -> str:
        """
        规范化术语
        
        Args:
            term: 原始术语
            
        Returns:
            规范化后的术语
        """
        # 转为小写
        normalized = term.lower()
        
        # 去除空格和特殊字符
        normalized = re.sub(r'[\s\-\_]', '', normalized)
        
        return normalized
    
    def suggest_standard_form(
        self, 
        variants: List[str]
    ) -> str:
        """
        建议标准术语形式
        
        Args:
            variants: 术语变体列表
            
        Returns:
            建议的标准形式
        """
        if not variants:
            return ""
        
        # 选择出现频率最高的形式（简化实现：选择最长的）
        return max(variants, key=len)
    
    def check_and_suggest(
        self, 
        text: str
    ) -> List[Dict]:
        """
        检查术语一致性并提供建议
        
        Args:
            text: 文本内容
            
        Returns:
            不一致的术语列表及其建议
        """
        inconsistent_terms = self.analyze_document(text)
        
        suggestions = []
        
        for normalized, variants in inconsistent_terms.items():
            if len(variants) > 1:
                standard = self.suggest_standard_form(variants)
                
                suggestions.append({
                    'type': 'terminology',
                    'original': variants,
                    'suggested': standard,
                    'reason': f'术语使用不一致，建议统一使用：{standard}'
                })
        
        return suggestions
