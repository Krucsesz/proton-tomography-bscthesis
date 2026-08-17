# Proton tomography simulation and data analysis (BSc Thesis)

A Monte-Carlo simulation and data processing pipeline developed for my Computational Physics BSc thesis at Eötvös Loránd University. This analysis was conducted in alignment with the research efforts of the international Bergen pCT collaboration.

This project simulates proton-beam transport for medical physics and includes a complete analytical workflow to process, clean, and visualize the resulting large-scale detector signals.

## Project Highlight: The Data Pipeline
While the data generation relies on specialized medical physics tools (Geant4/OpenGATE), the core of the project focuses on **Data Science and Statistical Analysis**:
- **Data Handling:** Parsing and processing complex simulation outputs.
- **Data Cleaning & Noise Reduction:** Applying statistical logic to filter out background noise and isolate valid detector signals.
- **Exploratory Data Analysis (EDA) & Visualization:** Evaluating detector efficiency, tracking energy loss, and creating comprehensive plots in Python.

## Repository Structure

- `gate10_sim.py` — The main simulation engine (geometry, source, actors, etc).
- `preconf/detector.py` — Configuration for detector geometry and hit collection.
- `analyze.ipynb` — **The Data Science Workflow:** Jupyter notebook containing the post-processing, statistical analysis, and visualization.
- `GateMaterials_v10.db` — Custom material database used by the simulation.
- `Szakdolgozat.pdf` — The original BSc thesis document (in Hungarian of course).

## Tech Stack & Requirements

- **Language:** Python 3.10+
- **Data Analysis & Viz:** `NumPy`, `SciPy`, `Jupyter`
- **Simulation Tools:** `OpenGATE for Python` (used classic Docker previously, but technology advanced even while I was working on it)
- **AI-Assisted Development:** Leveraged Gemini Pro 3.1 and GitHub Copilot for code optimization, debugging, and accelerating the data visualization pipeline.

*To install the standard data processing dependencies:*
```bash
pip install numpy scipy jupyter uproot
```
*(Note: OpenGATE installation depends on your platform. Follow the [official OpenGATE documentation](https://opengate-python.readthedocs.io/).)*

## Running the Simulation & Analysis

**1. Generate the Data**
From the repository root, run the main script to generate the `.root` output files (`Hits-*.root`, `PSA-*.root`):
```bash
python gate10_sim.py
```
*(Configuration parameters like phantom setup and beam energy can be modified at the top of `gate10_sim.py`)*

**2. Analyze the Results**
Open the Jupyter notebook to run the data cleaning and visualization pipeline on the generated outputs:
```bash
jupyter notebook analyze.ipynb
```
## License
This project is distributed under the terms of the MIT License. See the `LICENSE` file for details.
