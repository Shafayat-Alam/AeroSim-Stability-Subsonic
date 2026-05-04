# AeroSim-Stability-Subsonic

Subsonic aerodynamic modeling and passive stability analysis for small-scale launch vehicles. Leveraging NASA TM X-195 principles to quantify energy management ($L/D$) and control coupling through high-resolution OpenFOAM sweeps.



## 1. Project Overview

This study utilizes a **"Simulation-First"** methodology to develop a high-fidelity aerodynamic model for two distinct launch vehicle configurations in the subsonic, compressible regime. By leveraging **OpenFOAM v2412** for steady-state RANS simulations, we characterize the non-linear relationship between aerodynamic coefficients ($C_L, C_D, C_M$), Mach number ($M$), Angle of Attack ($\alpha$), and Sideslip Angle ($\beta$). This data is a mechanical necessity for reliable GNC (Guidance, Navigation, and Control) integration and the verification of passive stability.



---



## 2. Vehicle Configurations

The analysis covers two specific airframe designs with varying aerodynamic characteristics:



### 2.1 Mars Rover Rocket

*   **Nose Cone**: Elliptical profile.

*   **Stabilization**: Standard trapezoidal fins.

*   **Design Intent**: Characterization of a traditional high-power rocket geometry.



### 2.2 Altitude Rocket

*   **Nose Cone**: Tangent Ogive profile.

*   **Stabilization**: Tube fins.

*   **Design Intent**: High-altitude performance testing (Targeting 800 ft apogee) utilizing unique drag and stability profiles provided by tubular lifting surfaces.



---



## 3. Technical Justification



### 3.1 Criticality of Drag Prediction

In small-scale and hobby rocketry, drag is the primary governor of mission success due to a high **drag area-to-mass ratio**.

*   **Energy Management**: Precise $C_D$ characterization is required to predict apogee and coast-phase performance; as demonstrated in the X-15 flight tests, higher-than-predicted drag leads to rapid energy depletion.

*   **Trajectory Impact**: High drag necessitates steeper ascent profiles to exit the dense atmosphere quickly, which directly increases the total velocity ($\Delta V$) required to achieve mission objectives.

*   **Configuration Timing**: Analysis of high-drag vehicles confirms that the timing of configuration changes (such as deploying recovery gear) is critical; premature deployment can result in the vehicle falling short of the intended recovery zone.



---



## 4. Computational Methodology



### 4.1 Numerical Setup & HPC Workflow

*   **HPC Implementation**: All meshing and solving is computed in parallel on a supercomputer using **16 cores**.

*   **Automation**: Orchestrated by automated **Python**, **Bash**, and **SLURM** scripts to handle batch processing of sweeps.

*   **Solver**: Steady-state, pressure-based compressible solver (`rhoSimpleFoam`) to account for local density variations.

*   **Turbulence Model**: **Spalart-Allmaras (S-A)**. Selected for computational efficiency and established accuracy in aerospace applications involving adverse pressure gradients.



### 4.2 Unified 3D Sweep Approach (Mach, AoA, & Sideslip)

To maximize computational efficiency and ensure mesh preservation, the Mach number, Angle of Attack ($\alpha$), and Sideslip ($\beta$) sweeps are integrated into a single workflow.



*   **3D Sweep (Vector Direction)**: Sweeps are performed by modifying the inlet velocity direction vectors rather than physically rotating the vehicle geometry. This accounts for both vertical (pitch) and lateral (yaw) flow deviations.

*   **Vector Implementation**: 3D flow orientation is achieved via trigonometric decomposition in the `U` field:

    *   $U_x = \|U\| \cos(\alpha) \cos(\beta)$

    *   $U_y = \|U\| \sin(\beta)$

    *   $U_z = \|U\| \sin(\alpha) \cos(\beta)$



---



## 5. Configuration-Specific Parameters



### 5.1 Environmental Anchors & Thermophysics

Environmental values represent mid-flight baseline altitudes derived from the **International Standard Atmosphere (ISA)** model.



| Parameter | Mars Rover (1000 ft ISA) | Altitude (410 ft ISA) |

| :--- | :--- | :--- |

| **Atmospheric Pressure ($P$)** | 97,737 Pa | 99,878 Pa |

| **Atmospheric Temperature ($T$)** | 286.17 K | 287.36 K |

| **Speed of Sound ($a$)** | ~339.12 m/s | ~339.82 m/s |

| **Velocity ($magU$) @ Mach 0.7** | **237.4 m/s** | **237.9 m/s** |

| **Mol. Weight ($MW$)** | 28.96 g/mol | 28.96 g/mol |

