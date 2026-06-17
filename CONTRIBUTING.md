# Contributing

Thanks for your interest in improving the Wheelchair Interface Remapper.
Contributions of all kinds are welcome — bug reports, documentation, and code.

## Ground rules

- This project controls assistive mobility hardware. Prioritize **safety and
  predictability**. When in doubt about a change that affects driving behavior,
  describe the safety reasoning in your pull request.
- Be respectful and constructive in issues and reviews.

## Getting set up

See the [README](README.md) for full setup instructions. In short:

- **Remapper / API** (Python 3.10+):
  ```bash
  cd remapper
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  ```
- **Web UI** (Node.js 16+):
  ```bash
  cd web-server/wdi-reconfigurer
  npm install
  ```

Note that exercising the full input→HID path requires Linux with `evdev` and a
USB HID gadget (`/dev/hidg0`). Logic changes can often be reviewed without the
hardware, but please test on real hardware before changing driving behavior.

## Making changes

1. Fork the repository and create a feature branch.
2. Keep changes focused; one logical change per pull request.
3. Match the existing code style:
   - Python: standard PEP 8; the ROS package is linted with `ament_flake8` and
     `ament_pep257`.
   - JavaScript/React: follows the Create React App ESLint config.
4. Add the Apache license header to any **new** source file (see existing files
   for the exact text).
5. Update documentation (README, `settings.example.json`, etc.) when behavior
   or configuration changes.

## Tests / checks

- Web UI: `npm test` and `npm run build` in `web-server/wdi-reconfigurer/`.

## Licensing of contributions

By submitting a contribution, you agree that it is licensed under the
[Apache License, Version 2.0](LICENSE.md), consistent with the rest of the project.
