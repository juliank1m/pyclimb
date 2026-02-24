from django.db import migrations


COURSE_SLUG = "problem-solving-patterns"
LESSON_SLUGS = [
    "sliding-window-pattern",
    "monotonic-stack-pattern",
    "binary-search-patterns",
    "graph-traversal-patterns",
    "dynamic-programming-foundations",
    "backtracking-patterns",
    "greedy-patterns",
    "interval-and-sweep-line-patterns",
]


def add_problem_solving_pattern_lessons(apps, schema_editor):
    Course = apps.get_model("lessons", "Course")
    Lesson = apps.get_model("lessons", "Lesson")
    Problem = apps.get_model("problems", "Problem")

    course = Course.objects.filter(slug=COURSE_SLUG).first()
    if not course:
        return

    lessons_data = [
        {
            "title": "Sliding Window Pattern",
            "slug": "sliding-window-pattern",
            "summary": "Use moving windows to optimize subarray and substring scans.",
            "order": 2,
            "content_markdown": """# Sliding Window Pattern

Sliding window is useful when you need to evaluate contiguous ranges efficiently.

## When to use
- "longest/shortest subarray or substring"
- constraints that suggest O(n) over O(n^2)

## Fixed window template
```python
def fixed_window(nums, k):
    window_sum = 0
    best = float('-inf')
    for i, x in enumerate(nums):
        window_sum += x
        if i >= k:
            window_sum -= nums[i - k]
        if i >= k - 1:
            best = max(best, window_sum)
    return best
```

## Variable window template
```python
def variable_window(s):
    left = 0
    seen = set()
    best = 0
    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best
```

## Practice
- Longest Substring Without Repeating Characters
- Minimum Window Substring
- Sliding Window Maximum
""",
            "problem_slugs": [
                "longest-substring-without-repeating-characters",
                "minimum-window-substring",
                "sliding-window-maximum",
            ],
        },
        {
            "title": "Monotonic Stack Pattern",
            "slug": "monotonic-stack-pattern",
            "summary": "Track next greater/smaller information in linear time.",
            "order": 3,
            "content_markdown": """# Monotonic Stack Pattern

A monotonic stack keeps values ordered while scanning once.

## Typical signals
- next greater/smaller element
- nearest boundary to left/right
- histogram-style area problems

## Template
```python
def next_greater(nums):
    stack = []
    ans = [-1] * len(nums)
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            idx = stack.pop()
            ans[idx] = x
        stack.append(i)
    return ans
```

## Practice
- Daily Temperatures
- Largest Rectangle in Histogram
""",
            "problem_slugs": ["daily-temperatures", "largest-rectangle-in-histogram"],
        },
        {
            "title": "Binary Search Patterns",
            "slug": "binary-search-patterns",
            "summary": "Find exact values, boundaries, and answers on sorted spaces.",
            "order": 4,
            "content_markdown": """# Binary Search Patterns

Binary search is not just for exact lookup. It also solves boundary and "answer search" problems.

## Core invariant
Maintain a search interval where the answer still exists.

## Common variants
- exact target search
- first/last true in a predicate space
- minimum feasible value

## Practice
- Binary Search
- Search in Rotated Sorted Array
- Find Minimum in Rotated Sorted Array
- Median of Two Sorted Arrays
""",
            "problem_slugs": [
                "binary-search",
                "search-in-rotated-sorted-array",
                "find-minimum-in-rotated-sorted-array",
                "median-of-two-sorted-arrays",
            ],
        },
        {
            "title": "Graph Traversal Patterns",
            "slug": "graph-traversal-patterns",
            "summary": "Model reachability with DFS, BFS, and topological sorting.",
            "order": 5,
            "content_markdown": """# Graph Traversal Patterns

Many interview problems become straightforward once you model them as graphs.

## Tools
- DFS for connected components and deep exploration
- BFS for shortest path in unweighted graphs
- Topological sort for dependency ordering

## Practice
- Number of Islands
- Course Schedule
""",
            "problem_slugs": ["number-of-islands", "course-schedule"],
        },
        {
            "title": "Dynamic Programming Foundations",
            "slug": "dynamic-programming-foundations",
            "summary": "Define state, transitions, and base cases before coding.",
            "order": 6,
            "content_markdown": """# Dynamic Programming Foundations

DP works when a problem has overlapping subproblems and optimal substructure.

## Checklist
1. Define state clearly
2. Write transition relation
3. Set base cases
4. Choose top-down or bottom-up

## Practice
- Climbing Stairs
- Coin Change
- Minimum Path Sum
- Edit Distance
- Distinct Subsequences
""",
            "problem_slugs": [
                "climbing-stairs",
                "coin-change",
                "minimum-path-sum",
                "edit-distance",
                "distinct-subsequences",
            ],
        },
        {
            "title": "Backtracking Patterns",
            "slug": "backtracking-patterns",
            "summary": "Explore decision trees with pruning and state rollback.",
            "order": 7,
            "content_markdown": """# Backtracking Patterns

Backtracking is depth-first search over choices.

## Template
```python
def backtrack(path, choices):
    if done(path):
        collect(path)
        return
    for choice in choices:
        if not valid(choice, path):
            continue
        path.append(choice)
        backtrack(path, next_choices(choice))
        path.pop()
```

## Practice
- Target Sum Ways
- Partition Labels (greedy alternative to explore boundaries)
""",
            "problem_slugs": ["target-sum-ways", "partition-labels"],
        },
        {
            "title": "Greedy Patterns",
            "slug": "greedy-patterns",
            "summary": "Use locally optimal decisions when global correctness can be proven.",
            "order": 8,
            "content_markdown": """# Greedy Patterns

A greedy algorithm makes the best local move at each step.

## Key requirement
You must justify why local best leads to global best.

## Practice
- Jump Game
- Partition Labels
- Best Time to Buy and Sell Stock
""",
            "problem_slugs": ["jump-game", "partition-labels", "best-time-to-buy-and-sell-stock"],
        },
        {
            "title": "Interval and Sweep Line Patterns",
            "slug": "interval-and-sweep-line-patterns",
            "summary": "Sort endpoints and process events in order.",
            "order": 9,
            "content_markdown": """# Interval and Sweep Line Patterns

Interval problems often become simpler after sorting by start/end.

## Typical moves
- sort intervals by one endpoint
- merge while overlaps exist
- or sweep all boundary events

## Practice direction
Use this pattern mindset on matrix and range problems where order matters.
Start with:
- Spiral Matrix
- Set Matrix Zeroes
""",
            "problem_slugs": ["spiral-matrix", "set-matrix-zeroes"],
        },
    ]

    for lesson_data in lessons_data:
        lesson, _ = Lesson.objects.get_or_create(
            slug=lesson_data["slug"],
            defaults={
                "course": course,
                "title": lesson_data["title"],
                "summary": lesson_data["summary"],
                "content_markdown": lesson_data["content_markdown"],
                "order": lesson_data["order"],
                "is_published": True,
            },
        )

        if lesson.course_id != course.id:
            lesson.course = course
            lesson.save(update_fields=["course"])

        for problem_slug in lesson_data["problem_slugs"]:
            problem = Problem.objects.filter(slug=problem_slug, is_published=True).first()
            if problem:
                lesson.problems.add(problem)


def remove_problem_solving_pattern_lessons(apps, schema_editor):
    Lesson = apps.get_model("lessons", "Lesson")
    Lesson.objects.filter(slug__in=LESSON_SLUGS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0003_add_more_seed_lessons"),
        ("problems", "0015_add_fifty_one_problems"),
    ]

    operations = [
        migrations.RunPython(
            add_problem_solving_pattern_lessons,
            remove_problem_solving_pattern_lessons,
        ),
    ]
