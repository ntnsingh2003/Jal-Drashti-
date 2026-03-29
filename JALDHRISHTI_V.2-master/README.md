# Jal Drishti

Jal Drishti is a flood intelligence and mission control project for rainfall simulation, flood risk visualization, rescue routing, and resource allocation.

## What This Project Does

Jal Drishti is designed as a disaster-response support system. It combines a map-based dashboard with backend analytical logic so a user can:

- view simulated flood conditions for selected locations
- inspect flood risk trends and exposed population
- estimate safer rescue paths between points
- evaluate how limited emergency resources should be distributed

The current project is structured as a static frontend experience plus a Python backend demo of the core algorithms.

## How The System Works

The project has two main parts:

- `frontend/`: the user-facing dashboard
- `backend/`: the Python logic for route estimation, flood-risk demonstration, and resource allocation

The frontend focuses on interaction and visualization:

- mission-control layout
- rainfall controls and time-based simulation
- population risk summaries
- rescue mode and route visualization
- methodology and user-guide pages

The backend focuses on computational logic:

- `RescuePathFinder` estimates a travel path between two coordinates
- `ResourceAllocator` computes response-time cost matrices and allocates resources to clusters
- `backend/app.py` demonstrates the main backend features from the terminal

## Core Features

### 1. Flood Risk Visualization

The dashboard simulates flood progression over time and presents flood risk through map layers, metrics, and summaries. It is built to help users understand where risk is increasing and which zones need attention first.

### 2. Rescue Route Estimation

The rescue routing module estimates a path between a source and a destination and returns:

- path coordinates
- approximate distance in meters
- approximate travel time in minutes

At the moment, the backend path finder uses straight-line distance as a simplified travel-time proxy.

### 3. Resource Allocation

The resource allocator models how emergency resources such as ambulances, boats, and relief kits can be assigned to affected clusters. It supports:

- minimizing worst-case response time
- minimizing average response time
- estimating coverage population
- generating deployment plans and recommendations

### 4. Documentation Pages

The project includes two static documentation pages inside the frontend:

- `user-guide.html`: explains how to operate the dashboard
- `methodology.html`: explains the hydrological and risk-modeling concepts used in the UI

## Project Structure

```text
JALDHRISHTI_V.2-master/
|-- frontend/
|   |-- index.html
|   |-- pages/
|   |   |-- methodology.html
|   |   `-- user-guide.html
|   `-- assets/
|       |-- css/
|       |   `-- dashboard.css
|       |-- js/
|       |   `-- dashboard-app.js
|       `-- images/
|           `-- graphs/
|-- backend/
|   |-- app.py
|   |-- requirements.txt
|   `-- services/
|       |-- rescue_path_finder.py
|       `-- resource_allocator.py
|-- docs/
|   `-- system-technical-documentation.md
|-- vercel.json
`-- .env.local
```

## Important Files

- `frontend/index.html`: main dashboard page
- `frontend/assets/js/dashboard-app.js`: frontend logic and interactions
- `frontend/assets/css/dashboard.css`: styling and responsive layout
- `frontend/pages/user-guide.html`: operational guide
- `frontend/pages/methodology.html`: technical explanation page
- `backend/app.py`: backend demo entry point
- `backend/services/rescue_path_finder.py`: route estimation service
- `backend/services/resource_allocator.py`: resource planning service
- `docs/system-technical-documentation.md`: additional technical reference
- `docs/map-integration-readme.md`: focused explanation of how the map is integrated into the project

## Local Development

### Run The Frontend

Start a simple local web server from the project root:

```bash
python -m http.server 8001
```

Open:

```text
http://localhost:8001/frontend
```

### Run The Backend Demo

Run the backend demonstration module:

```bash
python -m backend.app
```

This demo shows:

- rescue path estimation
- resource allocation example output
- a simple flood risk classification example

## Deployment

Vercel can be configured in either of these ways:

1. Project root set to the repository root.
   In this case, the root `vercel.json` rewrites incoming routes to the `frontend/` directory so the static dashboard can be served directly.

2. Project root set to `frontend`.
   In this case, Vercel should use `frontend/vercel.json`, and no extra rewrites are needed because `index.html` is already at that deployment root.

If you see Vercel's `404: NOT_FOUND` page, verify that the Vercel project's **Root Directory** matches the config being used. A common failure mode is keeping the project root set to `frontend` while Vercel is still reading rewrite targets intended for the repository root.

## Dependencies

Install Python dependencies with:

```bash
pip install -r backend/requirements.txt
```

## Current Scope And Limitations

- The frontend is static and runs without a full API server.
- The backend currently demonstrates algorithmic behavior rather than serving a live production API.
- The rescue path finder is simplified and does not yet use road-network or terrain-aware routing.
- The dashboard is suitable as a prototype, demo, or base for further full-stack integration.

## Notes

- `.env.local` is available for local environment settings.
- Python may generate `__pycache__` directories after execution.
- The frontend, backend, and docs are now separated by responsibility for easier maintenance.
- `backend/requirements.txt` is kept inside the backend folder so Vercel can treat the repository root as a static frontend deployment.
"# Jal-Drashti-" 
"# Jal-Drashti-" 
