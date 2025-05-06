# Teoría de la información -  Teorema de Shannon

### Entropía de la fuente

$$
H(X) = -\sum_{i=1}^n p(x_i) \log_2 p(x_i)
$$

* $H(X)$: Entropía de la fuente (bits/símbolo)
* $n$: Número total de símbolos distintos
* $p(x_i)$: Probabilidad del símbolo $x_i$

---

### Longitud media del código Huffman

$$
L = \sum_{i=1}^n p(x_i) \cdot l_i
$$

* $L$: Longitud media del código (bits/símbolo)
* $l_i$: Longitud del código asignado al símbolo $x_i$
* $p(x_i)$: Probabilidad del símbolo $x_i$
* $n$: Número total de símbolos

---

### Varianza de la longitud del código

$$
\text{Var}(L) = \sum_{i=1}^{n} p(x_i) \cdot (l_i - L)^2
$$

* $\text{Var}(L)$: Varianza de las longitudes de los códigos (bits²)
* $L$: Longitud media del código
* $l_i$: Longitud del código del símbolo $x_i$
* $p(x_i)$: Probabilidad del símbolo $x_i$

---

### Eficiencia del código

$$
\text{Eficiencia} = \frac{H(X)}{L} \cdot 100\%
$$

* $\text{Eficiencia}$: Porcentaje de eficiencia del código
* $H(X)$: Entropía de la fuente (bits/símbolo)
* $L$: Longitud media del código (bits/símbolo)

---