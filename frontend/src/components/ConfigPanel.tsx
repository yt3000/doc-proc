import React from 'react';
import { useApp } from '@/context/AppContext';

const ConfigPanel: React.FC = () => {
  const { llmConfig, updateLLMConfig, correctionRules, updateCorrectionRules } = useApp();

  const providers = [
    { value: 'ollama', label: 'Ollama (本地)' },
    { value: 'openai', label: 'OpenAI' },
    { value: 'anthropic', label: 'Anthropic' },
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">大模型配置</h2>
      
      {/* 模型提供商 */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          模型提供商
        </label>
        <select
          value={llmConfig.provider}
          onChange={(e) =>
            updateLLMConfig({ provider: e.target.value as 'ollama' | 'openai' | 'anthropic' })
          }
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          {providers.map((p) => (
            <option key={p.value} value={p.value}>
              {p.label}
            </option>
          ))}
        </select>
      </div>

      {/* API Key */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          API Key
          {llmConfig.provider === 'ollama' && (
            <span className="text-xs text-gray-500 ml-2">（Ollama 本地部署可不填）</span>
          )}
        </label>
        <input
          type="password"
          value={llmConfig.apiKey}
          onChange={(e) => updateLLMConfig({ apiKey: e.target.value })}
          placeholder={llmConfig.provider === 'ollama' ? '可选' : '请输入 API Key'}
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          disabled={llmConfig.provider === 'ollama'}
        />
      </div>

      {/* Base URL（可选） */}
      {llmConfig.provider !== 'ollama' && (
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Base URL（可选）
          </label>
          <input
            type="text"
            value={llmConfig.baseUrl || ''}
            onChange={(e) => updateLLMConfig({ baseUrl: e.target.value })}
            placeholder="例如：https://api.openai.com/v1"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
      )}

      {/* 模型名称 */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          模型名称
        </label>
        <input
          type="text"
          value={llmConfig.modelName}
          onChange={(e) => updateLLMConfig({ modelName: e.target.value })}
          placeholder="例如：llama2, gpt-4, claude-2"
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
      </div>

      {/* 温度参数 */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          温度 (Temperature): {llmConfig.temperature}
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={llmConfig.temperature}
          onChange={(e) => updateLLMConfig({ temperature: parseFloat(e.target.value) })}
          className="w-full"
        />
        <div className="flex justify-between text-xs text-gray-500">
          <span>精确 (0)</span>
          <span>创造性 (1)</span>
        </div>
      </div>

      {/* 校对规则 */}
      <div className="border-t pt-6">
        <h3 className="text-lg font-medium text-gray-800 mb-4">校对规则</h3>
        
        <div className="space-y-3">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={correctionRules.checkTerminology}
              onChange={(e) =>
                updateCorrectionRules({ checkTerminology: e.target.checked })
              }
              className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
            />
            <span className="ml-2 text-sm text-gray-700">
              检查专业术语一致性
            </span>
          </label>

          <label className="flex items-center">
            <input
              type="checkbox"
              checked={correctionRules.checkStyle}
              onChange={(e) =>
                updateCorrectionRules({ checkStyle: e.target.checked })
              }
              className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
            />
            <span className="ml-2 text-sm text-gray-700">
              检查风格统一性
            </span>
          </label>
        </div>
      </div>
    </div>
  );
};

export default ConfigPanel;
