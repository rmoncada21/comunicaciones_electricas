# Cálculo de tiempos de desfase

- Una señal de **audio estéreo (canal izquierdo y derecho)** con frecuencia **15 kHz** y un desfase de **π radianes (180°)**
- Una señal de **video simulada** con frecuencia **42 MHz (42 × 10⁶ Hz)** y un desfase de **π/2 radianes (90°)**



## 1. Señal de audio:  
$ f = 15 \text{kHz}, \phi = \pi $ rad

Usamos la fórmula general:

$$
\Delta t = \frac{\phi}{2\pi} \cdot \frac{1}{f}
$$


$$
\Delta t = \frac{\pi}{2\pi} \cdot \frac{1}{15000}
$$

$$
\boxed{66.66\ \mu\text{s}}
$$



## 2. Señal de video:  
$ f = 42 \text{MHz}, \phi = \frac{\pi}{2} $ rad

Primero calculamos el período de la señal de video:


$$
\Delta t  = \frac{\pi/4}{2\pi} \cdot \frac{1}{42e6} \text{ ns}
$$

$$
\boxed{5.95 \ \text{ns}}
$$



## 📊 Tabla comparativa final

| Parámetro | Señal de Audio (15 kHz) | Señal de Video (42 MHz) |
|----------|--------------------------|--------------------------|
| Frecuencia | 15,000 Hz | 42,000,000 Hz |
| Desfase en radianes | π (180°) | π/2 (90°) |
| Período (T) | 66.67 μs | 23.81 ns |
| Desfase en tiempo | 33.33 μs | 5.95 ns |

---

## ¿Relación entre señales?

### 1. **En magnitud absoluta**
- El desfase del **audio es mucho mayor** que el del **video**:
  - $ 33.33 \ \mu\text{s} > 5.95 \ \text{ns} $
- Cabe recalcar que las señales de audio tienen frecuencias más bajas → **ciclos más largos**, por lo tanto, **desfases similares en radianes equivalen a tiempos mayores**.

### 2. **En proporción del período**
- En audio:  
  $$
  \frac{\pi}{2\pi} = \frac{1}{2} \Rightarrow \text{El desfase representa el } \boxed{50\%} \text{ del período}
  $$
- En video:  
  $$
  \frac{\pi/2}{2\pi} = \frac{1}{4} \Rightarrow \text{El desfase representa el } \boxed{25\%} \text{ del período}
  $$

### 3. **Impacto perceptivo**
- **Audio**: Un desfase de **33.33 μs** puede no ser perceptible individualmente, pero si hay acumulación o diferencia con el video, podría afectar la experiencia.
- **Video**: Un desfase de **5.95 ns** es **muy pequeño incluso en términos relativos al ciclo**, y **no tendría impacto visual**.



## Relación en sistemas multimedia

En sistemas donde conviven **señales de audio y video** (como en emisiones de TV, streaming o Blu-ray), los desfases aceptables están en el rango de **milisegundos** (ej: ITU recomienda hasta 45 ms de diferencia entre audio y video).

Por tanto:

- Estos desfases (**microsegundos y nanosegundos**) **no causarían problemas visibles ni audibles por sí solos**.
- Sin embargo, **en sistemas de medición de sincronía o corrección automática**, estos pequeños desfases pueden usarse como base para ajustar con precisión la sincronización global.



### Resumen

| Concepto | Señal de Audio (15 kHz) | Señal de Video (42 MHz) |
|---------|--------------------------|--------------------------|
| Frecuencia | 15,000 Hz | 42,000,000 Hz |
| Desfase | π rad (180°) | π/2 rad (90°) |
| Período | 66.67 μs | 23.81 ns |
| Retraso en tiempo | 33.33 μs | 5.95 ns |
| % del período | 50% | 25% |
| Impacto perceptivo | Puede contribuir a error de sincronización audio-video | Ninguno perceptible |

