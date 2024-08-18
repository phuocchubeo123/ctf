I am learning a bit about integral closure. 

*Definition 1. [Integral element]* Let $A$ be a subring of $B$. An element $u \in B$ is integral over $A$ if there exists a *monic* polynomial $f$ in $A[X]$ such that $f(u) = 0$.

The *integral* idea here is kind of analoguous to the case of $\mathbb{Z}$, when a *monic* polynomial with integer coefficients only takes integer roots, if these roots are rational. 
Before going into another viewpoint of Definition 1, we introduce the notation of module.

*Definition 2. [Module]* Let $R$ be a ring. A *left $R$-module* $M$ consists of an abelian group $(M, +)$ and an operation $\cdot: R \times M \to M$ such that for all $r, s \in R$ and $x, y \in M$, we have:
* $r \cdot (x + y) = r \cdot x + r \cdot y$
* $(r + s) \cdot x = r \cdot x + s \cdot x$
* (rs) \cdot x = r \cdot (s \cdot x)
* 1 \cdot x = x

Basically, an $R$-module is like a vector space with scalar in ring $R$, instead of the usual vector space with scalar in a field.

*Lemma 1.* Let $A$ be a subring of $B$. An element $u \in B$ is integral over $A$ if and only if $B$ contains an $A[u]$-module that contains $1$ and is finitely generated as an $A$-module. 