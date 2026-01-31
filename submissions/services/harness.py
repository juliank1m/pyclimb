"""
Harness templates for function-call mode execution.

These templates are written to the temp directory and executed
in a subprocess to safely run user code.
"""

# Template for Solution class (LeetCode default style)
# Placeholders: {method_name}
SOLUTION_CLASS_HARNESS = '''
import json
import sys

try:
    from submission import Solution
except SyntaxError as e:
    print(json.dumps({{"error": "syntax", "message": str(e), "lineno": e.lineno}}))
    sys.exit(1)
except Exception as e:
    print(json.dumps({{"error": "import", "message": str(e)}}))
    sys.exit(1)

try:
    with open("input.json", "r") as f:
        args = json.load(f)
    
    solution = Solution()
    method = getattr(solution, "{method_name}")
    
    if isinstance(args, dict):
        result = method(**args)
    else:
        result = method(*args)
    
    print(json.dumps({{"ok": True, "result": result}}))
except Exception as e:
    import traceback
    print(json.dumps({{
        "error": "runtime",
        "message": str(e),
        "traceback": traceback.format_exc()
    }}))
    sys.exit(1)
'''

# Template for bare function style
# Placeholders: {function_name}
FUNCTION_HARNESS = '''
import json
import sys

try:
    from submission import {function_name}
except SyntaxError as e:
    print(json.dumps({{"error": "syntax", "message": str(e), "lineno": e.lineno}}))
    sys.exit(1)
except Exception as e:
    print(json.dumps({{"error": "import", "message": str(e)}}))
    sys.exit(1)

try:
    with open("input.json", "r") as f:
        args = json.load(f)
    
    if isinstance(args, dict):
        result = {function_name}(**args)
    else:
        result = {function_name}(*args)
    
    print(json.dumps({{"ok": True, "result": result}}))
except Exception as e:
    import traceback
    print(json.dumps({{
        "error": "runtime",
        "message": str(e),
        "traceback": traceback.format_exc()
    }}))
    sys.exit(1)
'''


def get_harness_code(entrypoint_type: str, entrypoint_name: str) -> str:
    """
    Generate the harness runner code for the given entrypoint configuration.
    
    Args:
        entrypoint_type: 'class' for Solution class, 'function' for bare function
        entrypoint_name: The method/function name to call
        
    Returns:
        Python code string for the harness runner
    """
    if entrypoint_type == 'class':
        return SOLUTION_CLASS_HARNESS.format(method_name=entrypoint_name)
    else:
        return FUNCTION_HARNESS.format(function_name=entrypoint_name)
