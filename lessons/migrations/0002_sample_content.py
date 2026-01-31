# Generated manually - Sample courses and lessons

from django.db import migrations


def create_sample_content(apps, schema_editor):
    Course = apps.get_model('lessons', 'Course')
    Lesson = apps.get_model('lessons', 'Lesson')
    Problem = apps.get_model('problems', 'Problem')
    
    # ==========================================================================
    # Course 1: Python Fundamentals
    # ==========================================================================
    python_basics = Course.objects.create(
        title="Python Fundamentals",
        slug="python-fundamentals",
        description="Master the core concepts of Python programming. Perfect for beginners starting their coding journey.",
        is_published=True,
        order=1
    )
    
    # Lesson 1.1: Introduction to Python
    Lesson.objects.create(
        course=python_basics,
        title="Introduction to Python",
        slug="introduction-to-python",
        summary="What is Python and why learn it?",
        order=1,
        is_published=True,
        content_markdown="""# Introduction to Python

Python is one of the most popular programming languages in the world, and for good reason. It's **readable**, **versatile**, and **beginner-friendly**.

## Why Learn Python?

1. **Easy to Read** - Python's syntax is clean and intuitive
2. **Versatile** - Used in web development, data science, AI, automation, and more
3. **Large Community** - Tons of libraries, tutorials, and support
4. **In-Demand** - One of the most sought-after skills in tech

## Your First Python Program

The classic first program in any language is "Hello, World!":

```python
print("Hello, World!")
```

When you run this code, Python will display:

```
Hello, World!
```

## How Python Works

Python is an **interpreted language**, which means:
- You write code in a `.py` file
- The Python interpreter reads and executes your code line by line
- You see the results immediately

This makes Python great for learning because you get instant feedback!

## What You'll Learn

In this course, we'll cover:
- Variables and data types
- Control flow (if statements, loops)
- Functions
- Working with data structures (lists, dictionaries)
- And much more!

> **Tip:** The best way to learn programming is by doing. Try to code along with each lesson and complete the practice problems!

Ready to start? Let's move on to variables!
"""
    )
    
    # Lesson 1.2: Variables and Data Types
    variables_lesson = Lesson.objects.create(
        course=python_basics,
        title="Variables and Data Types",
        slug="variables-and-data-types",
        summary="Learn how to store and work with data in Python.",
        order=2,
        is_published=True,
        content_markdown="""# Variables and Data Types

Variables are containers for storing data. Think of them as labeled boxes where you can put information.

## Creating Variables

In Python, you create a variable by giving it a name and assigning a value:

```python
name = "Alice"
age = 25
height = 5.6
is_student = True
```

Notice that we didn't have to declare the type - Python figures it out automatically!

## Data Types

Python has several built-in data types:

### Strings (`str`)
Text data, enclosed in quotes:

```python
greeting = "Hello"
name = 'Bob'
message = \"\"\"This is a
multi-line string\"\"\"
```

### Integers (`int`)
Whole numbers:

```python
count = 42
temperature = -10
year = 2024
```

### Floats (`float`)
Decimal numbers:

```python
pi = 3.14159
price = 19.99
percentage = 0.75
```

### Booleans (`bool`)
True or False values:

```python
is_active = True
has_permission = False
```

## Checking Types

Use `type()` to check a variable's type:

```python
x = 42
print(type(x))  # <class 'int'>

y = "hello"
print(type(y))  # <class 'str'>
```

## Variable Naming Rules

1. Must start with a letter or underscore
2. Can contain letters, numbers, and underscores
3. Case-sensitive (`name` and `Name` are different)
4. Cannot use Python keywords (`if`, `for`, `while`, etc.)

```python
# Good names
user_name = "Alice"
totalCount = 100
_private = "secret"

# Bad names (will cause errors)
# 2nd_place = "silver"  # Can't start with number
# my-variable = 5       # Can't use hyphens
# class = "Math"        # Can't use keywords
```

## Practice

Try creating variables of different types and printing them:

```python
# Your turn!
my_name = "Your Name"
my_age = 20
favorite_number = 7.5

print(f"Hi, I'm {my_name}!")
print(f"I'm {my_age} years old.")
print(f"My favorite number is {favorite_number}")
```

> **Note:** The `f` before the string creates an "f-string" which lets you embed variables directly in text!
"""
    )
    
    # Lesson 1.3: Operators and Expressions
    Lesson.objects.create(
        course=python_basics,
        title="Operators and Expressions",
        slug="operators-and-expressions",
        summary="Perform calculations and comparisons in Python.",
        order=3,
        is_published=True,
        content_markdown="""# Operators and Expressions

Operators let you perform operations on values and variables.

## Arithmetic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `5 + 3` → `8` |
| `-` | Subtraction | `5 - 3` → `2` |
| `*` | Multiplication | `5 * 3` → `15` |
| `/` | Division | `5 / 3` → `1.666...` |
| `//` | Floor Division | `5 // 3` → `1` |
| `%` | Modulo (remainder) | `5 % 3` → `2` |
| `**` | Exponentiation | `5 ** 3` → `125` |

```python
a = 10
b = 3

print(a + b)   # 13
print(a - b)   # 7
print(a * b)   # 30
print(a / b)   # 3.333...
print(a // b)  # 3
print(a % b)   # 1
print(a ** b)  # 1000
```

## Comparison Operators

These return `True` or `False`:

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equal to | `5 == 5` → `True` |
| `!=` | Not equal to | `5 != 3` → `True` |
| `>` | Greater than | `5 > 3` → `True` |
| `<` | Less than | `5 < 3` → `False` |
| `>=` | Greater or equal | `5 >= 5` → `True` |
| `<=` | Less or equal | `5 <= 3` → `False` |

```python
x = 10
y = 5

print(x == y)   # False
print(x != y)   # True
print(x > y)    # True
print(x < y)    # False
```

## Logical Operators

Combine boolean expressions:

| Operator | Description | Example |
|----------|-------------|---------|
| `and` | Both must be True | `True and False` → `False` |
| `or` | At least one True | `True or False` → `True` |
| `not` | Inverts the value | `not True` → `False` |

```python
age = 25
has_license = True

# Can they rent a car?
can_rent = age >= 21 and has_license
print(can_rent)  # True

# Is it a weekend?
is_saturday = True
is_sunday = False
is_weekend = is_saturday or is_sunday
print(is_weekend)  # True
```

## String Operators

```python
# Concatenation
first = "Hello"
last = "World"
full = first + " " + last
print(full)  # "Hello World"

# Repetition
line = "-" * 20
print(line)  # "--------------------"
```

## Order of Operations

Python follows standard math precedence (PEMDAS):

1. **P**arentheses `()`
2. **E**xponents `**`
3. **M**ultiplication/Division `* / // %`
4. **A**ddition/Subtraction `+ -`

```python
result = 2 + 3 * 4      # 14 (not 20!)
result = (2 + 3) * 4    # 20 (parentheses first)
```

> **Tip:** When in doubt, use parentheses to make your intentions clear!
"""
    )
    
    # Lesson 1.4: Control Flow - If Statements
    Lesson.objects.create(
        course=python_basics,
        title="Control Flow: If Statements",
        slug="control-flow-if-statements",
        summary="Make decisions in your code with conditional statements.",
        order=4,
        is_published=True,
        content_markdown="""# Control Flow: If Statements

Programs often need to make decisions. If statements let your code take different paths based on conditions.

## Basic If Statement

```python
age = 18

if age >= 18:
    print("You are an adult")
```

The code inside the `if` block only runs when the condition is `True`.

## If-Else

Handle both cases:

```python
temperature = 72

if temperature > 80:
    print("It's hot outside!")
else:
    print("The weather is nice.")
```

## If-Elif-Else

Check multiple conditions:

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade is: {grade}")
```

> **Important:** Python checks conditions from top to bottom and stops at the first `True` condition.

## Indentation Matters!

Python uses indentation (spaces) to define code blocks:

```python
if True:
    print("This is inside the if block")
    print("This too!")
print("This is outside the if block")
```

Use 4 spaces for indentation (this is the Python standard).

## Nested If Statements

You can put if statements inside other if statements:

```python
has_ticket = True
age = 15

if has_ticket:
    if age >= 13:
        print("Enjoy the movie!")
    else:
        print("Sorry, this movie is PG-13")
else:
    print("Please buy a ticket first")
```

## Combining Conditions

Use `and`, `or`, and `not` to combine conditions:

```python
age = 25
has_license = True
has_car = False

# Need both license AND car to drive
if has_license and has_car:
    print("You can drive!")
else:
    print("You can't drive right now")

# Can vote if 18 or older
if age >= 18:
    print("You can vote")

# Check if NOT a minor
if not age < 18:
    print("You're an adult")
```

## Common Patterns

### Checking for empty values

```python
name = ""

if name:
    print(f"Hello, {name}!")
else:
    print("Name is empty")
```

### Checking membership

```python
fruits = ["apple", "banana", "cherry"]

if "banana" in fruits:
    print("We have bananas!")
```

## Practice Problem

Write a program that checks if a number is positive, negative, or zero:

```python
number = -5

if number > 0:
    print("Positive")
elif number < 0:
    print("Negative")
else:
    print("Zero")
```
"""
    )
    
    # Lesson 1.5: Loops
    Lesson.objects.create(
        course=python_basics,
        title="Loops: For and While",
        slug="loops-for-and-while",
        summary="Repeat actions with for loops and while loops.",
        order=5,
        is_published=True,
        content_markdown="""# Loops: For and While

Loops let you repeat code multiple times without writing it over and over.

## For Loops

Use `for` when you know how many times to loop:

```python
# Print numbers 0 to 4
for i in range(5):
    print(i)
```

Output:
```
0
1
2
3
4
```

### Looping Over Lists

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I like {fruit}")
```

### Range Variations

```python
# Start at 1, go to 5
for i in range(1, 6):
    print(i)  # 1, 2, 3, 4, 5

# Start at 0, go to 10, step by 2
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Count backwards
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

## While Loops

Use `while` when you don't know how many iterations you need:

```python
count = 0

while count < 5:
    print(count)
    count += 1  # Don't forget this!
```

### Common Pattern: User Input

```python
password = ""

while password != "secret":
    password = input("Enter password: ")

print("Access granted!")
```

## Break and Continue

### Break - Exit the loop early

```python
for i in range(10):
    if i == 5:
        break  # Stop the loop
    print(i)
# Prints: 0, 1, 2, 3, 4
```

### Continue - Skip to next iteration

```python
for i in range(5):
    if i == 2:
        continue  # Skip this iteration
    print(i)
# Prints: 0, 1, 3, 4
```

## Nested Loops

Loops inside loops:

```python
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})")
```

### Example: Multiplication Table

```python
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i * j:3}", end=" ")
    print()  # New line after each row
```

Output:
```
  1   2   3   4   5 
  2   4   6   8  10 
  3   6   9  12  15 
  4   8  12  16  20 
  5  10  15  20  25 
```

## Loop with Else

Python has an unusual feature - loops can have an `else` clause:

```python
for i in range(5):
    if i == 10:
        break
else:
    print("Loop completed without break")
```

The `else` block runs only if the loop completes normally (no `break`).

## Common Patterns

### Sum of numbers

```python
numbers = [1, 2, 3, 4, 5]
total = 0

for num in numbers:
    total += num

print(f"Sum: {total}")  # 15
```

### Find an item

```python
names = ["Alice", "Bob", "Charlie"]
search = "Bob"

for name in names:
    if name == search:
        print(f"Found {search}!")
        break
else:
    print(f"{search} not found")
```

> **Warning:** Be careful with `while` loops - make sure your condition will eventually become `False`, or you'll create an infinite loop!
"""
    )
    
    # ==========================================================================
    # Course 2: Data Structures
    # ==========================================================================
    data_structures = Course.objects.create(
        title="Python Data Structures",
        slug="python-data-structures",
        description="Learn to organize and manipulate data with lists, dictionaries, sets, and tuples.",
        is_published=True,
        order=2
    )
    
    # Lesson 2.1: Lists
    lists_lesson = Lesson.objects.create(
        course=data_structures,
        title="Working with Lists",
        slug="working-with-lists",
        summary="Create, modify, and manipulate lists in Python.",
        order=1,
        is_published=True,
        content_markdown="""# Working with Lists

Lists are ordered, mutable collections that can hold any type of data.

## Creating Lists

```python
# Empty list
empty = []

# List with values
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", 3.14, True]

# Using list() constructor
letters = list("hello")  # ['h', 'e', 'l', 'l', 'o']
```

## Accessing Elements

```python
fruits = ["apple", "banana", "cherry", "date"]

# Positive indexing (from start)
print(fruits[0])   # "apple"
print(fruits[1])   # "banana"

# Negative indexing (from end)
print(fruits[-1])  # "date"
print(fruits[-2])  # "cherry"
```

## Slicing

Get a portion of a list:

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[2:5])    # [2, 3, 4]
print(numbers[:3])     # [0, 1, 2]
print(numbers[7:])     # [7, 8, 9]
print(numbers[::2])    # [0, 2, 4, 6, 8] (every 2nd)
print(numbers[::-1])   # [9, 8, 7, ...] (reversed)
```

## Modifying Lists

```python
fruits = ["apple", "banana", "cherry"]

# Change an element
fruits[1] = "blueberry"
print(fruits)  # ["apple", "blueberry", "cherry"]

# Add to end
fruits.append("date")
print(fruits)  # ["apple", "blueberry", "cherry", "date"]

# Insert at position
fruits.insert(1, "apricot")
print(fruits)  # ["apple", "apricot", "blueberry", "cherry", "date"]

# Remove by value
fruits.remove("cherry")

# Remove by index
del fruits[0]
# or
popped = fruits.pop(0)  # Returns the removed item
```

## List Methods

| Method | Description | Example |
|--------|-------------|---------|
| `append(x)` | Add item to end | `lst.append(4)` |
| `insert(i, x)` | Insert at index | `lst.insert(0, "first")` |
| `remove(x)` | Remove first occurrence | `lst.remove("apple")` |
| `pop(i)` | Remove and return item | `lst.pop()` or `lst.pop(0)` |
| `clear()` | Remove all items | `lst.clear()` |
| `index(x)` | Find index of item | `lst.index("apple")` |
| `count(x)` | Count occurrences | `lst.count(5)` |
| `sort()` | Sort in place | `lst.sort()` |
| `reverse()` | Reverse in place | `lst.reverse()` |
| `copy()` | Create a copy | `new = lst.copy()` |

## List Comprehensions

A concise way to create lists:

```python
# Traditional way
squares = []
for x in range(5):
    squares.append(x ** 2)

# List comprehension
squares = [x ** 2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]

# With condition
evens = [x for x in range(10) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]
```

## Common Operations

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Length
print(len(numbers))  # 8

# Sum
print(sum(numbers))  # 31

# Min/Max
print(min(numbers))  # 1
print(max(numbers))  # 9

# Check membership
print(5 in numbers)  # True
print(7 in numbers)  # False

# Concatenation
a = [1, 2]
b = [3, 4]
c = a + b  # [1, 2, 3, 4]
```

## Practice

Try solving the Two Sum problem after this lesson - it's a classic list manipulation challenge!
"""
    )
    
    # Lesson 2.2: Dictionaries
    Lesson.objects.create(
        course=data_structures,
        title="Dictionaries",
        slug="dictionaries",
        summary="Store and retrieve data using key-value pairs.",
        order=2,
        is_published=True,
        content_markdown="""# Dictionaries

Dictionaries store data as key-value pairs. They're perfect for when you want to look up values by a unique identifier.

## Creating Dictionaries

```python
# Empty dictionary
empty = {}

# With values
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Using dict() constructor
person = dict(name="Alice", age=30, city="New York")
```

## Accessing Values

```python
person = {"name": "Alice", "age": 30, "city": "New York"}

# Using brackets
print(person["name"])  # "Alice"

# Using get() - safer, returns None if key doesn't exist
print(person.get("name"))       # "Alice"
print(person.get("country"))    # None
print(person.get("country", "USA"))  # "USA" (default value)
```

> **Tip:** Use `get()` when the key might not exist to avoid `KeyError`.

## Modifying Dictionaries

```python
person = {"name": "Alice", "age": 30}

# Add or update a key
person["city"] = "New York"  # Add new key
person["age"] = 31           # Update existing key

# Remove a key
del person["city"]

# Pop - remove and return value
age = person.pop("age")
print(age)  # 31
```

## Dictionary Methods

| Method | Description |
|--------|-------------|
| `keys()` | Returns all keys |
| `values()` | Returns all values |
| `items()` | Returns key-value pairs as tuples |
| `get(key, default)` | Get value with default if missing |
| `pop(key)` | Remove and return value |
| `update(dict2)` | Merge another dictionary |
| `clear()` | Remove all items |

```python
person = {"name": "Alice", "age": 30, "city": "NYC"}

print(list(person.keys()))    # ["name", "age", "city"]
print(list(person.values()))  # ["Alice", 30, "NYC"]
print(list(person.items()))   # [("name", "Alice"), ...]
```

## Looping Over Dictionaries

```python
person = {"name": "Alice", "age": 30, "city": "NYC"}

# Loop over keys
for key in person:
    print(key)

# Loop over values
for value in person.values():
    print(value)

# Loop over both
for key, value in person.items():
    print(f"{key}: {value}")
```

## Nested Dictionaries

```python
students = {
    "alice": {
        "grade": "A",
        "age": 20
    },
    "bob": {
        "grade": "B",
        "age": 21
    }
}

# Access nested values
print(students["alice"]["grade"])  # "A"
```

## Dictionary Comprehensions

```python
# Create a dictionary of squares
squares = {x: x**2 for x in range(5)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Filter while creating
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
```

## Common Use Cases

### Counting occurrences

```python
text = "hello world"
char_count = {}

for char in text:
    if char in char_count:
        char_count[char] += 1
    else:
        char_count[char] = 1

print(char_count)
# {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
```

### Grouping data

```python
students = [
    {"name": "Alice", "grade": "A"},
    {"name": "Bob", "grade": "B"},
    {"name": "Charlie", "grade": "A"}
]

by_grade = {}
for student in students:
    grade = student["grade"]
    if grade not in by_grade:
        by_grade[grade] = []
    by_grade[grade].append(student["name"])

print(by_grade)
# {"A": ["Alice", "Charlie"], "B": ["Bob"]}
```

> **When to use dictionaries:** Use them when you need fast lookups by a unique key, or when data naturally has key-value relationships.
"""
    )
    
    # ==========================================================================
    # Course 3: Problem Solving
    # ==========================================================================
    problem_solving = Course.objects.create(
        title="Problem Solving Patterns",
        slug="problem-solving-patterns",
        description="Learn common algorithmic patterns to tackle coding challenges effectively.",
        is_published=True,
        order=3
    )
    
    # Lesson 3.1: Two Pointers
    Lesson.objects.create(
        course=problem_solving,
        title="Two Pointers Technique",
        slug="two-pointers-technique",
        summary="Use two pointers to solve array problems efficiently.",
        order=1,
        is_published=True,
        content_markdown="""# Two Pointers Technique

The two pointers technique is a pattern where you use two indices to traverse a data structure, often from different ends or at different speeds.

## When to Use Two Pointers

- Searching for pairs in a sorted array
- Reversing or comparing elements
- Finding subarrays with certain properties
- Removing duplicates

## Pattern 1: Opposite Direction

Start one pointer at the beginning, one at the end, and move them toward each other.

### Example: Is Palindrome?

```python
def is_palindrome(s):
    left = 0
    right = len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True

print(is_palindrome("racecar"))  # True
print(is_palindrome("hello"))    # False
```

### Example: Two Sum (Sorted Array)

Given a **sorted** array, find two numbers that add up to a target:

```python
def two_sum_sorted(numbers, target):
    left = 0
    right = len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1   # Need larger sum
        else:
            right -= 1  # Need smaller sum
    
    return []  # No solution found

nums = [1, 2, 3, 4, 6]
print(two_sum_sorted(nums, 6))  # [1, 3] (indices of 2 and 4)
```

## Pattern 2: Same Direction (Fast/Slow)

Both pointers move in the same direction, but at different speeds.

### Example: Remove Duplicates (In-Place)

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    
    slow = 0
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    
    return slow + 1  # Length of unique elements

nums = [1, 1, 2, 2, 3, 4, 4]
length = remove_duplicates(nums)
print(nums[:length])  # [1, 2, 3, 4]
```

### Example: Move Zeros to End

```python
def move_zeros(nums):
    slow = 0
    
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
    
    return nums

print(move_zeros([0, 1, 0, 3, 12]))  # [1, 3, 12, 0, 0]
```

## Pattern 3: Sliding Window Variant

Sometimes two pointers define a "window" in the array:

```python
def longest_substring_without_repeating(s):
    seen = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        
        seen.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length

print(longest_substring_without_repeating("abcabcbb"))  # 3 ("abc")
```

## Key Insights

1. **Sorted arrays** - Two pointers from opposite ends often work well
2. **In-place modifications** - Fast/slow pointer pattern
3. **Time complexity** - Usually O(n) since each pointer moves at most n times
4. **Space complexity** - Usually O(1) since we only use pointer variables

## Practice Problems

After this lesson, try these problems:
- Two Sum (if the array is sorted)
- Valid Palindrome
- Container With Most Water
- 3Sum

> **Tip:** When you see "find a pair" or "in-place" in a problem, consider two pointers!
"""
    )
    
    # Link some problems to lessons
    try:
        two_sum = Problem.objects.filter(slug='two-sum').first()
        if two_sum and lists_lesson:
            lists_lesson.problems.add(two_sum)
        
        valid_palindrome = Problem.objects.filter(slug='valid-palindrome').first()
        if valid_palindrome:
            # Get the two pointers lesson we just created
            two_pointers = Lesson.objects.get(slug='two-pointers-technique')
            two_pointers.problems.add(valid_palindrome)
    except:
        pass  # Problems might not exist


def remove_sample_content(apps, schema_editor):
    Course = apps.get_model('lessons', 'Course')
    Course.objects.filter(slug__in=[
        'python-fundamentals',
        'python-data-structures', 
        'problem-solving-patterns'
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_content, remove_sample_content),
    ]
