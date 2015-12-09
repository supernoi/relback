<?php

namespace relback;

use Illuminate\Auth\Authenticatable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Auth\Passwords\CanResetPassword;
use Illuminate\Foundation\Auth\Access\Authorizable;
use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;
use Illuminate\Contracts\Auth\Access\Authorizable as AuthorizableContract;
use Illuminate\Contracts\Auth\CanResetPassword as CanResetPasswordContract;

class User extends Model implements AuthenticatableContract,
                                    AuthorizableContract,
                                    CanResetPasswordContract
{
    use Authenticatable, Authorizable, CanResetPassword;

    public $primaryKey = 'id_user';

    //public $timestamps = false;
    protected $dateFormat = 'd/m/y H:i:s';

    protected $table = 'users';

    protected $fillable = ['name', 'username', 'password'];

    protected $hidden = ['password', 'remember_token'];

    public function client(){
        return $this->hasMany('relback\Client','id_client');
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
