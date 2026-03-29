# Map Integration README

This document explains how the map is integrated into Jal Drishti, both in simple words and in technical terms.

## 1. Simple Explanation

The map is the visual backbone of Jal Drishti.

We first load a real satellite map in the browser. Then we place our own disaster-intelligence layers on top of it, such as:

- flood risk zones
- village boundaries
- population heatmaps
- rescue routes
- safe haven markers

So the map is not just a background. It is the main surface where all flood analysis is shown in a form that is easy to understand and act on.

## 2. Where The Map Is Connected

The map integration is handled in the frontend.

- `frontend/index.html`
  This file loads the mapping library and contains the map container.
- `frontend/assets/js/dashboard-app.js`
  This file creates the map, adds map sources and layers, and updates the map when the user changes village, rainfall, or rescue mode.

## 3. Library Used

Jal Drishti uses **MapLibre GL JS** as the map engine.

MapLibre is responsible for:

- creating the interactive map
- drawing raster satellite imagery
- loading GeoJSON sources
- rendering lines, fills, circles, symbols, and heatmaps
- supporting pitch, zoom, fly animations, and 3D terrain

## 4. Integration Flow

The map is integrated in this order:

1. `frontend/index.html` loads MapLibre CSS and JS.
2. The HTML page defines `<div id="map"></div>` as the map container.
3. `dashboard-app.js` runs when the page loads.
4. `run()` initializes the dashboard data.
5. `init3DMap()` creates the MapLibre map object.
6. `initLayers()` creates the flood and soil overlay layers.
7. `updateMapVision()` updates the visible map data for the selected village and timestep.
8. Rescue, population, and boundary layers are added as needed.

## 5. Base Map Setup

The base map uses satellite raster tiles.

- Satellite imagery source:
  Esri World Imagery
- Terrain elevation source:
  AWS Terrarium elevation tiles

This gives the project:

- a realistic satellite background
- 3D terrain effect
- better disaster visualization for hills, slopes, and low-lying zones

## 6. How Data Is Shown On The Map

The system uses multiple layer types on top of the satellite base map.

### Flood Risk Layer

Flood risk is shown as colored fill layers.

- green = lower risk
- yellow/orange = medium risk
- red/dark red = high to extreme risk

The flood layer changes based on:

- selected village
- rainfall input
- current simulation timestep

### Village Boundary Layer

Village limits are shown using a glowing dashed line. This helps the user see the operational area clearly.

### Population Heatmap

Population concentration is shown using a heatmap so responders can identify where more people may be at risk.

### Rescue Route Layer

When rescue mode is active, the system draws:

- rescue paths
- user/start marker
- safe haven markers
- route labels

This helps users see the safest available evacuation direction.

## 7. Current Data Behavior

At the moment, the frontend is running in **standalone synthetic mode**.

That means:

- the map integration is fully active
- the UI updates correctly
- map overlays are generated and rendered
- the live backend API is currently bypassed

In `dashboard-app.js`, `fetchFromAPI()` currently returns `null`, so the application falls back to locally generated or synthetic data.

This is useful for demos because the map still works even without a live backend service.

## 8. Key Functions Involved

Important map-related functions inside `frontend/assets/js/dashboard-app.js`:

- `run()`
  Starts the app and initializes data.
- `init3DMap()`
  Creates the actual MapLibre map.
- `initLayers()`
  Prepares flood and soil layers.
- `updateMapVision(village)`
  Moves the camera and refreshes active flood visuals.
- `addVillageBoundary(villageId)`
  Draws the selected village boundary.
- `updateAnalyticsLayers(village)`
  Updates population and analytics overlays.
- `renderAPIBoundary()`
  Renders API boundary data if available.
- `renderAPIPOIs()`
  Renders infrastructure and safe-haven points.
- `renderAPIPopulation()`
  Renders the population heatmap.

## 9. Why The Map Matters

The map is important because it turns technical output into operational understanding.

Instead of reading raw coordinates, flood scores, or model tables, a user can immediately see:

- where flooding is increasing
- which areas are exposed
- where people are concentrated
- which route is safer for rescue

In short, the backend does the analysis, and the map makes that analysis usable.

## 10. One-Line Explanation For Judges

"We integrated a real interactive satellite map and layered our flood prediction, population risk, and rescue intelligence on top of it so disaster decisions can be made visually and quickly."

## 11. Short Speaking Version

"In our project, the map is the main decision interface. We load a real satellite map using MapLibre, then place our own layers on top of it such as flood risk, village boundary, population density, and rescue routes. So the map is not only for viewing location, it becomes a live disaster management dashboard."

## 12. Related Files

- `frontend/index.html`
- `frontend/assets/js/dashboard-app.js`
- `frontend/assets/css/dashboard.css`
- `docs/system-technical-documentation.md`
