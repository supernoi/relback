@extends('layout.principal')

@section('content')
<div class="container container-fluid">
	<h1>Backup Policy detail: ID number <strong>{{$policy->policy_name}}</strong></h1>  
		<ul>
			<li>
				<b>Id Policy:</b> {{$policy->id_policy}} 
			</li>
			<li>
				<b>Client name:</b> {{$policy->client->name}} 
			</li>
			<li>
				<b>Database(DB_NAME):</b> {{$policy->database->db_name}} 
			</li>
			<li>
				<b>Hostname:</b> {{$policy->host->hostname}}
			</li>
			<li>
				<b>Backup Type:</b> {{$policy->backup_type}}
			</li>
			<li>
				<b>Destination:</b> {{$policy->destination}}
			</li>
			<li>
				<b>Minute:</b> {{$policy->minute}}
			</li>
			<li>
				<b>Hour:</b> {{$policy->hour}}
			</li>
			<li>
				<b>Day:</b> {{$policy->day}}
			</li>
			<li>
				<b>Month:</b> {{$policy->month}}
			</li>
			<li>
				<b>Day Week:</b> {{$policy->day_week}}
			</li>
			<li>
				<b>Duration Estimate:</b> {{$policy->duration}}
			</li>
			<li>
				<b>Backup Size Estimate:</b> {{$policy->size_backup}}
			</li>
			<li>
				<b>Status:</b> {{$policy->status}}
			</li>
			<li>
				<b>Description:</b> {{$policy->description}}
			</li>

		</ul>
		
		<br><a class="btn btn-default" href="{{ action('PoliciesController@read') }}">Back</a>
</div>
@stop