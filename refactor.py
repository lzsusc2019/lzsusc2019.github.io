import os
import re

backup_dir = '../blog_backup/_posts'
target_path = '_posts/2023-07-24-剑指offer全系列大归档.md'

# LeetCode links mapping
links = {
    "移动零": "https://leetcode.cn/problems/move-zeroes/",
    "删除有序数组中重复元素": "https://leetcode.cn/problems/remove-duplicates-from-sorted-array/",
    "替换空格": "https://leetcode.cn/problems/ti-huan-kong-ge-lcof/",
    "反转链表": "https://leetcode.cn/problems/reverse-linked-list/",
    "移除链表元素": "https://leetcode.cn/problems/remove-linked-list-elements/",
    "环形链表II": "https://leetcode.cn/problems/linked-list-cycle-ii/",
    "相交链表": "https://leetcode.cn/problems/intersection-of-two-linked-lists/",
    "链表的中间节点": "https://leetcode.cn/problems/middle-of-the-linked-list/",
    "有效的括号": "https://leetcode.cn/problems/valid-parentheses/",
    "逆波兰表达式的值": "https://leetcode.cn/problems/evaluate-reverse-polish-notation/",
    "存在重复元素": "https://leetcode.cn/problems/contains-duplicate/",
    "两数之和": "https://leetcode.cn/problems/two-sum/",
    "每日温度": "https://leetcode.cn/problems/daily-temperatures/",
    "合并两个有序数组": "https://leetcode.cn/problems/merge-sorted-array/",
    "二分查找": "https://leetcode.cn/problems/binary-search/",
    "只出现一次的数字 II": "https://leetcode.cn/problems/single-number-ii/",
    "只出现一次的数字 III": "https://leetcode.cn/problems/single-number-iii/",
    "柠檬水找零": "https://leetcode.cn/problems/lemonade-change/",
    "种花问题": "https://leetcode.cn/problems/can-place-flowers/",
    "单调递增的数字": "https://leetcode.cn/problems/monotone-increasing-digits/",
    "岛屿数量": "https://leetcode.cn/problems/number-of-islands/",
    "斐波那契数列": "https://leetcode.cn/problems/fibonacci-number/",
    "爬楼梯的最少成本": "https://leetcode.cn/problems/min-cost-climbing-stairs/",
    "爬楼梯": "https://leetcode.cn/problems/climbing-stairs/",
    "买卖股票的最佳时机II": "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/",
    "买卖股票的最佳时机III": "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/",
    "买卖股票的最佳时机IV": "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iv/",
    "买卖股票的最佳时机": "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/",
    "接雨水": "https://leetcode.cn/problems/trapping-rain-water/",
    "宝石与石头": "https://leetcode.cn/problems/jewels-and-stones/",
    "二叉树前序遍历": "https://leetcode.cn/problems/binary-tree-preorder-traversal/",
    "二叉树中序遍历": "https://leetcode.cn/problems/binary-tree-inorder-traversal/",
    "二叉树后序遍历": "https://leetcode.cn/problems/binary-tree-postorder-traversal/",
    "二叉树层序遍历": "https://leetcode.cn/problems/binary-tree-level-order-traversal/"
}

categories = {
    "数组与双指针": ["移动零", "删除有序数组中重复元素", "两数之和", "合并两个有序数组", "每日温度", "存在重复元素"],
    "链表专题": ["替换空格", "反转链表", "移除链表元素", "环形链表II", "相交链表", "链表的中间节点", "找倒数第k个元素", "找最中间的元素", "判断是否有环", "环入口查找"],
    "二叉树专题": ["二叉树前序遍历", "二叉树后序遍历", "二叉树中序遍历", "二叉树层序遍历"],
    "栈与队列": ["有效的括号", "逆波兰表达式的值"],
    "动态规划与贪心": ["爬楼梯", "买卖股票", "接雨水", "斐波那契数列", "柠檬水找零", "种花问题", "单调递增的数字"],
    "搜索与位运算": ["二分查找", "岛屿数量", "只出现一次的数字", "宝石与石头"],
    "其他综合": []
}

