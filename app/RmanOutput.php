<?php

namespace relback;

use Illuminate\Database\Eloquent\Model;

class RmanOutput extends Model
{
	public $primaryKey = 'db_key';
    public $timestamps = false;

    protected $table = 'vw_rman_output';

	public function RmanBackupJobDetails(){
		return $this->hasOne('relback\RmanBackupJobDetails', 'db_key');
	}
    
}