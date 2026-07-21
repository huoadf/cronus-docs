# 32-bit VM Updates

The transition of the Cronus Zen Virtual Machine (VM) to 32-bit architecture is one of the most significant upgrades for GPC script developers. This page outlines the benefits of 32-bit support, variable changes, and the new functions introduced to exploit this architecture.

---

## 32-bit Architecture Advantages

Older controller adapters compile GPC scripts on a 16-bit virtual machine. The modern Cronus Zen VM compiles in 32-bit.

```
16-bit: [ -32,768 ] ───────────────────────── [ 32,767 ] (Small Range)
32-bit: [ -2,147,483,648 ] ─────────── [ 2,147,483,647 ] (Massive Range)
```

### 1. Expanded Value Range
The integer bounds change dramatically:
* **Old 16-bit bounds**: `-32,768` to `32,767`
* **New 32-bit bounds**: `-2,147,483,648` to `2,147,483,647`

### 2. High-Precision Math (Anti-Recoil & Aim Assist)
Without decimals, complex math relies on scaling integers up and down.
* Under 16-bit limits, multiplying a stick value by `1000` could easily exceed the `32,767` threshold, causing overflow bugs.
* Under 32-bit, developers can scale values into the millions to perform trigonometric calculations (sine, cosine for circular/polar aim assist) without any risk of overflow.

---

## Polar Stick Coordinates API

The 32-bit firmware introduces native polar coordinate translation functions. Instead of managing Cartesian coordinates (X and Y stick positions) manually, the VM can translate stick deflection into an angle and radius.

```
       Cartesian (X, Y)                       Polar (Angle, Radius)
       
              +Y                                      90° (Up)
              |                                        |
       -X ----+---- +X                        180° ----+---- 0° (Right)
              |                                        |
              -Y                                      270° (Down)
```

### `get_polar`
Translates stick position into polar coordinates (direction and distance from the center).
* **Syntax**: `get_polar(<stick_id>, <coordinate_type>);`
* **Parameters**:
  * `<stick_id>`: `XB1_LX` or `XB1_RX`.
  * `<coordinate_type>`: 
    * `POLAR_ANGLE` (Returns `0` to `359` degrees, where `0` is Right, `90` is Up, `180` is Left, `270` is Down).
    * `POLAR_RADIUS` (Returns `0` to `32767`, representing the distance the stick is pushed from the center).

### `get_ipolar`
Retrieves the **original, unmodified** polar stick values directly from the controller before any script transformations (e.g. anti-recoil offsets) were applied.
* **Syntax**: `get_ipolar(<stick_id>, <coordinate_type>);`

---

## Performance Functions

### `get_info`
Retrieves internal processor diagnostics and script slot runtime statistics.
* **Syntax**: `get_info(<info_type>);`
* **Common Info Types**:
  * `INFO_CPU_LOAD`: Returns the current CPU usage of the GPC Virtual Machine as a percentage (`0` to `100`). Keep this under `80` to avoid lag.
  * `INFO_SLOT`: Returns the current active memory slot index number (`1` to `8`).
  * `INFO_VM_SPEED`: Returns the execution frequency cycle rate of the script.
