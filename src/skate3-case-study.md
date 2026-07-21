# Case Study: Skate 3 Speed Glitch

This page provides a deep-dive analysis of a real-world GPC script used to automate speed glitches in *Skate 3* (Version 1.10 by Void Vids). It integrates almost every GPC concept — including screen management, multi-mode profiles, LED controls, screen savers, complex stick-movement combos, and custom layout functions.

---

## Complete Script Source

Below is the verified working script. Save this as a `.gpc` file in Zen Studio to compile and run it.

```c
// GPC Online Library
// skate_3_speed_glitch
// Version: 1.10
// Author: Void Vids
// Link: https://gpclib.cmindapi.com/gpc-library/10116

enum {
    AUTO_THROW,
    NO_THROW,
    FOWARD,
    CANNON,
    OFF
}

const string Title1 = "Void's";
const string Title2 = "Skate 3 Script";

const string Modnames[] = {
    "AutoThrow",
    "NoThrow",
    "Fowardman",
    "Cannon",
    "Off"
}

define Screen_Saver_Time = 15000;

int activeMod;
int screen_saver_timer = Screen_Saver_Time;

init {
    cls_oled(OLED_BLACK);
    print(center_x(sizeof(Title1) - 1, OLED_FONT_LARGE_WIDTH), 10, OLED_FONT_LARGE, OLED_WHITE, Title1[0]);
    print(center_x(sizeof(Title2) - 1, OLED_FONT_SMALL_WIDTH), 40, OLED_FONT_SMALL, OLED_WHITE, Title2[0]);
}

main {
    // Cycle active mods: Hold L2 and press D-pad RIGHT
    if(get_val(PS3_L2) && event_press(PS3_RIGHT)) {
        activeMod++;
        combo_run(RumbleNotifier);
        if(activeMod >= 5) {
            activeMod = 0;
        }
        cls_oled(OLED_BLACK);
        print(16, 22, OLED_FONT_MEDIUM, OLED_WHITE, Modnames[activeMod]);
        print(center_x(sizeof(Title2) - 1, OLED_FONT_SMALL_WIDTH), 40, OLED_FONT_SMALL, OLED_WHITE, Title2[0]);
        screen_saver_timer = Screen_Saver_Time;
    }

    // Run active mod logic
    if(activeMod == AUTO_THROW) {
        colorled(0, 0, 1, 0); // Blue LED
        if (get_val(PS3_LEFT)) {
            combo_run(throw);
        }
    }

    if(activeMod == NO_THROW) {
        colorled(0, 1, 0, 0); // Red LED
        if (get_val(PS3_LEFT)) {
            combo_run(nothrow);
        }
    }

    if(activeMod == FOWARD) {
        colorled(1, 1, 0, 0); // Pink/Purple LED
        if (get_val(PS3_LEFT)) {
            combo_run(foward);
        }
    }
    
    if(activeMod == CANNON) {
        colorled(1, 0, 1, 0); // Cyan/Teal LED
        if (get_val(PS3_LEFT)) {
            combo_run(cannon);
        }
    }

    if(activeMod == OFF) {
        colorled(0, 0, 0, 0); // Turn LEDs off
    }

    // Screen Saver: Clear screen after 15 seconds of inactivity to prevent burn-in
    if(screen_saver_timer) {
        if(screen_saver_timer <= get_rtime()) {
            cls_oled(OLED_BLACK);
        }
        screen_saver_timer = max(0, screen_saver_timer - get_rtime());
    }
}

// --- COMBOS (Speed Glitch Macros) ---

combo throw {
    set_val(PS3_R2, 100);
    wait(220);
    set_val(PS3_R2, 0);
    wait(50);
    set_val(PS3_SQUARE, 100);
    wait(470);
    set_val(PS3_R1, 100);
    set_val(PS3_SQUARE, 0);
    wait(110);
    set_val(PS3_R1, 0);
    wait(40);
    set_val(PS3_TRIANGLE, 100);
    wait(120);
    set_val(PS3_TRIANGLE, 0);
}

combo nothrow {
    set_val(PS3_SQUARE, 100);
    wait(470);
    set_val(PS3_R1, 100);
    set_val(PS3_SQUARE, 0);
    wait(110);
    set_val(PS3_R1, 0);
    wait(40);
    set_val(PS3_TRIANGLE, 100);
    wait(120);
    set_val(PS3_TRIANGLE, 0);
}

combo foward {
    set_val(PS3_R2, 100);
    wait(160);
    set_val(PS3_R2, 0);
    wait(10);
    set_val(PS3_LY, -20);
    wait(10);
    set_val(PS3_LY, -35);
    wait(10);
    set_val(PS3_LY, -55);
    wait(10);
    set_val(PS3_LY, -70);
    wait(10);
    set_val(PS3_R1, 100);
    set_val(PS3_LY, -84);
    wait(10);
    set_val(PS3_R1, 100);
    set_val(PS3_LY, -95);
    wait(10);
    set_val(PS3_R1, 100);
    set_val(PS3_LY, -100);
    wait(70);
    set_val(PS3_R1, 100);
    set_val(PS3_LY, -100);
    set_val(PS3_CROSS, 100);
    wait(990);
    set_val(PS3_R1, 100);
    set_val(PS3_LY, -100);
    set_val(PS3_CROSS, 100);
    set_val(PS3_SQUARE, 100);
    wait(30);
    set_val(PS3_R1, 100);
    set_val(PS3_LY, -100);
    set_val(PS3_CROSS, 0);
    set_val(PS3_SQUARE, 100);
    wait(130);
    
    // Smooth Right Stick rotation logic to execute the glitch
    set_val(PS3_R1, 100);
    set_val(PS3_RX, -23);
    set_val(PS3_RY, 27);
    set_val(PS3_LY, -100);
    set_val(PS3_SQUARE, 100);
    wait(10);
    set_val(PS3_R1, 100);
    set_val(PS3_RX, -34);
    set_val(PS3_RY, 41);
    set_val(PS3_LY, -100);
    set_val(PS3_SQUARE, 100);
    wait(10);
    set_val(PS3_R1, 100);
    set_val(PS3_RX, -45);
    set_val(PS3_RY, 56);
    set_val(PS3_LY, -100);
    set_val(PS3_SQUARE, 100);
    wait(10);
    set_val(PS3_R1, 100);
    set_val(PS3_RX, -53);
    set_val(PS3_RY, 69);
    set_val(PS3_LY, -100);
    set_val(PS3_SQUARE, 100);
    wait(10);
    set_val(PS3_R1, 100);
    set_val(PS3_RX, -64);
    set_val(PS3_RY, 85);
    set_val(PS3_LY, -100);
    set_val(PS3_SQUARE, 100);
    wait(10);
    set_val(PS3_R1, 100);
    set_val(PS3_RX, -70);
    set_val(PS3_RY, 97);
    set_val(PS3_LY, -100);
    set_val(PS3_SQUARE, 100);
    wait(10);
    set_val(PS3_R1, 100);
    set_val(PS3_RX, -71);
    set_val(PS3_RY, 100);
    set_val(PS3_LY, -100);
    set_val(PS3_SQUARE, 100);
    wait(10);
    set_val(PS3_R1, 100);
    set_val(PS3_RX, -70);
    set_val(PS3_RY, 100);
    set_val(PS3_LY, -100);
    set_val(PS3_SQUARE, 0);
    wait(90);
    set_val(PS3_R1, 100);
    set_val(PS3_RX, -70);
    set_val(PS3_RY, 100);
    set_val(PS3_LY, 0);
    wait(40);
    set_val(PS3_R1, 0);
    set_val(PS3_RX, -70);
    set_val(PS3_RY, 100);
    wait(40);
    set_val(PS3_RX, -74);
    set_val(PS3_RY, 100);
    wait(10);
    set_val(PS3_RX, -78);
    set_val(PS3_RY, 100);
    wait(10);
    set_val(PS3_RX, -82);
    set_val(PS3_RY, 100);
    wait(20);
    set_val(PS3_RX, -82);
    set_val(PS3_RY, 94);
    wait(10);
    set_val(PS3_RX, -85);
    set_val(PS3_RY, 92);
    wait(10);
    set_val(PS3_RX, -87);
    set_val(PS3_RY, 90);
    wait(10);
    set_val(PS3_RX, -89);
    set_val(PS3_RY, 86);
    wait(10);
    set_val(PS3_RX, -96);
    set_val(PS3_RY, 81);
    wait(10);
    set_val(PS3_RX, -96);
    set_val(PS3_RY, 72);
    wait(10);
    set_val(PS3_RX, -100);
    set_val(PS3_RY, 69);
    wait(10);
    set_val(PS3_RX, -100);
    set_val(PS3_RY, 67);
    wait(10);
    set_val(PS3_RX, -98);
    set_val(PS3_RY, 52);
    wait(10);
    set_val(PS3_RX, -76);
    set_val(PS3_RY, 26);
    wait(10);
    set_val(PS3_RX, -44);
    set_val(PS3_RY, 0);
    wait(10);
    set_val(PS3_RX, 0);
    wait(40);
    
    // Jump cancel sequence
    set_val(PS3_TRIANGLE, 100);
    wait(100);
    set_val(PS3_DOWN, 100);
    set_val(PS3_TRIANGLE, 100);
    wait(30);
    set_val(PS3_DOWN, 100);
    set_val(PS3_TRIANGLE, 0);
    wait(70);
    set_val(PS3_DOWN, 0);
}

combo cannon {
    set_val(PS3_R2, 22);
    wait(10);
    set_val(PS3_R2, 30);
    wait(10);
    set_val(PS3_R2, 40);
    wait(10);
    set_val(PS3_R2, 48);
    wait(10);
    set_val(PS3_R2, 57);
    wait(10);
    set_val(PS3_R2, 69);
    wait(10);
    set_val(PS3_R2, 86);
    wait(10);
    set_val(PS3_R2, 100);
    wait(140);
    set_val(PS3_R2, 70);
    set_val(PS3_LY, -20);
    wait(10);
    set_val(PS3_R2, 43);
    set_val(PS3_LY, -26);
    wait(10);
    set_val(PS3_R2, 25);
    set_val(PS3_LY, -35);
    wait(10);
    set_val(PS3_R2, 0);
    set_val(PS3_LY, -42);
    wait(10);
    set_val(PS3_LY, -54);
    wait(10);
    set_val(PS3_LY, -56);
    wait(10);
    set_val(PS3_LY, -67);
    wait(10);
    set_val(PS3_LY, -74);
    wait(10);
    set_val(PS3_LY, -76); 
    wait(10);
    set_val(PS3_LY, -85);
    set_val(PS3_CROSS, 100);
    wait(10);
    set_val(PS3_LY, -92);
    set_val(PS3_CROSS, 100);
    wait(10);
    set_val(PS3_LY, -100);
    set_val(PS3_CROSS, 100);
    wait(1270);
    set_val(PS3_LY, -100);
    set_val(PS3_CROSS, 100);
    set_val(PS3_SQUARE, 100);
    wait(40);
    set_val(PS3_LY, -100);
    set_val(PS3_CROSS, 0);
    set_val(PS3_SQUARE, 100);
    wait(70);
    set_val(PS3_LY, -100);
    set_val(PS3_SQUARE, 0);
    wait(120);
    set_val(PS3_RY, -36);
    set_val(PS3_LY, -100);
    wait(10);
    set_val(PS3_RY, -63);
    set_val(PS3_LY, -100);
    wait(10);
    set_val(PS3_RY, -94);
    set_val(PS3_LY, -100);
    wait(10);
    set_val(PS3_RY, -100);
    set_val(PS3_LY, -88);
    wait(10);
    set_val(PS3_RY, -100);
    set_val(PS3_LY, 42);
    wait(10);
    set_val(PS3_RY, -100);
    set_val(PS3_LY, 0);
    wait(250);
    set_val(PS3_RY, -73);
    wait(10);
    set_val(PS3_RY, 49);
    wait(10);
    set_val(PS3_RY, -24);
    wait(10);
    set_val(PS3_RY, 0);
    wait(10);
    set_val(PS3_TRIANGLE, 100);
    wait(60);
    set_val(PS3_DOWN, 100);
    set_val(PS3_TRIANGLE, 100);
    wait(100);
    set_val(PS3_DOWN, 100);
    set_val(PS3_TRIANGLE, 0);
    wait(40);
    set_val(PS3_DOWN, 0);
}

combo RumbleNotifier {
    set_rumble(RUMBLE_A, 100);
    wait(300);
    reset_rumble();
}

function colorled(a,b,c,d) {
    set_led(LED_1, a);
    set_led(LED_2, b);
    set_led(LED_3, c);
    set_led(LED_4, d);
}

function center_x(f_chars, f_font) {
    return (OLED_WIDTH / 2) - ((f_chars * f_font) / 2);
}
```

