# proton-tomography-bscthesis

BSc thesis project focused on proton tomography simulation and detector-signal analysis for medical physics research.

## Overview

This repository contains:
- a Geant4/OpenGATE simulation setup for proton-beam transport through a water phantom and layered detector geometry,
- detector and phase-space output generation for multiple particle types,
- a Jupyter notebook for post-processing and analysis.

## Repository structure

- `gate10_sim.py` — main simulation script (geometry, source, actors, outputs).
- `preconf/detector.py` — detector geometry and hit collection configuration.
- `analyze.ipynb` — analysis and visualization workflow.
- `GateMaterials_v10.db` — custom material database used by the simulation.
- `Szakdolgozat.pdf` — thesis document.

## Requirements

- Python 3.10+
- [OpenGATE for Python](https://opengate-python.readthedocs.io/)
- NumPy
- SciPy
- Jupyter (for notebook analysis)

Install dependencies in your preferred environment, for example:

```bash
pip install numpy scipy jupyter
```

> OpenGATE installation depends on your platform and Geant4 setup. Follow the official OpenGATE documentation for installation instructions.

## Running the simulation

From the repository root:

```bash
python gate10_sim.py
```

The main configuration parameters are defined near the top of `gate10_sim.py`, including:
- phantom setup (`PHANTOM`, `WATER_PHANTOM_THICKNESS`, rotation),
- detector rotation (`DETECTOR_ROTATION_ANGLE`),
- number of primaries (`PRIMARY_NUMBER`),
- beam particle/energy selection (`particle`, `energy`).

## Outputs

Running the simulation creates ROOT files (prefixes shown below, with particle suffixes):
- `Hits-*.root`
- `PSA-*.root`
- `Hits-track-*.root`
- `Hits-calor-*.root`

These files can be used for downstream detector-signal analysis and visualization.

## Analysis

Open the notebook to analyze generated simulation outputs:

```bash
jupyter notebook analyze.ipynb
```

## License

This project is distributed under the terms in the `LICENSE` file.
