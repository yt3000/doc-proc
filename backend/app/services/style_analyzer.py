from typing import List, Dict
import re


class StyleAnalyzer:
    """风格分析器 - 检查文档风格统一性"""
    
    @staticmethod
    def analyze_text_style(text: str) -> Dict:
        """
        分析文本风格特征
        
        Args:
            text: 文本内容
            
        Returns:
            风格特征字典
        """
        # 分析句式长度分布
        sentences = StyleAnalyzer._split_sentences(text)
        sentence_lengths = [len(s) for s in sentences]
        
        avg_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        # 分析语气词使用
        modal_particles = StyleAnalyzer._count_modal_particles(text)
        
        # 分析正式程度
        formality_score = StyleAnalyzer._calculate_formality(text)
        
        # 分析标点符号使用
        punctuation_usage = StyleAnalyzer._analyze_punctuation(text)
        
        return {
            'avg_sentence_length': avg_length,
            'sentence_count': len(sentences),
            'modal_particles': modal_particles,
            'formality_score': formality_score,
            'punctuation': punctuation_usage
        }
    
    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        """分割句子"""
        # 按句号、问号、感叹号分割
        sentences = re.split(r'[。！？.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def _count_modal_particles(text: str) -> Dict[str, int]:
        """统计语气词使用"""
        particles = ['的', '了', '着', '过', '吗', '呢', '吧', '啊', '呀', '哇']
        
        counts = {}
        for particle in particles:
            counts[particle] = text.count(particle)
        
        return counts
    
    @staticmethod
    def _calculate_formality(text: str) -> float:
        """
        计算正式程度（0-1，1 最正式）
        
        Args:
            text: 文本
            
        Returns:
            正式程度分数
        """
        # 简单的正式程度计算
        # 口语化词汇
        colloquial_words = ['超', '特别', '挺', '蛮', '啥', '啥的', '呗', '嘛']
        
        colloquial_count = sum(text.count(word) for word in colloquial_words)
        
        # 正式词汇
        formal_words = ['因此', '然而', '此外', '综上所述', '鉴于', '据此', '对此']
        
        formal_count = sum(text.count(word) for word in formal_words)
        
        total = colloquial_count + formal_count
        if total == 0:
            return 0.7  # 中性
        
        return formal_count / total
    
    @staticmethod
    def _analyze_punctuation(text: str) -> Dict:
        """分析标点符号使用"""
        punctuation_marks = {
            'comma': '，',
            'period': '。',
            'question': '？',
            'exclamation': '！',
            'semicolon': '；',
            'colon': '：',
            'parenthesis': ('（', '）'),
            'bracket': ('【', '】'),
        }
        
        usage = {}
        for name, mark in punctuation_marks.items():
            if isinstance(mark, tuple):
                usage[name] = text.count(mark[0]) + text.count(mark[1])
            else:
                usage[name] = text.count(mark)
        
        return usage
    
    @staticmethod
    def detect_style_inconsistencies(
        segments: List[str]
    ) -> List[Dict]:
        """
        检测段落间的风格不一致
        
        Args:
            segments: 段落列表
            
        Returns:
            不一致列表
        """
        if len(segments) < 2:
            return []
        
        issues = []
        
        # 分析每个段落的风格
        styles = [StyleAnalyzer.analyze_text_style(seg) for seg in segments]
        
        # 检查句式长度差异
        avg_lengths = [s['avg_sentence_length'] for s in styles]
        length_diff = max(avg_lengths) - min(avg_lengths) if avg_lengths else 0
        
        if length_diff > 50:  # 句式长度差异过大
            issues.append({
                'type': 'style',
                'issue': 'sentence_length',
                'message': f'段落间句式长度差异较大 (最大差异：{length_diff:.1f}字)',
                'severity': 'medium'
            })
        
        # 检查正式程度差异
        formality_scores = [s['formality_score'] for s in styles]
        if formality_scores:
            formality_diff = max(formality_scores) - min(formality_scores)
            
            if formality_diff > 0.3:  # 正式程度差异较大
                issues.append({
                    'type': 'style',
                    'issue': 'formality',
                    'message': f'段落间正式程度差异较大 (最大差异：{formality_diff:.2f})',
                    'severity': 'high'
                })
        
        # 检查标点符号使用一致性
        for seg_idx, style in enumerate(styles):
            if style['punctuation'].get('exclamation', 0) > 5:
                issues.append({
                    'type': 'style',
                    'issue': 'punctuation',
                    'message': f'段落 {seg_idx + 1} 感叹号使用过多 ({style["punctuation"]["exclamation"]}个)',
                    'severity': 'low'
                })
        
        return issues
    
    @staticmethod
    def generate_style_report(
        segments: List[str]
    ) -> str:
        """
        生成风格分析报告
        
        Args:
            segments: 段落列表
            
        Returns:
            分析报告文本
        """
        inconsistencies = StyleAnalyzer.detect_style_inconsistencies(segments)
        
        if not inconsistencies:
            return "✓ 文档风格统一，无明显问题"
        
        report = "发现以下风格问题：\n\n"
        
        for issue in inconsistencies:
            report += f"- [{issue['severity'].upper()}] {issue['message']}\n"
        
        report += "\n建议保持文档风格的一致性，包括句式长度、正式程度和标点符号使用。"
        
        return report
