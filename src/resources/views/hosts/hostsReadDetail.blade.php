@extends('layout.principal')

@section('content')
<div class="container container-fluid">
	<h1>Host detail: <strong>{{$host->hostname}}</strong></h1>  
		<ul>
			<li>
				<b>Client Name:</b> {{$host->client->name}} 
			</li>
			<li>
				<b>Hostname:</b> {{$host->hostname}} 
			</li>
			<li>
				<b>IP:</b> {{$host->ip}} 
			</li>
			<li>
				<b>Host description:</b> {{$host->description}}
			</li>
		</ul>
		
		<br><a class="btn btn-default" href="{{ action('HostsController@read') }}">Back</a>
</div>
@stop