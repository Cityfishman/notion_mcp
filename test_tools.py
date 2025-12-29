"""
测试 Notion MCP 工具的基本功能
"""

import os
from dotenv import load_dotenv
from main import get_notion_client, search_notion, get_page, create_page, append_block

load_dotenv()

print("=" * 80)
print("🧪 Notion MCP 功能测试")
print("=" * 80)

# 测试 1: 客户端初始化
print("\n【测试 1】Notion 客户端初始化")
try:
    client = get_notion_client()
    print("✅ 客户端初始化成功")
except Exception as e:
    print(f"❌ 失败: {e}")
    exit(1)

# 测试 2: 搜索功能
print("\n【测试 2】search_notion - 搜索页面")
print("提示: 将搜索你工作区中的所有内容")
result = search_notion(query="", filter_type="all", limit=5)
print(result)

# 测试 3: 获取页面（需要用户提供 page_id）
print("\n" + "=" * 80)
print("【测试 3】get_page - 获取页面内容")
print("=" * 80)
print("\n⚠️  需要手动测试:")
print("运行以下命令（替换为你的页面 ID）:")
print('python -c "from main import get_page; print(get_page(\'你的页面ID\'))"')

# 测试 4: 创建页面（需要用户提供 parent_id）
print("\n" + "=" * 80)
print("【测试 4】create_page - 创建新页面")
print("=" * 80)
print("\n⚠️  需要手动测试:")
print("运行以下命令（替换为你的父页面 ID）:")
print('python -c "from main import create_page; print(create_page(\'测试页面\', \'父页面ID\', \'page\', \'这是测试内容\'))"')

# 测试 5: 追加块（需要用户提供 page_id）
print("\n" + "=" * 80)
print("【测试 5】append_block - 追加内容块")
print("=" * 80)
print("\n⚠️  需要手动测试:")
print("运行以下命令（替换为你的页面 ID）:")
print('python -c "from main import append_block; print(append_block(\'你的页面ID\', \'测试内容\', \'paragraph\'))"')

print("\n" + "=" * 80)
print("✅ 自动化测试完成!")
print("=" * 80)
print("\n📝 完整功能列表:")
print("  1. ✅ search_notion - 搜索页面和数据库")
print("  2. ✅ get_page - 获取页面完整内容")
print("  3. ✅ create_page - 创建新页面")
print("  4. ✅ append_block - 追加内容块")
print("\n💡 下一步: 运行 MCP 服务器")
print("   命令: mcp run main.py")
print("   或者: uv run mcp run main.py")
