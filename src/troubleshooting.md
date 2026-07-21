# Troubleshooting & Limits

When writing scripts for embedded hardware like the Cronus Zen, you are working under strict memory and processor limits. This guide covers debugging techniques, optimization tips, and troubleshooting common GPC VM crashes.

---

## Bytecode & Memory Limits

Cronus Zen memory slots have a physical file size cap. GPC compiles down to VM bytecode, which must fit within **4,096 bytes (4KB)** per script slot.

### Checking Code Size
When you compile your script in Zen Studio (by pressing **F7**), look at the compiler output status bar:
* It will show the percentage of bytecode slot memory consumed (e.g. `GPC Compiler: Success. Bytecode size: 1024 bytes (25%)`).
* If your script exceeds 100%, it will fail to program onto the device.

### Bytecode Optimization Tips
If you are running out of space, use these techniques to shrink your bytecode size:

* **Use `define` Instead of Variables**:
  Constants declared with `define` do not take up variable memory slots.
  ```c
  // Bad (uses variable space):
  int RAPID_FIRE_DELAY = 40;
  
  // Good (compile-time replacement, 0 byte overhead):
  define RAPID_FIRE_DELAY = 40;
  ```
* **Avoid Duplicate Code Blocks**:
  If you are running the same calculations (like stick scaling or coordinate mappings) in multiple places, move them to a **user-defined function** at the bottom of the script.
* **Consolidate Variables**:
  Do not create separate boolean variables for every toggle. You can store multiple boolean flags inside a single integer using bitwise operations, or reuse utility variables (e.g., `temp_val`).
* **Reduce Combo Counts**:
  Combos take up significant space. If multiple features do similar button sequences, write a single parametric combo or function.

---

## VM Watchdog Timeouts

The Cronus Zen operates on a **Watchdog Timer** system. The GPC Virtual Machine expects your `main {}` block to complete execution and exit within a few milliseconds so the hardware can process device communications.

{% hint style="danger" %}
**Watchdog Timeout Error**
If the virtual machine is blocked for too long, the watchdog timer triggers, resetting the Cronus Zen. This causes your controller to disconnect, freeze, or cycle through a connection loop.
{% endhint %}

### The Cause: Blocking Loops
Watchdog timeouts are almost always caused by writing blocking loops (like `while` or `for` loops) inside `main {}`.

```c
// CRITICAL ERROR: This script will trigger a watchdog reset instantly!
main {
    if (get_val(XB1_RT)) {
        // This loop freezes the VM and blocks hardware USB communications!
        while (get_val(XB1_RT)) { 
            set_val(XB1_RT, 100);
        }
    }
}
```

### The Solution: Timed Combos
Never use loops to manage durations. Use **combos** and the `wait()` instruction. The `wait()` command tells the combo to pause execution and release control back to the VM, allowing the `main` block to continue running in parallel on every tick.

---

## VM CPU Overload & Input Lag

Even if your script doesn't crash the watchdog, it can suffer from high CPU load. If CPU load exceeds **80%**, the Cronus Zen will experience **input lag** (noticeable delay between pressing a button and the action happening in-game) or dropped inputs.

### Optimizing CPU Load
1. **Reduce Active Combos**: Avoid running multiple combos simultaneously if they read or write the same buttons.
2. **Conditional Calculations**: Do not perform complex calculations (like progressive recoil math) continuously. Wrap them in conditional statements so they only run when they are actually needed (e.g. only when firing).
   ```c
   main {
       // Bad: Calculates progressive math on every frame
       int pull = calculate_recoil(); 
       
       // Good: Only calculates when actually firing
       if (get_val(XB1_RT)) {
           int pull = calculate_recoil();
           set_val(XB1_RY, pull);
       }
   }
   ```

---

## Debugging with Trace Logs

Because GPC scripts run on an embedded chip without a screen output, you cannot use a standard debugger or `print` statements. Instead, you write debug values to **Trace Slots**.

### Using TRACE variables
Zen Studio has 6 trace variables: `TRACE_1`, `TRACE_2`, `TRACE_3`, `TRACE_4`, `TRACE_5`, and `TRACE_6`. You can write variables to these slots inside your script.

```c
main {
    // Write current recoil force to TRACE_1 so we can inspect it
    set_val(TRACE_1, active_recoil_force);
}
```

### Reading Trace Values
1. Connect your Zen to your PC via the **PROG** port.
2. Open Zen Studio and navigate to the **Compiler** tab.
3. Open the **Device Monitor** panel (on the bottom right).
4. Run your script. The Device Monitor will show live values updating inside the `TRACE_1` to `TRACE_6` output boxes.
