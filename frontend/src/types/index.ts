export interface DocumentSegment {
  id: string;
  content: string;
  startIndex: number;
  endIndex: number;
  corrections: Correction[];
}

export interface Correction {
  original: string;
  suggested: string;
  reason: string;
  type: 'grammar' | 'terminology' | 'style' | 'logic';
}

export interface LLMConfig {
  provider: 'ollama' | 'openai' | 'anthropic';
  apiKey: string;
  baseUrl?: string;
  modelName: string;
  temperature: number;
  maxTokens: number;
}

export interface CorrectionRules {
  checkTerminology: boolean;
  checkStyle: boolean;
  customRules: Record<string, string>;
}

export interface CorrectRequest {
  fileId: string;
  llmConfig: LLMConfig;
  correctionRules?: CorrectionRules;
}

export interface SegmentResult {
  segmentId: string;
  correctedContent: string;
  corrections: Correction[];
}

export interface CorrectResponse {
  success: boolean;
  message: string;
  results?: SegmentResult[];
  error?: string;
}

export interface UploadResponse {
  success: boolean;
  fileId: string;
  filename: string;
  size: number;
  message: string;
}

export interface StreamProgress {
  progress: number;
  message: string;
  results?: SegmentResult[];
  error?: string;
}
