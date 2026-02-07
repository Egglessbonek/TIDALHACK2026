# 🖍️ Master Project Specification: "Causal Canvas"

**Project Name:** Causal Canvas (The Living City)
**Type:** Web-based Policy Simulator / City Builder
**Theme:** "Digital Pop-Up Book" (Hand-drawn, Crayon, Graph Paper aesthetic)

---

## 1. The Core Concept
A 2D side-scrolling city builder where the user acts as a policy maker. The goal is to balance **Economy**, **Environment**, and **Happiness** by drawing buildings into empty slots.
* **The Hook:** It uses **Causal AI** logic. Actions have unintended Second-Order Effects (e.g., Building a factory increases jobs $\to$ increases pollution $\to$ decreases health $\to$ lowers tax revenue).
* **The Stakes:** **No Undo.** Mistakes are permanent and costly. The user must live with their policy decisions or pay heavily to fix them.

---

## 2. The Tech Stack & Architecture
**Monorepo Structure:**
* `/frontend` (SvelteKit + TypeScript + Tailwind CSS)
* `/backend` (Python FastAPI + `DoWhy` for Causal Inference)

**Key Libraries:**
* **Styling:** Tailwind CSS + Custom CSS for "wobbly" hand-drawn borders.
* **Rendering:** `Rough.js` (for procedural sketch lines) + SVG Assets.
* **Animation:** Svelte Transitions / Framer Motion (for physics-based UI).
* **AI (Frontend):** TensorFlow.js (MobileNet) for recognizing user sketches.
* **AI (Backend):** `DoWhy` (Causal Logic) + LangChain (RAG for "feeding" the city data).

---

## 3. Visual Design (The "Paper Theater")
**Perspective:** 2D Panoramic Side-Scroller.

**Parallax Layers:**
1.  **Background (Static):** Sky, distant mountains (pencil sketches). Atmosphere changes here (Grey smog vs. Blue sky).
2.  **Mid-Ground (Reactive):** Infrastructure density. Starts empty; fills with roads/power lines as the city grows.
3.  **Foreground (Active):** The 10 Building Slots and the "Ground Line" where stick-figure agents walk.

**Aesthetic Rules:**
* Everything looks drawn with crayons on graph paper.
* Fonts: "Kalam" or "Permanent Marker."
* UI Panels: Look like crumpled paper or masking tape.

---

## 4. Gameplay Mechanics

### A. The Map Layout (10 Slots)
The world is a horizontal strip divided into zones:
* **Slots 0-2 (The Grime Zone):** Industrial focus. Dirty paper texture.
* **Slots 3-6 (The Bridge/Transit):** Connects work to home.
* **Slots 7-9 (The Green Zone):** Residential/Nature focus. Clean paper texture.

### B. The Building Palette (10 Types)
Each building has a **Cost**, **Upkeep (per tick)**, and **Causal Effect**.

| Building | Sketch Shape | Role | Trade-off |
| :--- | :--- | :--- | :--- |
| **1. Coal Factory** | Box + Smoke Stacks | Industry | High Jobs/Tax, Heavy Pollution. |
| **2. Nuclear Plant** | Dome | Power | Massive Energy, Meltdown Risk. |
| **3. Skyscraper** | Tall Rectangle | Business | High Jobs, High Traffic/Noise. |
| **4. Residential House** | Square + Triangle Roof | Housing | +Pop, Needs Jobs/Parks. |
| **5. High Density Apts** | Grid Box | Housing | +++Pop, +Crime Risk. |
| **6. Hospital** | Cross (+) | Service | ++Health, **High Upkeep Cost**. |
| **7. School** | Flag on Roof | Service | ++Tech/Stability, **High Upkeep**. |
| **8. Park / Tree** | Cloud on Stick | Nature | ++Happiness, Zero Income. |
| **9. Wind Turbine** | Pinwheel | Green Energy | Clean Power, Low Output. |
| **10. Landfill** | Mound | Waste | Essential for High Pop, Lowers Land Value. |

### C. The "Draw-to-Build" Interaction
1.  User clicks an empty slot (marked with a "For Sale" sign).
2.  A `<canvas>` overlay appears.
3.  User sketches the shape (e.g., a square with a roof).
4.  **AI Recognition:** The system classifies the sketch.
    * *Match:* Spawns the corresponding "Crayon Asset." Deducts money.
    * *No Match:* Asks user to try again.

### D. The Economy Game Loop
Runs every **2 seconds (1 Tick)**.
* **Formula:** `Income = (Population * Base Tax * Happiness_Multiplier) - Total_Upkeep`
* **Visuals:**
    * **Positive:** Green dollar signs float up from houses.
    * **Negative:** Red numbers drop from the UI.
    * **Recession:** World colors desaturate (turn sepia).

---

## 5. UI Components

### The "Paper Pull" Dashboard
A side panel hidden off-screen (right).
* **Trigger:** A piece of masking tape sticking out.
* **Action:** Click & Drag to slide a crumpled sheet of lined paper over the screen.
* **Content:**
    * **Stats:** Happiness (Smiley Face), Treasury (Piggy Bank).
    * **Log:** A narrative timeline of the city's history (e.g., *"Turn 5: Built Factory. Turn 8: Asthma rate rose."*).

### The Atmosphere System
Global variables controlled by the "Master Agent":
* **Fog Level:** Renders grey scribbles over the screen.
* **Chaos:** Renders "jitter" on building lines using `Rough.js`.

---

## 6. Development Roadmap (Phase 1)
1.  **Setup:** Initialize SvelteKit in `/frontend`. Install Tailwind & Rough.js.
2.  **State:** Create `stores/game.ts` to hold the Money, Population, and Slot Array.
3.  **Layout:** Build the `ParallaxWorld.svelte` component with horizontal scrolling.
4.  **Logic:** Implement the `GameLoop` to trigger the 2-second economy tick.
