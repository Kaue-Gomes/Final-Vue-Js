# Instruções de Instalação e Execução

## Pré-requisitos

- Node.js 18+ e npm
- Python 3.8+ e pip

## Instalação do Frontend

1. Instale as dependências:
```bash
npm install
```

2. Execute o servidor de desenvolvimento:
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

## Instalação do Backend

1. Navegue até a pasta backend:
```bash
cd backend
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Execute o servidor Flask:
```bash
python app.py
```

O backend estará disponível em `http://localhost:5000`

## Primeiro Acesso

1. Acesse `http://localhost:3000`
2. Clique em "Registrar" para criar uma nova conta
3. Ou use as credenciais padrão (se criadas):
   - Email: `admin@admin.com`
   - Senha: `admin123`

## Estrutura de Pastas

```
Projeto final/
├── backend/          # API Flask
├── src/             # Frontend Vue.js
├── public/          # Arquivos públicos
└── package.json     # Dependências do frontend
```

## Funcionalidades

- ✅ Autenticação completa (Login/Registro)
- ✅ CRUD de produtos
- ✅ Dashboard com métricas
- ✅ Filtros e busca
- ✅ Tema claro/escuro
- ✅ Interface responsiva

## Troubleshooting

### Erro de CORS
Certifique-se de que o backend está rodando na porta 5000 e o frontend na porta 3000.

### Erro de banco de dados
O banco SQLite será criado automaticamente na primeira execução do backend.

### Porta já em uso
Altere a porta no arquivo `vite.config.js` (frontend) ou `app.py` (backend).

