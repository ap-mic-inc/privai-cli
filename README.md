# PrivAI CLI

<!-- Badges -->
<p align="center">
  <a href="https://pypi.org/project/privai-cli/"><img src="https://img.shields.io/pypi/v/privai-cli.svg" alt="PyPI Version"></a>
  <a href="https://github.com/your-username/privai-cli/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/privai-cli.svg" alt="License"></a>
  <a href="https://github.com/your-username/privai-cli/actions"><img src="https://img.shields.io/github/actions/workflow/status/your-username/privai-cli/main.yml?branch=main" alt="Build Status"></a>
  <a href="https://python.org"><img src="https://img.shields.io/pypi/pyversions/privai-cli.svg" alt="Python Version"></a>
</p>

**`privai-cli`** 是一個功能強大的命令列介面（CLI）工具，旨在簡化與 PrivAI 平台的互動。無論您是想管理 AI 模型、處理檔案、優化提示詞，還是進行即時問答，這個工具都能讓您在終端機中輕鬆完成。

## ✨ 主要功能

*   **🤖 模型管理**: 輕鬆列出所有可用的 AI 模型。
*   **📂 檔案與資料集**: 上傳、下載、刪除和管理您的檔案與資料集（Filesets）。
*   **🚀 資料處理**: 提交資料集以進行嵌入（Embedding）處理。
*   **💬 即時互動**: 與模型進行聊天，支援 RAG 功能。
*   **✍️ 提示詞工程**: 建立、管理並自動優化您的提示詞（Prompts）。
*   **❓ QA 生成**: 從您的資料集中自動生成問答對。
*   **🔌 LangServe 整合**: 直接與 LangServe 的 runnables 互動。

## 🚀 快速入門

### 1. 安裝

首先，複製本專案並在虛擬環境中安裝：

```bash
git clone https://github.com/your-username/privai-cli.git
cd privai-cli

# 建立並啟用虛擬環境
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# .\venv\Scripts\activate  # Windows

# 使用 pip 安裝專案及其依賴
pip install .
```
安裝完成後，`privai-cli` 指令即可在已啟用的虛擬環境中使用。

### 2. 設定

在使用之前，您需要設定 PrivAI 的 API URL 和您的 Bearer Token：

```bash
privai-cli config set --api-url <your-api-url> --token <your-bearer-token>
```

### 3. 完整工作流程範例

體驗一個從上傳檔案到進行 RAG 問答的完整流程：

```bash
# 1. 上傳一個檔案
privai-cli files upload ./path/to/your/document.pdf

# 2. 建立一個資料集 (Fileset)
# (請將 <file-id-1> 替換為上一步回傳的檔案 ID)
privai-cli filesets create --file-ids <file-id-1>

# 3. 提交資料集進行處理
# (請將 <fileset-id-1> 替換為上一步回傳的資料集 ID)
privai-cli filesets commit <fileset-id-1>

# 4. 建立一個聊天用的 Prompt
privai-cli prompt create "You are a helpful assistant."

# 5. 開始聊天！
# (請將 <prompt-id-1> 和 <fileset-id-1> 替換為先前步驟中獲得的 ID)
privai-cli chat completions \
  --model "gpt-4" \
  --messages '[{"role": "user", "content": "根據我提供的文件，總結一下重點。"}]' \
  --fileset-id <fileset-id-1> \
  --prompt-id <prompt-id-1>
```

## 📚 指令參考

以下是 `privai-cli` 的詳細指令說明。

### 模型 (Models)

*   `privai-cli models list`: 列出所有可用的 AI 模型。

### 檔案 (Files)

*   `privai-cli files list`: 列出檔案，支援篩選和分頁。
*   `privai-cli files upload <path> --purpose <purpose>`: 上傳一個檔案。
*   `privai-cli files get <file-id>`: 根據 ID 獲取特定檔案的元數據。
*   `privai-cli files delete <file-id>`: 根據 ID 刪除一個檔案。
*   `privai-cli files content <file-id> --file-type <type>`: 下載特定檔案的內容。

### 資料集 (Filesets)

*   `privai-cli filesets list`: 列出所有資料集。
*   `privai-cli filesets create --file-ids <id1> <id2> ...`: 建立一個新的資料集。
*   `privai-cli filesets get <fileset-id>`: 根據 ID 獲取特定資料集。
*   `privai-cli filesets update <fileset-id> --file-ids <id1> ...`: 更新資料集的檔案列表或元數據。
*   `privai-cli filesets delete <fileset-id>`: 根據 ID 刪除一個資料集。
*   `privai-cli filesets commit <fileset-id>`: 提交資料集以進行嵌入處理。
*   `privai-cli filesets duplicate <fileset-id>`: 複製一個資料集。

### 聊天 (Chat)

*   `privai-cli chat completions --model <model> --messages '[{"role": "user", ...}]'`: 發起一個聊天請求。
    *   可選參數: `--prompt-id`, `--fileset-id`, `--temperature`

### 提示詞 (Prompt)

*   `privai-cli prompt create <value>`: 建立一個新的提示詞。
*   `privai-cli prompt list`: 列出所有提示詞。
*   `privai-cli prompt get <prompt-id>`: 根據 ID 獲取特定提示詞。
*   `privai-cli prompt delete <prompt-id>`: 根據 ID 刪除一個提示詞。
*   `privai-cli prompt optimize-auto <prompt-id>`: 自動優化一個提示詞。
*   `privai-cli prompt optimize-instruct <prompt-id> --current-issue <issue> --desired-behavior <behavior>`: 根據指示優化提示詞。

### 問答生成 (QA)

*   `privai-cli qa generate --fileset-id <fileset-id>`: 從資料集中生成問答對。

### LangServe

*   `privai-cli langserve input-schema`: 獲取 runnable 的輸入 schema。
*   `privai-cli langserve output-schema`: 獲取 runnable 的輸出 schema。
*   `privai-cli langserve config-schema`: 獲取 runnable 的設定 schema。
*   `privai-cli langserve invoke '<input-json>'`: 叫用 runnable。
*   `privai-cli langserve stream '<input-json>'`: 以串流方式叫用 runnable。

## 🤝 貢獻

歡迎各種形式的貢獻！如果您有任何建議或發現了 bug，請隨時提出 [Issue](https://github.com/your-username/privai-cli/issues) 或發送 [Pull Request](https://github.com/your-username/privai-cli/pulls)。

## 📄 授權條款

本專案採用 [MIT License](LICENSE) 授權。
