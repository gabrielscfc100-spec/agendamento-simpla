from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = "function sairPortal(mostrarTela=true){['simpla_portal_empresa_id','simpla_portal_token','simpla_portal_expira_em','simpla_portal_cliente'].forEach(k=>sessionStorage.removeItem(k));portalState.selecaoToken=null;if(mostrarTela)reiniciarPortal()}"
new = "async function sairPortal(mostrarTela=true){const token=sessionStorage.getItem('simpla_portal_token');const empresaId=sessionStorage.getItem('simpla_portal_empresa_id')||state.empresa?.id;try{if(token&&empresaId)await chamarFuncaoPortal('portal-sair',{empresa_id:empresaId,token})}catch(err){console.warn('Não foi possível revogar a sessão no servidor.',err)}finally{['simpla_portal_empresa_id','simpla_portal_token','simpla_portal_expira_em','simpla_portal_cliente'].forEach(k=>sessionStorage.removeItem(k));portalState.selecaoToken=null;if(mostrarTela)reiniciarPortal()}}"

if old not in s:
    raise SystemExit('funcao sairPortal alvo nao encontrada')

s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('logout do portal atualizado')
