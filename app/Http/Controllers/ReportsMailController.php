<?php

namespace relback\Http\Controllers;

use Illuminate\Support\Facades\DB;

use relback\Http\Requests;
use relback\Http\Controllers\Controller;
use relback\Database;
use relback\Host;
use relback\Policy;
use relback\RmanOutput;
use relback\RmanBackupJobDetails;

use View;
use Request;
use Validator;

class ReportsMailController extends Controller
{

	public function mailDailyDefault(){
		$reportMailDefault = DB::select("
				select
					pbv.id_policy as id_policy,
					upper(substr(pbv.hostname,1,30)) as hostname,
					upper(pbv.db_name) as  db_name,
					pbv.SCHEDULE_START as schedule_start,
					bjd.start_time as start_r,
					case 
						when bjd.status is null and pbv.schedule_start > sysdate then 'SCHEDULED' 
						when bjd.status is null and bjd.start_time is null then 'NOT RUN'
						when bjd.status is not null then bjd.status
					end as status,
					bjd.time_taken_display as 	 duration_r,
					TO_CHAR(TRUNC(pbv.duration/3600),'FM9900') || ':' ||
					TO_CHAR(TRUNC(MOD(pbv.duration,3600)/60),'FM00') || ':' ||
					TO_CHAR(MOD(pbv.duration,60),'FM00') as  duration_e,
					trunc(decode(substr(bjd.output_bytes_display,-1,1),'M',
					to_number(substr(bjd.output_bytes_display,1,    length(bjd.output_bytes_display)-1)/1024),
					'G',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1)),
					'T',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1))*1024),2)   size_backup_r_gb,
					trunc(decode(substr(pbv.size_backup,-1,1),'M',
					to_number(substr(pbv.size_backup,1,    length(pbv.size_backup)-1)/1024),
					'G',to_number(substr(pbv.size_backup,1,length(pbv.size_backup)-1)),
					'T',to_number(substr(pbv.size_backup,1,length(pbv.size_backup)-1*1024))),2) as size_backup_p_gb,
					pbv.destination as destination,
					pbv.backup_type as backup_type,
					pbv.description as description
				from rman.rc_rman_backup_job_details bjd
					right outer join relback.vw_backup_policies pbv on (
					upper(bjd.db_name) = upper(pbv.db_name)
					and upper(decode(bjd.output_device_type,null,'SBT_TAPE',bjd.output_device_type))  = upper(pbv.destination)
					and upper(bjd.input_type) = upper(pbv.backup_type)
					and bjd.start_time between  pbv.SCHEDULE_START - 1/24/4 and pbv.SCHEDULE_START + 1/24/4)
				where
					to_char(pbv.SCHEDULE_START,'dd/mm/yy') between to_char(sysdate-3,'dd/mm/yy') and to_char(sysdate+1,'dd/mm/yy HH24:MM:SS')
				order by
					to_char(pbv.SCHEDULE_START,   'yyyy-mm-dd hh24:mi:ss') desc
			");

		return view('reports.reportsReadMailDaily')
			->with('reportMailDefault', $reportMailDefault);

	}

	public function mailDataDaily(){
		$reportMailDefault = DB::select("
				select
					pbv.id_policy as id_policy,
					upper(substr(pbv.hostname,1,30)) as hostname,
					upper(pbv.db_name) as  db_name,
					pbv.SCHEDULE_START as schedule_start,
					bjd.start_time as start_r,
					case 
						when bjd.status is null and pbv.schedule_start > sysdate then 'SCHEDULED' 
						when bjd.status is null and bjd.start_time is null then 'NOT RUN'
						when bjd.status is not null then bjd.status
					end as status,
					bjd.time_taken_display as 	 duration_r,
					TO_CHAR(TRUNC(pbv.duration/3600),'FM9900') || ':' ||
					TO_CHAR(TRUNC(MOD(pbv.duration,3600)/60),'FM00') || ':' ||
					TO_CHAR(MOD(pbv.duration,60),'FM00') as  duration_e,
					trunc(decode(substr(bjd.output_bytes_display,-1,1),'M',
					to_number(substr(bjd.output_bytes_display,1,    length(bjd.output_bytes_display)-1)/1024),
					'G',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1)),
					'T',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1))*1024),2)   size_backup_r_gb,
					trunc(decode(substr(pbv.size_backup,-1,1),'M',
					to_number(substr(pbv.size_backup,1,    length(pbv.size_backup)-1)/1024),
					'G',to_number(substr(pbv.size_backup,1,length(pbv.size_backup)-1)),
					'T',to_number(substr(pbv.size_backup,1,length(pbv.size_backup)-1*1024))),2) as size_backup_p_gb,
					pbv.destination as destination,
					pbv.backup_type as backup_type,
					pbv.description as description
				from relback.vw_rman_backup_job_details bjd
					right outer join relback.vw_backup_policies pbv on (
					upper(bjd.db_name) = upper(pbv.db_name)
					and upper(decode(bjd.output_device_type,null,'SBT_TAPE',bjd.output_device_type))  = upper(pbv.destination)
					and upper(bjd.input_type) = upper(pbv.backup_type)
					and bjd.start_time between  pbv.SCHEDULE_START - 1/24/4 and pbv.SCHEDULE_START + 1/24/4)
				where
					to_char(pbv.SCHEDULE_START,'dd/mm/yy') between to_char(sysdate-3,'dd/mm/yy') and to_char(sysdate+1,'dd/mm/yy HH24:MM:SS')
				order by
					to_char(pbv.SCHEDULE_START,   'yyyy-mm-dd hh24:mi:ss') desc
			");

		return $reportMailDefault;

	}
}


