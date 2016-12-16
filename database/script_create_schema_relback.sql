
/*

Alter diskgroup or filesystem of Datafile destination

*/

CREATE TABLESPACE "TBS_RELBACK" DATAFILE '+DATA' SIZE 64M AUTOEXTEND ON NEXT 64M MAXSIZE 1024M 
LOGGING EXTENT MANAGEMENT LOCAL SEGMENT SPACE MANAGEMENT AUTO;

CREATE USER RELBACK IDENTIFIED BY "relback" DEFAULT TABLESPACE TBS_RELBACK QUOTA UNLIMITED ON TBS_RELBACK ACCOUNT UNLOCK ;

GRANT CREATE SESSION, UNLIMITED TABLESPACE TO RELBACK ;
GRANT CREATE VIEW TO RELBACK;
GRANT CREATE MATERIALIZED VIEW TO RELBACK;

GRANT SELECT ON RMAN.RC_RMAN_BACKUP_JOB_DETAILS TO RELBACK ;
GRANT SELECT ON RMAN.RC_RMAN_BACKUP_SUBJOB_DETAILS TO RELBACK ;
GRANT SELECT ON RMAN.RC_DATABASE TO RELBACK ;
GRANT SELECT ON RMAN.RC_RMAN_STATUS TO RELBACK ;
GRANT SELECT ON RMAN.RC_RMAN_OUTPUT TO RELBACK ;

CREATE SEQUENCE RELBACK.BACKUP_POLICIES_PK_SEQ01 INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 NOCACHE ;
CREATE SEQUENCE RELBACK.CLIENTS_PK_SEQ01 INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 NOCACHE ;
CREATE SEQUENCE RELBACK.DATABASES_PK_SEQ01 INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 NOCACHE ;
CREATE SEQUENCE RELBACK.HOSTS_PK_SEQ01 INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 NOCACHE ;
CREATE SEQUENCE RELBACK.USERS_PK_SEQ01 INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 NOCACHE ;

/*
Create tables of relBack
*/

CREATE TABLE RELBACK.BACKUP_POLICIES
  (
    ID_POLICY       NUMBER (38) NOT NULL ,
    POLICY_NAME     VARCHAR2 (150) ,
    ID_CLIENT       NUMBER (38) NOT NULL ,
    ID_DATABASE     NUMBER (38) NOT NULL ,
    ID_HOST         NUMBER (38) NOT NULL ,
    BACKUP_TYPE     VARCHAR2 (30) NOT NULL ,
    DESTINATION     VARCHAR2 (8) NOT NULL ,
    MINUTE          VARCHAR2 (100) DEFAULT '0' NOT NULL ,
    HOUR            VARCHAR2 (100) DEFAULT '*' NOT NULL ,
    DAY             VARCHAR2 (100) DEFAULT '*' NOT NULL ,
    MONTH           VARCHAR2 (100) DEFAULT '*' NOT NULL ,
    DAY_WEEK        VARCHAR2 (100) DEFAULT '*' NOT NULL ,
    DURATION        NUMBER NOT NULL ,
    SIZE_BACKUP     VARCHAR2 (10) NOT NULL ,
    STATUS          VARCHAR2 (8) DEFAULT 'ACTIVE' NOT NULL ,
    DESCRIPTION     VARCHAR2 (100) ,
    CREATED_ID_USER NUMBER NOT NULL ,
    CREATED_AT      DATE ,
    UPDATED_ID_USER NUMBER ,
    UPDATED_AT      DATE
  )
  TABLESPACE TBS_RELBACK LOGGING ;
ALTER TABLE RELBACK.BACKUP_POLICIES ADD CONSTRAINT POLITICA_DE_BACKUP_CK2 CHECK ( UPPER("BACKUP_TYPE")='ARCHIVELOG' OR UPPER("BACKUP_TYPE")='DB FULL' OR UPPER("BACKUP_TYPE")='DB INCR' OR UPPER("BACKUP_TYPE")='RECVR AREA' OR UPPER("BACKUP_TYPE")='ARCHIVELOG' OR UPPER("BACKUP_TYPE")='BACKUPSET') ;
ALTER TABLE RELBACK.BACKUP_POLICIES ADD CONSTRAINT POLITICA_DE_BACKUP_CK3 CHECK ( UPPER("DESTINATION")='DISK' OR UPPER("DESTINATION")='SBT_TAPE' OR UPPER("DESTINATION")='*') ;
ALTER TABLE RELBACK.BACKUP_POLICIES ADD CONSTRAINT POLITICA_DE_BACKUP_CK1 CHECK ( upper(status) IN ('ACTIVE','INACTIVE')) ;
CREATE UNIQUE INDEX RELBACK.IDX_BACKUP_POLICY_PK ON RELBACK.BACKUP_POLICIES ( ID_POLICY ASC ) TABLESPACE TBS_RELBACK LOGGING ;
ALTER TABLE RELBACK.BACKUP_POLICIES ADD CONSTRAINT BACKUP_POLICIES_PK PRIMARY KEY ( ID_POLICY ) USING INDEX RELBACK.IDX_BACKUP_POLICY_PK ;


CREATE TABLE RELBACK.DATABASES
  (
    ID_DATABASE     NUMBER (38) NOT NULL ,
    ID_CLIENT       NUMBER (38) NOT NULL ,
    ID_HOST         NUMBER NOT NULL ,
    DB_NAME         VARCHAR2 (20) NOT NULL ,
    DESCRIPTION     VARCHAR2 (100) NOT NULL ,
    LAST_RESYNC     DATE ,
    CREATED_ID_USER NUMBER NOT NULL ,
    CREATED_AT      DATE ,
    UPDATED_ID_USER NUMBER ,
    UPDATED_AT      DATE ,
    DBID            NUMBER NOT NULL
  )
  TABLESPACE TBS_RELBACK LOGGING ;
