# Built-in GPC Functions

This page provides an exhaustive alphabetical reference for the built-in API functions supported by the Cronus Zen GPC language.

---

## Combo & Execution Functions

### `combo_run`
Triggers a combo block to start running asynchronously.
* **Syntax**: `combo_run(<combo_name>);`

### `combo_stop`
Stops a currently running combo block immediately.
* **Syntax**: `combo_stop(<combo_name>);`

### `combo_restart`
Restarts a combo from its first instruction, even if the combo is already active.
* **Syntax**: `combo_restart(<combo_name>);`

---

## Controller Input / Output Functions

### `get_val`
Reads the current value of a controller button or axis.
* **Syntax**: `get_val(<button_id>);`
* **Returns**: `0` to `100` (for buttons/triggers); `-100` to `100` (for analog axes).

### `set_val`
Overrides the output value of a button or axis sent to the console.
* **Syntax**: `set_val(<button_id>, <value>);`

### `get_lval`
Reads the value of a button/axis from the previous execution loop tick.
* **Syntax**: `get_lval(<button_id>);`

### `event_press`
Detects if a button was just pressed (transitioned from released to pressed).
* **Syntax**: `event_press(<button_id>);`
* **Returns**: `TRUE` (1) once per press event, otherwise `FALSE` (0).

### `event_release`
Detects if a button was just released (transitioned from pressed to released).
* **Syntax**: `event_release(<button_id>);`

### `get_ptime`
Returns the duration in milliseconds that a button has remained in its current state.
* **Syntax**: `get_ptime(<button_id>);`

### `block`
Blocks a button's output signal from reaching the console for a set duration.
* **Syntax**: `block(<button_id>, <time_ms>);`

### `unmap`
Disables a button's output entirely. Use `unmap ALL_REMAPS;` to clear all remappings.
* **Syntax**: `unmap(<button_id>);`

### `swap`
Swaps the logic values of two buttons at the software layer.
* **Syntax**: `swap(<button_id_1>, <button_id_2>);`

---

## Math & Trigonometry Functions

### `clamp`
Restricts an integer value within a specific range.
* **Syntax**: `clamp(<value>, <min>, <max>);`

### `abs`
Returns the absolute (positive) value of an integer.
* **Syntax**: `abs(<value>);`

### `random`
Generates a pseudo-random integer within the specified range (inclusive).
* **Syntax**: `random(<min>, <max>);`

### `inv`
Inverts the sign of a number (multiplies by `-1`).
* **Syntax**: `inv(<value>);`

### `get_polar`
Translates Cartesian stick axes coordinates (X, Y) into polar coordinates.
* **Syntax**: `get_polar(<stick_id>, <polar_type>);`
* **Types**: `POLAR_ANGLE` (0 to 359), `POLAR_RADIUS` (0 to 32767).

### `get_ipolar`
Retrieves original polar coordinate values directly from the controller before any script overrides.
* **Syntax**: `get_ipolar(<stick_id>, <polar_type>);`

---

## Device & Platform Diagnostics

### `get_console`
Returns the platform identifier representing the console the Zen is plugged into.
* **Syntax**: `get_console();`
* **Returns**: A `PIO_` constant (e.g. `PIO_PS5`, `PIO_XB1`).

### `get_controller`
Returns the platform profile of the controller currently plugged into the Zen.
* **Syntax**: `get_controller();`

### `get_rtime`
Returns the execution loop cycle duration of the main script block in milliseconds.
* **Syntax**: `get_rtime();`

### `get_info`
Queries real-time hardware status metrics.
* **Syntax**: `get_info(<info_type>);`
* **Types**: `INFO_CPU_LOAD` (0-100), `INFO_SLOT` (1-8), `INFO_VM_SPEED`.

---

## Storage & Memory Functions

### `get_pvar`
Reads a saved variable value from the slot's private EEPROM storage.
* **Syntax**: `get_pvar(<spvar_id>, <min>, <max>, <default_value>);`

### `set_pvar`
Saves an integer value to a slot-private persistent EEPROM variable.
* **Syntax**: `set_pvar(<spvar_id>, <value>);`
* **Note**: Do not call this continuously in the `main` loop to protect EEPROM longevity.

---

## Bitwise Manipulation Functions

### `set_bit`
Forces a specific bit index inside a variable to `1`.
* **Syntax**: `set_bit(<variable>, <bit_index>);`

### `clear_bit`
Forces a specific bit index inside a variable to `0`.
* **Syntax**: `clear_bit(<variable>, <bit_index>);`

### `test_bit`
Reads the state of a specific bit.
* **Syntax**: `test_bit(<value>, <bit_index>);`
* **Returns**: `TRUE` if the bit is `1`, `FALSE` if the bit is `0`.

---

## OLED Screen Functions

### `cls_oled`
Clears the OLED screen to black (`0`) or white (`1`).
* **Syntax**: `cls_oled(<color>);`

### `pixel_oled`
Draws a single pixel at coordinate (X, Y).
* **Syntax**: `pixel_oled(<x>, <y>, <color>);`

### `line_oled`
Draws a line from one point to another.
* **Syntax**: `line_oled(<x1>, <y1>, <x2>, <y2>, <thickness>, <color>);`

### `rect_oled`
Draws an outlined or filled rectangle.
* **Syntax**: `rect_oled(<x>, <y>, <width>, <height>, <fill_flag>, <color>);`

### `circle_oled`
Draws an outlined or filled circle.
* **Syntax**: `circle_oled(<x>, <y>, <radius>, <fill_flag>, <color>);`

### `putc_oled`
Pushes a character code into the rendering string buffer.
* **Syntax**: `putc_oled(<buffer_index>, <char_code>);`

### `puts_oled`
Renders the character string buffer at a specific coordinate.
* **Syntax**: `puts_oled(<x>, <y>, <font_id>, <num_chars>, <color>);`

---

## Rumble & LED Feedback Functions

### `set_rumble`
Triggers vibration on a specific motor.
* **Syntax**: `set_rumble(<rumble_id>, <strength>);`
* **IDs**: `RUMBLE_A` (heavy motor), `RUMBLE_B` (light motor).

### `reset_rumble`
Turns off all rumble motor vibration.
* **Syntax**: `reset_rumble();`

### `set_led`
Overrides an individual LED color channel on the controller or device.
* **Syntax**: `set_led(<led_id>, <state>);`
* **IDs**: `LED_1` (Blue), `LED_2` (Red), `LED_3` (Green), `LED_4` (Yellow).
* **States**: `0` (Off), `1` (On).

### `reset_leds`
Resets LED color channels back to default system mappings.
* **Syntax**: `reset_leds();`
