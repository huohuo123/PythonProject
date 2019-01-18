%PYTHON% setup.py install --hdf5=%LIBRARY_PREFIX% ^
                          --bzip2=%LIBRARY_PREFIX% ^
                          --lzo=%LIBRARY_PREFIX% ^
                          --blosc=%LIBRARY_PREFIX% ^
                          --single-version-externally-managed --record record.txt
if errorlevel 1 exit 1
