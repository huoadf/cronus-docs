# Zen Studio Live (Web IDE)

Collective Minds has introduced **Zen Studio Live**, a full web-based IDE that runs directly in your web browser. This tool eliminates the need to install a Windows executable, making Cronus Zen scripting and device configuration accessible across multiple operating systems.

---

## Accessing the Web IDE

* **Official Portal**: [https://zenstudio.collectivemindsstore.com/](https://zenstudio.collectivemindsstore.com/)
* **Supported Browsers**: Any Chromium-based browser (Google Chrome, Microsoft Edge, Opera, Brave).
* **Cross-Platform Compatibility**: Rebuilt to run on **Windows, macOS, Linux, and ChromeOS** (Chromebooks).

```
  [ Browser (Chrome/Edge) ]
             |
             +---> Uses WebHID / WebUSB API
             |
  [ Cronus Zen Device ] (Programmed directly from browser!)
```

---

## Core Features

### 1. Browser-to-Device Programmer
Using the browser's native **WebHID** and **WebUSB** APIs, Zen Studio Live establishes direct communication with the Cronus Zen hardware.
* No local service drivers or bridge tools are required to be running.
* You can connect your device via the **PROG** port, click "Connect", and write GPC compile scripts directly into the Zen's physical memory slots (`1` to `8`) from the page.

### 2. Modern GPC Editor with Git Version Control
The Web IDE features a code editor optimized for the GPC compiler:
* **Built-in Compiler**: Compiles your GPC scripts in the browser to detect syntax errors before flashing.
* **Git Version Control**: Integrates directly with Git repositories, allowing you to track code changes, save file histories, and back up scripts to online platforms (like GitHub) directly from the IDE interface.

### 3. OLED Message Screen Studio
Designing layouts for the Zen's 128x64 display is significantly simplified in the Web IDE:
* **Visual Designer**: Drag-and-drop layer management, drawing shapes, and layout alignment tools.
* **Text Generator**: Render text blocks using any system font files.
* **Image Dithering Import**: Upload png/jpg images, dither them automatically to monochrome (1-bit black and white), and click **Export GPC** to generate the corresponding byte-array coordinates.

### 4. Ballistic MK Curve Editor
For Mouse & Keyboard configurations, Zen Studio Live includes a visual Ballistic Curve editor:
* Adjust translation scaling curves to fine-tune mouse acceleration.
* Configure keybind translation layouts.

### 5. Installable PWA (Offline Support)
Zen Studio Live is built as a Progressive Web App (PWA):
* You can install it as a desktop shortcut (click the install icon in the Chrome address bar).
* Once installed, it **works offline** without an active internet connection.
* When online, updates to compiler drivers and features are applied automatically in the background.

---

## Browser Requirements & Troubleshooting

### WebHID & WebUSB Permission Requests
When connecting your device for the first time, your browser will trigger a device permission prompt:

```
  zenstudio.collectivemindsstore.com wants to connect to a HID device:
  [ Cronus Zen ] [ Connect ] [ Cancel ]
```
* **Fix**: Ensure your Zen is connected via the **PROG** micro-USB port (on the side of the device) to your computer. Click the device in the browser list and select **Connect**.

### Unsupported Browser Notice
If you load the site on **Firefox** or **Safari**, the hardware connection will be disabled. 
* **Reason**: WebHID and WebUSB are security-restricted and are currently unsupported by Mozilla Firefox and Apple Safari. You must use a Chromium-based browser (Chrome, Edge, or Brave) to transfer scripts.
