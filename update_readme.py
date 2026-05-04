import os
import re

# --- 配置 ---
# 排除不需要统计的文件夹
EXCLUDE_DIRS = {'.git', '.github', 'scripts', 'images', 'figures'}

def count_papers():
    folder_stats = {}
    total_papers = 0
    
    # 遍历当前目录
    for root, dirs, files in os.walk('.'):
        # 计算相对路径
        folder_name = os.path.relpath(root, '.')
        
        # 跳过根目录和排除列表中的目录
        if folder_name == '.' or any(ex in folder_name.split(os.sep) for ex in EXCLUDE_DIRS):
            continue
            
        # 统计以 .pdf 结尾的文件
        pdf_count = len([f for f in files if f.lower().endswith('.pdf')])
        
        if pdf_count > 0:
            folder_stats[folder_name] = pdf_count
            total_papers += pdf_count
            
    return folder_stats, total_papers

def update_readme(stats, total):
    if not os.path.exists("README.md"):
        print("❌ 未找到 README.md 文件")
        return

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # 构建 Markdown 表格
    table_content = "<!-- STATS_START -->\n"
    table_content += f"**📊 Total Papers: {total}**\n\n"
    table_content += "| Folder Name | Paper Count |\n"
    table_content += "| :--- | :---: |\n"
    
    # 按文件夹名称排序
    for folder in sorted(stats.keys()):
        table_content += f"| `{folder}` | {stats[folder]} |\n"
    
    table_content += "<!-- STATS_END -->"

    # 替换占位符之间的内容
    new_content = re.sub(
        r"<!-- STATS_START -->.*?<!-- STATS_END -->",
        table_content,
        content,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"✅ 统计完成！共发现 {total} 篇论文，README 已更新。")

if __name__ == "__main__":
    stats, total = count_papers()
    update_readme(stats, total)
