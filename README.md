
Use SWIG to build a simple Python wrapper for the Kinova library.  SWIG is used
to generate a wrapper shared library `_kinovapy.so` and a wrapper python module
`kinovapy.py`.  

Building
--------

Run `make` to build.  The Makefile assumes you are using Python
2.7 and have the Kinova API libraries and header files installed in default
locations.  To use a different version of Python or alternate locations or Kinova 
library, you can override the Make variables `PYTHON_INCLUDE` (Python include
directory path), `KINOVA_INCLUDE_DIR` (Kinova include directory path),
`KINOVA_LINK` (Kinova linker flags).

You will need `swig` (tested with SWIG 1.3) and Python development packages
installed (install `python2.7-dev` on Ubuntu/Debian).

The default Python include directory (`PYTHON_INCLUDE`) is 
`/usr/include/python2.7` for Python 2.7.  If you have a different version 
of Python installed, you can set `PYTHON_INCLUDE` to a different directory.

SWIG cannot parse some nested classes and the relatively new GCC "visibilty" 
attribute used by the standard Kinova header files, so you may want to use the 
header files from `emulate-kinova-api` even if using the real Kinova library, 
since the emulate-kinova-api headers have been modified to omit the "visibilty" 
attributes on functions if `KINOVA_NOEXPORT` is defined, which this SWIG wrapper 
does, and other minor changes.

To do so, first clonen the `emulate-kinova-api` repository from 
<http://github.com/MobileRobots/emulate-kinova-api>.  Next, set a 
`KINOVA_INCLUDE_DIR` environment variable or set it on the `make`
command line to use the header files from `emulate-kinova-api`.  
You must choose the headers directory that matches the version
of the real Kinova library you are going to link to. For example, for version
5.2.0:

    make KINOVA_INCLUDE_DIR=../emulate-kinova-api/headers.50200

For 5.1.4 instead, use "headers.50104", and for 5.1.1, use "headers.50101".
This will prevent mismatch between the contents of the headers and the actual
symbols library.

You will also need to add the library directory to the `LD_LIBRARY_PATH`
environment variable (e.g. for the example above, use `export
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../emulate-kinova-api`). Or copy the shared
library to the same directory as the Python module.


You can also set `KINOVA_LINK` to choose which libraries to link to.
For example, to use the `emulate_kinova` library instead of the real 5.2.0
Kinova libraries, build emulate-kinova-api first, then make this wrapper with:

    make KINOVA_INCLUDE_DIR=../emulate-kinova-api/headers.50200 KINOVA_LINK="-L../emulate-kinova-api -l:emulate_kinova_50200.so"

We have to use the `-l:` link option instead of `-l` since the Kinova libraries and
don't start with "lib".  To use a different header
file version, specify the alternate version in both thet headers directory
and library name.  For example, for 5.2.0:

Use
---

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

An extra function has been added to the wrapper that only returns
the count, or -1 on error: `GetNumDevices()`.

An extra function has also been added to the Python wrapper: `SetActiveDeviceNum(i)`
takes an index instead of a `KinovaDevice` object.

The contents of the following objects can be printed/converted to strings for easier 
debugging and logging, similar to native Python objects and data structures:
* QuickStatus
* AngularPosition
* AngularInfo
* CartesianPosition
* CartesianInfo
* ForcesInfo

(i.e. they have __str__() methods defined)
