from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_cors import CORS
import os
from dotenv import load_dotenv
from src.secret.get_rds_credentials import get_secret
from src.models.professor_model import Professor
from src.repository.database import Database
from src.repository.professor_repository import ProfessorRepository
from src.service.professor_service import ProfessorService
from src.repository.agendamento_repository import AgendamentoRepository
from src.service.agendamento_service import AgendamentoService
from src.exceptions.custom_exception import ErrorType, CustomException
from src.auth.auth import authenticate_professor

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

app = Flask(__name__)

# Hbilitando CORS, para consumo no front end
CORS(app, resources={r"/*": {"origins": "*"}})

# Configurações do JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Configurações do banco de dados
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Conexão com o banco de dados
db_password_user = get_secret()

database = Database(db_name, db_password_user['username'], db_password_user['password'], db_host)

# Instânciando repositorios e serviços
professor_service = ProfessorService(ProfessorRepository(database))
agendamento_repository = AgendamentoRepository(database)
agendamento_service = AgendamentoService(agendamento_repository)

@app.errorhandler(CustomException)
def handle_custom_exception(error):
    response = jsonify({
        'message': error.message,
        'error_type': error.error_type.value
    })
    response.status_code = error.http_status_code()
    return response

# CREATE
@app.route('/professores', methods=['POST'])
def create_professor():
    data = request.json
    nome = data['nome']
    email = data['email']
    senha = data['senha']

    professor_id = professor_service.criar_professor(nome, email, senha)
    
    return jsonify({'message': 'Professor criado com sucesso!', 'id': professor_id})

# UPDATE
@app.route('/professores/<int:id>', methods=['PUT'])
def update_professor(id):
    data = request.json
    nome = data['nome']
    email = data['email']
    senha = data['senha']

    professor_service.atualizar_professor(Professor(id, nome, email, senha))

    return jsonify({'message': 'Professor atualizado com sucesso!'})

# READ
@app.route('/professores', methods=['GET'])
def get_professores():
    professores = professor_service.listar_professores()
    return jsonify([vars(professor) for professor in professores])

# READ BY ID
@app.route('/professores/<int:id>', methods=['GET'])
def get_id_professor(id):
    professor = professor_service.busca_professor_id(id)
    return jsonify(professor)

# DELETE
@app.route('/professores/<int:id>', methods=['DELETE'])
def delete_professor(id):
    professor_service.deletar_professor(id)
    return jsonify({'message': 'Professor deletado com sucesso!'})

# Rota de login
@app.route('/login', methods=['POST'])
def login_professor():
    data = request.json
    email = data['email']
    senha = data['senha']

    access_token = authenticate_professor(professor_service, email, senha)

    if access_token:
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401

# Rota de refresh token
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_access_token}), 200


# Rotas de agendamento
@app.route('/agendamentos', methods=['POST'])
@jwt_required()
def create_agendamento():
    try:
        current_user = get_jwt_identity()

        data = request.json
        id_laboratorio = data.get('id_laboratorio')
        id_professor = current_user
        data_agendamento = data.get('data')
        hora_inicio = data.get('hora_inicio')
        hora_fim = data.get('hora_fim')

        agendamento_id = agendamento_service.create_agendamento(id_laboratorio, id_professor, data_agendamento, hora_inicio, hora_fim)

        return jsonify(agendamento_id), 201


    except CustomException as e:
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/agendamentos', methods=['GET'])
@jwt_required()
def get_all_agendamentos():
    agendamentos = agendamento_service.get_all_agendamentos()
    agendamentos_dict = [
        {
            'id': a.id,
            'id_laboratorio': a.id_laboratorio,
            'id_professor': a.id_professor,
            'data': a.data,
            'hora_inicio': a.hora_inicio.strftime('%H:%M:%S'),  # Convertendo para string
            'hora_fim': a.hora_fim.strftime('%H:%M:%S')  # Convertendo para string
        } for a in agendamentos
    ]
    return jsonify(agendamentos_dict)

@app.route('/agendamentos/<int:agendamento_id>', methods=['GET'])
@jwt_required()
def get_agendamento_by_id(agendamento_id):
    agendamento = agendamento_service.get_agendamento_by_id(agendamento_id)
    agendamento_dict = {
        'id': agendamento.id,
        'id_laboratorio': agendamento.id_laboratorio,
        'id_professor': agendamento.id_professor,
        'data': agendamento.data,
        'hora_inicio': agendamento.hora_inicio.strftime('%H:%M:%S'),  # Convertendo para string
        'hora_fim': agendamento.hora_fim.strftime('%H:%M:%S')  # Convertendo para string
    }
    return jsonify(agendamento_dict)

@app.route('/agendamentos/<int:agendamento_id>', methods=['PUT'])
@jwt_required()
def update_agendamento(agendamento_id):
    current_user = get_jwt_identity()
    data = request.json
    id_laboratorio = data.get('id_laboratorio')
    id_professor = current_user
    data_agendamento = data.get('data')
    hora_inicio = data.get('hora_inicio')
    agendamento_service.update_agendamento(agendamento_id, id_laboratorio, id_professor, data_agendamento, hora_inicio)
    return jsonify({'message': 'Agendamento atualizado com sucesso'})

@app.route('/agendamentos/<int:agendamento_id>', methods=['DELETE'])
@jwt_required()
def delete_agendamento(agendamento_id):
    agendamento_service.delete_agendamento(agendamento_id)
    return jsonify({'message': 'Agendamento deletado com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
