# Wheelchair Interface Remapper

The Wheelchair Interface Remapper lets people drive and control a powered
wheelchair through alternative input devices. It reads input from a standard
HID device — a **keyboard** or a **gamepad/joystick** — and translates it into
the HID control reports that a wheelchair
controller expects. A web UI lets a clinician or caregiver remap which input
maps to which wheelchair action without touching code.

This is intended as a flexible, low-cost access platform: pick whatever input
hardware works best for a given user and remap it to the wheelchair functions
they need.

> **Status:** Research/prototype code. It runs on real hardware (see
> [Hardware](#hardware)) and is shared in the hope it is useful. It is **not** a
> certified medical device. Use it at your own risk and test thoroughly before
> relying on it.

## Repository layout

| Path | What it is |
| --- | --- |
| [`remapper/`](remapper/) | Python core. Reads the input device, applies the active mapping, and writes wheelchair HID reports. Also hosts the Flask configuration API. Entry point: [`remapper/main.py`](remapper/main.py). |
| [`web-server/wdi-reconfigurer/`](web-server/wdi-reconfigurer/) | React single-page app for editing the input-to-action mappings. |

## How it works

```
  Input device (keyboard / gamepad)
        │  (Linux evdev: /dev/input/eventN)
        ▼
  remapper/main.py ── applies the active mapping from settings.json
        │                                   ▲
        │  writes HID report                │ reads/writes mapping
        ▼                                   │
  /dev/hidg0 (USB HID gadget)        Flask API (remapper/API.py, port 5000)
        │                                   ▲
        ▼                                   │ HTTP
  Wheelchair controller            React UI (web-server, port 3000)
```

- The remapper runs a simple state machine:
  - **RUN** (`STATE = 1`): input events are translated to wheelchair HID reports.
  - **CONFIGURE** (`STATE = 0`): driving is paused while the mapping is edited
    through the web UI; the new mapping is written to `settings.json` on upload.
- Mappings live in [`remapper/settings.json`](remapper/settings.example.json)
  (a runtime file — see [`settings.example.json`](remapper/settings.example.json)
  for the format). Per-input default option sets are defined in
  [`remapper/interface_dicts/`](remapper/interface_dicts/).
- HID report construction (byte/bit layout for drive, lights, seating, etc.)
  lives in [`remapper/wdi_report.py`](remapper/wdi_report.py).

## Supported inputs

- **Keyboard** — keys mapped to discrete actions (drive directions, lights,
  seating, speed, etc.). Supports up to 3 layers and combo bindings (two keys held simultaneously).
- **Gamepad / joystick** — buttons and analog axes. Supports up to 3 layers and combo bindings.

## Getting started

### Prerequisites

- Linux host (the remapper uses Linux `evdev` and a USB **HID gadget** at
  `/dev/hidg0`). It is designed to run on a single-board computer configured in
  USB gadget mode (see [Hardware](#hardware)).
- Python 3.10+
- Node.js 16+ and npm (for the web UI)
- Read access to the input device and write access to `/dev/hidg0` (typically
  requires running as root or adding the appropriate udev rules / group
  membership).

### 1. Run the remapper + configuration API

```bash
cd remapper
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Optional: choose the interface the API binds to (defaults below).
export REMAPPER_HOST=0.0.0.0      # default 0.0.0.0
export REMAPPER_PORT=5000         # default 5000
# Optional: allow the web UI's origin for CORS (comma-separated).
export REMAPPER_CORS_ORIGINS="http://localhost:3000"

python main.py
```

The remapper auto-detects connected input devices. Use the web UI to select the
active device and input type.

### 2. Run the web configuration UI

```bash
cd web-server/wdi-reconfigurer
npm install

# Point the UI at the remapper API (defaults to http://localhost:5000).
cp .env.example .env        # then edit REACT_APP_API_URL if needed
npm start                   # dev server on http://localhost:3000
# or
npm run build               # production build into ./build
```

Open the UI, choose an input type, remap actions, and upload — the remapper
picks up the new `settings.json` and resumes driving.

### Configuration

| Variable | Component | Default | Purpose |
| --- | --- | --- | --- |
| `REMAPPER_HOST` | remapper API | `0.0.0.0` | Interface the Flask API binds to. |
| `REMAPPER_PORT` | remapper API | `5000` | Port for the Flask API. |
| `REMAPPER_CORS_ORIGINS` | remapper API | `http://localhost:3000` | Comma-separated allowed CORS origins. |
| `REACT_APP_API_URL` | web UI | `http://localhost:5000` | Base URL of the remapper API. |

## Hardware

The remapper is built to run on a single-board computer (developed on an Orange
Pi) operating as a **USB HID gadget**. The board reads the chosen input device
via `evdev` and presents itself to the wheelchair controller as a HID device.

### USB gadget setup

The remapper writes HID reports to `/dev/hidg0`, created by `gadget/configfs.sh` using
the Linux USB gadget framework (ConfigFS + `libcomposite`). Run `gadget/configfs.sh`
as root on each boot before starting `main.py`.

`hid_desc.bin` is the USB HID Report Descriptor that defines the 10-byte report
format. It was hand-written based on the [WDI example descriptors](https://github.com/Open-Mobility-Hub/wheelchair-digital-interface/blob/main/docs/usb/example-report-descriptors.md).
See [`gadget/README.md`](gadget/README.md) for the annotated byte-by-byte breakdown.

**One-time system configuration (OrangePi)**

Add to `/boot/orangepiEnv.txt`:
```
dtoverlay=dwc2
```

Add to `/etc/modules`:
```
dwc2
libcomposite
```

Reboot after making these changes. The script requires root and must be run on
every boot. How you invoke it depends on your setup (e.g. `@reboot` in crontab,
a systemd unit, or manually). After a successful run, `/dev/hidg0` should exist.
If it does not appear, check `dmesg` for gadget or UDC errors.

## Wheelchair Digital Interface (WDI) Protocol 

The HID reports produced by this remapper follow the [WDI (Wheelchair Digital Interface) USB interface specification](https://github.com/Open-Mobility-Hub/wheelchair-digital-interface/blob/main/docs/usb/wdi-usb-interface.md), targeting the **LUCI** smart wheelchair controller.

The WDI specification designates certain buttons as implementation-specific, leaving vendors free to assign them as they choose. LUCI uses `BTN_EAST` as a proprietary "LUCI Button" whose function is not publicly documented. This mapping was reverse-engineered by probing the controller with a gamepad. The complete byte/bit mapping is defined in [`remapper/wdi_report.py`](remapper/wdi_report.py).

### Report format

Each report is **10 bytes**, written to `/dev/hidg0`:

| Bytes | Content |
| --- | --- |
| 0 | Left/right drive axis — signed integer, two's complement, range −100 to 100 |
| 1 | Forward/backward drive axis — signed integer, two's complement, range −100 to 100 |
| 2–6 | Button bitfields (drive controls, lights, seating presets, and chair functions) |
| 7 | Hat switch byte — encodes directional mode switching (neutral = `0x08`) |
| 8–9 | Keyboard HID keycodes for speed and profile selection |

### Adapting for a different controller

If your wheelchair uses the WDI interface but not LUCI, the standard WDI mappings in [`remapper/wdi_report.py`](remapper/wdi_report.py) can be kept as-is. Remove or reassign the `LUCI Button` entry and replace it with your controller's implementation-specific mapping. The report length and [`gadget/hid_desc.bin`](gadget/hid_desc.bin) do not need to change.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE.md) and
[NOTICE](NOTICE.md). Third-party components are listed in [NOTICE](NOTICE.md).
