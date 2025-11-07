@echo off
echo ================================
echo  PSUR Generator System
echo ================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

echo.
echo Environment activated. Ready to generate PSUR sections.
echo.
echo Available commands:
echo   cd section_c ^& python c.py        - Generate Section C (Sales ^& Population)
echo   cd section_d ^& python psur_section_d_generator.py - Generate Section D (Serious Incidents)
echo   cd section_f ^& python psur_section_f_generator.py - Generate Section F (Performance/Safety)
echo   cd section_g ^& python g.py        - Generate Section G (Complaints/Trends)
echo   cd section_j ^& python j.py        - Generate Section J (Literature Review)
echo   cd section_k ^& python k.py        - Generate Section K (Marketed vs Evaluated)
echo   cd section_l ^& python l.py        - Generate Section L (Clinical Data)
echo   cd section_m ^& python m.py        - Generate Section M (Risk-Benefit)
echo.
echo ================================
echo.

cmd /k

