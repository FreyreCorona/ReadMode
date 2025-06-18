from ctypes import Structure,CDLL,POINTER,c_int,c_ulong,c_void_p,c_char_p,c_ushort,cast
from datetime import datetime
import time
import atexit
import signal
import sys

display = None
res = None

libX11 = CDLL("libX11.so")
libXrandr = CDLL("libXrandr.so")

Display_p = c_void_p
Window = c_ulong
RRCrtc = c_ulong

class XRRScreenResources(Structure):
    _fields_ = [
        ("timestamp", c_ulong),
        ("configTimestamp", c_ulong),
        ("ncrtc", c_int),
        ("crtcs", POINTER(RRCrtc)),
        ("noutput", c_int),
        ("outputs", POINTER(c_ulong)),
        ("nmode", c_int),
        ("modes", c_void_p),
    ]

class XRRCrtcGamma(Structure):
    _fields_ = [
        ("size", c_int),
        ("red", POINTER(c_ushort)),
        ("green", POINTER(c_ushort)),
        ("blue", POINTER(c_ushort)),
    ]

libX11.XOpenDisplay.restype = Display_p
libX11.XOpenDisplay.argtypes = [c_char_p]
libX11.XCloseDisplay.restype = c_int
libX11.XCloseDisplay.argtypes = [Display_p]
libX11.XDefaultScreen.restype = c_int
libX11.XDefaultScreen.argtypes = [Display_p]
libX11.XRootWindow.restype = Window
libX11.XRootWindow.argtypes = [Display_p,c_int]

libXrandr.XRRSetCrtcGamma.restype = None
libXrandr.XRRSetCrtcGamma.argtypes = [Display_p,RRCrtc,POINTER(XRRCrtcGamma)]
libXrandr.XRRGetCrtcGamma.restype = POINTER(XRRCrtcGamma)
libXrandr.XRRGetCrtcGamma.argtypes = [Display_p,RRCrtc]
libXrandr.XRRGetCrtcGammaSize.restype = c_int
libXrandr.XRRGetCrtcGammaSize.argtypes = [Display_p,RRCrtc]
libXrandr.XRRGetScreenResources.restype = POINTER(XRRScreenResources)
libXrandr.XRRGetScreenResources.argtypes = [Display_p,Window]
libXrandr.XRRAllocGamma.restype = POINTER(XRRCrtcGamma)
libXrandr.XRRAllocGamma.argtypes = [c_int]
libXrandr.XRRFreeGamma.restype = None
libXrandr.XRRFreeGamma.argtypes = [POINTER(XRRCrtcGamma)]
libXrandr.XRRFreeScreenResources.restype = None
libXrandr.XRRFreeScreenResources.argtypes = [POINTER(XRRScreenResources)]

def open_display():
    display = libX11.XOpenDisplay(None)
    if not display:
        raise OSError('Error to connect to the X server')
    return display

def get_screen_resources(display, root):
    return libXrandr.XRRGetScreenResources(display, root)

def alloc_gamma(size):
    return libXrandr.XRRAllocGamma(size)

def free_gamma(gamma):
    libXrandr.XRRFreeGamma(gamma)

def set_gamma(display, crtc, gamma):
    libXrandr.XRRSetCrtcGamma(display, crtc, gamma)

def get_gamma_size(display, crtc):
    return libXrandr.XRRGetCrtcGammaSize(display, crtc)

def enable_warm_mode(display, res):
    crtcs = cast(res.contents.crtcs, POINTER(RRCrtc * res.contents.ncrtc)).contents

    for crtc in crtcs:
        gamma_size = get_gamma_size(display, crtc)
        gamma = alloc_gamma(gamma_size)
        red = cast(gamma.contents.red, POINTER(c_ushort * gamma_size)).contents
        green = cast(gamma.contents.green, POINTER(c_ushort * gamma_size)).contents
        blue = cast(gamma.contents.blue, POINTER(c_ushort * gamma_size)).contents

        for i in range(gamma_size):
            value = int(i * (65535 / (gamma_size - 1)))
            red[i] = value
            green[i] = int(value * 0.85)
            blue[i] = int(value * 0.75)

        set_gamma(display, crtc, gamma)
        free_gamma(gamma)

def disable_warm_mode(display, res):
    crtcs = cast(res.contents.crtcs, POINTER(RRCrtc * res.contents.ncrtc)).contents

    for crtc in crtcs:
        gamma_size = get_gamma_size(display, crtc)
        gamma = alloc_gamma(gamma_size)

        red = cast(gamma.contents.red, POINTER(c_ushort * gamma_size)).contents
        green = cast(gamma.contents.green, POINTER(c_ushort * gamma_size)).contents
        blue = cast(gamma.contents.blue, POINTER(c_ushort * gamma_size)).contents

        for i in range(gamma_size):
            value = int(i * (65535 / (gamma_size - 1)))
            red[i] = value
            green[i] = value
            blue[i] = value

        set_gamma(display, crtc, gamma)
        free_gamma(gamma)

def is_night():
    now = datetime.now().time()
    if now >= datetime.strptime('18:00','%H:%M').time() or now <= datetime.strptime('06:00','%H:%M').time():
        return True
    return False

def cleanup():
    global display, res

    if display and res:
        disable_warm_mode(display,res)
        libXrandr.XRRFreeScreenResources(res)
        libX11.XCloseDisplay(display)

atexit.register(cleanup)

def handle_signal(signum,frame):
    sys.exit(0)

signal.signal(signal.SIGINT,handle_signal)
signal.signal(signal.SIGTERM,handle_signal)

def main():
    global display,res
    is_activated = False
    print('This program activates and deactivates the read-mode from your screen automatically from 16:00 hours to 06:00 hours')
    while True:
        display = open_display()
        screen = libX11.XDefaultScreen(display)
        root = libX11.XRootWindow(display, screen)
        res = get_screen_resources(display, root)
        if is_night() and not is_activated:
            print('Turning ON the Read-Mode')
            enable_warm_mode(display,res)
            is_activated = True
        elif not is_night() and is_activated:
            print('Turning OFF the Read-Mode')
            disable_warm_mode(display,res)
            is_activated = False
        
        time.sleep(3600)

        libXrandr.XRRFreeScreenResources(res)
        libX11.XCloseDisplay(display)


if __name__ == "__main__":
    main()

