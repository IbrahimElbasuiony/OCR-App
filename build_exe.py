import os
import shutil
from pathlib import Path
import subprocess
import platform

def create_build_script():
    # Create spec file content
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('src', 'src')],  # Only include src directory, .env will be handled separately
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='YourApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='x86_64',  # Specifically target 64-bit
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='YourApp',
)
"""
    
    # Write spec file
    with open('build.spec', 'w') as f:
        f.write(spec_content)

def create_env_template():
    """Create a template .env file without sensitive data"""
    env_template_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here
MODEL_NAME = "your model name"

# Instructions:
# 1. Rename this file to .env
# 2. Replace 'your_api_key_here' with your actual OpenAI API key
# 3. Make sure this .env file is in the same folder as the executable
# make sure to put the API key inside ""
# example :
    # OPENAI_API_KEY = "1234"
    # MODEL_NAME = "gpt-4o"
"""
    with open('.env.template', 'w') as f:
        f.write(env_template_content)

def create_readme():
    """Create a README with instructions"""
    readme_content = """# Application Instructions

## System Requirements
- Windows 64-bit operating system
- Python 3.7 or higher (64-bit version)

## For Users
1. Before running the application:
   - Find the .env.template file in the application folder
   - Rename it to .env
   - Open it with a text editor
   - Replace 'your_api_key_here' with your OpenAI API key
   - Replace 'your model' with the openai model
   - Save and close the file

2. Run YourApp.exe

Important:
- Keep your API key secret
- Never share your .env file
- The application will look for the .env file in the same folder as the executable

## For Developers
1. Install required packages:
   ```
   pip install pyinstaller python-dotenv
   ```

2. Build the executable:
   ```
   python build_exe.py
   ```

Note: This application is built for 64-bit Windows systems only.
"""
    with open('README.md', 'w') as f:
        f.write(readme_content)

def check_system_compatibility():
    """Check if the build environment is compatible"""
    if platform.system() != 'Windows':
        print("Warning: Building on a non-Windows system may cause compatibility issues")
    
    if platform.architecture()[0] != '64bit':
        raise RuntimeError("Error: You must use 64-bit Python to build a 64-bit executable")

def main():
    # Check system compatibility
    check_system_compatibility()
    
    # Create necessary files
    create_build_script()
    create_env_template()
    create_readme()
    
    # Run PyInstaller
    if os.environ.get('VIRTUAL_ENV'):
        venv_python = Path(os.environ['VIRTUAL_ENV'])
        if os.name == 'nt':  # Windows
            python_path = venv_python / 'Scripts' / 'python.exe'
        else:  # Unix-like
            python_path = venv_python / 'bin' / 'python'
    else:
        python_path = 'python'
    
    subprocess.run([str(python_path), '-m', 'PyInstaller', 'build.spec'], check=True)
    
    # Create dist directory if it doesn't exist
    os.makedirs('dist/YourApp', exist_ok=True)
    
    # Copy .env.template to dist directory
    shutil.copy2('.env.template', 'dist/YourApp/.env.template')
    
    print("\nBuild completed! Check the 'dist/YourApp' directory for your executable.")
    print("\nImportant notes:")
    print("1. Your current .env file with the actual API key is NOT included in the build")
    print("2. Users will need to create their own .env file using the template")
    print("3. Make sure to distribute the README.md file with instructions")
    print("4. The executable is built for 64-bit Windows systems only")

if __name__ == '__main__':
    main()