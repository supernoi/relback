(  p_data          IN date        , --  DEFAULT trunc(sysdate),
   p_tipo_execucao IN varchar2     DEFAULT 'MONITORAMENTO')
AS
        cursor c_politica    is
        select
           a.CODIGO_POLITICA,
           upper(a.DB_NAME) DB_NAME,
           upper(a.HOSTNAME) HOSTNAME,
           a.TIPO_BACKUP,
           a.DESTINO,
           a.MINUTO,
           a.HORA,
           a.DIA,
           a.MES,
           a.DIA_SEMANA,
           a.DURACAO,
           a.TAMANHO,
           a.STATUS
        from
           politica_backup a
       where
           upper(STATUS) = 'ATIVO';

        v_politica c_politica%ROWTYPE;
        
        v_minuto        varchar2(2000);
        v_qtd_virgulas  integer;
        v_qtd_traco     integer;
        v_inicio_campo  integer;
        v_fim_campo     integer;
        v_campo         varchar2(200);        
        v_hora          varchar2(10);
        v_dia           varchar2(10);
        v_mes           varchar2(10);
        v_dia_semana    varchar2(10);

        cursor c_cron_mes           is     select codigo_politica, mes        from cron_mes         where codigo_politica = v_politica.codigo_politica;
               --and mes between to_number(to_char(p_data,'mm')) and to_number(to_char(sysdate,'mm'));
        v_cron_mes        c_cron_mes%rowtype;

        cursor c_cron_dia_semana    is     select codigo_politica, dia_semana from cron_dia_semana  where codigo_politica = v_politica.codigo_politica;  -- and dia_semana = to_number(to_char(p_data,'D'));
        v_cron_dia_semana c_cron_dia_semana%rowtype;

        cursor c_cron_dia           is     select codigo_politica, dia        from cron_dia         where codigo_politica = v_politica.codigo_politica ;
        --and dia between  to_number(to_char(p_data,'dd'));
        v_cron_dia        c_cron_dia%rowtype;

        cursor c_cron_hora          is     select codigo_politica, hora       from cron_hora        where codigo_politica = v_politica.codigo_politica;
        v_cron_hora       c_cron_hora%rowtype;

        cursor c_cron_minuto        is     select codigo_politica, minuto     from cron_minuto      where codigo_politica = v_politica.codigo_politica;
        v_cron_minuto     c_cron_minuto%rowtype;


        v_inicio_backup   varchar2(100);
        v_segundos_e      number;
        v_segundos_r      number;

--------------------------------------------------------------------------------------------------------

    cursor c_monitora_backup is
    select
      pbv.codigo_politica                                                                                 pid,
      upper(substr(pbv.hostname,1,30))                                                                    hostname,
      upper(pbv.db_name)                                                                                  db_name,
      pbv.HORA_INICIO                                                                                     inicio_p,
      bjd.start_time                                                                                      inicio_r,
      decode(bjd.status,null,'AGENDADO',bjd.status)                                                       status,
      bjd.time_taken_display                                                                              duracao_r,
        TO_CHAR  (TRUNC(pbv.duracao/3600),'FM9900') || ':' ||
        TO_CHAR(TRUNC(MOD(pbv.duracao,3600)/60),'FM00') || ':' ||
        TO_CHAR(MOD(pbv.duracao,60),'FM00')                                                               duracao_e,
      trunc(decode(substr(bjd.output_bytes_display,-1,1),'M',
          to_number(substr(bjd.output_bytes_display,1,    length(bjd.output_bytes_display)-1)/1024),
          'G',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1)),
          'T',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1))*1024),2)   tamanho_r_gb,
      trunc(decode(substr(pbv.tamanho,-1,1),'M',
          to_number(substr(pbv.tamanho,1,    length(pbv.tamanho)-1)/1024),
          'G',to_number(substr(pbv.tamanho,1,length(pbv.tamanho)-1)),
          'T',to_number(substr(pbv.tamanho,1,length(pbv.tamanho)-1*1024))),2)                             tamanho_p_gb,
          pbv.destino                                                                                     destino,
         pbv.tipo_backup                                                                                  tipo,
      pbv.descricao                                                                                       descricao,
      bjd.last_resync                                                                                     last_resync
      from
  rman_common.rc_rman_backup_job_details bjd
