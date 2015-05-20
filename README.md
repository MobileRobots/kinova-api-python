
Use SWIG to build a simple Python wrapper for the Kinova library.  Swig is used
to generate a wrapper shared library `_kinovapy.so` and a wrapper python module
`kinovapy.py`.  

Run `make` to build.  The Makefile assumes you are using Python
2.7 and have the Kinova API libraries and header files installed in default
locations.  To use a different version of Python or alternate locations or Kinova 
library, you can override the Make variables `PYTHON_INCLUDE` (Python include
directory path), `KINOVA_INCLUDE_DIR` (Kinova include directory path),
`KINOVA_LIB_DIR` (Kinova library directory), or `KINOVA_LIB` (name of the Kinova
shared library to link to). For example, to use `emulate_kinova` library instead
of the real Kinova library:
    make KINOVA_INCLUDE_DIR=../emulate-kinova-api/headers.50104 KINOVA_LIB_DIR=../emulate-kinova-api KINOVA_LIB=emulate_kinova_50104.so
You will also need to add the library directory to the `LD_LIBRARY_PATH`
environment variable (e.g. for the example above, use `export
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../emulate-kinova-api`). Or copy the shared
library to the same directory as the Python module.

The Python module is named `kinovapy`:

    import kinovapy
    
    kinovapy.InitAPI()

Importing the `kinovapy` Python module will automatically load the
`_kinovapi.so` wrapper library.  

You will need to set `PYTHONPATH` and `LD_LIBRARY_PATH` environment variables
to include this directory before running programs.  `

Note: The Python wrapper links directly to the Kinova API shared library, it
does not load it using dlopen as the Kinova C++ example programs do.

This has been tested with version 50104.

Only a few functions have been tested.

Some functions in the Kinova API take an `int&` argument via which the
result/error code is passed back to the caller.  In Python, values cannot
be returned via argument references, instead a set (tuple) of values is
returned by the function.  For example, the GetDeviceCount function uses an
int reference argument in C++:
 
    int result;
    int count = GetDeviceCount(result);

but in Python both the result and count are returned:

    result,count = kinovapy.GetDeviceCount()

An extra function has been added to the Python wrapper: `SetActiveDeviceNum(i)`
takes an index instead of a `KinovaDevice` object.


