## 产品概述

一个基于大模型的智能文档校对优化网页应用，支持用户上传 Word 文档，通过可配置的大模型进行分段智能校对，输出带修订标记和批注的 Word 文档。

## 核心功能

### 1. 文档上传与处理

- 用户上传 .docx 文档
- 自动提取文档文本内容
- 智能分段（保持语义完整，不切断句子）

### 2. 大模型配置

- 支持多模型配置（Ollama/OpenAI/Anthropic 等）
- 用户可设置 API Key、Base URL、模型名称
- 支持本地 Ollama 部署

### 3. 智能校对流程

- 分段检查优化
- 上下文汇总校对
- 专业术语一致性检查
- 风格统一性检查
- 可自定义校对规则

### 4. 结果输出

- 生成带 Word 修订模式标记的文档
- 生成带批注的文档
- 支持在线预览和下载

## 技术栈

### 前端

- **框架**: React 18 + TypeScript + Vite
- **UI 组件**: shadcn/ui（简洁优雅的 enterprise 级组件）
- **样式**: Tailwind CSS
- **状态管理**: React Hooks + Context（轻量级）
- **HTTP 客户端**: Axios
- **文档预览**: 自定义组件

### 后端

- **框架**: FastAPI（Python 3.11+）
- **文档处理**: python-docx（Word 文档操作）
- **大模型集成**: 原生 requests 库（轻量级，无需 LangChain 重量级依赖）
- **文件处理**: 内存处理 + 临时文件（处理完即删，不持久化存储）

### 核心架构设计

#### 系统架构图（简化版）

```
┌─────────────┐      ┌──────────────┐      ┌──────────┐
│  React 前端  │ ◄───► │  FastAPI 后端 │ ◄───► │ 大模型 API │
│  - 文件上传  │      │  - 文档解析   │      │ Ollama   │
│  - 配置面板  │      │  - 智能分段   │      │ OpenAI   │
│  - 进度展示  │      │  - 校对引擎   │      │ Anthropic│
│  - 结果对比  │      │  - 文档导出   │      └──────────┘
└─────────────┘      └──────────────┘
```

#### 核心模块划分

**1. 文档处理模块**

- `DocumentParser`: 提取 docx 文本内容
- `SegmentStrategy`: 智能分段算法（保持语义完整）
- `ContextManager`: 维护上下文窗口（内存中）

**2. 校对引擎模块**

- `LLMClient`: 统一大模型接口（支持多 provider）
- `CorrectorService`: 分段校对服务
- `TermConsistencyChecker`: 术语一致性检查
- `StyleAnalyzer`: 风格统一性分析

**3. 结果输出模块**

- `RevisionMarker`: Word 修订标记生成
- `CommentInjector`: 批注注入器
- `DocumentExporter`: 文档导出器

### 关键数据结构

```typescript
// 前端类型定义
interface DocumentSegment {
  id: string;
  content: string;
  startIndex: number;
  endIndex: number;
  corrections: Correction[];
}

interface Correction {
  original: string;
  suggested: string;
  reason: string;
  type: 'grammar' | 'terminology' | 'style' | 'logic';
}

interface LLMConfig {
  provider: 'ollama' | 'openai' | 'anthropic';
  apiKey: string;
  baseUrl?: string;
  modelName: string;
}
```

### 性能优化策略

1. **智能分段**: 合并过短段落，减少 API 调用次数
2. **上下文缓存**: 维护滑动窗口，避免重复分析
3. **流式响应**: 使用 SSE 实时反馈校对进度
4. **超时控制**: 单个文档处理超时 60 秒，超时后自动分段重试

### 错误处理

- 文档格式错误 → 友好提示
- API 调用失败 → 自动重试（3 次）+ 降级方案
- 大模型超时 → 分段重试机制
- 文件过大（>10MB） → 提示用户拆分文档

## 实现步骤

1. **初始化项目** - 前后端脚手架
2. **文档处理核心** - 智能分段、修订标记
3. **大模型集成** - 统一 API、校对逻辑
4. **前后端联调** - API 接口设计
5. **UI 组件开发** - 上传、进度、结果展示
6. **测试与部署** - 单元测试、启动脚本

## 项目结构

```
doc-corrector/
├── frontend/           # React 前端
│   ├── src/
│   │   ├── components/
│   │   │   ├── Upload.tsx
│   │   │   ├── ConfigPanel.tsx
│   │   │   ├── Progress.tsx
│   │   │   ├── Result.tsx
│   │   │   └── ui/     # shadcn 组件
│   │   ├── hooks/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
├── backend/            # FastAPI 后端
│   ├── app/
│   │   ├── api/
│   │   │   ├── upload.py
│   │   │   ├── correct.py
│   │   │   └── download.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── exceptions.py
│   │   ├── services/
│   │   │   ├── document.py
│   │   │   ├── segment.py
│   │   │   ├── llm.py
│   │   │   └── corrector.py
│   │   └── main.py
│   └── requirements.txt
└── README.md
```

### 1. 首页（上传与配置）

- **顶部导航栏**: 应用 Logo + 简洁导航
- **主内容区**: 
- 大尺寸拖拽上传区域（支持点击选择文件）
- 大模型配置面板（可折叠的卡片）
- 校对规则设置（术语检查、风格统一等开关）
- 开始校对按钮（带状态反馈）

### 2. 校对进度页

- **顶部**: 文档标题 + 进度条（百分比 + 当前分段）
- **中间**: 实时显示校对中的段落预览
- **底部**: 取消按钮 + 预计剩余时间

### 3. 结果展示页

- **左侧**: 文档原文预览（只读）
- **中间**: 校对后内容（高亮修订）
- **右侧**: 批注面板（点击修订项显示建议理由）
- **顶部操作栏**: 下载修订文档、下载批注文档、重新校对

## 交互设计

- 拖拽上传 → 文件自动识别
- 配置项即时保存（LocalStorage）
- 校对过程实时进度反馈
- 修订项悬停高亮
- 批注面板可折叠
