# Methodology
 
Several methods exist for solving optimization problems in general, and combinatorial optimization problems in particular. Each of these methods has its own way of operating, along with its own set of assumptions, advantages, and limitations.
 
In this work, we focus specifically on the class of discrete optimization problems with binary variables. The instances of our problem can in principle be solved using exact methods; however, their main drawback is that they require an unreasonable amount of computation time as the instance size grows. For this reason, approximate methods are a more practical choice, they yield good-quality solutions within a significantly reduced runtime.
 
Since the problem studied in this thesis can be regarded as a vehicle routing problem, it inherits the same computational complexity as that class of problems.
 
## Exact Methods
 
Formulating our problem as an integer linear program with binary variables ($0$ and $1$) naturally points toward using a solver as the most suitable exact resolution tool.
 
One such solver is CPLEX, a commercial optimization software marketed by IBM since its acquisition of the French company ILOG in $2009$. Its name is a reference to the **C** programming language and the simplex algorithm.
 
CPLEX is capable of solving:
+ Linear and mixed-integer linear programs.
+ Quadratic and mixed-integer quadratic programs.
+ Programs with quadratic and mixed-integer quadratic constraints.

## Approximate Methods
 
As established earlier, our problem can be reduced to an uncapacitated vehicle routing problem. The associated solution therefore consists of a set of $m$ routes (one per rig) where each route defines the ordered sequence of wells to be drilled by that rig. With this structure in mind, the nearest neighbor and insertion heuristics are natural candidates for generating feasible solutions.
 
### Heuristics

#### 1. *Nearest Neighbor*

Each route begins with a move from the dummy well to the closest available well. The heuristic builds all routes successively: each rig in turn is assigned the well closest to its last assigned well. This continues until the number of rigs exceeds the number of remaining wells, at which point rigs are selected randomly, each time assigning the nearest undrilled well, until all wells have been assigned.

$$
  
    \text{-------------------------------------------------------------------------------------}\\
    \text{Pseudocode: Nearest Neighbor}\\ 
    \text{-------------------------------------------------------------------------------------}\\
    - \text{Let $P = \lbrace 1, 2,..., n \rbrace$ be the set of wells.}\\
    - \text{Let $R = \lbrace 1, 2,..., m \rbrace$ be the set of rigs.}\\
    \text{\textit{While} $|P| \geq |R|$ \textit{do}}\\
    \hspace{1cm}\text{\textit{For each} rig $k \in R$ \textit{do}}\\
    \hspace{2cm}- \text{Assign the nearest well in $P$ to the last well assigned to rig $k$.}\\
    \hspace{2cm}- \text{Remove that well from $P$.}\\
    \hspace{1cm}\textit{end for}\\
    \textit{end while}\\
    \text{\textit{While} $|P| \geq 1$ \textit{do}}\\
    \hspace{1cm}- \text{Randomly select a rig $k$.}\\
    \hspace{1cm}- \text{Assign the nearest well in $P$ to the last well assigned to rig $k$.}\\
    \hspace{1cm}- \text{Remove that well from $P$.}\\
    \textit{end while}\\
    \text{-------------------------------------------------------------------------------------}\\
  
$$

#### 2. *Insertion Heuristic*  
 
Similarly to the previous heuristic, this method starts by building $m$ cycles of length $2$, each connecting the dummy well to the closest available well. Rigs are then selected in turn, and for each one, the uninserted well closest to that rig's current cycle is identified. Once such a well, denoted $k$ is found, it is inserted between two consecutive wells $i$ and $j$ in the cycle in a way that minimizes the additional travel time ($T_{ik} + T_{kj} + T_{ij}$ minimum). This continues until the number of rigs exceeds the number of remaining wells, at which point rigs are selected randomly and the nearest insertion process continues until all wells have been assigned.

$$
  \begin{array}{l} 
    \text{-------------------------------------------------------------------------------------}\\
    \text{Pseudocode: Insertion}\\ 
    \text{-------------------------------------------------------------------------------------}\\    
    - \text{Let $P = \lbrace 1, 2,..., n \rbrace$ be the set of wells.}\\
    - \text{Let $R = \lbrace 1, 2,..., m \rbrace$ be the set of rigs.}\\
    - \text{Let $C = \lbrace C_{1}, C_{2},..., C_{m}\rbrace$ be the set of cycles.}\\
    \text{\textit{For each} rig $k \in R$ \textit{do}}\\
    \hspace{1cm}- \text{Build cycle $C_k$ between the dummy well and the closest well in $P$.}\\
    \hspace{1cm}- \text{Remove that well from $P$.}\\
    \textit{end for}\\
    \text{\textit{While} $|P| \geq |R|$ \textit{do}}\\
    \hspace{1cm}\text{\textit{For each} rig $k \in R$ \textit{do}}\\
    \hspace{2cm}- \text{Find $j \in C_{k}$ and $w \in P$ such that $T_{jw}$ is minimum.}\\
    \hspace{2cm}- \text{Find edge $(i,j)$ in $C_k$ such that $T_{iw} + T_{wj} + T_{ij}$ is minimum.}\\
    \hspace{2cm}- \text{Insert well $w$ between wells $i$ and $j$ in $C_k$.}\\
    \hspace{2cm}- \text{Remove well $w$ from $P$.}\\
    \hspace{1cm}\textit{end for}\\
    \textit{end while}\\
    \text{\textit{While} $|P| \geq 1$ \textit{do}}\\
    \hspace{1cm}- \text{Randomly select a rig $k$.}\\
    \hspace{1cm}- \text{Find $j \in C_{k}$ and $w \in P$ such that $T_{jw}$ is minimum.}\\
    \hspace{1cm}- \text{Find edge $(i,j)$ in $C_k$ such that $T_{iw} + T_{wj} + T_{ij}$ is minimum.}\\
    \hspace{1cm}- \text{Insert well $w$ between wells $i$ and $j$ in $C_k$.}\\
    \hspace{1cm}- \text{Remove well $w$ from $P$.}\\
    \textit{end while}\\
  \text{-------------------------------------------------------------------------------------}\\
  \end{array}
$$

This is specifically a *nearest insertion* heuristic, since at each iteration the well chosen for insertion is the one closest to the current cycle