files = sorted([f for f in os.listdir(backup_dir) if '剑指offer' in f])

all_blocks = []

for filename in files:
    with open(os.path.join(backup_dir, filename), 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip front matter
    parts = content.split('---')
    if len(parts) >= 3:
        body = '---'.join(parts[2:]).strip()
    else:
        body = content.strip()
        
    # Split by ## 
    chunks = re.split(r'\n## ', '\n' + body)
    for chunk in chunks:
        if not chunk.strip(): continue
        if '剑指offer 第' in chunk.split('\n')[0]:
            # This is a day header, we skip it and look at its children if any, but split usually handles it.
            # Sometimes a day header has no content before the next ##. 
            continue
            
        all_blocks.append(chunk.strip())

# Process and categorize blocks
cat_content = {cat: [] for cat in categories.keys()}
seen = set()

def format_title(raw_title):
    # Clean up prefixes like "一、", "二、", "1.", "2."
    clean = re.sub(r'^(?:[一二三四五六七八九十]+、|\d+\.)\s*', '', raw_title).strip()
    
    # Extract LeetCode number if exists
    num_match = re.search(r'(?:LeetCode|Leetcode|剑指Offer|剑指 Offer II)\s*(\d+)', clean, re.IGNORECASE)
    or_match = re.search(r'（(\d+)）$', clean)
    
    num = ""
    if num_match:
        num = num_match.group(1)
    elif or_match:
        num = or_match.group(1)
        
    # Remove all parenthetical content for the pure title name
    pure_name = re.sub(r'（.*?）|\(.*?\)|\[.*?\]', '', clean).strip()
    
    # Check if there is an existing markdown link (like 宝石与石头)
    if ']' in raw_title and '(' in raw_title:
        # Just use the original markdown title without prefixes
        md_match = re.search(r'\[(.*?)\]\((.*?)\)', clean)
        if md_match:
            return f"### [{md_match.group(1)}]({md_match.group(2)})"
    
    # Find matching link
    url = ""
    for key in links:
        if key in pure_name:
            url = links[key]
            pure_name = key
            break
            
    prefix = ""
    if num:
        prefix = f"LeetCode {num} "
        
    if url:
        return f"### [{prefix}{pure_name}]({url})"
    else:
        return f"### {prefix}{pure_name}"

for block in all_blocks:
    lines = block.split('\n')
    raw_title = lines[0].strip()
    
    # skip empty or irrelevant blocks
    if not raw_title: continue
    
    formatted_title = format_title(raw_title)
    
    # Process the body of the block
    new_lines = [formatted_title]
    for line in lines[1:]:
        # Downgrade ### to ####
        if line.startswith('### '):
            new_lines.append(line.replace('### ', '#### '))
        else:
            new_lines.append(line)
            
    processed_block = '\n'.join(new_lines)
    
    # Categorize
    assigned = False
    for cat, kws in categories.items():
        if any(kw in raw_title for kw in kws):
            cat_content[cat].append(processed_block)
            assigned = True
            break
            
    if not assigned:
        cat_content["其他综合"].append(processed_block)


final_lines = [
    "---\n",
    "title: \"剑指offer：全系列题解大归档\"\n",
    "date: 2023-07-24 12:00:00 +0800\n",
    "categories: [Java, 算法]\n",
    "tags: [算法, 剑指offer]\n",
    "permalink: /posts/jianzhi-offer-all-in-one/\n",
    "layout: post\n",
    "---\n\n"
]

for cat, blocks in cat_content.items():
    if not blocks: continue
    final_lines.append(f"## {cat}\n\n")
    for b in blocks:
        final_lines.append(b + "\n\n---\n\n")

with open(target_path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("Refactoring completed successfully.")
