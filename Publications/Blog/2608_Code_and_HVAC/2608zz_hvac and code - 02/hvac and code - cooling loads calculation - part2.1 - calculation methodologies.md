#Engineering #HVAC #CoolingLoads #Engineering #Automation #SolarGain #BuildingScience #EnergyEfficiency

Autor: "Donchenko Michail",  date: 2026-04-23,
___ 
In HVAC projects, calculating cooling loads is a complex but crucial task. Accurate calculations help design efficient cooling systems that maintain comfort while minimizing energy consumption.

-----
## Method

Based on the method from Manual [1], we will describe the calculation structure.

The heat gain Q, W, in premises from solar radiation is determined by the formula:
$$
Q = \sum\limits_{i=1}^a Q_i + \sum\limits_{i=1}^b Q_im \tag{1}
$$
- Q_i  -  heat flux through the i-th light opening, W;
- Q_im - heat flux through the i-th massive enclosure, W;
- a - number of light openings;
- b - number of massive enclosures.

_In this work, we will consider only the first part of this formula — heat gains from the heat flux through light openings (windows, façade systems, etc.). The calculation supplement accounting for heat gains through massive enclosures (walls, roof) will be performed in a separate work._

The heat flux of direct and diffuse solar radiation (hereinafter referred to as “solar radiation”) through the i-th glazed light opening (hereinafter referred to as a “light opening”), W, should be determined by the formula:
$$
Q_{sun} = Q_{sun,i} \cdot a_d + Q_{\delta t} \tag{2}
$$
- $Q_{sun}$ - heat flux, W, of solar radiation through a glazed light opening;
-  a_d - absorption factor of the solar radiation heat flux;
- $Q_{\delta t}$ - heat transfer flux through the light opening

The heat flux, W, of solar radiation through a light opening is calculated by the formula:
$$
Q_{sun, i} = (q_d \cdot K_1 + q_nd \cdot K_2) \cdot K3 \cdot K4 \cdot A_{gl} \tag{3}
$$
- $q_d, q_nd$ - surface density of the heat flux, W/m², through a glazed light opening in July at a given hour of the day, from direct (qd​) and diffuse (qnd​) solar radiation, respectively;
- K1​ — insolation coefficients for direct solar radiation to account for the area of the light opening;
- K2​ — insolation coefficients to account for diffuse solar radiation entering through light openings;
- K3​ — heat transmission coefficients of solar protection devices;
- K4​ — heat transmission coefficient of glazing for light openings;
- Agl​ — area of the light opening (glazing), m².

13. The heat transfer flux, W, for a given hour of the day through a glazed light opening (glazing) is calculated by the formula:
$$
Q_{\delta t} = (t_{out-day-mid} + 0.5 \cdot A_{air-day} \cdot \theta - t_{in}) \cdot (F_{m^2} / R) \tag{18}
$$
- $t_{out-day-mid}$ -  average daily outdoor air temperature, $^\circ$C;
- $A_{air-day}$ -  maximum daily amplitude of outdoor air temperature in July,$^\circ$C;
- $\theta$ - coefficient expressing the harmonic variation of outdoor air temperature;
- $t_{in}$ -  indoor air temperature, $^\circ$C;
- F, R - area, m²;
- R -  reduced thermal resistance of glazing for the light opening, $m^2С/W$.

---
## Calculation pipeline

Draw this method as a graph for defining necessary input parameters and visualizing calculation pipeline
<img src="Cooling_load_en.png" width="800" alt="Cooling_load_en">
Pic. 1. General Cooling load graph  

---
<img src="Q_rad_devour+Q_conduction_en.png" width="800" alt="Cooling_load_en">
Pic. 2. Specified Cooling load graph  

---
## Object model

Draw real world object model witch will be used for contain parameters for calculation and results of calculations. 
This approach simplifies understanding the calculations by mapping them to real‑world concepts.

<img src="Building_tree.png" width="800" alt="Building_tree_en">
Pic. 3. Building objects tree  

