from django.db import migrations
from django.template.defaultfilters import slugify
import json
import re


ADDED_PROBLEM_SLUGS = [
    "happy-number",
    "majority-element",
    "valid-perfect-square",
    "monotonic-array",
    "min-cost-climbing-stairs",
    "reshape-the-matrix",
    "kth-missing-positive-number",
    "intersection-of-two-arrays-ii",
    "gas-station",
    "merge-intervals",
    "insert-interval",
    "non-overlapping-intervals",
    "find-k-closest-elements",
    "task-scheduler",
    "word-break",
    "decode-ways",
    "unique-binary-search-trees",
    "asteroid-collision",
    "remove-k-digits",
    "network-delay-time",
    "longest-increasing-subsequence",
    "maximum-product-subarray",
    "find-all-anagrams-in-a-string",
    "split-array-largest-sum",
    "n-queens-ii",
    "word-ladder",
    "minimum-genetic-mutation",
    "minimum-number-of-arrows-to-burst-balloons",
]


def _normalize_title(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "", value)
    return value


def _build_starter(signature_text):
    return (
        "class Solution:\n"
        f"    {signature_text}:\n"
        "        pass"
    )


def apply_cleanup_and_expand(apps, schema_editor):
    Problem = apps.get_model("problems", "Problem")
    TestCase = apps.get_model("problems", "TestCase")
    Tag = apps.get_model("problems", "Tag")

    def get_tag(name):
        tag, _ = Tag.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
        return tag

    # 1) Remove duplicate published questions by normalized title.
    published = list(Problem.objects.filter(is_published=True).order_by("id"))
    grouped = {}
    for problem in published:
        grouped.setdefault(_normalize_title(problem.title), []).append(problem)

    for _, group in grouped.items():
        if len(group) < 2:
            continue

        ranked = []
        for problem in group:
            tc_count = TestCase.objects.filter(problem_id=problem.id).count()
            tag_count = problem.tags.count()
            ranked.append((problem, tc_count, tag_count))

        ranked.sort(key=lambda item: (-item[1], -item[2], item[0].id))
        keep = ranked[0][0]

        for candidate, _, _ in ranked[1:]:
            if candidate.id != keep.id:
                candidate.delete()

    candidates = [
        {
            "title": "Happy Number",
            "slug": "happy-number",
            "description": "Determine if n is a happy number.",
            "constraints": "1 <= n <= 2^31 - 1",
            "difficulty": 1,
            "entrypoint_name": "isHappy",
            "signature_text": "def isHappy(self, n: int) -> bool",
            "tags": ["Math", "Hashing"],
            "cases": [({"n": 19}, True), ({"n": 2}, False)],
        },
        {
            "title": "Majority Element",
            "slug": "majority-element",
            "description": "Return the element that appears more than n/2 times.",
            "constraints": "1 <= nums.length <= 5 * 10^4",
            "difficulty": 1,
            "entrypoint_name": "majorityElement",
            "signature_text": "def majorityElement(self, nums: list[int]) -> int",
            "tags": ["Arrays", "Greedy"],
            "cases": [({"nums": [3, 2, 3]}, 3), ({"nums": [2, 2, 1, 1, 1, 2, 2]}, 2)],
        },
        {
            "title": "Valid Perfect Square",
            "slug": "valid-perfect-square",
            "description": "Return true if num is a perfect square.",
            "constraints": "1 <= num <= 2^31 - 1",
            "difficulty": 1,
            "entrypoint_name": "isPerfectSquare",
            "signature_text": "def isPerfectSquare(self, num: int) -> bool",
            "tags": ["Math", "Binary Search"],
            "cases": [({"num": 16}, True), ({"num": 14}, False)],
        },
        {
            "title": "Monotonic Array",
            "slug": "monotonic-array",
            "description": "Return true if array is monotone increasing or decreasing.",
            "constraints": "1 <= nums.length <= 10^5",
            "difficulty": 1,
            "entrypoint_name": "isMonotonic",
            "signature_text": "def isMonotonic(self, nums: list[int]) -> bool",
            "tags": ["Arrays"],
            "cases": [({"nums": [1, 2, 2, 3]}, True), ({"nums": [1, 3, 2]}, False)],
        },
        {
            "title": "Min Cost Climbing Stairs",
            "slug": "min-cost-climbing-stairs",
            "description": "Return minimum cost to reach the top.",
            "constraints": "2 <= cost.length <= 1000",
            "difficulty": 1,
            "entrypoint_name": "minCostClimbingStairs",
            "signature_text": "def minCostClimbingStairs(self, cost: list[int]) -> int",
            "tags": ["Dynamic Programming"],
            "cases": [({"cost": [10, 15, 20]}, 15), ({"cost": [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]}, 6)],
        },
        {
            "title": "Reshape the Matrix",
            "slug": "reshape-the-matrix",
            "description": "Reshape matrix to r x c if possible, else return original.",
            "constraints": "1 <= m, n <= 100",
            "difficulty": 1,
            "entrypoint_name": "matrixReshape",
            "signature_text": "def matrixReshape(self, mat: list[list[int]], r: int, c: int) -> list[list[int]]",
            "tags": ["Matrix", "Arrays"],
            "cases": [({"mat": [[1, 2], [3, 4]], "r": 1, "c": 4}, [[1, 2, 3, 4]]), ({"mat": [[1, 2], [3, 4]], "r": 2, "c": 4}, [[1, 2], [3, 4]])],
        },
        {
            "title": "Kth Missing Positive Number",
            "slug": "kth-missing-positive-number",
            "description": "Return the k-th missing positive integer.",
            "constraints": "1 <= arr.length <= 1000",
            "difficulty": 1,
            "entrypoint_name": "findKthPositive",
            "signature_text": "def findKthPositive(self, arr: list[int], k: int) -> int",
            "tags": ["Arrays", "Binary Search"],
            "cases": [({"arr": [2, 3, 4, 7, 11], "k": 5}, 9), ({"arr": [1, 2, 3, 4], "k": 2}, 6)],
        },
        {
            "title": "Intersection of Two Arrays II",
            "slug": "intersection-of-two-arrays-ii",
            "description": "Return intersection with multiplicity in sorted order.",
            "constraints": "1 <= nums1.length, nums2.length <= 1000",
            "difficulty": 1,
            "entrypoint_name": "intersect",
            "signature_text": "def intersect(self, nums1: list[int], nums2: list[int]) -> list[int]",
            "tags": ["Arrays", "Hashing"],
            "cases": [({"nums1": [1, 2, 2, 1], "nums2": [2, 2]}, [2, 2]), ({"nums1": [4, 9, 5], "nums2": [9, 4, 9, 8, 4]}, [4, 9])],
        },
        {
            "title": "Gas Station",
            "slug": "gas-station",
            "description": "Return starting station index to complete circuit, else -1.",
            "constraints": "1 <= gas.length == cost.length <= 10^5",
            "difficulty": 2,
            "entrypoint_name": "canCompleteCircuit",
            "signature_text": "def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int",
            "tags": ["Arrays", "Greedy"],
            "cases": [({"gas": [1, 2, 3, 4, 5], "cost": [3, 4, 5, 1, 2]}, 3), ({"gas": [2, 3, 4], "cost": [3, 4, 3]}, -1)],
        },
        {
            "title": "Merge Intervals",
            "slug": "merge-intervals",
            "description": "Merge all overlapping intervals.",
            "constraints": "1 <= intervals.length <= 10^4",
            "difficulty": 2,
            "entrypoint_name": "merge",
            "signature_text": "def merge(self, intervals: list[list[int]]) -> list[list[int]]",
            "tags": ["Intervals", "Sorting"],
            "cases": [({"intervals": [[1, 3], [2, 6], [8, 10], [15, 18]]}, [[1, 6], [8, 10], [15, 18]]), ({"intervals": [[1, 4], [4, 5]]}, [[1, 5]])],
        },
        {
            "title": "Insert Interval",
            "slug": "insert-interval",
            "description": "Insert a new interval and merge if necessary.",
            "constraints": "0 <= intervals.length <= 10^4",
            "difficulty": 2,
            "entrypoint_name": "insert",
            "signature_text": "def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]",
            "tags": ["Intervals", "Arrays"],
            "cases": [({"intervals": [[1, 3], [6, 9]], "newInterval": [2, 5]}, [[1, 5], [6, 9]]), ({"intervals": [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], "newInterval": [4, 8]}, [[1, 2], [3, 10], [12, 16]])],
        },
        {
            "title": "Non-overlapping Intervals",
            "slug": "non-overlapping-intervals",
            "description": "Return minimum intervals to remove to eliminate overlaps.",
            "constraints": "1 <= intervals.length <= 10^5",
            "difficulty": 2,
            "entrypoint_name": "eraseOverlapIntervals",
            "signature_text": "def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int",
            "tags": ["Intervals", "Greedy"],
            "cases": [({"intervals": [[1, 2], [2, 3], [3, 4], [1, 3]]}, 1), ({"intervals": [[1, 2], [1, 2], [1, 2]]}, 2)],
        },
        {
            "title": "Find K Closest Elements",
            "slug": "find-k-closest-elements",
            "description": "Return k closest elements to x in ascending order.",
            "constraints": "1 <= k <= arr.length <= 10^4",
            "difficulty": 2,
            "entrypoint_name": "findClosestElements",
            "signature_text": "def findClosestElements(self, arr: list[int], k: int, x: int) -> list[int]",
            "tags": ["Arrays", "Binary Search", "Two Pointers"],
            "cases": [({"arr": [1, 2, 3, 4, 5], "k": 4, "x": 3}, [1, 2, 3, 4]), ({"arr": [1, 2, 3, 4, 5], "k": 4, "x": -1}, [1, 2, 3, 4])],
        },
        {
            "title": "Task Scheduler",
            "slug": "task-scheduler",
            "description": "Return least intervals needed to execute tasks with cooldown n.",
            "constraints": "1 <= tasks.length <= 10^4",
            "difficulty": 2,
            "entrypoint_name": "leastInterval",
            "signature_text": "def leastInterval(self, tasks: list[str], n: int) -> int",
            "tags": ["Greedy", "Heap"],
            "cases": [({"tasks": ["A", "A", "A", "B", "B", "B"], "n": 2}, 8), ({"tasks": ["A", "A", "A", "B", "B", "B"], "n": 0}, 6)],
        },
        {
            "title": "Word Break",
            "slug": "word-break",
            "description": "Return true if s can be segmented into dictionary words.",
            "constraints": "1 <= s.length <= 300",
            "difficulty": 2,
            "entrypoint_name": "wordBreak",
            "signature_text": "def wordBreak(self, s: str, wordDict: list[str]) -> bool",
            "tags": ["Dynamic Programming", "Strings"],
            "cases": [({"s": "leetcode", "wordDict": ["leet", "code"]}, True), ({"s": "catsandog", "wordDict": ["cats", "dog", "sand", "and", "cat"]}, False)],
        },
        {
            "title": "Decode Ways",
            "slug": "decode-ways",
            "description": "Return number of ways to decode the string.",
            "constraints": "1 <= s.length <= 100",
            "difficulty": 2,
            "entrypoint_name": "numDecodings",
            "signature_text": "def numDecodings(self, s: str) -> int",
            "tags": ["Dynamic Programming", "Strings"],
            "cases": [({"s": "12"}, 2), ({"s": "226"}, 3)],
        },
        {
            "title": "Unique Binary Search Trees",
            "slug": "unique-binary-search-trees",
            "description": "Return number of structurally unique BSTs that store values 1..n.",
            "constraints": "1 <= n <= 19",
            "difficulty": 2,
            "entrypoint_name": "numTrees",
            "signature_text": "def numTrees(self, n: int) -> int",
            "tags": ["Dynamic Programming", "Math"],
            "cases": [({"n": 3}, 5), ({"n": 1}, 1)],
        },
        {
            "title": "Asteroid Collision",
            "slug": "asteroid-collision",
            "description": "Simulate asteroid collisions and return final state.",
            "constraints": "2 <= asteroids.length <= 10^4",
            "difficulty": 2,
            "entrypoint_name": "asteroidCollision",
            "signature_text": "def asteroidCollision(self, asteroids: list[int]) -> list[int]",
            "tags": ["Stack", "Simulation"],
            "cases": [({"asteroids": [5, 10, -5]}, [5, 10]), ({"asteroids": [8, -8]}, [])],
        },
        {
            "title": "Remove K Digits",
            "slug": "remove-k-digits",
            "description": "Remove k digits to make the smallest possible number string.",
            "constraints": "1 <= num.length <= 10^5",
            "difficulty": 2,
            "entrypoint_name": "removeKdigits",
            "signature_text": "def removeKdigits(self, num: str, k: int) -> str",
            "tags": ["Stack", "Greedy"],
            "cases": [({"num": "1432219", "k": 3}, "1219"), ({"num": "10200", "k": 1}, "200")],
        },
        {
            "title": "Network Delay Time",
            "slug": "network-delay-time",
            "description": "Return time for all nodes to receive signal, else -1.",
            "constraints": "1 <= n <= 100",
            "difficulty": 2,
            "entrypoint_name": "networkDelayTime",
            "signature_text": "def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int",
            "tags": ["Graphs", "Shortest Path", "Heap"],
            "cases": [({"times": [[2, 1, 1], [2, 3, 1], [3, 4, 1]], "n": 4, "k": 2}, 2), ({"times": [[1, 2, 1]], "n": 2, "k": 2}, -1)],
        },
        {
            "title": "Longest Increasing Subsequence",
            "slug": "longest-increasing-subsequence",
            "description": "Return length of the longest strictly increasing subsequence.",
            "constraints": "1 <= nums.length <= 2500",
            "difficulty": 2,
            "entrypoint_name": "lengthOfLIS",
            "signature_text": "def lengthOfLIS(self, nums: list[int]) -> int",
            "tags": ["Dynamic Programming", "Binary Search"],
            "cases": [({"nums": [10, 9, 2, 5, 3, 7, 101, 18]}, 4), ({"nums": [0, 1, 0, 3, 2, 3]}, 4)],
        },
        {
            "title": "Maximum Product Subarray",
            "slug": "maximum-product-subarray",
            "description": "Return maximum product of a contiguous subarray.",
            "constraints": "1 <= nums.length <= 2 * 10^4",
            "difficulty": 2,
            "entrypoint_name": "maxProduct",
            "signature_text": "def maxProduct(self, nums: list[int]) -> int",
            "tags": ["Dynamic Programming", "Arrays"],
            "cases": [({"nums": [2, 3, -2, 4]}, 6), ({"nums": [-2, 0, -1]}, 0)],
        },
        {
            "title": "Find All Anagrams in a String",
            "slug": "find-all-anagrams-in-a-string",
            "description": "Return start indices of p's anagrams in s.",
            "constraints": "1 <= s.length, p.length <= 3 * 10^4",
            "difficulty": 2,
            "entrypoint_name": "findAnagrams",
            "signature_text": "def findAnagrams(self, s: str, p: str) -> list[int]",
            "tags": ["Strings", "Sliding Window"],
            "cases": [({"s": "cbaebabacd", "p": "abc"}, [0, 6]), ({"s": "abab", "p": "ab"}, [0, 1, 2])],
        },
        {
            "title": "Split Array Largest Sum",
            "slug": "split-array-largest-sum",
            "description": "Split array into k non-empty subarrays minimizing the largest subarray sum.",
            "constraints": "1 <= nums.length <= 1000",
            "difficulty": 3,
            "entrypoint_name": "splitArray",
            "signature_text": "def splitArray(self, nums: list[int], k: int) -> int",
            "tags": ["Binary Search", "Dynamic Programming"],
            "cases": [({"nums": [7, 2, 5, 10, 8], "k": 2}, 18), ({"nums": [1, 2, 3, 4, 5], "k": 2}, 9)],
        },
        {
            "title": "N-Queens II",
            "slug": "n-queens-ii",
            "description": "Return the number of distinct solutions to the n-queens puzzle.",
            "constraints": "1 <= n <= 9",
            "difficulty": 3,
            "entrypoint_name": "totalNQueens",
            "signature_text": "def totalNQueens(self, n: int) -> int",
            "tags": ["Backtracking"],
            "cases": [({"n": 4}, 2), ({"n": 1}, 1)],
        },
        {
            "title": "Word Ladder",
            "slug": "word-ladder",
            "description": "Return shortest transformation sequence length from beginWord to endWord.",
            "constraints": "1 <= wordList.length <= 5000",
            "difficulty": 3,
            "entrypoint_name": "ladderLength",
            "signature_text": "def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int",
            "tags": ["Graphs", "BFS"],
            "cases": [({"beginWord": "hit", "endWord": "cog", "wordList": ["hot", "dot", "dog", "lot", "log", "cog"]}, 5), ({"beginWord": "hit", "endWord": "cog", "wordList": ["hot", "dot", "dog", "lot", "log"]}, 0)],
        },
        {
            "title": "Minimum Genetic Mutation",
            "slug": "minimum-genetic-mutation",
            "description": "Return minimum mutations from startGene to endGene, else -1.",
            "constraints": "Each gene has length 8",
            "difficulty": 3,
            "entrypoint_name": "minMutation",
            "signature_text": "def minMutation(self, startGene: str, endGene: str, bank: list[str]) -> int",
            "tags": ["Graphs", "BFS"],
            "cases": [({"startGene": "AACCGGTT", "endGene": "AACCGGTA", "bank": ["AACCGGTA"]}, 1), ({"startGene": "AACCGGTT", "endGene": "AAACGGTA", "bank": ["AACCGGTA", "AACCGCTA", "AAACGGTA"]}, 2)],
        },
        {
            "title": "Minimum Number of Arrows to Burst Balloons",
            "slug": "minimum-number-of-arrows-to-burst-balloons",
            "description": "Return the minimum arrows required to burst all balloons.",
            "constraints": "1 <= points.length <= 10^5",
            "difficulty": 3,
            "entrypoint_name": "findMinArrowShots",
            "signature_text": "def findMinArrowShots(self, points: list[list[int]]) -> int",
            "tags": ["Intervals", "Greedy"],
            "cases": [({"points": [[10, 16], [2, 8], [1, 6], [7, 12]]}, 2), ({"points": [[1, 2], [3, 4], [5, 6], [7, 8]]}, 4)],
        },
    ]

    # 2) Add new unique questions until we hit exactly 100 published problems.
    for pdata in candidates:
        current_count = Problem.objects.filter(is_published=True).count()
        if current_count >= 100:
            break

        if Problem.objects.filter(slug=pdata["slug"]).exists():
            continue

        problem = Problem.objects.create(
            title=pdata["title"],
            slug=pdata["slug"],
            description=pdata["description"],
            constraints=pdata.get("constraints", ""),
            follow_up=pdata.get("follow_up", ""),
            difficulty=pdata["difficulty"],
            judge_mode="function",
            entrypoint_type="class",
            entrypoint_name=pdata["entrypoint_name"],
            signature_text=pdata["signature_text"],
            starter_code=_build_starter(pdata["signature_text"]),
            is_published=True,
        )

        for tag_name in pdata.get("tags", []):
            problem.tags.add(get_tag(tag_name))

        for index, (args, expected) in enumerate(pdata.get("cases", [])):
            input_json = json.dumps(args)
            output_json = json.dumps(expected)
            TestCase.objects.create(
                problem=problem,
                input_data=input_json,
                expected_output=output_json,
                display_input=input_json,
                display_output=output_json,
                is_sample=index == 0,
            )


def reverse_cleanup_and_expand(apps, schema_editor):
    Problem = apps.get_model("problems", "Problem")
    Problem.objects.filter(slug__in=ADDED_PROBLEM_SLUGS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0015_add_fifty_one_problems"),
    ]

    operations = [
        migrations.RunPython(apply_cleanup_and_expand, reverse_cleanup_and_expand),
    ]
