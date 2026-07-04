from datetime import date

from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

oauth.register(
    name='suap',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    api_base_url='https://suap.ifrn.edu.br/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://suap.ifrn.edu.br/o/token/',
    authorize_url='https://suap.ifrn.edu.br/o/authorize/',
    fetch_token=lambda: session.get('suap_token')
)


BOLETIM_FIELDS = [
    'codigo_diario',
    'disciplina',
    'segundo_semestre',
    'carga_horaria',
    'carga_horaria_cumprida',
    'numero_faltas',
    'percentual_carga_horaria_frequentada',
    'situacao',
    'quantidade_avaliacoes',
    'nota_etapa_1',
    'nota_etapa_2',
    'nota_etapa_3',
    'nota_etapa_4',
    'media_disciplina',
    'nota_avaliacao_final',
    'media_final_disciplina',
]


def get_user_data():
    return oauth.suap.get('rh/meus-dados').json()


def get_student_data():
    response = oauth.suap.get('ensino/meus-dados-aluno/')
    return response.json() if response.status_code == 200 else {}


def get_paginated_results(endpoint):
    results = []
    page = 1

    while page <= 20:
        response = oauth.suap.get(endpoint, params={'page': page})

        if response.status_code != 200:
            return results, response.status_code

        data = response.json()

        if not isinstance(data, dict):
            return data if isinstance(data, list) else [], None

        results.extend(data.get('results', []))

        if not data.get('next'):
            break

        page += 1

    return results, None


def get_periodos_letivos():
    periodos, erro = get_paginated_results('ensino/meus-periodos-letivos/')
    periodos = [periodo for periodo in periodos if isinstance(periodo, dict)]

    periodos.sort(
        key=lambda periodo: (
            periodo.get('ano_letivo', 0),
            periodo.get('periodo_letivo', 0)
        ),
        reverse=True
    )

    return periodos, erro


def get_boletim_fields(disciplinas):
    campos = [field for field in BOLETIM_FIELDS if any(field in item for item in disciplinas)]

    for disciplina in disciplinas:
        for campo in disciplina:
            if campo not in campos:
                campos.append(campo)

    return campos


def get_periodos_by_ano(periodos_letivos, ano_letivo):
    return sorted(
        {
            periodo['periodo_letivo']
            for periodo in periodos_letivos
            if periodo.get('ano_letivo') == ano_letivo and periodo.get('periodo_letivo')
        },
        reverse=True
    )


@app.template_filter('format_value')
def format_value(value):
    if value is None or value == '':
        return '-'

    if isinstance(value, bool):
        return 'Sim' if value else 'Nao'

    if isinstance(value, dict):
        parts = []

        for key, content in value.items():
            label = key.replace('_', ' ').title()
            content = '-' if content is None or content == '' else content
            parts.append(f'{label}: {content}')

        return ' | '.join(parts) or '-'

    if isinstance(value, (list, tuple, set)):
        return ', '.join(str(item) for item in value) or '-'

    return value


@app.route('/')
def index():
    if 'suap_token' in session:
        return render_template(
            'user.html',
            user_data=get_user_data(),
            student_data=get_student_data()
        )
    else:
        return render_template('index.html')


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    print(redirect_uri)
    return oauth.suap.authorize_redirect(redirect_uri)


@app.route('/logout')
def logout():
    session.pop('suap_token', None)
    return redirect(url_for('index'))


@app.route('/perfil')
def perfil():
    if 'suap_token' not in session:
        return redirect(url_for('index'))

    return render_template(
        'user.html',
        user_data=get_user_data(),
        student_data=get_student_data()
    )


@app.route('/boletim')
def boletim():
    if 'suap_token' not in session:
        return redirect(url_for('index'))

    user_data = get_user_data()
    periodos_letivos, erro_periodos = get_periodos_letivos()
    ano_query = request.args.get('ano', type=int)
    periodo_query = request.args.get('periodo', type=int)

    if ano_query:
        ano_letivo = ano_query
        periodos_do_ano = get_periodos_by_ano(periodos_letivos, ano_letivo)

        if periodo_query in periodos_do_ano:
            periodo_letivo = periodo_query
        elif periodos_do_ano:
            periodo_letivo = periodos_do_ano[0]
        else:
            periodo_letivo = periodo_query or 1
    elif periodos_letivos:
        ano_letivo = periodos_letivos[0]['ano_letivo']
        periodo_letivo = periodos_letivos[0]['periodo_letivo']
    else:
        ano_letivo = date.today().year
        periodo_letivo = 1

    anos = sorted(
        {periodo['ano_letivo'] for periodo in periodos_letivos if periodo.get('ano_letivo')},
        reverse=True
    ) or [ano_letivo]
    periodos = sorted(get_periodos_by_ano(periodos_letivos, ano_letivo)) or [periodo_letivo]

    disciplinas, erro_boletim = get_paginated_results(
        f'ensino/meu-boletim/{ano_letivo}/{periodo_letivo}/'
    )
    disciplinas = [disciplina for disciplina in disciplinas if isinstance(disciplina, dict)]
    campos = get_boletim_fields(disciplinas)

    return render_template(
        'boletim.html',
        user_data=user_data,
        disciplinas=disciplinas,
        campos=campos,
        anos=anos,
        periodos=periodos,
        periodos_letivos=periodos_letivos,
        ano_letivo=ano_letivo,
        periodo_letivo=periodo_letivo,
        erro=erro_boletim or erro_periodos
    )


@app.route('/login/authorized')
def auth():
    token = oauth.suap.authorize_access_token()
    session['suap_token'] = token
    return redirect(url_for('perfil'))

if __name__ == "__main__":
    app.run()
