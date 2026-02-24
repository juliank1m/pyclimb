from django.db import migrations
from django.template.defaultfilters import slugify
import json


PROBLEM_SLUGS = [
    "valid-palindrome",
    "binary-search",
    "product-of-array-except-self",
    "maximum-subarray",
]


def add_more_seed_problems(apps, schema_editor):
    Problem = apps.get_model("problems", "Problem")
    TestCase = apps.get_model("problems", "TestCase")
    Tag = apps.get_model("problems", "Tag")

    def get_tag(name):
        tag, _ = Tag.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
        return tag

    problems_data = [
        {
            "title": "Valid Palindrome",
            "slug": "valid-palindrome",
            "description": (
                "Given a string s, return true if it is a palindrome, or false otherwise.\n\n"
                "A palindrome reads the same forward and backward after converting all "
                "uppercase letters into lowercase letters and removing all non-alphanumeric "
                "characters."
            ),
            "constraints": "1 <= s.length <= 2 * 10^5\ns consists of printable ASCII characters.",
            "difficulty": 1,
            "judge_mode": "function",
            "entrypoint_type": "class",
            "entrypoint_name": "isPalindrome",
            "signature_text": "def isPalindrome(self, s: str) -> bool",
            "starter_code": (
                "class Solution:\n"
                "    def isPalindrome(self, s: str) -> bool:\n"
                "        pass"
            ),
            "tags": ["Strings", "Two Pointers"],
            "test_cases": [
                {
                    "input": json.dumps({"s": "A man, a plan, a canal: Panama"}),
                    "output": json.dumps(True),
                    "display_in": 's = "A man, a plan, a canal: Panama"',
                    "display_out": "true",
                    "is_sample": True,
                },
                {
                    "input": json.dumps({"s": "race a car"}),
                    "output": json.dumps(False),
                    "display_in": 's = "race a car"',
                    "display_out": "false",
                    "is_sample": True,
                },
                {
                    "input": json.dumps({"s": " "}),
                    "output": json.dumps(True),
                    "is_sample": False,
                },
            ],
        },
        {
            "title": "Binary Search",
            "slug": "binary-search",
            "description": (
                "Given an array of integers nums sorted in ascending order and an integer "
                "target, return the index of target if it exists, otherwise return -1."
            ),
            "constraints": (
                "1 <= nums.length <= 10^4\n"
                "-10^4 < nums[i], target < 10^4\n"
                "All integers in nums are unique.\n"
                "nums is sorted in ascending order."
            ),
            "difficulty": 1,
            "judge_mode": "function",
            "entrypoint_type": "class",
            "entrypoint_name": "search",
            "signature_text": "def search(self, nums: list[int], target: int) -> int",
            "starter_code": (
                "class Solution:\n"
                "    def search(self, nums: list[int], target: int) -> int:\n"
                "        pass"
            ),
            "tags": ["Arrays", "Binary Search"],
            "test_cases": [
                {
                    "input": json.dumps({"nums": [-1, 0, 3, 5, 9, 12], "target": 9}),
                    "output": json.dumps(4),
                    "display_in": "nums = [-1, 0, 3, 5, 9, 12], target = 9",
                    "display_out": "4",
                    "is_sample": True,
                },
                {
                    "input": json.dumps({"nums": [-1, 0, 3, 5, 9, 12], "target": 2}),
                    "output": json.dumps(-1),
                    "display_in": "nums = [-1, 0, 3, 5, 9, 12], target = 2",
                    "display_out": "-1",
                    "is_sample": True,
                },
                {
                    "input": json.dumps({"nums": [5], "target": 5}),
                    "output": json.dumps(0),
                    "is_sample": False,
                },
            ],
        },
        {
            "title": "Product of Array Except Self",
            "slug": "product-of-array-except-self",
            "description": (
                "Given an integer array nums, return an array answer such that answer[i] "
                "is equal to the product of all the elements of nums except nums[i].\n\n"
                "You must write an algorithm that runs in O(n) time and without using division."
            ),
            "constraints": "2 <= nums.length <= 10^5\n-30 <= nums[i] <= 30",
            "difficulty": 2,
            "judge_mode": "function",
            "entrypoint_type": "class",
            "entrypoint_name": "productExceptSelf",
            "signature_text": "def productExceptSelf(self, nums: list[int]) -> list[int]",
            "starter_code": (
                "class Solution:\n"
                "    def productExceptSelf(self, nums: list[int]) -> list[int]:\n"
                "        pass"
            ),
            "tags": ["Arrays", "Prefix Sum"],
            "test_cases": [
                {
                    "input": json.dumps({"nums": [1, 2, 3, 4]}),
                    "output": json.dumps([24, 12, 8, 6]),
                    "display_in": "nums = [1, 2, 3, 4]",
                    "display_out": "[24, 12, 8, 6]",
                    "is_sample": True,
                },
                {
                    "input": json.dumps({"nums": [-1, 1, 0, -3, 3]}),
                    "output": json.dumps([0, 0, 9, 0, 0]),
                    "display_in": "nums = [-1, 1, 0, -3, 3]",
                    "display_out": "[0, 0, 9, 0, 0]",
                    "is_sample": True,
                },
                {
                    "input": json.dumps({"nums": [2, 3, 4, 5]}),
                    "output": json.dumps([60, 40, 30, 24]),
                    "is_sample": False,
                },
            ],
        },
        {
            "title": "Maximum Subarray",
            "slug": "maximum-subarray",
            "description": (
                "Given an integer array nums, find the subarray with the largest sum and "
                "return its sum."
            ),
            "constraints": "1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4",
            "difficulty": 2,
            "judge_mode": "function",
            "entrypoint_type": "class",
            "entrypoint_name": "maxSubArray",
            "signature_text": "def maxSubArray(self, nums: list[int]) -> int",
            "starter_code": (
                "class Solution:\n"
                "    def maxSubArray(self, nums: list[int]) -> int:\n"
                "        pass"
            ),
            "tags": ["Arrays", "Dynamic Programming"],
            "test_cases": [
                {
                    "input": json.dumps({"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}),
                    "output": json.dumps(6),
                    "display_in": "nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]",
                    "display_out": "6",
                    "is_sample": True,
                },
                {
                    "input": json.dumps({"nums": [1]}),
                    "output": json.dumps(1),
                    "display_in": "nums = [1]",
                    "display_out": "1",
                    "is_sample": True,
                },
                {
                    "input": json.dumps({"nums": [5, 4, -1, 7, 8]}),
                    "output": json.dumps(23),
                    "display_in": "nums = [5, 4, -1, 7, 8]",
                    "display_out": "23",
                    "is_sample": True,
                },
                {
                    "input": json.dumps({"nums": [-5, -3, -1]}),
                    "output": json.dumps(-1),
                    "is_sample": False,
                },
            ],
        },
    ]

    for pdata in problems_data:
        if Problem.objects.filter(slug=pdata["slug"]).exists():
            continue

        problem = Problem.objects.create(
            title=pdata["title"],
            slug=pdata["slug"],
            description=pdata["description"],
            constraints=pdata.get("constraints", ""),
            follow_up=pdata.get("follow_up", ""),
            difficulty=pdata["difficulty"],
            judge_mode=pdata["judge_mode"],
            entrypoint_type=pdata.get("entrypoint_type", ""),
            entrypoint_name=pdata.get("entrypoint_name", ""),
            signature_text=pdata.get("signature_text", ""),
            starter_code=pdata.get("starter_code", ""),
            is_published=True,
        )

        for tag_name in pdata.get("tags", []):
            problem.tags.add(get_tag(tag_name))

        for tc in pdata.get("test_cases", []):
            TestCase.objects.create(
                problem=problem,
                input_data=tc["input"],
                expected_output=tc["output"],
                display_input=tc.get("display_in", ""),
                display_output=tc.get("display_out", ""),
                explanation=tc.get("explanation", ""),
                is_sample=tc.get("is_sample", False),
            )


def remove_more_seed_problems(apps, schema_editor):
    Problem = apps.get_model("problems", "Problem")
    Problem.objects.filter(slug__in=PROBLEM_SLUGS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0013_refresh_problem_set"),
    ]

    operations = [
        migrations.RunPython(add_more_seed_problems, remove_more_seed_problems),
    ]

