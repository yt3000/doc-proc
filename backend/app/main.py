from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

from app.api import upload, correct, download, export
from app.core.config import settings

app = FastAPI(
    title="智能文档校对优化 API",
    description="基于大模型的文档校对和优化服务",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(upload.router, prefix="/api/upload", tags=["文档上传"])
app.include_router(correct.router, prefix="/api/correct", tags=["文档校对"])
app.include_router(download.router, prefix="/api/download", tags=["文档下载"])
app.include_router(export.router, prefix="/api/export", tags=["文档导出"])


@app.get("/")
async def root():
    return {
        "app": "智能文档校对优化 API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
