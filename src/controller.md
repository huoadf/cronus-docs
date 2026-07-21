# Controller Hardware

GPC scripts can control hardware feedback features on the controller and Cronus Zen, including rumble motors and LED indicators. This section covers hardware interaction APIs and the standard layout constants.

---

## Rumble Control

You can trigger the controller's internal vibration motors (rumble) to provide tactile feedback to the user when they toggle script options.

### `set_rumble`
Triggers one of the controller's rumble motors.
* **Syntax**: `set_rumble(<rumble_id>, <strength>)`
* **Parameters**:
  * `<rumble_id>`: `RUMBLE_A` (Large/heavy motor) or `RUMBLE_B` (Small/high-frequency motor).
  * `<strength>`: Vibration speed percentage (integer between `0` and `100`).
* **Example**:
  ```c
  combo RumbleFeedback {
      set_rumble(RUMBLE_A, 40); // Turn heavy motor on at 40% strength
      wait(150);                // Vibrate for 150ms
      reset_rumble();           // Turn off motors
  }
  ```

### `reset_rumble`
Turns off all active rumble motors immediately.
* **Syntax**: `reset_rumble()`

---

## LED Control

You can change the color of the Cronus Zen's backlight or the controller's built-in lightbar (e.g. PlayStation Lightbar).

### `set_led`
Modifies the state of an individual color channel.
* **Syntax**: `set_led(<led_id>, <state>)`
* **Parameters**:
  * `<led_id>`: `LED_1` (Blue), `LED_2` (Red), `LED_3` (Green), `LED_4` (Yellow).
  * `<state>`: `0` (Off) or `1` (On).
* **Example**:
  ```c
  main {
      if (rapid_fire_active) {
          set_led(LED_3, 1); // Turn Green LED on
          set_led(LED_2, 0); // Turn Red LED off
      } else {
          set_led(LED_3, 0); // Turn Green LED off
          set_led(LED_2, 1); // Turn Red LED on
      }
  }
  ```

### `reset_leds`
Resets LEDs to their default system behaviors.
* **Syntax**: `reset_leds()`

---

## Button Mappings Reference

The Cronus Zen maps inputs to platform-agnostic integer constants. Zen Studio understands the following button mappings automatically. 

| Index | Xbox Identity | PlayStation Identity |
| :--- | :--- | :--- |
| `0` | `XB1_HOME` | `PS4_PS` |
| `1` | `XB1_VIEW` | `PS4_SHARE` |
| `2` | `XB1_MENU` | `PS4_OPTIONS` |
| `3` | `XB1_RB` | `PS4_R1` |
| `4` | `XB1_RT` | `PS4_R2` |
| `5` | `XB1_RS` | `PS4_R3` |
| `6` | `XB1_LB` | `PS4_L1` |
| `7` | `XB1_LT` | `PS4_L2` |
| `8` | `XB1_LS` | `PS4_L3` |
| `9` | `XB1_RX` | `PS4_RX` |
| `10` | `XB1_RY` | `PS4_RY` |
| `11` | `XB1_LX` | `PS4_LX` |
| `12` | `XB1_LY` | `PS4_LY` |
| `13` | `XB1_UP` | `PS4_UP` |
| `14` | `XB1_DOWN` | `PS4_DOWN` |
| `15` | `XB1_LEFT` | `PS4_LEFT` |
| `16` | `XB1_RIGHT` | `PS4_RIGHT` |
| `17` | `XB1_Y` | `PS4_TRIANGLE` |
| `18` | `XB1_B` | `PS4_CIRCLE` |
| `19` | `XB1_A` | `PS4_CROSS` |
| `20` | `XB1_X` | `PS4_SQUARE` |

{% hint style="info" %}
In GPC, `XB1_` and `PS4_` labels are aliases pointing to the same index. E.g., `XB1_RT` and `PS4_R2` are compiled to the exact same value (`4`). Scripts written with `XB1_RT` work perfectly on PlayStation consoles, and vice versa.
{% endhint %}
