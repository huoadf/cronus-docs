# OLED Display API

The Cronus Zen features a built-in 128x64 pixel monochrome OLED display. GPC scripts can draw text, shapes, and custom user interfaces directly onto this display.

---

## Screen Coordinates & Colors

The OLED display uses a grid system starting from the top-left corner:
* **Width**: `128` pixels (X-axis: `0` to `127`)
* **Height**: `64` pixels (Y-axis: `0` to `63`)

```
(0,0) ------------------- (127,0)
  |                         |
  |      OLED SCREEN        |
  |        128 x 64         |
  |                         |
(0,63) ----------------- (127,63)
```

* **Colors**: 
  * `0` = Black (pixel off)
  * `1` = White (pixel on)

---

## Draw Functions

### `cls_oled`
Clears the entire display to a single color.
* **Syntax**: `cls_oled(<color>);`
* **Example**:
  ```c
  init {
      cls_oled(0); // Clear screen to black at script startup
  }
  ```

### `pixel_oled`
Illuminates a single pixel at a specific coordinate.
* **Syntax**: `pixel_oled(<x>, <y>, <color>);`

### `line_oled`
Draws a straight line from one coordinate to another.
* **Syntax**: `line_oled(<x1>, <y1>, <x2>, <y2>, <thickness>, <color>);`
* **Example**:
  ```c
  main {
      // Draw a horizontal line at the center
      line_oled(0, 32, 127, 32, 1, 1);
  }
  ```

### `rect_oled`
Draws a rectangle on the screen.
* **Syntax**: `rect_oled(<x>, <y>, <width>, <height>, <fill_flag>, <color>);`
* **Parameters**:
  * `<fill_flag>`: `0` for outline outline only, `1` to fill the rectangle.
* **Example**:
  ```c
  main {
      // Draw a filled white box on the left half of the screen
      rect_oled(0, 0, 64, 64, 1, 1);
  }
  ```

### `circle_oled`
Draws a circle.
* **Syntax**: `circle_oled(<x>, <y>, <radius>, <fill_flag>, <color>);`

---

## Text Output API

Writing text to the OLED screen is a two-step process in GPC:
1. Load characters into the Zen's text string buffer using `putc_oled()`.
2. Render the string buffer to a specific position on the display using `puts_oled()`.

### `putc_oled`
Pushes a single ASCII character into the text buffer.
* **Syntax**: `putc_oled(<buffer_index>, <char_code>);`
* **Parameters**:
  * `<buffer_index>`: The index inside the text buffer array (usually incremented per character).
  * `<char_code>`: The ASCII value or character constant.

### `puts_oled`
Draws the loaded text buffer onto the screen.
* **Syntax**: `puts_oled(<x>, <y>, <font_id>, <num_chars>, <color>);`
* **Fonts**: `OLED_FONT_SMALL` (5x7 pixels) or `OLED_FONT_MEDIUM` (8x12 pixels).

### Example: Displaying a Status String

This example demonstrates how to build and write "ON" or "OFF" to the screen depending on script variables.

```c
define OLED_FONT_SMALL = 0;
int rapid_fire_active = TRUE;

main {
    if (event_press(XB1_Y)) {
        rapid_fire_active = !rapid_fire_active;
        combo_run(UpdateDisplay);
    }
}

combo UpdateDisplay {
    cls_oled(0); // Clear screen first
    
    // Write static text header "STATUS:"
    putc_oled(0, 'S');
    putc_oled(1, 'T');
    putc_oled(2, 'A');
    putc_oled(3, 'T');
    putc_oled(4, 'U');
    putc_oled(5, 'S');
    putc_oled(6, ':');
    puts_oled(0, 0, OLED_FONT_SMALL, 7, 1); // Render header
    
    if (rapid_fire_active) {
        putc_oled(0, 'O');
        putc_oled(1, 'N');
        puts_oled(50, 0, OLED_FONT_SMALL, 2, 1);
    } else {
        putc_oled(0, 'O');
        putc_oled(1, 'F');
        putc_oled(2, 'F');
        puts_oled(50, 0, OLED_FONT_SMALL, 3, 1);
    }
}
```

{% hint style="warning" %}
**CPU Optimization Notice**
Updating the OLED display is a relatively heavy hardware operation. **Never call display functions directly inside the `main` loop on every tick.** Only trigger updates inside a conditional statement or timed `combo` when a setting changes.
{% endhint %}
