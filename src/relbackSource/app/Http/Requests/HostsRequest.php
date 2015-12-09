<?php

namespace relback\Http\Requests;

use relback\Http\Requests\Request;

class HostsRequest extends Request
{

    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'hostname' => 'required',
            'ip' => 'required|ip',
            'description' => 'required'
        ];
    }
}
