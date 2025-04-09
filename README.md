# Fuzzy Logic Sprinkler Control System

An intelligent irrigation system using fuzzy logic principles to optimize water usage based on soil moisture and temperature conditions.

## Overview

This system implements a fuzzy logic controller that manages water sprinkling intensity by:
- Monitoring soil moisture (0-100%)
- Reading temperature (0-50°C)
- Calculating optimal sprinkling levels
- Applying fuzzy logic rules for decision making

## Requirements

- Python 3.x
- Core dependencies:
  ```bash
  numpy
  scikit-fuzzy
  matplotlib
  ```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv fuzzy
   source fuzzy/bin/activate  # On Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install numpy scikit-fuzzy matplotlib
   ```

## System Components

1. Input Variables:
   - Soil Moisture (dry, moist, wet)
   - Temperature (cold, warm, hot)

2. Output:
   - Water Sprinkling Level (low, medium, high)

3. Fuzzy Rules:
   - 5 rules handling different environmental conditions
   - Adaptive response based on input combinations

## Usage

Run the core system:
```bash
python fuzzy.py
```

## Contributors

- WAINAINA, NIXON MBURU – 665507
- WILLIAM MUNGAI – 666494
- BRACKCIDIS TEMKO – 666989
- LEE KAMAU – 666591
- STEPHEN KAHANYA – 668435
