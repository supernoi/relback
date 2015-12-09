<?php

namespace relback\Http\Controllers;

use Illuminate\Support\Facades\DB;

use relback\Http\Requests;
use relback\Http\Controllers\Controller;
use relback\Http\Requests\ClientsRequest;
use relback\Client;

use Request;
use Validator;
use Auth;

class ClientsController extends Controller
{

    public function __construct()
    {
        $this->middleware('auth');
    }

    public function read()
    {

        $clients = Client::orderBy('lower(name)','asc')->get();

        return view('clients.clientsRead')->with('clients', $clients);
    }

    public function readDetail($id_client)
    {

        $client = Client::find($id_client);

        if (empty($id_client)){
            return 'Client not found!';
        }

        return view('clients.clientsReadDetail')
            ->with('client',$client); 

    }

    public function create()
    {
        return view('clients.clientsCreate');
    }

    public function createAdd(ClientsRequest $clientsCreateRequest)
    {

        Client::create($clientsCreateRequest->all());

        return redirect()
            ->action('ClientsController@read')
            ->withInput(Request::only('id_client'));
        
    }

    public function updateForm($id_client)
    {
        $client = Client::find($id_client);

        if (empty($id_client)){
            return 'Client not found';
        }

        return view('clients.clientsUpdate')
            ->with('client',$client);
    }

    public function updateSave(ClientsRequest $clientUpdateRequest)
    {

        Client::where('id_client', $clientUpdateRequest['id_client'])
                ->update($clientUpdateRequest
                        ->except('_token'));

        return redirect()
            ->action('ClientsController@read')
            ->withInput(Request::only('name'));            
        
    }

    public function update($id_client)
    {
        Client::find($id_client)
            ->fill(Input::all());

    }    

    public function delete($id_client)
    {
        Client::destroy($id_client);

        return redirect()
            ->action('ClientsController@read')
            ->withInput(Request::only('id_client'));        
    }
}
