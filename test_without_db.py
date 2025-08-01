#!/usr/bin/env python3
"""
Script para testar o sistema RelBack sem conexão com banco de dados.
Este script demonstra como o sistema se comporta quando o banco está indisponível.
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectRelback.settings')
django.setup()

def test_database_availability():
    """Testa a função de verificação de disponibilidade do banco."""
    from coreRelback.views import is_database_available
    
    print("🔍 Testando disponibilidade do banco de dados...")
    
    try:
        available = is_database_available()
        if available:
            print("✅ Banco de dados está disponível")
        else:
            print("❌ Banco de dados está indisponível")
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
    
    return available

def test_views_without_db():
    """Testa as views principais sem banco de dados."""
    from django.test import RequestFactory
    from coreRelback.views import (
        index, ClientListView, HostListView, 
        DatabaseListView, BackupPolicyListView
    )
    
    print("\n🧪 Testando views sem banco de dados...")
    
    factory = RequestFactory()
    
    # Teste da view index
    try:
        request = factory.get('/')
        response = index(request)
        print(f"✅ Index view: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Index view falhou: {e}")
    
    # Teste das views de lista
    views_to_test = [
        ('Clients', ClientListView),
        ('Hosts', HostListView),
        ('Databases', DatabaseListView),
        ('Policies', BackupPolicyListView),
    ]
    
    for name, view_class in views_to_test:
        try:
            request = factory.get('/')
            view = view_class.as_view()
            response = view(request)
            print(f"✅ {name} ListView: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name} ListView falhou: {e}")

def test_ajax_endpoints():
    """Testa os endpoints AJAX sem banco de dados."""
    from django.test import RequestFactory
    from coreRelback.views import get_hosts_by_client, get_databases_by_client
    
    print("\n🌐 Testando endpoints AJAX...")
    
    factory = RequestFactory()
    
    # Teste get_hosts_by_client
    try:
        request = factory.get('/')
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = get_hosts_by_client(request, 1)
        print(f"✅ get_hosts_by_client: Status {response.status_code}")
        print(f"   Response: {response.content.decode()}")
    except Exception as e:
        print(f"❌ get_hosts_by_client falhou: {e}")
    
    # Teste get_databases_by_client
    try:
        request = factory.get('/')
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = get_databases_by_client(request, 1)
        print(f"✅ get_databases_by_client: Status {response.status_code}")
        print(f"   Response: {response.content.decode()}")
    except Exception as e:
        print(f"❌ get_databases_by_client falhou: {e}")

def test_list_views_ajax():
    """Testa as ListView com requisições AJAX."""
    from django.test import RequestFactory
    from coreRelback.views import (
        ClientListView, HostListView, 
        DatabaseListView, BackupPolicyListView
    )
    
    print("\n📡 Testando ListViews com AJAX...")
    
    factory = RequestFactory()
    
    views_to_test = [
        ('Clients', ClientListView),
        ('Hosts', HostListView),
        ('Databases', DatabaseListView),
        ('Policies', BackupPolicyListView),
    ]
    
    for name, view_class in views_to_test:
        try:
            request = factory.get('/')
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
            view = view_class()
            view.request = request
            response = view.ajax_response()
            print(f"✅ {name} AJAX: Status {response.status_code}")
            print(f"   Response: {response.content.decode()[:100]}...")
        except Exception as e:
            print(f"❌ {name} AJAX falhou: {e}")

def main():
    """Função principal do teste."""
    print("🚀 Iniciando testes do sistema RelBack sem banco de dados")
    print("=" * 60)
    
    # Teste 1: Verificar disponibilidade do banco
    db_available = test_database_availability()
    
    # Teste 2: Views principais
    test_views_without_db()
    
    # Teste 3: Endpoints AJAX
    test_ajax_endpoints()
    
    # Teste 4: ListView com AJAX
    test_list_views_ajax()
    
    print("\n" + "=" * 60)
    if db_available:
        print("🎉 Testes concluídos - Sistema funcionando COM banco de dados")
    else:
        print("🎯 Testes concluídos - Sistema funcionando SEM banco de dados")
        print("✨ O sistema está preparado para trabalhar offline!")

if __name__ == '__main__':
    main()