CREATE UNIQUE INDEX RELBACK.IDX_DATABASE_PK ON RELBACK.DATABASES
  (
    ID_DATABASE ASC , ID_CLIENT ASC , ID_HOST ASC
  )
  TABLESPACE TBS_RELBACK LOGGING ;
ALTER TABLE RELBACK.DATABASES ADD CONSTRAINT DATABASES_PK PRIMARY KEY ( ID_DATABASE, ID_CLIENT, ID_HOST ) USING INDEX RELBACK.IDX_DATABASE_PK ;


CREATE TABLE RELBACK.HOSTS
  (
    ID_HOST         NUMBER NOT NULL ,
    HOSTNAME        VARCHAR2 (100) NOT NULL ,
    DESCRIPTION     VARCHAR2 (100) NOT NULL ,
    IP              VARCHAR2 (15) NOT NULL ,
    ID_CLIENT       NUMBER (38) NOT NULL ,
    CREATED_ID_USER NUMBER NOT NULL ,
    CREATED_AT      DATE ,
    UPDATED_ID_USER NUMBER ,
    UPDATED_AT      DATE
  )
  TABLESPACE TBS_RELBACK LOGGING ;
CREATE UNIQUE INDEX RELBACK.IDX_HOST_PK ON RELBACK.HOSTS
  (
    ID_HOST ASC
  )
  TABLESPACE TBS_RELBACK LOGGING ;
ALTER TABLE RELBACK.HOSTS ADD CONSTRAINT HOSTS_PK PRIMARY KEY ( ID_HOST ) USING INDEX RELBACK.IDX_HOST_PK ;


CREATE GLOBAL TEMPORARY TABLE RELBACK.CRON_MONTH ( ID_POLICY NUMBER (38) NOT NULL , MONTH NUMBER (38) NOT NULL ) ON COMMIT PRESERVE ROWS ;
CREATE UNIQUE INDEX RELBACK.CRON_MONTH_IDX ON RELBACK.CRON_MONTH ( ID_POLICY ASC , MONTH ASC ) ;
  GRANT
  SELECT ON RELBACK.CRON_MONTH TO RMAN ;
ALTER TABLE RELBACK.CRON_MONTH ADD CONSTRAINT CRON_MONTH_PK PRIMARY KEY ( ID_POLICY, MONTH ) USING INDEX RELBACK.CRON_MONTH_IDX ;


CREATE GLOBAL TEMPORARY TABLE RELBACK.CRON_DAY_WEEK ( ID_POLICY NUMBER (38) NOT NULL , DAY_WEEK NUMBER (38) NOT NULL ) ON COMMIT PRESERVE ROWS ;
  ALTER TABLE RELBACK.CRON_DAY_WEEK ADD CONSTRAINT CHK_DAY_WEEK CHECK ( "DAY_WEEK">=0 AND "DAY_WEEK"<=6) ;
  CREATE INDEX RELBACK.CRON_DAY_WEEK_IDX ON RELBACK.CRON_DAY_WEEK
    (
      ID_POLICY ASC ,
      DAY_WEEK ASC
    ) ;
ALTER TABLE RELBACK.CRON_DAY_WEEK ADD CONSTRAINT CRON_DAY_WEEK_PK PRIMARY KEY ( ID_POLICY, DAY_WEEK ) USING INDEX RELBACK.CRON_DAY_WEEK_IDX ;


CREATE GLOBAL TEMPORARY TABLE RELBACK.CRON_DAY ( ID_POLICY NUMBER (38) NOT NULL , DAY NUMBER (38) NOT NULL ) ON COMMIT PRESERVE ROWS ;
  ALTER TABLE RELBACK.CRON_DAY ADD CONSTRAINT CRON_DAY_CK CHECK ( "DAY">=1 AND "DAY"<=31) ;
  CREATE INDEX RELBACK.CRON_DAY_IDX ON RELBACK.CRON_DAY
    (
      ID_POLICY ASC ,
      DAY ASC
    ) ;
ALTER TABLE RELBACK.CRON_DAY ADD CONSTRAINT CRON_DAY_PK PRIMARY KEY ( ID_POLICY, DAY ) USING INDEX RELBACK.CRON_DAY_IDX ;


CREATE GLOBAL TEMPORARY TABLE RELBACK.CRON_HOUR ( ID_POLICY NUMBER (38) NOT NULL , HOUR NUMBER (38) NOT NULL ) ON COMMIT PRESERVE ROWS ;
  ALTER TABLE RELBACK.CRON_HOUR ADD CONSTRAINT CRON_HOUR_CK CHECK ( "HOUR">=0 AND "HOUR"<=23) ;
CREATE UNIQUE INDEX RELBACK.CRON_HOUR_IDX ON RELBACK.CRON_HOUR ( ID_POLICY ASC , HOUR ASC ) ;
ALTER TABLE RELBACK.CRON_HOUR ADD CONSTRAINT CRON_HOUR_PK PRIMARY KEY ( ID_POLICY, HOUR ) USING INDEX RELBACK.CRON_HOUR_IDX ;


CREATE GLOBAL TEMPORARY TABLE RELBACK.CRON_MINUTE ( ID_POLICY NUMBER (38) NOT NULL , MINUTE NUMBER (38) NOT NULL ) ON COMMIT PRESERVE ROWS ;
  ALTER TABLE RELBACK.CRON_MINUTE ADD CONSTRAINT CRON_MINUTE_CK CHECK ( "MINUTE">=0 AND "MINUTE"<=59) ;
