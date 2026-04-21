# 智能文档校对优化系统

一个基于大模型的智能文档校对优化网页应用，支持用户上传 Word 文档，通过可配置的大模型进行分段智能校对，输出带修订标记和批注的 Word 文档。

## 功能特性

- 📄 **文档上传与处理**：支持 .docx 文档上传，自动提取文本内容
- 🤖 **多模型支持**：支持 Ollama、OpenAI、Anthropic 等多种大模型
- 🧠 **智能校对**：
  - 智能分段（保持语义完整）
  - 上下文关联校对
  - 专业术语一致性检查
  - 风格统一性检查
  - 自定义校对规则
- 📊 **实时进度**：流式响应，实时反馈校对进度
- 📝 **结果展示**：
  - 原文与校对结果对比
  - 修订高亮显示
  - 批注详细说明
- 💾 **文档导出**：支持下载修订文档和批注文档

## 技术栈

### 前端
- React 18 + TypeScript + Vite
- shadcn/ui 组件库
- Tailwind CSS
- Axios

### 后端
- FastAPI (Python 3.11+)
- python-docx
- requests

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 http://localhost:8000 启动

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 http://localhost:3000 启动

## 项目结构

```
doc-corrector/
├── frontend/           # React 前端
│   ├── src/
│   │   ├── components/     # UI 组件
│   │   ├── context/        # 状态管理
│   │   ├── services/       # API 服务
│   │   ├── types/          # TypeScript 类型
│   │   └── App.tsx         # 主应用
│   └── package.json
├── backend/            # FastAPI 后端
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── core/         # 核心配置
│   │   ├── services/     # 业务逻辑
│   │   └── main.py       # 应用入口
│   └── requirements.txt
└── README.md
```

## 核心模块

### 后端服务

- **DocumentParser**: 文档解析器，提取 docx 内容
- **SegmentStrategy**: 智能分段策略，保持语义完整
- **LLMClient**: 统一大模型客户端，支持多 provider
- **CorrectorService**: 校对服务，基于大模型进行智能校对
- **RevisionMarker**: Word 修订标记生成
- **CommentInjector**: 批注注入器

### 前端组件

- **Upload**: 文档上传组件（支持拖拽）
- **ConfigPanel**: 大模型配置面板
- **Progress**: 校对进度展示
- **Result**: 校对结果展示

## API 接口

### 文档上传
- `POST /api/upload/document` - 上传文档
- `GET /api/upload/files/{file_id}` - 获取文件信息

### 文档校对
- `POST /api/correct/start` - 开始校对
- `GET /api/correct/stream` - 流式校对（SSE）

### 文档下载
- `GET /api/download/{file_id}` - 下载原始文档
- `POST /api/download/export-revised` - 导出修订文档

## 开发计划

- [x] 初始化项目结构
- [x] 后端基础架构
- [x] 前端基础架构
- [ ] 文档处理核心模块完善
- [ ] 大模型集成完善
- [ ] 前后端联调
- [ ] 文档导出功能
- [ ] 单元测试
- [ ] 性能优化

## 注意事项

1. 使用 Ollama 本地部署时，确保服务运行在默认端口 11434
2. 使用 OpenAI/Anthropic 时需要有效的 API Key
3. 文档大小限制为 10MB
4. 建议文档内容不超过 10 万字

## License

MIT
