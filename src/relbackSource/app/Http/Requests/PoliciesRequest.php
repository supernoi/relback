<?php

namespace relback\Http\Requests;

use relback\Http\Requests\Request;

class PoliciesRequest extends Request
{

    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return ['policy_name' => 'required'
                ,'id_client' => 'required'
                ,'id_database' => 'required'
                ,'id_host' => 'required'
                ,'backup_type' => 'required'
                ,'destination' => 'required'
                ,'minute' => 'required'
                ,'hour' => 'required'
                ,'day' => 'required'
                ,'month' => 'required'
                ,'day_week' => 'required'
                ,'duration' => 'required|numeric'
                ,'size_backup' => 'required'
                ,'status' => 'required'
                ,'description' => 'required'
        ];
    }
}
