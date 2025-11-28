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
 
load_dotenv()

app = Flask(__name__)

# Hbilitando CORS, para consumo no front end
CORS(app, resources={r"/*": {"origins": "*"}})

# Configurações do JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    app.logger.error(f"Erro JWT: Nenhuma autorização fornecida.")
    return jsonify({'message': 'Token de acesso não fornecido no cabeçalho Authorization.'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    app.logger.error(f"Erro JWT: Token inválido. Descrição: {callback}")
    return jsonify({'message': f'Token inválido: {callback}'}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    app.logger.error(f"Erro JWT: Token expirado. Payload: {jwt_payload}")
    return jsonify({'message': 'Token de acesso expirado.'}), 401

def handle_jwt_errors(error):
    app.logger.error(f"Erro JWT Capturado: {type(error).__name__} - {str(error)}")
    # Retorna o erro 401 para qualquer falha de autenticação JWT
    return jsonify({'message': 'Falha na autenticação do Token', 'details': str(error)}), 401


# Configurações do banco de dados
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Conexão com o banco de dados
db_password_user = get_secret()

db_name = db_password_user['dbname']
user = db_password_user['username']
password = db_password_user['password']
db_host = db_password_user['host']
port = db_password_user['port']

database = Database(db_name, user, password, db_host)

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

    professor_service.atualizar_professor(id, nome, email, senha)

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

    tokens = authenticate_professor(professor_service, email, senha)

    if tokens is None:
        return jsonify({'message': 'Credenciais inválidas'}), 401
    
    access_token, refresh_token = tokens

    if access_token:
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200

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
    if not request.is_json:
            app.logger.error("Requisição negada: Content-Type não é application/json")
            return jsonify({'message': 'Content-Type deve ser application/json'}), 415 
    try:
        print("--- DEBUG: Rota Agendamentos Acessada ---")
        app.logger.info(f"--- DEBUG: Rota Agendamentos Acessada ---")
        current_user = get_jwt_identity()
        
        data = request.json
        app.logger.info(f"Payload Recebido no POST /agendamentos: {data}")
        print(request.json)
        id_laboratorio = data.get('id_laboratorio')
        id_professor = current_user
        data_agendamento = data.get('data')
        hora_inicio = data.get('hora_inicio')
        hora_fim = data.get('hora_fim')

        agendamento_id = agendamento_service.create_agendamento(id_laboratorio, id_professor, data_agendamento, hora_inicio, hora_fim)

        return jsonify(agendamento_id), 201


    except CustomException as e:
        app.logger.error(f"Erro CustomException: {e.message} ({e.error_type.name})")
        return jsonify({'message': e.message, 'type': e.error_type.name}), 400
    except Exception as e:
        app.logger.error(f"Erro interno não tratado: {e}")
        return jsonify({'message': 'Erro interno do servidor', 'type': 'INTERNAL_ERROR'}), 500


@app.route('/agendamentos', methods=['GET'])
@jwt_required()
def get_all_agendamentos():
    try:
        agendamentos = agendamento_service.get_all_agendamentos()
        
        agendamentos_dict = []
        for a in agendamentos:
            agendamentos_dict.append({
                'id': a.id,
                'id_laboratorio': a.id_laboratorio,
                'id_professor': a.id_professor,
                'data_agendamento': a.data_agendamento,
                'hora_inicio': a.hora_inicio.strftime('%H:%M:%S') if hasattr(a.hora_inicio, 'strftime') else str(a.hora_inicio),
                'hora_fim': a.hora_fim.strftime('%H:%M:%S') if hasattr(a.hora_fim, 'strftime') else str(a.hora_fim)
            })
            
        return jsonify(agendamentos_dict)
        
    except CustomException as e:
        app.logger.error(f"Erro CustomException no GET /agendamentos: {e.message}")
        return jsonify({'message': e.message, 'type': e.error_type.name}), e.http_status_code()
    
    except Exception as e:
        import traceback
        app.logger.error(f"Erro INESPERADO no GET /agendamentos: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'Erro interno ao listar agendamentos', 'type': 'INTERNAL_SERVER_ERROR'}), 500

@app.route('/agendamentos/<int:agendamento_id>', methods=['GET'])
@jwt_required()
def get_agendamento_by_id(agendamento_id):
    agendamento = agendamento_service.get_agendamento_by_id(agendamento_id)
    agendamento_dict = {
        'id': agendamento.id,
        'id_laboratorio': agendamento.id_laboratorio,
        'id_professor': agendamento.id_professor,
        'data_agendamento': agendamento.data_agendamento,
        'hora_inicio': agendamento.hora_inicio.strftime('%H:%M:%S'), 
        'hora_fim': agendamento.hora_fim.strftime('%H:%M:%S') 
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
    hora_fim = data.get('hora_fim')
    agendamento_service.update_agendamento(agendamento_id, id_laboratorio, id_professor, data_agendamento, hora_inicio, hora_fim)
    return jsonify({'message': 'Agendamento atualizado com sucesso'})

@app.route('/agendamentos/<int:agendamento_id>', methods=['DELETE'])
@jwt_required()
def delete_agendamento(agendamento_id):
    agendamento_service.delete_agendamento(agendamento_id)
    return jsonify({'message': 'Agendamento deletado com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
