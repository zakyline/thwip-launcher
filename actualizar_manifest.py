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

EXTERNAL_URLS = {
    'mods/watermedia_binaries-3.0.0.6.jar': 'https://cdn.modrinth.com/data/4997XcoK/versions/fYWsOuBz/watermedia_binaries-3.0.0.6.jar'
}

files_manifest = []

# Carpetas sincronizables
for category in ['mods', 'config', 'animations', 'fancymenu_data', 'resourcepacks', 'mystique']:
    cat_dir = os.path.join(sync_dir, category)
    if os.path.exists(cat_dir):
        for root, dirs, files in os.walk(cat_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, sync_dir).replace('\\', '/')
                item_data = {
                    'path': rel_path,
                    'size': os.path.getsize(full_path),
                    'sha1': get_sha1(full_path)
                }
                if rel_path in EXTERNAL_URLS:
                    item_data['url'] = EXTERNAL_URLS[rel_path]
                files_manifest.append(item_data)

# Archivos de raiz sincronizables
for root_file in ['servers.dat', 'options.txt']:
    full_path = os.path.join(sync_dir, root_file)
    if os.path.exists(full_path):
        rel_path = root_file
        item_data = {
            'path': rel_path,
            'size': os.path.getsize(full_path),
            'sha1': get_sha1(full_path)
        }
        files_manifest.append(item_data)

whitelist = []
if os.path.exists(whitelist_path):
    try:
        with open(whitelist_path, 'r', encoding='utf-8') as f:
            whitelist = json.load(f)
    except Exception:
        pass

manifest_data = {
    'version': (json.load(open(manifest_path, 'r', encoding='utf-8')).get('version', '1.0.9') if os.path.exists(manifest_path) else '1.0.9'),
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
