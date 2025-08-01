#!/bin/bash

# Script para atualizar Django
echo "🚀 Iniciando atualização do Django..."

# Ativar ambiente virtual
source venvRelback/bin/activate

echo "📦 Atualizando Django para 5.2.4..."
pip install --upgrade django==5.2.4

echo "📦 Atualizando dependências..."
pip install --upgrade django-tables2
pip install --upgrade oracledb

echo "🔍 Verificando configurações..."
python manage.py check --deploy

echo "🗄️ Executando migrações..."
python manage.py makemigrations
python manage.py migrate

echo "📋 Listando versões atuais..."
pip list | grep -i django

echo "✅ Atualização concluída!"
echo "🧪 Execute 'python manage.py runserver' para testar"
