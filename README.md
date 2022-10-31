# parker-multiplicative-persistance-augmentator

A tool to find a number with a greater multiplicative persistence of any* input

_This is an exercise project to have fun and also learn some Rust_  
_A slower python version is in its own branch._

## The Inspiration

Like many, I've been inspired in this fun project by the only Matt Parker. In the numberphile video ["What's special about 277777788888899?"](https://www.youtube.com/watch?v=Wim9WJeDTHQ), Matt talks about the number 277777788888899 and how it is the number with the biggest **multiplicative persistance (MP)** found.
Watch the video to get the full explanation:

[![Watch the video](https://img.youtube.com/vi/Wim9WJeDTHQ/default.jpg)](https://www.youtube.com/watch?v=Wim9WJeDTHQ)


## The Problem

The objective is to **find a number with a greater multiplicative persistance** than 277777788888899.

The first approach that may come to mind is the *brute-force approach*: simply checking the MP of all numbers one by one. This is terribly boring without a supercomputer and it's not that fun of a challange.

So instead i thought: "Can i simply find a number **N** whose product of the digits results in another number **M**?"

By definition we would have `MP(N) = MP(M) + 1`

So if M=277777788888899, we necessarily have the new Most Multiplicative Persistent number! (and we could go on in theory)

Of course, **this number probably does not exist** and this project won't be solving this problem (but what's wrong with a pointless math fun project)

From [Wikipedia](https://en.wikipedia.org/wiki/Persistence_of_a_number#Smallest_numbers_of_a_given_multiplicative_persistence):
```
[...] the number of candidates for n-digit numbers with record-breaking persistence is only proportional to the square of n, 
a tiny fraction of all possible n-digit numbers. However, any number that is missing from the sequence above 
would have multiplicative persistence > 11; 

such numbers are believed not to exist, and would need to have over 20,000 digits if they do exist.
```

## The basic implementation

The quest is to find a set of single-digit divisors of M so that the product equals exactly **M**

So we simply loop from 2 to **M**-1 and if we hit a divisor **D** of **M** we check recursively trying to find single-digit divisors of **D** and **M**-**D** and so on (if **D** is a single digit, recursion stops)

In the end we should have a set of single digits that multiplied together should give **M**

## Improvements

Since the basic approach is terribly slow, I had to come up with some improvements

### Cutting the check for divisors

First, if you have to find divisors of a number  **M**, you don't need to check every number to **M**-1, but only up to `ceil(sqrt( **M** ))`, over that you're double-checking. 
This was a big improvement, but we were still too slow for numbers like 277777788888899


### Dead-ends 

If any sub-computation ends up in a dead-end (no single-digit divisor found) the whole current stack can be considered a dead-end and there's no reason to keep checking it


### Computation Caching 

_(Python version only, still TODO in Rust version)_

Second, every call to `try_to_find_single_digit_divisors` can be a pure function (if we ignore caching itself) so simply caching the results would save a lot of duplicate execution time

### Permutations Check

This is not a speed improvement, because it actually made the speed problem millions of times more challenging. It is a solution improvement though! 

The idea is that, given the nature of the problem, **a solution to a "permutation" of M is also a solution for M**.
By permutation I mean of its digits of course.

That would mean that other than M, I have to check also all of the unique permutations of its digits, which in the case of 277777788888899 are 1261260 in mumber (see what I mean by more challenging?)

### Rust rewrite

Python is notoriously slow, so for speed'sake I tried rewriting the problem in Rust (which I never used before), hoping that I could learn it good enough to take advantage of its speed.

## The Result

Still too slow for me to have an answer, I could leave it running for 32 days until it finishes but what's the fun in that? (matt fans will know)
So I will keep improving until I have a fast solution for 277777788888899 and if it doesn't exist maybe I'll keep toying with this problem to keep challenging myself.




