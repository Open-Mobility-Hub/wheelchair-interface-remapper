# Gadget Setup

`configfs.sh` configures the OrangePi as a USB HID gadget using the Linux
ConfigFS / libcomposite framework. It must be run as root on every boot before
starting `main.py`.

## hid_desc.bin

`hid_desc.bin` is the raw USB HID Report Descriptor loaded into the kernel at
`functions/hid.usb0/report_desc`. It was hand-written based on the example
descriptors in the [WDI USB interface documentation](https://github.com/Open-Mobility-Hub/wheelchair-digital-interface/blob/main/docs/usb/example-report-descriptors.md).

The descriptor defines a **composite device** with two top-level Application
Collections — a gamepad (for drive axes, buttons, and hat switch) and a keyboard
(for speed and profile keycodes) — producing a **10-byte report**:

| Bytes | Bits | Content |
| --- | --- | --- |
| 0 | 8 | Left/right drive axis — signed, two's complement, −100 to 100 |
| 1 | 8 | Forward/backward drive axis — signed, two's complement, −100 to 100 |
| 2–6 | 40 | Button bitfield — 16 standard gamepad buttons + BTN_TRIGGER_HAPPY1–24 (one bit each) |
| 7 | 4+4 | Hat switch (0–7, neutral = 8) + 4 padding bits |
| 8–9 | 8+8 | Keyboard keycodes (one per byte, 0x00 = no key) |

### Annotated descriptor

```
; ── Gamepad Application Collection ───────────────────────────────────────────
05 01        ; Usage Page (Generic Desktop Controls)
09 05        ; Usage (Game Pad)
A1 01        ; Collection (Application)

; Drive axes: 2 × signed 8-bit (-100 to 100) ─────────────────────────────────
15 9C        ;   Logical Minimum (-100)
25 64        ;   Logical Maximum (100)
09 01        ;   Usage (Pointer)
A1 00        ;   Collection (Physical)
09 30        ;     Usage (X)  — left/right
09 31        ;     Usage (Y)  — forward/backward
75 08        ;     Report Size (8)
95 02        ;     Report Count (2)
81 02        ;     Input (Data, Variable, Absolute)
C0           ;   End Collection (Physical)

; Buttons 1–40: 16 standard gamepad buttons + BTN_TRIGGER_HAPPY1–24 ──────────
05 09        ;   Usage Page (Button)
19 01        ;   Usage Minimum (Button 1)
29 28        ;   Usage Maximum (Button 40)
15 00        ;   Logical Minimum (0)
25 01        ;   Logical Maximum (1)
75 01        ;   Report Size (1)
95 28        ;   Report Count (40)
81 02        ;   Input (Data, Variable, Absolute)

; Hat switch: 4-bit value (0–7) + 4-bit padding ──────────────────────────────
05 01        ;   Usage Page (Generic Desktop Controls)
09 39        ;   Usage (Hat Switch)
15 00        ;   Logical Minimum (0)
25 07        ;   Logical Maximum (7)
35 00        ;   Physical Minimum (0)
46 3B 01     ;   Physical Maximum (315 degrees)
65 14        ;   Unit (Degrees)
75 04        ;   Report Size (4)
95 01        ;   Report Count (1)
81 02        ;   Input (Data, Variable, Absolute)
75 04        ;   Report Size (4)  — padding
95 01        ;   Report Count (1)
81 03        ;   Input (Constant) — padding
C0           ; End Collection (Application — Gamepad)

; ── Keyboard Application Collection ──────────────────────────────────────────
05 01        ; Usage Page (Generic Desktop Controls)
09 06        ; Usage (Keyboard)
A1 01        ; Collection (Application)
05 07        ;   Usage Page (Keyboard/Keypad)
75 08        ;   Report Size (8)
95 02        ;   Report Count (2)
15 00        ;   Logical Minimum (0)
26 FF 00     ;   Logical Maximum (255)
05 07        ;   Usage Page (Keyboard/Keypad)
19 00        ;   Usage Minimum (0x00)
29 38        ;   Usage Maximum (0x38)
81 00        ;   Input (Data, Array, Absolute)
C0           ; End Collection (Application — Keyboard)
```
