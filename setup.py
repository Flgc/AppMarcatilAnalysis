#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================================================
setup.py - Script de configuração para compilar o Marcatili Analyzer no Linux Mint

Este script verifica dependências e configura o ambiente para compilação
com PyInstaller, otimizado para distribuições Linux baseadas em Debian/Ubuntu.

Uso:
    python3 setup.py          # Modo interativo
    python3 setup.py --build  # Compilar diretamente
    python3 setup.py --clean  # Limpar arquivos temporários

Data: 13/04/2026
====================================================================================================        
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

# Configurações do projeto
PROJECT_NAME = "MarcatiliAnalyzer"
PROJECT_VERSION = "1.0.0"
PROJECT_AUTHOR = "Marcatili Analyzer Team"
PROJECT_DESCRIPTION = "Análise de Guias de Onda Ópticos pelo Método de Marcatili"

# Cores para output no terminal
class Colors:
    """Cores ANSI para output no terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Imprime cabeçalho formatado"""
    print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """Imprime mensagem de erro"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    """Imprime mensagem de aviso"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    """Imprime mensagem informativa"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

def check_python_version():
    """Verifica a versão do Python"""
    print_info("Verificando versão do Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} - Versão muito antiga. Necessário Python 3.8+")
        return False

def check_dependencies():
    """Verifica e instala dependências necessárias"""
    print_info("Verificando dependências...")
    
    dependencies = {
        'numpy': 'numpy',
        'matplotlib': 'matplotlib',
        'PyInstaller': 'pyinstaller'
    }
    
    missing = []
    
    for module, package in dependencies.items():
        try:
            __import__(module.lower())
            print_success(f"{module} - OK")
        except ImportError:
            print_warning(f"{module} - NÃO INSTALADO")
            missing.append(package)
    
    if missing:
        print_info(f"\nInstalando dependências faltantes: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user"] + missing)
            print_success("Todas as dependências instaladas com sucesso!")
        except subprocess.CalledProcessError as e:
            print_error(f"Erro ao instalar dependências: {e}")
            return False
    
    return True

def check_system_requirements():
    """Verifica requisitos do sistema Linux Mint"""
    print_info("Verificando requisitos do sistema...")
    
    # Verifica sistema operacional
    system = platform.system()
    if system != "Linux":
        print_warning(f"Sistema: {system} (recomendado Linux)")
    else:
        print_success(f"Sistema: {system}")
    
    # Verifica distribuição
    try:
        with open('/etc/os-release', 'r') as f:
            os_info = f.read()
        if 'Linux Mint' in os_info or 'Ubuntu' in os_info:
            print_success("Distribuição compatível com Linux Mint/Ubuntu")
        else:
            print_warning("Distribuição não totalmente testada, mas pode funcionar")
    except:
        print_warning("Não foi possível identificar a distribuição")
    
    # Verifica memória disponível
    try:
        import psutil
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)
        if available_gb > 1:
            print_success(f"Memória disponível: {available_gb:.1f} GB")
        else:
            print_warning(f"Memória disponível: {available_gb:.1f} GB (recomendado > 1GB)")
    except ImportError:
        print_info("psutil não instalado - pulando verificação de memória")
    
    # Verifica espaço em disco
    try:
        stat = shutil.disk_usage(Path.home())
        free_gb = stat.free / (1024**3)
        if free_gb > 1:
            print_success(f"Espaço em disco disponível: {free_gb:.1f} GB")
        else:
            print_warning(f"Espaço em disco disponível: {free_gb:.1f} GB (recomendado > 1GB)")
    except:
        print_warning("Não foi possível verificar espaço em disco")
    
    return True

