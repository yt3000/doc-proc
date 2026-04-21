import React, { useState } from 'react';
import { AppProvider, useApp } from '@/context/AppContext';
import Upload from '@/components/Upload';
import ConfigPanel from '@/components/ConfigPanel';
import Progress from '@/components/Progress';
import Result from '@/components/Result';
import { startCorrection, exportRevisedDocument } from '@/services/api';
import type { SegmentResult } from '@/types';

const AppContent: React.FC = () => {
  const {
    uploadedFile,
    fileId,
    uploadFile,
    llmConfig,
    correctionRules,
    isProcessing,
    setProcessing,
  } = useApp();

  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState('');
  const [results, setResults] = useState<SegmentResult[]>([]);
  const [showResult, setShowResult] = useState(false);

  const handleUploadComplete = (uploadedFileId: string) => {
    // 这里应该通过 context 更新 fileId
    // 简化处理，暂时不实现
    console.log('文件上传成功:', uploadedFileId);
  };

  const handleCorrection = async () => {
    if (!uploadedFile) {
      alert('请先上传文档');
      return;
    }

    setProcessing(true);
    setProgress(0);
    setProgressMessage('准备开始校对...');
    setShowResult(false);

    try {
      // TODO: 这里需要实现先上传文件获取 fileId
      // 简化演示，直接调用校对接口
      setProgress(50);
      setProgressMessage('校对进行中...');

      // 模拟校对过程
      await new Promise(resolve => setTimeout(resolve, 2000));

      setProgress(100);
      setProgressMessage('校对完成');

      // 模拟结果
      setResults([
        {
          segmentId: 'seg_0',
          correctedContent: '这是第一段的内容，经过校对后更加准确。',
          corrections: [
            {
              original: '准确的',
              suggested: '准确',
              reason: '语法优化',
              type: 'grammar',
            },
          ],
        },
        {
          segmentId: 'seg_1',
          correctedContent: '这是第二段的内容，没有发现需要修改的地方。',
          corrections: [],
        },
      ]);

      setShowResult(true);
    } catch (error) {
      console.error('校对失败:', error);
      alert('校对失败，请重试');
    } finally {
      setProcessing(false);
    }
  };

  const handleDownloadRevised = async () => {
    // TODO: 实现下载修订文档
    alert('下载修订文档功能开发中');
  };

  const handleDownloadComments = async () => {
    // TODO: 实现下载批注文档
    alert('下载批注文档功能开发中');
  };

  const handleRetrigger = () => {
    setShowResult(false);
    setResults([]);
    setProgress(0);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* 顶部导航栏 */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-800">
            智能文档校对优化
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            基于大模型的文档智能校对与优化
          </p>
        </div>
      </header>

      {/* 主内容区 */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="space-y-6">
          {/* 上传和配置 */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Upload onUploadComplete={handleUploadComplete} />
            <ConfigPanel />
          </div>

          {/* 开始校对按钮 */}
          <div className="flex justify-center">
            <button
              onClick={handleCorrection}
              disabled={!uploadedFile || isProcessing}
              className={`px-8 py-3 text-lg font-medium rounded-md transition-colors ${
                !uploadedFile || isProcessing
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-primary-600 text-white hover:bg-primary-700'
              }`}
            >
              {isProcessing ? '校对中...' : '开始校对'}
            </button>
          </div>

          {/* 进度展示 */}
          {isProcessing && (
            <Progress
              progress={progress}
              message={progressMessage}
            />
          )}

          {/* 结果展示 */}
          {showResult && (
            <Result
              segments={results}
              onDownloadRevised={handleDownloadRevised}
              onDownloadComments={handleDownloadComments}
              onRetrigger={handleRetrigger}
            />
          )}
        </div>
      </main>

      {/* 页脚 */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-sm text-gray-600">
          智能文档校对优化系统 v1.0.0
        </div>
      </footer>
    </div>
  );
};

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;
