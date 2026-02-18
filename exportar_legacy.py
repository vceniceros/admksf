import subprocess
import os

# CONFIGURACIÓN:
# ---------------------------------------------------------
OUTPUT_FILE = "historial_completo_proyecto.md"
DIAS_ATRAS = 7 # 10 años -> Básicamente todo el historial
# Extensiones a ignorar (Archivos que no aportan lógica de negocio)
EXCLUDE_EXTENSIONS = [
    '.json', '.lock', '.png', '.jpg', '.svg', '.map', 
    '.csv', '.txt', '.md', '.pyc', '.gitignore'
]
# ---------------------------------------------------------

def run_git_command(command):
    try:
        # encoding='utf-8' y errors='ignore' son clave para no romper con tildes o emojis
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8', errors='ignore').strip()
    except subprocess.CalledProcessError as e:
        return ""

def generate_markdown():
    print(f"--- Iniciando extracción de historial ({DIAS_ATRAS} días) ---")
    
    # Obtener hashes desde hace X días hasta hoy
    cmd_hashes = f'git log --since="{DIAS_ATRAS} days ago" --format="%H" --reverse' # --reverse para cronología real
    hashes = run_git_command(cmd_hashes).split('\n')
    
    if not hashes or hashes == ['']:
        print("No se encontraron commits. ¿Tienes git iniciado en esta carpeta?")
        return

    total = len(hashes)
    print(f"Se encontraron {total} commits para procesar.")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# Documentación Viva del Proyecto (Basada en Git Log)\n")
        f.write(f"> Generado automáticamente para análisis de IA.\n\n")

        for i, commit_hash in enumerate(hashes):
            # Barra de progreso simple en consola
            if i % 10 == 0: print(f"Procesando commit {i+1}/{total}...")

            # Metadatos
            info = run_git_command(f'git show -s --format="## Commit: %h%n**Fecha:** %ad%n**Mensaje:** %s" {commit_hash}')
            f.write(info + "\n\n")
            
            # Archivos modificados en este commit
            files_changed = run_git_command(f'git show --name-only --format="" {commit_hash}').split('\n')
            
            for file_path in files_changed:
                if not file_path: continue
                
                # Filtro de extensiones
                _, ext = os.path.splitext(file_path)
                if ext in EXCLUDE_EXTENSIONS:
                    continue
                
                # Obtener el diff limpio
                diff = run_git_command(f'git show {commit_hash} -- "{file_path}"')
                
                # Limpieza de ruido del diff header
                lines = diff.split('\n')
                clean_diff = []
                for line in lines:
                    if line.startswith('index ') or line.startswith('diff --git'):
                        continue
                    clean_diff.append(line)
                
                diff_text = "\n".join(clean_diff)

                if diff_text:
                    f.write(f"#### 📄 `{file_path}`\n")
                    f.write("```python\n") # Forzamos python por defecto para coloreado genérico
                    f.write(diff_text[:4000]) # Límite por archivo para no explotar
                    if len(diff_text) > 4000:
                        f.write("\n... (truncado) ...")
                    f.write("\n```\n\n")
            
            f.write("---\n")

    print(f"✅ ¡Éxito! Archivo generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_markdown()