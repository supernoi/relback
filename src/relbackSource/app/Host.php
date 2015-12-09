<?php

namespace relback;

use Illuminate\Database\Eloquent\Model;

class Host extends Model
{
	public $primaryKey = 'id_host';
    //public $timestamps = false;

	protected $dateFormat = 'd/m/y H:i:s';
    protected $fillable = array('hostname'
    							,'ip'
    							,'description'
    							,'id_client'
                                ,'created_id_user');

    public function user(){
        return $this->belongsTo('relback\User','id_user');
    }

    public function client()
    {
        return $this->belongsTo('relback\Client','id_client');
    }
}
