# Program Analysis using Constraints

Realized I forgot to write this up last week, so doing it quickly now! 

I really struggled with understanding Farkas' lemma and how to apply it, so after spending several hours trying to do it out on paper and get it working, I decided to try implementing different parts of the paper.

First, I wrote a program to constraints generator for programs with very similar form to the first example given in the paper. Given an input program of such a form, my code outputs a list of constraints with an unknown loop invariant, following the syntax and model of the paper. With more time, I would make this more generalized, likely using a graph approach rather than a syntax/pure parsing approach, but this method is effective if the program space is strictly limited to specific program types.

I then played around with Z3, first understanding how it worked and how to use it, and then performed some constraint simplifications by hand and plugged the results into Z3 to try and get solutions. I managed to get several solutions without using Farkas' lemma, but they were far more complex and messy than the paper's solutions for the same constraints. I tried to apply Farkas' lemma as well, but couldn't figure out how to do it in a programmatic or algorithmic fashion.

Overall, I understand the paper and the process far more, but still don't quite understand most of the difficult "magic" steps that use Farkas' lemma to get simple loop invariants as shown in the paper.
