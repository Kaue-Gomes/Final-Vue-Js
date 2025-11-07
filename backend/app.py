from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sys

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///produtos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'sua-chave-secreta-super-segura-aqui')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

# Criar instância do SQLAlchemy
db = SQLAlchemy()
db.init_app(app)

jwt = JWTManager(app)
CORS(app)

# Configurar handlers de erro do JWT
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'mensagem': 'Token expirado. Por favor, faça login novamente.'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'mensagem': f'Token inválido: {str(error)}. Por favor, faça login novamente.'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'mensagem': 'Token de autenticação não fornecido.'}), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({'mensagem': 'Token não é recente. Por favor, faça login novamente.'}), 401

# Modelos - definidos após db.init_app()
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    produtos = db.relationship('Produto', backref='usuario', lazy=True)
    
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)
    
    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, default=0)
    categoria = db.Column(db.String(100))
    imagem_url = db.Column(db.String(500))
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, onupdate=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'estoque': self.estoque,
            'categoria': self.categoria,
            'imagem_url': self.imagem_url,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            'usuario_id': self.usuario_id
        }

# Importar rotas DEPOIS de definir os modelos
# Importação local para evitar problemas quando executado diretamente
if __name__ == '__main__':
    # Quando executado diretamente, importar como módulo
    from routes import auth, produtos, dashboard
else:
    # Quando importado, usar caminho relativo
    from .routes import auth, produtos, dashboard

# Registrar blueprints
app.register_blueprint(auth.auth_bp, url_prefix='/api/auth')
app.register_blueprint(produtos.produtos_bp, url_prefix='/api/produtos')
app.register_blueprint(dashboard.dashboard_bp, url_prefix='/api/dashboard')

def init_database():
    with app.app_context():
        db.create_all()
        
        # Criar usuário admin padrão se não existir
        if not Usuario.query.filter_by(email='admin@admin.com').first():
            admin = Usuario(
                nome='Administrador',
                email='admin@admin.com'
            )
            admin.set_senha('admin123')
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    init_database()
    app.run(debug=True, port=5000)
