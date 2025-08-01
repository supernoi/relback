create or replace PROCEDURE         SP_CREATE_SCHEDULE
(
  p_date IN date DEFAULT trunc(sysdate)-3
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
                                 insert into schedules (backup_policy_id, schedule_start) values (v_policy.id_policy, to_date(v_schedule_start,'dd-mm-yyyy hh24:mi'));
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
