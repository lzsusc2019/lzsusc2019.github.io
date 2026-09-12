---
title: "算法核心之双指针：从 O(N^2) 到 O(N) 的时空跳跃"
date: 2026-05-11 16:00:00 +0800
categories: [算法]
tags: [双指针, 算法, 复杂度优化]
permalink: /posts/mastering-two-pointers/
layout: post
---

{: .prompt-info }
**Quick Recall**：双指针（Two Pointers）不是一种具体的算法，而是一种**空间换时间**或**利用有序性减少重复计算**的编程技巧。核心口诀：**左右夹击找目标，快慢追及破循环，滑动窗口控区间**。

---

## 一、 核心思想：为什么要用双指针？

在处理线性结构（数组、链表、字符串）时，最直观的解法往往是**嵌套循环**（暴力解 $O(N^2)$）。

**双指针的核心思想**是：利用数据本身的**有序性**、**逻辑关联**或**拓扑结构**，通过两个方向（或速度）不同的指针，在一次遍历内（$O(N)$）完成任务。它本质上是利用了单调性，过滤掉了那些“绝对不可能成为答案”的状态空间。

### 为什么适用？
- **减少冗余计算**：例如在排序数组中找两数之和，当 `left + right > target` 时，由于数组有序，`right` 指向的值已经太大了，没必要再用更小的 `left` 去试它，直接 `right--`。
- **状态压缩**：将二维的扫描压缩成一维的移动。

---

## 二、 三大经典范式与适用场景

### 1. 左右指针（Opposite Direction）
指针从两端向中间移动。

- **适用场景**：已排序数组、字符串反转、二分查找、回文判断。
- **典型题目**：
  - **[LeetCode 167 两数之和 II]**：有序数组找目标值。
  - **[LeetCode 15 三数之和]**：排序后固定一个数，左右指针找另外两个。
  - **[LeetCode 11 盛最多水的容器]**：贪心移动较短的那一侧。

### 2. 快慢指针（Same Direction / Fast-Slow）
两个指针同向移动，但速度或起点逻辑不同。

- **适用场景**：链表环检测、找中点、原地修改数组（去重/移动元素）。
- **典型题目**：
  - **[LeetCode 141 环形链表]**：步长 1 vs 步长 2，若有环必相遇。
  - **[LeetCode 26 删除去重]**：慢指针记录“新数组”位置，快指针扫描。
  - **[LeetCode 283 移动零]**：快指针找非零值，慢指针记录待覆盖位置。

### 3. 滑动窗口（Sliding Window）
快指针（右边界）负责扩张窗口，慢指针（左边界）负责收缩窗口以满足约束条件。

- **适用场景**：子串、子数组、连续区间问题。
- **典型题目**：
  - **[LeetCode 3 无重复字符的最长子串]**。
  - **[LeetCode 76 最小覆盖子串]**。

---

## 三、 代码示例与深度解析

### 示例 1：原地数组修改（快慢指针）
// 场景：在不创建新数组的前提下，删除有序数组重复项
```java
// filepath: LeetCode 26
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;
    int slow = 0; // 慢指针：维护[0...slow]是唯一元素
    for (int fast = 1; fast < nums.length; fast++) {
        // 当发现新元素时，移动慢指针并赋值
        if (nums[fast] != nums[slow]) {
            slow++;
            nums[slow] = nums[fast]; // 核心：原地覆盖
        }
    }
    return slow + 1;
}
```

### 示例 2：环形链表检测（快慢追及）
// 场景：判断链表是否有环
```java
// filepath: LeetCode 141
public boolean hasCycle(ListNode head) {
    ListNode slow = head;
    ListNode fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;        // 走一步
        fast = fast.next.next;   // 走两步
        if (slow == fast) {      // 逻辑核心：速度差导致在环内必相遇
            return true;
        }
    }
    return false;
}
```

---

## 四、 总结：避坑指南

1.  **边界检查**：快慢指针中最容易出现 `fast.next.next` 的空指针异常，务必检查 `fast != null && fast.next != null`。
2.  **死循环**：在左右指针中，确保有 `left++` 或 `right--` 的出口逻辑。
3.  **索引陷阱**：返回的是“长度”还是“最大索引”？注意 `slow` 和 `slow + 1` 的区别。

---
{: .prompt-tip }
**思考题**：如果你在一个**未排序**的数组中找两数之和，还能直接用双指针吗？（答案：不能，除非先 $O(N \log N)$ 排序，否则只能用哈希表 $O(N)$ 空间换时间）。
