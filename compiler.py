import sys
import os
import subprocess
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from codegen import CodeGenerator

def compile_boso_jowo(source_file):
    if not source_file.endswith('.jowo'):
        print("Error: File harus berekstensi .jowo")
        sys.exit(1)

    with open(source_file, 'r') as f:
        source_code = f.read()

    print(f"[*] Mengkompilasi {source_file}...")

    # 1. Lexical Analysis
    print("[1/6] Lexical Analysis...")
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    # 2. Parsing (Syntax Analysis)
    print("[2/6] Parsing (Syntax Analysis)...")
    parser = Parser(tokens)
    ast = parser.parse()

    # 3. Semantic Analysis
    print("[3/6] Semantic Analysis...")
    semantic = SemanticAnalyzer()
    semantic.analyze(ast)

    # 4. Code Optimization
    print("[4/6] Code Optimization...")
    optimizer = Optimizer()
    optimized_ast = optimizer.optimize(ast)

    # 5. Code Generation
    print("[5/6] Code Generation...")
    codegen = CodeGenerator()
    codegen.generate(optimized_ast)
    python_code = codegen.get_code()
    
    # Simpan hasil generate ke file python sementara
    base_name = os.path.splitext(os.path.basename(source_file))[0]
    out_py_file = f"{base_name}_generated.py"
    with open(out_py_file, 'w') as f:
        f.write(python_code)
    
    print(f"[+] File Python dihasilkan: {out_py_file}")

    # 6. Membuat Installer/Executable
    print("[6/6] Membuat Executable menggunakan PyInstaller...")
    try:
        # Menggunakan pyinstaller dengan flag --onefile untuk menjadikannya satu executable mandiri
        subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", out_py_file], check=True)
        print(f"\n[SUKSES] Kompilasi selesai! File .exe dapat ditemukan di folder 'dist'.")
    except subprocess.CalledProcessError as e:
        print(f"\n[GAGAL] Gagal membuat executable. Pastikan PyInstaller sudah terinstall (pip install pyinstaller).")
        sys.exit(1)
    except FileNotFoundError:
        print(f"\n[GAGAL] PyInstaller tidak ditemukan. Silakan install dengan: pip install pyinstaller")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Penggunaan: python compiler.py <file_sumber.jowo>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    compile_boso_jowo(source_file)
