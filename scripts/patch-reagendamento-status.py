from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="document.getElementById('sucesso-status').textContent=reagendando?'✓ NOVO HORÁRIO CONFIRMADO':solicitado?'⏳ AGUARDANDO CONFIRMAÇÃO DA EQUIPE':'✓ HORÁRIO CONFIRMADO';document.getElementById('sucesso-texto').textContent=`${state.profissional.nome} • ${state.servico.nome} • ${dataPt(state.data)} às ${state.horario}.`;document.getElementById('sucesso-orientacao').textContent=reagendando?'Seu agendamento foi transferido para o novo horário.':solicitado?'Seu pedido foi registrado, mas o horário ainda não está confirmado. A equipe fará a validação do agendamento.':'Seu horário já está confirmado.';"
new="document.getElementById('sucesso-status').textContent=reagendando?(solicitado?'⏳ NOVO HORÁRIO AGUARDANDO CONFIRMAÇÃO':'✓ NOVO HORÁRIO CONFIRMADO'):solicitado?'⏳ AGUARDANDO CONFIRMAÇÃO DA EQUIPE':'✓ HORÁRIO CONFIRMADO';document.getElementById('sucesso-texto').textContent=`${state.profissional.nome} • ${state.servico.nome} • ${dataPt(state.data)} às ${state.horario}.`;document.getElementById('sucesso-orientacao').textContent=reagendando?(solicitado?'Seu agendamento foi transferido para o novo horário e continua aguardando confirmação da equipe.':'Seu agendamento foi transferido para o novo horário e permanece confirmado.'):solicitado?'Seu pedido foi registrado, mas o horário ainda não está confirmado. A equipe fará a validação do agendamento.':'Seu horário já está confirmado.';"
if old not in s:
    raise SystemExit('Trecho alvo não encontrado')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('ok')
