import React from 'react';

interface ProgressProps {
  progress: number;
  message: string;
  onCancel?: () => void;
}

const Progress: React.FC<ProgressProps> = ({ progress, message, onCancel }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">校对进度</h2>
      
      {/* 进度条 */}
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">{message}</span>
          <span className="text-sm font-medium text-primary-600">{progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            className="bg-primary-600 h-3 rounded-full transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      {/* 状态图标 */}
      <div className="flex items-center justify-center py-6">
        <div className="relative">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-200 border-t-primary-600"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-lg font-medium text-primary-600">{progress}%</span>
          </div>
        </div>
      </div>

      {/* 取消按钮 */}
      {onCancel && (
        <div className="text-center">
          <button
            onClick={onCancel}
            className="px-6 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
          >
            取消校对
          </button>
        </div>
      )}
    </div>
  );
};

export default Progress;