right outer join politica_backup_vw pbv on (
            upper(bjd.db_name)                                                            = upper(pbv.db_name)          and
            upper(bjd.hostname)                                                           = upper(pbv.hostname)         and
      /* #1 upper(bjd.output_device_type)                                                 = upper(pbv.destino)          and*/   
            upper(decode(bjd.output_device_type,null,'SBT_TAPE',bjd.output_device_type))  = upper(pbv.destino)          and
            upper(bjd.input_type)                                                         = upper(pbv.tipo_backup)      and 
            bjd.start_time between  pbv.HORA_INICIO - 1/24/4 and
                                    pbv.HORA_INICIO + 1/24/4)
where
     pbv.hora_inicio between  trunc(p_data) and sysdate
     
order by
     to_char(pbv.HORA_INICIO,   'yyyy-mm-dd hh24:mi:ss') desc;

v_monitora_backup      c_monitora_backup%rowtype;
l_titulo_cols          varchar2(500);
m                      integer;
v_cor                  varchar2(200);
v_status_monitoramento varchar2(5) := 'OK';
v_last_resync          date;
--v_data_atual           varchar2(11);
v_data_atual           date;
k                      integer;
v_estilo               varchar2(200);
v_id                   number := 0;
v_duracao_r            number := 0;
v_rate                 varchar2(10);

-------------------------------------------------------------------------------------------------
-- INICIO
-------------------------------------------------------------------------------------------------
begin
     dbms_output.enable(2000000);

     open c_politica;
      loop
             fetch c_politica into v_politica;
             exit when c_politica%notfound;

----------------------------------------------------------------------------------------------------------------------------------------------------
--                                                                            MES
----------------------------------------------------------------------------------------------------------------------------------------------------

           v_qtd_virgulas := REGEXP_COUNT(v_politica.mes,',');

           if v_qtd_virgulas > 0 then
            v_inicio_campo := 1;
            --dbms_output.put_line(v_politica.mes);
            for i in 1..v_qtd_virgulas +1
            loop
              v_fim_campo := instr(v_politica.mes,',',1,i) -1;
              if v_fim_campo  < 1 then
               v_fim_campo := length(v_politica.mes);
              end if;
              v_campo := substr(v_politica.mes, v_inicio_campo, v_fim_campo - v_inicio_campo +1);
              v_qtd_traco := REGEXP_COUNT(v_campo,'-');
              if v_qtd_traco > 0 then
                for k in to_number(substr(v_campo,1,instr(v_campo,'-')-1)) .. to_number(substr(v_campo,instr(v_campo,'-')+1))
                loop
                  v_mes := lpad(to_char(k),2,0);
                  --dbms_output.put_line('v_mes..........: ' || v_mes);
                  insert into cron_mes (codigo_politica, mes) values (v_politica.codigo_politica, v_mes);
                end loop;
              else
               v_mes := lpad(v_campo,2,0);
              --dbms_output.put_line('v_mes..........: ' || v_mes);
               insert into cron_mes (codigo_politica, mes) values (v_politica.codigo_politica, v_mes);
              end if;
              v_inicio_campo := v_fim_campo+2;

            end loop;
           elsif  substr(v_politica.mes,1,1) = '*' then
             for j in 1..12
               loop
                 v_mes := lpad(to_char(j),2,0);
                  --dbms_output.put_line('v_mes..........: ' || v_mes);
                 insert into cron_mes (codigo_politica, mes) values (v_politica.codigo_politica, v_mes);
               end loop;
            elsif  instr(v_politica.mes,'-') > 0 then
             for l in to_number(substr(v_politica.mes,1,instr(v_politica.mes,'-')-1)) .. to_number(substr(v_politica.mes,instr(v_politica.mes,'-')+1))
                loop
                  v_mes := lpad(to_char(l),2,0);
                 --dbms_output.put_line('v_mes..........: ' || v_mes);
                  insert into cron_mes (codigo_politica, mes) values (v_politica.codigo_politica, v_mes);
                end loop;
            else
              v_mes := lpad(v_politica.dia,2,0);
             --dbms_output.put_line('v_mes..........: ' || v_mes);
              insert into cron_mes (codigo_politica, mes) values (v_politica.codigo_politica, v_mes);
             end if;

