CS2 Trade-Up Algorithm (Mathematical Breakdown)

This document details the complete algorithm for calculating the outcomes, probabilities, and expected value (EV) of a CS2 trade-up contract.

1. Definitions & Database Requirements

Before calculating, you must have a master skins.json database. The algorithm relies on looking up data from this file.

A. Inputs

$I$: The set of $n$ input skins, $I = \{i_1, i_2, ... i_n\}$.

$n$: The number of input skins. Must be 10 (legacy) or 5 (for Covert-to-Extraordinary).

$f_j$: The specific float value of the $j$-th input skin $i_j$.

$is\_stattrak$: A boolean (true/false) for whether the inputs are StatTrak™.

B. Database Properties (for each skin $s$)

Your skins.json file must be queryable for these properties for any skin:

s.name: (e.g., "AK-47 | Redline")

s.rarity: (e.g., "Classified")

s.collection: (e.g., "The Winter Offensive Collection")

s.float_min: The skin's minimum possible float (e.g., 0.10).

s.float_max: The skin's maximum possible float (e.g., 0.70).

s.price(condition): A function or lookup to get the market price for the skin at a specific condition (e.g., "Field-Tested").

s.has_stattrak: A boolean (true/false).

C. The GetOutcomes Function

This is a database lookup function you must create. It is not a mathematical formula.

GetOutcomes(collection, input_rarity, is_stattrak): Returns a list of all possible output skins from a given collection.

Example (Standard): GetOutcomes("Spectrum 2", "Mil-Spec", true)

Looks for all "Restricted" (next rarity up) skins from the "Spectrum 2" collection that have a StatTrak™ version.

Returns: ["ST AK-47 | The Empress", "ST P250 | See Ya Later", "ST M4A1-S | Leaded Glass"]

Example (Covert-to-Extraordinary): GetOutcomes("Fracture Collection", "Covert", false)

Identifies the "Fracture Case".

Finds all "Extraordinary" (rare) drops from that case (e.g., Skeleton, Nomad knives).

Returns the list of all non-StatTrak™ knife finishes available from that case.

2. Step 1: Input Validation & Metrics

Validate Contract:

Confirm all $n$ input skins $i_j \in I$ have the same rarity, $R_{\text{in}}$.

Confirm all $n$ input skins are either all StatTrak™ or all non-StatTrak™.

Confirm $n=10$ (if $R_{\text{in}} \neq$ "Covert") or $n=5$ (if $R_{\text{in}} = $ "Covert").

If any check fails, the contract is invalid.

Calculate Total Input Cost ($C_{\text{in}}$):
The total cost is the sum of the market price of each input skin.


$$C_{\text{in}} = \sum_{j=1}^{n} i_j\text{.price(GetCondition}(f_j))$$


(Where GetCondition(f) is a helper function that converts a float to a wear name, e.g., 0.25 -> "Field-Tested")

Calculate Average Input Float ($F_{\text{avg}}$):
The simple arithmetic mean of all input floats.


$$F_{\text{avg}} = \frac{1}{n} \sum_{j=1}^{n} f_j$$

3. Step 2: Outcome Probability Calculation

This is the most critical part of the algorithm.

Identify Unique Collections:

Create a set $C$ of all unique collections present in the input skins $I$.

Example: If you use 7 "Fracture" skins and 3 "D&N" skins, $C = \{\text{"Fracture Collection", "Dreams & Nightmares Collection"}\}$.

Count Inputs & Outcomes per Collection:

Create a map (dictionary) to store counts.

For each unique collection $c_k \in C$:

$N_{c_k}$ (Input Count): Count how many of your input skins are from collection $c_k$.

Example: $N_{\text{Fracture}} = 7$, $N_{\text{D&N}} = 3$

$O_{c_k}$ (Outcome Set): Get the list of possible outcomes:

$O_{c_k} = \text{GetOutcomes}(c_k, R_{\text{in}}, is\_stattrak)$

$|O_{c_k}|$ (Outcome Count): Count the number of skins in that list.

Example: $O_{\text{Fracture}}$ (Coverts) has 2 skins, so $|O_{\text{Fracture}}| = 2$. $O_{\text{D&N}}$ (Coverts) has 2 skins, so $|O_{\text{D&N}}| = 2$.

Calculate Total Probability Weight ($W_{\text{total}}$):
The "total weight" is the sum of (inputs from collection $\times$ outcomes from collection) for all unique collections.


$$W_{\text{EXAMPLE}} = (N_{\text{Fracture}} \times |O_{\text{Fracture}}|) + (N_{\text{D&N}} \times |O_{\text{D&N}}|)$$

$$W_{\text{EXAMPLE}} = (7 \times 2) + (3 \times 2) = 14 + 6 = 20$$

Formula: $W_{\text{total}} = \sum_{c_k \in C} (N_{c_k} \times |O_{c_k}|)$

Calculate Probability per Outcome ($P_s$):
For every possible outcome skin $s$:

First, find the probability of hitting its collection $c_s$.


$$P(\text{collection } c_s) = \frac{N_{c_s} \times |O_{c_s}|}{W_{\text{total}}}$$

This probability is divided equally among all skins in that collection's outcome set.

Therefore, the probability of hitting the specific skin $s$ is:


$$P_s = \frac{P(\text{collection } c_s)}{|O_{c_s}|} = \frac{N_{c_s}}{W_{\text{total}}}$$

Example (using $W_{\text{total}} = 20$):

Prob of hitting AK-47 | Legion of Anubis (from Fracture, $N=7$): $P_s = \frac{7}{20} = 35\%$

Prob of hitting MP9 | Starlight (from D&N, $N=3$): $P_s = \frac{3}{20} = 15\%$

4. Step 3: Output Float & Value Calculation

Get Full Outcome Set ($O_{\text{all}}$):

This is the set of all possible outcome skins from all collections.

$O_{\text{all}} = \bigcup_{c_k \in C} O_{c_k}$

Calculate Value for Each Outcome:

For each skin $s \in O_{\text{all}}$:

Calculate Output Float ($F_s$): This is the deterministic float the output skin will have.


$$F_s = (F_{\text{avg}} \times (s\text{.float}_{\text{max}} - s\text{.float}_{\text{min}})) + s\text{.float}_{\text{min}}$$

Determine Output Condition:

$\text{Condition}_s = \text{GetCondition}(F_s)$

Find Output Value ($V_s$):

$V_s = s\text{.price}(\text{Condition}_s)$

5. Step 4: EV & Risk Analysis

Calculate Expected Value ($EV$):
The EV is the sum of (Value $\times$ Probability) for every possible outcome.


$$EV = \sum_{s \in O_{\text{all}}} (V_s \times P_s)$$

Calculate EV Profitability:

Profit (absolute): $EV_{\text{profit}} = EV - C_{\text{in}}$

Profit (relative %): $EV_{\%} = \left( \frac{EV - C_{\text{in}}}{C_{\text{in}}} \right) \times 100\%$

Analyze Risk (Worst/Best Case):

Worst Outcome Value: $V_{\text{min}} = \min(V_s)$ for all $s \in O_{\text{all}}$

Best Outcome Value: $V_{\text{max}} = \max(V_s)$ for all $s \in O_{\text{all}}$

"No-Risk" Check: The trade-up is "no-risk" if $V_{\text{min}} > C_{\text{in}}$.

Calculate Odds to Profit:

Sum the probabilities of all outcomes whose value is greater than the input cost.

$\text{OddsToProfit} = \sum P_s$ for all $s$ where $V_s > C_{\text{in}}$