@echo off
REM ============================================================================
REM  Inventarium - build_me.cmd
REM  Build script for Nuitka compilation (STANDALONE mode)
REM  
REM  Updated: 2025-12-24
REM  Target: Windows 10 / 11, Python 3.7+
REM ============================================================================

cd /d "%~dp0"

echo.
echo ============================================================================
echo  Inventarium Build System
echo ============================================================================
echo.

REM ============================================================================
REM  Pre-Build Checks
REM ============================================================================

echo [1/5] Checking Python installation...
py --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found! Install Python 3.7+ first.
    pause
    goto :eof
)
py --version

echo.
echo [2/5] Checking Nuitka installation...
py -m nuitka --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Nuitka not found!
    echo Install with: py -m pip install nuitka
    pause
    goto :eof
)
py -m nuitka --version

echo.
echo [3/5] Checking MinGW64 compiler...
where gcc >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [WARNING] MinGW64 not found in PATH.
    echo Nuitka will download it automatically on first build.
    timeout /t 2 >nul
) ELSE (
    echo MinGW64 found
)

echo.
echo [4/5] Checking icon file...
IF NOT EXIST "images\inventarium.ico" (
    echo [WARNING] images\inventarium.ico not found!
    echo .exe will have default Windows icon.
    timeout /t 2 >nul
) ELSE (
    echo [OK] Icon found: images\inventarium.ico
)

echo.
echo [5/5] Checking required files...
IF NOT EXIST "inventarium.py" (
    echo [ERROR] inventarium.py not found!
    pause
    goto :eof
)
IF NOT EXIST "engine.py" (
    echo [ERROR] engine.py not found!
    pause
    goto :eof
)
IF NOT EXIST "dbms.py" (
    echo [ERROR] dbms.py not found!
    pause
    goto :eof
)
echo [OK] All required Python files found.

echo.
echo ============================================================================
echo  Starting Nuitka Compilation
echo ============================================================================
echo.
echo Mode: STANDALONE (creates dist\inventarium.dist\ folder)
echo Output: dist\inventarium.dist\inventarium.exe
echo Icon: images\inventarium.ico (embedded in .exe)
echo.
echo This may take 5-15 minutes depending on your system...
echo (First build will be slower - downloads MinGW64 if needed)
echo.

REM ============================================================================
REM  Nuitka Compilation Command
REM ============================================================================

py -m nuitka inventarium.py ^
    --standalone ^
    --output-dir=dist ^
    --output-filename=inventarium ^
    --windows-icon-from-ico=images\inventarium.ico ^
    --enable-plugin=tk-inter ^
    --follow-imports ^
    --mingw64 ^
    ^
    --nofollow-import-to=tkinter.test ^
    ^
    --include-data-dir=fonts=fonts ^
    --include-data-dir=images=images ^
    --include-data-dir=reports=reports ^
    --include-data-dir=sql=sql ^
    --include-data-dir=views=views ^
    ^
    --include-data-files=label_templates.json=label_templates.json ^
    --include-data-files=LICENSE=LICENSE

REM ============================================================================
REM  Post-Build Check
REM ============================================================================

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================================================
    echo  BUILD FAILED (ERRORLEVEL=%ERRORLEVEL%)
    echo ============================================================================
    echo.
    echo Common issues:
    echo  - MinGW64 not found (let Nuitka download it automatically)
    echo  - Missing dependencies (check imports)
    echo  - Syntax errors in Python code
    echo  - Icon file not found (build continues but without icon)
    echo.
    echo Check error messages above for details.
    echo.
    pause
    goto :eof
)

echo.
echo ============================================================================
echo  BUILD SUCCESSFUL!
echo ============================================================================
echo.
echo Output folder: dist\inventarium.dist\
echo Executable:    dist\inventarium.dist\inventarium.exe
echo Icon:          Embedded in .exe
echo.

REM ============================================================================
REM  Post-Build Verification
REM ============================================================================

echo ============================================================================
echo  Verifying Build Contents
echo ============================================================================
echo.

IF EXIST "dist\inventarium.dist\inventarium.exe" (
    echo [OK] inventarium.exe created
) ELSE (
    echo [ERROR] inventarium.exe NOT found!
)

echo.
echo Checking directories:

IF EXIST "dist\inventarium.dist\views" (
    echo [OK] views\ directory
) ELSE (
    echo [ERROR] views\ directory NOT found
)

IF EXIST "dist\inventarium.dist\sql" (
    echo [OK] sql\ directory
) ELSE (
    echo [ERROR] sql\ directory NOT found
)

IF EXIST "dist\inventarium.dist\images" (
    echo [OK] images\ directory
) ELSE (
    echo [WARNING] images\ directory NOT found
)

IF EXIST "dist\inventarium.dist\fonts" (
    echo [OK] fonts\ directory
) ELSE (
    echo [WARNING] fonts\ directory NOT found
)

IF EXIST "dist\inventarium.dist\reports" (
    echo [OK] reports\ directory
) ELSE (
    echo [WARNING] reports\ directory NOT found
)

echo.
echo Checking config files:

IF EXIST "dist\inventarium.dist\label_templates.json" (
    echo [OK] label_templates.json
) ELSE (
    echo [WARNING] label_templates.json NOT found
)

echo.
echo ============================================================================
echo  Build Summary
echo ============================================================================
echo.
echo What's inside dist\inventarium.dist\:
echo  - inventarium.exe         (main executable WITH ICON)
echo  - label_templates.json    (barcode label templates)
echo  - views\                  (GUI windows)
echo  - sql\                    (SQLite database)
echo  - images\                 (application icons)
echo  - fonts\                  (barcode fonts)
echo  - reports\                (report templates)
echo.

REM ============================================================================
REM  Testing Instructions
REM ============================================================================

echo ============================================================================
echo  Next Steps - Testing the Build
echo ============================================================================
echo.
echo 1. TEST LOCALLY:
echo    cd dist\inventarium.dist
echo    inventarium.exe
echo.
echo 2. FIRST RUN:
echo    - A configuration dialog will appear
echo    - Set the database path (local or network)
echo    - Settings are saved in config.ini automatically
echo.
echo 3. DISTRIBUTION:
echo    - Copy entire dist\inventarium.dist\ folder
echo    - Include sql\inventarium.db (or let user select existing)
echo    - First run shows configuration dialog
echo.
echo ============================================================================
echo.

echo BUILD COMPLETE! Ready for testing and distribution.
echo.
pause
