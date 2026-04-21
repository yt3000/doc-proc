import React from 'react';
import type { SegmentResult, Correction } from '@/types';

interface ResultProps {
  segments: SegmentResult[];
  onDownloadRevised?: () => void;
  onDownloadComments?: () => void;
  onRetrigger?: () => void;
}

const Result: React.FC<ResultProps> = ({
  segments,
  onDownloadRevised,
  onDownloadComments,
  onRetrigger,
}) => {
  const [expandedSegment, setExpandedSegment] = React.useState<string | null>(null);

  const totalCorrections = segments.reduce(
    (sum, seg) => sum + seg.corrections.length,
    0
  );

  const toggleSegment = (segmentId: string) => {
    setExpandedSegment(
      expandedSegment === segmentId ? null : segmentId
    );
  };

  const getCorrectionTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      grammar: 'bg-red-100 text-red-800',
      terminology: 'bg-blue-100 text-blue-800',
      style: 'bg-yellow-100 text-yellow-800',
      logic: 'bg-purple-100 text-purple-800',
      spelling: 'bg-green-100 text-green-800',
      wording: 'bg-orange-100 text-orange-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-800">校对结果</h2>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600">
            共发现 <span className="font-medium text-primary-600">{totalCorrections}</span> 处建议
          </span>
          <div className="flex space-x-2">
            <button
              onClick={onDownloadRevised}
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
            >
              下载修订文档
            </button>
            <button
              onClick={onDownloadComments}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
            >
              下载批注文档
            </button>
            <button
              onClick={onRetrigger}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
            >
              重新校对
            </button>
          </div>
        </div>
      </div>

      {/* 结果列表 */}
      <div className="space-y-4">
        {segments.map((segment, index) => (
          <div
            key={segment.segmentId}
            className="border border-gray-200 rounded-lg overflow-hidden"
          >
            {/* 段落标题 */}
            <div
              className="bg-gray-50 px-4 py-3 cursor-pointer hover:bg-gray-100 transition-colors flex justify-between items-center"
              onClick={() => toggleSegment(segment.segmentId)}
            >
              <span className="font-medium text-gray-700">
                段落 {index + 1}
              </span>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-500">
                  {segment.corrections.length} 处建议
                </span>
                <span className="text-gray-400">
                  {expandedSegment === segment.segmentId ? '▲' : '▼'}
                </span>
              </div>
            </div>

            {/* 段落内容 */}
            {expandedSegment === segment.segmentId && (
              <div className="p-4 space-y-4">
                {/* 原文 */}
                <div>
                  <h4 className="text-sm font-medium text-gray-600 mb-2">原文：</h4>
                  <p className="text-gray-800 bg-gray-50 p-3 rounded">
                    {segment.correctedContent}
                  </p>
                </div>

                {/* 修正建议 */}
                {segment.corrections.length > 0 ? (
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium text-gray-600">
                      修正建议：
                    </h4>
                    {segment.corrections.map((correction, idx) => (
                      <div
                        key={idx}
                        className="bg-yellow-50 border border-yellow-200 rounded p-3"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <span
                            className={`text-xs px-2 py-1 rounded ${getCorrectionTypeColor(
                              correction.type
                            )}`}
                          >
                            {correction.type.toUpperCase()}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-2">
                          <span className="font-medium">原文：</span>
                          <span className="line-through text-red-600">
                            {correction.original}
                          </span>
                        </p>
                        <p className="text-sm text-gray-700 mb-2">
                          <span className="font-medium">建议：</span>
                          <span className="text-green-600 font-medium">
                            {correction.suggested}
                          </span>
                        </p>
                        <p className="text-sm text-gray-600">
                          <span className="font-medium">理由：</span>
                          {correction.reason}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="bg-green-50 border border-green-200 rounded p-3">
                    <p className="text-sm text-green-700">
                      ✓ 此段落无需修改
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Result;
