import os, hashlib, json

sync_dir = os.path.dirname(os.path.abspath(__file__))
manifest_path = os.path.join(sync_dir, 'manifest.json')
whitelist_path = os.path.join(os.path.dirname(sync_dir), 'whitelist.json')

def get_sha1(filepath):
    h = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

files_manifest = []

for category in ['mods', 'animations', 'config']:
    cat_dir = os.path.join(sync_dir, category)
    if os.path.exists(cat_dir):
        for root, dirs, files in os.walk(cat_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, sync_dir).replace('\\', '/')
                files_manifest.append({
                    'path': rel_path,
                    'size': os.path.getsize(full_path),
                    'sha1': get_sha1(full_path)
                })

whitelist = []
if os.path.exists(whitelist_path):
    try:
        with open(whitelist_path, 'r', encoding='utf-8') as f:
            whitelist = json.load(f)
    except Exception:
        pass

manifest_data = {
    'version': '1.0.0',
    'gameVersion': '1.21.1',
    'loaderVersion': '0.16.10',
    'totalFiles': len(files_manifest),
    'files': files_manifest,
    'whitelist': whitelist
}

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest_data, f, indent=2)

print(f'[OK] Manifiesto actualizado exitosamente!')
print(f'Total de archivos sincronizables: {len(files_manifest)}')
print(f'Jugadores en Whitelist: {len(whitelist)}')
