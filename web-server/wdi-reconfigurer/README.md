# WDI Reconfigurer (web UI)

The web configuration UI for the [Wheelchair Interface Remapper](../../README.md).
It lets a user remap input-device controls to wheelchair actions and upload the
result to the remapper's configuration API.

This is a [Create React App](https://create-react-app.dev/) project.

## Setup

```bash
npm install
cp .env.example .env     # set REACT_APP_API_URL to your remapper API
```

| Variable | Default | Purpose |
| --- | --- | --- |
| `REACT_APP_API_URL` | `http://localhost:5000` | Base URL of the remapper Flask API. |

## Scripts

- `npm start` — run the dev server at <http://localhost:3000>.
- `npm run build` — produce a production build in `build/`.
- `npm test` — run the test runner.

## How it fits together

The UI talks to the remapper API (see [`../../remapper/API.py`](../../remapper/API.py)):
it fetches the current input type and per-mode settings, lets the user edit the
mappings, and POSTs them back. On upload, the remapper writes `settings.json`
and resumes driving with the new mapping.

See the [project README](../../README.md) for the full architecture.
