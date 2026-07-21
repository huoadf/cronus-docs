# Bitwise & Persistent Storage

GPC allows you to perform low-level bit operations and save variables directly to the Cronus Zen's EEPROM flash memory. These features let you write memory-efficient scripts that save settings across device power-cycles.

---

## Bitwise Manipulation API

To conserve bytecode memory, you can pack multiple boolean state toggles into a single 16-bit integer variable. GPC includes built-in functions to set, clear, and test individual bits.

### `set_bit`
Forces a specific bit in a variable to `1` (ON).
* **Syntax**: `set_bit(<variable>, <bit_index>);`
* **Bit Index**: `0` to `15` (for standard 16-bit integers).

### `clear_bit`
Forces a specific bit in a variable to `0` (OFF).
* **Syntax**: `clear_bit(<variable>, <bit_index>);`

### `test_bit`
Reads the state of a specific bit.
* **Syntax**: `test_bit(<value>, <bit_index>);`
* **Returns**: `TRUE` (1) if the bit is `1`, or `FALSE` (0) if the bit is `0`.

### C-Style Operators
You can also use standard C bitwise operators for manual adjustments:
* `&` : Bitwise AND
* `|` : Bitwise OR
* `^` : Bitwise XOR
* `~` : Bitwise NOT
* `<<` : Left shift
* `>>` : Right shift

### Example: Storing Flag States
```c
int toggles = 0; // Packed flags: Bit 0 = RapidFire, Bit 1 = AntiRecoil, Bit 2 = AutoSprint

main {
    // Check if Rapid Fire is enabled (Bit 0)
    if (test_bit(toggles, 0)) {
        combo_run(RapidFire);
    }
    
    // Toggle Anti-Recoil (Bit 1)
    if (event_press(XB1_Y)) {
        if (test_bit(toggles, 1)) {
            clear_bit(toggles, 1);
        } else {
            set_bit(toggles, 1);
        }
    }
}
```

---

## Persistent Variables (SPVAR)

The Cronus Zen has a built-in EEPROM chip that allows you to store **Slot Persistent Variables (SPVARs)**. The Zen reserves **64 private variables** (`SPVAR_1` to `SPVAR_64`) per memory slot.
* Settings saved on Slot 1 are isolated and cannot be accessed or overwritten by Slot 2.
* Values are retained in memory even if the Zen is unplugged or powered down.

### `set_pvar`
Saves an integer value to a persistent variable.
* **Syntax**: `set_pvar(<spvar_constant>, <value>);`
* **Parameters**:
  * `<spvar_constant>`: Identifier constant from `SPVAR_1` to `SPVAR_64`.
  * `<value>`: Integer value to write.

### `get_pvar`
Retrieves a saved value from a persistent variable.
* **Syntax**: `get_pvar(<spvar_constant>, <min>, <max>, <default_value>);`
* **Parameters**:
  * `<spvar_constant>`: Identifier constant.
  * `<min>` / `<max>`: Range bounds validation.
  * `<default_value>`: Fallback value returned if the saved value falls outside min/max or the EEPROM slot is blank (e.g. first-time run).

---

## EEPROM Protection Guidelines

{% hint style="danger" %}
**EEPROM Wear & Degradation Limit**
Vibration and data writes physically stress flash memory cells. The Zen's EEPROM has a limited write cycle lifetime. 
**Never call `set_pvar()` continuously inside the `main` loop on every tick.**
Only write to persistent variables inside conditional blocks triggered by a specific event (like a button press or when exiting a config menu).
{% endhint %}

### Correct Implementation Pattern: Save-on-Event

```c
int recoil_force;

init {
    // Load saved recoil setting at script startup (default to 20 if blank)
    recoil_force = get_pvar(SPVAR_1, 5, 80, 20);
}

main {
    // Increase recoil setting with D-pad UP
    if (event_press(XB1_UP)) {
        recoil_force = clamp(recoil_force + 2, 5, 80);
        
        // SAFE: set_pvar is only called ONCE when button is pressed, not held
        set_pvar(SPVAR_1, recoil_force); 
        combo_run(RumbleFeedback);
    }
}

combo RumbleFeedback {
    set_rumble(RUMBLE_A, 30);
    wait(100);
    reset_rumble();
}
```

---

## Bit-Packing SPVARs

If you need to store more than 64 settings, or want to consolidate saving, you can pack multiple configurations into a single SPVAR slot using shift math.

* **Formula**: `packed_value = settingA | (settingB << 8) | (settingC << 12)`
* **Extraction**: `settingB = (packed_value >> 8) & 0xF`

### Bit-Packing Sample Code

```c
int sens_profile;  // 0 - 3 (Requires 2 bits)
int rapid_fire;    // TRUE/FALSE (Requires 1 bit)
int recoil_power;  // 0 - 100 (Requires 7 bits)

init {
    int packed = get_pvar(SPVAR_1, 0, 32767, 0);
    
    // Unpack:
    sens_profile = packed & 0x03;          // Read first 2 bits
    rapid_fire   = (packed >> 2) & 0x01;   // Read next 1 bit
    recoil_power = (packed >> 3) & 0x7F;   // Read next 7 bits
}

main {
    // Trigger Save setting event
    if (event_press(XB1_MENU)) {
        // Pack variables:
        int packed = sens_profile | (rapid_fire << 2) | (recoil_power << 3);
        
        set_pvar(SPVAR_1, packed); // Save consolidated value
        combo_run(RumbleFeedback);
    }
}
```
