<?php

namespace relback;

use Illuminate\Database\Eloquent\Model;

class Policy extends Model
{
	public $primaryKey = 'id_policy';
    //public $timestamps = false;

    protected $table = 'backup_policies';
    protected $dateFormat = 'd/m/y H:i:s';
    
    protected $fillable = array('policy_name'
                                ,'id_client'
                                ,'id_database'
                                ,'id_host'
                                ,'backup_type'
                                ,'destination'
                                ,'minute'
                                ,'hour'
                                ,'day'
                                ,'month'
                                ,'day_week'
                                ,'duration'
                                ,'size_backup'
                                ,'status'
                                ,'description'
                                ,'created_id_user'
                                ,'updated_id_user'
								);

    public function user(){
    	return $this->belongsTo('relback\User','id_user');
    }

    public function client()
    {
        return $this->belongsTo('relback\Client','id_client');
    }

    public function host()
    {
        return $this->belongsTo('relback\Host','id_host');
    }

    public function database()
    {
    	return $this->belongsTo('relback\Database','id_database');
    }
}