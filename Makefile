
ifndef SWIG
SWIG:=swig
endif

ifndef PYTHON_INCLUDE
PYTHON_INCLUDE:=/usr/include/python2.7
endif

ifndef KINOVA_INCLUDE_DIR
KINOVA_INCLUDE_DIR:=/usr/include/KinovaAPI
endif

ifndef KINOVA_LIB_DIR
KINOVA_LIB_DIR:=/usr/lib
endif

ifndef KINOVA_LIB
KINOVA_LIB:=Kinova.API.USBCommandLayerUbuntu.so
endif

all: _kinovapy.so kinovapy.py

clean: 
	-rm _kinovapy.so kinovapy.py kinovapy.cc


_kinovapy.so: kinovapy.cc 
	$(CXX) -fPIC -g -shared -o $@ -I$(KINOVA_INCLUDE_DIR) -I$(PYTHON_INCLUDE) $< -L$(KINOVA_LIB_DIR)  -l:$(KINOVA_LIB)

# maybe need -Wl,-rpath,$(KINOVA_LIB_DIR)

kinovapy.cc kinovapy.py: swig_wrapper.i $(KINOVA_INCLUDE_DIR)/Kinova.API.CommLayerUbuntu.h $(KINOVA_INCLUDE_DIR)/Kinova.API.UsbCommandLayerUbuntu.h $(KINOVA_INCLUDE_DIR)/KinovaTypes.h
	$(SWIG) -Wall -c++ -python -modern -module kinovapy -I$(KINOVA_INCLUDE_DIR) -o kinovapy.cc swig_wrapper.i

.PHONY: all clean

