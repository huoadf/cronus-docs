# API Samples

This page provides various GPC API code samples demonstrating advanced implementations such as Bit-Packing states, runtime adjustments, and SendMsgAppSample interop hooks.

---

## Sample 1: Bit-Packed Option Menus

This script stores 4 separate configuration settings (Auto-Sprint, Rapid Fire, Anti-Recoil Strength, and Target Assist) inside a single persistent variable (`SPVAR_1`), conserving EEPROM slots.

```c
// Setting bounds
define MAX_RECOIL = 60;
define MIN_RECOIL = 5;

// Variables
int auto_sprint;  // 0 - 1 (1 bit)
int rapid_fire;   // 0 - 1 (1 bit)
int assist_type;  // 0 - 3 (2 bits)
int recoil_force; // 5 - 60 (6 bits)

init {
    // 1. Retrieve the packed value from persistent storage (default to 0)
    int packed = get_pvar(SPVAR_1, 0, 32767, 0);
    
    // 2. Unpack the values using shift and mask logic
    auto_sprint  = packed & 0x01;          // Bit 0
    rapid_fire   = (packed >> 1) & 0x01;   // Bit 1
    assist_type  = (packed >> 2) & 0x03;   // Bits 2-3
    recoil_force = (packed >> 4) & 0x3F;   // Bits 4-9
    
    // 3. Fallback defaults if first-time run
    if (recoil_force == 0) {
        recoil_force = 20; // Default recoil
    }
}

main {
    // Save settings trigger: Press VIEW + MENU simultaneously
    if (get_val(XB1_VIEW) && event_press(XB1_MENU)) {
        // Pack the states back into a single integer
        int packed = auto_sprint | (rapid_fire << 1) | (assist_type << 2) | (recoil_force << 4);
        
        // Save to slot private memory
        set_pvar(SPVAR_1, packed);
        combo_run(RumbleConfirm);
    }
}

combo RumbleConfirm {
    set_rumble(RUMBLE_B, 40);
    wait(150);
    reset_rumble();
}
```

---

## Sample 2: Double-Tap Activation

Detects if a user double-taps a specific button within a set time window, which is useful for activating macros like a slide cancel or quick reload.

```c
define DOUBLE_TAP_WINDOW = 250; // Milliseconds allowed between taps

int tap_timer = 0;
int tap_count = 0;

main {
    // Decrement tap window timer
    if (tap_timer > 0) {
        tap_timer = tap_timer - get_rtime();
    } else {
        tap_count = 0; // Window closed, reset count
    }

    // Monitor reload button tap event
    if (event_press(XB1_X)) {
        tap_count = tap_count + 1;
        
        if (tap_count == 1) {
            tap_timer = DOUBLE_TAP_WINDOW; // Start window
        } else if (tap_count == 2 && tap_timer > 0) {
            // Success: Double tap detected!
            combo_run(QuickReloadCancel);
            tap_count = 0;
            tap_timer = 0;
        }
    }
}

combo QuickReloadCancel {
    // Trigger double tap macro action
    set_val(XB1_Y, 100);
    wait(50);
    set_val(XB1_Y, 0);
    wait(50);
    set_val(XB1_Y, 100);
    wait(50);
    set_val(XB1_Y, 0);
}
```

---

## Sample 3: Custom OLED Menu Wrapper Function

This script wraps the text buffer calls into a modular, reusable function, saving bytecode space compared to repetitive inline code block arrays.

```c
define OLED_FONT_SMALL = 0;

main {
    if (event_press(XB1_UP)) {
        // Clear screen and draw menu title
        cls_oled(0);
        draw_text_string(0, 0, "MENU ACTIVE");
    }
}

// Custom wrapper function (defined at the very end of the GPC script)
function draw_text_string(x, y, string_ptr) {
    int i = 0;
    int character;
    
    // GPC strings are arrays of character bytes passed by reference
    // Loop until we reach the string null-terminator (ASCII 0)
    while (string_ptr[i] != 0) {
        character = string_ptr[i];
        putc_oled(i, character);
        i = i + 1;
    }
    
    // Render string to coordinates
    puts_oled(x, y, OLED_FONT_SMALL, i, 1);
}
```
