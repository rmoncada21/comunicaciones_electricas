import csv
import node_tree

def leer_diccionario(ruta_diccionario):
    with open(ruta_diccionario, 'r') as csvfile:
        reader = csv.reader(csvfile)
        bits_a_leer = None
        diccionario = dict()

        for row in reader:
            if bits_a_leer is None:
                bits_a_leer = int(row[0])
            else:
                diccionario[int(row[0])] = row[1]

    return bits_a_leer, diccionario

# def construir_arbol(diccionario):
#     Decoding = node_tree.NodeTree(None, None)
#     for entrada in diccionario:
#         node_tree.insert_in_tree(Decoding, diccionario[entrada], entrada)
#     return Decoding

def construir_arbol(diccionario):
    Decoding = node_tree.NodeTree(None, None)
    for entrada in diccionario:
        ruta = diccionario[entrada]
        
        # Verificar que la ruta no esté vacía antes de intentar insertarla
        if ruta != "":
            node_tree.insert_in_tree(Decoding, ruta, entrada)
        else:
            # Si la ruta está vacía, significa que solo hay un símbolo
            Decoding = entrada  # Asignamos directamente el valor al árbol raíz
    return Decoding

def decodificar_binario(string,huffmanCode, Decoding):
    nodo = Decoding
    data_estimated = []
    binary_string = [] # lista

    for c in string :
        # print(f"Huffman_code: {huffmanCode[c]}")  
        binary_string += huffmanCode[c]
    
    # print(f"binary_string: {binary_string}")

    compressed_length_bit = len (binary_string)

    for i in range(compressed_length_bit):
        (l, r) = nodo.children()
        if binary_string[i] == '1':
            nodo = r
        else:
            nodo = l

        if type(nodo) is int:
            data_estimated.append(nodo)
            nodo = Decoding

    return data_estimated
