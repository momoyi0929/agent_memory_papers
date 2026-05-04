import os
import re

# --- 配置区 ---
# 排除不需要统计的文件夹（隐藏文件夹和非论文目录）
EXCLUDE_DIRS = {'.git', '.github', 'scripts', 'images', 'figures', 'node_modules'}

def count_pdf_papers():
    folder_stats = {}
    total_count = 0
    
    # 遍历当前目录下的所有子目录
    for root, dirs, files in os.walk('.'):
        # 获取相对路径作为文件夹名
        folder_path = os.path.relpath(root, '.')
        
        # 过滤掉不需要统计的目录
        if folder_path == '.' or any(part.startswith('.') or part in EXCLUDE_DIRS for part in folder_path.split(os.sep)):
            continue
            
        # 只统计扩展名为 .pdf 的文件
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]
        count = len(pdf_files)
        
        if count > 0:
            folder_stats[folder_path] = count
            total_count += count
            
    return folder_stats, total_count

def write_to_readme(stats, total):
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("Error: 找不到 README.md 文件")
        return

    # 构建 Markdown 表格内容
    table_lines = [
        "<!-- STATS_START -->",
        f"**🔥 仓库内共有论文: {total} 篇**\n",
        "| 文件夹 (Category) | 论文数量 (Count) |",
        "| :--- | :---: |"
    ]
    
    # 按文件夹名称字母顺序排序并添加行
    for folder in sorted(stats.keys()):
        table_lines.append(f"| `{folder}` | {stats[folder]} |")
    
    table_lines.append("<!-- STATS_END -->")
    new_stats_block = "\n".join(table_lines)

    # 读取并替换 README 内容
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 使用正则替换掉旧的统计块
    pattern = r"<!-- STATS_START -->.*?<!-- STATS_END -->"
    updated_content = re.sub(pattern, new_stats_block, content, flags=re.DOTALL)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    print("正在扫描论文并更新 README...")
    f_stats, total = count_pdf_papers()
    write_to_readme(f_stats, total)
    print(f"成功！共统计到 {total} 篇论文。")
