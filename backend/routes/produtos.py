from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, func
from datetime import datetime
import csv
import io
import sys
from fpdf import FPDF
import traceback

produtos_bp = Blueprint('produtos', __name__)

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

def construir_query_produtos(Produto, usuario_id, params):
    query = Produto.query.filter_by(usuario_id=usuario_id)

    busca = (params.get('busca') or '').strip()
    if busca:
        query = query.filter(or_(
            Produto.nome.ilike(f'%{busca}%'),
            Produto.descricao.ilike(f'%{busca}%')
        ))

    categoria = (params.get('categoria') or '').strip()
    if categoria:
        query = query.filter(Produto.categoria == categoria)

    preco_min = params.get('preco_min')
    if preco_min not in (None, '', 'null'):
        try:
            valor = float(preco_min)
            query = query.filter(Produto.preco >= valor)
        except ValueError:
            pass

    preco_max = params.get('preco_max')
    if preco_max not in (None, '', 'null'):
        try:
            valor = float(preco_max)
            query = query.filter(Produto.preco <= valor)
        except ValueError:
            pass

    ativo = params.get('ativo')
    if ativo not in (None, ''):
        valor = str(ativo).lower() == 'true'
        query = query.filter(Produto.ativo == valor)

    ordenar = (params.get('ordenar') or 'data_criacao').lower()
    ordem = (params.get('ordem') or 'desc').lower()

    if ordenar == 'nome':
        campo = Produto.nome
    elif ordenar == 'preco':
        campo = Produto.preco
    else:
        campo = Produto.data_criacao

    if ordem == 'asc':
        query = query.order_by(campo.asc())
    else:
        query = query.order_by(campo.desc())

    return query


def formatar_moeda(valor):
    try:
        return f"R$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (TypeError, ValueError):
        return 'R$ 0,00'


def sanitize_text(texto):
    if texto is None:
        return ''
    if not isinstance(texto, str):
        texto = str(texto)
    return texto.encode('latin-1', 'replace').decode('latin-1')


@produtos_bp.route('', methods=['GET'])
@jwt_required()
def listar_produtos():
    _, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        if isinstance(usuario_id, str):
            usuario_id = int(usuario_id)

        query = construir_query_produtos(Produto, usuario_id, request.args)
        produtos = query.all()

        return jsonify([p.to_dict() for p in produtos]), 200
    except Exception as e:
        print('Erro ao listar produtos:', e)
        print(traceback.format_exc())
        return jsonify({'mensagem': str(e)}), 500

@produtos_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def buscar_produto(id):
    _, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=id, usuario_id=usuario_id).first()
        
        if not produto:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
        
        return jsonify(produto.to_dict()), 200
    except Exception as e:
        print('Erro ao buscar produto:', e)
        print(traceback.format_exc())
        return jsonify({'mensagem': str(e)}), 500

@produtos_bp.route('', methods=['POST'])
@jwt_required()
def criar_produto():
    db, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        
        if not usuario_id:
            return jsonify({'mensagem': 'Usuário não autenticado'}), 401
        
        # Converter para int se necessário
        if isinstance(usuario_id, str):
            usuario_id = int(usuario_id)
            
        data = request.get_json()
        
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos'}), 400
        
        if not data.get('nome') or not data.get('preco'):
            return jsonify({'mensagem': 'Nome e preço são obrigatórios'}), 400
        
        try:
            produto = Produto(
                nome=data['nome'],
                descricao=data.get('descricao', ''),
                preco=float(data['preco']),
                estoque=int(data.get('estoque', 0)),
                categoria=data.get('categoria', ''),
                imagem_url=data.get('imagem_url', ''),
                ativo=data.get('ativo', True),
                usuario_id=usuario_id
            )
            
            db.session.add(produto)
            db.session.commit()
            
            return jsonify(produto.to_dict()), 201
        except ValueError as e:
            return jsonify({'mensagem': f'Erro ao processar dados: {str(e)}'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'mensagem': f'Erro ao criar produto: {str(e)}'}), 500
    except Exception as e:
        print('Erro interno ao criar produto:', e)
        print(traceback.format_exc())
        return jsonify({'mensagem': f'Erro interno: {str(e)}'}), 500

@produtos_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_produto(id):
    db, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=id, usuario_id=usuario_id).first()
        
        if not produto:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
        
        data = request.get_json()
        
        if data.get('nome'):
            produto.nome = data['nome']
        if 'descricao' in data:
            produto.descricao = data['descricao']
        if data.get('preco'):
            produto.preco = float(data['preco'])
        if 'estoque' in data:
            produto.estoque = int(data['estoque'])
        if 'categoria' in data:
            produto.categoria = data['categoria']
        if 'imagem_url' in data:
            produto.imagem_url = data['imagem_url']
        if 'ativo' in data:
            produto.ativo = data['ativo']
        
        db.session.commit()
        
        return jsonify(produto.to_dict()), 200
    except Exception as e:
        print('Erro ao atualizar produto:', e)
        print(traceback.format_exc())
        return jsonify({'mensagem': str(e)}), 500

