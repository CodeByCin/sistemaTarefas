from sistematarefas.models import Tarefas
from flask import render_template, redirect, url_for, flash, request
from sistematarefas import app, database
from sistematarefas.forms import FormCriarTarefas
from datetime import datetime


@app.route('/')
def homePage():
    tarefas = Tarefas.query.all()
    return render_template('index.html', tarefas=tarefas)

@app.route('/tarefas', methods=['GET', 'POST'])
def criarTarefa():
    formTarefas = FormCriarTarefas() 
    if request.method == 'POST':
        if formTarefas.validate_on_submit():
            tarefa = Tarefas(
                nome_tarefa=formTarefas.nome_tarefa.data,
                custo=formTarefas.custo.data,
                data_limite=formTarefas.data_limite.data
            )
        try:
            database.session.add(tarefa)
            database.session.commit()
            flash('Tarefa adicionada com sucesso!', 'alert-success')
            return redirect(url_for('homePage'))
        except Exception as e:
            database.session.rollback()
            flash('Ocorreu um erro ao adicionar a tarefa. Tente novamente!', 'alert-danger')
            print(f'Erro da exceção: {e}')
    return render_template('tarefas.html', formTarefas=formTarefas)



@app.route('/deletar/<int:id>', methods=['GET', 'POST'])
def excluirTarefa(id):  
    tarefa_excluir = Tarefas.query.get_or_404(id)
    database.session.delete(tarefa_excluir)
    database.session.commit()
    flash('Tarefa removida com sucesso!', 'alert-warning')
    return redirect(url_for('homePage'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    tarefa = Tarefas.query.get_or_404(id)
    if request.method == 'POST':
        novo_nome_tarefa = request.form['nome']
        if Tarefas.query.filter(Tarefas.nome_tarefa == novo_nome_tarefa ,Tarefas.id != id).first():
            flash('Já existe uma tarefa com esse nome. Por favor, escolha outro.', 'alert-danger')
            return redirect(url_for('homePage', id=id))
        
        tarefa.nome_tarefa = novo_nome_tarefa
        tarefa.custo = request.form['custo']
        tarefa.data_limite = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        try:
            database.session.commit()
            flash('Tarefa alterada com sucesso!', 'alert-warning')
        except Exception as e:
            database.session.rollback()
            flash('Ocorreu um erro ao adicionar a tarefa. Tente novamente!', 'alert-danger')
            print(f'Erro da exceção: {e}')
        return redirect(url_for('homePage', id=id))
    
    tarefas = Tarefas.query.all()
    flash('Erro: A página de adição não foi encontrada.', 'alert-danger')
    return render_template('index.html', tarefas=tarefas)

    
        


    





        
    