#Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

#Sum of the squares the first 100 natural numbers:
sum_squares = sum([i*i for i in range(1, 101)])
square_sum = sum(range(1, 101)) ** 2
difference = square_sum - sum_squares
print(f"Difference between square of the first 100 numbers sum and sum of squares of them is {difference}")
