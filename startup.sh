#!/bin/bash
# Instalar dependências (opcional)
pip install -r requirements.txt

# Iniciar a aplicação com Gunicorn
gunicorn --bind 0.0.0.0:$PORT app:app