Each class holds data of its associated subclasses. "Room" contains all "Window" inside it, "Apartment" contains all "Rooms" and "Windows in this Rooms" etc.

Of course, there’s no need to recalculate everything for each `Window` or `Room` instance; we can reuse the calculations for similar objects instead.

<img src="Building_tree_lists.png" width="800" alt="Building_tree__lists_en">
Pic. 4. Building objects tree with links

Finally, create abstract objects in the form of Python classes to encapsulate the main input data. 
 
```python
from dataclasses import dataclass, field
from typing import Literal

import pandas as pd

Orientation = Literal["nw", "n", "ne", "e", "se", "s", "sw", "w"]

@dataclass
class Window:
    area_sqm: float
    orientation: Orientation
    cooling_load: pd.DataFrame | None = None
    R_value_m2K_W: float = 1.45
    K1: float = 0.9
    K2: float = 1.0
    K3: float = 1.0
    K4_SF_solar_factor: float = 0.34

@dataclass
class Location:
    city_name: str = "Москва"
    latitude: int = 56
    t_out_day_mid: float = 23
    A_air_day: float = 24

@dataclass
class Room:
    number: str
    name: str
    windows: list[Window]
    cooling_load: pd.DataFrame | None = None
    required_air_temperature_C: float = 24
    people_heat_kW: float = 0
    appliances_heat_kW: float = 0
    air_flow_m3_h: float = 0

@dataclass
class Apartment:
    number: str
    rooms: list[Room]
    cooling_load: pd.DataFrame | None = None

@dataclass
class Level:
    number: str
    elevation_m: float
    apartment: list[Apartment]
    cooling_load: pd.DataFrame | None = None

@dataclass
class Building:
    number: str
    name: str
    levels: list[Level]
    location: Location
    cooling_load: pd.DataFrame | None = None

```

## Calculation model

Union this method and object model to implement structure of calculation input parameters and response.

<img src="Input-output-building.png" width="1200" alt="Input-output-building">
Pic. 5. Calculation input and response (there is fragment of data)

In this example, we will calculate a general building with a number of restrictions, such as identical windows, no schedule for occupancy, and no electrical appliances, as we are currently defining a conceptual model.

This table info easy to present as plot 

<img src="graph-building.png" width="800" alt="graph-building">
Pic. 6. Calculation result as plot 



--- 
### **Practical Example: Small House Calculation**
Let’s consider a small house with the following parameters:
- **Window size:** 3 m2 per window.
- **Windows by orientation:**
    - South wall: 20 windows.
    - North wall: 20 windows.
    - West wall: 10 windows.
    - East wall: 10 windows.
- **Location:** latitude 56∘.
- **Occupancy:** 20 people.
- **Ventilation:** 20 people×60 m3/h=1200 m3/h of outdoor air.

Here are the key input parameters defined in Python:
```python
t_out_day_mid = 23 # Average outdoor air temperature by day
A_air_day = 24     # Amplitude outdoor air temperature by day

R_value = 1.45  # R-value of glass
K1 = 0.9        # default value for direct solar radiation intensity (glass is vertical)
K2 = 1          # default value for non direct solar radiation intensity (glass is vertical)
K3 = 0.4        # sun protection devices
K4 = 0.34/0.87  # solar factor for glass manufactory defined

# Glassing by directions
glassing = {
    'w' : 3*10,
    'e' : 3*10,
    'n' : 3*20,
    's' : 3*20,
}
  
Q_people_kW = {'occupancy' : 20}
Q_appliances_kW = {'equipment_load' : 10}   
L_m3_h = 20*60                               # Outdoor air for ventilation
```

