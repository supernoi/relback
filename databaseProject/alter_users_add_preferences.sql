/*
Script para adicionar colunas de preferências de usuário na tabela USERS
Execute este script no Oracle para adicionar as colunas necessárias
*/

-- Adicionar colunas de preferências de usuário
ALTER TABLE RELBACK.USERS ADD (
    THEME_PREFERENCE VARCHAR2(20) DEFAULT 'light' NOT NULL,
    LANGUAGE_PREFERENCE VARCHAR2(10) DEFAULT 'en' NOT NULL,
    NOTIFICATIONS_ENABLED NUMBER(1) DEFAULT 1 NOT NULL
);

-- Adicionar constraints para validar os valores
ALTER TABLE RELBACK.USERS ADD CONSTRAINT CK_USERS_THEME_PREFERENCE 
    CHECK (THEME_PREFERENCE IN ('light', 'dark', 'auto'));

ALTER TABLE RELBACK.USERS ADD CONSTRAINT CK_USERS_LANGUAGE_PREFERENCE 
    CHECK (LANGUAGE_PREFERENCE IN ('en', 'pt'));

ALTER TABLE RELBACK.USERS ADD CONSTRAINT CK_USERS_NOTIFICATIONS_ENABLED 
    CHECK (NOTIFICATIONS_ENABLED IN (0, 1));

-- Comentários das colunas
COMMENT ON COLUMN RELBACK.USERS.THEME_PREFERENCE IS 'User interface theme preference: light, dark, or auto';
COMMENT ON COLUMN RELBACK.USERS.LANGUAGE_PREFERENCE IS 'User language preference: en (English) or pt (Portuguese)';
COMMENT ON COLUMN RELBACK.USERS.NOTIFICATIONS_ENABLED IS 'Enable/disable notifications: 1 = enabled, 0 = disabled';

COMMIT;