CREATE UNIQUE INDEX RELBACK.CRON_MINUTE_IDX ON RELBACK.CRON_MINUTE ( ID_POLICY ASC , MINUTE ASC ) ;
ALTER TABLE RELBACK.CRON_MINUTE ADD CONSTRAINT CRON_MINUTE_PK PRIMARY KEY ( ID_POLICY, MINUTE ) USING INDEX RELBACK.CRON_MINUTE_IDX ;


CREATE TABLE RELBACK.SCHEDULES
  (
    ID_POLICY      NUMBER (38) NOT NULL ,
    SCHEDULE_START DATE NOT NULL
  )
  TABLESPACE TBS_RELBACK LOGGING ;
COMMENT ON COLUMN RELBACK.SCHEDULES.ID_POLICY
IS
  'IDENTIFY POLICY ' ;
  COMMENT ON COLUMN RELBACK.SCHEDULES.SCHEDULE_START
IS
  'DATE SCHEDULE START' ;
CREATE UNIQUE INDEX RELBACK.IDX_SCHEDULE ON RELBACK.SCHEDULES
  (
    ID_POLICY ASC , SCHEDULE_START ASC
  )
  TABLESPACE TBS_RELBACK LOGGING ;
ALTER TABLE RELBACK.SCHEDULES ADD CONSTRAINT SCHEDULE_PK PRIMARY KEY ( ID_POLICY, SCHEDULE_START ) USING INDEX RELBACK.IDX_SCHEDULE ;

CREATE TABLE RELBACK.CLIENTS
  (
    ID_CLIENT       NUMBER (38) NOT NULL ,
    NAME            VARCHAR2 (100) ,
    DESCRIPTION     VARCHAR2 (200) ,
    CREATED_ID_USER NUMBER NOT NULL ,
    CREATED_AT      DATE NOT NULL ,
    UPDATED_ID_USER NUMBER ,
    UPDATED_AT      DATE
  )
  TABLESPACE TBS_RELBACK LOGGING ;
COMMENT ON COLUMN RELBACK.CLIENTS.NAME
IS
  'Field client name -  client/customer can be internal or external customer in the company.' ;
CREATE UNIQUE INDEX RELBACK.CLIENTS_PK ON RELBACK.CLIENTS
  (
    ID_CLIENT ASC
  )
  TABLESPACE TBS_RELBACK LOGGING ;
ALTER TABLE RELBACK.CLIENTS ADD CONSTRAINT CLIENTS_PK PRIMARY KEY ( ID_CLIENT ) USING INDEX RELBACK.CLIENTS_PK ;


CREATE GLOBAL TEMPORARY TABLE RELBACK.CRON_YEAR ( ID_POLICY NUMBER (38) NOT NULL , YEAR NUMBER (38) NOT NULL ) ON COMMIT PRESERVE ROWS ;
CREATE UNIQUE INDEX RELBACK.CRON_YEAR__IDX ON RELBACK.CRON_YEAR ( ID_POLICY ASC , YEAR ASC ) ;
ALTER TABLE RELBACK.CRON_YEAR ADD CONSTRAINT CRON_YEAR_PK PRIMARY KEY ( ID_POLICY, YEAR ) USING INDEX RELBACK.CRON_YEAR__IDX ;


CREATE TABLE RELBACK.USERS
  (
    ID_USER        NUMBER CONSTRAINT NNC_USERS_ID_USER NOT NULL ,
    NAME           VARCHAR2 (50) ,
    USERNAME       VARCHAR2 (100) ,
    PASSWORD       VARCHAR2 (60) ,
    STATUS         NUMBER (*,0) DEFAULT 1 ,
    EMAIL          VARCHAR2 (150) ,
    REMEMBER_TOKEN VARCHAR2 (100) ,
    TIMESTAMPS     TIMESTAMP ,
    UPDATED_AT     TIMESTAMP ,
    CREATED_AT     TIMESTAMP
  )
  TABLESPACE TBS_RELBACK LOGGING ;
ALTER TABLE RELBACK.USERS ADD CONSTRAINT CK_USERS_STATUS CHECK ( STATUS IN (1, 2)) ;
CREATE UNIQUE INDEX RELBACK.USERS_PK ON RELBACK.USERS ( ID_USER ASC ) TABLESPACE TBS_RELBACK LOGGING ;
ALTER TABLE RELBACK.USERS ADD CONSTRAINT USERS_PK PRIMARY KEY ( ID_USER ) USING INDEX RELBACK.USERS_PK ;


ALTER TABLE RELBACK.BACKUP_POLICIES ADD CONSTRAINT BACKUP_POLICIES_DATABASES_FK FOREIGN KEY ( ID_DATABASE, ID_CLIENT, ID_HOST ) REFERENCES RELBACK.DATABASES ( ID_DATABASE, ID_CLIENT, ID_HOST ) ON
DELETE CASCADE NOT DEFERRABLE ;

ALTER TABLE RELBACK.BACKUP_POLICIES ADD CONSTRAINT BKP_POLICIES_USERS_CREATED_FK FOREIGN KEY ( CREATED_ID_USER ) REFERENCES RELBACK.USERS ( ID_USER ) NOT DEFERRABLE ;

ALTER TABLE RELBACK.BACKUP_POLICIES ADD CONSTRAINT BKP_POLICIES_USERS_UPDATED_FK FOREIGN KEY ( UPDATED_ID_USER ) REFERENCES RELBACK.USERS ( ID_USER ) NOT DEFERRABLE ;

