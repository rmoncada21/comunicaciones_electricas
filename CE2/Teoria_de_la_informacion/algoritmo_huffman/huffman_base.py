import os
import sys
import getopt
import csv
import shannon_functions as shannon_compute
import compress
import node_tree
import decompress

# Parametros de entrada y ayuda:
file_full_path = ""
file_split_path = [];
def myfunc(argv):
    global file_full_path, file_split_path
    arg_output = ""
    arg_user = ""
    arg_help = "{0} -i <input>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "hi:", ["help", "input="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  
            sys.exit(2)
        elif opt in ("-i", "--input"):
            file_full_path = arg
            file_split_path = os.path.normpath(file_full_path)
            file_split_path = os.path.split(file_split_path)


if __name__ == "__main__":
    myfunc(sys.argv)


file_huffman_comprimido = file_full_path+".huffman"
ruta_diccionario = file_full_path+".diccionario.csv"
recovered_path = os.path.join(file_split_path[0], "recovered_"+file_split_path[1]);

#-----------------------------------------------------
# Algoritmo de compresión de huffman
#-----------------------------------------------------

#Apertura y lectura del archivo
string=[];
with open(file_full_path, "rb") as f:
    while (byte := f.read(1)):
        # Do stuff with byte.
        int_val = int.from_bytes(byte, "big")
        string.append(int_val)

# print(f"{string}");
# # Árbol binario
# class NodeTree(object):
#     def __init__(self, left=None, right=None):
#         self.left = left
#         self.right = right
#     def children(self):
#         return (self.left, self.right)
#     def nodes(self):
#         return (self.left, self.right)
#     def __str__(self):
#         return '%s_%s' % (self.left, self.right)

# def insert_in_tree(raiz, ruta, valor):
#     if(len(ruta)==1):
#         if(ruta=='0'):
#             raiz.left = valor;
#         else:
#             raiz.right = valor;
#     else:
#         if(ruta[0]=='0'):
#             #if type(raiz.left) is int:
#             if(raiz.left==None):
#                 raiz.left = NodeTree(None,None);
#             ruta = ruta[1:];
#             insert_in_tree(raiz.left,ruta,valor);
#         else:
#             #if type(raiz.right) is int:
#             if(raiz.right==None):
#                 raiz.right = NodeTree(None,None);
#             ruta = ruta[1:];
#             insert_in_tree(raiz.right,ruta,valor);

# Función principal del algoritmo de Huffman
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is int:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d
    

# calculo de frecuencias y probabilidades
prob_unit = 1/len(string) # string contiene todos los caracteres repetidos
freq = {} # diccionario
for c in string:
    if c in freq:
        freq[c] += prob_unit
    else:
        freq[c] = prob_unit

freq = sorted(freq.items(), key=lambda x: x[1], reverse=True) # se convierte a lista de tuplas
# print(f"Longitud de freq: {len(freq)}")
# print(f"freq: {freq}")
nodes = freq
# print(f"Nodos: {nodes}")

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = node_tree.NodeTree(key1, key2)
    nodes.append((node, c1 + c2))
    #print(nodes)
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

huffmanCode = huffman_code_tree(nodes[0][0])

# print(' Char | Huffman code ')
# print('----------------------')
# for (char, frequency) in freq:
#     print(' %-4r |%12s' % (char, huffmanCode[char]))


################################## Implementaciones
L_og = shannon_compute.longitud_original(freq)
HX = shannon_compute.entropia_fuente(freq) # entropia de la fuente
L_huff = shannon_compute.longitud_promedio_huffman_code(freq, huffmanCode)
var = shannon_compute.varianza_huffman_code(freq, huffmanCode, L_huff)
eff_og = shannon_compute.eficiencia_original(HX, L_og)
eff_huff = shannon_compute.eficiencia_original(HX, L_huff)
################################## Impresiones
# print("========== Resultados de la Compresión ==========")
# # print(f"Size string: {len(string)}")
# print(f"Longitud del alfabeto de la fuente:  {len(freq)}")
# print(f"Longitud del código original (fijo): {L_og} bits/símbolo")
# print(f"Entropía de la fuente:               {HX} bits/símbolo")
# print(f"Longitud media del código Huffman:   {L_huff} bits/símbolo")
# print(f"Varianza del código Huffman:         {var} bits²")
# print(f"Eficiencia respecto al original:     {eff_og:.2f} %")
# print(f"Eficiencia del código Huffman:       {eff_huff:.2f} %")
# print("=================================================")

################################## Compresión
print("========== Segunda Parte: Compresión ==========")
# print(f"Cadena original:\n{string}\n");
# Realiza la compresión de la cadena utilizando el diccionario de Huffman
byte_string = compress.huffman_compress(string, huffmanCode)
# print(f"Representación binaria (byte_string):\n{byte_string}\n")
# Convierte la representación binaria a una lista de bytes
lista_byte = compress.convert_lista_byte(byte_string)
# print(f"Lista de bytes generada:\n{lista_byte}\n")
# Escribe los datos comprimidos en un archivo binario
compress.write_binary_file(file_huffman_comprimido, lista_byte)
# Escribe el diccionario de Huffman en un archivo CSV
compress.write_csv_file(string, ruta_diccionario, huffmanCode)
# Cálculo de tamaños y tasa de compresión
original_size_bytes = compress.original_file_size(string)
compressed_size_bytes = compress.compressed_file_size(file_huffman_comprimido)
compression_rate_percent = compress.compression_rate_precent(original_size_bytes, compressed_size_bytes)
################################## Resultados
print("========== Tamaño y Tasa de Compresión ==========")
print(f"Tamaño original (bytes):           {original_size_bytes}")
print(f"Tamaño comprimido (bytes):         {compressed_size_bytes}")
print(f"Tasa de compresión:                {compression_rate_percent:.2f} %")
print("=================================================")

################################## Descompresión
bits_a_leer,diccionario = decompress.leer_diccionario(ruta_diccionario)
decoding = decompress.construir_arbol(diccionario)
data_estimated = decompress.decodificar_binario(string, huffmanCode, decoding)
compress.write_binary_file(recovered_path, data_estimated)
recovered_size_bytes = compress.compressed_file_size(recovered_path)
################################## Resultados
print("\n========== Descompresión ==========")
print(f"Tamaño original (bytes):           {original_size_bytes}")
print(f"Tamaño recovered (bytes):          {recovered_size_bytes}")
print(f"string==data_estimated:            {string==data_estimated}")
print("")
print(f"String: {string}")
print(f"Data estimado: {data_estimated}")
print("=================================================")