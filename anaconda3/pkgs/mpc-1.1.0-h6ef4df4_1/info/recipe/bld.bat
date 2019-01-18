if "%ARCH%"=="32" (
    set PLATFORM=Win32
) else (
    set PLATFORM=x64
)

mkdir dll\%PLATFORM%\Release
mkdir lib\%PLATFORM%\Release

set mpc_root=%cd%
cd ..

for %%d in (mpir, mpfr) do (
    mkdir %%d\dll\%PLATFORM%\Release
    mkdir %%d\lib\%PLATFORM%\Release

    REM copy libraries
    copy %LIBRARY_BIN%\%%d.dll %%d\dll\%PLATFORM%\Release\%%d.dll
    copy %LIBRARY_LIB%\%%d.lib %%d\dll\%PLATFORM%\Release\%%d.lib
    copy %LIBRARY_LIB%\%%d_static.lib %%d\lib\%PLATFORM%\Release\%%d.lib
)

REM copy headers
xcopy %LIBRARY_INC%\*.h mpir\lib\%PLATFORM%\Release\ /E
xcopy %LIBRARY_INC%\*.h mpir\dll\%PLATFORM%\Release\ /E
copy %LIBRARY_INC%\gmp-config.h mpir\lib\%PLATFORM%\Release\config.h
copy %LIBRARY_INC%\gmp-config.h mpir\dll\%PLATFORM%\Release\config.h
copy %LIBRARY_INC%\gmp-longlong.h mpir\lib\%PLATFORM%\Release\longlong.h
copy %LIBRARY_INC%\gmp-longlong.h mpir\dll\%PLATFORM%\Release\longlong.h

cd %mpc_root%\build.vc14

msbuild.exe /p:Platform=%PLATFORM% /p:Configuration=Release /p:PostBuildEvent="" mpc_lib\mpc_lib.vcxproj
msbuild.exe /p:Platform=%PLATFORM% /p:Configuration=Release /p:PostBuildEvent="" mpc_dll\mpc_dll.vcxproj

copy dll\%PLATFORM%\Release\mpc.lib %LIBRARY_LIB%\mpc.lib
copy dll\%PLATFORM%\Release\mpc.dll %LIBRARY_BIN%\mpc.dll
copy dll\%PLATFORM%\Release\mpc.pdb %LIBRARY_BIN%\mpc.pdb

copy lib\%PLATFORM%\Release\mpc.lib %LIBRARY_LIB%\mpc_static.lib

cd %mpc_root%
copy src\mpc.h %LIBRARY_INC%\mpc.h


REM testing
cd build.vc14
xcopy dll\%PLATFORM%\Release\mpc.* ..\dll\%PLATFORM%\Release\ /E
mkdir dll_tests\%PLATFORM%\Release

msbuild.exe /property:SolutionDir=..\..\ /property:OutDir=..\..\%PLATFORM%\Release\ /p:Platform=%PLATFORM% /p:Configuration=Release dll_tests\add_test_lib\add_test_lib.vcxproj
copy %PLATFORM%\Release\test_lib.lib dll_tests\%PLATFORM%\Release\test_lib.lib

for /d %%d in (dll_tests\*) do (
    for %%f in (%%d\*.vcxproj) do (
        msbuild.exe /property:SolutionDir=..\..\ /property:OutDir=..\..\%PLATFORM%\Release\ /p:Platform=%PLATFORM% /p:Configuration=Release %%f
    )
)

REM for /r "%PLATFORM%\Release\" %%a in (*.exe) do ( %%~fa )
xcopy ..\tests\* %PLATFORM%\Release\ /E
cd %PLATFORM%\Release
treal.exe
if errorlevel 1 exit 1
