@extends('layout.principal')

@section('content')
<div class="container container-fluid">
	<h1>Client detail: <strong>{{$client->name}}</strong></h1>  
		<ul>
			<li>
				<b>Client name:</b> {{$client->name}} 
			</li>
			<li>
				<b>Client description:</b> {{$client->description}}
			</li>
		</ul>
		
		<br><a class="btn btn-default" href="{{ action('ClientsController@read') }}">Back</a>
</div>
@stop