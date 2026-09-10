from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_state = "const state={empresa:null,profissional:null,servico:null,data:'',horario:'',nome:'',telefone:'',email:'',whatsappEmpresa:'',reagendamentoId:null,reagendamentoAnterior:null};"
new_state = "const state={empresa:null,profissional:null,servico:null,data:'',horario:'',nome:'',telefone:'',email:'',whatsappEmpresa:'',reagendamentoId:null,reagendamentoAnterior:null,identidadeConfirmadaOutraPessoa:''};"
if old_state not in s:
    raise SystemExit('state alvo nao encontrado')
s = s.replace(old_state, new_state, 1)

pattern = re.compile(r"  function irParaProfissionais\(\)\{.*?\n  async function carregarProfissionais\(\)\{", re.S)
replacement = r'''  async function irParaProfissionais(){
    const nome=document.getElementById('cliente-nome').value.trim(),telefone=document.getElementById('cliente-telefone').value.trim(),email=document.getElementById('cliente-email').value.trim().toLowerCase(),numeros=telefone.replace(/\D/g,'');
    if(nome.length<2){setStatus('status-global','Informe seu nome para continuar.','erro');return}
    if(numeros.length<10||numeros.length>11){setStatus('status-global','Informe um telefone com DDD válido.','erro');return}
    if(email&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){setStatus('status-global','Informe um e-mail válido ou deixe o campo em branco.','erro');return}

    const chaveIdentidade=`${nome.toUpperCase().replace(/\s+/g,' ').trim()}|${numeros}|${email}`;
    setStatus('status-global','Validando seus dados...','info');

    try{
      const{data,error}=await db.rpc('agendamento_publico_validar_identidade',{
        p_slug:slug,
        p_cliente_nome:nome,
        p_telefone:telefone,
        p_email:email||null
      });
      if(error)throw error;

      const registro=Array.isArray(data)?data[0]:data;
      const situacao=String(registro?.situacao||'NOVO').toUpperCase();

      if(situacao==='TELEFONE_EM_USO'&&state.identidadeConfirmadaOutraPessoa!==chaveIdentidade){
        setStatus('status-global');
        const continuar=window.confirm('Este telefone já está associado a outro cadastro nesta empresa.\n\nSe este agendamento é para outra pessoa que utiliza o mesmo telefone, clique em OK.\n\nSe você deseja corrigir o nome, telefone ou e-mail informado, clique em Cancelar.');
        if(!continuar){setStatus('status-global','Revise os dados antes de continuar.','info');return}
        state.identidadeConfirmadaOutraPessoa=chaveIdentidade;
      }else if(situacao!=='TELEFONE_EM_USO'){
        state.identidadeConfirmadaOutraPessoa='';
      }

      Object.assign(state,{nome,telefone,email});
      setStatus('status-global');
      carregarProfissionais();
    }catch(err){
      console.error(err);
      setStatus('status-global',err?.message||'Não foi possível validar seus dados. Tente novamente.','erro');
    }
  }
  async function carregarProfissionais(){'''

s2, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit(f'funcao irParaProfissionais nao encontrada: {n}')

p.write_text(s2, encoding='utf-8')
print('patch aplicado')
