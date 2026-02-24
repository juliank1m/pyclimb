from django.db import migrations


COURSE_SLUG = "algorithm-practice-track"
LESSON_SLUGS = [
    "hash-maps-for-lookups",
    "binary-search-template",
    "prefix-and-suffix-products",
    "palindrome-two-pointer-technique",
]


def add_more_seed_lessons(apps, schema_editor):
    Course = apps.get_model("lessons", "Course")
    Lesson = apps.get_model("lessons", "Lesson")
    Problem = apps.get_model("problems", "Problem")

    course, _ = Course.objects.get_or_create(
        slug=COURSE_SLUG,
        defaults={
            "title": "Algorithm Practice Track",
            "description": (
                "A practical track focused on interview-style algorithm patterns with "
                "direct problem practice."
            ),
            "is_published": True,
            "order": 4,
        },
    )

    lessons_data = [
        {
            "title": "Hash Maps for Constant-Time Lookups",
            "slug": "hash-maps-for-lookups",
            "summary": "Use dictionaries to reduce nested-loop solutions to linear time.",
            "order": 1,
            "content_markdown": """# Hash Maps for Constant-Time Lookups

Hash maps (Python dictionaries) are a core tool for making solutions fast.

## Why they matter

- You can check whether a value exists in average **O(1)** time
- You can map a value to its index, count, or metadata
- They often remove one full loop from brute-force solutions

## Pattern

1. Iterate once through the list
2. Store useful state in a dict
3. Query the dict while iterating

```python
def two_sum(nums, target):
    seen = {}
    for i, value in enumerate(nums):
        needed = target - value
        if needed in seen:
            return [seen[needed], i]
        seen[value] = i
```

## Common mistakes

- Updating the dict before checking for the complement
- Forgetting duplicate values can appear
- Using dict keys that are not hashable

## Practice

Work on:
- Two Sum
- Valid Anagram
- Contains Duplicate
""",
            "problem_slugs": ["two-sum", "valid-anagram", "contains-duplicate"],
        },
        {
            "title": "Binary Search Template",
            "slug": "binary-search-template",
            "summary": "A reliable loop template for sorted arrays.",
            "order": 2,
            "content_markdown": """# Binary Search Template

When data is sorted, binary search reduces lookup time from **O(n)** to **O(log n)**.

## Core loop

```python
def search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

## Invariants to remember

- Search space is always `left..right`
- If `nums[mid] < target`, eliminate left half including `mid`
- If `nums[mid] > target`, eliminate right half including `mid`

## Edge cases

- Empty arrays
- One-element arrays
- Target smaller or larger than every element
""",
            "problem_slugs": ["binary-search"],
        },
        {
            "title": "Prefix and Suffix Products",
            "slug": "prefix-and-suffix-products",
            "summary": "Compute range products without division.",
            "order": 3,
            "content_markdown": """# Prefix and Suffix Products

Some array problems require combining information from the left and right side of each index.

## Idea

- `prefix[i]`: product of values before `i`
- `suffix[i]`: product of values after `i`
- answer at `i` is `prefix[i] * suffix[i]`

You can do this in O(n) time and O(1) extra space (excluding output).

```python
def product_except_self(nums):
    result = [1] * len(nums)

    prefix = 1
    for i in range(len(nums)):
        result[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result
```

## Why it works

Each index gets all multiplication from the left pass and right pass, excluding itself.
""",
            "problem_slugs": ["product-of-array-except-self"],
        },
        {
            "title": "Palindrome Checks with Two Pointers",
            "slug": "palindrome-two-pointer-technique",
            "summary": "Scan inward from both ends while skipping non-alphanumeric characters.",
            "order": 4,
            "content_markdown": """# Palindrome Checks with Two Pointers

Two pointers are ideal when you need to compare elements from both ends.

## Template for string palindrome checks

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

## Benefits

- O(n) time
- O(1) additional space
- Works well with normalized string comparisons

## Related problem

This exact pattern solves Valid Palindrome.
""",
            "problem_slugs": ["valid-palindrome"],
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

        for problem_slug in lesson_data["problem_slugs"]:
            problem = Problem.objects.filter(slug=problem_slug, is_published=True).first()
            if problem:
                lesson.problems.add(problem)


def remove_more_seed_lessons(apps, schema_editor):
    Course = apps.get_model("lessons", "Course")
    Lesson = apps.get_model("lessons", "Lesson")

    Lesson.objects.filter(slug__in=LESSON_SLUGS).delete()
    Course.objects.filter(slug=COURSE_SLUG).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0002_sample_content"),
        ("problems", "0014_add_more_seed_problems"),
    ]

    operations = [
        migrations.RunPython(add_more_seed_lessons, remove_more_seed_lessons),
    ]

