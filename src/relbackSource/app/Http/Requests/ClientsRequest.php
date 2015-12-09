<?php

namespace relback\Http\Requests;

use relback\Http\Requests\Request;

class ClientsRequest extends Request
{

    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'name' => 'required',
            'description' => 'required'
        ];
    }
}