ALTER TABLE RELBACK.CLIENTS ADD CONSTRAINT CLIENTS_USERS_CREATED_FK FOREIGN KEY ( CREATED_ID_USER ) REFERENCES RELBACK.USERS ( ID_USER ) NOT DEFERRABLE ;

ALTER TABLE RELBACK.CLIENTS ADD CONSTRAINT CLIENTS_USERS_UPDATED_FK FOREIGN KEY ( UPDATED_ID_USER ) REFERENCES RELBACK.USERS ( ID_USER ) NOT DEFERRABLE ;

ALTER TABLE RELBACK.DATABASES ADD CONSTRAINT DATABASES_CLIENTS_FK FOREIGN KEY ( ID_CLIENT ) REFERENCES RELBACK.CLIENTS ( ID_CLIENT ) ON
DELETE CASCADE NOT DEFERRABLE ;

ALTER TABLE RELBACK.DATABASES ADD CONSTRAINT DATABASES_HOSTS_FK FOREIGN KEY ( ID_HOST ) REFERENCES RELBACK.HOSTS ( ID_HOST ) ON
DELETE CASCADE NOT DEFERRABLE ;

ALTER TABLE RELBACK.DATABASES ADD CONSTRAINT DATABASES_USERS_CREATED_FK FOREIGN KEY ( CREATED_ID_USER ) REFERENCES RELBACK.USERS ( ID_USER ) NOT DEFERRABLE ;

ALTER TABLE RELBACK.DATABASES ADD CONSTRAINT DATABASES_USERS_UPDATED_FK FOREIGN KEY ( UPDATED_ID_USER ) REFERENCES RELBACK.USERS ( ID_USER ) NOT DEFERRABLE ;

ALTER TABLE RELBACK.HOSTS ADD CONSTRAINT HOSTS_CLIENTS_FK FOREIGN KEY ( ID_CLIENT ) REFERENCES RELBACK.CLIENTS ( ID_CLIENT ) ON
DELETE CASCADE NOT DEFERRABLE ;

ALTER TABLE RELBACK.HOSTS ADD CONSTRAINT HOSTS_USERS_CREATED_FK FOREIGN KEY ( CREATED_ID_USER ) REFERENCES RELBACK.USERS ( ID_USER ) NOT DEFERRABLE ;

ALTER TABLE RELBACK.HOSTS ADD CONSTRAINT HOSTS_USERS_UPDATED_FK FOREIGN KEY ( UPDATED_ID_USER ) REFERENCES RELBACK.USERS ( ID_USER ) NOT DEFERRABLE ;



/*
Create StoredProcedure that create SCHEDULE of Backup Policies
*/

CREATE OR REPLACE PROCEDURE                         RELBACK.SP_CREATE_SCHEDULE
(
  p_date    IN date         --DEFAULT trunc(sysdate)-3
)
AS
        cursor c_policy    is
    select
       bp.ID_POLICY,
       upper(d.DB_NAME) DB_NAME,
       upper(h.HOSTNAME) HOSTNAME,
       bp.BACKUP_TYPE,
       bp.DESTINATION,
       bp.MINUTE,
       bp.HOUR,
       bp.DAY,
       bp.MONTH,
       bp.DAY_WEEK,
       bp.DURATION,
       bp.SIZE_BACKUP,
       bp.STATUS
    from
       relback.backup_policies bp
        inner join relback.databases d on (bp.ID_DATABASE = d.ID_DATABASE)
        inner join relback.hosts h on (bp.ID_HOST = h.ID_HOST)
    where
       upper(STATUS) = 'ACTIVE'
    order by
      bp.ID_POLICY;

        v_policy c_policy%ROWTYPE;

        v_minute          varchar2(2000);
        v_count_comma     integer;
        v_count_hyphen    integer;
        v_start_field     integer;
        v_end_field       integer;
        v_field           varchar2(200);
        v_hour            varchar2(10);
        v_day             varchar2(10);
        v_month           varchar2(10);
        v_day_week        varchar2(10);

        cursor c_cron_month       is     select id_policy, month        from cron_month         where id_policy = v_policy.id_policy;
        v_cron_month        c_cron_month%rowtype;

        cursor c_cron_day_week      is     select id_policy, day_week from cron_day_week  where id_policy = v_policy.id_policy;
        v_cron_day_week c_cron_day_week%rowtype;

        cursor c_cron_day           is     select id_policy, day        from cron_day         where id_policy = v_policy.id_policy ;
        v_cron_day        c_cron_day%rowtype;

        cursor c_cron_hour          is     select id_policy, hour       from cron_hour        where id_policy = v_policy.id_policy;
        v_cron_hour       c_cron_hour%rowtype;

        cursor c_cron_minute        is     select id_policy, minute     from cron_minute      where id_policy = v_policy.id_policy;
        v_cron_minute     c_cron_minute%rowtype;


        v_schedule_start   varchar2(100);
        v_seconds_e      number;
        v_seconds_r      number;

-------------------------------------------------------------------------------------------------
-- Start
-------------------------------------------------------------------------------------------------
begin

     open c_policy;
      loop
        fetch c_policy into v_policy;
             exit when c_policy%notfound;

       --dbms_output.put_line('1.v_policy..: ' || v_policy.id_policy);