----------------------------------------------------------------------------------------------------------------------------------------------------
--                                                                            DIA_SEMANA
----------------------------------------------------------------------------------------------------------------------------------------------------

           v_qtd_virgulas := REGEXP_COUNT(v_politica.dia_semana,',');

           if v_qtd_virgulas > 0 then
            v_inicio_campo := 1;
            --dbms_output.put_line(v_politica.dia_semana);
            for i in 1..v_qtd_virgulas +1
            loop
              v_fim_campo := instr(v_politica.dia_semana,',',1,i) -1;
              if v_fim_campo  < 1 then
               v_fim_campo := length(v_politica.dia_semana);
              end if;
              v_campo := substr(v_politica.dia_semana, v_inicio_campo, v_fim_campo - v_inicio_campo +1);
              v_qtd_traco := REGEXP_COUNT(v_campo,'-');
              if v_qtd_traco > 0 then
                for k in to_number(substr(v_campo,1,instr(v_campo,'-')-1)) .. to_number(substr(v_campo,instr(v_campo,'-')+1))
                loop
                  v_dia_semana := lpad(to_char(k),2,0);
                  --dbms_output.put_line('v_dia_semana..........: ' || v_dia_semana);
                  insert into cron_dia_semana (codigo_politica, dia_semana) values (v_politica.codigo_politica, v_dia_semana);
                end loop;
              else
               v_dia_semana := lpad(v_campo,2,0);
               --dbms_output.put_line('v_dia_semana..........: ' || v_dia_semana);
               insert into cron_dia_semana (codigo_politica, dia_semana) values (v_politica.codigo_politica, v_dia_semana);
              end if;
              v_inicio_campo := v_fim_campo+2;

            end loop;
           elsif  substr(v_politica.dia_semana,1,1) = '*' then
             --dbms_output.put_line(v_politica.dia_semana);
             for j in 0..6
               loop
                 v_dia_semana := lpad(to_char(j),2,0);
                 --dbms_output.put_line('v_dia_semana..........: ' ||  v_dia_semana);
                 insert into cron_dia_semana (codigo_politica, dia_semana) values (v_politica.codigo_politica, v_dia_semana);
               end loop;
            elsif  instr(v_politica.dia_semana,'-') > 0 then
             for l in to_number(substr(v_politica.dia_semana,1,instr(v_politica.dia_semana,'-')-1)) .. to_number(substr(v_politica.dia_semana,instr(v_politica.dia_semana,'-')+1))
                loop
                  v_dia_semana := lpad(to_char(l),2,0);
                  --dbms_output.put_line('v_dia_semana..........: ' || v_dia_semana);
                  insert into cron_dia_semana (codigo_politica, dia_semana) values (v_politica.codigo_politica, v_dia_semana);
                end loop;
            else
              v_dia_semana := lpad(v_politica.dia_semana,2,0);
              --dbms_output.put_line('v_dia_semana..........: ' || v_dia_semana);
              insert into cron_dia_semana (codigo_politica, dia_semana) values (v_politica.codigo_politica, v_dia_semana);
             end if;

