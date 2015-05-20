%module kinovapy
%feature("autodoc", "1");

%include "typemaps.i"
%apply int &OUTPUT { int &result };

#define KINOVAAPI_NOEXPORT 1

%{
#include "KinovaTypes.h"
#include "Kinova.API.CommLayerUbuntu.h"
#include "Kinova.API.UsbCommandLayerUbuntu.h"


int SetActiveDeviceNum(int d) {
  KinovaDevice devices[MAX_KINOVA_DEVICE];
  int result;
  int count = GetDevices(devices, result);
  if(result != NO_ERROR_KINOVA) 
    return -1;
  if(d > count || d > MAX_KINOVA_DEVICE)
    return -1;
  return SetActiveDevice(devices[d]);
}

%}


/*
%typemap(in,numinputs=0) int& result (int temp) "$1 = &temp;"

%typemap(argout) int& result {
  %append_output(PyInt_FromLong(*$1));
}
*/

%include "KinovaTypes.h"
%include "Kinova.API.CommLayerUbuntu.h"
%include "Kinova.API.UsbCommandLayerUbuntu.h"

int SetActiveDeviceNum(int d);

