# Custom OLED Button Prompts

This guide demonstrates how to display dynamic controller button prompt icons (like A/Cross, B/Circle) on the Cronus Zen's built-in screen. These prompt glyphs are highly useful for creating interactive menus or layout configuration screens.

---

## OLED Glyphs Reference

The Zen's built-in fonts contain unique graphics mapped to character codes starting at `127`. Instead of drawing letters, they render button graphics.

* **`OLED_CROSS`** (ASCII `127`) : DualShock Cross / Xbox A
* **`OLED_CIRCLE`** (ASCII `128`) : DualShock Circle / Xbox B
* **`OLED_SQUARE`** (ASCII `129`) : DualShock Square / Xbox X
* **`OLED_TRIANGLE`** (ASCII `130`) : DualShock Triangle / Xbox Y
* **`OLED_UP`** (ASCII `131`) : D-pad UP
* **`OLED_DOWN`** (ASCII `132`) : D-pad DOWN
* **`OLED_LEFT`** (ASCII `133`) : D-pad LEFT
* **`OLED_RIGHT`** (ASCII `134`) : D-pad RIGHT
* **`OLED_VIEW`** (ASCII `135`) : Back / View / Share button
* **`OLED_MENU`** (ASCII `136`) : Start / Menu option button

---

## Implementation Method

To render a button prompt:
1. Put the custom prompt constant into the character buffer using `putc_oled()`.
2. Call `puts_oled()` at the desired coordinates.

### Code Example: Controller Layout Config Menu

This script displays a visual instruction menu on the OLED screen. It asks the user to press options and renders visual icons (like D-Pad UP/DOWN and CROSS/CIRCLE) on the screen to represent commands.

```c
define OLED_FONT_SMALL = 0;

// Button glyph aliases
define GLYPH_A = 127;
define GLYPH_B = 128;
define GLYPH_UP = 131;
define GLYPH_DOWN = 132;

int current_layout = 0; // 0 = Standard, 1 = Tactical, 2 = Bumper Jumper

main {
    // Open layout config: Hold ADS (LT) and press MENU
    if (get_val(XB1_LT) && event_press(XB1_MENU)) {
        combo_run(ShowConfigMenu);
    }
    
    // If menu is active and user presses D-pad UP/DOWN, cycle profiles
    if (combo_running(ShowConfigMenu)) {
        if (event_press(XB1_UP)) {
            current_layout = clamp(current_layout - 1, 0, 2);
            combo_run(ShowConfigMenu); // Redraw
        }
        if (event_press(XB1_DOWN)) {
            current_layout = clamp(current_layout + 1, 0, 2);
            combo_run(ShowConfigMenu); // Redraw
        }
        
        // Prevent default actions while in menu
        block(XB1_UP, 200);
        block(XB1_DOWN, 200);
    }
}

combo ShowConfigMenu {
    cls_oled(0); // Clear screen
    
    // Draw Title: "SELECT LAYOUT"
    putc_oled(0, 'S'); putc_oled(1, 'E'); putc_oled(2, 'L'); putc_oled(3, 'E'); 
    putc_oled(4, 'C'); putc_oled(5, 'T'); putc_oled(6, ' '); putc_oled(7, 'L');
    putc_oled(8, 'A'); putc_oled(9, 'Y'); putc_oled(10, 'O'); putc_oled(11, 'U');
    putc_oled(12, 'T');
    puts_oled(10, 0, OLED_FONT_SMALL, 13, 1);
    
    // Draw visual button prompt icons: Up & Down Arrows
    putc_oled(0, GLYPH_UP);
    putc_oled(1, '/');
    putc_oled(2, GLYPH_DOWN);
    putc_oled(3, ' ');
    putc_oled(4, 'C'); putc_oled(5, 'h'); putc_oled(6, 'a'); putc_oled(7, 'n');
    putc_oled(8, 'g'); putc_oled(9, 'e');
    puts_oled(10, 20, OLED_FONT_SMALL, 10, 1);
    
    // Display the selected layout string
    if (current_layout == 0) {
        putc_oled(0, '>'); putc_oled(1, 'S'); putc_oled(2, 't'); putc_oled(3, 'a');
        putc_oled(4, 'n'); putc_oled(5, 'd'); putc_oled(6, 'a'); putc_oled(7, 'r');
        putc_oled(8, 'd');
        puts_oled(10, 40, OLED_FONT_SMALL, 9, 1);
    } else if (current_layout == 1) {
        putc_oled(0, '>'); putc_oled(1, 'T'); putc_oled(2, 'a'); putc_oled(3, 'c');
        putc_oled(4, 't'); putc_oled(5, 'i'); putc_oled(6, 'c'); putc_oled(7, 'a');
        putc_oled(8, 'l');
        puts_oled(10, 40, OLED_FONT_SMALL, 9, 1);
    } else {
        putc_oled(0, '>'); putc_oled(1, 'B'); putc_oled(2, 'u'); putc_oled(3, 'm');
        putc_oled(4, 'p'); putc_oled(5, 'e'); putc_oled(6, 'r'); putc_oled(7, 'J');
        putc_oled(8, 'm'); putc_oled(9, 'p');
        puts_oled(10, 40, OLED_FONT_SMALL, 10, 1);
    }
}
```
