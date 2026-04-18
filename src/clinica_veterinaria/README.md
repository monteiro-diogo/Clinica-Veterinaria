# 💻 Guia de Desenvolvimento (src)

Esta pasta contém o coração da aplicação Django. Foi adotada uma estrutura modular para facilitar a manutenção.

## 🏗️ Arquitetura do Código
- **`clinica_vet/`**: Pasta principal do projeto (Settings, URLs globais, WSGI).
- **`core/`**: Aplicação principal que gere a lógica de negócio (Models, Views, Forms).
- **`templates/`**: Ficheiros HTML organizados por funcionalidade.
- **`static/`**: Ficheiros CSS e JavaScript globais.
- **`media/`**: Ficheiros imagem necessários.

## 🔑 Variáveis de Ambiente (.env)
O projeto utiliza `python-dotenv` para segurança. Variáveis necessárias:
- `SECRET_KEY`: Chave de segurança do Django.
- `DEBUG`: `True` para desenvolvimento, `False` para produção.
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Credenciais da base de dados.

## 📋 Comandos Úteis
- **Criar ficheiro db.sqlite3:** `python manage.py migrate`
- **Correr servidor offline:** `python manage.py runserver `