| **Specific Heat ($C_p$)** | 1005 J/kg·K | 1005 J/kg·K |

| **Transport Model** | Sutherland ($A_s$: 1.458e-06, $T_s$: 110.4) | Sutherland ($A_s$: 1.458e-06, $T_s$: 110.4) |



### 5.2 Geometry & Control Settings

| Setting | Mars Rover | Altitude |

| :--- | :--- | :--- |

| **Patch Naming** | `Mars` | `Alt` |

| **Reference Area ($A_{ref}$)** | $0.01865 \, \text{m}^2$ | $0.00138 \, \text{m}^2$ |

| **Reference Length ($L_{ref}$)** | $2.009 \, \text{m}$ | $1.066 \, \text{m}$ |

| **Center of Rotation (CG)** | (1.151, 0, 0) | (0.544, 0, 0) |



---



## 8. Sampling Strategy & Results

The simulation utilizes a 3D grid sweep methodology to capture non-linear coupling effects between axial, lateral (yaw), and vertical (pitch) flow components.



| Parameter | Range | Delta ($\Delta$) | Justification |

| :--- | :--- | :--- | :--- |

| **Mach Number ($M$)** | $0.1 - 0.7$ | $0.1$ | Subsonic compressibility effects. |

| **Angle of Attack ($\alpha$)** | $0^{\circ} - 10^{\circ}$ | $2.0^{\circ}$ | Pitch-plane stability characterization. |

| **Sideslip Angle ($\beta$)** | $0^{\circ} - 10^{\circ}$ | $2.0^{\circ}$ | Yaw-plane stability & crosswind coupling. |

---



## 6. Boundary Conditions (Numerical Details)

Boundary conditions utilize mathematical wall functions to ensure boundary layer accuracy across the 3D domain.



| Math Symbol | OpenFOAM Field | Mars Rover (1000 ft) | Altitude (410 ft) |

| :--- | :--- | :--- | :--- |

| $\mathbf{U}$ | Velocity | `magU 237.4` | `magU 237.9` |

| $P$ | Pressure | `internal 97737` | `internal 99878` |

| $T$ | Temperature | `internal 286.17` | `internal 287.36` |

| $\tilde{\nu}$ | Modified Turb. Visc. | `internal 4.7e-05` | `internal 4.7e-05` |

| $\nu_t$ | Turb. Kin. Visc. | `internal 1.565e-06` | `internal 1.565e-06` |

| $\alpha_t$ | Turb. Thermal Diff. | `internal 1.841e-06` | `internal 1.841e-06` |



---



## 7. Meshing Methodology

Meshing is performed with `blockMesh`, `surfaceFeatureExtract`, and `snappyHexMesh`.



### 7.1 Domain and Base Mesh

*   **Dimensions**: 19.4322m (X) x 9.9168m (Y) x 9.9168m (Z).

*   **Base Grid**: 210 x 120 x 110 cells.



### 7.2 Configuration-Specific Mesh Controls

*   **Extraction**: Included angle of 150° for both `mars.stl` and `alt.stl`.



| Control Feature | Feature Value |

| :--- | :--- |

| **Refinement Surface** | Level (6 7) |

| **Feature Level** | Level 7 |

| **Wake Refinement** | ((0.05 6) (0.2 5) (0.5 4)) |

| **minVol** | $1 \times 10^{-18}$ |

| **nSolveIter (Snap)** | 100 |

| **nSmoothScale** | 20 |



---



## 8. Sampling Strategy & Results

The simulation sweep captures non-linear coupling effects between axial and lateral flow components.



| Parameter | Range | Delta ($\Delta$) | Justification |

| :--- | :--- | :--- | :--- |

| **Mach Number ($M$)** | $0.1 - 0.7$ | $0.1$ | Subsonic compressibility effects. |

| **Angle of Attack ($\alpha$)** | $0^{\circ} - 10^{\circ}$ | **$2.0^{\circ}$** | Pitch-plane stability characterization. |

| **Sideslip Angle ($\beta$)** | **$0^{\circ} - 10^{\circ}$** | **$2.0^{\circ}$** | Yaw-plane stability & crosswind coupling. |



---



## 9. References

*   **Finch, T. W., & Matranga, G. J. (1959).** *NASA TM X-195: Launch, Low-Speed, and Landing Characteristics of the X-15.*

*   **Negandhi, R., et al. (2025).** *Aerodynamic Modeling for Thrust Vector Control Rocketry.*

*   **Stern, F., et al. (1999).** *IIHR Report No. 407: Verification and Validation of CFD Simulations.*

*   **International Civil Aviation Organization (ICAO). (1993).** *Manual of the ICAO Standard Atmosphere.*

