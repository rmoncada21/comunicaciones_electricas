from math import log2

# Cálculo de la entropia de la fuente
def entropia_fuente(freq):
    HX = 0;
    print("Entropia de la fuente");
    for clave, valor_pi in freq: # probabilidad del simbolo i
        # print(f"{valor_pi}");
        HX += -(valor_pi*log2(valor_pi))
    
    print(f"H(X) = {HX}")
    return HX

# Cálculo de la longitud promedio de los códigos generados por huffman
def longitud_media(freq, huffman_code):
    longitud = 0
    
    for clave, valor_pi in freq:
        # print(f"pi: {valor_pi}") # pi
        # print(f"li: {(len(huffman_code[clave]))}") # li
        longitud += valor_pi * len(huffman_code[clave])
    print(f"Longitud promedio: {longitud}")

    return longitud
