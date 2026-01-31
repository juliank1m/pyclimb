# Data migration to remove overly simple problems and add common LeetCode-style ones

from django.db import migrations
from django.template.defaultfilters import slugify
import json


def add_new_problems(apps, schema_editor):
    Problem = apps.get_model('problems', 'Problem')
    TestCase = apps.get_model('problems', 'TestCase')
    Tag = apps.get_model('problems', 'Tag')

    remove_slugs = [
        'sum-of-two-numbers',
        'count-vowels',
        'array-statistics',
    ]
    Problem.objects.filter(slug__in=remove_slugs).delete()

    def get_tag(name):
        tag, _ = Tag.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
        return tag

    problems_data = [
        {
            'title': 'Two Sum',
            'slug': 'two-sum',
            'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.',
            'constraints': '2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9\nExactly one valid answer exists.',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'twoSum',
            'signature_text': 'def twoSum(self, nums: list[int], target: int) -> list[int]',
            'starter_code': 'class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        pass',
            'tags': ['Arrays', 'Hashing'],
            'test_cases': [
                {
                    'input': json.dumps({'nums': [2, 7, 11, 15], 'target': 9}),
                    'output': json.dumps([0, 1]),
                    'display_in': 'nums = [2, 7, 11, 15], target = 9',
                    'display_out': '[0, 1]',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [3, 2, 4], 'target': 6}),
                    'output': json.dumps([1, 2]),
                    'display_in': 'nums = [3, 2, 4], target = 6',
                    'display_out': '[1, 2]',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [3, 3], 'target': 6}),
                    'output': json.dumps([0, 1]),
                    'display_in': 'nums = [3, 3], target = 6',
                    'display_out': '[0, 1]',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [1, 2, 3, 4], 'target': 7}),
                    'output': json.dumps([2, 3]),
                    'is_sample': False,
                },
            ],
        },
        {
            'title': 'Valid Anagram',
            'slug': 'valid-anagram',
            'description': 'Given two strings s and t, return true if t is an anagram of s, and false otherwise.',
            'constraints': '1 <= s.length, t.length <= 5 * 10^4\ns and t consist of lowercase English letters.',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'isAnagram',
            'signature_text': 'def isAnagram(self, s: str, t: str) -> bool',
            'starter_code': 'class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:\n        pass',
            'tags': ['Strings', 'Hashing'],
            'test_cases': [
                {
                    'input': json.dumps({'s': 'anagram', 't': 'nagaram'}),
                    'output': json.dumps(True),
                    'display_in': 's = "anagram", t = "nagaram"',
                    'display_out': 'true',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'s': 'rat', 't': 'car'}),
                    'output': json.dumps(False),
                    'display_in': 's = "rat", t = "car"',
                    'display_out': 'false',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'s': 'a', 't': 'a'}),
                    'output': json.dumps(True),
                    'is_sample': False,
                },
                {
                    'input': json.dumps({'s': 'a', 't': 'ab'}),
                    'output': json.dumps(False),
                    'is_sample': False,
                },
            ],
        },
        {
            'title': 'Best Time to Buy and Sell Stock',
            'slug': 'best-time-to-buy-and-sell-stock',
            'description': 'You are given an array prices where prices[i] is the price of a stock on the i-th day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve. If you cannot achieve any profit, return 0.',
            'constraints': '1 <= prices.length <= 10^5\n0 <= prices[i] <= 10^4',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'maxProfit',
            'signature_text': 'def maxProfit(self, prices: list[int]) -> int',
            'starter_code': 'class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        pass',
            'tags': ['Arrays', 'Dynamic Programming'],
            'test_cases': [
                {
                    'input': json.dumps({'prices': [7, 1, 5, 3, 6, 4]}),
                    'output': json.dumps(5),
                    'display_in': 'prices = [7, 1, 5, 3, 6, 4]',
                    'display_out': '5',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'prices': [7, 6, 4, 3, 1]}),
                    'output': json.dumps(0),
                    'display_in': 'prices = [7, 6, 4, 3, 1]',
                    'display_out': '0',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'prices': [2, 4, 1]}),
                    'output': json.dumps(2),
                    'display_in': 'prices = [2, 4, 1]',
                    'display_out': '2',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'prices': [1, 2]}),
                    'output': json.dumps(1),
                    'is_sample': False,
                },
            ],
        },
        {
            'title': 'Contains Duplicate',
            'slug': 'contains-duplicate',
            'description': 'Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.',
            'constraints': '1 <= nums.length <= 10^5\n-10^9 <= nums[i] <= 10^9',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'containsDuplicate',
            'signature_text': 'def containsDuplicate(self, nums: list[int]) -> bool',
            'starter_code': 'class Solution:\n    def containsDuplicate(self, nums: list[int]) -> bool:\n        pass',
            'tags': ['Arrays', 'Hashing'],
            'test_cases': [
                {
                    'input': json.dumps({'nums': [1, 2, 3, 1]}),
                    'output': json.dumps(True),
                    'display_in': 'nums = [1, 2, 3, 1]',
                    'display_out': 'true',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [1, 2, 3, 4]}),
                    'output': json.dumps(False),
                    'display_in': 'nums = [1, 2, 3, 4]',
                    'display_out': 'false',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]}),
                    'output': json.dumps(True),
                    'display_in': 'nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]',
                    'display_out': 'true',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [1]}),
                    'output': json.dumps(False),
                    'is_sample': False,
                },
            ],
        },
        {
            'title': 'Move Zeroes',
            'slug': 'move-zeroes',
            'description': 'Given an integer array nums, move all 0\'s to the end of it while maintaining the relative order of the non-zero elements.\n\nReturn the array after moving zeros.',
            'constraints': '1 <= nums.length <= 10^4\n-2^31 <= nums[i] <= 2^31 - 1',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'moveZeroes',
            'signature_text': 'def moveZeroes(self, nums: list[int]) -> list[int]',
            'starter_code': 'class Solution:\n    def moveZeroes(self, nums: list[int]) -> list[int]:\n        pass',
            'tags': ['Arrays', 'Two Pointers'],
            'test_cases': [
                {
                    'input': json.dumps({'nums': [0, 1, 0, 3, 12]}),
                    'output': json.dumps([1, 3, 12, 0, 0]),
                    'display_in': 'nums = [0, 1, 0, 3, 12]',
                    'display_out': '[1, 3, 12, 0, 0]',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [0]}),
                    'output': json.dumps([0]),
                    'display_in': 'nums = [0]',
                    'display_out': '[0]',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [1, 0, 1]}),
                    'output': json.dumps([1, 1, 0]),
                    'display_in': 'nums = [1, 0, 1]',
                    'display_out': '[1, 1, 0]',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [4, 2, 4, 0, 0, 3, 0, 5, 1, 0]}),
                    'output': json.dumps([4, 2, 4, 3, 5, 1, 0, 0, 0, 0]),
                    'is_sample': False,
                },
            ],
        },
        {
            'title': 'Climbing Stairs',
            'slug': 'climbing-stairs',
            'description': 'You are climbing a staircase. It takes n steps to reach the top.\n\nEach time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?',
            'constraints': '1 <= n <= 45',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'climbStairs',
            'signature_text': 'def climbStairs(self, n: int) -> int',
            'starter_code': 'class Solution:\n    def climbStairs(self, n: int) -> int:\n        pass',
            'tags': ['Dynamic Programming'],
            'test_cases': [
                {
                    'input': json.dumps({'n': 2}),
                    'output': json.dumps(2),
                    'display_in': 'n = 2',
                    'display_out': '2',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'n': 3}),
                    'output': json.dumps(3),
                    'display_in': 'n = 3',
                    'display_out': '3',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'n': 4}),
                    'output': json.dumps(5),
                    'display_in': 'n = 4',
                    'display_out': '5',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'n': 1}),
                    'output': json.dumps(1),
                    'is_sample': False,
                },
            ],
        },
        {
            'title': 'Kth Largest Element in an Array',
            'slug': 'kth-largest-element-in-an-array',
            'description': 'Given an integer array nums and an integer k, return the k-th largest element in the array.\n\nNote that it is the k-th largest element in the sorted order, not the k-th distinct element.',
            'constraints': '1 <= k <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'findKthLargest',
            'signature_text': 'def findKthLargest(self, nums: list[int], k: int) -> int',
            'starter_code': 'class Solution:\n    def findKthLargest(self, nums: list[int], k: int) -> int:\n        pass',
            'tags': ['Arrays', 'Sorting', 'Divide and Conquer'],
            'test_cases': [
                {
                    'input': json.dumps({'nums': [3, 2, 1, 5, 6, 4], 'k': 2}),
                    'output': json.dumps(5),
                    'display_in': 'nums = [3, 2, 1, 5, 6, 4], k = 2',
                    'display_out': '5',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [3, 2, 3, 1, 2, 4, 5, 5, 6], 'k': 4}),
                    'output': json.dumps(4),
                    'display_in': 'nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4',
                    'display_out': '4',
                    'is_sample': True,
                },
                {
                    'input': json.dumps({'nums': [1], 'k': 1}),
                    'output': json.dumps(1),
                    'is_sample': False,
                },
            ],
        },
    ]

    for pdata in problems_data:
        if Problem.objects.filter(slug=pdata['slug']).exists():
            continue

        problem = Problem.objects.create(
            title=pdata['title'],
            slug=pdata['slug'],
            description=pdata['description'],
            constraints=pdata.get('constraints', ''),
            follow_up=pdata.get('follow_up', ''),
            difficulty=pdata['difficulty'],
            judge_mode=pdata['judge_mode'],
            entrypoint_type=pdata.get('entrypoint_type', ''),
            entrypoint_name=pdata.get('entrypoint_name', ''),
            signature_text=pdata.get('signature_text', ''),
            starter_code=pdata.get('starter_code', ''),
            is_published=True,
        )

        for tag_name in pdata.get('tags', []):
            problem.tags.add(get_tag(tag_name))

        for tc in pdata.get('test_cases', []):
            TestCase.objects.create(
                problem=problem,
                input_data=tc['input'],
                expected_output=tc['output'],
                display_input=tc.get('display_in', ''),
                display_output=tc.get('display_out', ''),
                explanation=tc.get('explanation', ''),
                is_sample=tc.get('is_sample', False),
            )


def remove_new_problems(apps, schema_editor):
    Problem = apps.get_model('problems', 'Problem')
    Problem.objects.filter(slug__in=[
        'two-sum',
        'valid-anagram',
        'best-time-to-buy-and-sell-stock',
        'contains-duplicate',
        'move-zeroes',
        'climbing-stairs',
        'kth-largest-element-in-an-array',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0012_convert_remaining_stdin_to_class'),
    ]

    operations = [
        migrations.RunPython(add_new_problems, remove_new_problems),
    ]
