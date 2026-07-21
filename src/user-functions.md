# User Functions

In GPC scripting, you can define your own custom functions. Custom functions help you write cleaner, modular code, reduce repetition, and save bytecode space in your Cronus Zen memory slots.

---

## Defining a Function

User-defined functions are created using the `function` keyword. They must accept only integer arguments and can optionally return an integer value using the `return` statement.

### Syntax

```c
function function_name(parameter_1, parameter_2) {
    // Logic and calculations
    int result = parameter_1 * parameter_2;
    
    return result; // Exit function and return the value
}
```

{% hint style="important" %}
**Placement Constraint**
In GPC scripts, user-defined functions **must be defined at the very end of your script** — after the `main {}` block and after all `combo {}` blocks. Placing them at the beginning or middle of the script will cause compiler errors.
{% endhint %}

---

## Function Guidelines & Rules

### 1. Unified Data Types
Unlike standard C, GPC is dynamically integer-typed for functions. 
* All arguments are implicitly signed 16-bit integers (`int`). You do not need to specify `int` before argument names in the function signature (e.g. use `function add(a, b)`, not `function add(int a, int b)`).
* The return value is also an `int`. If your function does not contain a `return` statement, it will return `0` by default.

### 2. Passed by Value
All variables passed to a function are **passed by value**, not by reference. This means the function receives a copy of the variable's value. If you modify an argument's value inside the function, it will not change the value of the original variable outside the function.

```c
int score = 10;

main {
    double_value(score);
    // score is STILL 10, because it was passed by value!
}

function double_value(val) {
    val = val * 2;
    return val;
}
```

### 3. Global Scope
All user-defined functions have a global scope and can be called from anywhere in the script — inside the `init` block, the `main` block, or inside combos.

### 4. No Recursion
GPC does not support recursive function calls (a function calling itself). Attempting to do so will result in compile-time errors or stack overflows on the Cronus Zen microprocessor.

---

## Code Example: Deadzone Correction Function

A common application of functions is correcting analog stick inputs. The function below checks if a stick's deflection is within a specific deadzone, and if not, scales it appropriately.

```c
int stick_x;
int stick_y;

main {
    // Call the custom deadzone check function for both stick axes
    stick_x = apply_deadzone(get_val(XB1_LX), 12);
    stick_y = apply_deadzone(get_val(XB1_LY), 12);
    
    set_val(XB1_LX, stick_x);
    set_val(XB1_LY, stick_y);
}

// Function defined at the very end of the GPC script
function apply_deadzone(raw_value, deadzone_limit) {
    int absolute_val = abs(raw_value);
    
    // If stick deflection is smaller than the deadzone, center it to 0
    if (absolute_val < deadzone_limit) {
        return 0;
    }
    
    // Otherwise, return the original value
    return raw_value;
}
```