----------------------------------------------------------------------------------------------------------------------------------------------------
--                                                                            month
----------------------------------------------------------------------------------------------------------------------------------------------------

           v_count_comma := REGEXP_COUNT(v_policy.month,',');

           if v_count_comma > 0 then
            v_start_field := 1;
            --dbms_output.put_line(v_policy.month);
            for i in 1..v_count_comma +1
            loop
              v_end_field := instr(v_policy.month,',',1,i) -1;
              if v_end_field  < 1 then
               v_end_field := length(v_policy.month);
              end if;
              v_field := substr(v_policy.month, v_start_field, v_end_field - v_start_field +1);
              v_count_hyphen := REGEXP_COUNT(v_field,'-');
              if v_count_hyphen > 0 then
                for k in to_number(substr(v_field,1,instr(v_field,'-')-1)) .. to_number(substr(v_field,instr(v_field,'-')+1))
                loop
                  v_month := lpad(to_char(k),2,0);
                  --dbms_output.put_line('1.v_month..........: ' || v_month);
                  insert into cron_month (id_policy, month) values (v_policy.id_policy, v_month);
                  commit;
                end loop;
              else
               v_month := lpad(v_field,2,0);
               --dbms_output.put_line('2.v_month..........: ' || v_month);
               insert into cron_month (id_policy, month) values (v_policy.id_policy, v_month);
               commit;
              end if;
              v_start_field := v_end_field+2;

            end loop;
           elsif  substr(v_policy.month,1,1) = '*' then
             for j in 1..12
               loop
                 v_month := lpad(to_char(j),2,0);
                  --dbms_output.put_line('3.v_month..........: ' || v_month ||' ... v_cp: ..' || v_policy.id_policy);
                  insert into cron_month (id_policy, month) values (v_policy.id_policy, v_month);
               end loop;
            elsif  instr(v_policy.month,'-') > 0 then
             for l in to_number(substr(v_policy.month,1,instr(v_policy.month,'-')-1)) .. to_number(substr(v_policy.month,instr(v_policy.month,'-')+1))
                loop
                  v_month := lpad(to_char(l),2,0);
                  --dbms_output.put_line('4.v_month..........: ' || v_month);
                  insert into cron_month (id_policy, month) values (v_policy.id_policy, v_month);
                  commit;
                end loop;
            else
              v_month := lpad(v_policy.day,2,0);
             --dbms_output.put_line('v_month..........: ' || v_month);
              insert into cron_month (id_policy, month) values (v_policy.id_policy, v_month);
              commit;
             end if;

----------------------------------------------------------------------------------------------------------------------------------------------------
--                                                                            day_week
----------------------------------------------------------------------------------------------------------------------------------------------------

           v_count_comma := REGEXP_COUNT(v_policy.day_week,',');

           if v_count_comma > 0 then
            v_start_field := 1;
            --dbms_output.put_line(v_policy.day_week);
            for i in 1..v_count_comma +1
            loop
              v_end_field := instr(v_policy.day_week,',',1,i) -1;
              if v_end_field  < 1 then
               v_end_field := length(v_policy.day_week);
              end if;
              v_field := substr(v_policy.day_week, v_start_field, v_end_field - v_start_field +1);
              v_count_hyphen := REGEXP_COUNT(v_field,'-');
              if v_count_hyphen > 0 then
                for k in to_number(substr(v_field,1,instr(v_field,'-')-1)) .. to_number(substr(v_field,instr(v_field,'-')+1))
                loop
                  v_day_week := lpad(to_char(k),2,0);
                  --dbms_output.put_line('v_day_week..........: ' || v_day_week);
                  insert into cron_day_week (id_policy, day_week) values (v_policy.id_policy, v_day_week);
                  commit;
                end loop;
              else
               v_day_week := lpad(v_field,2,0);
               --dbms_output.put_line('v_day_week..........: ' || v_day_week);
               insert into cron_day_week (id_policy, day_week) values (v_policy.id_policy, v_day_week);
               commit;
              end if;
              v_start_field := v_end_field+2;

            end loop;
           elsif  substr(v_policy.day_week,1,1) = '*' then
             --dbms_output.put_line(v_policy.day_week);
             for j in 0..6
               loop
                 v_day_week := lpad(to_char(j),2,0);
                 --dbms_output.put_line('v_day_week..........: ' ||  v_day_week);
                 insert into cron_day_week (id_policy, day_week) values (v_policy.id_policy, v_day_week);
                 commit;
               end loop;
            elsif  instr(v_policy.day_week,'-') > 0 then
             for l in to_number(substr(v_policy.day_week,1,instr(v_policy.day_week,'-')-1)) .. to_number(substr(v_policy.day_week,instr(v_policy.day_week,'-')+1))
                loop
                  v_day_week := lpad(to_char(l),2,0);
                  --dbms_output.put_line('v_day_week..........: ' || v_day_week);
                  insert into cron_day_week (id_policy, day_week) values (v_policy.id_policy, v_day_week);
                  commit;
                end loop;
            else
              v_day_week := lpad(v_policy.day_week,2,0);
              --dbms_output.put_line('v_day_week..........: ' || v_day_week);
              insert into cron_day_week (id_policy, day_week) values (v_policy.id_policy, v_day_week);
              commit;
             end if;

