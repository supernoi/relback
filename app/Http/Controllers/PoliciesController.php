<?php

namespace relback\Http\Controllers;

use Illuminate\Support\Facades\DB;

use relback\Http\Requests;
use relback\Http\Controllers\Controller;
use relback\Http\Requests\PoliciesRequest;
use relback\Database;
use relback\Host;
use relback\Policy;
use relback\Client;

use View;
use Request;
use Validator;

class PoliciesController extends Controller
{

    public function __construct()
    {
        $this->middleware('auth');
    }

    public function read()
    {

        $policies = Policy::with('client','host','database')
                    ->orderBy('id_policy','asc')->get();

        $clients = Client::orderBy('name')->get();
        $hostnames = Host::orderBy('hostname')->get();
        $databases = Database::orderBy('db_name')->get();

         return View::make('policies.policiesRead')
              ->with('policies',$policies)
              ->with('clients', $clients)
              ->with('hostnames',$hostnames)
              ->with('databases',$databases);
    }

    public function readDetail($id_policy)
    {

        $policy = Policy::find($id_policy);

        if (empty($policy)){
            return 'Backup Policy not found!';
        }

        return view('policies.policiesReadDetail')
            ->with('policy',$policy); 

    }

    public function create()
    {
        $hostnames = Host::orderBy('hostname')->get();
        $databases = Database::orderBy('db_name')->get();
        $clients = Client::orderBy('name')->get();

        return View::make('policies.policiesCreate')
            ->with('hostnames', $hostnames)
            ->with('databases', $databases)
            ->with('clients', $clients);
    }

    public function createAdd(PoliciesRequest $PoliciesCreateRequest)
    {

        Policy::create($PoliciesCreateRequest->all());
        //dd($PoliciesCreateRequest->all());

        return redirect()
            ->action('PoliciesController@read')
            ->withInput(Request::only('id_policy'));
        
    }

    public function updateForm($id_policy)
    {
        $policy = Policy::find($id_policy);
        $clients = Client::orderBy('name')->get();
        $hostnames = Host::orderBy('hostname')->get();
        $databases = Database::orderBy('db_name')->get();

        if (empty($policy)){
            return 'Backup Policy not found!';
        }

         return View::make('policies.policiesUpdate')
              ->with('policy',$policy)
              ->with('clients', $clients)
              ->with('hostnames',$hostnames)
              ->with('databases',$databases);
    }

    public function updateSave(PoliciesRequest $policyUpdateRequest)
    {

        Policy::where('id_policy', $policyUpdateRequest['id_policy'])
                ->update($policyUpdateRequest
                        ->except('_token'));

        // dd($policyUpdateRequest->except('_token'));

        return redirect()
            ->action('PoliciesController@read')
            ->withInput(Request::only('id_policy'));            
        
    }

    public function update($id_policy)
    {
        Policy::find($id_policy)
            ->fill(Input::all());
    }    

    public function delete($id_policy)
    {
        Policy::destroy($id_policy);

        return redirect()
            ->action('PoliciesController@read')
            ->withInput(Request::only('id_policy'));        
    }
}
