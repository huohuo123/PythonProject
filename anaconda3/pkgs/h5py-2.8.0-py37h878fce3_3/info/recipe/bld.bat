SETLOCAL EnableDelayedExpansion

pushd %PREFIX%\conda-meta\
for %%g in (hdf5*.json) do (set JSON_FILE=%%~g)
popd

for /f "tokens=2 delims=-" %%i in ("%JSON_FILE%") do (set HDF5_VER=%%i)

:: hdf5 env var provided by conda-build 3 variant
python setup.py configure --hdf5="%LIBRARY_PREFIX%"  --hdf5-version=%HDF5_VER%
if errorlevel 1 exit 1

python setup.py install --single-version-externally-managed --record record.txt
if errorlevel 1 exit 1
