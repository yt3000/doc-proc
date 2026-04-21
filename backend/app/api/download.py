from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from app.core.config import settings

router = APIRouter()


@router.get("/{file_id}")
async def download_original(file_id: str):
    """
    下载原始文档
    
    Args:
        file_id: 文件 ID
        
    Returns:
        原始文件
    """
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.docx")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=file_path,
        filename=f"original_{file_id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@router.post("/export-revised")
async def export_revised_document(file_id: str, corrected_content: str):
    """
    导出修订后的文档
    
    Args:
        file_id: 文件 ID
        corrected_content: 修正后的内容
        
    Returns:
        修订后的文件
    """
    # TODO: 实现文档导出逻辑
    # 这里简化处理，直接返回原文
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.docx")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    output_path = os.path.join(settings.TEMP_DIR, f"revised_{file_id}.docx")
    
    # 复制原文（后续需要实现真正的修订标记）
    import shutil
    shutil.copy2(file_path, output_path)
    
    return FileResponse(
        path=output_path,
        filename=f"revised_{file_id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