----------------------------------------------------------------------------------------------------------------------------------------------------
--                                                                            DAY
----------------------------------------------------------------------------------------------------------------------------------------------------

           v_count_comma := REGEXP_COUNT(v_policy.day,',');

           if v_count_comma > 0 then
            v_start_field := 1;
            --dbms_output.put_line(v_policy.day);
            for i in 1..v_count_comma +1
            loop
              v_end_field := instr(v_policy.day,',',1,i) -1;
              if v_end_field  < 1 then
               v_end_field := length(v_policy.day);
              end if;
              v_field := substr(v_policy.day, v_start_field, v_end_field - v_start_field +1);
              v_count_hyphen := REGEXP_COUNT(v_field,'-');
              if v_count_hyphen > 0 then
                for k in to_number(substr(v_field,1,instr(v_field,'-')-1)) .. to_number(substr(v_field,instr(v_field,'-')+1))
                loop
                  v_day := lpad(to_char(k),2,0);
                  --dbms_output.put_line('v_day..........: ' || v_day);
                  insert into cron_day (id_policy, day) values (v_policy.id_policy, v_day);
                  commit;
                end loop;
              else
               v_day := lpad(v_field,2,0);
               --dbms_output.put_line('v_day..........: ' || v_day);
               insert into cron_day (id_policy, day) values (v_policy.id_policy, v_day);
               commit;
              end if;
              v_start_field := v_end_field+2;

            end loop;
           elsif  substr(v_policy.day,1,1) = '*' then
             for j in 1..31
               loop
                 v_day := lpad(to_char(j),2,0);
                 --dbms_output.put_line('v_day..........: ' || v_day);
                 insert into cron_day (id_policy, day) values (v_policy.id_policy, v_day);
                 commit;
               end loop;
            elsif  instr(v_policy.day,'-') > 0 then
             for l in to_number(substr(v_policy.day,1,instr(v_policy.day,'-')-1)) .. to_number(substr(v_policy.day,instr(v_policy.day,'-')+1))
                loop
                  v_day := lpad(to_char(l),2,0);
                  --dbms_output.put_line('v_day..........: ' || v_day);
                  insert into cron_day (id_policy, day) values (v_policy.id_policy, v_day);
                  commit;
                end loop;
            else
              v_day := lpad(v_policy.day,2,0);
              --dbms_output.put_line('v_day..........: ' || v_day);
              insert into cron_day (id_policy, day) values (v_policy.id_policy, v_day);
              commit;
             end if;

----------------------------------------------------------------------------------------------------------------------------------------------------
--                                                                            HOUR
----------------------------------------------------------------------------------------------------------------------------------------------------

           v_count_comma := REGEXP_COUNT(v_policy.hour,',');

           if v_count_comma > 0 then
            v_start_field := 1;
            --dbms_output.put_line(v_policy.hour);
            for i in 1..v_count_comma +1
            loop
              v_end_field := instr(v_policy.hour,',',1,i) -1;
              if v_end_field  < 1 then
               v_end_field := length(v_policy.hour);
              end if;
              v_field := substr(v_policy.hour, v_start_field, v_end_field - v_start_field +1);
              v_count_hyphen := REGEXP_COUNT(v_field,'-');
              if v_count_hyphen > 0 then
                for k in to_number(substr(v_field,1,instr(v_field,'-')-1)) .. to_number(substr(v_field,instr(v_field,'-')+1))
                loop
                  v_hour := lpad(to_char(k),2,0);
                  --dbms_output.put_line('v_hour..........: ' || v_hour);
                  insert into cron_hour (id_policy, hour) values (v_policy.id_policy, v_hour);
                  commit;
                end loop;
              else
               v_hour := lpad(v_field,2,0);
               --dbms_output.put_line('v_hour..........: ' || v_hour);
               insert into cron_hour (id_policy, hour) values (v_policy.id_policy, v_hour);
               commit;
              end if;
              v_start_field := v_end_field+2;

            end loop;
           elsif  substr(v_policy.hour,1,1) = '*' then
             for j in 0..23
               loop
                 v_hour := lpad(to_char(j),2,0);
                 --dbms_output.put_line('v_hour..........: ' || v_hour);
                 insert into cron_hour (id_policy, hour) values (v_policy.id_policy, v_hour);
                 commit;
               end loop;
            elsif  instr(v_policy.hour,'-') > 0 then
             for l in to_number(substr(v_policy.hour,1,instr(v_policy.hour,'-')-1)) .. to_number(substr(v_policy.hour,instr(v_policy.hour,'-')+1))
                loop
                  v_hour := lpad(to_char(l),2,0);
                 --dbms_output.put_line('v_hour..........: ' || v_hour);
                  insert into cron_hour (id_policy, hour) values (v_policy.id_policy, v_hour);
                  commit;
                end loop;
            else
              v_hour := lpad(v_policy.hour,2,0);
              --dbms_output.put_line('v_hour..........: ' || v_hour);
              insert into cron_hour (id_policy, hour) values (v_policy.id_policy, v_hour);
              commit;
             end if;

