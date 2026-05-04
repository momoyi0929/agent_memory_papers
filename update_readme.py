import os
import re
from collections import Counter

# --- 配置区 ---
# 匹配文件名中的会议关键字（不区分大小写）
CONFS = ["ICLR", "NeurIPS", "ACL", "EMNLP", "CVPR", "ICCV", "AAAI", "IJCAI", "SIGGRAPH", "UIST", "CoRL", "Arxiv"]
# 需要统计的文件夹列表（排除隐藏目录）
EXCLUDE_DIRS = {'.git', '.github', 'scripts', 'images'}

def get_paper_info():
    folder_stats = {}
    conf_list = []
    
    # 遍历当前目录下所有文件夹
    for root, dirs, files in os.walk('.'):
        folder_name = os.path.relpath(root, '.')
        if folder_name == '.' or any(ex in folder_name for ex in EXCLUDE_DIRS):
            continue
            
        # 统计 pdf 数量（你也可以改成统计 .md）
        papers = [f for f in files if f.lower().endswith('.pdf')]
        if papers:
            folder_stats[folder_name] = len(papers)
            for p in papers:
                # 匹配文件名中的会议信息
                found = False
                for c in CONFS:
                    if c.lower() in p.lower():
                        conf_list.append(c)
                        found = True
                        break
                if not found:
                    conf_list.append("Others/Preprint")
                    
    return folder_stats, Counter(conf_list)

def update_readme(folder_stats, conf_stats):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # 构建统计表格
    stats_text = "<!-- STATS_START -->\n\n"
    
    # 文件夹统计表格
    stats_text += "### 📂 Folder Statistics\n| Folder | Papers Count |\n| :--- | :---: |\n"
    for folder, count in sorted(folder_stats.items()):
        stats_text += f"| `{folder}` | {count} |\n"
    
    # 会议统计表格
    stats_text += "\n### 🏆 Conference Distribution\n| Venue | Count |\n| :--- | :---: |\n"
    for conf, count in conf_stats.most_common():
        stats_text += f"| **{conf}** | {count} |\n"
    
    stats_text += "\n<!-- STATS_END -->"

    # 使用正则替换 README 中的旧统计块
    new_content = re.sub(
        r"<!-- STATS_START -->.*?<!-- STATS_END -->",
        stats_text,
        content,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ README statistics updated successfully!")

if __name__ == "__main__":
    f_stats, c_stats = get_paper_info()
    update_readme(f_stats, c_stats)