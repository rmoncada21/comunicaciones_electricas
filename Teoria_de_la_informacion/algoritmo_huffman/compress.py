import csv

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
    print(f"byte_string: {byte_string}")

    # print(f"byte_string: {byte_string}")
    return byte_string

def convert_lista_byte(lista_binaria):
    lista_byte = []
    lista_byte = [int(b, 2) for b in lista_binaria]
    # print(f"lista_byte: {lista_byte}")
    return lista_byte

# def huffman_compress_2(ruta_diccionario, binary_string, huffmanCode):    
#     csvfile = open (ruta_diccionario,'w')
#     compressed_length_bit = len (binary_string)

#     writer = csv.writer (csvfile)
#     writer.writerow ([str( compressed_length_bit) ,"bits"])
    
#     for entrada in huffmanCode:
#         writer . writerow ([ str(entrada) , huffmanCode[entrada]])
#         csvfile . close ()