We pass these parameters to the calculation function:
```python
calculation = Solar_radiation_cooling_load()

calculation.calculate(
    A_m2_w = glassing['w'],
    A_m2_e = glassing['e'],
    A_m2_n = glassing['n'],
    A_m2_s = glassing['s'],
    Q_people_kW = Q_people_kW['occupancy'],
    Q_appliances_kW = Q_appliances_kW['equipment_load'],
    L_m3_h = L_m3_h,
    t_out_day_mid = t_out_day_mid,
    A_air_day = A_air_day,
    R = R_value,
    K1 = K1,    
    K2 = K2,    
    K3 = K3,    
    K4 = K4,
)
```

---
### **Results**
The calculation results are presented in the table below:

| hour | w_Q_sun_kW | e_Q_sun_kW | n_Q_sun_kW | s_Q_sun_kW | Q_people_kW | Rad_kW | Q_conduction_kW | Q_heating_air_kW | Q_sum_kW |
|------|------------|------------|------------|------------|-------------|--------|-----------------|------------------|----------|
| 01   | 0.000      | 0.000      | 0.000      | 0.000      | 2.0         | 0.000  | -1.420          | -4.0             | -0.420   |
| 02   | 0.000      | 0.000      | 0.000      | 0.000      | 2.0         | 0.000  | -1.569          | -4.0             | -0.569   |
| 03   | 0.000      | 0.000      | 0.000      | 0.000      | 2.0         | 0.000  | -1.614          | -4.0             | -0.614   |
| 04   | 0.006      | 0.090      | 0.074      | 0.010      | 2.0         | 0.180  | -1.569          | -4.0             | -0.389   |
| 05   | 0.014      | 0.326      | 0.209      | 0.030      | 2.0         | 0.579  | -1.420          | -4.0             | 0.159    |
| 06   | 0.020      | 0.714      | 0.198      | 0.044      | 2.0         | 0.976  | -1.182          | -3.0             | 1.794    |
| 07   | 0.020      | 1.095      | 0.232      | 0.070      | 2.0         | 1.417  | -0.869          | -2.0             | 3.548    |
| 08   | 0.023      | 1.225      | 0.268      | 0.282      | 2.0         | 1.798  | -0.511          | -1.0             | 5.287    |
| 09   | 0.021      | 1.011      | 0.272      | 0.752      | 2.0         | 2.056  | -0.124          | 0.0              | 6.932    |
| 10   | 0.022      | 0.574      | 0.262      | 1.438      | 2.0         | 2.296  | 0.263           | 2.0              | 9.559    |
| 11   | 0.037      | 0.197      | 0.217      | 1.943      | 2.0         | 2.394  | 0.621           | 3.0              | 11.015   |
| 12   | 0.122      | 0.088      | 0.155      | 2.112      | 2.0         | 2.477  | 0.934           | 4.0              | 12.411   |
| 13   | 0.445      | 0.060      | 0.118      | 1.854      | 2.0         | 2.477  | 1.172           | 4.0              | 12.649   |
| 14   | 0.930      | 0.050      | 0.103      | 1.215      | 2.0         | 2.298  | 1.321           | 5.0              | 13.619   |
| 15   | 1.331      | 0.044      | 0.099      | 0.563      | 2.0         | 2.037  | 1.366           | 5.0              | 13.403   |
| 16   | 1.412      | 0.034      | 0.092      | 0.194      | 2.0         | 1.732  | 1.321           | 5.0              | 13.053   |
| 17   | 1.154      | 0.028      | 0.104      | 0.103      | 2.0         | 1.389  | 1.172           | 4.0              | 11.561   |
| 18   | 0.652      | 0.018      | 0.181      | 0.056      | 2.0         | 0.907  | 0.934           | 4.0              | 10.841   |
| 19   | 0.248      | 0.008      | 0.120      | 0.017      | 2.0         | 0.393  | 0.621           | 3.0              | 9.014    |
| 20   | 0.000      | 0.000      | 0.000      | 0.000      | 2.0         | 0.000  | 0.263           | 2.0              | 7.263    |
| 21   | 0.000      | 0.000      | 0.000      | 0.000      | 2.0         | 0.000  | -0.124          | 0.0              | 4.876    |
| 22   | 0.000      | 0.000      | 0.000      | 0.000      | 2.0         | 0.000  | -0.511          | -1.0             | 3.489    |
| 23   | 0.000      | 0.000      | 0.000      | 0.000      | 2.0         | 0.000  | -0.869          | -2.0             | 2.131    |
| 24   | 0.000      | 0.000      | 0.000      | 0.000      | 2.0         | 0.000  | -1.182          | -3.0             | 0.818    |

