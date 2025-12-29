"""
测试 append_image 功能
"""

from main import append_image

# 测试用例配置
TEST_PAGE_ID = "26f50b4fa060801ba409c911f194e9aa"  # 替换为你的测试页面 ID
TEST_IMAGE_URL = "https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=800"  # 公开图片 URL

print("=" * 80)
print("🧪 测试 append_image 功能")
print("=" * 80)

# 测试 1: 添加图片（无说明）
print("\n【测试 1】添加图片（无说明）")
result = append_image(
    page_id=TEST_PAGE_ID,
    image_url=TEST_IMAGE_URL
)
print(result)

# 测试 2: 添加图片（带说明）
print("\n【测试 2】添加图片（带说明）")
result = append_image(
    page_id=TEST_PAGE_ID,
    #image_url="https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800",
    image_url="https://images.unsplash.com/photo-1497633762265-9d179a990aa6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
    caption="美丽的风景照片 - 来自 Unsplash"
)
print(result)

print("\n" + "=" * 80)
print("✅ 测试完成！")
print("💡 前往 Notion 页面查看效果")
print("=" * 80)
