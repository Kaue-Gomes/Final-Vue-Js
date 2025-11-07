from flask_jwt_extended import get_jwt_identity

def get_usuario_id():
    """Obtém o ID do usuário do token JWT e converte para int"""
    usuario_id = get_jwt_identity()
    if isinstance(usuario_id, str):
        return int(usuario_id)
    return usuario_id


