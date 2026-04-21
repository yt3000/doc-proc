from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import os
import json
import asyncio
from typing import Dict, List
from app.core.schemas import CorrectRequest, CorrectResponse, SegmentResult, Correction
from app.core.config import settings
from app.services.document import DocumentParser
from app.services.segment import SegmentStrategy
from app.services.llm import LLMClient
from app.services.corrector import CorrectorService

router = APIRouter()

# 临时存储（生产环境应使用数据库）
correcting_tasks: Dict[str, Dict] = {}


@router.post("/start")
async def start_correction(request: CorrectRequest) -> CorrectResponse:
    """
    开始文档校对
    
    Args:
        request: 校对请求
        
    Returns:
        校对结果
    """
    try:
        # 验证文件存在
        file_path = os.path.join(settings.UPLOAD_DIR, f"{request.file_id}.docx")
        if not os.path.exists(file_path):
            return CorrectResponse(
                success=False,
                message="文件不存在",
                error="文件不存在或已被删除"
            )
        
        # 提取文档文本
        text = DocumentParser.extract_text(file_path)
        if not text.strip():
            return CorrectResponse(
                success=False,
                message="文档内容为空",
                error="无法提取文档内容"
            )
        
        # 智能分段
        segment_strategy = SegmentStrategy(
            max_length=settings.SEGMENT_MAX_LENGTH,
            context_window=settings.CONTEXT_WINDOW_SIZE
        )
        segments = segment_strategy.segment(text)
        
        if not segments:
            return CorrectResponse(
                success=False,
                message="无法分割文档",
                error="文档分割失败"
            )
        
        # 初始化大模型
        llm_client = LLMClient(
            provider=request.llm_config.provider.value,
            api_key=request.llm_config.api_key,
            model_name=request.llm_config.model_name,
            base_url=request.llm_config.base_url,
            temperature=request.llm_config.temperature,
            max_tokens=request.llm_config.max_tokens
        )
        
        # 初始化校对服务
        corrector = CorrectorService(llm_client)
        
        # 逐段校对
        results = []
        for i, (segment_text, start_idx, end_idx) in enumerate(segments):
            # 获取上下文
            context = segment_strategy.get_context_window(segments, i)
            
            # 自定义规则
            custom_rules = None
            if request.correction_rules and request.correction_rules.custom_rules:
                custom_rules = request.correction_rules.custom_rules
            
            # 校对段落
            corrected_text, corrections = corrector.correct_segment(
                segment_text, context, custom_rules
            )
            
            # 构建结果
            segment_result = SegmentResult(
                segment_id=f"seg_{i}",
                corrected_content=corrected_text,
                corrections=[
                    Correction(
                        original=c.original,
                        suggested=c.suggested,
                        reason=c.reason,
                        correction_type=c.correction_type
                    )
                    for c in corrections
                ]
            )
            results.append(segment_result)
        
        # 合并所有修正
        all_corrections = []
        for result in results:
            all_corrections.extend(result.corrections)
        
        return CorrectResponse(
            success=True,
            message=f"校对完成，共处理 {len(segments)} 个段落，发现 {len(all_corrections)} 处建议",
            results=results
        )
    
    except Exception as e:
        return CorrectResponse(
            success=False,
            message="校对失败",
            error=str(e)
        )


@router.post("/stream")
async def stream_correction(request: CorrectRequest):
    """
    流式校对（实时反馈进度）
    
    Args:
        request: 校对请求
        
    Returns:
        SSE 流式响应
    """
    async def generate():
        try:
            # 验证文件
            file_path = os.path.join(settings.UPLOAD_DIR, f"{request.file_id}.docx")
            if not os.path.exists(file_path):
                yield f"data: {json.dumps({'error': '文件不存在'})}\n\n"
                return
            
            # 提取文档
            text = DocumentParser.extract_text(file_path)
            yield f"data: {json.dumps({'progress': 10, 'message': '正在提取文档内容...'})}\n\n"
            await asyncio.sleep(0.1)
            
            # 分段
            segment_strategy = SegmentStrategy()
            segments = segment_strategy.segment(text)
            yield f"data: {json.dumps({'progress': 20, 'message': f'文档已分割为 {len(segments)} 个段落'})}\n\n"
            await asyncio.sleep(0.1)
            
            # 初始化模型
            yield f"data: {json.dumps({'progress': 30, 'message': '正在初始化大模型...'})}\n\n"
            llm_client = LLMClient(
                provider=request.llm_config.provider.value,
                api_key=request.llm_config.api_key,
                model_name=request.llm_config.model_name,
                base_url=request.llm_config.base_url
            )
            corrector = CorrectorService(llm_client)
            
            # 逐段校对
            results = []
            for i, (segment_text, start_idx, end_idx) in enumerate(segments):
                progress = 30 + int((i + 1) / len(segments) * 60)
                yield f"data: {json.dumps({'progress': progress, 'message': f'正在校对第 {i+1}/{len(segments)} 段...'})}\n\n"
                
                context = segment_strategy.get_context_window(segments, i)
                corrected_text, corrections = corrector.correct_segment(segment_text, context)
                
                results.append({
                    "segment_id": f"seg_{i}",
                    "corrected_content": corrected_text,
                    "corrections": [
                        {
                            "original": c.original,
                            "suggested": c.suggested,
                            "reason": c.reason,
                            "type": c.correction_type
                        }
                        for c in corrections
                    ]
                })
            
            yield f"data: {json.dumps({'progress': 100, 'message': '校对完成', 'results': results})}\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
