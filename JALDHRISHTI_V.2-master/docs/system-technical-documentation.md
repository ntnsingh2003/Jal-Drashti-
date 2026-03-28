# Jal Drishti: Technical & Architectural Documentation
*Comprehensive Guide for Presentation & Development Reference*

---

## 1. Project Overview

### **Problem Statement**
Disaster management today suffers from **reactive** rather than **proactive** responses.
- **Generic Data:** Flood warnings are region-wide, not localized to specific streets or buildings.
- **Blind Rescue:** Rescue teams often navigate without knowledge of safe paths or submerged hazards.
- **Inefficient Logistics:** Resources (boats, medical kits) are distributed manually, leading to shortages in critical zones.

### **Solution: Jal Drishti (Water Vision)**
A **Mission Control Dashboard** that combines real-time 3D simulation, AI-driven risk assessment, and tactical support to turn data into life-saving decisions.
- **Visual Intelligence:** 3D Terrain & Flood Simulation.
- **Predictive Power:** AI-based Risk & Population analysis.
- **Tactical Support:** Automated Rescue Routing & Resource Optimization.

---

## 2. Technology Stack

### **Frontend (The Core Interface)**
- **Language:** HTML5, CSS3 (Glassmorphism), JavaScript (ES6+).
- **Mapping Engine:** **MapLibre GL JS** (High-performance WebGL rendering).
- **Visualization:** 
    - **Chart.js**: Temporal weather & forecast data.
    - **Custom Canvas Layers**: For dynamic flood water rendering.
- **State Management:** Reactive local state (`appState`) with event-driven updates.

### **Backend & Data Processing**
- **Language:** Python 3.9+ (Data Pre-processing).
- **libraries:** `numpy`, `scipy` (Optimization), `geopandas` (Spatial Data).
- **Simulation Logic:** Client-side heuristic modeling for real-time responsiveness.

### **Infrastructure & Deployment**
- **Hosting:** Vercel (Edge Network Distribution).
- **Source Control:** GitHub.
- **Data Formats:** GeoJSON (Vectors), AWS Terrarium (Elevation Tiles).

---

## 3. Core Algorithms & Logic (The "Secret Sauce")

### **A. Risk-Aware A* Pathfinding (Rescue Routes)**
*Goal: Find the safest and fastest path from a stranded user to a Safe Haven.*

1.  **Grid Generation:** The map is divided into a high-resolution grid (e.g., 40x40m cells).
2.  **Cost Function (`f = g + h + penalty`):**
    -   `g`: Distance from start.
    -   `h`: Euclidean distance to safe haven.
    -   **`penalty`**: The critical innovation.
        -   **Risk Weight (25x):** High flood depth = massive movement cost.
        -   **Danger Threshold (0.7):** If risk > 70%, the node is **IMPASSABLE** (Hard Block).
3.  **Path Smoothing:** Raw A* grid paths are jagged. We use **Catmull-Rom Splines** to create realistic, smooth curves for vehicle/foot navigation.

### **B. Intelligent Population Heatmap (AI Building Analysis)**
*Goal: Predict where people are actually located, avoiding random distribution.*

1.  **Terrain Analysis:** The system reads elevation data to identify "flat" vs "slope" vs "riverbed".
2.  **Building Prioritization:**
    -   If a `buildings.geojson` layer exists, 95% of population points are snapped to building centroids.
    -   If data is sparse, it uses an **inverse-risk probability**: `Prob(Pop) ∝ 1 / FloodRisk`.
3.  **Result:** Clusters appear in logical settlements, not in the middle of rivers or steep cliffs.

### **C. Mission-Linked Resource Optimization**
*Goal: Distribute scarce resources (Boats, Ambulances) where they save the most lives.*

1.  **Simulation Check:** Optimization is **blocked** if Rainfall = 0 (prevents false positives).
2.  **Risk-Weighted Demand:**
    -   `Demand_Cluster_i = Population_i * (1 + Risk_Score_i * 2.5)`
    -   A cluster of 100 people in *Extreme Risk* has higher priority than 200 people in *Low Risk*.
3.  **Heuristic Allocation:** 
    -   Sorts all clusters by `Demand_Score`.
    -   Greedily assigns inventory until depletion.
    -   **Stop Mechanism**: A dedicated interrupt flag allows the user to halt the `async` calculation loop instantly.

---

## 4. System Architecture

```mermaid
graph TD
    User[User / Disaster Manager] -->|Interacts| UI[Mission Control UI]
    
    subgraph Client_Side_App ["Browser (Client-Side Intelligence)"]
        UI -->|Triggers| Sim[Flood Simulation Engine]
        Sim -->|Updates| RiskGrid[Dynamic Risk Grid]
        
        RiskGrid -->|Feed Data| Path[A* Rescue Routing]
        RiskGrid -->|Feed Data| Heatmap[Population AI]
        RiskGrid -->|Feed Data| Optimizer[Resource Allocator]
        
        Optimizer -->|Output| Plan[Deployment Plan]
        Path -->|Output| Route[Safe Evacuation Path]
    end
    
    subgraph Data_Layer ["Static Data Sources"]
        AWS[AWS Terrarium (Elevation)] -->|Tiles| Map[MapLibre GL]
        GeoJSON[Boundaries & Buildings] -->|Vectors| Map
    end
    
    Client_Side_App -->|Visualizes on| Map
```

---

## 5. Key Differentiators (Why This Wins)

1.  **It's NOT Just a Map:** It's an active decision-support system. Most competitors show *what is happening*. Jal Drishti shows *what to do*.
2.  **Hyper-Local Intelligence:** We don't just say "Meppadi is flooded." We say "Route via Main St is blocked; use the Northern Ridge path."
3.  **Professional UX:** The interface mirrors real-world military/tactical dashboards (Dark mode, HUD elements), reducing cognitive load during high-stress disasters.

---

## 6. Future Scope

1.  **IoT Integration:** Connect to real-time river level sensors (Arduino/IoT) for live data feed.
2.  **Crowdsourcing:** Allow citizens to mark "SOS" locations via a mobile companion app.
3.  **Drone Link:** Import drone aerial imagery overlays for post-disaster damage assessment.
