<?php

namespace relback;

use Illuminate\Database\Eloquent\Model;

class Client extends Model
{
	public $primaryKey = 'id_client';
    #public $timestamps = false;

	protected $dateFormat = 'd/m/y H:i:s';
    protected $fillable = array('name'
    							,'description'
    							,'created_id_user');


    public function user(){
    	return $this->belongsTo('relback\User','id_user');
    }

    public function host(){
    	return $this->hasMany('relback\Host','id_host');
    }

    public function database(){
    	return $this->hasMany('relback\Database','id_database');
    }

    public function policy(){
        return $this->hasMany('relback\Policy','id_policy');
    }

}
