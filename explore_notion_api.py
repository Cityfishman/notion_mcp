"""
Notion SDK API 方法探索工具
用于查看 notion_client.Client 支持的所有方法和用法
"""

import os
from dotenv import load_dotenv
from notion_client import Client

# 加载环境变量
load_dotenv()

# 初始化客户端
try:
    client = Client(auth=os.getenv('NOTION_API_KEY'))
    print("✅ Notion 客户端初始化成功\n")
except Exception as e:
    print(f"❌ 初始化失败: {e}\n")
    client = None

print("=" * 80)
print("📚 Notion SDK 可用方法列表")
print("=" * 80)

if client:
    # 获取所有非私有方法
    methods = [attr for attr in dir(client) if not attr.startswith('_')]
    
    print("\n🔧 Client 实例的主要属性和方法:\n")
    for method in methods:
        attr = getattr(client, method)
        attr_type = type(attr).__name__
        print(f"  • client.{method:<20} ({attr_type})")
    
    print("\n" + "=" * 80)
    print("📑 主要 API 端点详细说明")
    print("=" * 80)
    
#     # Pages API
#     print("\n1️⃣  Pages API (client.pages)")
#     print("   用于创建、读取、更新页面")
#     if hasattr(client, 'pages'):
#         pages_methods = [m for m in dir(client.pages) if not m.startswith('_')]
#         for method in pages_methods:
#             print(f"      • client.pages.{method}()")
    
#     # Blocks API
#     print("\n2️⃣  Blocks API (client.blocks)")
#     print("   用于操作页面中的内容块")
#     if hasattr(client, 'blocks'):
#         blocks_methods = [m for m in dir(client.blocks) if not m.startswith('_')]
#         for method in blocks_methods:
#             print(f"      • client.blocks.{method}")
        
#         # Blocks.children
#         if hasattr(client.blocks, 'children'):
#             print("\n      📦 Blocks.children (子块操作):")
#             children_methods = [m for m in dir(client.blocks.children) if not m.startswith('_')]
#             for method in children_methods:
#                 print(f"         • client.blocks.children.{method}()")
    
#     # Databases API
#     print("\n3️⃣  Databases API (client.databases)")
#     print("   用于查询和操作数据库")
#     if hasattr(client, 'databases'):
#         db_methods = [m for m in dir(client.databases) if not m.startswith('_')]
#         for method in db_methods:
#             print(f"      • client.databases.{method}()")
    
#     # Search API
#     print("\n4️⃣  Search API (client.search)")
#     print("   全局搜索页面和数据库")
#     if hasattr(client, 'search') and callable(client.search):
#         print(f"      • client.search(query='关键词', ...)")
    
#     # Users API
#     print("\n5️⃣  Users API (client.users)")
#     print("   获取用户信息")
#     if hasattr(client, 'users'):
#         users_methods = [m for m in dir(client.users) if not m.startswith('_')]
#         for method in users_methods:
#             print(f"      • client.users.{method}()")
    
#     # Comments API
#     print("\n6️⃣  Comments API (client.comments)")
#     print("   创建和获取评论")
#     if hasattr(client, 'comments'):
#         comments_methods = [m for m in dir(client.comments) if not m.startswith('_')]
#         for method in comments_methods:
#             print(f"      • client.comments.{method}()")
    
#     print("\n" + "=" * 80)
#     print("💡 常用方法示例")
#     print("=" * 80)
    
#     print("""
#     # 搜索页面
#     client.search(query="会议记录", filter={"property": "object", "value": "page"})
    
#     # 获取页面
#     client.pages.retrieve(page_id="abc123...")
    
#     # 创建页面
#     client.pages.create(
#         parent={"page_id": "parent_id"},
#         properties={"title": {"title": [{"text": {"content": "新页面"}}]}}
#     )
    
#     # 更新页面
#     client.pages.update(page_id="abc123...", properties={...})
    
#     # 获取页面内容块
#     client.blocks.children.list(block_id="page_id")
    
#     # 追加内容块
#     client.blocks.children.append(
#         block_id="page_id",
#         children=[{"object": "block", "type": "paragraph", ...}]
#     )
    
#     # 查询数据库
#     client.databases.query(
#         database_id="db_id",
#         filter={"property": "Status", "select": {"equals": "进行中"}}
#     )
    
#     # 获取当前用户
#     client.users.me()
    
#     # 列出所有用户
#     client.users.list()
#     """)
    
#     print("\n" + "=" * 80)
#     print("📖 获取方法详细帮助")
#     print("=" * 80)
#     print("""
#     在 Python 交互式环境中使用 help() 查看详细文档:
    
#     >>> from notion_client import Client
#     >>> client = Client(auth="your_key")
#     >>> help(client.pages.create)
#     >>> help(client.blocks.children.append)
#     """)

# print("\n✅ 探索完成！")
# print("💡 提示: 运行 'python -i explore_notion_api.py' 可进入交互模式继续探索\n")
