from fastapi import HTTPException, status


class DocumentError(Exception):
    """文档处理异常"""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code


class APIError(Exception):
    """API 调用异常"""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code


class ValidationError(Exception):
    """验证异常"""
    def __init__(self, message: str, status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY):
        self.message = message
        self.status_code = status_code
