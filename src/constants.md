# System Constants

GPC provides a set of pre-defined system constants for managing the OLED screen, ASCII characters, and identifying connected hardware platforms.

---

## OLED Display Constants

Use these constants to format text sizes, layout coordinates, and define colors when drawing to the built-in screen.

```c
// General Display Properties
define OLED_WIDTH = 128;         // Screen width in pixels
define OLED_HEIGHT = 64;         // Screen height in pixels
define OLED_WHITE = 1;           // Pixel ON color
define OLED_BLACK = 0;           // Pixel OFF color

// Font Size Identifiers
define OLED_FONT_SMALL = 0;      // 5x7 pixel spacing
define OLED_FONT_MEDIUM = 1;     // 8x12 pixel spacing
define OLED_FONT_LARGE = 2;      // Larger bold typeface
```

### OLED Button Prompt Glyphs
The Cronus Zen has built-in character assets for console button prompt glyphs. When passed to the text rendering buffers, they draw corresponding controller button symbols instead of text letters.

* `OLED_CROSS` = `127`
* `OLED_CIRCLE` = `128`
* `OLED_SQUARE` = `129`
* `OLED_TRIANGLE` = `130`
* `OLED_UP` = `131`
* `OLED_DOWN` = `132`
* `OLED_LEFT` = `133`
* `OLED_RIGHT` = `134`
* `OLED_VIEW` = `135`
* `OLED_MENU` = `136`

---

## PIO (Peripheral I/O) Constants

PIO constants represent gaming platforms and controller profiles. They are returned by the system query functions `get_console()` and `get_controller()`.

```c
define PIO_NONE = 0;             // No console / controller connected
define PIO_AUTO = 0;             // Automatic detection profile
define PIO_PS3 = 1;              // PlayStation 3
define PIO_XB360 = 2;            // Xbox 360
define PIO_WII = 3;              // Nintendo Wii
define PIO_PS4 = 4;              // PlayStation 4
define PIO_XB1 = 5;              // Xbox One / Series X|S
define PIO_SWITCH = 6;           // Nintendo Switch
define PIO_PS5 = 7;              // PlayStation 5
```

### Example: Adapting Layout Dynamically

You can use PIO constants to write layouts that adapt automatically depending on whether a PlayStation or Xbox controller is plugged in.

```c
int jump_button;

init {
    // Detect which controller is plugged into the input slot
    if (get_controller() == PIO_PS4 || get_controller() == PIO_PS5) {
        jump_button = PS4_CROSS;
    } else {
        jump_button = XB1_A;
    }
}

main {
    if (event_press(jump_button)) {
        // Run jump logic
    }
}
```

---

## ASCII Character Constants

The table below lists common ASCII character constants used with `putc_oled()` to write characters to the screen buffer.

| Constant Name | Character | Integer Value |
| :--- | :--- | :--- |
| `ASCII_SPACE` | (space) | `32` |
| `ASCII_EXCLAMATION` | `!` | `33` |
| `ASCII_DOUBLE_QUOTE` | `"` | `34` |
| `ASCII_POUND` | `#` | `35` |
| `ASCII_PERCENT` | `%` | `37` |
| `ASCII_AMPERSAND` | `&` | `38` |
| `ASCII_DIGIT0` to `ASCII_DIGIT9` | `0` to `9` | `48` to `57` |
| `ASCII_COLON` | `:` | `58` |
| `ASCII_SEMICOLON` | `;` | `59` |
| `ASCII_EQUALS` | `=` | `61` |
| `ASCII_QUESTION` | `?` | `63` |
| `ASCII_A` to `ASCII_Z` | `A` to `Z` | `65` to `90` |
| `ASCII_a` to `ASCII_z` | `a` to `z` | `97` to `122` |
