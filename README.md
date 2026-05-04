import os
import re
from collections import Counter

# 预定义的顶会关键词，用于模糊匹配
CONFERENCES = [
    "ICLR", "NeurIPS", "ACL", "EMNLP", "CVPR", "ICCV", 
    "AAAI", "IJCAI", "KDD", "UIST", "CoRL", "Arxiv"
]

def analyze_papers(repo_path):
    stats_per_folder = {}
    all_conferences = []
    
    # 遍历仓库文件夹（排除隐藏文件夹如 .git）
    for root, dirs, files in os.walk(repo_path):
        if '.git' in root:
            continue
            
        # 统计 PDF 或在 README 中记录的论文条目
        # 这里假设论文以 .pdf 结尾，或者你在文件夹里有对应的 md 描述
        paper_files = [f for f in files if f.endswith('.pdf') or f.endswith('.md') and f != "README.md"]
        
        folder_name = os.path.basename(root)
        if paper_files:
            stats_per_folder[folder_name] = len(paper_files)
            
        # 尝试从文件名或内容中提取会议信息
        for f in paper_files:
            found = False
            for conf in CONFERENCES:
                if conf.lower() in f.lower():
                    all_conferences.append(conf)
                    found = True
                    break
            if not found:
                all_conferences.append("Other/To-be-determined")

    return stats_per_folder, Counter(all_conferences)

def generate_readme_snippet(folder_stats, conf_stats):
    lines = ["## 📊 Paper Statistics\n"]
    
    # 1. 文件夹论文数量统计
    lines.append("### 📂 Folder Distribution")
    lines.append("| Folder | Count |")
    lines.append("| :--- | :--- |")
    for folder, count in folder_stats.items():
        lines.append(f"| {folder} | {count} |")
    
    lines.append("\n### 🏆 Conference Distribution")
    # 2. 会议分布统计
    lines.append("| Conference | Count |")
    lines.append("| :--- | :--- |")
    for conf, count in conf_stats.items():
        lines.append(f"| {conf} | {count} |")
        
    return "\n".join(lines)

# 使用示例
if __name__ == "__main__":
    # 替换为你本地克隆的仓库路径
    path = "." 
    f_stats, c_stats = analyze_papers(path)
    print(generate_readme_snippet(f_stats, c_stats))
