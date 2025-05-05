# target: prerequisites
# 	command to build target

# construir el comando de compilación:
# python3 archivo.py -i archivo_test.ext ext=(txt, bin, tiff)

MAIN=huffman_base.py
PYTHON=python3
SYNTAX=-m py_compile

FILES=$(wildcard *.*)

APP=$(filter %.py, $(FILES))
APP_SYNTAX=$(addprefix syntax_, $(APP:.py=))
BIN_FILES=$(filter %.bin, $(FILES))
CSV_FILES=$(filter %.csv, $(FILES))
HUFFMAN_FILES=$(filter %.huffman, $(FILES))

IMG_TEST_FILES=$(wildcard ../img_test/*)
TIFF_FILES=$(patsubst ../img_test/%, %,$(IMG_TEST_FILES))
TEST_FILE=$(filter-out %.py, $(FILES))

TEMP_FILE=temp.txt
PYCACHE=__pycache__

# funciones Makefile
all:

touch_testf:
	touch $(TEMP_FILE)

$(TIFF_FILES):
	@echo -e "$(PYTHON) $(MAIN) -i $(addprefix ../img_test/, $@) \n"
	@$(PYTHON) $(MAIN) -i ../img_test/$@

$(BIN_FILES:.bin=): touch_testf
	xxd $@.bin > $(TEMP_FILE)

$(TEST_FILE):
	@echo -e "$(PYTHON) $(MAIN) -i $@ \n"
	@$(PYTHON) $(MAIN) -i $@

$(APP_SYNTAX):
	@echo -e "$(PYTHON) $(SYNTAX) $(patsubst syntax_%,%,$@).py \n"
	@$(PYTHON) $(SYNTAX) $(patsubst syntax_%,%,$@).py

# probar las variables 
echo:
# @echo "$(FILES)"
	@echo "$(BIN_FILES)"
	@echo "$(APP)"
	@echo "$(patsubst syntax_%,%,$(APP_SYNTAX))"
	@echo "$(TEST_FILE)"
	@echo "$(patsubst ../img_test/%,%,$(TIFF_FILES))"

clean:
	rm -rf $(PYCACHE)

.PHONY: all $(TIFF_FILES) $(BIN_FILES) $(TEST_FILE) $(APP_SYNTAX) echo clean