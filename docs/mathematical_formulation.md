# Mathematical Formulation
 
## Notation and Data
 
### Sets and Indices
 
$\hspace{0.5cm} P$ : Set of wells to be drilled, augmented with a dummy well numbered $0$.<br>
$\hspace{0.5cm} R$ : Set of drilling rigs, $R = \lbrace R_{1}, R_{2},..., R_{m} \rbrace$.<br>
$\hspace{0.5cm} i, j$ : Well indices, $i, j \in P$.<br>
$\hspace{0.5cm} k$ : Rig index, $k \in R$.<br>
$\hspace{0.5cm} n$ : Cardinality of the set of wells to be drilled, $n = \mid P \mid$.<br>
$\hspace{0.5cm} m$ : Cardinality of the set of rigs, $m = \mid R \mid$.<br>
 
### Parameters
 
+ $h_{i}$ : Drilling time for well $i$, $i \in P$.<br>
+ Rig travel time:<br>
$T = (T_{ij})$: represents the travel time of the drilling rig from well $i$ to well $j$ (expressed in days), with $i, j \in P$.<br>

## Mathematical Model
 
To better frame the problem, we embedded it within the class of vehicle routing problems.
 
### Decision Variables
 
These are binary variables indicating the route taken by each rig in use.<br>
We define:<br>
$$Y_{ijk} =
\begin{cases}
1 & \text{if well $j$ is drilled immediately after well $i$ by rig $k$} \\
0 & \text{otherwise, } i, j \in P \text{ and } k \in R
\end{cases}$$
 
### Objective Function
 
The total operating time of the $k^{\text{th}}$ rig, $k=1,...,m$, is given by:
$$t_{k} = \left( \sum_{i \in P} \sum_{j \in P} h_{i} Y_{ijk} \right) + \sum_{i \in P} \sum_{j \in P} T_{ij} \cdot Y_{ijk}$$
where $\sum_{i \in P} \sum_{j \in P} Y_{ijk}$ represents the number of wells drilled by rig $k$, $k \in R$.
 
The total project completion time corresponds to the duration required to drill all wells — which equals the finishing time of the last rig to complete its assignment:
$$\max_{k=1}^{m} \left\lbrace t_{k} \right\rbrace$$
The objective function is therefore:
$$\text{min } Z = \max_{k=1}^{m} \left\lbrace t_{k} \right\rbrace$$
 
### Constraints
 
+ Each rig departs from the dummy depot to drill exactly one first well (the choice of which well is left to the optimizer):
$$\sum_{j \in P, j \neq 0} Y_{0jk} = 1  \hspace*{0.8cm} \forall k \in R \hspace*{3cm}(1)$$
+ Each well must be drilled exactly once:
$$\sum_{k \in R} \sum_{j \in P} Y_{ijk} = 1  \hspace*{0.8cm} \forall i \in P , i \neq 0 \hspace*{2.5cm}(2)$$
$$\sum_{k \in R} \sum_{i \in P} Y_{ijk} = 1  \hspace*{0.8cm} \forall j \in P , j \neq 0 \hspace*{2.5cm}(3)$$
+ Each rig must return to the dummy well:
$$\sum_{i \in P, i \neq 0} Y_{i0k} = 1  \hspace*{0.8cm} \forall k \in R \hspace*{3cm}(4)$$
+ A rig cannot drill the same well twice (no self-loops):
$$Y_{iik} = 0  \hspace*{0.8cm} \forall i \in P , \forall k \in R \hspace*{3cm}(5)$$
+ Travel between two wells occurs in one direction only:
$$\sum_{k \in R} \left( Y_{ijk} + Y_{jik} \right) \leq 1  \hspace*{0.8cm} \forall i,j \in P \hspace*{2.5cm}(6)$$
+ Route continuity (flow conservation):
$$\sum_{i \in P} Y_{ilk} = \sum_{j \in P} Y_{ljk}  \hspace*{0.8cm} \forall l \in P , \forall k \in R \hspace*{2.7cm}(7)$$

### Complete Mathematical Model
 
The full integer linear program is written as:
 
$$
  \text{minimize} \quad Z = \max_{k=1}^{m} \left\lbrace t_{k} \right\rbrace
$$
 
