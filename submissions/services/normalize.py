"""
Output normalization and comparison for judge verdicts.

Normalization rules:
- Strip trailing whitespace from each line
- Normalize line endings to \n
- Strip trailing newlines from the entire output
- Compare exact match after normalization
"""


def normalize_output(output: str) -> str:
    """
    Normalize program output for comparison.
    
    - Strips trailing whitespace from each line
    - Normalizes line endings
    - Removes trailing blank lines
    """
    if not output:
        return ''
    
    # Normalize line endings
    output = output.replace('\r\n', '\n').replace('\r', '\n')
    
    # Strip trailing whitespace from each line
    lines = [line.rstrip() for line in output.split('\n')]
    
    # Remove trailing empty lines
    while lines and lines[-1] == '':
        lines.pop()
    
    return '\n'.join(lines)


def outputs_match(actual: str, expected: str) -> bool:
    """
    Compare two outputs after normalization.
    
    Returns True if the normalized outputs are identical.
    """
    return normalize_output(actual) == normalize_output(expected)
