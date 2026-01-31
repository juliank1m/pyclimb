# Convert remaining stdin problems to class-based function-call mode

from django.db import migrations
import json


def convert_to_class_based(apps, schema_editor):
    Problem = apps.get_model('problems', 'Problem')
    TestCase = apps.get_model('problems', 'TestCase')

    # Define conversions for each remaining stdin problem
    conversions = {
        'reverse-words': {
            'entrypoint_name': 'reverseWords',
            'signature_text': 'def reverseWords(self, s: str) -> str',
            'starter_code': '''class Solution:
    def reverseWords(self, s: str) -> str:
        """
        Given a sentence, reverse the order of words.
        """
        pass''',
            'convert_test': lambda inp, out: (
                json.dumps({'s': inp}),
                json.dumps(out)
            ),
            'convert_display': lambda inp: f's = "{inp}"',
        },
        'pascal-triangle-row': {
            'entrypoint_name': 'getRow',
            'signature_text': 'def getRow(self, rowIndex: int) -> list[int]',
            'starter_code': '''class Solution:
    def getRow(self, rowIndex: int) -> list[int]:
        """
        Return the rowIndex-th (0-indexed) row of Pascal's triangle.
        """
        pass''',
            'convert_test': lambda inp, out: (
                json.dumps({'rowIndex': int(inp)}),
                json.dumps([int(x) for x in out.split()])
            ),
            'convert_display': lambda inp: f'rowIndex = {inp}',
            'convert_display_out': lambda out: str([int(x) for x in out.split()]),
        },
        'gcd-of-two-numbers': {
            'entrypoint_name': 'gcd',
            'signature_text': 'def gcd(self, a: int, b: int) -> int',
            'starter_code': '''class Solution:
    def gcd(self, a: int, b: int) -> int:
        """
        Return the Greatest Common Divisor of a and b.
        """
        pass''',
            'convert_test': lambda inp, out: (
                json.dumps({'a': int(inp.split()[0]), 'b': int(inp.split()[1])}),
                out
            ),
            'convert_display': lambda inp: f'a = {inp.split()[0]}, b = {inp.split()[1]}',
        },
        'fizzbuzz': {
            'entrypoint_name': 'fizzBuzz',
            'signature_text': 'def fizzBuzz(self, n: int) -> list[str]',
            'starter_code': '''class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        """
        Return a list of strings from 1 to n following FizzBuzz rules.
        """
        pass''',
            'convert_test': lambda inp, out: (
                json.dumps({'n': int(inp)}),
                json.dumps(out.split('\n'))
            ),
            'convert_display': lambda inp: f'n = {inp}',
            'convert_display_out': lambda out: str(out.split('\n')[:5]) + '...' if len(out.split('\n')) > 5 else str(out.split('\n')),
        },
    }

    for slug, config in conversions.items():
        try:
            problem = Problem.objects.get(slug=slug)
        except Problem.DoesNotExist:
            continue

        # Skip if already converted
        if problem.judge_mode == 'function':
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
                    tc.display_input = config['convert_display'](tc.display_input.split(' = ')[-1] if ' = ' in tc.display_input else tc.display_input)
                if tc.display_output and 'convert_display_out' in config:
                    tc.display_output = config['convert_display_out'](tc.display_output)
                elif tc.display_output:
                    # Keep as JSON output
                    tc.display_output = new_output
                tc.save()
            except Exception:
                # Skip if conversion fails
                pass


def reverse_conversion(apps, schema_editor):
    # This is a data migration, we don't reverse it
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0011_convert_stdin_to_class'),
    ]

    operations = [
        migrations.RunPython(convert_to_class_based, reverse_conversion),
    ]
