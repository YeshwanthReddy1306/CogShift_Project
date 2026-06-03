# ⚙️ CogShift — 3D Gear Logic Puzzle Game

> A fully playable 3D puzzle game built with **Python + Panda3D**, featuring procedural geometry, BFS power propagation, C++ integration, and a GitHub Actions CI pipeline.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Panda3D](https://img.shields.io/badge/Panda3D-1.10-green?logo=panda3d)
![C++](https://img.shields.io/badge/C++-17-00599C?logo=c%2B%2B&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎮 What is CogShift?

CogShift is a **3D mechanical puzzle game** where you rotate interconnected gears to transfer power from a **green source** to a **yellow target**. Each level introduces new challenges — locked gears, branching chains, and direction constraints — that require logical thinking to solve.

```
🟢 Source Gear  →  ⚪ Normal Gear  →  🟡 Target Gear
   (always CW)      (click to flip)     (must be powered)
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🧩 **Puzzle Logic** | BFS power propagation — meshing gears always reverse direction |
| 🎯 **Mouse Picking** | Collision ray-casting for precise gear click detection |
| 🔄 **Spin Animation** | Powered gears spin in real-time using Panda3D intervals |
| 📐 **Procedural Models** | Gear meshes generated at runtime via Panda3D's EGG API |
| ⚡ **C++ Module** | BFS direction logic and torque ratio implemented in C++ |
| 🗂️ **JSON Levels** | All levels defined in `levels/levels.json` — no code changes needed |
| ✅ **CI Pipeline** | GitHub Actions runs flake8 lint + pytest on every push |

---

## 🕹️ How to Play

| Action | Result |
|---|---|
| **Click** a grey gear | Toggle its spin direction (CW ↔ CCW) |
| 🔴 Red gear | Locked — cannot be rotated |
| 🟢 Green gear | Power source — always spinning clockwise |
| 🟡 Yellow gear | Target — must receive power to win the level |

Power travels along connected edges. **Meshing gears always reverse direction.**  
Get power to every yellow gear to advance to the next level!

---

## 📁 Project Structure

```
cogshift/
├── main.py                   # Entry point — initialises ShowBase, lighting, camera
├── requirements.txt          # pip dependencies
│
├── game/
│   ├── gear.py               # Gear data model, colour coding, spin animation
│   ├── level_manager.py      # JSON level loader, BFS propagation, win detection
│   ├── input_handler.py      # Mouse ray-cast → collision sphere → gear interaction
│   ├── rotation_bridge.py    # C++ bridge with pure-Python fallback
│   └── ui.py                 # HUD, level label, win screen, next-level button
│
├── levels/
│   └── levels.json           # 5 hand-crafted puzzle levels
│
├── tools/
│   └── generate_gear.py      # Procedural gear .egg model generator
│
├── cpp/
│   └── rotation_utils.cpp    # C++ BFS + torque ratio module
│
├── tests/
│   └── test_logic.py         # pytest unit tests (headless, no window needed)
│
└── .github/
    └── workflows/ci.yml      # GitHub Actions — lint + test on every push
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/YeshwanthReddy1306/CogShift_Project.git
cd CogShift_Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the 3D gear model
python tools/generate_gear.py

# 4. Run tests
pytest tests/ -v

# 5. Launch the game!
python main.py
```

---

## 🧠 Technical Highlights

### BFS Power Propagation
Every time a player rotates a gear, a **Breadth-First Search** traverses the gear graph from the source, assigning clockwise/counter-clockwise directions. Meshing gears always reverse their neighbour's direction — just like real gears.

### C++ Integration
The core BFS logic and torque ratio calculation are implemented in `cpp/rotation_utils.cpp` and bound to Python via Panda3D's interrogate tool. A Python fallback ensures the game runs even without the compiled module.

### Procedural Geometry
Rather than loading external assets, gear meshes are **generated at runtime** using Panda3D's EGG API — front faces, back faces, and side walls are all computed from parametric tooth geometry.

---

## 📋 Levels

| # | Name | Challenge |
|---|---|---|
| 1 | Tutorial | 3 gears in a line — learn the basics |
| 2 | Branch | Power splits across two paths |
| 3 | Direction Challenge | Locked gear blocks the chain |
| 4 | The Cross | Source at centre, 3 targets to power |
| 5 | Zigzag | Navigate a winding locked-gear path |

---

## 🛠️ Built With

- [Python 3.14](https://www.python.org/)
- [Panda3D 1.10](https://www.panda3d.org/)
- [C++17](https://isocpp.org/)
- [pytest](https://pytest.org/)
- [GitHub Actions](https://github.com/features/actions)

---

## 👨‍💻 Author

**Yeshwanth Reddy**  
[![GitHub](https://img.shields.io/badge/GitHub-YeshwanthReddy1306-181717?logo=github)](https://github.com/YeshwanthReddy1306)

---

*Built as a portfolio project demonstrating Python game development, 3D engine integration, C++ interop, and software engineering best practices.*
