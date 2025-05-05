import csv
import os

def huffman_compress(string, huffmanCode):
    binary_string = [] # lista

    for c in string :
        # print(f"Huffman_code: {huffmanCode[c]}")  
        binary_string += huffmanCode[c]
    
    # print(f"binary_string: {binary_string}")

    compressed_length_bit = len (binary_string)
    # print(f"compressed_length_bit: {compressed_length_bit}")

    #por si compressed_lenght_bit no es multiplo de 8 - rellenar lista con 0    
    if (compressed_length_bit%8 >0) :
        for i in range (8 - len(binary_string) % 8) :
            binary_string += '0'

    byte_string = "".join ([str(i) for i in binary_string])
    # print(f"byte_string: {byte_string}")
    
    # entrega byte_string con secciones de 8 bits cada uno
    byte_string = [byte_string [i:i+8] for i in range (0 , len (byte_string), 8) ];
    # print(f"byte_string: {byte_string}")

    # print(f"byte_string: {byte_string}")
    return byte_string

def convert_lista_byte(lista_binaria):
    lista_byte = []
    lista_byte = [int(b, 2) for b in lista_binaria]
    # print(f"lista_byte: {lista_byte}")
    return lista_byte

def write_binary_file(file_huffman_comprimido, lista_byte):
    with open(file_huffman_comprimido, "wb") as file:
        file.write(bytearray(lista_byte))


def write_csv_file(string, ruta_diccionario, huffmanCode):
    
    csvfile = open(ruta_diccionario,'w')
    writer = csv.writer (csvfile)
    
    binary_string = []
    for c in string :
        binary_string += huffmanCode[c]
    
    compressed_length_bit = len (binary_string)
    writer.writerow([str(compressed_length_bit) ,"bits" ])
    
    for entrada in huffmanCode:
        writer.writerow([str(entrada) , huffmanCode[entrada]])
    
    csvfile.close ()


def original_file_size(string):
    return len(string)

def compressed_file_size(file_huffman_comprimido):
    print(f"Archivo: {file_huffman_comprimido}")
    return os.path.getsize(file_huffman_comprimido)

def compression_rate_precent(original_file_size, compressed_file_size):
    if original_file_size > 0 & compressed_file_size != 0:
        compression_rate = 1 - (compressed_file_size / original_file_size)
        compression_rate_percent = compression_rate * 100
    else:
        compression_rate_percent = 0.0
    
    return compression_rate_percent