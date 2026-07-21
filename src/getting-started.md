# Getting started

Welcome to the **Cronus Zen GPC Scripting Documentation**. This guide will help you understand how the Cronus Zen execution environment works, how to set up your environment, and how to write and load your first script.

::: cards
- [**Syntax Basics** Master variables, defines, loops, and script structure](/cronus-docs/syntax/)
- [**Input/Output API** Read controller states and write virtual inputs](/cronus-docs/input-output/)
- [**Combos & Timing** Create non-blocking timed macro sequences](/cronus-docs/combos-timing/)
- [**Advanced Guides** Learn anti-recoil and rapid fire math](/cronus-docs/advanced-guides/)
:::

---

## What is Cronus Zen?

The Cronus Zen is a hardware passthrough adapter that interfaces between your controller (or mouse/keyboard) and your gaming console or PC. It intercepts physical inputs, processes them through a custom scripting engine, and outputs the modified signals to the gaming platform.

Because it operates at the hardware level, it does not modify game code or system memory. However, GPC scripting must be written carefully to avoid robotic input cadences that modern game anti-cheat engines (like Ricochet or Vanguard) scan for.

---

## Setting Up Your Development Environment

To write, compile, and upload custom scripts to your Cronus Zen, you need **Zen Studio**.

### 1. Download Zen Studio
Download the official **Zen Studio** software from the Cronus support portal.

### 2. Connect Your Device
To program scripts:
- Connect the **PROG** port (on the right side of the Zen) to your PC using a Mini-USB cable.
- This port allows Zen Studio to read/write GPC slots and update the device firmware.

{% hint style="warning" %}
Do not confuse the **PROG** port (Mini-USB on the side) with the **CON** ports (Micro-USB/USB-A on the top/front). Always use the PROG port when uploading scripts from Zen Studio.
{% endhint %}

---

## Creating Your First Script

GPC scripts are simple plain-text files with a `.gpc` extension.

1. Open Zen Studio and navigate to the **Compiler** tab.
2. Click **File** -> **New** -> **GPC Script**.
3. Paste the following basic script which enables a simple rapid-fire macro:

```c
// Rapid Fire speed in milliseconds (Wait delay between actions)
define RAPID_FIRE_DELAY = 40;

main {
    // If the Right Trigger (RT/R2) is held down
    if (get_val(XB1_RT)) {
        // Run the RapidFire combo sequence
        combo_run(RapidFire);
    }
}

// A combo is a non-blocking sequence of events
combo RapidFire {
    set_val(XB1_RT, 100);       // Simulate pressing the trigger fully
    wait(RAPID_FIRE_DELAY);     // Wait for 40ms
    set_val(XB1_RT, 0);         // Simulate releasing the trigger
    wait(RAPID_FIRE_DELAY);     // Wait for 40ms
}
```

4. Press **F7** on your keyboard (or click **Compiler** -> **Compile**).
5. The status bar at the bottom will display `Compile Success!` if there are no errors.

---

## Programming the Script into a Slot

To run a script on your console or PC:

1. In Zen Studio, click on the **Programmer** tab.
2. Under the **GPC Files** list on the left, find your saved `.gpc` script.
3. Drag and drop your script into one of the **8 Memory Slots** in the center panel.
4. Click the **Play** button (on the left action panel) or click **Save to Device**.
5. Once complete, unplug the Zen from your PC.
6. Plug the Zen's console port into your console/PC, connect your controller, and use the physical blue buttons on the Zen to select the slot number you loaded.
