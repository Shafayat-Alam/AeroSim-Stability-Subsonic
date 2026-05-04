# AeroSim-Stability-Subsonic

Subsonic aerodynamic modeling and passive stability analysis for small-scale launch vehicles. Leveraging NASA TM X-195 principles to quantify energy management ($L/D$) and control coupling through high-resolution OpenFOAM sweeps.

---

## 1. Project Overview
This study utilizes a **"Simulation-First"** methodology to develop a high-fidelity aerodynamic model for two distinct launch vehicle configurations in the subsonic, compressible regime. By leveraging **OpenFOAM v2412** for steady-state RANS simulations, we characterize the non-linear relationship between aerodynamic coefficients ($C_L, C_D, C_M$), Mach number ($M$), Angle of Attack ($\alpha$), and Sideslip Angle ($\beta$). This data is a mechanical necessity for reliable GNC (Guidance, Navigation, and Control) integration and the verification of passive stability.

---

## 2. Vehicle Configurations
The analysis covers two specific airframe designs with varying aerodynamic characteristics:

### 2.1 Mars Rover
*   **Nose Cone**: Elliptical profile.
*   **Stabilization**: Standard trapezoidal fins.
*   **Design Intent**: Characterization of a traditional high-power rocket geometry.

### Altitude
*   **Nose Cone**: Tangent Ogive profile.
*   **Stabilization**: Tube fins.
*   **Design Intent**: High-altitude performance testing (Targeting 800 ft apogee) utilizing unique drag and stability profiles provided by tubular lifting surfaces.

---

## 3. Technical Justification

### 3.1 Criticality of Drag Prediction
In small-scale rocketry, drag is the primary governor of mission success due to a high **drag area-to-mass ratio**.
*   **Energy Management**: Precise $C_D$ characterization is required to predict apogee; as demonstrated in NASA TM X-195, higher-than-predicted drag leads to rapid energy depletion.
*   **Trajectory Impact**: High drag necessitates steeper ascent profiles to exit the dense atmosphere quickly, increasing the total $\Delta V$ required.
*   **Configuration Timing**: Analysis confirms that the timing of configuration changes (e.g., recovery deployment) is critical to ensuring the vehicle reaches the recovery zone.

---

## 4. Computational Methodology

### 4.1 Numerical Setup & HPC Workflow
*   **HPC Implementation**: All meshing and solving is computed in parallel using **16 cores**.
*   **Automation**: Orchestrated by automated **Python**, **Bash**, and **SLURM** scripts to handle batch processing of sweeps.
*   **Solver**: Steady-state, pressure-based compressible solver (`rhoSimpleFoam`).
*   **Turbulence Model**: **Spalart-Allmaras (S-A)**. Selected for computational efficiency and established accuracy in aerospace applications.

### 4.2 Unified 3D Sweep Approach
To maximize efficiency, Mach, $\alpha$, and $\beta$ sweeps are integrated into a single workflow. We modify inlet velocity vectors rather than rotating the geometry to maintain mesh integrity.

**Vector Implementation:**
* $$U_x = |U| \cos(\alpha) \cos(\beta)$$
* $$U_y = |U| \sin(\beta)$$
* $$U_z = |U| \sin(\alpha) \cos(\beta)$$

---

## 5. Configuration-Specific Parameters

### 5.1 Environmental Anchors & Thermophysics (ISA Model)
| Parameter | Mars Rover (1000 ft) | Altitude (410 ft) |
| :--- | :--- | :--- |
| **Atmospheric Pressure ($P$)** | 97,737 Pa | 99,878 Pa |
| **Atmospheric Temperature ($T$)** | 286.17 K | 287.36 K |
| **Speed of Sound ($a$)** | ~339.12 m/s | ~339.82 m/s |
| **Velocity ($U$) @ Mach 0.7** | **237.4 m/s** | **237.9 m/s** |
| **Transport Model** | Sutherland | Sutherland |

### 5.2 Geometry & Control Settings
| Setting | Mars Rover 2 | Blue Phenix Jr |
| :--- | :--- | :--- |
| **Patch Naming** | `Mars` | `Alt` |
| **Reference Area ($A_{ref}$)** | $0.01865 \, \text{m}^2$ | $0.00138 \, \text{m}^2$ |
| **Reference Length ($L_{ref}$)** | $2.009 \, \text{m}$ | $1.066 \, \text{m}$ |
| **Center of Rotation (CG)** | (1.151, 0, 0) | (0.544, 0, 0) |

---

## 6. Boundary Conditions
Boundary conditions utilize mathematical wall functions to ensure accuracy across the 3D domain.

| Symbol | OpenFOAM Field | Mars Rover (1000 ft) | Altitude (410 ft) |
| :--- | :--- | :--- | :--- |
| $\mathbf{U}$ | Velocity | `magU 237.4` | `magU 237.9` |
| $P$ | Pressure | `97737` | `99878` |
| $T$ | Temperature | `286.17` | `287.36` |
| $\tilde{\nu}$ | Modified Turb. Visc. | `4.7e-05` | `4.7e-05` |
| $\nu_t$ | Turb. Kin. Visc. | `1.565e-06` | `1.565e-06` |

---

## 7. Meshing Methodology
Meshing is performed using `blockMesh` and `snappyHexMesh`.

*   **Domain**: 19.43m (X) x 9.92m (Y) x 9.92m (Z).
*   **Base Grid**: 210 x 120 x 110 cells.
*   **Refinement**: Level 7 feature refinement and wake refinement ((0.05 6) (0.2 5) (0.5 4)).

---

## 8. Sampling Strategy
The simulation captures non-linear coupling effects between axial and lateral flow components using a spherical sweep.

| Parameter | Range | Delta ($\Delta$) | Justification |
| :--- | :--- | :--- | :--- |
| **Mach Number ($M$)** | $0.1 - 0.7$ | $0.1$ | Subsonic compressibility. |
| **Angle of Attack ($\alpha$)** | $0^{\circ} - 10^{\circ}$ | $2.0^{\circ}$ | Pitch-plane stability. |
| **Sideslip Angle ($\beta$)** | $0^{\circ} - 10^{\circ}$ | $2.0^{\circ}$ | Yaw-plane & crosswind coupling. |

---

## 9. References
*   **Finch & Matranga (1959).** *NASA TM X-195: Launch Characteristics of the X-15.*
*   **Negandhi, R. (2025).** *Aerodynamic Modeling for Thrust Vector Control.*
*   **Stern, F. (1999).** *Verification and Validation of CFD Simulations.*
*   **ICAO (1993).** *Manual of the ICAO Standard Atmosphere.*