$$
(PL)
   \left\{
         \begin{array}{lr}
 
 \sum_{j \in P, j \neq 0} Y_{0jk}  = 1 & \hspace*{1cm} \forall k \in R\\ \\
 \sum_{k \in R} \sum_{j \in P} Y_{ijk}  = 1 & \hspace*{1cm}  \forall i \in P , i \neq 0\\ \\
 \sum_{k \in R} \sum_{i \in P} Y_{ijk}  = 1 & \hspace*{1cm}  \forall j \in P , j \neq 0\\ \\
 \sum_{i \in P, i \neq 0} Y_{i0k}  = 1 & \hspace*{1cm}  \forall k \in R\\ \\
 Y_{iik}  = 0 & \hspace*{1cm} \forall i \in P , \forall k \in R \\ \\
\sum_{k \in R} \left( Y_{ijk} + Y_{jik} \right)  \leq 1 & \hspace*{1cm}  \forall i,j \in P \\ \\
\sum_{i \in P} Y_{ilk}  = \sum_{j \in P} Y_{ljk} & \hspace*{1cm} \forall l \in P , \forall k \in R\\ \\
Y_{ijk} \in \lbrace 0 , 1 \rbrace & \hspace*{1cm} \forall i,j \in P , \forall k \in R\\ \\
  \end{array}
             \right.
$$

## Linearization
 
The objective function above is nonlinear. Let $W$ denote the total project completion time. After linearization $\left( W \in \mathbb{R}_{+}^{*} \right)$, the objective becomes:
 
$$\text{minimize} \quad Z = W$$
 
with the additional constraint:
 
$$ \sum_{i \in P} \sum_{j \in P} \left( h_{i} + T_{ij} \right) \cdot Y_{ijk} \leq W \hspace*{1cm}, \forall k \in R$$
 
By incorporating this linearization constraint and updating the objective, we obtain the following integer linear program that fully models our problem:
 
$$
  \text{minimize} \quad Z = W
$$
 
$$
(PL)
   \left\{
         \begin{array}{lr}
  \sum_{i \in P} \sum_{j \in P} \left( h_{i} + T_{ij} \right) \cdot Y_{ijk} \leq W & \hspace*{1cm} \forall k \in R\\ \\
  \sum_{j \in P, j \neq 0} Y_{0jk}  = 1 & \hspace*{1cm} \forall k \in R\\ \\
 \sum_{k \in R} \sum_{j \in P} Y_{ijk}  = 1 & \hspace*{1cm}  \forall i \in P , i \neq 0\\ \\
 \sum_{k \in R} \sum_{i \in P} Y_{ijk}  = 1 & \hspace*{1cm}  \forall j \in P , j \neq 0\\ \\
 \sum_{i \in P, i \neq 0} Y_{i0k}  = 1 & \hspace*{1cm}  \forall k \in R\\ \\
 Y_{iik}  = 0 & \hspace*{1cm} \forall i \in P , \forall k \in R \\ \\
\sum_{k \in R} \left( Y_{ijk} + Y_{jik} \right)  \leq 1 & \hspace*{1cm}  \forall i,j \in P \\ \\
\sum_{i \in P} Y_{ilk}  = \sum_{j \in P} Y_{ljk} & \hspace*{1cm} \forall l \in P , \forall k \in R\\ \\
Y_{ijk} \in \lbrace 0 , 1 \rbrace & \hspace*{1cm} \forall i,j \in P , \forall k \in R\\ \\
W \in \mathbb{R}_{+}^{*}\\ \\
  \end{array}
             \right.
$$
 
## Model Size
 
### Number of Variables
 
The total number of variables is: $\mid P \mid \cdot \mid P \mid \cdot \mid R \mid + 1 = \left( \mid P \mid \right)^{2} \cdot \mid R \mid + 1 = n^{2} \cdot m + 1$
 
### Number of Constraints
 
We have:
+ $m$ constraints of type $(1)$.
+ $n-1$ constraints of type $(2)$.
+ $n-1$ constraints of type $(3)$.
+ $m$ constraints of type $(4)$.
+ $n \cdot m$ constraints of type $(5)$.
+ $n^{2}$ constraints of type $(6)$.
+ $n \cdot m$ constraints of type $(7)$.
+ $m$ linearization constraints.
The total number of constraints is: $n \left( n + 2m + 2 \right) + 3m + 2$

# Remark
 
Based on the mathematical formulation derived above, the problem at hand is a combinatorial optimization problem that reduces to the **uncapacitated vehicle routing problem (VRP)**.
 