# Password Generator

## What does this program do?
This program generates a random password at any length specified.

## Libraries used
I imported `random` and `string`. These libraries give us access to 
`string.ascii_letters`, `string.digits`, `string.punctuation`, and 
`random.choice()`.

## How it works
The `gen_rand_password(length)` function builds a character pool by combining 
letters, digits, and punctuation into one string. It then uses `random.choice()` 
to pick a single random character from that pool, repeating it as many times as 
specified by the `length` parameter. The results are joined together into one 
string using `"".join()` and returned as the final password.

`length` is a parameter instead of a hardcoded number so the function is 
reusable — you can call `gen_rand_password(8)` or `gen_rand_password(20)` 
without changing the code.

## What I learned
- How the `random` and `string` libraries work together
- How to write a reusable custom function with a parameter
- How to use `random.choice()` inside a generator expression
- How `"".join()` combines individual characters into a single string
