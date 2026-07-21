# Input & Output API

The core capability of GPC scripting is inspecting physical buttons and sticks, modifying their values, and outputting the results. This section details the functions used to interact with controller inputs.

---

## Reading Inputs

### `get_val`
Reads the current value of a controller input.
* **Syntax**: `get_val(<identifier>)`
* **Returns**: An integer. For buttons and triggers, it returns `0` (released) to `100` (fully pressed). For analog sticks, it returns a value from `-100` to `100`.
* **Example**:
  ```c
  main {
      // Check if Right Stick Y-axis (vertical) is pushed down past 50%
      if (get_val(XB1_RY) > 50) {
          // Do something
      }
  }
  ```

### `get_lval`
Reads the value of a controller input from the *previous* execution frame. Useful for detecting changes in analog stick positions or trigger changes.
* **Syntax**: `get_lval(<identifier>)`
* **Example**:
  ```c
  main {
      // Compare current stick value to previous frame
      if (get_val(XB1_RX) != get_lval(XB1_RX)) {
          // Right Stick X-axis is moving
      }
  }
  ```

---

## Trigger Events

### `event_press`
Detects if a button was pressed during the current frame. This function only returns `TRUE` once per button press event.
* **Syntax**: `event_press(<identifier>)`
* **Returns**: `TRUE` (1) if the button transitioned from released to pressed in the current cycle, otherwise `FALSE` (0).
* **Example**:
  ```c
  main {
      // Toggle a feature when pressing the button once
      if (event_press(XB1_Y)) {
          toggleState = !toggleState;
      }
  }
  ```

### `event_release`
Detects if a button was released during the current frame.
* **Syntax**: `event_release(<identifier>)`
* **Returns**: `TRUE` (1) if the button transitioned from pressed to released, otherwise `FALSE` (0).
* **Example**:
  ```c
  main {
      // Run reload macro when reloading button is released
      if (event_release(XB1_X)) {
          combo_run(ReloadMacro);
      }
  }
  ```

---

## Overwriting & Blocking Outputs

### `set_val`
Overrides the physical value of a button or stick and sends the new value to the console or PC.
* **Syntax**: `set_val(<identifier>, <value>)`
* **Parameters**:
  * `<identifier>`: The controller button/axis to override.
  * `<value>`: The value to set (integer between `-100` and `100`).
* **Example**:
  ```c
  main {
      // Auto-sprint: If pushing Left Stick forward (negative Y values), force press LS button
      if (get_val(XB1_LY) < -90) {
          set_val(XB1_LS, 100);
      }
  }
  ```

### `block`
Blocks output signals from a specific button from reaching the console for a specified duration.
* **Syntax**: `block(<identifier>, <time_ms>)`
* **Example**:
  ```c
  main {
      // If pressing Menu button, block the signal for 200ms to allow local script action
      if (event_press(XB1_MENU)) {
          block(XB1_MENU, 200);
          combo_run(LocalMenuLogic);
      }
  }
  ```

## Remapping & Unmapping

Remapping changes how buttons are mapped from the controller to the console. GPC provides compile-time remappings and runtime modifications.

### `remap`
Assigns a controller button to a different output destination.
* **Syntax**: `remap <physical_input> -> <virtual_output>;`
* **Placement**: Must be placed at the **very beginning of the script** (before `init` and `main`).
* **Behavior**: Remappings are processed at the *end* of each tick. Therefore, in your GPC script logic (like `get_val`), **always reference the physical button**, not the remapped button.

```c
// Force physical Cross/A button to send Square/X signals to the console
remap PS4_CROSS -> PS4_SQUARE;

main {
    // If the physical CROSS button is pressed
    if (event_press(PS4_CROSS)) {
        // Run logic. The console will still receive PS4_SQUARE.
    }
}
```

### `unmap`
Disconnects a button's output channel so the console never registers it, although the GPC script can still read it using `get_val()`.
* **Syntax**: `unmap <identifier>;`
* **Syntax (Clear all)**: `unmap ALL_REMAPS;` (clears all current script remappings).
* **Example**:
  ```c
  init {
      // Disconnect the Back/View button from the console so we can use it as a custom script toggle
      unmap(XB1_VIEW);
  }
  ```

### `swap`
Swaps the values of two controller buttons at the software layer.
* **Syntax**: `swap(<button_1>, <button_2>);`
* **Example**:
  ```c
  init {
      // Flipped layout: Swap bumpers and triggers
      swap(XB1_LB, XB1_LT);
      swap(XB1_RB, XB1_RT);
  }
  ```
