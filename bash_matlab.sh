# exportar variable de entorno al PATH
echo 'export PATH="$PATH:/mnt/c/Program\ Files/MATLAB/R2023a/bin/win64"' >> ~/.bashrc
source ~/.bashrc

# Flujo de trabajo desde wsl

# trabajar desde la terminal -  no muestra imagines, guardar imagines con saveas(gcf, 'nombre.png')
matlab.exe -batch "run('script.m');"

# trabajar desde la terminal -  abre command windows de matlab, imprime imagines

matlab.exe -nodisplay -nosplash -nodesktop -r "run('script.m'); pause(10);exit;"


"MATLAB.installPath": "/mnt/c/'Program Files'/MATLAB/R2023b/bin/matlab.exe"