@extends('layout.principal')

@section('title', 'Report Log Detail')

@section('content')

    <div class="container">
     <br><br>
		<div class="span10 offset1">
			<div class="row">
				<center>
					<h1>Report Backup Policy Detail</h1>
				</center>
				<br>
			</div>
			
			<div class="row">
				<div class="col-xs-6 col-md-2"><b>ID Policy: </b>{{ $policyDetail->id_policy }}</div>
				<div class="col-xs-6 col-md-2"><b>Status: </b> {{ $policyDetail->status }}</div>
				<div class="col-xs-6 col-md-3"><b>Client: </b>{{ $policyDetail->client->name }}</div>
			 	<div class="col-xs-6 col-md-5"><b>Policy Name: </b> {{ $policyDetail->policy_name }}</div>
			</div>
			<div class="row">
				<div class="col-xs-6 col-md-4"><b>Database(DB_NAME): </b> {{ $policyDetail->database->db_name }}</div>
			 	<div class="col-xs-6 col-md-4"><b>Hostname: </b> {{ $policyDetail->host->hostname }}</div>
			 	<div class="col-xs-6 col-md-4"><b>Backup Type: </b> {{ $policyDetail->backup_type }}</div>
			</div>
			<div class="row">
				<div class="col-xs-6 col-md-4"><b>Duration Estimated: </b> {{ $policyDetail->duration }} Minutes</div>
			 	<div class="col-xs-6 col-md-4"><b>Size Backup Estimated: </b> {{ $policyDetail->size_backup }}</div>
			</div>
			<div class="row">
				<div class="col-xs-6 col-md-4"><b>Duration Realized: </b> {{ $execDetail->time_taken_display }} H:M:S</div>
			 	<div class="col-xs-6 col-md-4"><b>Size Backup Realized: </b> {{ $execDetail->output_bytes_display }}</div>
			</div>

			
			<br>
			<div class="panel panel-default">
				<div class="panel-heading text-center"><h4>Log of the backup execution (RMAN_OUTPUT)</h4></div>
				<div class="table-responsive">
				<table class="table table-striped table-bordered">
					<tr>					
						<th class="text-center" id="text-middle">RECID</th>
						<th class="text-center" id="text-middle">RNAN Output</th>
					</tr>
					@foreach ($reportLog as $rl)
						<tr>
							<td class="text-center" id="text-middle">{{ $rl->recid }}</td>
							<td class="text-center" id="text-middle">{{ $rl->output }}</td>
						</tr>
					@endforeach
				</table>

					<div class="form-actions">
						<br>
					  <center><a class="btn btn-default" href="{{ action('ReportsController@readDefault') }}">Voltar</a></center>
					</div>
				 
				</div>
			</div>
		</div>
                 
    </div>

@stop   