# 🛰️ BMX Core — Bitcoin Mining Metrics Dashboard

**BMX Core** is a fully interactive data dashboard designed to visualize Bitcoin mining activity across the globe.  
Built with Python, Plotly Dash, and hosted on Render, it helps users explore environmental impact, regional stats, and mining volumes at a glance.

---

## 🔗 Live App

**Coming soon:** [https://bitcoinmetrics.org](https://bitcoinmetrics.org)

---

## 📊 Key Features

### 🌍 Globe Visualization

- Dark-themed 3D globe with **emissive gold lighting**
- Base globe color: deep gray `#1a1a1a`
- **Eco-friendly companies** displayed in green, **high-carbon companies** in red
- Companies visualized as 3D buildings with height scaled to mining volume
- Smooth animations when showing or hiding buildings
- Click on a point to view company info in a draggable popup
- Label rendering for either **city** or **country** (not both) to reduce clutter
- Clean UI with responsive hover effects and popups styled by carbon category

### 🎛 Interactive Controls

- **Show Mining Buildings** toggle button (bottom center)
- **Green / High** carbon-level filters highlight matching buildings and pause rotation
- Popup and UI elements update in real time with filter selection
- Camera pans to selected company without zooming distortion

---

## 📁 Data Handling

- Based on `mining_locations.json`  
- Each record contains:
  - `lat`, `lng`, `company_name`, `mining_volume`, `co2_level`
- Eco-friendly logic:
  - `co2_level === 'green'` **AND**
  - Company name contains “energy” or “eco”
- Mining volumes normalized between `0 - 0.5` altitude units (up to 50cm display height)

---

## 🛠️ Tech Stack

- Python
- Dash & Plotly
- Dash Bootstrap Components
- Deployed on Render

---

## 🚀 Performance & UX

- Optimized for 60fps animation using `requestAnimationFrame`
- Internal state managed for popups, filters, and animations
- All UI actions toggle through well-isolated states
- Clean, minimal layout with focus on smooth user experience

---

## 📌 Roadmap

- Add live mining data from blockchain APIs
- Enable user-uploaded data overlays
- Multi-globe comparison mode (region vs region)

---

## 📜 License

MIT License
