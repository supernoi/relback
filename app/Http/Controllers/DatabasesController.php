<?php

namespace relback\Http\Controllers;

use Illuminate\Support\Facades\DB;

use relback\Http\Requests;
use relback\Http\Controllers\Controller;
use relback\Http\Requests\DatabasesRequest;
use relback\Database;
use relback\Host;
use relback\Client;
use relback\Policy;

use View;
use Request;
use Validator;

class DatabasesController extends Controller
{

/*    public function __construct()
    {
        $this->middleware('auth');
    }*/

    public function read()
    {

        $databases = Database::with('host','client')
                        ->orderBy('db_name','asc')->get();

        $hosts = Host::orderBy('hostname')->get();

        $clients = Client::orderBy('name','asc')->get();

        return View::make('databases.databasesRead')
             ->with('databases',$databases)
             ->with('hosts',$hosts)
             ->with('clients', $clients);
    }

    public function readDetail($db_name)
    {

        $database = Database::with('host','client')
                        ->find($db_name);

        if (empty($db_name)){
            return 'Database(DB_NAME) not found!';
        }

        return view('databases.databasesReadDetail')
            ->with('database',$database); 

    }

    public function create()
    {
        $hostnames = Host::with('client')
                        ->orderBy('hostname)')->get();

        $clients = Client::orderBy('name)','asc')->get();

        return View::make('databases.databasesCreate')
                    ->with('hostnames',$hostnames)
                    ->with('clients',$clients);
    }

    public function createAdd(DatabasesRequest $DatabasesCreateRequest)
    {

        Database::create($DatabasesCreateRequest->all());

        //dd($DatabasesCreateRequest->all());

        return redirect()
            ->action('DatabasesController@read')
            ->withInput(Request::only('db_name'));
        
    }

    public function updateForm($db_name)
    {
        $database = Database::with('host','client')
                    ->find($db_name);

        $hosts = Host::orderBy('hostname)')->get();
        $clients = Client::orderBy('name)','asc')->get();

        if (empty($db_name)){
            return 'Database(DB_NAME) not found!';
        }

        return View::make('databases.databasesUpdate')
             ->with('database',$database)
             ->with('hosts',$hosts)
             ->with('clients', $clients);
    }

    public function updateSave(DatabasesRequest $databaseUpdateRequest)
    {

        Database::where('id_database', $databaseUpdateRequest['id_database'])
                 ->update($databaseUpdateRequest
                        ->except('_token'));

        return redirect()
            ->action('DatabasesController@read')
            ->withInput(Request::only('db_name'));            
        
    }

    public function update($db_name)
    {
        Database::find($db_name)
            ->fill(Input::all());

    }    

    public function delete($db_name)
    {
        Database::destroy($db_name);

        return redirect()
            ->action('DatabasesController@read')
            ->withInput(Request::only('db_name'));        
    }
}
