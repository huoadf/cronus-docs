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
    // ASCII codes: 83 = 'S', 69 = 'E', 76 = 'L', 67 = 'C', 84 = 'T', 32 = ' ', 65 = 'A', 89 = 'Y', 79 = 'O', 85 = 'U'
    putc_oled(0, 83); putc_oled(1, 69); putc_oled(2, 76); putc_oled(3, 69); 
    putc_oled(4, 67); putc_oled(5, 84); putc_oled(6, 32); putc_oled(7, 76);
    putc_oled(8, 65); putc_oled(9, 89); putc_oled(10, 79); putc_oled(11, 85);
    putc_oled(12, 84);
    puts_oled(10, 0, OLED_FONT_SMALL, 13, 1);
    
    // Draw visual button prompt icons: Up & Down Arrows
    // ASCII codes: 47 = '/', 32 = ' ', 67 = 'C', 104 = 'h', 97 = 'a', 110 = 'n', 103 = 'g', 101 = 'e'
    putc_oled(0, GLYPH_UP);
    putc_oled(1, 47);
    putc_oled(2, GLYPH_DOWN);
    putc_oled(3, 32);
    putc_oled(4, 67); putc_oled(5, 104); putc_oled(6, 97); putc_oled(7, 110);
    putc_oled(8, 103); putc_oled(9, 101);
    puts_oled(10, 20, OLED_FONT_SMALL, 10, 1);
    
    // Display the selected layout string
    if (current_layout == 0) {
        // ASCII codes: 62 = '>', 83 = 'S', 116 = 't', 97 = 'a', 110 = 'n', 100 = 'd', 114 = 'r'
        putc_oled(0, 62); putc_oled(1, 83); putc_oled(2, 116); putc_oled(3, 97);
        putc_oled(4, 110); putc_oled(5, 100); putc_oled(6, 97); putc_oled(7, 114);
        putc_oled(8, 100);
        puts_oled(10, 40, OLED_FONT_SMALL, 9, 1);
    } else if (current_layout == 1) {
        // ASCII codes: 62 = '>', 84 = 'T', 97 = 'a', 99 = 'c', 116 = 't', 105 = 'i', 108 = 'l'
        putc_oled(0, 62); putc_oled(1, 84); putc_oled(2, 97); putc_oled(3, 99);
        putc_oled(4, 116); putc_oled(5, 105); putc_oled(6, 99); putc_oled(7, 97);
        putc_oled(8, 108);
        puts_oled(10, 40, OLED_FONT_SMALL, 9, 1);
    } else {
        // ASCII codes: 62 = '>', 66 = 'B', 117 = 'u', 109 = 'm', 112 = 'p', 101 = 'e', 114 = 'r', 74 = 'J'
        putc_oled(0, 62); putc_oled(1, 66); putc_oled(2, 117); putc_oled(3, 109);
        putc_oled(4, 112); putc_oled(5, 101); putc_oled(6, 114); putc_oled(7, 74);
        putc_oled(8, 109); putc_oled(9, 112);
        puts_oled(10, 40, OLED_FONT_SMALL, 10, 1);
    }
}
```
