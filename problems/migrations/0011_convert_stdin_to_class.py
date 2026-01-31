# Convert stdin problems to class-based function-call mode

from django.db import migrations
import json


def convert_to_class_based(apps, schema_editor):
    Problem = apps.get_model('problems', 'Problem')
    TestCase = apps.get_model('problems', 'TestCase')

    # Define conversions for each stdin problem
    conversions = {
        'sum-of-two-numbers': {
            'entrypoint_name': 'addTwoNumbers',
            'signature_text': 'def addTwoNumbers(self, a: int, b: int) -> int',
            'starter_code': '''class Solution:
    def addTwoNumbers(self, a: int, b: int) -> int:
        pass''',
            'convert_test': lambda inp, out: (
                json.dumps({'a': int(inp.split()[0]), 'b': int(inp.split()[1])}),
                out
            ),
            'convert_display': lambda inp: f'a = {inp.split()[0]}, b = {inp.split()[1]}',
        },
        'count-vowels': {
            'entrypoint_name': 'countVowels',
            'signature_text': 'def countVowels(self, s: str) -> int',
            'starter_code': '''class Solution:
    def countVowels(self, s: str) -> int:
        pass''',
            'convert_test': lambda inp, out: (
                json.dumps({'s': inp}),
                out
            ),
            'convert_display': lambda inp: f's = "{inp}"',
        },
        'fibonacci-number': {
            'entrypoint_name': 'fib',
            'signature_text': 'def fib(self, n: int) -> int',
            'starter_code': '''class Solution:
    def fib(self, n: int) -> int:
        pass''',
            'convert_test': lambda inp, out: (
                json.dumps({'n': int(inp)}),
                out
            ),
            'convert_display': lambda inp: f'n = {inp}',
        },
        'prime-check': {
            'entrypoint_name': 'isPrime',
            'signature_text': 'def isPrime(self, n: int) -> bool',
            'starter_code': '''class Solution:
    def isPrime(self, n: int) -> bool:
        pass''',
            'convert_test': lambda inp, out: (
                json.dumps({'n': int(inp)}),
                'true' if out == 'YES' else 'false'
            ),
            'convert_display': lambda inp: f'n = {inp}',
        },
        'array-statistics': {
            'entrypoint_name': 'getStatistics',
            'signature_text': 'def getStatistics(self, nums: list[int]) -> list[int]',
            'starter_code': '''class Solution:
    def getStatistics(self, nums: list[int]) -> list[int]:
        """
        Return [sum, min, max] of the array.
        """
        pass''',
            'convert_test': lambda inp, out: (
                json.dumps({'nums': list(map(int, inp.split('\n')[1].split()))}),
                json.dumps(list(map(int, out.split('\n'))))
            ),
            'convert_display': lambda inp: f'nums = {list(map(int, inp.split(chr(10))[1].split()))}',
        },
    }

    for slug, config in conversions.items():
        try:
            problem = Problem.objects.get(slug=slug)
        except Problem.DoesNotExist:
            continue

        # Update problem
        problem.judge_mode = 'function'
        problem.entrypoint_type = 'class'
        problem.entrypoint_name = config['entrypoint_name']
        problem.signature_text = config['signature_text']
        problem.starter_code = config['starter_code']
        problem.save()

        # Update test cases
        for tc in TestCase.objects.filter(problem=problem):
            try:
                new_input, new_output = config['convert_test'](tc.input_data, tc.expected_output)
                tc.input_data = new_input
                tc.expected_output = new_output
                if tc.display_input:
                    tc.display_input = config['convert_display'](tc.display_input)
                if tc.display_output and slug == 'prime-check':
                    tc.display_output = 'true' if tc.display_output == 'YES' else 'false'
                tc.save()
            except Exception:
                # Skip if conversion fails
                pass


def reverse_conversion(apps, schema_editor):
    # This is a data migration, we don't reverse it
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0010_initial'),
    ]

    operations = [
        migrations.RunPython(convert_to_class_based, reverse_conversion),
    ]
