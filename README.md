
# 📖 ReadMode

**ReadMode** is a simple tool to **toggle reading mode on Linux using X11**. Reading mode adjusts the screen color temperature to reduce blue light, helping to reduce eye strain when reading or working at night.

---

## 🚀 Features

- ✅ Enable or disable reading mode on any X11-based Linux desktop (GNOME, KDE, XFCE, etc.).
- ✅ Standalone executable with no external dependencies.
- ✅ Can run silently in the background.
- ✅ Simple interface via desktop launcher or terminal.
- ✅ Compatible with most Linux distributions.

---

## 🖥️ Requirements

- A Linux desktop environment using **X11** (not compatible with Wayland).
- Tested on Ubuntu, Debian, Mint, Arch, Fedora, and others.

---

## 🔧 Installation

### ✅ Method 1 — Install system-wide (recommended)

1. Copy the executable to the system's binary folder:

```bash
sudo cp ReadMode /usr/local/bin/
```

2. Copy the icon to the system icons directory:

```bash
sudo cp ReadMode.png /usr/share/icons/hicolor/256x256/apps/
```

3. Copy the desktop launcher to the applications directory:

```bash
sudo cp ReadMode.desktop /usr/share/applications/
```

4. (Optional) Update the icon cache to ensure the icon displays properly:

```bash
sudo gtk-update-icon-cache /usr/share/icons/hicolor/
```

5. ✅ Done!  
**ReadMode** will now appear in your application menu. You can also run it from the terminal simply by typing:

```bash
ReadMode
```

---

### ✅ Method 2 — Run locally (portable mode)

If you don't want to install it system-wide, you can run it directly from any folder:

1. Make sure the executable and desktop file are in the same folder.

2. Edit `ReadMode.desktop` and update the paths:

```ini
Exec=/path/to/your/folder/ReadMode
Icon=/path/to/your/folder/ReadMode.png
```

3. Make the desktop file executable:

```bash
chmod +x ReadMode.desktop
```

4. Double-click the desktop file to run it.

❗ Note: In portable mode, the launcher won’t show in the main applications menu unless installed to `/usr/share/applications/`.

---

## 🧠 Usage

### 🔥 From the terminal:

```bash
ReadMode
```

✔️ This toggles reading mode on or off automatically based on the current time of your System.

### 🔥 From the desktop menu or launcher:

- ✔️ Click → Toggle reading mode (on/off) based on the current time of your System.

---

## ⚙️ How It Works

- Uses X11 commands (`xrandr`) and Xlib (Xlib11) APIs to adjust screen gamma and color temperature.
- Reduces blue light to protect your eyes and improve comfort during reading or nighttime use.
- It will automatically changes betwen modes based on the current time starts at 16:00 and finish at 06:00 

---

## 🐧 Compatibility

- ✅ Ubuntu, Debian, Linux Mint, Pop!_OS, MX Linux.
- ✅ Arch Linux, Manjaro, EndeavourOS.
- ✅ Fedora, OpenSUSE.
- ❌ Not compatible with Wayland (X11 only).
- x  Not compatible with Windows

---

## 👨‍💻 Author

- **@FreyreCorona**

---

## 📝 License

This project is licensed under the **GNU General Public Licence (GPL.3)**.  

