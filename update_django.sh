#!/bin/bash

# Script para atualizar dependências do projeto
echo "🚀 Iniciando atualização das dependências..."

# Ativar ambiente virtual
if [ -f .venv/bin/activate ]; then
	source .venv/bin/activate
elif [ -f venvRelback/bin/activate ]; then
	source venvRelback/bin/activate
else
	echo "❌ Ambiente virtual não encontrado (.venv ou venvRelback)."
	exit 1
fi

echo "📦 Atualizando pip..."
pip install --upgrade pip

echo "📦 Atualizando dependências Python conforme requirements.txt..."
pip install --upgrade -r requirements.txt

echo "🔍 Verificando configurações..."
python manage.py check --deploy

echo "🗄️ Executando migrações..."
python manage.py makemigrations
python manage.py migrate

echo "📋 Listando versões atuais..."
pip show Django oracledb django-tables2 | grep -E "^(Name|Version):"

echo "✅ Atualização concluída!"
echo "🧪 Execute 'python manage.py runserver' para testar"
