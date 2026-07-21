# Case Study: Skate 3 Speed Glitch

This page provides a deep-dive analysis of a real-world GPC script used to automate speed glitches in *Skate 3* (Version 2.00 by Void Vids, upgraded with timing calibration). It integrates almost every GPC concept — including screen management, multi-mode profiles, LED controls, screen savers, complex stick-movement combos, and custom layout functions.

---

## Calibrated Script Source

Below is the verified working script. It has been corrected to use decimal ASCII values, ensuring it compiles with **0 errors and 0 warnings** in the GPC compiler.

```c
// Skate 3 Speed Glitch Suite
// Version: 2.00 (Calibrated)
// Features: Auto-Centering OLED, Calibration HUD, Burn-in Screen Saver, Cross-Platform Support

enum {
    AUTO_THROW,
    NO_THROW,
    FOWARD,
    CANNON,
    BACKWARD,
    OFF
}

const string Title = "Skate 3 Pro";

const string Modnames[] = {
    "AutoThrow",
    "NoThrow",
    "Fowardman",
    "Cannon",
    "BackwardMan",
    "Off"
}

define Screen_Saver_Time = 15000;

int activeMod;
int screen_saver_timer = Screen_Saver_Time;

// Calibration Offsets (Adjust timing on the fly for lag / FPS calibration)
int timing_offset = 0; // Managed via D-pad UP/DOWN (e.g. +10ms, -20ms)

init {
    cls_oled(OLED_BLACK);
    // Draw Title Header (Centered)
    print(center_x(sizeof(Title) - 1, OLED_FONT_LARGE_WIDTH), 10, OLED_FONT_LARGE, OLED_WHITE, Title[0]);
    draw_hud();
}

main {
    // 1. Swap Glitch Profile: Hold LT (L2) and press D-pad RIGHT
    if(get_val(XB1_LT) && event_press(XB1_RIGHT)) {
        activeMod++;
        combo_run(RumbleNotifier);
        if(activeMod >= 6) { // 6 modes total
            activeMod = 0;
        }
        draw_hud();
        screen_saver_timer = Screen_Saver_Time;
    }

    // 2. Timing Calibrator: Hold LT (L2) and press D-pad UP/DOWN to adjust wait speeds on the fly
    if(get_val(XB1_LT)) {
        if(event_press(XB1_UP)) {
            timing_offset = clamp(timing_offset + 10, -100, 200); // Add 10ms wait delay
            combo_run(RumbleNotifier);
            draw_hud();
            screen_saver_timer = Screen_Saver_Time;
        }
        if(event_press(XB1_DOWN)) {
            timing_offset = clamp(timing_offset - 10, -100, 200); // Subtract 10ms wait delay
            combo_run(RumbleNotifier);
            draw_hud();
            screen_saver_timer = Screen_Saver_Time;
        }
        // Block D-pad actions while using shortcut modifiers
        block(XB1_UP, 200);
        block(XB1_DOWN, 200);
        block(XB1_RIGHT, 200);
    }

    // 3. Glitch Activator: Hold D-pad LEFT to execute active mod combo
    if(get_val(XB1_LEFT)) {
        if(activeMod == AUTO_THROW) {
            colorled(0, 0, 1, 0); // Blue LED
            combo_run(throw);
        }
        else if(activeMod == NO_THROW) {
            colorled(0, 1, 0, 0); // Red LED
            combo_run(nothrow);
        }
        else if(activeMod == FOWARD) {
            colorled(1, 1, 0, 0); // Pink LED
            combo_run(foward);
        }
        else if(activeMod == CANNON) {
            colorled(1, 0, 1, 0); // Teal LED
            combo_run(cannon);
        }
        else if(activeMod == BACKWARD) {
            colorled(0, 1, 1, 0); // Yellow/Orange LED
            combo_run(backwardman);
        }
    }

    if(activeMod == OFF) {
        colorled(0, 0, 0, 0); // Off
    }

    // 4. OLED Saver Tick
    if(screen_saver_timer) {
        if(screen_saver_timer <= get_rtime()) {
            cls_oled(OLED_BLACK);
        }
        screen_saver_timer = max(0, screen_saver_timer - get_rtime());
    }
}

// --- COMBOS (Speed Glitch Macros) ---

combo throw {
    set_val(XB1_RT, 100); // Throw board
    wait(220);
    set_val(XB1_RT, 0);
    wait(50);
    set_val(XB1_X, 100);  // Jump
    wait(470);
    set_val(XB1_RB, 100); // Summon board
    set_val(XB1_X, 0);
    wait(110);
    set_val(XB1_RB, 0);
    wait(40);
    set_val(XB1_Y, 100);  // Get on board
    wait(120 + timing_offset); // Dynamic calibration delay
    set_val(XB1_Y, 0);
}

combo nothrow {
    set_val(XB1_X, 100);
    wait(470);
    set_val(XB1_RB, 100);
    set_val(XB1_X, 0);
    wait(110);
    set_val(XB1_RB, 0);
    wait(40);
    set_val(XB1_Y, 100);
    wait(120 + timing_offset);
    set_val(XB1_Y, 0);
}

combo backwardman {
    set_val(XB1_RT, 100); // Throw
    wait(100);
    set_val(XB1_RT, 0);
    wait(180);
    set_val(XB1_X, 100);  // Jump
    wait(100);
    set_val(XB1_X, 0);
    wait(350);            // Peak height wait
    set_val(XB1_RB, 100); // Summon board
    wait(50);
    set_val(XB1_RB, 0);
    wait(90);
    set_val(XB1_Y, 100);  // Hop on board
    wait(100 + timing_offset);
    set_val(XB1_Y, 0);
}

combo foward {
    set_val(XB1_RT, 100);
    wait(160);
    set_val(XB1_RT, 0);
    wait(10);
    set_val(XB1_LY, -20);
    wait(10);
    set_val(XB1_LY, -35);
    wait(10);
    set_val(XB1_LY, -55);
    wait(10);
    set_val(XB1_LY, -70);
    wait(10);
    set_val(XB1_RB, 100);
    set_val(XB1_LY, -84);
    wait(10);
    set_val(XB1_RB, 100);
    set_val(XB1_LY, -95);
    wait(10);
    set_val(XB1_RB, 100);
    set_val(XB1_LY, -100);
    wait(70);
    set_val(XB1_RB, 100);
    set_val(XB1_LY, -100);
    set_val(XB1_A, 100);
    wait(990);
    set_val(XB1_RB, 100);
    set_val(XB1_LY, -100);
    set_val(XB1_A, 100);
    set_val(XB1_X, 100);
    wait(30);
    set_val(XB1_RB, 100);
    set_val(XB1_LY, -100);
    set_val(XB1_A, 0);
    set_val(XB1_X, 100);
    wait(130);
    set_val(XB1_RB, 100);
    set_val(XB1_RX, -23);
    set_val(XB1_RY, 27);
    set_val(XB1_LY, -100);
    set_val(XB1_X, 100);
    wait(10);
    set_val(XB1_RB, 100);
    set_val(XB1_RX, -34);
    set_val(XB1_RY, 41);
    set_val(XB1_LY, -100);
    set_val(XB1_X, 100);
    wait(10);
    set_val(XB1_RB, 100);
    set_val(XB1_RX, -45);
    set_val(XB1_RY, 56);
    set_val(XB1_LY, -100);
    set_val(XB1_X, 100);
    wait(10);
    set_val(XB1_RB, 100);
    set_val(XB1_RX, -53);
    set_val(XB1_RY, 69);
    set_val(XB1_LY, -100);
    set_val(XB1_X, 100);
    wait(10);
    set_val(XB1_RB, 100);
    set_val(XB1_RX, -64);
    set_val(XB1_RY, 85);
    set_val(XB1_LY, -100);
    set_val(XB1_X, 100);
    wait(10);
    set_val(XB1_RB, 100);
    set_val(XB1_RX, -70);
    set_val(XB1_RY, 97);
    set_val(XB1_LY, -100);
    set_val(XB1_X, 100);
    wait(10);
    set_val(XB1_RB, 100);
    set_val(XB1_RX, -71);
    set_val(XB1_RY, 100);
    set_val(XB1_LY, -100);
    set_val(XB1_X, 100);
    wait(10);
    set_val(XB1_RB, 100);
    set_val(XB1_RX, -70);
    set_val(XB1_RY, 100);
    set_val(XB1_LY, -100);
    set_val(XB1_X, 0);
    wait(90);
    set_val(XB1_RB, 100);
    set_val(XB1_RX, -70);
    set_val(XB1_RY, 100);
    set_val(XB1_LY, 0);
    wait(40);
    set_val(XB1_RB, 0);
    set_val(XB1_RX, -70);
    set_val(XB1_RY, 100);
    wait(40);
    set_val(XB1_RX, -74);
    set_val(XB1_RY, 100);
    wait(10);
    set_val(XB1_RX, -78);
    set_val(XB1_RY, 100);
    wait(10);
    set_val(XB1_RX, -82);
    set_val(XB1_RY, 100);
    wait(20);
    set_val(XB1_RX, -82);
    set_val(XB1_RY, 94);
    wait(10);
    set_val(XB1_RX, -85);
    set_val(XB1_RY, 92);
    wait(10);
    set_val(XB1_RX, -87);
    set_val(XB1_RY, 90);
    wait(10);
    set_val(XB1_RX, -89);
    set_val(XB1_RY, 86);
    wait(10);
    set_val(XB1_RX, -96);
    set_val(XB1_RY, 81);
    wait(10);
    set_val(XB1_RX, -96);
    set_val(XB1_RY, 72);
    wait(10);
    set_val(XB1_RX, -100);
    set_val(XB1_RY, 69);
    wait(10);
    set_val(XB1_RX, -100);
    set_val(XB1_RY, 67);
    wait(10);
    set_val(XB1_RX, -98);
    set_val(XB1_RY, 52);
    wait(10);
    set_val(XB1_RX, -76);
    set_val(XB1_RY, 26);
    wait(10);
    set_val(XB1_RX, -44);
    set_val(XB1_RY, 0);
    wait(10);
    set_val(XB1_RX, 0);
    wait(40);
    set_val(XB1_Y, 100);
    wait(100 + timing_offset);
    set_val(XB1_DOWN, 100);
    set_val(XB1_Y, 100);
    wait(30);
    set_val(XB1_DOWN, 100);
    set_val(XB1_Y, 0);
    wait(70);
    set_val(XB1_DOWN, 0);
}

combo cannon {
    set_val(XB1_RT, 22);
    wait(10);
    set_val(XB1_RT, 30);
    wait(10);
    set_val(XB1_RT, 40);
    wait(10);
    set_val(XB1_RT, 48);
    wait(10);
    set_val(XB1_RT, 57);
    wait(10);
    set_val(XB1_RT, 69);
    wait(10);
    set_val(XB1_RT, 86);
    wait(10);
    set_val(XB1_RT, 100);
    wait(140);
    set_val(XB1_RT, 70);
    set_val(XB1_LY, -20);
    wait(10);
    set_val(XB1_RT, 43);
    set_val(XB1_LY, -26);
    wait(10);
    set_val(XB1_RT, 25);
    set_val(XB1_LY, -35);
    wait(10);
    set_val(XB1_RT, 0);
    set_val(XB1_LY, -42);
    wait(10);
    set_val(XB1_LY, -54);
    wait(10);
    set_val(XB1_LY, -56);
    wait(10);
    set_val(XB1_LY, -67);
    wait(10);
    set_val(XB1_LY, -74);
    wait(10);
    set_val(XB1_LY, -76); 
    wait(10);
    set_val(XB1_LY, -85);
    set_val(XB1_A, 100);
    wait(10);
    set_val(XB1_LY, -92);
    set_val(XB1_A, 100);
    wait(10);
    set_val(XB1_LY, -100);
    set_val(XB1_A, 100);
    wait(1270);
    set_val(XB1_LY, -100);
    set_val(XB1_A, 100);
    set_val(XB1_X, 100);
    wait(40);
    set_val(XB1_LY, -100);
    set_val(XB1_A, 0);
    set_val(XB1_X, 100);
    wait(70);
    set_val(XB1_LY, -100);
    set_val(XB1_X, 0);
    wait(120);
    set_val(XB1_RY, -36);
    set_val(XB1_LY, -100);
    wait(10);
    set_val(XB1_RY, -63);
    set_val(XB1_LY, -100);
    wait(10);
    set_val(XB1_RY, -94);
    set_val(XB1_LY, -100);
    wait(10);
    set_val(XB1_RY, -100);
    set_val(XB1_LY, -88);
    wait(10);
    set_val(XB1_RY, -100);
    set_val(XB1_LY, 42);
    wait(10);
    set_val(XB1_RY, -100);
    set_val(XB1_LY, 0);
    wait(250);
    set_val(XB1_RY, -73);
    wait(10);
    set_val(XB1_RY, 49);
    wait(10);
    set_val(XB1_RY, -24);
    wait(10);
    set_val(XB1_RY, 0);
    wait(10);
    set_val(XB1_Y, 100);
    wait(60);
    set_val(XB1_DOWN, 100);
    set_val(XB1_Y, 100);
    wait(100 + timing_offset);
    set_val(XB1_DOWN, 100);
    set_val(XB1_Y, 0);
    wait(40);
    set_val(XB1_DOWN, 0);
}

combo RumbleNotifier {
    set_rumble(RUMBLE_A, 100);
    wait(150);
    reset_rumble();
}

// --- USER FUNCTIONS (Display & HUD Drivers) ---

function draw_hud() {
    cls_oled(OLED_BLACK);
    // 1. Print Active Mod String (Line 20)
    print(10, 20, OLED_FONT_MEDIUM, OLED_WHITE, Modnames[activeMod]);
    
    // 2. Draw Calibrated Offset HUD indicator (Line 44)
    // ASCII values: 67 = 'C', 65 = 'A', 76 = 'L', 58 = ':', 32 = ' '
    putc_oled(0, 67); putc_oled(1, 65); putc_oled(2, 76); putc_oled(3, 58);
    putc_oled(4, 32);
    
    int sign = 32;
    if(timing_offset < 0) {
        sign = 45; // '-'
    } else if(timing_offset > 0) {
        sign = 43; // '+'
    }
    putc_oled(5, sign);
    
    // Deconstruct offset integer to characters for putc formatting
    int abs_val = abs(timing_offset);
    int hundred = (abs_val / 100) + 48;       // Hundreds column character code
    int ten = ((abs_val % 100) / 10) + 48;    // Tens column
    int unit = (abs_val % 10) + 48;           // Units column
    
    putc_oled(6, hundred);
    putc_oled(7, ten);
    putc_oled(8, unit);
    // ASCII values: 109 = 'm', 115 = 's'
    putc_oled(9, 109); putc_oled(10, 115);
    
    puts_oled(10, 44, OLED_FONT_SMALL, 11, OLED_WHITE);
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
Instead of using random integers to track active mods, the script uses an `enum {}` block. This assigns index numbers `0` to `5` to labels:
```c
enum {
    AUTO_THROW, // = 0
    NO_THROW,   // = 1
    FOWARD,     // = 2
    CANNON,     // = 3
    BACKWARD,   // = 4
    OFF         // = 5
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

---

## Compiler Constraints: Avoid Character Literals

> [!WARNING]
> **Compiler Lexical Bug Notice**
> The GPC Lexical scanner has a bug where it throws syntax warnings or fails compilation when using single-quote character constants (e.g., `'C'`). If single-quotes are used in comments (like `// Void's`), it will warn about invalid symbols on line 1.
> 
> To resolve this, **never use single quotes in comments or strings**, and always write raw decimal ASCII values for `putc_oled` buffer indices:
> * Instead of `putc_oled(0, 'C');`, write `putc_oled(0, 67);`
> * Instead of `sign = '-';`, write `sign = 45;`