----------------------------------------------------------------------------------------------------------------------------------------------------
--                                                                            DIA
----------------------------------------------------------------------------------------------------------------------------------------------------

           v_qtd_virgulas := REGEXP_COUNT(v_politica.dia,',');

           if v_qtd_virgulas > 0 then
            v_inicio_campo := 1;
            --dbms_output.put_line(v_politica.dia);
            for i in 1..v_qtd_virgulas +1
            loop
              v_fim_campo := instr(v_politica.dia,',',1,i) -1;
              if v_fim_campo  < 1 then
               v_fim_campo := length(v_politica.dia);
              end if;
              v_campo := substr(v_politica.dia, v_inicio_campo, v_fim_campo - v_inicio_campo +1);
              v_qtd_traco := REGEXP_COUNT(v_campo,'-');
              if v_qtd_traco > 0 then
                for k in to_number(substr(v_campo,1,instr(v_campo,'-')-1)) .. to_number(substr(v_campo,instr(v_campo,'-')+1))
                loop
                  v_dia := lpad(to_char(k),2,0);
                  --dbms_output.put_line('v_dia..........: ' || v_dia);
                  insert into cron_dia (codigo_politica, dia) values (v_politica.codigo_politica, v_dia);
                end loop;
              else
               v_dia := lpad(v_campo,2,0);
               --dbms_output.put_line('v_dia..........: ' || v_dia);
               insert into cron_dia (codigo_politica, dia) values (v_politica.codigo_politica, v_dia);
              end if;
              v_inicio_campo := v_fim_campo+2;

            end loop;
           elsif  substr(v_politica.dia,1,1) = '*' then
             for j in 1..31
               loop
                 v_dia := lpad(to_char(j),2,0);
                 --dbms_output.put_line('v_dia..........: ' || v_dia);
                 insert into cron_dia (codigo_politica, dia) values (v_politica.codigo_politica, v_dia);
               end loop;
            elsif  instr(v_politica.dia,'-') > 0 then
             for l in to_number(substr(v_politica.dia,1,instr(v_politica.dia,'-')-1)) .. to_number(substr(v_politica.dia,instr(v_politica.dia,'-')+1))
                loop
                  v_dia := lpad(to_char(l),2,0);
                  --dbms_output.put_line('v_dia..........: ' || v_dia);
                  insert into cron_dia (codigo_politica, dia) values (v_politica.codigo_politica, v_dia);
                end loop;
            else
              v_dia := lpad(v_politica.dia,2,0);
              --dbms_output.put_line('v_dia..........: ' || v_dia);
              insert into cron_dia (codigo_politica, dia) values (v_politica.codigo_politica, v_dia);
             end if;

----------------------------------------------------------------------------------------------------------------------------------------------------
--                                                                            HORA
----------------------------------------------------------------------------------------------------------------------------------------------------

           v_qtd_virgulas := REGEXP_COUNT(v_politica.hora,',');

           if v_qtd_virgulas > 0 then
            v_inicio_campo := 1;
            --dbms_output.put_line(v_politica.hora);
            for i in 1..v_qtd_virgulas +1
            loop
              v_fim_campo := instr(v_politica.hora,',',1,i) -1;
              if v_fim_campo  < 1 then
               v_fim_campo := length(v_politica.hora);
              end if;
              v_campo := substr(v_politica.hora, v_inicio_campo, v_fim_campo - v_inicio_campo +1);
              v_qtd_traco := REGEXP_COUNT(v_campo,'-');
              if v_qtd_traco > 0 then
                for k in to_number(substr(v_campo,1,instr(v_campo,'-')-1)) .. to_number(substr(v_campo,instr(v_campo,'-')+1))
                loop
                  v_hora := lpad(to_char(k),2,0);
                  --dbms_output.put_line('v_hora..........: ' || v_hora);
                  insert into cron_hora (codigo_politica, hora) values (v_politica.codigo_politica, v_hora);
                end loop;
              else
               v_hora := lpad(v_campo,2,0);
               --dbms_output.put_line('v_hora..........: ' || v_hora);
               insert into cron_hora (codigo_politica, hora) values (v_politica.codigo_politica, v_hora);
              end if;
              v_inicio_campo := v_fim_campo+2;

            end loop;
           elsif  substr(v_politica.hora,1,1) = '*' then
             for j in 0..23
               loop
                 v_hora := lpad(to_char(j),2,0);
                 --dbms_output.put_line('v_hora..........: ' || v_hora);
                 insert into cron_hora (codigo_politica, hora) values (v_politica.codigo_politica, v_hora);
               end loop;
            elsif  instr(v_politica.hora,'-') > 0 then
             for l in to_number(substr(v_politica.hora,1,instr(v_politica.hora,'-')-1)) .. to_number(substr(v_politica.hora,instr(v_politica.hora,'-')+1))
                loop
                  v_hora := lpad(to_char(l),2,0);
                 --dbms_output.put_line('v_hora..........: ' || v_hora);
                  insert into cron_hora (codigo_politica, hora) values (v_politica.codigo_politica, v_hora);
                end loop;
            else
              v_hora := lpad(v_politica.hora,2,0);
              --dbms_output.put_line('v_hora..........: ' || v_hora);
              insert into cron_hora (codigo_politica, hora) values (v_politica.codigo_politica, v_hora);
             end if;

