import subprocess
import time
import os

from screeninfo import get_monitors


# =========================================================
# SETTINGS
# =========================================================

DISPLAY_URL = "http://127.0.0.1:8000/display"

CHROME_PROFILE = os.path.join(
    os.environ["TEMP"],
    "ReceptionistRobotChrome"
)


# =========================================================
# FIND HDMI DISPLAY
# =========================================================

def find_hdmi_display():

    monitors = get_monitors()

    print()
    print("Detected displays:")
    print("==============================")

    for monitor in monitors:

        print(
            f"Name: {monitor.name} | "
            f"Position: ({monitor.x}, {monitor.y}) | "
            f"Size: {monitor.width}x{monitor.height}"
        )

    print("==============================")


    for monitor in monitors:

        if monitor.width == 800 and monitor.height == 480:

            return monitor

    return None


# =========================================================
# FIND CHROME
# =========================================================

def find_chrome():

    chrome_paths = [

        r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        )
    ]

    for path in chrome_paths:

        if os.path.exists(path):

            return path

    return None


# =========================================================
# OPEN HDMI DISPLAY
# =========================================================

def open_display():

    chrome = find_chrome()

    if chrome is None:

        print("ERROR: Google Chrome was not found.")

        return


    monitor = find_hdmi_display()

    if monitor is None:

        print(
            "ERROR: 800x480 HDMI display was not detected."
        )

        return


    print()
    print("HDMI display found.")

    print(
        f"Position: {monitor.x}, {monitor.y}"
    )

    print(
        f"Resolution: "
        f"{monitor.width}x{monitor.height}"
    )


    os.makedirs(
        CHROME_PROFILE,
        exist_ok=True
    )


    # =====================================================
    # CHROME KIOSK MODE
    # =====================================================

    command = [

        chrome,

        f"--user-data-dir={CHROME_PROFILE}",

        "--new-window",

        # Put Chrome on HDMI
        f"--window-position={monitor.x},{monitor.y}",

        # Match HDMI
        f"--window-size={monitor.width},{monitor.height}",

        # TRUE FULLSCREEN / KIOSK
        "--kiosk",

        # Disable browser UI
        "--disable-infobars",

        "--disable-session-crashed-bubble",

        "--disable-features=Translate",

        # Open display
        DISPLAY_URL
    ]


    print()
    print("Launching receptionist display...")
    print()

    subprocess.Popen(command)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print()
    print("===================================")
    print(" Receptionist HDMI Display")
    print("===================================")

    time.sleep(2)

    open_display()

    print()
    print("Display launcher finished.")