@echo off
echo Starting...

cd ..
cd ..

rem Create a virtual environment
python -m venv JigglyConnect

rem Activate the virtual environment
call JigglyConnect\Scripts\activate.bat

rem Install dependencies
pip install -r setup/win/requirements.txt

pip install --upgrade --pre --extra-index-url https://marcelotduarte.github.io/packages/ cx_Freeze

rem Compile the project
python setup/win/setup.py build

rem Navigate to the build directory
cd build
cd exe.win-amd64-3.11

rem Sign all the executables
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool" sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 JigglyConnect.exe
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool" sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 JC-updater.exe

echo Build done!
