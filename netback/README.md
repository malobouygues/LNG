# US LNG Netback & Destination Arbitrage (JKM vs. TTF)

This project models the decision-making process of a US Gulf Coast (USGC) LNG exporter. It calculates the Netback to the loading flange to determine the optimal destination for a cargo: Asia (JKM) or Europe (TTF).

**Objective:** To answer the daily logistical question: Given current charter rates and boil-off losses, is the premium in Asia sufficient to cover the extra 15 days of voyage compared to Europe?

## 1. Context & Rationale

Since the US became a major LNG exporter, it acts as the "Swing Supplier" between the Atlantic and Pacific basins. Unlike oil, LNG cannot be easily stored; it must be kept moving.

**The Problem** Retail analysis often looks at the simple spread: JKM Price - TTF Price. If positive, they assume flows go to Asia.

**The Pivot** I realized that a positive spread is meaningless without factoring in the Cost of Voyage.

**Rationale:** A $2.00/MMBtu premium in Asia can be completely eroded by high charter rates or the "Boil-off" (natural evaporation of gas) during the longer journey.

**The Metric:** The Netback. It works backwards from the destination price, subtracting all logistical costs to find the value of the gas at the moment of loading.

## 2. Adapting the Code to Market Realities (Logistics & Physics)

The logic of this tool integrates the specific constraints of the cryogenic supply chain.

### A. The Tycoon of Costs: Freight & Charter Rates

My initial model treated shipping as a fixed cost. In reality, Spot Charter Rates are the most volatile component of the arb (ranging historically from $30k/day to >$300k/day in winter).

The Baltic Exchange

Basé à Londres, c'est l'indice sur lequel se règlent les contrats financiers.

Benchmark: The Baltic Exchange route definitions.

US to Europe: Based on BLNG2 (Sabine Pass → Isle of Grain).

US to Asia: Based on BLNG3 (Sabine Pass → Tokyo via Panama).

Vessel Class: 174,000 m³ (2-Stroke/MEGI). This model assumes modern, efficient tonnage rather than older TFDE/Steam vessels (160k), reflecting current fleet economics.

Data Proxy: CME Group LNG Freight Futures are used as the pricing reference for the simulation.

Indices clés pour toi :

BLNG2-174 : US Gulf to Continent (Europe/TTF).

https://www.cmegroup.com/markets/energy/freight/lng-freight-us-gulf-to-continent-blng2-174.html

BLNG3 : US Gulf to Japan (Asie/JKM).

https://www.cmegroup.com/markets/energy/freight/lng-freight-us-gulf-to-japan-blng3-174.html

**Implementation:** The code (netback_formulas.py) inputs a variable Charter Rate against specific voyage durations:

- **Europe (10 Days):** Fast rotation, lower exposure to freight volatility.

- **Asia (25 Days):** Assumes transit via Panama Canal.

**Market Reality:** If Panama is congested (forcing a route via Cape of Good Hope), travel days double, and the Asia Netback collapses. This model allows for stress-testing these duration assumptions.

### B. The Thermodynamics: "Boil-off" (Inventory Loss)

Unlike Grain or Oil, LNG evaporates. A ship arriving in Japan has less cargo than when it left Louisiana.

**The "Merchant" Logic:** I included a Boil-off calculation (0,15% daily loss).

?????!!!!!!! SOURCE ?????!!!!!!!

**Impact:** On a 25-day voyage to Asia, around 3,75% of the cargo value evaporates (or is used as fuel). On a standard 3,5 TBtu cargo, this represents a significant P&L erosion that simple spread analysis ignores.

### C. The Destination Decision (JKM vs. TTF)

The model compares two benchmark Netbacks:

- **JKM (Japan/Korea Marker):** The Asian price anchor.

Asia (JKM): Pricing based on S&P Global Platts JKM™ (Japan Korea Marker), the standard assessment for spot LNG deliveries in Northeast Asia.

Le JKM est un indice calculé par S&P Global Platts (une agence de reporting), mais les traders traitent le "Future" qui est listé sur le CME ou l'ICE. Le lien ci-dessous est celui du contrat Future le plus utilisé pour se couvrir.

Benchmark: S&P Global Platts JKM™ (Japan Korea Marker), the standard assessment for spot LNG deliveries in Northeast Asia.

Instrument: CME Group JKM (Platts) Futures.

Source : CME Group (Clearé contre l'indice Platts)

https://www.cmegroup.com/markets/energy/natural-gas/lng-japan-korea-marker-platts-swap.quotes.html

- **TTF (Title Transfer Facility):** The European price anchor.

Europe (TTF): Pricing based on ICE Endex Dutch TTF Gas Futures, the primary reference for continental European gas.

L'indice hollandais est principalement tradé sur ICE (Intercontinental Exchange). C'est le contrat le plus liquide en Europe.

Benchmark: ICE Endex Dutch TTF Gas Futures, the primary reference for continental European gas liquidity.

Instrument: ICE Endex TTF Futures (Front Month).

Source : ICE Endex

https://www.ice.com/products/27996665/Dutch-TTF-Natural-Gas-Futures

**The Signal:** Netback_Asia - Netback_Europe.

- **If Positive:** The "Call on Gas" is in Asia. Ships turn west through Panama.

- **If Negative:** The Arb is closed. US cargoes flood Europe (as seen in 2022/2023), acting as the balancer for European energy security.

## 3. Technical Implementation

This project is built to handle scenario analysis.

- **Architecture:** Modular design separating physical constants (config) from financial formulas.

- **Main Formula:**

  Netback = Destination_Price - [ (Charter_Rate * Days / Cargo_Size) + Boil_off_Loss + Regas_Fees ]

- **Visualization:** Plots the Netback differential over time to visualize the "Arb Window" opening and closing, independent of the absolute price of gas.

(Note: The current version uses synthetic market data to demonstrate the logic, designed to be plugged into a Platts/Bloomberg API).
