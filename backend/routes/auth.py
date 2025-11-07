from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import sys

auth_bp = Blueprint('auth', __name__)

def get_models():
    """Obtém db e modelos do módulo correto"""
    # Quando executado como python app.py, o módulo é __main__
    # Quando importado, é app
    try:
        if '__main__' in sys.modules and hasattr(sys.modules['__main__'], 'db'):
            main = sys.modules['__main__']
            return main.db, main.Usuario
        else:
            from app import db, Usuario
            return db, Usuario
    except ImportError:
        # Fallback: tentar importar do __main__
        import __main__
        return __main__.db, __main__.Usuario

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        db, Usuario = get_models()
        
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('senha') or not data.get('nome'):
            return jsonify({'mensagem': 'Campos obrigatórios faltando'}), 400
        
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({'mensagem': 'Email já cadastrado'}), 400
        
        usuario = Usuario(
            nome=data['nome'],
            email=data['email']
        )
        usuario.set_senha(data['senha'])
        
        db.session.add(usuario)
        db.session.commit()
        
        # Criar token com identity como string do ID
        token = create_access_token(identity=str(usuario.id))
        
        return jsonify({
            'mensagem': 'Usuário criado com sucesso',
            'token': token,
            'usuario': usuario.to_dict()
        }), 201
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return jsonify({'mensagem': f'Erro ao registrar: {error_msg}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        _, Usuario = get_models()
        
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados inválidos'}), 400
            
        email = data.get('email')
        senha = data.get('senha')
        
        if not email or not senha:
            return jsonify({'mensagem': 'Email e senha são obrigatórios'}), 400
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario or not usuario.check_senha(senha):
            return jsonify({'mensagem': 'Credenciais inválidas'}), 401
        
        # Criar token com identity como string do ID
        token = create_access_token(identity=str(usuario.id))
        
        return jsonify({
            'token': token,
            'usuario': usuario.to_dict()
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'mensagem': f'Erro ao fazer login: {str(e)}'}), 500

@auth_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    try:
        _, Usuario = get_models()
        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(usuario_id)
        
        if not usuario:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
        
        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@auth_bp.route('/perfil', methods=['PUT'])
@jwt_required()
def atualizar_perfil():
    try:
        db, Usuario = get_models()
        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(usuario_id)
        
        if not usuario:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados inválidos'}), 400
        
        if data.get('nome'):
            usuario.nome = data['nome']
        if data.get('email'):
            if Usuario.query.filter_by(email=data['email']).filter(Usuario.id != usuario_id).first():
                return jsonify({'mensagem': 'Email já está em uso'}), 400
            usuario.email = data['email']
        if data.get('senha'):
            usuario.set_senha(data['senha'])
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Perfil atualizado com sucesso',
            'usuario': usuario.to_dict()
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'mensagem': str(e)}), 500
