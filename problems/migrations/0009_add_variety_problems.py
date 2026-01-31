# Data migration to add more variety of problems across different categories

from django.db import migrations


def add_tags_and_problems(apps, schema_editor):
    Problem = apps.get_model('problems', 'Problem')
    TestCase = apps.get_model('problems', 'TestCase')
    Tag = apps.get_model('problems', 'Tag')

    # Create additional tags (must set slug explicitly in migrations)
    from django.template.defaultfilters import slugify
    additional_tags = [
        'Sorting', 'Greedy', 'Backtracking', 'Bit Manipulation',
        'Matrix', 'Stack', 'Queue', 'Math', 'Simulation',
        'Sliding Window', 'Prefix Sum', 'Trees', 'Graphs',
    ]
    for tag_name in additional_tags:
        tag_slug = slugify(tag_name)
        if not Tag.objects.filter(slug=tag_slug).exists():
            Tag.objects.create(name=tag_name, slug=tag_slug)

    def get_tag(name):
        try:
            return Tag.objects.get(name=name)
        except Tag.DoesNotExist:
            return None

    problems_data = [
        # ============ MATRIX PROBLEMS ============
        {
            'title': 'Rotate Image',
            'slug': 'rotate-image',
            'description': '''You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.''',
            'constraints': 'n == matrix.length == matrix[i].length\n1 <= n <= 20\n-1000 <= matrix[i][j] <= 1000',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'rotate',
            'signature_text': 'def rotate(self, matrix: list[list[int]]) -> None',
            'starter_code': 'class Solution:\n    def rotate(self, matrix: list[list[int]]) -> None:\n        """\n        Do not return anything, modify matrix in-place instead.\n        """\n        pass',
            'tags': ['Matrix', 'Arrays'],
            'test_cases': [
                {'input': '{"matrix": [[1,2,3],[4,5,6],[7,8,9]]}', 'output': '[[7,4,1],[8,5,2],[9,6,3]]', 'display_in': 'matrix = [[1,2,3],[4,5,6],[7,8,9]]', 'display_out': '[[7,4,1],[8,5,2],[9,6,3]]', 'is_sample': True},
                {'input': '{"matrix": [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]}', 'output': '[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]', 'display_in': 'matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]', 'display_out': '[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]', 'is_sample': True},
                {'input': '{"matrix": [[1]]}', 'output': '[[1]]', 'is_sample': False},
            ]
        },
        {
            'title': 'Spiral Matrix',
            'slug': 'spiral-matrix',
            'description': '''Given an m x n matrix, return all elements of the matrix in spiral order.''',
            'constraints': 'm == matrix.length\nn == matrix[i].length\n1 <= m, n <= 10\n-100 <= matrix[i][j] <= 100',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'spiralOrder',
            'signature_text': 'def spiralOrder(self, matrix: list[list[int]]) -> list[int]',
            'starter_code': 'class Solution:\n    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:\n        pass',
            'tags': ['Matrix', 'Arrays', 'Simulation'],
            'test_cases': [
                {'input': '{"matrix": [[1,2,3],[4,5,6],[7,8,9]]}', 'output': '[1,2,3,6,9,8,7,4,5]', 'display_in': 'matrix = [[1,2,3],[4,5,6],[7,8,9]]', 'display_out': '[1,2,3,6,9,8,7,4,5]', 'is_sample': True},
                {'input': '{"matrix": [[1,2,3,4],[5,6,7,8],[9,10,11,12]]}', 'output': '[1,2,3,4,8,12,11,10,9,5,6,7]', 'display_in': 'matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]', 'display_out': '[1,2,3,4,8,12,11,10,9,5,6,7]', 'is_sample': True},
                {'input': '{"matrix": [[1]]}', 'output': '[1]', 'is_sample': False},
                {'input': '{"matrix": [[1,2],[3,4]]}', 'output': '[1,2,4,3]', 'is_sample': False},
            ]
        },
        {
            'title': 'Set Matrix Zeroes',
            'slug': 'set-matrix-zeroes',
            'description': '''Given an m x n integer matrix, if an element is 0, set its entire row and column to 0\'s.

You must do it in place.''',
            'constraints': 'm == matrix.length\nn == matrix[0].length\n1 <= m, n <= 200\n-2^31 <= matrix[i][j] <= 2^31 - 1',
            'follow_up': 'Can you solve it using O(1) extra space?',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'setZeroes',
            'signature_text': 'def setZeroes(self, matrix: list[list[int]]) -> None',
            'starter_code': 'class Solution:\n    def setZeroes(self, matrix: list[list[int]]) -> None:\n        """\n        Do not return anything, modify matrix in-place instead.\n        """\n        pass',
            'tags': ['Matrix', 'Arrays'],
            'test_cases': [
                {'input': '{"matrix": [[1,1,1],[1,0,1],[1,1,1]]}', 'output': '[[1,0,1],[0,0,0],[1,0,1]]', 'display_in': 'matrix = [[1,1,1],[1,0,1],[1,1,1]]', 'display_out': '[[1,0,1],[0,0,0],[1,0,1]]', 'is_sample': True},
                {'input': '{"matrix": [[0,1,2,0],[3,4,5,2],[1,3,1,5]]}', 'output': '[[0,0,0,0],[0,4,5,0],[0,3,1,0]]', 'display_in': 'matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]', 'display_out': '[[0,0,0,0],[0,4,5,0],[0,3,1,0]]', 'is_sample': True},
                {'input': '{"matrix": [[1,2,3],[4,5,6]]}', 'output': '[[1,2,3],[4,5,6]]', 'is_sample': False},
            ]
        },
        # ============ STACK PROBLEMS ============
        {
            'title': 'Min Stack',
            'slug': 'min-stack',
            'description': '''Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:
- MinStack() initializes the stack object.
- void push(int val) pushes the element val onto the stack.
- void pop() removes the element on the top of the stack.
- int top() gets the top element of the stack.
- int getMin() retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.

For this problem, you'll receive a list of operations and their arguments, and return a list of results.''',
            'constraints': '-2^31 <= val <= 2^31 - 1\nMethods pop, top and getMin operations will always be called on non-empty stacks.\nAt most 3 * 10^4 calls will be made to push, pop, top, and getMin.',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'minStack',
            'signature_text': 'def minStack(self, operations: list[tuple]) -> list',
            'starter_code': '''class MinStack:
    def __init__(self):
        pass
    
    def push(self, val: int) -> None:
        pass
    
    def pop(self) -> None:
        pass
    
    def top(self) -> int:
        pass
    
    def getMin(self) -> int:
        pass

class Solution:
    def minStack(self, operations: list[tuple]) -> list:
        """
        operations is a list of (method_name, args) tuples.
        Return a list of results for each operation (None for void methods).
        """
        stack = MinStack()
        results = []
        for op, args in operations:
            if op == "push":
                results.append(stack.push(args[0]))
            elif op == "pop":
                results.append(stack.pop())
            elif op == "top":
                results.append(stack.top())
            elif op == "getMin":
                results.append(stack.getMin())
        return results''',
            'tags': ['Stack'],
            'test_cases': [
                {'input': '{"operations": [["push", [-2]], ["push", [0]], ["push", [-3]], ["getMin", []], ["pop", []], ["top", []], ["getMin", []]]}', 'output': '[null,null,null,-3,null,0,-2]', 'display_in': 'push(-2), push(0), push(-3), getMin(), pop(), top(), getMin()', 'display_out': '[null,null,null,-3,null,0,-2]', 'is_sample': True, 'explanation': 'MinStack minStack = new MinStack(); minStack.push(-2); minStack.push(0); minStack.push(-3); minStack.getMin(); -> -3; minStack.pop(); minStack.top(); -> 0; minStack.getMin(); -> -2'},
                {'input': '{"operations": [["push", [1]], ["push", [2]], ["top", []], ["getMin", []]]}', 'output': '[null,null,2,1]', 'is_sample': False},
            ]
        },
        {
            'title': 'Daily Temperatures',
            'slug': 'daily-temperatures',
            'description': '''Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.''',
            'constraints': '1 <= temperatures.length <= 10^5\n30 <= temperatures[i] <= 100',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'dailyTemperatures',
            'signature_text': 'def dailyTemperatures(self, temperatures: list[int]) -> list[int]',
            'starter_code': 'class Solution:\n    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:\n        pass',
            'tags': ['Stack', 'Arrays'],
            'test_cases': [
                {'input': '{"temperatures": [73,74,75,71,69,72,76,73]}', 'output': '[1,1,4,2,1,1,0,0]', 'display_in': 'temperatures = [73,74,75,71,69,72,76,73]', 'display_out': '[1,1,4,2,1,1,0,0]', 'is_sample': True},
                {'input': '{"temperatures": [30,40,50,60]}', 'output': '[1,1,1,0]', 'display_in': 'temperatures = [30,40,50,60]', 'display_out': '[1,1,1,0]', 'is_sample': True},
                {'input': '{"temperatures": [30,60,90]}', 'output': '[1,1,0]', 'display_in': 'temperatures = [30,60,90]', 'display_out': '[1,1,0]', 'is_sample': True},
                {'input': '{"temperatures": [90,80,70,60]}', 'output': '[0,0,0,0]', 'is_sample': False},
            ]
        },
        # ============ SLIDING WINDOW PROBLEMS ============
        {
            'title': 'Maximum Average Subarray I',
            'slug': 'maximum-average-subarray-i',
            'description': '''You are given an integer array nums consisting of n elements, and an integer k.

Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value. Any answer with a calculation error less than 10^-5 will be accepted.''',
            'constraints': 'n == nums.length\n1 <= k <= n <= 10^5\n-10^4 <= nums[i] <= 10^4',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'findMaxAverage',
            'signature_text': 'def findMaxAverage(self, nums: list[int], k: int) -> float',
            'starter_code': 'class Solution:\n    def findMaxAverage(self, nums: list[int], k: int) -> float:\n        pass',
            'tags': ['Arrays', 'Sliding Window'],
            'test_cases': [
                {'input': '{"nums": [1,12,-5,-6,50,3], "k": 4}', 'output': '12.75', 'display_in': 'nums = [1,12,-5,-6,50,3], k = 4', 'display_out': '12.75', 'is_sample': True, 'explanation': 'Maximum average is (12 + -5 + -6 + 50) / 4 = 51 / 4 = 12.75'},
                {'input': '{"nums": [5], "k": 1}', 'output': '5.0', 'display_in': 'nums = [5], k = 1', 'display_out': '5.0', 'is_sample': True},
                {'input': '{"nums": [0,4,0,3,2], "k": 1}', 'output': '4.0', 'is_sample': False},
            ]
        },
        {
            'title': 'Minimum Size Subarray Sum',
            'slug': 'minimum-size-subarray-sum',
            'description': '''Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.''',
            'constraints': '1 <= target <= 10^9\n1 <= nums.length <= 10^5\n1 <= nums[i] <= 10^4',
            'follow_up': 'If you have figured out the O(n) solution, try coding another solution of which the time complexity is O(n log(n)).',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'minSubArrayLen',
            'signature_text': 'def minSubArrayLen(self, target: int, nums: list[int]) -> int',
            'starter_code': 'class Solution:\n    def minSubArrayLen(self, target: int, nums: list[int]) -> int:\n        pass',
            'tags': ['Arrays', 'Sliding Window', 'Two Pointers'],
            'test_cases': [
                {'input': '{"target": 7, "nums": [2,3,1,2,4,3]}', 'output': '2', 'display_in': 'target = 7, nums = [2,3,1,2,4,3]', 'display_out': '2', 'is_sample': True, 'explanation': 'The subarray [4,3] has the minimal length under the problem constraint.'},
                {'input': '{"target": 4, "nums": [1,4,4]}', 'output': '1', 'display_in': 'target = 4, nums = [1,4,4]', 'display_out': '1', 'is_sample': True},
                {'input': '{"target": 11, "nums": [1,1,1,1,1,1,1,1]}', 'output': '0', 'display_in': 'target = 11, nums = [1,1,1,1,1,1,1,1]', 'display_out': '0', 'is_sample': True},
                {'input': '{"target": 15, "nums": [5,1,3,5,10,7,4,9,2,8]}', 'output': '2', 'is_sample': False},
            ]
        },
        # ============ GREEDY PROBLEMS ============
        {
            'title': 'Jump Game',
            'slug': 'jump-game',
            'description': '''You are given an integer array nums. You are initially positioned at the array\'s first index, and each element in the array represents your maximum jump length at that position.

Return true if you can reach the last index, or false otherwise.''',
            'constraints': '1 <= nums.length <= 10^4\n0 <= nums[i] <= 10^5',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'canJump',
            'signature_text': 'def canJump(self, nums: list[int]) -> bool',
            'starter_code': 'class Solution:\n    def canJump(self, nums: list[int]) -> bool:\n        pass',
            'tags': ['Arrays', 'Greedy', 'Dynamic Programming'],
            'test_cases': [
                {'input': '{"nums": [2,3,1,1,4]}', 'output': 'true', 'display_in': 'nums = [2,3,1,1,4]', 'display_out': 'true', 'is_sample': True, 'explanation': 'Jump 1 step from index 0 to 1, then 3 steps to the last index.'},
                {'input': '{"nums": [3,2,1,0,4]}', 'output': 'false', 'display_in': 'nums = [3,2,1,0,4]', 'display_out': 'false', 'is_sample': True, 'explanation': 'You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.'},
                {'input': '{"nums": [0]}', 'output': 'true', 'is_sample': False},
                {'input': '{"nums": [2,0,0]}', 'output': 'true', 'is_sample': False},
            ]
        },
        {
            'title': 'Best Time to Buy and Sell Stock II',
            'slug': 'best-time-to-buy-and-sell-stock-ii',
            'description': '''You are given an integer array prices where prices[i] is the price of a given stock on the ith day.

On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can buy it then immediately sell it on the same day.

Find and return the maximum profit you can achieve.''',
            'constraints': '1 <= prices.length <= 3 * 10^4\n0 <= prices[i] <= 10^4',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'maxProfit',
            'signature_text': 'def maxProfit(self, prices: list[int]) -> int',
            'starter_code': 'class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        pass',
            'tags': ['Arrays', 'Greedy', 'Dynamic Programming'],
            'test_cases': [
                {'input': '{"prices": [7,1,5,3,6,4]}', 'output': '7', 'display_in': 'prices = [7,1,5,3,6,4]', 'display_out': '7', 'is_sample': True, 'explanation': 'Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4. Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3. Total profit is 4 + 3 = 7.'},
                {'input': '{"prices": [1,2,3,4,5]}', 'output': '4', 'display_in': 'prices = [1,2,3,4,5]', 'display_out': '4', 'is_sample': True, 'explanation': 'Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.'},
                {'input': '{"prices": [7,6,4,3,1]}', 'output': '0', 'display_in': 'prices = [7,6,4,3,1]', 'display_out': '0', 'is_sample': True, 'explanation': 'There is no way to make a positive profit.'},
                {'input': '{"prices": [1]}', 'output': '0', 'is_sample': False},
            ]
        },
        # ============ BIT MANIPULATION PROBLEMS ============
        {
            'title': 'Single Number',
            'slug': 'single-number',
            'description': '''Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.''',
            'constraints': '1 <= nums.length <= 3 * 10^4\n-3 * 10^4 <= nums[i] <= 3 * 10^4\nEach element in the array appears twice except for one element which appears only once.',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'singleNumber',
            'signature_text': 'def singleNumber(self, nums: list[int]) -> int',
            'starter_code': 'class Solution:\n    def singleNumber(self, nums: list[int]) -> int:\n        pass',
            'tags': ['Arrays', 'Bit Manipulation'],
            'test_cases': [
                {'input': '{"nums": [2,2,1]}', 'output': '1', 'display_in': 'nums = [2,2,1]', 'display_out': '1', 'is_sample': True},
                {'input': '{"nums": [4,1,2,1,2]}', 'output': '4', 'display_in': 'nums = [4,1,2,1,2]', 'display_out': '4', 'is_sample': True},
                {'input': '{"nums": [1]}', 'output': '1', 'display_in': 'nums = [1]', 'display_out': '1', 'is_sample': True},
                {'input': '{"nums": [-1,-1,-2]}', 'output': '-2', 'is_sample': False},
            ]
        },
        {
            'title': 'Number of 1 Bits',
            'slug': 'number-of-1-bits',
            'description': '''Write a function that takes the binary representation of a positive integer and returns the number of set bits it has (also known as the Hamming weight).''',
            'constraints': '1 <= n <= 2^31 - 1',
            'follow_up': 'If this function is called many times, how would you optimize it?',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'hammingWeight',
            'signature_text': 'def hammingWeight(self, n: int) -> int',
            'starter_code': 'class Solution:\n    def hammingWeight(self, n: int) -> int:\n        pass',
            'tags': ['Bit Manipulation'],
            'test_cases': [
                {'input': '{"n": 11}', 'output': '3', 'display_in': 'n = 11 (binary: 1011)', 'display_out': '3', 'is_sample': True, 'explanation': 'The input binary string 1011 has a total of three set bits.'},
                {'input': '{"n": 128}', 'output': '1', 'display_in': 'n = 128 (binary: 10000000)', 'display_out': '1', 'is_sample': True},
                {'input': '{"n": 2147483645}', 'output': '30', 'display_in': 'n = 2147483645', 'display_out': '30', 'is_sample': True},
                {'input': '{"n": 1}', 'output': '1', 'is_sample': False},
                {'input': '{"n": 15}', 'output': '4', 'is_sample': False},
            ]
        },
        {
            'title': 'Counting Bits',
            'slug': 'counting-bits',
            'description': '''Given an integer n, return an array ans of length n + 1 such that for each i (0 <= i <= n), ans[i] is the number of 1\'s in the binary representation of i.''',
            'constraints': '0 <= n <= 10^5',
            'follow_up': 'Can you do it in O(n) time and O(1) extra space (not counting the output)?',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'countBits',
            'signature_text': 'def countBits(self, n: int) -> list[int]',
            'starter_code': 'class Solution:\n    def countBits(self, n: int) -> list[int]:\n        pass',
            'tags': ['Bit Manipulation', 'Dynamic Programming'],
            'test_cases': [
                {'input': '{"n": 2}', 'output': '[0,1,1]', 'display_in': 'n = 2', 'display_out': '[0,1,1]', 'is_sample': True, 'explanation': '0 --> 0, 1 --> 1, 2 --> 10'},
                {'input': '{"n": 5}', 'output': '[0,1,1,2,1,2]', 'display_in': 'n = 5', 'display_out': '[0,1,1,2,1,2]', 'is_sample': True, 'explanation': '0 --> 0, 1 --> 1, 2 --> 10, 3 --> 11, 4 --> 100, 5 --> 101'},
                {'input': '{"n": 0}', 'output': '[0]', 'is_sample': False},
            ]
        },
        # ============ BACKTRACKING PROBLEMS ============
        {
            'title': 'Subsets',
            'slug': 'subsets',
            'description': '''Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.''',
            'constraints': '1 <= nums.length <= 10\n-10 <= nums[i] <= 10\nAll the numbers of nums are unique.',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'subsets',
            'signature_text': 'def subsets(self, nums: list[int]) -> list[list[int]]',
            'starter_code': 'class Solution:\n    def subsets(self, nums: list[int]) -> list[list[int]]:\n        pass',
            'tags': ['Arrays', 'Backtracking', 'Bit Manipulation'],
            'test_cases': [
                {'input': '{"nums": [1,2,3]}', 'output': '[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]', 'display_in': 'nums = [1,2,3]', 'display_out': '[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]', 'is_sample': True},
                {'input': '{"nums": [0]}', 'output': '[[],[0]]', 'display_in': 'nums = [0]', 'display_out': '[[],[0]]', 'is_sample': True},
                {'input': '{"nums": [1,2]}', 'output': '[[],[1],[2],[1,2]]', 'is_sample': False},
            ]
        },
        {
            'title': 'Permutations',
            'slug': 'permutations',
            'description': '''Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.''',
            'constraints': '1 <= nums.length <= 6\n-10 <= nums[i] <= 10\nAll the integers of nums are unique.',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'permute',
            'signature_text': 'def permute(self, nums: list[int]) -> list[list[int]]',
            'starter_code': 'class Solution:\n    def permute(self, nums: list[int]) -> list[list[int]]:\n        pass',
            'tags': ['Arrays', 'Backtracking'],
            'test_cases': [
                {'input': '{"nums": [1,2,3]}', 'output': '[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]', 'display_in': 'nums = [1,2,3]', 'display_out': '[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]', 'is_sample': True},
                {'input': '{"nums": [0,1]}', 'output': '[[0,1],[1,0]]', 'display_in': 'nums = [0,1]', 'display_out': '[[0,1],[1,0]]', 'is_sample': True},
                {'input': '{"nums": [1]}', 'output': '[[1]]', 'display_in': 'nums = [1]', 'display_out': '[[1]]', 'is_sample': True},
            ]
        },
        {
            'title': 'Combination Sum',
            'slug': 'combination-sum',
            'description': '''Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.''',
            'constraints': '1 <= candidates.length <= 30\n2 <= candidates[i] <= 40\nAll elements of candidates are distinct.\n1 <= target <= 40',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'combinationSum',
            'signature_text': 'def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]',
            'starter_code': 'class Solution:\n    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:\n        pass',
            'tags': ['Arrays', 'Backtracking'],
            'test_cases': [
                {'input': '{"candidates": [2,3,6,7], "target": 7}', 'output': '[[2,2,3],[7]]', 'display_in': 'candidates = [2,3,6,7], target = 7', 'display_out': '[[2,2,3],[7]]', 'is_sample': True, 'explanation': '2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times. 7 is a candidate, and 7 = 7. These are the only two combinations.'},
                {'input': '{"candidates": [2,3,5], "target": 8}', 'output': '[[2,2,2,2],[2,3,3],[3,5]]', 'display_in': 'candidates = [2,3,5], target = 8', 'display_out': '[[2,2,2,2],[2,3,3],[3,5]]', 'is_sample': True},
                {'input': '{"candidates": [2], "target": 1}', 'output': '[]', 'display_in': 'candidates = [2], target = 1', 'display_out': '[]', 'is_sample': True},
            ]
        },
        # ============ MORE DYNAMIC PROGRAMMING ============
        {
            'title': 'Climbing Stairs',
            'slug': 'climbing-stairs',
            'description': '''You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?''',
            'constraints': '1 <= n <= 45',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'climbStairs',
            'signature_text': 'def climbStairs(self, n: int) -> int',
            'starter_code': 'class Solution:\n    def climbStairs(self, n: int) -> int:\n        pass',
            'tags': ['Dynamic Programming', 'Math'],
            'test_cases': [
                {'input': '{"n": 2}', 'output': '2', 'display_in': 'n = 2', 'display_out': '2', 'is_sample': True, 'explanation': 'There are two ways to climb to the top: 1. 1 step + 1 step, 2. 2 steps'},
                {'input': '{"n": 3}', 'output': '3', 'display_in': 'n = 3', 'display_out': '3', 'is_sample': True, 'explanation': 'There are three ways: 1. 1+1+1, 2. 1+2, 3. 2+1'},
                {'input': '{"n": 1}', 'output': '1', 'is_sample': False},
                {'input': '{"n": 5}', 'output': '8', 'is_sample': False},
            ]
        },
        {
            'title': 'House Robber',
            'slug': 'house-robber',
            'description': '''You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.''',
            'constraints': '1 <= nums.length <= 100\n0 <= nums[i] <= 400',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'rob',
            'signature_text': 'def rob(self, nums: list[int]) -> int',
            'starter_code': 'class Solution:\n    def rob(self, nums: list[int]) -> int:\n        pass',
            'tags': ['Arrays', 'Dynamic Programming'],
            'test_cases': [
                {'input': '{"nums": [1,2,3,1]}', 'output': '4', 'display_in': 'nums = [1,2,3,1]', 'display_out': '4', 'is_sample': True, 'explanation': 'Rob house 1 (money = 1) and then rob house 3 (money = 3). Total amount = 1 + 3 = 4.'},
                {'input': '{"nums": [2,7,9,3,1]}', 'output': '12', 'display_in': 'nums = [2,7,9,3,1]', 'display_out': '12', 'is_sample': True, 'explanation': 'Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1). Total amount = 2 + 9 + 1 = 12.'},
                {'input': '{"nums": [1]}', 'output': '1', 'is_sample': False},
                {'input': '{"nums": [2,1,1,2]}', 'output': '4', 'is_sample': False},
            ]
        },
        {
            'title': 'Coin Change',
            'slug': 'coin-change',
            'description': '''You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.''',
            'constraints': '1 <= coins.length <= 12\n1 <= coins[i] <= 2^31 - 1\n0 <= amount <= 10^4',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'coinChange',
            'signature_text': 'def coinChange(self, coins: list[int], amount: int) -> int',
            'starter_code': 'class Solution:\n    def coinChange(self, coins: list[int], amount: int) -> int:\n        pass',
            'tags': ['Arrays', 'Dynamic Programming'],
            'test_cases': [
                {'input': '{"coins": [1,2,5], "amount": 11}', 'output': '3', 'display_in': 'coins = [1,2,5], amount = 11', 'display_out': '3', 'is_sample': True, 'explanation': '11 = 5 + 5 + 1'},
                {'input': '{"coins": [2], "amount": 3}', 'output': '-1', 'display_in': 'coins = [2], amount = 3', 'display_out': '-1', 'is_sample': True},
                {'input': '{"coins": [1], "amount": 0}', 'output': '0', 'display_in': 'coins = [1], amount = 0', 'display_out': '0', 'is_sample': True},
                {'input': '{"coins": [1,2,5], "amount": 100}', 'output': '20', 'is_sample': False},
            ]
        },
        {
            'title': 'Unique Paths',
            'slug': 'unique-paths',
            'description': '''There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.''',
            'constraints': '1 <= m, n <= 100',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'uniquePaths',
            'signature_text': 'def uniquePaths(self, m: int, n: int) -> int',
            'starter_code': 'class Solution:\n    def uniquePaths(self, m: int, n: int) -> int:\n        pass',
            'tags': ['Dynamic Programming', 'Math'],
            'test_cases': [
                {'input': '{"m": 3, "n": 7}', 'output': '28', 'display_in': 'm = 3, n = 7', 'display_out': '28', 'is_sample': True},
                {'input': '{"m": 3, "n": 2}', 'output': '3', 'display_in': 'm = 3, n = 2', 'display_out': '3', 'is_sample': True, 'explanation': 'From the top-left corner, there are a total of 3 ways to reach the bottom-right corner: 1. Right -> Down -> Down, 2. Down -> Down -> Right, 3. Down -> Right -> Down'},
                {'input': '{"m": 1, "n": 1}', 'output': '1', 'is_sample': False},
                {'input': '{"m": 7, "n": 3}', 'output': '28', 'is_sample': False},
            ]
        },
        # ============ SORTING PROBLEMS ============
        {
            'title': 'Merge Sorted Array',
            'slug': 'merge-sorted-array',
            'description': '''You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be stored inside the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. nums2 has a length of n.''',
            'constraints': 'nums1.length == m + n\nnums2.length == n\n0 <= m, n <= 200\n1 <= m + n <= 200\n-10^9 <= nums1[i], nums2[j] <= 10^9',
            'follow_up': 'Can you come up with an algorithm that runs in O(m + n) time?',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'merge',
            'signature_text': 'def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None',
            'starter_code': 'class Solution:\n    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:\n        """\n        Do not return anything, modify nums1 in-place instead.\n        """\n        pass',
            'tags': ['Arrays', 'Sorting', 'Two Pointers'],
            'test_cases': [
                {'input': '{"nums1": [1,2,3,0,0,0], "m": 3, "nums2": [2,5,6], "n": 3}', 'output': '[1,2,2,3,5,6]', 'display_in': 'nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3', 'display_out': '[1,2,2,3,5,6]', 'is_sample': True, 'explanation': 'The arrays we are merging are [1,2,3] and [2,5,6].'},
                {'input': '{"nums1": [1], "m": 1, "nums2": [], "n": 0}', 'output': '[1]', 'display_in': 'nums1 = [1], m = 1, nums2 = [], n = 0', 'display_out': '[1]', 'is_sample': True},
                {'input': '{"nums1": [0], "m": 0, "nums2": [1], "n": 1}', 'output': '[1]', 'display_in': 'nums1 = [0], m = 0, nums2 = [1], n = 1', 'display_out': '[1]', 'is_sample': True},
            ]
        },
        {
            'title': 'Sort Colors',
            'slug': 'sort-colors',
            'description': '''Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library\'s sort function.''',
            'constraints': 'n == nums.length\n1 <= n <= 300\nnums[i] is either 0, 1, or 2.',
            'follow_up': 'Can you solve it without using extra space and in one pass?',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'sortColors',
            'signature_text': 'def sortColors(self, nums: list[int]) -> None',
            'starter_code': 'class Solution:\n    def sortColors(self, nums: list[int]) -> None:\n        """\n        Do not return anything, modify nums in-place instead.\n        """\n        pass',
            'tags': ['Arrays', 'Sorting', 'Two Pointers'],
            'test_cases': [
                {'input': '{"nums": [2,0,2,1,1,0]}', 'output': '[0,0,1,1,2,2]', 'display_in': 'nums = [2,0,2,1,1,0]', 'display_out': '[0,0,1,1,2,2]', 'is_sample': True},
                {'input': '{"nums": [2,0,1]}', 'output': '[0,1,2]', 'display_in': 'nums = [2,0,1]', 'display_out': '[0,1,2]', 'is_sample': True},
                {'input': '{"nums": [0]}', 'output': '[0]', 'is_sample': False},
                {'input': '{"nums": [1,2,0]}', 'output': '[0,1,2]', 'is_sample': False},
            ]
        },
        # ============ MORE STDIN/STDOUT PROBLEMS ============
        {
            'title': 'Reverse Words',
            'slug': 'reverse-words',
            'description': '''Given a sentence (a string of words separated by single spaces), reverse the order of the words.

Input: A single line containing a sentence.
Output: The sentence with words in reverse order.''',
            'constraints': '1 <= number of words <= 100\n1 <= length of each word <= 100\nWords are separated by single spaces.',
            'difficulty': 1,
            'judge_mode': 'stdin',
            'tags': ['Strings'],
            'test_cases': [
                {'input': 'hello world', 'output': 'world hello', 'display_in': 'hello world', 'display_out': 'world hello', 'is_sample': True},
                {'input': 'the sky is blue', 'output': 'blue is sky the', 'display_in': 'the sky is blue', 'display_out': 'blue is sky the', 'is_sample': True},
                {'input': 'a', 'output': 'a', 'is_sample': False},
                {'input': 'Bob Loves Alice', 'output': 'Alice Loves Bob', 'is_sample': False},
            ]
        },
        {
            'title': 'Pascal Triangle Row',
            'slug': 'pascal-triangle-row',
            'description': '''Given a row number n (0-indexed), return the nth row of Pascal\'s triangle.

Pascal\'s triangle starts with 1 at the top. Each number in a row is the sum of the two numbers directly above it.

Row 0: 1
Row 1: 1 1
Row 2: 1 2 1
Row 3: 1 3 3 1
Row 4: 1 4 6 4 1

Output the numbers in the row, space-separated.''',
            'constraints': '0 <= n <= 33',
            'difficulty': 1,
            'judge_mode': 'stdin',
            'tags': ['Arrays', 'Dynamic Programming'],
            'test_cases': [
                {'input': '3', 'output': '1 3 3 1', 'display_in': '3', 'display_out': '1 3 3 1', 'is_sample': True},
                {'input': '0', 'output': '1', 'display_in': '0', 'display_out': '1', 'is_sample': True},
                {'input': '1', 'output': '1 1', 'display_in': '1', 'display_out': '1 1', 'is_sample': True},
                {'input': '4', 'output': '1 4 6 4 1', 'is_sample': False},
                {'input': '5', 'output': '1 5 10 10 5 1', 'is_sample': False},
            ]
        },
        {
            'title': 'GCD of Two Numbers',
            'slug': 'gcd-of-two-numbers',
            'description': '''Given two positive integers a and b, find their Greatest Common Divisor (GCD).

The GCD of two numbers is the largest positive integer that divides both numbers without leaving a remainder.

Input: Two space-separated integers a and b.
Output: Their GCD.''',
            'constraints': '1 <= a, b <= 10^9',
            'follow_up': 'Can you solve this efficiently using the Euclidean algorithm?',
            'difficulty': 1,
            'judge_mode': 'stdin',
            'tags': ['Math', 'Recursion'],
            'test_cases': [
                {'input': '12 18', 'output': '6', 'display_in': '12 18', 'display_out': '6', 'is_sample': True},
                {'input': '7 11', 'output': '1', 'display_in': '7 11', 'display_out': '1', 'is_sample': True, 'explanation': '7 and 11 are coprime.'},
                {'input': '100 25', 'output': '25', 'display_in': '100 25', 'display_out': '25', 'is_sample': True},
                {'input': '1 1', 'output': '1', 'is_sample': False},
                {'input': '1000000000 999999999', 'output': '1', 'is_sample': False},
            ]
        },
    ]

    for pdata in problems_data:
        # Skip if problem already exists
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

        # Add tags
        for tag_name in pdata.get('tags', []):
            tag = get_tag(tag_name)
            if tag:
                problem.tags.add(tag)

        # Add test cases
        for tc in pdata['test_cases']:
            TestCase.objects.create(
                problem=problem,
                input_data=tc['input'],
                expected_output=tc['output'],
                display_input=tc.get('display_in', ''),
                display_output=tc.get('display_out', ''),
                explanation=tc.get('explanation', ''),
                is_sample=tc['is_sample'],
            )


def remove_problems(apps, schema_editor):
    Problem = apps.get_model('problems', 'Problem')
    slugs = [
        'rotate-image', 'spiral-matrix', 'set-matrix-zeroes',
        'min-stack', 'daily-temperatures',
        'maximum-average-subarray-i', 'minimum-size-subarray-sum',
        'jump-game', 'best-time-to-buy-and-sell-stock-ii',
        'single-number', 'number-of-1-bits', 'counting-bits',
        'subsets', 'permutations', 'combination-sum',
        'climbing-stairs', 'house-robber', 'coin-change', 'unique-paths',
        'merge-sorted-array', 'sort-colors',
        'reverse-words', 'pascal-triangle-row', 'gcd-of-two-numbers',
    ]
    Problem.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0008_add_more_problems'),
    ]

    operations = [
        migrations.RunPython(add_tags_and_problems, remove_problems),
    ]
