# Caelestis RGB

A small Caelestia hook that integrates with OpenRGB to control RGB lighting, based on your theme, while running Caelestia.

## Overview

Caelestis RGB connects with Caelestia theme file, reads it, and sets all OpenRGB compatible lighting devices accordingly to your theme, after making sure it's the most optimized color for an RGB led device, quantizing it with CIEDE2000.

## Requirements

- Caelestia
- OpenRGB
- RGB hardware supported by OpenRGB

## Installation

1. Clone this repo to any desired directory;

    ``` sh
    git clone https://github.com/batalhadev/Caelestis-RGB.git
    ```

2. Ensure the hook and the script are executable:

    ``` sh
    chmod +x ~*/desired/directory/*openrgbMYOU ~*/desired/directory/*caelestia-openrgb-daemon.sh
    ```

3. Configure your hypr-conf.lua to load the hook on startup with:

   ``` lua
   hl.on("hyprland.start", function()
    hl.exec_cmd("~*/desired/directory/*caelestia-openrgb-daemon.sh")
   end)
   ```

4.(Optional) Configure a system service to execute the caelestia-openrgb-daemon.sh on wake up, if you use the hybernation or sleep feature.

## Usage

You don't need to have openRGB running for the script to run sucessfully, the script uses the openRGB cli. If you want to tinker with the quantize_color.py, or just test things out, use the -d option when running openrgbMYOU script to skip the lengthy OpenRGB setup.

## License

Modify and use it as needed for your Caelestia/OpenRGB setup.
