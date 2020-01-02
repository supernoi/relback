CALL RELBACK.SP_CREATE_SCHEDULE(sysdate-7);
COMMIT;


SELECT *
FROM schedules;


select * from cron_day;
select * from cron_month;
select * from cron_day_week;
select * from cron_hour;
select * from cron_minute;