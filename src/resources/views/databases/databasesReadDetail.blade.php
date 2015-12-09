@extends('layout.principal')

@section('content')
<div class="container container-fluid">
	<h1>Database detail: <strong>{{$database->db_name}}</strong></h1>  
		<ul>
			<li>
				<b>Client name:</b> {{$database->client->name}} 
			</li>
			<li>
				<b>Hostname:</b> {{$database->host->hostname}} 
			</li>
			<li>
				<b>Database(DB_NAME):</b> {{$database->db_name}} 
			</li>
			<li>
				<b>DBID:</b> {{$database->dbid}} 
			</li>
			<li>
				<b>Host description:</b> {{$database->description}}
			</li>
		</ul>
		
		<br><a class="btn btn-default" href="{{ action('DatabasesController@read') }}">Back</a>
</div>
@stop