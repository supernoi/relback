<?php

namespace relback;

use Illuminate\Database\Eloquent\Model;

class RmanBackupJobDetails extends Model
{
	public $primaryKey = 'db_key';
    public $timestamps = false;

    protected $table = 'vw_rman_backup_job_details';

	public function RmanOutput(){
		return $this->hasOne('relback\RmanOutput', 'db_key');
	}
    
}