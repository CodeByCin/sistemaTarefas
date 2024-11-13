from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FloatField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from sistematarefas.models import Tarefas


class FormCriarTarefas(FlaskForm):
   
    nome_tarefa = StringField('Adicione sua tarefa', validators=[DataRequired(message='Por favor, insira um nome válido.')], render_kw={"placeholder": "Exemplo: 'Ir à academia', 'Fazer compras no supermercado'"})
    custo = FloatField('Custo', validators=[DataRequired(message='Por favor, insira um valor numérico.'), NumberRange(min=0, message='O custo deve ser um valor positivo.')], render_kw={"placeholder": "R$ 00,00"})
    data_limite = DateField('Data Limite', validators=[DataRequired(message='Por favor, insira uma data válida.')], format='%Y-%m-%d')
    botao_submit = SubmitField('Feito!')


    def validate_custo(form, field):
        if field.data < 0:
            raise ValidationError('Insira outro valor e tente novamente.')
                
    def validate_nome_tarefa(self, nome_tarefa):
        tarefa_existente = Tarefas.query.filter_by(nome_tarefa=nome_tarefa.data).first()
        if tarefa_existente:
            raise ValidationError('O nome que você está tentando utilizar já está em uso. Tente outro nome.')


