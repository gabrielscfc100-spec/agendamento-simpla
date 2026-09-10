from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = "  const params=new URLSearchParams(window.location.search);\n  const slug=(params.get('empresa')||params.get('slug')||'simpla-barbearia').trim().toLowerCase();"
new = "  const params=new URLSearchParams(window.location.search);\n  const pathSlug=decodeURIComponent(window.location.pathname.split('/').filter(Boolean).pop()||'').trim().toLowerCase();\n  const slug=(params.get('empresa')||params.get('slug')||pathSlug||'simpla-barbearia').trim().toLowerCase();"
if old not in s:
    raise SystemExit('Trecho esperado não encontrado em index.html')
p.write_text(s.replace(old, new, 1), encoding='utf-8')
