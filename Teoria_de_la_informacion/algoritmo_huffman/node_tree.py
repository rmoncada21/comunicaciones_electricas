

# Árbol binario
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def nodes(self):
        return (self.left, self.right)
    def __str__(self):
        return '%s_%s' % (self.left, self.right)

def insert_in_tree(raiz, ruta, valor):
    if len(ruta) == 1:
        if ruta == '0':
            raiz.left = valor
        else:
            raiz.right = valor
    else:
        if ruta[0] == '0':
            if raiz.left is None:
                raiz.left = NodeTree(None, None)
            insert_in_tree(raiz.left, ruta[1:], valor)
        else:
            if raiz.right is None:
                raiz.right = NodeTree(None, None)
            insert_in_tree(raiz.right, ruta[1:], valor)