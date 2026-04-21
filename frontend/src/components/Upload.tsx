import React, { useState, useCallback } from 'react';
import { useApp } from '@/context/AppContext';
import { uploadDocument } from '@/services/api';

interface UploadProps {
  onUploadComplete?: (fileId: string) => void;
}

const Upload: React.FC<UploadProps> = ({ onUploadComplete }) => {
  const { uploadFile, uploadedFile, clearFile } = useApp();
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    setError(null);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, []);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, []);

  const handleFileSelect = async (file: File) => {
    // 验证文件类型
    if (!file.name.endsWith('.docx')) {
      setError('只支持 .docx 格式文件');
      return;
    }

    // 验证文件大小 (10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('文件大小不能超过 10MB');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      uploadFile(file);
      
      // 上传到后端
      const response = await uploadDocument(file);
      
      if (response.success) {
        onUploadComplete?.(response.fileId);
      } else {
        setError(response.message || '上传失败');
        clearFile();
      }
    } catch (err) {
      setError('上传失败，请重试');
      clearFile();
    } finally {
      setUploading(false);
    }
  };

  const handleClear = () => {
    clearFile();
    setError(null);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">文档上传</h2>
      
      {!uploadedFile ? (
        <div
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            isDragging
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <div className="space-y-4">
            <div className="text-5xl text-gray-400">📄</div>
            <div>
              <p className="text-lg text-gray-600">
                拖拽文档到此处，或
                <label className="text-primary-600 cursor-pointer font-medium ml-1">
                  点击选择
                  <input
                    type="file"
                    accept=".docx"
                    className="hidden"
                    onChange={handleFileChange}
                  />
                </label>
              </p>
              <p className="text-sm text-gray-500 mt-2">
                只支持 .docx 格式，最大 10MB
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-gray-50 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="text-4xl">📄</div>
              <div>
                <p className="font-medium text-gray-800">{uploadedFile.name}</p>
                <p className="text-sm text-gray-500">
                  {(uploadedFile.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
            <button
              onClick={handleClear}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-100 transition-colors"
              disabled={uploading}
            >
              移除
            </button>
          </div>
          {uploading && (
            <div className="mt-4 flex items-center space-x-2 text-primary-600">
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-primary-600 border-t-transparent"></div>
              <span>上传中...</span>
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}
    </div>
  );
};

export default Upload;
