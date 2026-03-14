# Common Python Errors

## Off-by-One Error
**Pattern:** Using `index + 1` or `index - 1` incorrectly when accessing list elements.
**Example:** `return lst[idx+1]` when you mean `return lst[idx]`
**Fix:** Check boundary conditions and verify the index logic matches the intended behavior.
**Languages:** Python, JavaScript, Java, C++

## IndexError: list index out of range
**Pattern:** Accessing an index that doesn't exist in a list or array.
**Example:** Iterating with `range(len(lst))` but accessing `lst[i+1]`.
**Fix:** Use `range(len(lst) - 1)` or add bounds checking.

## KeyError in dictionary access
**Pattern:** Accessing a dictionary key that may not exist without using `.get()`.
**Example:** `return data["key"]` when key might be missing.
**Fix:** Use `data.get("key", default_value)` or check with `if "key" in data`.

## Mutable Default Arguments
**Pattern:** Using mutable objects (list, dict) as default function arguments.
**Example:** `def func(items=[])` — the list is shared across all calls.
**Fix:** Use `None` as default and create the mutable object inside the function.

## UnboundLocalError
**Pattern:** Referencing a variable before assignment inside a function that also assigns to it.
**Example:** `x = x + 1` inside a function without declaring `nonlocal x` or `global x`.
**Fix:** Use `nonlocal` or `global`, or pass the variable as a parameter.

## TypeError: unsupported operand types
**Pattern:** Performing operations between incompatible types.
**Example:** `"score: " + 42` — string + int.
**Fix:** Convert types explicitly: `"score: " + str(42)` or use f-strings.

## Infinite Loop
**Pattern:** Loop condition never becomes False.
**Example:** `while i < 10:` without incrementing `i`.
**Fix:** Ensure the loop variable is modified to eventually meet the exit condition.

## None Return
**Pattern:** Function missing a return statement or returning None implicitly.
**Example:** A function that processes data but forgets `return result`.
**Fix:** Add explicit return statement with the computed value.

## Shallow Copy Bug
**Pattern:** Modifying a copy of a nested structure that still references the original.
**Example:** `copy = original[:]` for a list of lists — inner lists are shared.
**Fix:** Use `copy.deepcopy()` for nested structures.

## String Comparison vs Identity
**Pattern:** Using `is` instead of `==` for value comparison.
**Example:** `if name is "admin"` — works sometimes due to interning but is unreliable.
**Fix:** Always use `==` for value comparison; `is` is for identity (e.g., `is None`).
