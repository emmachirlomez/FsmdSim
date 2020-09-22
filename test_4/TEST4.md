# This test checks if a number is or not a prime number.

The FSMD that does this has the following:

## Variables

1. P: We want P factorial
2. x: number we will vary from 2 to p - 1, to check if p is divisible by x
3. is_prime: contains true if p is prime and false otherwise

## States

1. INIT_STATE
1. LOOP_STATE
1. END_STATE

## Conditions

- Name: "X_equal_P"
  Value: "x == p"
- Name: "X_not_div_P"
  Value: "x != p and p % x != 0"
- Name: "X_div_P"
  Value "x != p and p % x == 0"

## Transitions

- From INIT_STATE
  - Condition: "True"
    Expresion: "init_P init_x init_is_prime"
    Next State: LOOP_STATE
- From LOOP_STATE
  - Condition: X_equal_P
    Expression: "POS"
    Next State: END_STATE
  - Condition: X_not_div_P
    Expression: "increase_x"
    Next State: LOOP_STATE
  - Condition: X_div_P
    Expression: "set_not_prime"
    Next State: END_STATE
- From END_STATE
  - Condition: "True"
    Expression: "POS"
    Next State: END_STATE
