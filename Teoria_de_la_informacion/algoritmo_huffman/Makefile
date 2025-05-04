# target: prerequisites
# 	command to build target

# construir el comando de compilación:
# python3 archivo.py -i archivo_test.ext ext=(txt, bin, tiff)

FILES=$(wildcard *.*)
MAIN=huffman_base.py
APP=$(filter %.py, $(FILES))
APP_SYNTAX=$(addprefix syntax_, $(APP:.py=))
TEST_FILE=$(filter-out %.py, $(FILES))
PYTHON=python3
SYNTAX=-m py_compile
PYCACHE=__pycache__

# funciones Makefile
all:

$(TEST_FILE):
	@echo -e "$(PYTHON) $(MAIN) -i $@ \n"
	@$(PYTHON) $(MAIN) -i $@

$(APP_SYNTAX):
	@echo -e "$(PYTHON) $(SYNTAX) $(patsubst syntax_%,%,$@).py \n"
	@$(PYTHON) $(SYNTAX) $(patsubst syntax_%,%,$@).py

# probar las variables 
echo:
# @echo "$(FILES)"
	@echo "$(APP)"
	@echo "$(patsubst syntax_%,%,$(APP_SYNTAX))"
	@echo "$(TEST_FILE)"

clean:
	rm -rf $(PYCACHE)

.PHONY: all $(TEST_FILE) $(APP_SYNTAX) echo clean