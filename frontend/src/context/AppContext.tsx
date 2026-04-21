import React, { createContext, useContext, useState, useCallback } from 'react';
import type { LLMConfig, CorrectionRules } from '@/types';

interface AppContextType {
  // 文档状态
  uploadedFile: File | null;
  fileId: string | null;
  uploadFile: (file: File) => void;
  clearFile: () => void;

  // LLM 配置
  llmConfig: LLMConfig;
  updateLLMConfig: (config: Partial<LLMConfig>) => void;

  // 校对规则
  correctionRules: CorrectionRules;
  updateCorrectionRules: (rules: Partial<CorrectionRules>) => void;

  // 处理状态
  isProcessing: boolean;
  setProcessing: (processing: boolean) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

const defaultLLMConfig: LLMConfig = {
  provider: 'ollama',
  apiKey: '',
  baseUrl: '',
  modelName: 'llama2',
  temperature: 0.7,
  maxTokens: 4096,
};

const defaultCorrectionRules: CorrectionRules = {
  checkTerminology: true,
  checkStyle: true,
  customRules: {},
};

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [fileId, setFileId] = useState<string | null>(null);
  const [llmConfig, setLLMConfig] = useState<LLMConfig>(defaultLLMConfig);
  const [correctionRules, setCorrectionRules] = useState<CorrectionRules>(defaultCorrectionRules);
  const [isProcessing, setIsProcessing] = useState(false);

  // 从 localStorage 加载配置
  React.useEffect(() => {
    const savedConfig = localStorage.getItem('llmConfig');
    if (savedConfig) {
      try {
        setLLMConfig(JSON.parse(savedConfig));
      } catch (e) {
        console.error('Failed to load LLM config:', e);
      }
    }

    const savedRules = localStorage.getItem('correctionRules');
    if (savedRules) {
      try {
        setCorrectionRules(JSON.parse(savedRules));
      } catch (e) {
        console.error('Failed to load correction rules:', e);
      }
    }
  }, []);

  // 保存配置到 localStorage
  React.useEffect(() => {
    localStorage.setItem('llmConfig', JSON.stringify(llmConfig));
  }, [llmConfig]);

  React.useEffect(() => {
    localStorage.setItem('correctionRules', JSON.stringify(correctionRules));
  }, [correctionRules]);

  const uploadFile = useCallback((file: File) => {
    setUploadedFile(file);
    setFileId(null); // 清除之前的 fileId
  }, []);

  const clearFile = useCallback(() => {
    setUploadedFile(null);
    setFileId(null);
  }, []);

  const updateLLMConfig = useCallback((config: Partial<LLMConfig>) => {
    setLLMConfig(prev => ({ ...prev, ...config }));
  }, []);

  const updateCorrectionRules = useCallback((rules: Partial<CorrectionRules>) => {
    setCorrectionRules(prev => ({ ...prev, ...rules }));
  }, []);

  const setProcessing = useCallback((processing: boolean) => {
    setIsProcessing(processing);
  }, []);

  return (
    <AppContext.Provider
      value={{
        uploadedFile,
        fileId,
        uploadFile,
        clearFile,
        llmConfig,
        updateLLMConfig,
        correctionRules,
        updateCorrectionRules,
        isProcessing,
        setProcessing,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
