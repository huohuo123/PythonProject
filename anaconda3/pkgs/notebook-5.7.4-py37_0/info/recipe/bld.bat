set MENU_DIR=%PREFIX%\Menu
mkdir %MENU_DIR%

copy %RECIPE_DIR%\jupyter.ico %MENU_DIR%
if errorlevel 1 exit 1

copy %RECIPE_DIR%\menu-windows.json %MENU_DIR%\notebook.json
if errorlevel 1 exit 1

pip install --no-deps .
if errorlevel 1 exit 1

rd /s /q %SCRIPTS%
