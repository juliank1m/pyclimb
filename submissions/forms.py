from django import forms
from .models import Submission


# Default code template for stdin/stdout mode
DEFAULT_STDIN_TEMPLATE = '''# Read input using input()
# Print output using print()

# Example:
# n = int(input())
# nums = list(map(int, input().split()))
# ... your solution ...
# print(result)

'''

# Default code template for function-call mode (Solution class)
DEFAULT_FUNCTION_CLASS_TEMPLATE = '''class Solution:
    def {method_name}(self{params}):
        # Your solution here
        pass
'''

# Default code template for function-call mode (bare function)
DEFAULT_FUNCTION_BARE_TEMPLATE = '''def {function_name}({params}):
    # Your solution here
    pass
'''


class SubmissionForm(forms.ModelForm):
    """Form for submitting code to a problem."""

    class Meta:
        model = Submission
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={
                'rows': 20,
                'spellcheck': 'false',
                'style': 'font-family: monospace; font-size: 14px;',
            })
        }

    def __init__(self, *args, problem=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial code value based on problem configuration
        if not self.initial.get('code') and not (args and args[0]):
            self.initial['code'] = self._get_starter_code(problem)

    def _get_starter_code(self, problem):
        """Get appropriate starter code for the problem."""
        if problem is None:
            return DEFAULT_STDIN_TEMPLATE
        
        # Use problem's custom starter code if provided
        if problem.starter_code:
            return problem.starter_code
        
        # Generate default template based on judge mode
        if problem.judge_mode == 'function':
            if problem.entrypoint_type == 'class':
                return DEFAULT_FUNCTION_CLASS_TEMPLATE.format(
                    method_name=problem.entrypoint_name or 'solve',
                    params=''
                )
            else:
                return DEFAULT_FUNCTION_BARE_TEMPLATE.format(
                    function_name=problem.entrypoint_name or 'solve',
                    params=''
                )
        else:
            return DEFAULT_STDIN_TEMPLATE

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        if not code:
            raise forms.ValidationError('Code cannot be empty.')
        if len(code) > 50000:  # 50KB limit
            raise forms.ValidationError('Code exceeds maximum length (50,000 characters).')
        return code
