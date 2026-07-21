# Math & Utilities

Because GPC is designed for low-power embedded microcontrollers, standard decimal math (floating points) is unsupported. GPC includes built-in functions to keep operations fast, safe, and bound within controller limits.

---

## Utility Functions

### `clamp`
Constrains a value between a minimum and maximum limit. This is critical for preventing controller inputs from sending values beyond expected boundaries (like `-100` or `100`), which can cause unintended visual glitches in games.
* **Syntax**: `clamp(<value>, <min>, <max>)`
* **Example**:
  ```c
  main {
      // Limit Right Stick Y-axis input to a max of 80% strength
      int stick_y = get_val(XB1_RY);
      int restricted_y = clamp(stick_y, -80, 80);
      set_val(XB1_RY, restricted_y);
  }
  ```

### `abs`
Returns the absolute (positive) value of an integer.
* **Syntax**: `abs(<value>)`
* **Example**:
  ```c
  main {
      // Calculate how far stick is pushed from center, ignoring direction
      int drift_x = abs(get_val(XB1_RX));
      if (drift_x > 10) {
          // Input is outside deadzone
      }
  }
  ```

### `random`
Generates a pseudo-random integer between a minimum and maximum range (inclusive).
* **Syntax**: `random(<min>, <max>)`
* **Use Case**: Frequently used to randomize timing to prevent detection by anti-cheat systems analyzing for static delays.
* **Example**:
  ```c
  combo RandomizedRapidFire {
      set_val(XB1_RT, 100);
      // Wait for a random duration between 35ms and 55ms
      wait(random(35, 55));
      
      set_val(XB1_RT, 0);
      wait(random(35, 55));
  }
  ```

### `inv`
Inverts the sign of an integer. This is a shortcut for multiplying a variable by `-1`.
* **Syntax**: `inv(<value>)`
* **Example**:
  ```c
  main {
      // Invert stick behavior (invert Y-axis control)
      set_val(XB1_RY, inv(get_val(XB1_RY)));
  }
  ```

---

## Fixed-Point Math Patterns

Without floats, calculations like dividing a value by `2.5` must be structured differently.

### Pattern 1: Scaling up
Multiply your numbers by `10`, `100`, or `1000` to simulate decimal places, perform calculations, and divide at the end.

* **Problem**: You want to reduce stick sensitivity to exactly `85.5%` (`0.855`).
* **Solution**:
  ```c
  main {
      int stick_x = get_val(XB1_RX);
      // Multiply by 855 (representing 85.5% scaled by 1000)
      int reduced = (stick_x * 855) / 1000;
      set_val(XB1_RX, reduced);
  }
  ```

### Pattern 2: Rounding division
By default, dividing in GPC truncates the decimal component (e.g. `5 / 2 = 2`). To round to the nearest whole integer:
* Add half of the divisor before dividing for positive values.
* Subtract half of the divisor for negative values.

```c
// Normal truncation: (5 / 2) = 2
// Rounding logic: (5 + 1) / 2 = 3
int rounded_value = (numerator + (denominator / 2)) / denominator;
```
