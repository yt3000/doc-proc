from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from app.core.config import settings
from app.core.exceptions import DocumentError

router = APIRouter()


@router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    """
    上传文档
    
    Args:
        file: 上传的 docx 文件
        
    Returns:
        文件 ID 和基本信息
    """
    # 验证文件类型
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="只支持 .docx 格式文件")
    
    # 验证文件大小
    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小不能超过 10MB")
    
    try:
        # 生成唯一文件 ID
        file_id = str(uuid.uuid4())
        
        # 保存文件
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.docx")
        
        # 读取并保存文件
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # 验证文件有效性
        from app.services.document import DocumentParser
        if not DocumentParser.validate_file(file_path):
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="无效的 docx 文件")
        
        return {
            "success": True,
            "file_id": file_id,
            "filename": file.filename,
            "size": len(contents),
            "message": "文档上传成功"
        }
    
    except DocumentError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败：{str(e)}")


@router.get("/files/{file_id}")
async def get_file_info(file_id: str):
    """
    获取文件信息
    
    Args:
        file_id: 文件 ID
        
    Returns:
        文件信息
    """
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.docx")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    file_size = os.path.getsize(file_path)
    
    return {
        "success": True,
        "file_id": file_id,
        "filename": f"{file_id}.docx",
        "size": file_size
    }
