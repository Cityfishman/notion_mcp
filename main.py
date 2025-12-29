import os
from typing import Optional
from dotenv import load_dotenv
from notion_client import Client
from mcp.server.fastmcp import FastMCP

# 加载环境变量
load_dotenv()

# 初始化 FastMCP
mcp = FastMCP('Notion MCP Server' )

# 初始化 Notion 客户端
def get_notion_client() -> Client:
    """获取 Notion 客户端实例"""
    api_key = os.getenv('NOTION_API_KEY')
    if not api_key:
        raise ValueError(
            "未找到 NOTION_API_KEY 环境变量。"
            "请在 .env 文件中设置你的 Notion API Key。"
            "获取方式: https://www.notion.so/my-integrations"
        )
    return Client(auth=api_key)


@mcp.tool(
    name='search_notion',
    description='在 Notion 工作区中搜索页面和数据库'
)
def search_notion(
    query: str,
    filter_type: str = 'all',
    limit: int = 10
) -> str:
    """
    搜索 Notion 页面和数据库
    
    Args:
        query: 搜索关键词
        filter_type: 过滤类型，支持: all, page, database
        limit: 返回结果数量限制（默认10）
    
    Returns:
        搜索结果列表（包含标题、ID、类型、URL）
    """
    try:
        notion = get_notion_client()
        
        # 构建过滤器
        search_params = {
            "query": query,
            "page_size": limit
        }
        
        if filter_type in ['page', 'database']:
            search_params["filter"] = {
                "property": "object",
                "value": filter_type
            }
        
        # 执行搜索
        response = notion.search(**search_params)
        
        results = response.get('results', [])
        
        if not results:
            return f"📭 未找到包含 '{query}' 的结果"
        
        # 格式化结果
        output = [f"🔍 找到 {len(results)} 个结果（关键词: '{query}'）\n"]
        
        for i, item in enumerate(results, 1):
            item_type = item.get('object', 'unknown')
            item_id = item.get('id', '').replace('-', '')
            url = item.get('url', '')
            
            # 获取标题
            if item_type == 'page':
                props = item.get('properties', {})
                title_prop = props.get('title', {})
                title_array = title_prop.get('title', [])
                title = title_array[0].get('text', {}).get('content', '无标题') if title_array else '无标题'
            elif item_type == 'database':
                title_array = item.get('title', [])
                title = title_array[0].get('text', {}).get('content', '无标题') if title_array else '无标题'
            else:
                title = '未知'
            
            # 图标
            icon = "📄" if item_type == 'page' else "🗄️"
            
            output.append(f"{i}. {icon} {title}")
            output.append(f"   类型: {item_type}")
            output.append(f"   ID: {item_id}")
            output.append(f"   URL: {url}\n")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ 搜索失败: {str(e)}"


@mcp.tool(
    name='get_page',
    description='获取 Notion 页面的完整内容（包括属性和所有内容块）'
)
def get_page(
    page_id: str,
    include_blocks: bool = True
) -> str:
    """
    获取 Notion 页面的完整内容
    
    Args:
        page_id: Notion 页面 ID（32位字符）
        include_blocks: 是否包含页面内容块（默认 True）
    
    Returns:
        页面的详细信息（标题、属性、内容）
    """
    try:
        notion = get_notion_client()
        
        # 获取页面属性
        page = notion.pages.retrieve(page_id=page_id)
        
        # 提取基本信息
        page_url = page.get('url', '')
        created_time = page.get('created_time', '')
        last_edited = page.get('last_edited_time', '')
        
        # 提取标题
        props = page.get('properties', {})
        title_prop = props.get('title', {})
        title_array = title_prop.get('title', [])
        title = title_array[0].get('text', {}).get('content', '无标题') if title_array else '无标题'
        
        # 构建输出
        output = [
            f"📄 页面: {title}",
            f"🆔 ID: {page_id}",
            f"🔗 URL: {page_url}",
            f"📅 创建时间: {created_time}",
            f"✏️  最后编辑: {last_edited}",
            ""
        ]
        
        # 获取页面内容块
        if include_blocks:
            blocks_response = notion.blocks.children.list(block_id=page_id)
            blocks = blocks_response.get('results', [])
            
            if blocks:
                output.append("📝 页面内容:")
                output.append("-" * 50)
                
                for block in blocks:
                    block_type = block.get('type', '')
                    block_content = _extract_block_text(block)
                    
                    if block_type.startswith('heading_'):
                        level = block_type.split('_')[1]
                        output.append(f"\n{'#' * int(level)} {block_content}")
                    elif block_type == 'paragraph':
                        output.append(block_content)
                    elif block_type == 'bulleted_list_item':
                        output.append(f"• {block_content}")
                    elif block_type == 'numbered_list_item':
                        output.append(f"1. {block_content}")
                    elif block_type == 'to_do':
                        checked = block.get('to_do', {}).get('checked', False)
                        checkbox = "☑" if checked else "☐"
                        output.append(f"{checkbox} {block_content}")
                    elif block_type == 'code':
                        language = block.get('code', {}).get('language', 'plain text')
                        output.append(f"\n```{language}\n{block_content}\n```")
                    else:
                        output.append(f"[{block_type}] {block_content}")
            else:
                output.append("📭 页面内容为空")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ 获取页面失败: {str(e)}\n\n提示：确认 page_id 正确且 Integration 已被授权访问此页面"


