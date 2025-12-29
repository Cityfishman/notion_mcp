# Notion MCP Server

一个基于 Model Context Protocol (MCP) 的 Notion API 集成工具，让 AI 助手能够操作你的 Notion 工作区。

## 功能特性

### 已实现工具 (Tools)

- ✅ **search_notion**: 在 Notion 工作区中搜索页面和数据库
- ✅ **get_page**: 获取页面完整内容（包括属性和所有内容块）
- ✅ **create_page**: 创建新的 Notion 页面（支持父页面/数据库）
- ✅ **append_block**: 向页面追加内容块（段落、标题、列表、待办事项等）
- ✅ **append_image**: 向页面追加图片块（支持外部图片 URL）

## 快速开始

### 1. 获取 Notion API Key

1. 访问 [Notion Integrations](https://www.notion.so/my-integrations)
2. 点击 **+ New integration**
3. 填写名称（如 "MCP Server"），选择关联的工作区
4. 复制生成的 **Internal Integration Token**（格式：`secret_xxxxx`）
5. 在需要操作的 Notion 页面右上角点击 **···** → **Add connections** → 选择你的 Integration

### 2. 配置环境变量

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# NOTION_API_KEY=secret_your_actual_key_here
```

### 3. 安装依赖

```bash
# 使用 uv 安装
uv pip install -e .

# 或使用 pip
pip install -e .
```

### 4. 运行服务器

```bash
# 使用 mcp 命令
mcp run main.py

# 或使用 uv
uv run mcp run main.py
```

## 工具使用指南

### 1. search_notion - 搜索页面和数据库

```python
search_notion(
    query="会议记录",           # 搜索关键词
    filter_type="page",         # 过滤类型: all, page, database
    limit=10                    # 返回结果数量
)
```

**示例输出：**
```
🔍 找到 3 个结果（关键词: '会议记录'）

1. 📄 团队周会 2024-12-01
   类型: page
   ID: abc123def456...
   URL: https://www.notion.so/abc123def456...
```

### 2. get_page - 获取页面内容

```python
get_page(
    page_id="abc123def456",     # 页面 ID（32位字符）
    include_blocks=True          # 是否包含内容块
)
```

**如何获取页面 ID：**
- URL: `https://www.notion.so/My-Page-123abc456def789?pvs=4`
- Page ID: `123abc456def789`（去掉连字符的32位字符）

**示例输出：**
```
📄 页面: 项目计划
🆔 ID: abc123def456
🔗 URL: https://www.notion.so/abc123def456
📅 创建时间: 2024-12-01T10:00:00.000Z
✏️  最后编辑: 2024-12-07T12:00:00.000Z

📝 页面内容:
--------------------------------------------------

# 项目目标
完成 Notion MCP 集成

• 实现搜索功能
• 实现页面管理
• 实现数据库查询
```

### 3. create_page - 创建新页面

```python
create_page(
    title="新项目文档",
    parent_id="abc123def456",    # 父页面或数据库 ID
    parent_type="page",          # "page" 或 "database"
    content="这是初始内容"        # 可选，支持多行
)
```

**示例输出：**
```
✅ 成功创建页面!

📄 标题: 新项目文档
🆔 ID: xyz789abc123
🔗 URL: https://www.notion.so/xyz789abc123
```

### 4. append_block - 追加内容块

```python
append_block(
    page_id="abc123def456",
    content="这是新添加的内容",
    block_type="paragraph"       # 块类型
)
```

**支持的块类型：**
- `paragraph` - 普通段落
- `heading_1` - 一级标题
- `heading_2` - 二级标题
- `heading_3` - 三级标题
- `bulleted_list_item` - 无序列表
- `numbered_list_item` - 有序列表
- `to_do` - 待办事项（默认未勾选）
- `code` - 代码块

### 5. append_image - 追加图片块

```python
append_image(
    page_id="abc123def456",
    image_url="https://example.com/image.jpg",  # 外部图片直接链接
    caption="这是图片说明"                        # 可选
)
```

**支持的图片格式：**
- `.jpg` / `.jpeg`
- `.png`
- `.gif`
- `.svg`
- `.bmp`
- `.tiff`
- `.heic`

**重要提示：**
- URL 必须是**直接链接**到图片文件（如 `https://domain.com/photo.jpg`）
- 不支持需要重定向或认证的 URL
- 推荐使用 CDN 或图床（如 Imgur、Cloudinary）托管的图片

**示例输出：**
```
✅ 成功添加图片到页面 abc123def456
🔗 URL: https://example.com/image.jpg
📝 说明: 这是图片说明
```

## 测试功能

运行测试脚本验证工具：

```bash
python test_tools.py
```

或手动测试单个工具：

```bash
# 搜索页面
python -c "from main import search_notion; print(search_notion('关键词'))"

# 获取页面
python -c "from main import get_page; print(get_page('你的页面ID'))"

# 创建页面
python -c "from main import create_page; print(create_page('测试页面', '父页面ID'))"

# 追加内容
python -c "from main import append_block; print(append_block('页面ID', '测试内容'))"
```

## 故障排查

### 错误：未找到 NOTION_API_KEY

确保 `.env` 文件存在且包含有效的 API Key：
```bash
cat .env  # 检查文件内容
```

### 错误：Could not find page

1. 检查 page_id 是否正确（32位字符，无连字符）
2. 确认该页面已授权给你的 Integration（在页面设置中 Add connections）

### 错误：Invalid request URL

page_id 格式错误，应为纯 32 位字符（如 `a1b2c3d4e5f6...`），不含连字符。

### 搜索返回空结果

1. 确认工作区中有内容
2. 检查 Integration 是否有访问权限
3. 尝试使用空字符串搜索所有内容：`search_notion("")`

## 在 Claude Desktop 中使用

配置 Claude Desktop 连接此 MCP 服务器：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "notion": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/你的用户名/notion_ai_mcp",
        "run",
        "mcp",
        "run",
        "main.py"
      ],
      "env": {
        "NOTION_API_KEY": "secret_your_api_key_here"
      }
    }
  }
}
```

重启 Claude Desktop 后，即可使用 AI 操作 Notion：
- "帮我搜索包含'项目'的页面"
- "获取页面 abc123 的内容"
- "创建一个名为'会议纪要'的新页面"

## 技术栈

- **MCP Framework**: FastMCP
- **Notion SDK**: notion-client 2.7.0
- **Environment**: python-dotenv
- **Python**: 3.12+

## 开发计划

- [x] 基础框架搭建
- [x] search_notion（搜索页面和数据库）
- [x] get_page（获取页面内容）
- [x] create_page（创建新页面）
- [x] append_block（追加内容块）
- [ ] query_database（查询数据库）
- [ ] update_page（更新页面属性）
- [ ] delete_block（删除内容块）
- [ ] Resources（数据库列表、页面内容资源）
- [ ] Prompts（Markdown 转换、内容总结）

## License

MIT
