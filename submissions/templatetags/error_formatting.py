"""
Template filters for formatting error messages and tracebacks.
"""

import re
from django import template

register = template.Library()


@register.filter
def format_traceback(traceback_text: str, max_lines: int = 15) -> str:
    """
    Format a Python traceback for display.
    
    - Removes internal framework lines (runner.py, harness references)
    - Highlights the user's code (submission.py / solution.py)
    - Truncates long tracebacks while preserving the most relevant parts
    """
    if not traceback_text:
        return ""
    
    lines = traceback_text.strip().split('\n')
    
    # Find user-relevant lines (from submission.py or solution.py)
    filtered_lines = []
    skip_until_next_file = False
    
    for line in lines:
        # Skip internal harness/runner lines
        if 'runner.py' in line or 'harness' in line.lower():
            skip_until_next_file = True
            continue
        
        # Check if this is a file reference line
        if line.strip().startswith('File "'):
            skip_until_next_file = False
            # Keep user code references, mark them
            if 'submission.py' in line or 'solution.py' in line:
                # Normalize the file reference to just "your code"
                line = re.sub(r'File "[^"]*(?:submission|solution)\.py"', 'File "your_code.py"', line)
            filtered_lines.append(line)
        elif not skip_until_next_file:
            filtered_lines.append(line)
    
    # If we have too many lines, truncate from the middle
    if len(filtered_lines) > max_lines:
        # Keep first 5 and last (max_lines - 6) lines
        head = filtered_lines[:5]
        tail = filtered_lines[-(max_lines - 6):]
        filtered_lines = head + ['    ... (traceback truncated) ...'] + tail
    
    return '\n'.join(filtered_lines)


@register.filter
def format_error_line(error_text: str) -> str:
    """
    Extract and format the most relevant error line from an error message.
    
    For display in a compact format (e.g., "Line 5: NameError: name 'x' is not defined")
    """
    if not error_text:
        return ""
    
    lines = error_text.strip().split('\n')
    
    # Find the line number and error type
    line_info = ""
    error_type = ""
    error_message = ""
    
    for line in lines:
        # Look for "File ... line X" pattern
        match = re.search(r'line (\d+)', line, re.IGNORECASE)
        if match and ('submission.py' in line or 'solution.py' in line or 'your_code' in line):
            line_info = f"Line {match.group(1)}"
        
        # Look for error type (e.g., "NameError:", "TypeError:")
        if ': ' in line and not line.startswith(' '):
            parts = line.split(': ', 1)
            if len(parts) == 2 and parts[0].endswith('Error'):
                error_type = parts[0]
                error_message = parts[1]
    
    # Also check the last line for the error message
    if lines and ': ' in lines[-1]:
        parts = lines[-1].split(': ', 1)
        if len(parts) == 2 and 'Error' in parts[0]:
            error_type = parts[0]
            error_message = parts[1]
    
    if line_info and error_type:
        return f"{line_info}: {error_type}: {error_message}"
    elif error_type:
        return f"{error_type}: {error_message}"
    elif lines:
        # Return last non-empty line as fallback
        return lines[-1] if lines[-1].strip() else error_text[:200]
    
    return error_text[:200]


@register.filter
def verdict_description(verdict: str, test_index: int = None) -> str:
    """
    Return a human-readable description for a verdict.
    """
    descriptions = {
        'AC': 'All tests passed!',
        'WA': 'Wrong Answer',
        'RE': 'Runtime Error',
        'TLE': 'Time Limit Exceeded',
        'CE': 'Syntax Error',
        'pending': 'Pending...',
    }
    
    base = descriptions.get(verdict, verdict)
    
    if test_index and verdict in ('WA', 'RE', 'TLE'):
        return f"{base} on test {test_index}"
    
    return base
