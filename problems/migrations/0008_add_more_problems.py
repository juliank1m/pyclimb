# Data migration to add variety of problems

from django.db import migrations
import json


def add_problems(apps, schema_editor):
    Problem = apps.get_model('problems', 'Problem')
    TestCase = apps.get_model('problems', 'TestCase')
    Tag = apps.get_model('problems', 'Tag')

    # Get or create tags
    def get_tag(name):
        tag, _ = Tag.objects.get_or_create(name=name)
        return tag

    problems_data = [
        # ============ EASY PROBLEMS ============
        {
            'title': 'Reverse String',
            'slug': 'reverse-string',
            'description': 'Write a function that reverses a string.\n\nThe input string is given as a list of characters. You must do this by modifying the input list in-place with O(1) extra memory.',
            'constraints': '1 <= s.length <= 10^5\ns[i] is a printable ASCII character.',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'reverseString',
            'signature_text': 'def reverseString(self, s: list[str]) -> None',
            'starter_code': 'class Solution:\n    def reverseString(self, s: list[str]) -> None:\n        """\n        Do not return anything, modify s in-place instead.\n        """\n        pass',
            'tags': ['Strings', 'Two Pointers'],
            'test_cases': [
                {'input': '{"s": ["h","e","l","l","o"]}', 'output': '["o","l","l","e","h"]', 'display_in': 's = ["h","e","l","l","o"]', 'display_out': '["o","l","l","e","h"]', 'is_sample': True, 'explanation': 'The string "hello" reversed is "olleh".'},
                {'input': '{"s": ["H","a","n","n","a","h"]}', 'output': '["h","a","n","n","a","H"]', 'display_in': 's = ["H","a","n","n","a","h"]', 'display_out': '["h","a","n","n","a","H"]', 'is_sample': True},
                {'input': '{"s": ["a"]}', 'output': '["a"]', 'is_sample': False},
                {'input': '{"s": ["a","b"]}', 'output': '["b","a"]', 'is_sample': False},
            ]
        },
        {
            'title': 'Valid Parentheses',
            'slug': 'valid-parentheses',
            'description': 'Given a string s containing just the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\', determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.',
            'constraints': '1 <= s.length <= 10^4\ns consists of parentheses only \'()[]{}\'.',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'isValid',
            'signature_text': 'def isValid(self, s: str) -> bool',
            'starter_code': 'class Solution:\n    def isValid(self, s: str) -> bool:\n        pass',
            'tags': ['Strings', 'Hashing'],
            'test_cases': [
                {'input': '{"s": "()"}', 'output': 'true', 'display_in': 's = "()"', 'display_out': 'true', 'is_sample': True},
                {'input': '{"s": "()[]{}"}', 'output': 'true', 'display_in': 's = "()[]{}"', 'display_out': 'true', 'is_sample': True},
                {'input': '{"s": "(]"}', 'output': 'false', 'display_in': 's = "(]"', 'display_out': 'false', 'is_sample': True},
                {'input': '{"s": "([)]"}', 'output': 'false', 'is_sample': False},
                {'input': '{"s": "{[]}"}', 'output': 'true', 'is_sample': False},
                {'input': '{"s": "(((())))"}', 'output': 'true', 'is_sample': False},
            ]
        },
        {
            'title': 'FizzBuzz',
            'slug': 'fizzbuzz',
            'description': 'Given an integer n, return a string array answer (1-indexed) where:\n\n- answer[i] == "FizzBuzz" if i is divisible by 3 and 5.\n- answer[i] == "Fizz" if i is divisible by 3.\n- answer[i] == "Buzz" if i is divisible by 5.\n- answer[i] == i (as a string) if none of the above conditions are true.',
            'constraints': '1 <= n <= 10^4',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'fizzBuzz',
            'signature_text': 'def fizzBuzz(self, n: int) -> list[str]',
            'starter_code': 'class Solution:\n    def fizzBuzz(self, n: int) -> list[str]:\n        pass',
            'tags': ['Arrays'],
            'test_cases': [
                {'input': '{"n": 3}', 'output': '["1","2","Fizz"]', 'display_in': 'n = 3', 'display_out': '["1","2","Fizz"]', 'is_sample': True},
                {'input': '{"n": 5}', 'output': '["1","2","Fizz","4","Buzz"]', 'display_in': 'n = 5', 'display_out': '["1","2","Fizz","4","Buzz"]', 'is_sample': True},
                {'input': '{"n": 15}', 'output': '["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]', 'display_in': 'n = 15', 'display_out': '["1","2","Fizz","4","Buzz",...,"FizzBuzz"]', 'is_sample': True},
                {'input': '{"n": 1}', 'output': '["1"]', 'is_sample': False},
            ]
        },
        {
            'title': 'Maximum Subarray',
            'slug': 'maximum-subarray',
            'description': 'Given an integer array nums, find the subarray with the largest sum, and return its sum.\n\nA subarray is a contiguous non-empty sequence of elements within an array.',
            'constraints': '1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4',
            'follow_up': 'If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'maxSubArray',
            'signature_text': 'def maxSubArray(self, nums: list[int]) -> int',
            'starter_code': 'class Solution:\n    def maxSubArray(self, nums: list[int]) -> int:\n        pass',
            'tags': ['Arrays', 'Dynamic Programming'],
            'test_cases': [
                {'input': '{"nums": [-2,1,-3,4,-1,2,1,-5,4]}', 'output': '6', 'display_in': 'nums = [-2,1,-3,4,-1,2,1,-5,4]', 'display_out': '6', 'is_sample': True, 'explanation': 'The subarray [4,-1,2,1] has the largest sum 6.'},
                {'input': '{"nums": [1]}', 'output': '1', 'display_in': 'nums = [1]', 'display_out': '1', 'is_sample': True},
                {'input': '{"nums": [5,4,-1,7,8]}', 'output': '23', 'display_in': 'nums = [5,4,-1,7,8]', 'display_out': '23', 'is_sample': True},
                {'input': '{"nums": [-1]}', 'output': '-1', 'is_sample': False},
                {'input': '{"nums": [-2,-1]}', 'output': '-1', 'is_sample': False},
            ]
        },
        {
            'title': 'Palindrome Number',
            'slug': 'palindrome-number',
            'description': 'Given an integer x, return true if x is a palindrome, and false otherwise.\n\nAn integer is a palindrome when it reads the same forward and backward.',
            'constraints': '-2^31 <= x <= 2^31 - 1',
            'follow_up': 'Could you solve it without converting the integer to a string?',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'isPalindrome',
            'signature_text': 'def isPalindrome(self, x: int) -> bool',
            'starter_code': 'class Solution:\n    def isPalindrome(self, x: int) -> bool:\n        pass',
            'tags': [],
            'test_cases': [
                {'input': '{"x": 121}', 'output': 'true', 'display_in': 'x = 121', 'display_out': 'true', 'is_sample': True, 'explanation': '121 reads as 121 from left to right and from right to left.'},
                {'input': '{"x": -121}', 'output': 'false', 'display_in': 'x = -121', 'display_out': 'false', 'is_sample': True, 'explanation': 'From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.'},
                {'input': '{"x": 10}', 'output': 'false', 'display_in': 'x = 10', 'display_out': 'false', 'is_sample': True},
                {'input': '{"x": 0}', 'output': 'true', 'is_sample': False},
                {'input': '{"x": 12321}', 'output': 'true', 'is_sample': False},
            ]
        },
        # ============ MEDIUM PROBLEMS ============
        {
            'title': 'Container With Most Water',
            'slug': 'container-with-most-water',
            'description': 'You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).\n\nFind two lines that together with the x-axis form a container, such that the container contains the most water.\n\nReturn the maximum amount of water a container can store.\n\nNotice that you may not slant the container.',
            'constraints': 'n == height.length\n2 <= n <= 10^5\n0 <= height[i] <= 10^4',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'maxArea',
            'signature_text': 'def maxArea(self, height: list[int]) -> int',
            'starter_code': 'class Solution:\n    def maxArea(self, height: list[int]) -> int:\n        pass',
            'tags': ['Arrays', 'Two Pointers'],
            'test_cases': [
                {'input': '{"height": [1,8,6,2,5,4,8,3,7]}', 'output': '49', 'display_in': 'height = [1,8,6,2,5,4,8,3,7]', 'display_out': '49', 'is_sample': True, 'explanation': 'The max area is between index 1 and 8, with height min(8,7)=7 and width 7, giving 49.'},
                {'input': '{"height": [1,1]}', 'output': '1', 'display_in': 'height = [1,1]', 'display_out': '1', 'is_sample': True},
                {'input': '{"height": [4,3,2,1,4]}', 'output': '16', 'is_sample': False},
                {'input': '{"height": [1,2,1]}', 'output': '2', 'is_sample': False},
            ]
        },
        {
            'title': 'Longest Substring Without Repeating Characters',
            'slug': 'longest-substring-without-repeating',
            'description': 'Given a string s, find the length of the longest substring without repeating characters.',
            'constraints': '0 <= s.length <= 5 * 10^4\ns consists of English letters, digits, symbols and spaces.',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'lengthOfLongestSubstring',
            'signature_text': 'def lengthOfLongestSubstring(self, s: str) -> int',
            'starter_code': 'class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        pass',
            'tags': ['Strings', 'Hashing', 'Two Pointers'],
            'test_cases': [
                {'input': '{"s": "abcabcbb"}', 'output': '3', 'display_in': 's = "abcabcbb"', 'display_out': '3', 'is_sample': True, 'explanation': 'The answer is "abc", with the length of 3.'},
                {'input': '{"s": "bbbbb"}', 'output': '1', 'display_in': 's = "bbbbb"', 'display_out': '1', 'is_sample': True, 'explanation': 'The answer is "b", with the length of 1.'},
                {'input': '{"s": "pwwkew"}', 'output': '3', 'display_in': 's = "pwwkew"', 'display_out': '3', 'is_sample': True, 'explanation': 'The answer is "wke", with the length of 3.'},
                {'input': '{"s": ""}', 'output': '0', 'is_sample': False},
                {'input': '{"s": " "}', 'output': '1', 'is_sample': False},
                {'input': '{"s": "dvdf"}', 'output': '3', 'is_sample': False},
            ]
        },
        {
            'title': 'Group Anagrams',
            'slug': 'group-anagrams',
            'description': 'Given an array of strings strs, group the anagrams together. You can return the answer in any order.\n\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.',
            'constraints': '1 <= strs.length <= 10^4\n0 <= strs[i].length <= 100\nstrs[i] consists of lowercase English letters.',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'groupAnagrams',
            'signature_text': 'def groupAnagrams(self, strs: list[str]) -> list[list[str]]',
            'starter_code': 'class Solution:\n    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:\n        pass',
            'tags': ['Strings', 'Hashing', 'Arrays'],
            'test_cases': [
                {'input': '{"strs": ["eat","tea","tan","ate","nat","bat"]}', 'output': '[["bat"],["nat","tan"],["ate","eat","tea"]]', 'display_in': 'strs = ["eat","tea","tan","ate","nat","bat"]', 'display_out': '[["bat"],["nat","tan"],["ate","eat","tea"]]', 'is_sample': True},
                {'input': '{"strs": [""]}', 'output': '[[""]]', 'display_in': 'strs = [""]', 'display_out': '[[""]]', 'is_sample': True},
                {'input': '{"strs": ["a"]}', 'output': '[["a"]]', 'display_in': 'strs = ["a"]', 'display_out': '[["a"]]', 'is_sample': True},
            ]
        },
        {
            'title': 'Product of Array Except Self',
            'slug': 'product-of-array-except-self',
            'description': 'Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].\n\nThe product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.\n\nYou must write an algorithm that runs in O(n) time and without using the division operation.',
            'constraints': '2 <= nums.length <= 10^5\n-30 <= nums[i] <= 30\nThe product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.',
            'follow_up': 'Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)',
            'difficulty': 2,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'productExceptSelf',
            'signature_text': 'def productExceptSelf(self, nums: list[int]) -> list[int]',
            'starter_code': 'class Solution:\n    def productExceptSelf(self, nums: list[int]) -> list[int]:\n        pass',
            'tags': ['Arrays'],
            'test_cases': [
                {'input': '{"nums": [1,2,3,4]}', 'output': '[24,12,8,6]', 'display_in': 'nums = [1,2,3,4]', 'display_out': '[24,12,8,6]', 'is_sample': True},
                {'input': '{"nums": [-1,1,0,-3,3]}', 'output': '[0,0,9,0,0]', 'display_in': 'nums = [-1,1,0,-3,3]', 'display_out': '[0,0,9,0,0]', 'is_sample': True},
                {'input': '{"nums": [2,3]}', 'output': '[3,2]', 'is_sample': False},
            ]
        },
        {
            'title': 'Binary Search',
            'slug': 'binary-search',
            'description': 'Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.\n\nYou must write an algorithm with O(log n) runtime complexity.',
            'constraints': '1 <= nums.length <= 10^4\n-10^4 < nums[i], target < 10^4\nAll the integers in nums are unique.\nnums is sorted in ascending order.',
            'difficulty': 1,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'search',
            'signature_text': 'def search(self, nums: list[int], target: int) -> int',
            'starter_code': 'class Solution:\n    def search(self, nums: list[int], target: int) -> int:\n        pass',
            'tags': ['Arrays', 'Binary Search'],
            'test_cases': [
                {'input': '{"nums": [-1,0,3,5,9,12], "target": 9}', 'output': '4', 'display_in': 'nums = [-1,0,3,5,9,12], target = 9', 'display_out': '4', 'is_sample': True},
                {'input': '{"nums": [-1,0,3,5,9,12], "target": 2}', 'output': '-1', 'display_in': 'nums = [-1,0,3,5,9,12], target = 2', 'display_out': '-1', 'is_sample': True},
                {'input': '{"nums": [5], "target": 5}', 'output': '0', 'is_sample': False},
                {'input': '{"nums": [2,5], "target": 5}', 'output': '1', 'is_sample': False},
            ]
        },
        # ============ HARD PROBLEMS ============
        {
            'title': 'Merge k Sorted Lists',
            'slug': 'merge-k-sorted-lists',
            'description': 'You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.\n\nMerge all the linked-lists into one sorted linked-list and return it.\n\nFor this problem, linked lists are represented as arrays. Return the merged result as an array.',
            'constraints': 'k == lists.length\n0 <= k <= 10^4\n0 <= lists[i].length <= 500\n-10^4 <= lists[i][j] <= 10^4\nlists[i] is sorted in ascending order.\nThe sum of lists[i].length will not exceed 10^4.',
            'difficulty': 3,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'mergeKLists',
            'signature_text': 'def mergeKLists(self, lists: list[list[int]]) -> list[int]',
            'starter_code': 'class Solution:\n    def mergeKLists(self, lists: list[list[int]]) -> list[int]:\n        # Lists are represented as arrays for simplicity\n        pass',
            'tags': ['Arrays', 'Linked Lists'],
            'test_cases': [
                {'input': '{"lists": [[1,4,5],[1,3,4],[2,6]]}', 'output': '[1,1,2,3,4,4,5,6]', 'display_in': 'lists = [[1,4,5],[1,3,4],[2,6]]', 'display_out': '[1,1,2,3,4,4,5,6]', 'is_sample': True},
                {'input': '{"lists": []}', 'output': '[]', 'display_in': 'lists = []', 'display_out': '[]', 'is_sample': True},
                {'input': '{"lists": [[]]}', 'output': '[]', 'display_in': 'lists = [[]]', 'display_out': '[]', 'is_sample': True},
                {'input': '{"lists": [[1],[2],[3]]}', 'output': '[1,2,3]', 'is_sample': False},
            ]
        },
        {
            'title': 'Trapping Rain Water',
            'slug': 'trapping-rain-water',
            'description': 'Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.',
            'constraints': 'n == height.length\n1 <= n <= 2 * 10^4\n0 <= height[i] <= 10^5',
            'difficulty': 3,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'trap',
            'signature_text': 'def trap(self, height: list[int]) -> int',
            'starter_code': 'class Solution:\n    def trap(self, height: list[int]) -> int:\n        pass',
            'tags': ['Arrays', 'Two Pointers', 'Dynamic Programming'],
            'test_cases': [
                {'input': '{"height": [0,1,0,2,1,0,1,3,2,1,2,1]}', 'output': '6', 'display_in': 'height = [0,1,0,2,1,0,1,3,2,1,2,1]', 'display_out': '6', 'is_sample': True, 'explanation': '6 units of rain water are trapped.'},
                {'input': '{"height": [4,2,0,3,2,5]}', 'output': '9', 'display_in': 'height = [4,2,0,3,2,5]', 'display_out': '9', 'is_sample': True},
                {'input': '{"height": [1,2,3,4,5]}', 'output': '0', 'is_sample': False},
                {'input': '{"height": [5,4,3,2,1]}', 'output': '0', 'is_sample': False},
            ]
        },
        {
            'title': 'Longest Valid Parentheses',
            'slug': 'longest-valid-parentheses',
            'description': 'Given a string containing just the characters \'(\' and \')\', return the length of the longest valid (well-formed) parentheses substring.',
            'constraints': '0 <= s.length <= 3 * 10^4\ns[i] is \'(\' or \')\'.',
            'difficulty': 3,
            'judge_mode': 'function',
            'entrypoint_type': 'class',
            'entrypoint_name': 'longestValidParentheses',
            'signature_text': 'def longestValidParentheses(self, s: str) -> int',
            'starter_code': 'class Solution:\n    def longestValidParentheses(self, s: str) -> int:\n        pass',
            'tags': ['Strings', 'Dynamic Programming'],
            'test_cases': [
                {'input': '{"s": "(()"}', 'output': '2', 'display_in': 's = "(()"', 'display_out': '2', 'is_sample': True, 'explanation': 'The longest valid parentheses substring is "()".'},
                {'input': '{"s": ")()())"}', 'output': '4', 'display_in': 's = ")()())"', 'display_out': '4', 'is_sample': True, 'explanation': 'The longest valid parentheses substring is "()()".'},
                {'input': '{"s": ""}', 'output': '0', 'display_in': 's = ""', 'display_out': '0', 'is_sample': True},
                {'input': '{"s": "()(()"}', 'output': '2', 'is_sample': False},
                {'input': '{"s": "(()())"}', 'output': '6', 'is_sample': False},
            ]
        },
        # ============ STDIN/STDOUT PROBLEMS ============
        {
            'title': 'Sum of Two Numbers',
            'slug': 'sum-of-two-numbers',
            'description': 'Given two integers on a single line separated by a space, output their sum.',
            'constraints': '-10^9 <= a, b <= 10^9',
            'difficulty': 1,
            'judge_mode': 'stdin',
            'tags': [],
            'test_cases': [
                {'input': '3 5', 'output': '8', 'display_in': '3 5', 'display_out': '8', 'is_sample': True},
                {'input': '-1 1', 'output': '0', 'display_in': '-1 1', 'display_out': '0', 'is_sample': True},
                {'input': '100 200', 'output': '300', 'is_sample': False},
                {'input': '-500 -300', 'output': '-800', 'is_sample': False},
            ]
        },
        {
            'title': 'Count Vowels',
            'slug': 'count-vowels',
            'description': 'Given a string, count the number of vowels (a, e, i, o, u) in it. Consider both uppercase and lowercase vowels.',
            'constraints': '1 <= len(s) <= 1000\nThe string contains only ASCII characters.',
            'difficulty': 1,
            'judge_mode': 'stdin',
            'tags': ['Strings'],
            'test_cases': [
                {'input': 'hello', 'output': '2', 'display_in': 'hello', 'display_out': '2', 'is_sample': True, 'explanation': 'The vowels are: e, o'},
                {'input': 'AEIOU', 'output': '5', 'display_in': 'AEIOU', 'display_out': '5', 'is_sample': True},
                {'input': 'rhythm', 'output': '0', 'display_in': 'rhythm', 'display_out': '0', 'is_sample': True},
                {'input': 'Programming', 'output': '3', 'is_sample': False},
            ]
        },
        {
            'title': 'Fibonacci Number',
            'slug': 'fibonacci-number',
            'description': 'Given an integer n, output the nth Fibonacci number.\n\nThe Fibonacci sequence is: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...\n\nwhere F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2) for n > 1.',
            'constraints': '0 <= n <= 30',
            'difficulty': 1,
            'judge_mode': 'stdin',
            'tags': ['Recursion', 'Dynamic Programming'],
            'test_cases': [
                {'input': '0', 'output': '0', 'display_in': '0', 'display_out': '0', 'is_sample': True},
                {'input': '1', 'output': '1', 'display_in': '1', 'display_out': '1', 'is_sample': True},
                {'input': '10', 'output': '55', 'display_in': '10', 'display_out': '55', 'is_sample': True},
                {'input': '20', 'output': '6765', 'is_sample': False},
                {'input': '30', 'output': '832040', 'is_sample': False},
            ]
        },
        {
            'title': 'Prime Check',
            'slug': 'prime-check',
            'description': 'Given an integer n, determine if it is a prime number. Output "YES" if it is prime, "NO" otherwise.\n\nA prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.',
            'constraints': '1 <= n <= 10^6',
            'difficulty': 1,
            'judge_mode': 'stdin',
            'tags': [],
            'test_cases': [
                {'input': '7', 'output': 'YES', 'display_in': '7', 'display_out': 'YES', 'is_sample': True},
                {'input': '4', 'output': 'NO', 'display_in': '4', 'display_out': 'NO', 'is_sample': True},
                {'input': '1', 'output': 'NO', 'display_in': '1', 'display_out': 'NO', 'is_sample': True},
                {'input': '2', 'output': 'YES', 'is_sample': False},
                {'input': '97', 'output': 'YES', 'is_sample': False},
                {'input': '100', 'output': 'NO', 'is_sample': False},
            ]
        },
        {
            'title': 'Array Statistics',
            'slug': 'array-statistics',
            'description': 'Given an array of integers, output three values on separate lines:\n1. The sum of all elements\n2. The minimum element\n3. The maximum element\n\nInput format:\n- First line: n (number of elements)\n- Second line: n space-separated integers',
            'constraints': '1 <= n <= 1000\n-10^6 <= arr[i] <= 10^6',
            'difficulty': 1,
            'judge_mode': 'stdin',
            'tags': ['Arrays'],
            'test_cases': [
                {'input': '5\n1 2 3 4 5', 'output': '15\n1\n5', 'display_in': '5\n1 2 3 4 5', 'display_out': '15\n1\n5', 'is_sample': True},
                {'input': '3\n-5 0 5', 'output': '0\n-5\n5', 'display_in': '3\n-5 0 5', 'display_out': '0\n-5\n5', 'is_sample': True},
                {'input': '1\n42', 'output': '42\n42\n42', 'is_sample': False},
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
            try:
                tag = Tag.objects.get(name=tag_name)
                problem.tags.add(tag)
            except Tag.DoesNotExist:
                pass

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
        'reverse-string', 'valid-parentheses', 'fizzbuzz', 'maximum-subarray',
        'palindrome-number', 'container-with-most-water', 
        'longest-substring-without-repeating', 'group-anagrams',
        'product-of-array-except-self', 'binary-search', 'merge-k-sorted-lists',
        'trapping-rain-water', 'longest-valid-parentheses', 'sum-of-two-numbers',
        'count-vowels', 'fibonacci-number', 'prime-check', 'array-statistics',
    ]
    Problem.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0007_add_tags'),
    ]

    operations = [
        migrations.RunPython(add_problems, remove_problems),
    ]