@mcp.tool(
    name='create_page',
    description='在 Notion 中创建新页面'
)
def create_page(
    title: str,
    parent_id: str,
    parent_type: str = 'page',
    content: str = ''
) -> str:
    """
    创建新的 Notion 页面
    
    Args:
        title: 页面标题
        parent_id: 父页面或数据库的 ID
        parent_type: 父级类型，支持: page, database
        content: 初始内容（可选，支持多行文本）
    
    Returns:
        新创建页面的信息
    """
    try:
        notion = get_notion_client()
        
        # 构建父级引用
        if parent_type == 'page':
            parent = {"page_id": parent_id}
        elif parent_type == 'database':
            parent = {"database_id": parent_id}
        else:
            return f"❌ 不支持的 parent_type: {parent_type}，仅支持 'page' 或 'database'"
        
        # 构建页面属性
        if parent_type == 'page':
            properties = {
                "title": {
                    "title": [
                        {
                            "text": {"content": title}
                        }
                    ]
                }
            }
        else:  # database
            # 数据库类型需要 Name 属性
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {"content": title}
                        }
                    ]
                }
            }
        
        # 创建页面
        new_page = notion.pages.create(
            parent=parent,
            properties=properties
        )
        
        page_id = new_page.get('id', '').replace('-', '')
        page_url = new_page.get('url', '')
        
        # 如果有初始内容，添加到页面
        if content:
            content_lines = content.split('\n')
            children = []
            
            for line in content_lines:
                if line.strip():  # 跳过空行
                    children.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": line}
                                }
                            ]
                        }
                    })
            
            if children:
                notion.blocks.children.append(
                    block_id=page_id,
                    children=children
                )
        
        return f"✅ 成功创建页面!\n\n📄 标题: {title}\n🆔 ID: {page_id}\n🔗 URL: {page_url}"
        
    except Exception as e:
        return f"❌ 创建页面失败: {str(e)}\n\n提示：\n1. 检查 parent_id 是否正确\n2. 确认 Integration 已被授权访问父页面/数据库\n3. 如果是数据库，确认使用 parent_type='database'"


@mcp.tool(
    name='append_image',
    description='向指定的 Notion 页面追加图片块（支持外部图片 URL）'
)
def append_image(
    page_id: str,
    image_url: str,
    caption: str = ''
) -> str:
    """
    向 Notion 页面追加图片块
    
    Args:
        page_id: Notion 页面 ID（32位字符）
        image_url: 图片的外部 URL（必须是直接链接，支持 .jpg/.png/.gif/.svg 等）
        caption: 可选的图片说明文字
    
    Returns:
        成功添加的图片信息
    """
    try:
        notion = get_notion_client()
        
        # 构建图片块
        image_block = {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {
                    "url": image_url
                }
            }
        }
        
        # 调用 API 追加图片块
        response = notion.blocks.children.append(
            block_id=page_id,
            children=[image_block]
        )
        
        # 如果有说明文字，追加一个段落
        if caption:
            notion.blocks.children.append(
                block_id=page_id,
                children=[{
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": f"📷 {caption}"}
                        }]
                    }
                }]
            )
            return f"✅ 成功添加图片到页面 {page_id}\n🔗 URL: {image_url}\n📝 说明: {caption}"
        
        return f"✅ 成功添加图片到页面 {page_id}\n🔗 URL: {image_url}"
        
    except Exception as e:
        return f"❌ 添加图片失败: {str(e)}\n\n提示：\n1. 检查 image_url 是否为有效的外部直接链接\n2. 确认 URL 指向支持的图片格式（jpg/png/gif/svg等）\n3. 确认该 Integration 已被授权访问此页面\n4. 验证 NOTION_API_KEY 是否有效"


@mcp.tool(
    name='append_block',
    description='向指定的 Notion 页面追加内容块（段落、标题、列表等）'
)
def append_block(
    page_id: str,
    content: str,
    block_type: str = 'paragraph'
) -> str:
    """
    向 Notion 页面追加内容块
    
    Args:
        page_id: Notion 页面 ID（32位字符，可从页面 URL 获取）
        content: 要添加的文本内容
        block_type: 块类型，支持: paragraph, heading_1, heading_2, heading_3, 
                    bulleted_list_item, numbered_list_item, to_do, code
    
    Returns:
        成功添加的块信息
    """
    try:
        notion = get_notion_client()
        
        # 构建块数据结构
        block_data = {
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": content}
                    }
                ]
            }
        }
        
        # 特殊处理 to_do 类型（需要 checked 字段）
        if block_type == "to_do":
            block_data[block_type]["checked"] = False
        
        # 特殊处理 code 类型（需要 language 字段）
        if block_type == "code":
            block_data[block_type]["language"] = "plain text"
        
        # 调用 API 追加块
        response = notion.blocks.children.append(
            block_id=page_id,
            children=[block_data]
        )
        
        return f"✅ 成功添加 {block_type} 块到页面 {page_id}\n内容: {content}"
        
    except Exception as e:
        return f"❌ 添加失败: {str(e)}\n\n提示：\n1. 检查 page_id 是否正确\n2. 确认该 Integration 已被授权访问此页面\n3. 验证 NOTION_API_KEY 是否有效"


# 辅助函数：提取块的文本内容
def _extract_block_text(block: dict) -> str:
    """从块对象中提取纯文本内容"""
    block_type = block.get('type', '')
    
    if block_type in ['paragraph', 'heading_1', 'heading_2', 'heading_3', 
                      'bulleted_list_item', 'numbered_list_item', 'to_do', 'code']:
        rich_text = block.get(block_type, {}).get('rich_text', [])
        return ''.join([text.get('plain_text', '') for text in rich_text])
    
    return ''

if __name__ == "__main__":
    mcp.run()