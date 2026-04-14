#====================================================================================================
#!/bin/bash
# setup_venv.sh - Configura ambiente virtual automaticamente
#
#Data: 14/04/2026
#====================================================================================================

echo "=========================================="
echo "  Configurando Ambiente Virtual"
echo "=========================================="

# Nome do ambiente virtual
VENV_NAME="marcatili_env"
echo ""
echo "✅ Ambiente virtual criado com sucesso!"
echo ""
echo "Para usar:"
echo "  source $VENV_NAME/bin/activate"
echo "  python3 main.py"
echo ""
echo "Para sair:"
echo "  deactivate"

python3 -m venv marcatili_env
source marcatili_env/bin/activate
python3 main.py
deactivate