----------------------------------------------------------------------------------------------------------------------------------------------------
--                                                                            Minute
----------------------------------------------------------------------------------------------------------------------------------------------------
           v_count_comma := REGEXP_COUNT(v_policy.minute,',');

           if v_count_comma > 0 then
            v_start_field := 1;
             --dbms_output.put_line(v_policy.minute);
            for i in 1..v_count_comma +1
            loop
              v_end_field := instr(v_policy.minute,',',1,i) -1;
              if v_end_field  < 1 then
               v_end_field := length(v_policy.minute);
              end if;
              v_field := substr(v_policy.minute, v_start_field, v_end_field - v_start_field +1);
              v_count_hyphen := REGEXP_COUNT(v_field,'-');
              if v_count_hyphen > 0 then
                for k in to_number(substr(v_field,1,instr(v_field,'-')-1)) .. to_number(substr(v_field,instr(v_field,'-')+1))
                loop
                  v_minute := lpad(to_char(k),2,0);
                  --dbms_output.put_line('v_minute..........: ' || v_minute);
                  insert into cron_minute (id_policy, minute) values (v_policy.id_policy, v_minute);
                  commit;
                end loop;
              else
               v_minute := lpad(v_field,2,0);
               --dbms_output.put_line('v_minute..........: ' || v_minute);
               insert into cron_minute (id_policy, minute) values (v_policy.id_policy, v_minute);
               commit;
              end if;
              v_start_field := v_end_field+2;

            end loop;
           elsif  substr(v_policy.minute,1,1) = '*' then
             for j in 0 .. 59
               loop
                 v_minute := lpad(to_char(j),2,0);
                 --dbms_output.put_line('v_minute..........: ' || v_minute);
                 insert into cron_minute (id_policy, minute) values (v_policy.id_policy, v_minute);
                 commit;

               end loop;
            elsif  instr(v_policy.minute,'-') > 0 then
             for l in to_number(substr(v_policy.minute,1,instr(v_policy.minute,'-')-1)) .. to_number(substr(v_policy.minute,instr(v_policy.minute,'-')+1))
                loop
                  v_minute := lpad(to_char(l),2,0);
                  --dbms_output.put_line('v_minute..........: ' || v_minute);
                  insert into cron_minute (id_policy, minute) values (v_policy.id_policy, v_minute);
                  commit;
                end loop;
            else
              v_minute := lpad(v_policy.minute,2,0);
              --dbms_output.put_line('v_minute..........: ' || v_minute);
              insert into cron_minute (id_policy, minute) values (v_policy.id_policy, v_minute);
              commit;
             end if;

      end loop;
      close c_policy;
 ---------------------------------------------------------------------------------------------------------------------------------------
      delete from SCHEDULES;
      commit;

      open c_policy;
        loop
            fetch c_policy into v_policy;
            --dbms_output.put_line('id_policy:...' || v_policy.id_policy);
            exit when c_policy%notfound;

        open c_cron_month;
        loop
            fetch c_cron_month into v_cron_month;
            --dbms_output.put_line('month:...' || v_cron_month.month);
            exit when c_cron_month%notfound;

             open c_cron_day;
             loop
               fetch c_cron_day into v_cron_day;
               exit when c_cron_day%notfound;

                 v_schedule_start := lpad(v_cron_month.month,2,0) || '-' || to_char(p_date, 'yyyy');
                 --dbms_output.put_line('v_schedule_start:...' || v_schedule_start);

                 if to_number(to_char(last_day(to_date(v_schedule_start,'mm-yyyy')),'dd')) >=  to_number(v_cron_day.day) then
                  open c_cron_hour;
                   loop
                     fetch c_cron_hour into v_cron_hour;
                     exit when c_cron_hour%notfound;
                     open c_cron_minute;
                     loop
                       fetch c_cron_minute into v_cron_minute;
                       exit when c_cron_minute%notfound;
                         open c_cron_day_week;
                         loop
                           fetch c_cron_day_week into v_cron_day_week;
                           exit when c_cron_day_week%notfound;
                           v_schedule_start := lpad(v_cron_day.day,2,0) || '-' || lpad(v_cron_month.month,2,0) || '-' || to_char(p_date, 'yyyy') || ' ' || lpad(v_cron_hour.hour,2,0) || ':' || lpad(v_cron_minute.minute,2,0);
                           --dbms_output.put_line('id_policy: ' || v_policy.id_policy || ' date: ' || to_date(v_schedule_start,'dd-mm-yyyy hh24:mi'));
                           if  to_number(to_char(to_date(v_schedule_start,'dd-mm-yyyy hh24:mi'),'D')) - 1 = to_number(to_char(v_cron_day_week.day_week)) and
                               to_date(v_schedule_start,'dd-mm-yyyy hh24:mi') < trunc(sysdate) + 1 then
                               if to_date(v_schedule_start,'dd-mm-yyyy hh24:mi') between p_date and trunc(sysdate) + 1 then
                                 insert into schedules (id_policy, schedule_start) values (v_policy.id_policy, to_date(v_schedule_start,'dd-mm-yyyy hh24:mi'));
                                 commit;
                                 --dbms_output.put_line('id_policy: ' || v_policy.id_policy || ' date: ' || to_date(v_schedule_start,'dd-mm-yyyy hh24:mi'));
                               end if;
                          end if;
                        end loop;
                        close c_cron_day_week;
                    end loop;
                    close c_cron_minute;
                  end loop;
                  close c_cron_hour;
               end if;
            end loop;
            close c_cron_day;
        end loop;
        close c_cron_month;
    end loop;
    close c_policy;

--exception
 -- when OTHERS then
--    raise;

END SP_CREATE_SCHEDULE;
/

/*
Insert default user of relBack - user: admin password: admin123
*/

Insert into RELBACK.USERS (ID_USER,NAME,USERNAME,PASSWORD,STATUS,EMAIL,REMEMBER_TOKEN,TIMESTAMPS,UPDATED_AT,CREATED_AT) values ('1','administrator','admin','$2y$10$zEL2U58nEERFSG.O4kp47.MKH.bvsYjl25lFQLNNSJIbqFRt9abVi','1',null,'TxYX1tcMY0oRbLO7Siqq7yatYFxLKFPwOYEcvmNhvDFAmw7pNJhpsruMePnD',null,to_timestamp('15/11/25 18:03:00','DD/MM/RR HH24:MI:SS'),null);
COMMIT;


CREATE VIEW "RELBACK"."VW_RMAN_BACKUP_JOB_DETAILS" ("DB_NAME",
  "DBID", "DB_KEY", "START_TIME", "END_TIME", "STATUS", "TIME_TAKEN_DISPLAY",
  "OUTPUT_BYTES_DISPLAY", "OUTPUT_DEVICE_TYPE", "SESSION_KEY", "SESSION_RECID",
  "SESSION_STAMP", "INPUT_TYPE")
