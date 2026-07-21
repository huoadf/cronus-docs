# Combos & Timing

GPC scripts use combos to execute automated macro sequences that require specific timing. Since the virtual machine execution loop must never block, combos run asynchronously parallel to the `main` block.

---

## Combo Subroutines

A `combo` block is a sequence of assignments (`set_val`) and timing delays (`wait`). 

### Writing a Combo

```c
combo JumpShot {
    set_val(XB1_A, 100);    // Press Jump (A/Cross)
    wait(80);               // Hold for 80 milliseconds
    set_val(XB1_A, 0);      // Release Jump
    wait(100);              // Wait 100 milliseconds
    set_val(XB1_RT, 100);   // Fire weapon
    wait(150);              // Keep firing for 150ms
}
```

### How Combos Execute
1. When a combo starts, it executes instructions sequentially.
2. The `wait(time)` command pauses execution of **that combo** for the specified duration (in milliseconds).
3. While the combo is waiting, the Zen's `main` block continues to execute on every single tick. It does not freeze!
4. The variables set inside a combo (like `set_val(XB1_A, 100)`) remain active until modified by another line in the combo, or overridden by the `main` loop.

---

## Combo Control Functions

### `combo_run`
Triggers the execution of a combo.
* **Syntax**: `combo_run(<combo_name>)`
* **Behavior**: If the combo is already running, calling `combo_run` has no effect (it does not restart it).
* **Example**:
  ```c
  main {
      if (get_val(XB1_RT)) {
          combo_run(RapidFire);
      }
  }
  ```

### `combo_stop`
Stops the execution of a running combo immediately.
* **Syntax**: `combo_stop(<combo_name>)`
* **Example**:
  ```c
  main {
      // Stop the reload macro if the user starts shooting
      if (get_val(XB1_RT)) {
          combo_stop(AutoReload);
      }
  }
  ```

---

## Timing Functions

### `get_ptime`
Returns the duration (in milliseconds) that a button or stick has spent in its current state.
* **Syntax**: `get_ptime(<identifier>)`
* **Behavior**: Every time the button is pressed, released, or its stick axis changes value, the internal timer for that input resets to `0`.
* **Example**:
  ```c
  main {
      // Long Press: Run combo only if holding the button for more than 500ms
      if (get_val(XB1_X) && get_ptime(XB1_X) > 500) {
          combo_run(SuperJump);
      }
  }
  ```

### `get_rtime`
Returns the loop iteration time (in milliseconds) of the `main` block. This tells you how long the last cycle of the script took to run.
* **Syntax**: `get_rtime()`
* **Use Case**: Used to increment custom timers inside the main loop independently of controller events.
* **Example**:
  ```c
  int timer = 0;

  main {
      if (timer > 0) {
          // Decrement the timer based on actual loop time elapsed
          timer = timer - get_rtime();
      }
      
      if (event_press(XB1_Y)) {
          timer = 2000; // Set timer to 2000ms
      }
  }
  ```
