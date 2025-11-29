"""
Verification Script for Arabic Sentiment Analysis Dashboard
Checks all dependencies and configuration before running the app.
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Verify Python version is 3.8+"""
    print("\n" + "="*60)
    print("1️⃣  CHECKING PYTHON VERSION")
    print("="*60)
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8+ required")
        return False
    return True


def check_dependencies():
    """Verify all required packages are installed"""
    print("\n" + "="*60)
    print("2️⃣  CHECKING DEPENDENCIES")
    print("="*60)
    
    required_packages = {
        'streamlit': 'Streamlit Web Framework',
        'pandas': 'Data Processing',
        'transformers': 'Hugging Face Transformers',
        'torch': 'PyTorch (ML Framework)',
        'openpyxl': 'Excel Export',
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            version = __import__(package).__version__ if hasattr(__import__(package), '__version__') else 'installed'
            print(f"✓ {package:<20} ({description:<25}) - v{version}")
        except ImportError:
            print(f"❌ {package:<20} ({description:<25}) - NOT INSTALLED")
            all_installed = False
    
    return all_installed


def check_local_modules():
    """Verify local module files exist"""
    print("\n" + "="*60)
    print("3️⃣  CHECKING LOCAL MODULES")
    print("="*60)
    
    required_files = {
        'analyzer.py': 'Sentiment Analysis Engine',
        'scraper.py': 'Social Media Scraper',
        'app.py': 'Streamlit Application',
    }
    
    all_exist = True
    for file, description in required_files.items():
        path = Path(file)
        if path.exists():
            size = path.stat().st_size
            print(f"✓ {file:<20} ({description:<25}) - {size:,} bytes")
        else:
            print(f"❌ {file:<20} ({description:<25}) - NOT FOUND")
            all_exist = False
    
    return all_exist


def check_model_directory():
    """Verify model directory exists and contains required files"""
    print("\n" + "="*60)
    print("4️⃣  CHECKING MODEL DIRECTORY")
    print("="*60)
    
    model_path = Path("./my_final_expert_model_v3")
    
    if not model_path.exists():
        print(f"❌ Model directory not found at: {model_path.absolute()}")
        print(f"   Expected location: {Path.cwd() / model_path}")
        return False
    
    print(f"✓ Model directory found at: {model_path.absolute()}")
    
    required_files = [
        'config.json',
        'model.safetensors',
        'tokenizer.json',
        'special_tokens_map.json',
        'tokenizer_config.json',
        'vocab.txt'
    ]
    
    found_files = list(model_path.glob('*'))
    print(f"\n  Files in model directory ({len(found_files)} total):")
    
    all_required_found = True
    for required_file in required_files:
        if (model_path / required_file).exists():
            size = (model_path / required_file).stat().st_size
            print(f"  ✓ {required_file:<30} - {size:,} bytes")
        else:
            print(f"  ❌ {required_file:<30} - MISSING")
            all_required_found = False
    
    return all_required_found


def check_permissions():
    """Verify file permissions"""
    print("\n" + "="*60)
    print("5️⃣  CHECKING FILE PERMISSIONS")
    print("="*60)
    
    files_to_check = ['analyzer.py', 'scraper.py', 'app.py']
    all_readable = True
    
    for file in files_to_check:
        path = Path(file)
        if path.exists():
            if os.access(path, os.R_OK):
                print(f"✓ {file} - Readable")
            else:
                print(f"❌ {file} - NOT READABLE")
                all_readable = False
        else:
            print(f"⚠ {file} - File not found")
    
    return all_readable


def main():
    """Run all checks"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🔍 ARABIC SENTIMENT ANALYZER - VERIFICATION SCRIPT  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Local Modules", check_local_modules),
        ("Model Directory", check_model_directory),
        ("File Permissions", check_permissions),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n❌ Error during {check_name}: {str(e)}")
            results[check_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 VERIFICATION SUMMARY")
    print("="*60)
    
    for check_name, passed in results.items():
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("\n🚀 Ready to launch:")
        print("   Run: python -u -m streamlit run app.py")
        print("\n📍 Access at: http://localhost:8501")
        print("="*60)
        return 0
    else:
        print("❌ SOME CHECKS FAILED!")
        print("\n📋 To fix issues:")
        print("   1. Install missing dependencies:")
        print("      pip install -r requirements.txt")
        print("   2. Verify model directory exists")
        print("   3. Ensure all .py files are present")
        print("="*60)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
