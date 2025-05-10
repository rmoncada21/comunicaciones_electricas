# Desfase y sincronización de señales

### 1. Representación compleja de una senoidal

Una señal senoidal puede expresarse como:

$$
x(t) = \sin(2\pi f t) = \frac{1}{2j} \left( e^{j2\pi f t} - e^{-j2\pi f t} \right)
$$

Sin embargo, para fines de procesamiento digital, se utiliza la **forma compleja**:

$$
x_{\text{complejo}}(t) = e^{j 2\pi f t}
$$

Esta representación ofrece varias ventajas:

* Permite **desfasar fácilmente** una señal mediante la multiplicación por un factor rotacional $e^{j\phi}$.
* La magnitud permanece constante, y solo se modifica la **fase**.

---

### 2. Aplicación del desfase: Multiplicación compleja

Para aplicar un desfase $\phi$ a la señal, se realiza la siguiente operación:

$$
x_{\text{desfasado}}(t) = x_{\text{complejo}}(t) \cdot e^{j\phi} = e^{j(2\pi f t + \phi)}
$$

La parte real de esta señal resulta en una senoide desplazada en fase:

$$
\text{Re}\left\{ e^{j(2\pi f t + \phi)} \right\} = \cos\left(2\pi f t + \phi\right)
$$

> De esta manera, un desfase en el dominio complejo **equivale a una rotación del fasor**.

---

### 3. Propiedades de la Transformada de Fourier implicadas

Este procedimiento se fundamenta en diversas propiedades de la Transformada de Fourier (TF):

#### a. Desplazamiento en el tiempo

La propiedad de desplazamiento en el tiempo establece que si una señal arbitraria $x(t)$ es desplazada un intervalo $t_0$, su transformada de Fourier se modifica multiplicándola por un exponencial complejo que depende del desplazamiento y su signo:

$$
x(t - t_0) \leftrightarrow X(\omega) e^{-j \omega t_0}
$$

donde:

* $x(t - t_0)$: Señal desplazada en el tiempo.
* $X(\omega)$: Transformada de Fourier de la señal original.
* $e^{-j \omega t_0}$: Término que incorpora el desfase en frecuencia.

#### b. Desplazamiento en frecuencia

Según esta propiedad, si una señal $x(t)$ se multiplica por un exponencial complejo de frecuencia $\omega_0$, su espectro se desplaza en el dominio de la frecuencia:

$$
x(t) e^{\pm j \omega_0 t} \leftrightarrow X(\omega \mp \omega_0)
$$

donde:

* $x(t) e^{\pm j \omega_0 t}$: Señal modulada.
* $X(\omega \mp \omega_0)$: Espectro desplazado en frecuencia.

#### c. Dualidad

La propiedad de dualidad indica que si $x(t)$ tiene transformada de Fourier $X(\omega)$, entonces $X(t)$ tendrá como transformada $2\pi x(-\omega)$:

$$
X(t) \leftrightarrow 2\pi x(-\omega)
$$

donde:

* $X(t)$: Función temporal equivalente a la transformada.
* $x(-\omega)$: Versión invertida de la señal original respecto a la frecuencia.
* El factor $2\pi$ surge por convenciones en la definición de la transformada.

---

### 4. Sincronización: Compensación del desfase

Para recuperar la señal original, se aplica un desfase inverso:

$$
x_{\text{re\_sync}}(t) = x_{\text{desfasado}}(t) \cdot e^{-j\phi} = e^{j(2\pi f t + \phi)} \cdot e^{-j\phi} = e^{j2\pi f t}
$$

$$
e^{j(2\pi f t + \phi)} \cdot e^{-j\phi} = e^{j2\pi f t}
$$

Posteriormente, al tomar la parte real, se recupera exactamente la señal original.

---