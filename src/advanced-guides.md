# Advanced Guides & Macros

This section covers practical design patterns and common scripts used in gaming macros, along with instructions on maintaining high device performance.

---

## CPU Load Management

The Cronus Zen has a limited microprocessor. If your GPC script executes too many complex calculations in a single tick, the processor load will exceed **80%**, causing input lag, dropped button presses, or script crashes.

### Rules for Efficient Code
* **Avoid Nested Loops**: Never write `while` or `for` loops inside the `main` block.
* **Minimize Floating Point Conversions**: Keep fixed-point math minimal. Only perform calculations when buttons are pressed, rather than continuously.
* **Keep Combos Clean**: Do not run multiple combos at the same time if they are writing to the exact same buttons. This causes resource contention.

---

## Pattern 1: Progressive Anti-Recoil

Standard anti-recoil pulls the right stick down at a static rate. Progressive anti-recoil increases or decreases the pull force over time to counteract weapons that kick harder the longer you hold the trigger.

```c
define START_RECOIL = 20;     // Initial pull force
define END_RECOIL = 42;       // Final pull force
define PROGRESS_TIME = 2000;  // Milliseconds to reach final force

int active_recoil_force;
int time_held;

main {
    // If holding Aim Down Sights (LT) and Fire (RT)
    if (get_val(XB1_LT) && get_val(XB1_RT)) {
        // Track how long the user has been firing
        time_held = get_ptime(XB1_RT);
        
        if (time_held < PROGRESS_TIME) {
            // Linearly interpolate between START_RECOIL and END_RECOIL
            active_recoil_force = START_RECOIL + (((END_RECOIL - START_RECOIL) * time_held) / PROGRESS_TIME);
        } else {
            active_recoil_force = END_RECOIL;
        }
        
        // Run the anti-recoil combo
        combo_run(ApplyAntiRecoil);
    } else {
        combo_stop(ApplyAntiRecoil);
    }
}

combo ApplyAntiRecoil {
    // Inject vertical stick downward pull
    set_val(XB1_RY, clamp(get_val(XB1_RY) + active_recoil_force, -100, 100));
    wait(10);
}
```

---

## Pattern 2: Rapid Fire with Adjustable Rate

This script allows you to adjust the fire rate speed directly from your controller on-the-fly without plugging it into a PC.

* **Controls**: Hold **LT/L2** + **D-PAD Left** to slow down, or **D-PAD Right** to speed up.

```c
int hold_delay = 40; // Initial delay of 40ms between shots

main {
    // Adjust rate of fire: Hold ADS and press D-pad
    if (get_val(XB1_LT)) {
        if (event_press(XB1_RIGHT)) {
            // Decrease delay (increases fire speed)
            hold_delay = clamp(hold_delay - 5, 20, 200);
            combo_run(RumbleFast);
        }
        if (event_press(XB1_LEFT)) {
            // Increase delay (decreases fire speed)
            hold_delay = clamp(hold_delay + 5, 20, 200);
            combo_run(RumbleSlow);
        }
    }

    // Trigger rapid fire
    if (get_val(XB1_RT)) {
        combo_run(AdjustableRapidFire);
    }
}

combo AdjustableRapidFire {
    set_val(XB1_RT, 100);
    wait(hold_delay);
    set_val(XB1_RT, 0);
    wait(hold_delay);
}

combo RumbleFast {
    set_rumble(RUMBLE_A, 30);
    wait(80);
    reset_rumble();
}

combo RumbleSlow {
    set_rumble(RUMBLE_A, 15);
    wait(160);
    reset_rumble();
}
```

---

## Pattern 3: Modern Warfare Slide Cancel Macro

A classic macro sequence. Performs a double slide followed by a jump crouch-cancel when you hold the sprint button or press a designated paddle.

```c
main {
    // Trigger Slide Cancel macro when pressing Slide/Crouch (B) while moving forward
    if (get_val(XB1_LY) < -80 && event_press(XB1_B)) {
        combo_run(SlideCancel);
    }
}

combo SlideCancel {
    set_val(XB1_B, 100);    // Slide 1
    wait(60);
    set_val(XB1_B, 0);
    wait(60);
    set_val(XB1_B, 100);    // Slide 2
    wait(60);
    set_val(XB1_B, 0);
    wait(40);
    set_val(XB1_A, 100);    // Jump to stand up
    wait(60);
    set_val(XB1_A, 0);
    wait(20);
}
```
