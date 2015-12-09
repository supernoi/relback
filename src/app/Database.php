<?php

namespace relback;

use Illuminate\Database\Eloquent\Model;

class Database extends Model
{
	public $primaryKey = 'id_database';
    //public $timestamps = false;

    protected $dateFormat = 'd/m/y H:i:s';

    protected $fillable = array( 'db_name'
                                ,'dbid'
    							,'id_client'
    							,'id_host'
    							,'description'
                                ,'created_id_user');

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
}