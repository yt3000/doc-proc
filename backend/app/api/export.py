from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from typing import Dict, List
from app.core.config import settings
from app.core.schemas import Correction
from app.services.document_exporter import DocumentExporter

router = APIRouter()


@router.post("/revised")
async def export_revised_document(
    file_id: str,
    corrections: Dict[str, List[Correction]]
):
    """
    导出修订文档
    
    Args:
        file_id: 文件 ID
        corrections: 修正列表
        
    Returns:
        修订后的文档
    """
    # 验证原始文件
    original_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.docx")
    
    if not os.path.exists(original_path):
        raise HTTPException(status_code=404, detail="原始文件不存在")
    
    # 生成输出文件路径
    output_filename = f"revised_{file_id}.docx"
    output_path = os.path.join(settings.TEMP_DIR, output_filename)
    
    try:
        # 导出修订文档
        DocumentExporter.export_revised_file(
            original_path,
            output_path,
            corrections
        )
        
        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败：{str(e)}")


@router.post("/comments")
async def export_comments_document(
    file_id: str,
    corrections: Dict[str, List[Correction]]
):
    """
    导出批注文档
    
    Args:
        file_id: 文件 ID
        corrections: 修正列表
        
    Returns:
        带批注的文档
    """
    # 验证原始文件
    original_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.docx")
    
    if not os.path.exists(original_path):
        raise HTTPException(status_code=404, detail="原始文件不存在")
    
    # 生成输出文件路径
    output_filename = f"comments_{file_id}.docx"
    output_path = os.path.join(settings.TEMP_DIR, output_filename)
    
    try:
        # 导出批注文档
        DocumentExporter.export_comments_file(
            original_path,
            output_path,
            corrections
        )
        
        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败：{str(e)}")


@router.post("/merged")
async def export_merged_document(
    file_id: str,
    corrections: Dict[str, List[Correction]]
):
    """
    导出合并后的文档（直接应用所有修正）
    
    Args:
        file_id: 文件 ID
        corrections: 修正列表
        
    Returns:
        合并后的文档
    """
    # 验证原始文件
    original_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.docx")
    
    if not os.path.exists(original_path):
        raise HTTPException(status_code=404, detail="原始文件不存在")
    
    # 生成输出文件路径
    output_filename = f"merged_{file_id}.docx"
    output_path = os.path.join(settings.TEMP_DIR, output_filename)
    
    try:
        # 导出合并文档
        DocumentExporter.export_merged_file(
            original_path,
            output_path,
            corrections
        )
        
        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败：{str(e)}")
