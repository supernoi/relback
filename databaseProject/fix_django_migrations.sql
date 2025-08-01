/*
Script para marcar migrações Django como aplicadas no banco Oracle
Execute este script para resolver problemas de migração
*/

-- Verificar migrações existentes
SELECT * FROM DJANGO_MIGRATIONS WHERE app = 'coreRelback' ORDER BY id;

-- Marcar migrações como aplicadas (se necessário)
INSERT INTO DJANGO_MIGRATIONS (app, name, applied) 
VALUES ('coreRelback', '0002_backuppolicy_client_database_host_relbackuser_and_more', CURRENT_TIMESTAMP);

INSERT INTO DJANGO_MIGRATIONS (app, name, applied) 
VALUES ('coreRelback', '0005_add_user_preferences', CURRENT_TIMESTAMP);

COMMIT;