---
### **Visualizing the Results**
To better understand the data, we can present the results as graphs:
- **Pic. 1: Heat gain from solar radiation only.** This graph shows the contribution of solar heat gains by orientation (East, West, North, South) and the total solar heat gain.
- **Pic. 2: Total heat surplus (solar + internal sources).** This graph includes all heat sources: solar radiation, occupants, equipment, conduction, and ventilation.

<img src="cooling_load_example_0.png" width="800" alt="Описание изображения">

Pic. 1. Heat gain from solar radiation only

<img src="cooling_load_example_1.png" width="800" alt="Описание изображения">

Pic. 2. Total heat surplus from all sources

---
### **Analysis of the Results**
From the data, we can identify several important patterns:
- **Night hours (21:00–06:00):** Cooling loads are relatively low or even negative (heat loss), as there is no solar radiation and outdoor temperatures are lower.
- **Morning hours (06:00–11:00):** Rapid increase in cooling load due to rising outdoor temperatures and increasing solar radiation, especially on the east and south facades.
- **Peak hours (12:00–16:00):** Maximum cooling load occurs, reaching up to 13,6 kW at 14:00. This peak is driven by:
    - strong solar radiation on the south facade;
    - accumulated heat gain on the west facade;
    - high outdoor temperatures;
    - internal heat gains from occupants and equipment.
- **Evening hours (17:00–21:00):** Gradual decrease in cooling load as solar radiation diminishes and outdoor temperatures drop.
---
### **Practical Implications**
This example, while simplified, illustrates several key points for HVAC design:
- **Timing matters:** The peak cooling load doesn’t necessarily occur at the hottest time of day, but rather when solar radiation, internal gains, and outdoor temperatures combine.
- **Orientation is crucial:** Building orientation significantly affects heat gain distribution. Proper shading and glazing selection for different facades can reduce peak loads.
- **Automation helps:** Hourly calculations are essential for accuracy, and automating them saves significant time and reduces errors.

---
### **Scaling to Real‑World Projects**
In real‑world building design, the complexity increases dramatically:
- buildings are divided into **hydraulic zones**, **building cores**, and **individual risers**;
- cooling supply may come from multiple systems;
- different areas have varying occupancy schedules and equipment loads.
To correctly select:
- chiller plant equipment;
- pumping equipment for individual networks;
- pipeline diameters;
- control strategies,
engineers must perform similar calculations for:
- **individual zones** (e.g., office areas, server rooms, lobbies);
- **system components** (chillers, air handling units, fan coils);
- **the entire building complex** as a whole.
---
### **Conclusion**
While our simple example shows the basic principles, real HVAC design requires sophisticated tools that can handle the complexity of modern buildings. Automation isn’t just about saving time — it’s about creating more sustainable, comfortable, and cost‑effective environments.

By combining engineering best practices with modern software development, we can transform cooling load calculations from a tedious task into a powerful design tool.

### **Next Steps**
In upcoming posts, we’ll dive deeper into:
1. **Calculation methodologies:** detailed breakdown of heat gain formulas.
2. **Solar radiation modeling:** algorithms for direct and diffuse radiation.
3. **Software architecture:** how the system is built and scaled.
4. **Case studies:** real‑world examples of the tool in action.
5. **API documentation:** full guide for developers.

---
### **References:**
 1)  Manual 2.91 to the Construction Norms and Rules (SNiP) 2.04.05‑91 — Calculation of Heat Gains Due to Solar Radiation in Rooms, Moscow, 1993.