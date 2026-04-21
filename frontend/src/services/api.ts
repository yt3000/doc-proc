import axios from 'axios';
import type { 
  UploadResponse, 
  CorrectRequest, 
  CorrectResponse,
  StreamProgress 
} from '@/types';

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 上传文档
export const uploadDocument = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post<UploadResponse>('/upload/document', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

// 开始校对
export const startCorrection = async (request: CorrectRequest): Promise<CorrectResponse> => {
  const response = await apiClient.post<CorrectResponse>('/correct/start', request);
  return response.data;
};

// 流式校对
export const streamCorrection = async (
  request: CorrectRequest,
  onProgress: (progress: StreamProgress) => void
): Promise<void> => {
  const eventSource = new EventSource(
    `/correct/stream?${new URLSearchParams({
      fileId: request.fileId,
      llmConfig: JSON.stringify(request.llmConfig),
      correctionRules: request.correctionRules ? JSON.stringify(request.correctionRules) : '',
    }).toString()}`
  );

  return new Promise((resolve, reject) => {
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onProgress(data);

      if (data.error) {
        eventSource.close();
        reject(new Error(data.error));
      } else if (data.progress === 100) {
        eventSource.close();
        resolve();
      }
    };

    eventSource.onerror = (error) => {
      eventSource.close();
      reject(new Error('SSE 连接错误'));
    };
  });
};

// 下载原始文档
export const downloadOriginal = async (fileId: string): Promise<Blob> => {
  const response = await apiClient.get(`/download/${fileId}`, {
    responseType: 'blob',
  });
  return response.data;
};

// 导出修订文档
export const exportRevisedDocument = async (
  fileId: string,
  correctedContent: string
): Promise<Blob> => {
  const response = await apiClient.post(
    `/download/export-revised?fileId=${fileId}`,
    { correctedContent },
    {
      responseType: 'blob',
    }
  );
  return response.data;
};

export default apiClient;
