# Controller Identifiers

GPC scripts use platform-agnostic integer indices to represent controller inputs. Zen Studio automatically maps these indices to platform-specific labels (constants) to make scripts readable.

---

## PlayStation 5 & Xbox Series X|S Identifiers

Modern console controllers feature new buttons (like the Share/Capture button) which have dedicated identifiers on the Cronus Zen.

### Xbox Series X|S Mappings

* **`XB1_SHARE`**: Represents the physical Share button located in the center of the Xbox Series X|S controller.
* All other buttons (`XB1_A`, `XB1_B`, `XB1_RT`, etc.) retain their standard mappings from the Xbox One profile.

### PlayStation 5 Mappings

* **`PS5_CREATE`**: Represents the physical Create/Share button on the DualSense controller.
* **`PS5_TOUCH`**: Represents clicking the dual-point capacitive touchpad.
* **`PS5_MUTE`**: Represents the built-in microphone mute button.
* Standard buttons use the `PS5_` prefixes (e.g. `PS5_CROSS`, `PS5_CIRCLE`, `PS5_L2`, `PS5_R2`).

---

## Universal Button Mapping Table

Because GPC buttons are compiled down to integer index positions (`0` to `20`), platform-specific aliases are interchangeable. A script written with `XB1_RT` runs identically when using a PS5 controller on a PS5 console.

The table below lists the universal GPC indices and their equivalents:

| Index | Generic Name | Xbox Constant | PlayStation Constant | Switch Constant |
| :--- | :--- | :--- | :--- | :--- |
| **0** | `PS` / `HOME` | `XB1_HOME` | `PS4_PS` / `PS5_PS` | `SWITCH_HOME` |
| **1** | `SHARE` / `VIEW` | `XB1_VIEW` / `XB1_SHARE` | `PS4_SHARE` / `PS5_CREATE` | `SWITCH_CAPTURE` |
| **2** | `OPTIONS` / `MENU` | `XB1_MENU` | `PS4_OPTIONS` / `PS5_OPTIONS` | `SWITCH_PLUS` |
| **3** | `R1` / `RB` | `XB1_RB` | `PS4_R1` / `PS5_R1` | `SWITCH_R` |
| **4** | `R2` / `RT` | `XB1_RT` | `PS4_R2` / `PS5_R2` | `SWITCH_ZR` |
| **5** | `R3` / `RS` | `XB1_RS` | `PS4_R3` / `PS5_R3` | `SWITCH_SR` |
| **6** | `L1` / `LB` | `XB1_LB` | `PS4_L1` / `PS5_L1` | `SWITCH_L` |
| **7** | `L2` / `LT` | `XB1_LT` | `PS4_L2` / `PS5_L2` | `SWITCH_ZL` |
| **8** | `L3` / `LS` | `XB1_LS` | `PS4_L3` / `PS5_L3` | `SWITCH_SL` |
| **9** | `RX` (Right Stick X) | `XB1_RX` | `PS4_RX` / `PS5_RX` | `SWITCH_RX` |
| **10** | `RY` (Right Stick Y) | `XB1_RY` | `PS4_RY` / `PS5_RY` | `SWITCH_RY` |
| **11** | `LX` (Left Stick X) | `XB1_LX` | `PS4_LX` / `PS5_LX` | `SWITCH_LX` |
| **12** | `LY` (Left Stick Y) | `XB1_LY` | `PS4_LY` / `PS5_LY` | `SWITCH_LY` |
| **13** | `UP` (D-pad) | `XB1_UP` | `PS4_UP` / `PS5_UP` | `SWITCH_UP` |
| **14** | `DOWN` (D-pad) | `XB1_DOWN` | `PS4_DOWN` / `PS5_DOWN` | `SWITCH_DOWN` |
| **15** | `LEFT` (D-pad) | `XB1_LEFT` | `PS4_LEFT` / `PS5_LEFT` | `SWITCH_LEFT` |
| **16** | `RIGHT` (D-pad) | `XB1_RIGHT` | `PS4_RIGHT` / `PS5_RIGHT` | `SWITCH_RIGHT` |
| **17** | `TRIANGLE` / `Y` | `XB1_Y` | `PS4_TRIANGLE` / `PS5_TRIANGLE` | `SWITCH_X` |
| **18** | `CIRCLE` / `B` | `XB1_B` | `PS4_CIRCLE` / `PS5_CIRCLE` | `SWITCH_A` |
| **19** | `CROSS` / `A` | `XB1_A` | `PS4_CROSS` / `PS5_CROSS` | `SWITCH_B` |
| **20** | `SQUARE` / `X` | `XB1_X` | `PS4_SQUARE` / `PS5_SQUARE` | `SWITCH_Y` |

---

## Keyboard & Mouse Mapping (KBM)

When using a Keyboard and Mouse connected to the Cronus Zen, the Zen maps key presses and mouse movements to these same controller indices based on your **Input Translator** file (`.git` layout mapping configured in Zen Studio). 

For example, moving your physical mouse to the right sends a positive X value to the `XB1_RX` (Index 9) channel, and pressing **W** on your keyboard maps to a negative Y value on the `XB1_LY` (Index 12) channel.
