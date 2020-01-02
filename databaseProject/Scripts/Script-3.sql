select
	to_number(pbv.id_policy)                                                                            id_policy,
	upper(substr(pbv.hostname,1,30))                                                                    hostname,
	upper(pbv.db_name)                                                                                  db_name,
	db_key																							  db_key,
	to_char(pbv.schedule_start, 'dd/mm/yy hh24:mi')                                                  		schedule_start,
    to_char(bjd.start_time, 'dd/mm/yy hh24:mi')                                                      		start_r,
    case 
	    when bjd.status is null and pbv.schedule_start > sysdate then 'SCHEDULED' 
	    when bjd.status is null and bjd.start_time is null then 'NOT RUN'
	    when bjd.status is not null then bjd.status
    end	                                                       										  status,
    bjd.time_taken_display                                                                              duration_r,
    TO_CHAR(TRUNC(pbv.duration/3600),'FM9900') || ':' ||
    TO_CHAR(TRUNC(MOD(pbv.duration,3600)/60),'FM00') || ':' ||
    TO_CHAR(MOD(pbv.duration,60),'FM00')                                                               duration_e,
    trunc(decode(substr(bjd.output_bytes_display,-1,1),'M',
    to_number(substr(bjd.output_bytes_display,1,    length(bjd.output_bytes_display)-1)/1024),
    'G',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1)),
    'T',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1*1024))),2)   size_r_gb,
    trunc(decode(substr(pbv.size_backup,-1,1),'M',
    to_number(substr(pbv.size_backup,1,    length(pbv.size_backup)-1)/1024),
    'G',to_number(substr(pbv.size_backup,1,length(pbv.size_backup)-1)),
    'T',to_number(substr(pbv.size_backup,1,length(pbv.size_backup)-1*1024))),2)                     size_p_gb,
    pbv.destination                                                                                 destination,
    pbv.backup_type                                                                                  backup_type,
    bjd.session_key																				  session_key,
    pbv.description                                                                                     description
from
    relback.vw_rman_backup_job_details bjd
    right outer join relback.vw_backup_policies pbv on (
    upper(bjd.db_name)                                                            = upper(pbv.db_name)          and
    upper(bjd.dbid)                                                               = upper(pbv.dbid)             and
    upper(decode(bjd.output_device_type,null,'SBT_TAPE',bjd.output_device_type))  = upper(pbv.destination)  	and
    upper(bjd.input_type)                                                         = upper(pbv.backup_type)      )
where
    trunc(pbv.schedule_start) between trunc(sysdate) - 7 and trunc(sysdate)
    order by pbv.schedule_start DESC;