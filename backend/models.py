from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

def create_models(db):
    """Cria os modelos usando a instância db fornecida"""
    
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
    
    return Usuario, Produto