----------------------------------------------------------------------------------------------------------------------------------------------------
--                                                                            MINUTO
----------------------------------------------------------------------------------------------------------------------------------------------------
           v_qtd_virgulas := REGEXP_COUNT(v_politica.minuto,',');

           if v_qtd_virgulas > 0 then
            v_inicio_campo := 1;
             --dbms_output.put_line(v_politica.minuto);
            for i in 1..v_qtd_virgulas +1
            loop
              v_fim_campo := instr(v_politica.minuto,',',1,i) -1;
              if v_fim_campo  < 1 then
               v_fim_campo := length(v_politica.minuto);
              end if;
              v_campo := substr(v_politica.minuto, v_inicio_campo, v_fim_campo - v_inicio_campo +1);
              v_qtd_traco := REGEXP_COUNT(v_campo,'-');
              if v_qtd_traco > 0 then
                for k in to_number(substr(v_campo,1,instr(v_campo,'-')-1)) .. to_number(substr(v_campo,instr(v_campo,'-')+1))
                loop
                  v_minuto := lpad(to_char(k),2,0);
                  --dbms_output.put_line('v_minuto..........: ' || v_minuto);
                  insert into cron_minuto (codigo_politica, minuto) values (v_politica.codigo_politica, v_minuto);
                end loop;
              else
               v_minuto := lpad(v_campo,2,0);
               --dbms_output.put_line('v_minuto..........: ' || v_minuto);
               insert into cron_minuto (codigo_politica, minuto) values (v_politica.codigo_politica, v_minuto);
              end if;
              v_inicio_campo := v_fim_campo+2;

            end loop;
           elsif  substr(v_politica.minuto,1,1) = '*' then
             for j in 0 .. 59
               loop
                 v_minuto := lpad(to_char(j),2,0);
                 --dbms_output.put_line('v_minuto..........: ' || v_minuto);
                 insert into cron_minuto (codigo_politica, minuto) values (v_politica.codigo_politica, v_minuto);

               end loop;
            elsif  instr(v_politica.minuto,'-') > 0 then
             for l in to_number(substr(v_politica.minuto,1,instr(v_politica.minuto,'-')-1)) .. to_number(substr(v_politica.minuto,instr(v_politica.minuto,'-')+1))
                loop
                  v_minuto := lpad(to_char(l),2,0);
                  --dbms_output.put_line('v_minuto..........: ' || v_minuto);
                  insert into cron_minuto (codigo_politica, minuto) values (v_politica.codigo_politica, v_minuto);
                end loop;
            else
              v_minuto := lpad(v_politica.minuto,2,0);
              --dbms_output.put_line('v_minuto..........: ' || v_minuto);
              insert into cron_minuto (codigo_politica, minuto) values (v_politica.codigo_politica, v_minuto);
             end if;

      end loop;
      close c_politica;
 ---------------------------------------------------------------------------------------------------------------------------------------
      delete from agenda;
      --delete from agenda1;
      open c_politica;
        loop
            fetch c_politica into v_politica;
            exit when c_politica%notfound;

        commit;
        open c_cron_mes;
        loop
            fetch c_cron_mes into v_cron_mes;
            exit when c_cron_mes%notfound;

             open c_cron_dia;
             loop
               fetch c_cron_dia into v_cron_dia;
               exit when c_cron_dia%notfound;

                 v_inicio_backup := lpad(v_cron_mes.mes,2,0) || '-' || to_char(p_data, 'yyyy');
                 --dbms_output.put_line(v_inicio_backup);

                 if to_number(to_char(last_day(to_date(v_inicio_backup,'mm-yyyy')),'dd')) >=  to_number(v_cron_dia.dia) then
                  open c_cron_hora;
                   loop
                     fetch c_cron_hora into v_cron_hora;
                     exit when c_cron_hora%notfound;
                     open c_cron_minuto;
                     loop
                       fetch c_cron_minuto into v_cron_minuto;
                       exit when c_cron_minuto%notfound;
                         open c_cron_dia_semana;
                         loop
                           fetch c_cron_dia_semana into v_cron_dia_semana;
                           exit when c_cron_dia_semana%notfound;
                           v_inicio_backup := lpad(v_cron_dia.dia,2,0) || '-' || lpad(v_cron_mes.mes,2,0) || '-' || to_char(p_data, 'yyyy') || ' ' || lpad(v_cron_hora.hora,2,0) || ':' || lpad(v_cron_minuto.minuto,2,0);
                           if  to_number(to_char(to_date(v_inicio_backup,'dd-mm-yyyy hh24:mi'),'D')) -1 = to_number(to_char(v_cron_dia_semana.dia_semana)) and
                               to_date(v_inicio_backup,'dd-mm-yyyy hh24:mi') < trunc(sysdate) + 1 then
                               if to_date(v_inicio_backup,'dd-mm-yyyy hh24:mi') between p_data and trunc(sysdate) + 1 then
                                 insert into agenda (codigo_politica, hora_inicio) values (v_politica.codigo_politica, to_date(v_inicio_backup,'dd-mm-yyyy hh24:mi'));
                              -- insert into agenda1 (codigo_politica, hora_inicio) values (v_politica.codigo_politica, to_date(v_inicio_backup,'dd-mm-yyyy hh24:mi'));
                               end if;
                          end if;
                        end loop;
                        close c_cron_dia_semana;
                    end loop;
                    close c_cron_minuto;
                  end loop;
                  close c_cron_hora;
               end if;
            end loop;
            close c_cron_dia;
        end loop;
        close c_cron_mes;
    end loop;
    close c_politica;

   if p_tipo_execucao = 'RELATORIO' then
     dbms_output.put_line('<html>');
     dbms_output.put_line('<head>');
     dbms_output.put_line('<title>Agendamento de Backup</title>');
     dbms_output.put_line('<meta http-equiv="content-type" content="text/html;charset=utf-8" />');
    --------------
     dbms_output.put_line('<style type="text/css">');
     dbms_output.put_line('#servidor');
     dbms_output.put_line('{');
     dbms_output.put_line('font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;');
     dbms_output.put_line('width:100%;');
     dbms_output.put_line('border-collapse:collapse; ');
     dbms_output.put_line('}');

     dbms_output.put_line('#servidor td, #servidor th ');
     dbms_output.put_line('{');
     dbms_output.put_line('font-size:11px;');

     dbms_output.put_line('border:1px solid #98bf21;');
     dbms_output.put_line('padding:3px 7px 2px 7px;');
     dbms_output.put_line('}');

     dbms_output.put_line('#servidor th');
     dbms_output.put_line('{');

     dbms_output.put_line('font-size:11px;');
     dbms_output.put_line('text-align:left;');
     dbms_output.put_line('padding-top:5px;');
     dbms_output.put_line('padding-bottom:4px;');
     dbms_output.put_line('background-color:#A7C942;');
     dbms_output.put_line('color:#ffffff;');
     dbms_output.put_line('}');

     dbms_output.put_line('#servidor tr.alt td ');
     dbms_output.put_line('{');
     dbms_output.put_line('color:#000000;');
     dbms_output.put_line('background-color:#EAF2D3;');
     dbms_output.put_line('}');
     dbms_output.put_line('</style>');

     dbms_output.put_line('</head>');

     dbms_output.put_line('<body>');
     
     l_titulo_cols    :=  '<tr><td>' || rpad('ID',4)      ||'</td><td> ' ||  rpad('POL',4)               ||'</td><td>'  ||  rpad('HOSTNAME',30)         ||'</td><td>' ||
                             rpad('DB_NAME',8)            ||'</td><td> ' ||  rpad('STATUS',10)           ||'</td><td>' ||
                             rpad('INICIO PREVISTO',20)   ||'</td><td>'  ||  rpad('INICIO REAL',20)      ||'</td><td>' ||
                             rpad('TEMPO MAXIMO',15)      ||'</td><td>'  ||  rpad('TEMPO REAL',15)       ||'</td><td>' ||  
                             rpad('TAMANHO MAX(GB)',16)   ||'</td><td>'  ||  rpad('TAMANHO REAL(GB)',16) ||'</td><td>' ||  rpad('MB/s',15) ||'</td><td>' ||
                             rpad('CONTEUDO',13)          ||'</td><td> ' ||  rpad('DESTINO',8)           ||'</td><td>' ||
                             rpad('DESCRICAO',30)         ||'</td></tr>';
     m := 0;

    
    dbms_output.put_line('<table id="servidor">');
    dbms_output.put_line('<tr><th colspan="15">DATA DO RELATORIO...............: ' || to_char(sysdate,'dd/mm/yyyy hh24:mi:ss') ||'</th></tr>');
    dbms_output.put_line('<br>');
    dbms_output.put_line('</table>');
  end if;
  k := 0;

  while k < 2 loop
    if p_tipo_execucao = 'RELATORIO' then
      dbms_output.put_line('<table id="servidor">');      
    end if;

    k := k + 1;
    v_cor := null;
    v_data_atual := p_data;
    
    open c_monitora_backup;
      loop
      fetch c_monitora_backup into v_monitora_backup;
      m := m  + 1;      
      v_cor := null;

      if upper(trim(v_monitora_backup.status)) = 'AGENDADO' then

        if sysdate > v_monitora_backup.inicio_p and v_monitora_backup.inicio_r  is null then

           select max(last_resync) into v_last_resync from rc_rman_backup_job_details where upper(hostname) = upper(v_monitora_backup.hostname) and upper(db_name) = upper(v_monitora_backup.db_name);

           if v_last_resync > v_monitora_backup.inicio_p then
              v_cor := 'RED';
              v_monitora_backup.status := 'NAO EXECUTADO';
            else
              v_cor := 'YELLOW';
              v_monitora_backup.status := 'SEM RESYNC';
            end if;
        end if;

      elsif   upper(trim(v_monitora_backup.status)) = 'FAILED'  then
            v_cor := 'RED';
            v_monitora_backup.status := 'FALHA';


      elsif  upper(trim(v_monitora_backup.status)) = 'RUNNING' then
            v_cor :='YELLOW';


      elsif upper(trim(v_monitora_backup.status)) like 'COMPLETED%' then
              v_monitora_backup.status := 'SUCESSO';

              v_segundos_e := to_number (substr(v_monitora_backup.duracao_e,1,2)) *3600 +
                              to_number (substr(v_monitora_backup.duracao_e,4,2)) *60 +
                              to_number (substr(v_monitora_backup.duracao_e,7,2));

              v_segundos_r := to_number (substr(v_monitora_backup.duracao_r,1,2)) *3600 +
                              to_number (substr(v_monitora_backup.duracao_r,4,2)) *60 +
                              to_number (substr(v_monitora_backup.duracao_r,7,2));

              v_cor := null;


              if  (to_number(v_monitora_backup.tamanho_r_gb) > to_number(v_monitora_backup.tamanho_p_gb) or
                  (v_segundos_r                              > v_segundos_e))  then

                  v_cor :='YELLOW';

              end if;
       end if;

       if p_tipo_execucao = 'RELATORIO' then
       
        if v_data_atual != trunc(v_monitora_backup.inicio_p) then
           v_data_atual :=trunc(v_monitora_backup.inicio_p);
           if k = 1 then
             dbms_output.put_line('<tr><th colspan="15">DESTAQUE DOS BACKUPS INICIADOS EM ' || to_char(v_data_atual,'dd/mm/yyyy') || ' COM WARNING OU FALHA</th></tr>');
           else
             dbms_output.put_line('<tr><th colspan="15">LISTA COMPLETA DOS BACKUPS INICIADOS EM ' || to_char(v_data_atual, 'dd/mm/yyyy') || '</th></tr>');
           end if;
           dbms_output.put_line(l_titulo_cols);
         end if;

         if v_cor is null then
           if mod(m,2) > 0 then
              v_estilo := '<tr class=alt><td>';
           else
              v_estilo := '<tr><td>';
           end if;
         else
             v_estilo := '<tr style="background-color:' || v_cor || ';"><td>';
         end if;
         
         if (k = 1 and v_cor in ('RED','YELLOW')) or k = 2 then
           v_id := v_id + 1;
           
           v_rate := null;
           
           if v_monitora_backup.duracao_r is not null and v_monitora_backup.tamanho_r_gb is not null  then
            v_duracao_r := (to_number(substr(v_monitora_backup.duracao_r,1,2))  *3600)  +
                           (to_number(substr(v_monitora_backup.duracao_r,4,2))   * 60)  +
                            to_number(substr(v_monitora_backup.duracao_r,7,2));
            
              v_rate := to_char(trunc((to_number(v_monitora_backup.tamanho_r_gb)*1024)/v_duracao_r,2),999.99);             
                         
           end if;
           dbms_output.put_line(v_estilo);
           dbms_output.put_line(
            rpad(v_id,4)                                           || '</td><td>' || rpad(v_monitora_backup.pid ,4)                         ||'</td><td>' || 
            rpad(v_monitora_backup.hostname,30)                    || '</td><td>' || rpad(v_monitora_backup.db_name ,8)                     ||'</td><td>' || 
            rpad(v_monitora_backup.status,20)                      || '</td><td>' || rpad(to_char(v_monitora_backup.inicio_p,'hh24:mi'),20) ||'</td><td>' || 
            rpad(to_char(v_monitora_backup.inicio_r,'hh24:mi'),20) || '</td><td>' || rpad(v_monitora_backup.duracao_e,10)                   ||'</td><td>' || 
            rpad(v_monitora_backup.duracao_r,10)                   || '</td><td>' || rpad(v_monitora_backup.tamanho_p_gb,9)                 ||'</td><td>' || 
            rpad(v_monitora_backup.tamanho_r_gb,9)                 || '</td><td>' || rpad(v_rate,15)                                        ||'</td><td>' ||
            rpad(v_monitora_backup.tipo,13)                        ||'</td><td>'  || rpad(v_monitora_backup.destino,8)                      ||'</td><td>' ||
            rpad(v_monitora_backup.descricao, 35)                  ||'</td></tr>');

         end if;
        end if;

        if v_cor = 'RED' then
         v_status_monitoramento := 'FALHA';
        end if;

       exit when c_monitora_backup%notfound;
      end loop;

    close c_monitora_backup;
    
    if p_tipo_execucao = 'RELATORIO' then
      dbms_output.put_line('</table">');
      dbms_output.put_line('<br>');
      dbms_output.put_line('</body>');
    else
      dbms_output.put_line (v_status_monitoramento);
      k := 2;
    end if;

  end loop;

--exception
 -- when OTHERS then
--    raise;

END MONITORA_BACKUP_HTML;