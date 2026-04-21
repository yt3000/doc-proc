from typing import List, Tuple
import re


class SegmentStrategy:
    """智能分段策略 - 保持语义完整"""
    
    def __init__(self, max_length: int = 2000, context_window: int = 4000):
        self.max_length = max_length
        self.context_window = context_window
    
    def segment(self, text: str) -> List[Tuple[str, int, int]]:
        """
        将文本智能分段
        
        Args:
            text: 待分段的文本
            
        Returns:
            分段列表，每个元素为 (内容，起始索引，结束索引)
        """
        if not text.strip():
            return []
        
        # 按段落分割
        paragraphs = self._split_paragraphs(text)
        
        # 合并过短段落
        merged = self._merge_short_paragraphs(paragraphs)
        
        # 如果超过最大长度，进一步分割
        segments = []
        for para, start, end in merged:
            if len(para) > self.max_length:
                segments.extend(self._split_long_paragraph(para, start))
            else:
                segments.append((para, start, end))
        
        return segments
    
    def _split_paragraphs(self, text: str) -> List[Tuple[str, int, int]]:
        """按段落分割文本"""
        paragraphs = []
        current_index = 0
        
        # 按双换行符分割
        lines = re.split(r'\n\s*\n', text)
        
        for line in lines:
            line = line.strip()
            if line:
                start_index = text.find(line, current_index)
                end_index = start_index + len(line)
                paragraphs.append((line, start_index, end_index))
                current_index = end_index
        
        return paragraphs
    
    def _merge_short_paragraphs(
        self, paragraphs: List[Tuple[str, int, int]], min_length: int = 100
    ) -> List[Tuple[str, int, int]]:
        """合并过短的段落"""
        if not paragraphs:
            return []
        
        merged = []
        current_para = paragraphs[0]
        
        for para, start, end in paragraphs[1:]:
            # 如果当前段落太短，合并到下一段
            if len(current_para[0]) < min_length:
                current_para = (
                    current_para[0] + "\n\n" + para,
                    current_para[1],
                    end
                )
            else:
                merged.append(current_para)
                current_para = (para, start, end)
        
        merged.append(current_para)
        return merged
    
    def _split_long_paragraph(
        self, text: str, start_index: int
    ) -> List[Tuple[str, int, int]]:
        """分割过长的段落"""
        segments = []
        current_index = 0
        
        # 尝试按句号分割
        sentences = re.split(r'([。！？.!?])', text)
        
        current_segment = ""
        segment_start = start_index
        
        for i, sentence in enumerate(sentences):
            if not sentence.strip():
                continue
            
            # 如果是标点符号，合并到前一句
            if i > 0 and sentence in '。！？.!?':
                current_segment += sentence
                continue
            
            if current_segment:
                current_segment += sentence
            
            # 如果超过最大长度，分割
            if len(current_segment) >= self.max_length:
                segments.append((current_segment, segment_start, segment_start + len(current_segment)))
                segment_start = segment_start + len(current_segment)
                current_segment = ""
        
        # 添加剩余部分
        if current_segment.strip():
            segments.append((current_segment, segment_start, segment_start + len(current_segment)))
        
        return segments if segments else [(text, start_index, start_index + len(text))]
    
    def get_context_window(self, segments: List[Tuple[str, int, int]], 
                          current_index: int) -> str:
        """
        获取当前段落的上下文窗口
        
        Args:
            segments: 所有分段
            current_index: 当前分段索引
            
        Returns:
            上下文窗口文本
        """
        if not segments:
            return ""
        
        # 获取前后各一个段落作为上下文
        context_parts = []
        
        # 前一个段落
        if current_index > 0:
            context_parts.append("【上文】" + segments[current_index - 1][0])
        
        # 当前段落
        context_parts.append("【当前】" + segments[current_index][0])
        
        # 后一个段落
        if current_index < len(segments) - 1:
            context_parts.append("【下文】" + segments[current_index + 1][0])
        
        return "\n\n".join(context_parts)
