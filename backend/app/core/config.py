import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # 应用配置
    APP_NAME: str = "智能文档校对优化 API"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # 文件配置
    UPLOAD_DIR: str = os.path.join(os.path.dirname(__file__), "../../uploads")
    TEMP_DIR: str = os.path.join(os.path.dirname(__file__), "../../temp")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # API 配置
    API_PREFIX: str = "/api"
    CORS_ORIGINS: List[str] = ["*"]
    
    # 处理配置
    MAX_SEGMENTS: int = 100
    SEGMENT_MAX_LENGTH: int = 2000
    CONTEXT_WINDOW_SIZE: int = 4000
    API_TIMEOUT: int = 60
    
    def __init__(self):
        # 确保目录存在
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.TEMP_DIR, exist_ok=True)


settings = Settings()
