#====================================================================================================
#!/bin/bash
# Instalação Automática via Script
#
#Data: 14/04/2026
#====================================================================================================

echo "=========================================="
echo "  Instalando Dependências do MarcatiliApp"
echo "=========================================="

# Atualiza os repositórios
echo "📦 Atualizando repositórios..."
sudo apt update

# Instala dependências do sistema
echo "📦 Instalando dependências do sistema..."
sudo apt install -y python3-pip python3-tk python3-dev
sudo apt install -y libfreetype6-dev libpng-dev libjpeg-dev

# Instala dependências Python
echo "📦 Instalando numpy..."
pip3 install --user numpy

echo "📦 Instalando matplotlib..."
pip3 install --user matplotlib

echo "📦 Instalando PyInstaller..."
pip3 install --user pyinstaller

echo "=========================================="
echo "  ✅ Instalação concluída!"
echo "=========================================="

# Verifica instalação
echo ""
echo "Verificando instalação:"
python3 -c "import numpy; print('numpy:', numpy.__version__)"
python3 -c "import matplotlib; print('matplotlib:', matplotlib.__version__)"
python3 -c "import PyInstaller; print('PyInstaller:', PyInstaller.__version__)"