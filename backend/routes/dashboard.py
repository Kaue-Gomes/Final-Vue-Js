from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
import sys

dashboard_bp = Blueprint('dashboard', __name__)

def get_models():
    """Obtém db e modelos do módulo correto"""
    try:
        if '__main__' in sys.modules and hasattr(sys.modules['__main__'], 'db'):
            main = sys.modules['__main__']
            return main.db, main.Produto
        else:
            from app import db, Produto
            return db, Produto
    except ImportError:
        import __main__
        return __main__.db, __main__.Produto

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def estatisticas():
    db, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        # Converter para int se necessário
        if isinstance(usuario_id, str):
            usuario_id = int(usuario_id)
        
        total_produtos = Produto.query.filter_by(usuario_id=usuario_id).count()
        
        resultado = db.session.query(
            func.sum(Produto.preco * Produto.estoque).label('valor_total')
        ).filter_by(usuario_id=usuario_id).first()
        
        valor_total = float(resultado.valor_total) if resultado.valor_total else 0
        
        produtos_baixo_estoque = Produto.query.filter_by(
            usuario_id=usuario_id,
            ativo=True
        ).filter(Produto.estoque < 10).count()
        
        produtos_ativos = Produto.query.filter_by(
            usuario_id=usuario_id,
            ativo=True
        ).count()
        
        return jsonify({
            'total_produtos': total_produtos,
            'valor_total_estoque': valor_total,
            'produtos_baixo_estoque': produtos_baixo_estoque,
            'produtos_ativos': produtos_ativos
        }), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@dashboard_bp.route('/categorias', methods=['GET'])
@jwt_required()
def produtos_por_categoria():
    db, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        
        resultados = db.session.query(
            Produto.categoria,
            func.count(Produto.id).label('quantidade')
        ).filter_by(
            usuario_id=usuario_id
        ).group_by(Produto.categoria).all()
        
        dados = [{'categoria': cat or 'Sem categoria', 'quantidade': qtd} 
                for cat, qtd in resultados]
        
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@dashboard_bp.route('/atividades', methods=['GET'])
@jwt_required()
def atividades_recentes():
    _, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        
        produtos = Produto.query.filter_by(
            usuario_id=usuario_id
        ).order_by(Produto.data_criacao.desc()).limit(10).all()
        
        atividades = []
        for produto in produtos:
            data_atual = produto.data_atualizacao if produto.data_atualizacao else produto.data_criacao
            atividades.append({
                'tipo': 'atualizado' if produto.data_atualizacao else 'criado',
                'produto': produto.nome,
                'data': data_atual.isoformat() if data_atual else None
            })
        
        return jsonify(atividades), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@dashboard_bp.route('/produtos-destaque', methods=['GET'])
@jwt_required()
def produtos_destaque():
    _, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        
        # Produtos mais caros
        produtos_caros = Produto.query.filter_by(
            usuario_id=usuario_id,
            ativo=True
        ).order_by(Produto.preco.desc()).limit(5).all()
        
        # Produtos com estoque baixo
        produtos_baixo_estoque = Produto.query.filter_by(
            usuario_id=usuario_id,
            ativo=True
        ).filter(Produto.estoque < 10).order_by(Produto.estoque.asc()).limit(5).all()
        
        return jsonify({
            'mais_caros': [p.to_dict() for p in produtos_caros],
            'baixo_estoque': [p.to_dict() for p in produtos_baixo_estoque]
        }), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500


@dashboard_bp.route('/vendas-mensais', methods=['GET'])
@jwt_required()
def vendas_mensais():
    db, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()

        resultados = (
            db.session.query(
                func.strftime('%Y-%m', Produto.data_criacao).label('mes'),
                func.sum(Produto.preco * Produto.estoque).label('total_vendas')
            )
            .filter_by(usuario_id=usuario_id)
            .group_by('mes')
            .order_by('mes')
            .all()
        )

        dados = [
            {
                'mes': mes,
                'total': float(total) if total else 0
            }
            for mes, total in resultados
        ]

        return jsonify(dados), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500


@dashboard_bp.route('/crescimento', methods=['GET'])
@jwt_required()
def crescimento_produtos():
    db, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()

        resultados = (
            db.session.query(
                func.strftime('%Y-%m', Produto.data_criacao).label('mes'),
                func.count(Produto.id).label('quantidade')
            )
            .filter_by(usuario_id=usuario_id)
            .group_by('mes')
            .order_by('mes')
            .all()
        )

        cumulativo = 0
        dados = []
        for mes, qtd in resultados:
            cumulativo += qtd or 0
            dados.append({
                'mes': mes,
                'quantidade': int(qtd or 0),
                'acumulado': cumulativo
            })

        return jsonify(dados), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
