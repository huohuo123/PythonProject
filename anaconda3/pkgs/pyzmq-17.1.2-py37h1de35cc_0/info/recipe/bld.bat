set DISTUTILS_USE_SDK=1


:: For now, we build pyzmq with the bundled zeromq for py<35. There were a number of reasons for
:: this, including lib\libzmq.dll not being available, as well as
:: src\stdint.hpp not being available.
:: https://github.com/conda-forge/staged-recipes/pull/292 has some more detail.

set ZMQ=%LIBRARY_PREFIX%
:: set ZMQ=bundled
copy %LIBRARY_PREFIX%\bin\libzmq.lib %LIBRARY_PREFIX%\lib\libzmq.lib
python -m pip install -v . "--install-option=--zmq=%ZMQ%"
if errorlevel 1 exit 1