---

## Architectural Breakdown & Code Analysis

This script demonstrates several highly sophisticated GPC scripting techniques:

### 1. Enumerated Selection States
Instead of using random integers to track active mods, the script uses an `enum {}` block. This assigns index numbers `0` to `4` to labels:
```c
enum {
    AUTO_THROW, // = 0
    NO_THROW,   // = 1
    FOWARD,     // = 2
    CANNON,     // = 3
    OFF         // = 4
}
```
This enables readable checks like `if(activeMod == AUTO_THROW)` instead of `if(activeMod == 0)`.

### 2. Auto-Centering OLED String Logic
The custom function `center_x()` calculates coordinate offsets to center string headers perfectly on the 128-pixel display, regardless of string size or font width:
```c
function center_x(f_chars, f_font) {
    return (OLED_WIDTH / 2) - ((f_chars * f_font) / 2);
}
```
When used inside `init`, it computes:
* Total text width = `number of characters * font pixel width`.
* Offsets = `(128 - total width) / 2`.
This is passed directly as the `X` parameter inside `print()`.

### 3. Non-Blocking Screen Saver
To prevent pixel burn-in on the Zen's OLED display, the script monitors a timer:
```c
if(screen_saver_timer) {
    if(screen_saver_timer <= get_rtime()) {
        cls_oled(OLED_BLACK); // Turn screen black
    }
    screen_saver_timer = max(0, screen_saver_timer - get_rtime());
}
```
This loop decrements by the actual execution cycle runtime (`get_rtime()`) on every frame. When 15 seconds (`Screen_Saver_Time`) elapse without user profile changes, the display is cleared to black.

### 4. Interactive LED Notifications
When switching modes, the script calls `colorled()` to swap LED colors on the controller, providing instant visual feedback on active presets (e.g. Red for NoThrow, Blue for AutoThrow).

### 5. Multi-Step Asynchronous Combos
The `foward` and `cannon` combos show the power of asynchronous execution. By daisy-chaining `set_val()` and `wait(10)` instructions, the script simulates fluid, precise analog stick movements (e.g., rotating the stick sequentially from `-23` to `-100` deflection in 10ms intervals) to execute the glitch, while the `main` thread remains active to process button releases or watchdog safety checks.