AS
  SELECT
    RBJD.db_name,
    D.dbid,
    D.db_key,
    RBJD.start_time,
    RBJD.end_time,
    RBJD.status,
    RBJD.time_taken_display,
    RBJD.output_bytes_display,
    RBJD.output_device_type,
    RBJD.session_key,
    RBJD.session_recid,
    RBJD.session_stamp,
    RBJD.input_type
  FROM
    RMAN.RC_RMAN_BACKUP_JOB_DETAILS RBJD
  JOIN RMAN.RC_DATABASE D
  ON
    (
      RBJD.DB_KEY    = D.DB_KEY
    AND RBJD.DB_NAME = D.NAME
    );
/    

CREATE VIEW "RELBACK"."VW_RMAN_BACKUP_SUBJOB_DETAILS" (
  "DB_NAME", "DBID", "OPERATION", "INPUT_TYPE", "STATUS", "SESSION_STAMP")
AS
  SELECT
    RBSD.db_name,
    RBSD.db_key,
    RBSD.operation,
    RBSD.input_type,
    RBSD.status,
    RBSD.session_stamp
  FROM
    RMAN.RC_RMAN_BACKUP_SUBJOB_DETAILS RBSD;
/    
  
CREATE VIEW "RELBACK"."VW_RMAN_OUTPUT" ("DB_KEY",
  "SESSION_KEY", "RECID", "STAMP", "OUTPUT")
AS
  SELECT
    RCRO.DB_KEY DB_KEY,
    RCRO.SESSION_KEY SESSION_KEY,
    RCRO.RECID RECID,
    RCRO.STAMP STAMP,
    RCRO.OUTPUT OUTPUT
  FROM
    RMAN.RC_RMAN_OUTPUT RCRO;
/    

CREATE OR REPLACE FORCE VIEW "RELBACK"."VW_BACKUP_POLICIES" ("ID_POLICY",
  "SCHEDULE_START", "HOSTNAME", "DB_NAME", "DBID", "DESTINATION", "BACKUP_TYPE"
  , "DURATION", "SIZE_BACKUP", "DESCRIPTION")
AS
  SELECT
    s.ID_POLICY,
    s.SCHEDULE_START,
    h.HOSTNAME,
    d.DB_NAME,
    d.DBID,
    b.DESTINATION,
    b.BACKUP_TYPE,
    b.DURATION,
    b.SIZE_BACKUP,
    b.DESCRIPTION
  FROM
    RELBACK.SCHEDULES s
  JOIN RELBACK.BACKUP_POLICIES b
  ON
    (
      s.ID_POLICY = b.ID_POLICY
    )
  JOIN RELBACK.HOSTS h
  ON
    (
      b.ID_HOST = h.ID_HOST
    )
  JOIN RELBACK.DATABASES d
  ON
    (
      b.ID_DATABASE = d.ID_DATABASE
    ) ;
/

CREATE OR REPLACE FORCE VIEW "RELBACK"."VW_RMAN_DATABASE" ("DB_KEY",
  "DBINC_KEY", "DBID", "NAME", "RESETLOGS_CHANGE#", "RESETLOGS_TIME")
AS
  SELECT
    DB_KEY,
    DBINC_KEY,
    DBID,
    NAME,
    RESETLOGS_CHANGE#,
    RESETLOGS_TIME
  FROM
    RMAN.RC_DATABASE ;
  
CREATE OR REPLACE FORCE VIEW "RELBACK"."VW_RMAN_STATUS" ("DB_KEY", "DB_NAME",
  "ROW_LEVEL", "OPERATION", "OBJECT_TYPE", "STATUS", "SESSION_KEY",
  "SESSION_RECID")
AS
  SELECT
    RS.DB_KEY,
    RS.DB_NAME,
    RS.row_level,
    RS.operation,
    RS.object_type,
    RS.status,
    RS.session_key,
    RS.session_recid
  FROM
    RMAN.RC_RMAN_STATUS RS;

CREATE OR REPLACE TRIGGER RELBACK.DATABASES_TRG1 
    BEFORE INSERT ON RELBACK.DATABASES 
    FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING THEN
      SELECT DATABASES_PK_SEQ01.NEXTVAL INTO :NEW.ID_DATABASE FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END; 
/

/*
Create Triggers to insert PKs
*/

CREATE OR REPLACE TRIGGER RELBACK.BACKUP_POLICIES_TRG1 BEFORE
  INSERT ON RELBACK.BACKUP_POLICIES FOR EACH ROW WHEN (NEW.ID_POLICY IS NULL) BEGIN :NEW.ID_POLICY := RELBACK.BACKUP_POLICIES_PK_SEQ01.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER RELBACK.CLIENTS_TRG1 BEFORE
  INSERT ON RELBACK.CLIENTS FOR EACH ROW WHEN (NEW.ID_CLIENT IS NULL) BEGIN :NEW.ID_CLIENT := RELBACK.CLIENTS_PK_SEQ01.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER RELBACK.HOSTS_TRG1 BEFORE
  INSERT ON RELBACK.HOSTS FOR EACH ROW WHEN (NEW.ID_HOST IS NULL) BEGIN :NEW.ID_HOST := RELBACK.HOSTS_PK_SEQ01.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER RELBACK.USERS_TRG1 BEFORE
  INSERT ON RELBACK.USERS FOR EACH ROW WHEN (NEW.ID_USER IS NULL) BEGIN :NEW.ID_USER := RELBACK.USERS_PK_SEQ01.NEXTVAL;
END;
/

/*
Update statistics of schema relBack
*/

EXECUTE DBMS_STATS.GATHER_SCHEMA_STATS(ownname => 'RELBACK');
--EXECUTE DBMS_STATS.GATHER_SCHEMA_STATS(ownname => 'RMAN');