@produtos_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_produto(id):
    db, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=id, usuario_id=usuario_id).first()
        
        if not produto:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
        
        db.session.delete(produto)
        db.session.commit()
        
        return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200
    except Exception as e:
        print('Erro ao deletar produto:', e)
        print(traceback.format_exc())
        return jsonify({'mensagem': str(e)}), 500

@produtos_bp.route('/categorias', methods=['GET'])
@jwt_required()
def listar_categorias():
    db, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        categorias = db.session.query(Produto.categoria).filter_by(
            usuario_id=usuario_id
        ).distinct().all()
        
        categorias_list = [cat[0] for cat in categorias if cat[0]]
        
        return jsonify(categorias_list), 200
    except Exception as e:
        print('Erro ao listar categorias:', e)
        print(traceback.format_exc())
        return jsonify({'mensagem': str(e)}), 500


@produtos_bp.route('/export/csv', methods=['GET'])
@jwt_required()
def exportar_csv():
    _, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        if isinstance(usuario_id, str):
            usuario_id = int(usuario_id)

        query = construir_query_produtos(Produto, usuario_id, request.args)
        produtos = query.all()

        output = io.StringIO()
        writer = csv.writer(output, delimiter=';')
        writer.writerow(['ID', 'Nome', 'Categoria', 'Preço', 'Estoque', 'Status', 'Criado em'])

        for produto in produtos:
            writer.writerow([
                produto.id,
                produto.nome,
                produto.categoria or 'Sem categoria',
                f'{produto.preco:.2f}',
                produto.estoque,
                'Ativo' if produto.ativo else 'Inativo',
                produto.data_criacao.strftime('%d/%m/%Y') if produto.data_criacao else ''
            ])

        csv_data = output.getvalue()
        output.close()

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        response = make_response(csv_data)
        response.headers['Content-Disposition'] = f'attachment; filename=produtos_{timestamp}.csv'
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        return response
    except Exception as e:
        print('Erro ao exportar CSV:', e)
        print(traceback.format_exc())
        return jsonify({'mensagem': str(e)}), 500


@produtos_bp.route('/export/pdf', methods=['GET'])
@jwt_required()
def exportar_pdf():
    _, Produto = get_models()
    try:
        usuario_id = get_jwt_identity()
        if isinstance(usuario_id, str):
            usuario_id = int(usuario_id)

        query = construir_query_produtos(Produto, usuario_id, request.args)
        produtos = query.all()

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 10, 'Relatório de Produtos', ln=True)
        pdf.ln(4)

        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 8, f'Gerado em {datetime.utcnow().strftime("%d/%m/%Y %H:%M")} UTC', ln=True)
        pdf.cell(0, 8, f'Total de produtos: {len(produtos)}', ln=True)
        pdf.ln(6)

        headers = ['Nome', 'Categoria', 'Preço', 'Estoque', 'Status']
        widths = [70, 40, 25, 20, 25]

        pdf.set_fill_color(102, 126, 234)
        pdf.set_text_color(255)
        pdf.set_font('Helvetica', 'B', 10)

        for header, width in zip(headers, widths):
            pdf.cell(width, 8, header, border=1, align='L', fill=True)
        pdf.ln()

        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(0)
        fill = False

        for produto in produtos:
            valores = [
                sanitize_text(produto.nome[:45]),
                sanitize_text((produto.categoria or 'Sem categoria')[:25]),
                sanitize_text(formatar_moeda(produto.preco)),
                sanitize_text(produto.estoque),
                sanitize_text('Ativo' if produto.ativo else 'Inativo')
            ]

            for valor, width in zip(valores, widths):
                pdf.cell(width, 8, valor, border=1, align='L', fill=fill)
            pdf.ln()
            fill = not fill

        pdf_output = pdf.output(dest='S')
        if isinstance(pdf_output, (bytes, bytearray)):
            pdf_bytes = bytes(pdf_output)
        else:
            pdf_bytes = pdf_output.encode('latin-1', 'replace')
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')

        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=produtos_{timestamp}.pdf'
        return response
    except Exception as e:
        print('Erro ao exportar PDF:', e)
        print(traceback.format_exc())
        return jsonify({'mensagem': str(e)}), 500
