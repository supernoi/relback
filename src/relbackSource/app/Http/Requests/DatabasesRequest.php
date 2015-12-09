<?php

namespace relback\Http\Requests;

use relback\Http\Requests\Request;

class DatabasesRequest extends Request
{

    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'db_name' => 'required'
            ,'dbid' => 'required'
            ,'description' => 'required'
        ];
    }
}