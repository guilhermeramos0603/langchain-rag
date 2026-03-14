# Common JavaScript Errors

## TypeError: Cannot read properties of undefined
**Pattern:** Accessing a property on an undefined or null value.
**Example:** `user.address.street` when `user.address` is undefined.
**Fix:** Use optional chaining: `user?.address?.street`.

## == vs === Comparison
**Pattern:** Using loose equality `==` which performs type coercion.
**Example:** `0 == ""` is true, `null == undefined` is true.
**Fix:** Always use strict equality `===` unless type coercion is intentional.

## Async/Await Missing await
**Pattern:** Calling an async function without `await`, getting a Promise instead of a value.
**Example:** `const data = fetchData()` — data is a Promise, not the result.
**Fix:** Add `await`: `const data = await fetchData()`.

## Closure in Loop
**Pattern:** Variables in closures inside loops capture by reference, not by value.
**Example:** `for (var i = 0; i < 5; i++) { setTimeout(() => console.log(i), 100) }` — prints 5 five times.
**Fix:** Use `let` instead of `var`, or create an IIFE.

## Array.sort() Without Comparator
**Pattern:** `Array.sort()` converts elements to strings by default.
**Example:** `[10, 2, 1].sort()` returns `[1, 10, 2]`.
**Fix:** Provide a comparator: `.sort((a, b) => a - b)`.

## this Context Loss
**Pattern:** Losing `this` context when passing methods as callbacks.
**Example:** `button.addEventListener('click', obj.handleClick)` — `this` is not `obj`.
**Fix:** Use arrow functions or `.bind(this)`.

## Off-by-One in slice/substring
**Pattern:** Misunderstanding that `slice(start, end)` excludes the end index.
**Example:** `"hello".slice(0, 4)` returns "hell", not "hello".
**Fix:** Use `end + 1` if you want to include the character at index `end`.
