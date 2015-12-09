<?php

namespace relback\Http\Controllers;

use Illuminate\Support\Facades\DB;

use relback\Http\Requests;
use relback\Http\Controllers\Controller;
use relback\Http\Requests\HostsRequest;
use relback\Host;
use relback\Client;

use Auth;
use View;
use Request;
use Validator;

class HostsController extends Controller
{

    public function __construct()
    {
        $this->middleware('auth');
    }

    public function read()
    {

        $clients = Client::orderBy('lower(name)','asc')->get();

        $hosts = Host::with('client')
                        ->orderBy('lower(hostname)','asc')
                        ->get();

        return View::make('hosts.hostsRead')
            ->with('hosts',$hosts)
            ->with('clients',$clients);

    }

    public function readDetail($id_host)
    {

        $host = Host::with('client')
                        ->find($id_host);

        if (empty($id_host)){
            return 'Host(Hostname) not found!';
        }

        return view('hosts.hostsReadDetail')
            ->with('host',$host); 

    }

    public function create()
    {

        $clients = Client::orderBy('lower(name)','asc')->get();

        return View::make('hosts.hostsCreate')
                    ->with('clients',$clients);
    }

    public function createAdd(HostsRequest $hostsCreateRequest)
    {

        Host::create($hostsCreateRequest->all());

        return redirect()
            ->action('HostsController@read')
            ->withInput(Request::only('hostname'));
        
    }

    public function updateForm($id_host)
    {
        $host = Host::with('client')
                        ->find($id_host);

        $clients = Client::orderBy('lower(name)','asc')->get();

        if (empty($id_host)){
            return 'Hostname não encontrado';
        }

        return View::make('hosts.hostsUpdate')
            ->with('host',$host)
            ->with('clients',$clients);
    }

    public function updateSave(HostsRequest $hostUpdateRequest)
    {

        Host::where('id_host', $hostUpdateRequest['id_host'])
                ->update($hostUpdateRequest
                        ->except('_token'));

        return redirect()
            ->action('HostsController@read')
            ->withInput(Request::only('hostname'));            
        
    }

    public function update($hostname)
    {
        Host::find($hostname)
            ->fill(Input::all());

    }    

    public function delete($hostname)
    {
        Host::destroy($hostname);

        return redirect()
            ->action('HostsController@read')
            ->withInput(Request::only('hostname'));        
    }
}