def create_spec_file():
    """Cria arquivo .spec para o PyInstaller"""
    print_info("Criando arquivo .spec para PyInstaller...")
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
"""
Arquivo de especificação do PyInstaller para {PROJECT_NAME}
Gerado automaticamente em Linux Mint
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Nome do executável
name = '{PROJECT_NAME}'

# Arquivo principal
main_script = 'main.py'

# Análise
a = Analysis(
    [main_script],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'numpy',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'tkinter',
        'PIL',
        'pkg_resources'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)

# Pyz (bytecode comprimido)
pyz = PYZ(a.pure)

# Executável
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,      # Modo GUI (sem console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)

# Configurações adicionais para Linux
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=name
)

# Adiciona informações de versão (opcional)
version_info = {{
    'version': '{PROJECT_VERSION}',
    'description': '{PROJECT_DESCRIPTION}',
    'author': '{PROJECT_AUTHOR}',
    'name': '{PROJECT_NAME}'
}}
'''
    
    spec_path = Path.cwd() / f"{PROJECT_NAME}.spec"
    with open(spec_path, 'w') as f:
        f.write(spec_content)
    
    print_success(f"Arquivo .spec criado: {spec_path}")
    return spec_path

def compile_with_pyinstaller(use_spec=True, onefile=True):
    """Compila o projeto com PyInstaller"""
    print_info("Iniciando compilação com PyInstaller...")
    
    # Limpa builds anteriores
    clean_build()
    
    # Prepara comando
    cmd = [sys.executable, "-m", "PyInstaller"]
    
    if use_spec and Path(f"{PROJECT_NAME}.spec").exists():
        cmd.append(f"{PROJECT_NAME}.spec")
    else:
        # Configurações básicas
        cmd.append("--name")
        cmd.append(PROJECT_NAME)
        
        # Para Linux Mint, usar console=False para aplicação GUI
        cmd.append("--windowed")
        
        if onefile:
            cmd.append("--onefile")
        else:
            cmd.append("--onedir")
        
        # Otimizações
        cmd.append("--strip")          # Remove símbolos de debug
        cmd.append("--noconfirm")      # Sobrescreve sem perguntar
        
        # Adiciona data (se houver)
        # cmd.append("--add-data")
        # cmd.append("assets:assets")
        
        # Arquivo principal
        cmd.append("main.py")
    
    print_info(f"Comando: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print_success("Compilação concluída com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Erro na compilação: {e}")
        return False

def clean_build():
    """Limpa arquivos temporários e builds anteriores"""
    print_info("Limpando arquivos temporários...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec', '*.pyc']
    
    for dir_name in dirs_to_clean:
        path = Path.cwd() / dir_name
        if path.exists():
            shutil.rmtree(path)
            print_success(f"Removido: {dir_name}/")
    
    for pattern in files_to_clean:
        for file in Path.cwd().glob(pattern):
            file.unlink()
            print_success(f"Removido: {file.name}")
    
    # Limpa __pycache__ em subdiretórios
    for pycache in Path.cwd().rglob('__pycache__'):
        shutil.rmtree(pycache)
        print_success(f"Removido: {pycache}")
    
    print_success("Limpeza concluída!")

def create_desktop_entry():
    """Cria entrada no menu do Linux Mint (.desktop)"""
    print_info("Criando entrada no menu...")
    
    desktop_content = f"""[Desktop Entry]
Version={PROJECT_VERSION}
Name={PROJECT_NAME}
Comment={PROJECT_DESCRIPTION}
Exec={Path.cwd()}/dist/{PROJECT_NAME}
Icon={Path.cwd()}/icon.png
Terminal=false
Type=Application
Categories=Science;Education;Graphics;
StartupNotify=true
"""
    
    desktop_path = Path.home() / ".local/share/applications" / f"{PROJECT_NAME}.desktop"
    desktop_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(desktop_path, 'w') as f:
        f.write(desktop_content)
    
    # Torna executável
    desktop_path.chmod(0o755)
    print_success(f"Entrada de menu criada: {desktop_path}")

def print_instructions():
    """Imprime instruções de uso"""
    print_header("INSTRUÇÕES")
    
    executable_path = Path.cwd() / "dist" / PROJECT_NAME
    
    print(f"""
Para executar o programa:

1. Pelo terminal:
   {Colors.GREEN}{executable_path}{Colors.ENDC}

2. Pelo menu (se criado):
   Menu > {PROJECT_NAME}

3. Duplo clique no arquivo:
   {Colors.CYAN}{executable_path}{Colors.ENDC}

Para executar a partir do código fonte:
   {Colors.BLUE}python3 main.py{Colors.ENDC}

Para recompilar:
   {Colors.BLUE}python3 setup.py --build{Colors.ENDC}

Para limpar arquivos:
   {Colors.BLUE}python3 setup.py --clean{Colors.ENDC}
""")

def main():
    """Função principal"""
    print_header(f"{PROJECT_NAME} - Setup para Linux Mint")
    
    # Parsing de argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == '--clean':
            clean_build()
            return
        elif sys.argv[1] == '--build':
            # Pula verificação interativa
            pass
        elif sys.argv[1] == '--help':
            print("Uso: python3 setup.py [opções]")
            print("\nOpções:")
            print("  --build    Compila o aplicativo")
            print("  --clean    Limpa arquivos temporários")
            print("  --help     Mostra esta ajuda")
            return
    
    # Verificações
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_system_requirements():
        print_warning("Algumas verificações falharam, mas continuando...")
    
    # Menu interativo
    print_header("OPÇÕES DE COMPILAÇÃO")
    print("1. Compilar com PyInstaller (recomendado)")
    print("2. Criar apenas arquivo .spec")
    print("3. Compilar e criar entrada no menu")
    print("4. Limpar arquivos temporários")
    print("5. Sair")
    
    choice = input(f"\n{Colors.BOLD}Escolha uma opção [1-5]: {Colors.ENDC}").strip()
    
    if choice == '1':
        if compile_with_pyinstaller(use_spec=False, onefile=True):
            print_success(f"Executável criado em: {Path.cwd()}/dist/{PROJECT_NAME}")
            print_instructions()
    
    elif choice == '2':
        create_spec_file()
    
    elif choice == '3':
        if compile_with_pyinstaller(use_spec=False, onefile=True):
            create_desktop_entry()
            print_instructions()
    
    elif choice == '4':
        clean_build()
    
    elif choice == '5':
        print_info("Saindo...")
        sys.exit(0)
    
    else:
        print_error("Opção inválida!")

if __name__ == "__main__":
    main()