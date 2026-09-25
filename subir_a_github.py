import os, subprocess, sys

def run_cmd(cmd):
    print(f">> {cmd}")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f"[!] Error ejecutando: {cmd}")
        return False
    return True

sync_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(sync_dir)

print("=" * 60)
print("     SUBIR ACTUALIZACION A GITHUB - DEDSAFIO PERUANO")
print("=" * 60)

# 1. Update manifest
print("\n[1/3] Regenerando manifest.json...")
subprocess.run([sys.executable, "actualizar_manifest.py"])

# 2. Check Git repo
git_dir = os.path.join(sync_dir, ".git")
if not os.path.exists(git_dir):
    print("\n[2/3] Inicializando repositorio Git local...")
    run_cmd("git init")
    run_cmd("git branch -M main")
    print("\n" + "-" * 50)
    print("Pega la URL de tu repositorio de GitHub")
    print("Ejemplo: https://github.com/TuUsuario/tu-repo.git")
    print("-" * 50)
    repo_url = input("URL del repositorio: ").strip()
    if repo_url:
        run_cmd(f'git remote add origin "{repo_url}"')
    else:
        print("[!] No ingresaste ninguna URL. Abortando.")
        input("\nPresiona Enter para salir...")
        sys.exit(1)
else:
    print("\n[2/3] Repositorio Git ya configurado.")

# 3. Add, commit, push
print("\n[3/3] Subiendo archivos a GitHub...")
run_cmd("git add .")
subprocess.run('git commit -m "Actualizacion de mods y manifest"', shell=True)
success = run_cmd("git push -u origin main")

print("\n" + "=" * 60)
if success:
    print("  ¡LISTO! Todos los archivos estan en GitHub.")
    print("  Tus amigos ya pueden actualizar abriendo el launcher.")
else:
    print("  [!] Hubo un detalle al hacer push.")
    print("  Asegurate de haber iniciado sesion en Git o verifica la URL.")
print("=" * 60)

input("\nPresiona Enter para salir...")
