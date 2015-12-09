@extends('layout.principal')

@section('title', 'Reports')

@section('content')

	<div class="container container-fluid">
		
		@if(old('empty_session_key'))
		  <div class="alert alert-warning">
		    <strong>Warning!</strong> 
		        The log for this scheduler not exist. Possible not run.
		  </div>
		@endif
		<div class="panel panel-default" ng-controller="filterController">
			<div class="panel-heading text-center"><h3>Report Backup Policy</h3></div>
										
						<table class="table table-striped table-responsive" id="tabReportResult1">

						<tr>
							<th class="text-center" id="text-middle">Policy</th>
							<th class="text-center" id="text-middle">Hostname</th>
							<th class="text-center" id="text-middle">DB_NAME</th>				
							<th class="text-center" id="text-middle">Expected<br>Start</th>
							<th class="text-center" id="text-middle">Start<br>Realized</th>
							<th class="text-center" id="text-middle">Executed<br>time</th>
							<th class="text-center" id="text-middle">Status</th>				
							<th class="text-center" id="text-middle">Destination</th>	
							<th class="text-center" id="text-middle">Backup<br>Type</th>						
							<th class="text-center" id="text-middle">Details</th>
						</tr>
						@foreach ($report as $r)

							@if($r->status=='COMPLETED') 
								<tr class="success" >
							@elseif($r->status=='NOT RUN')
								<tr class="danger" >
							@elseif($r->status=='SCHEDULED')
								<tr class="info" >										
							@elseif($r->status=='RUNNING') 
								<tr class="active" >
							@elseif($r->status=='COMPLETED WITH WARNINGS') 
								<tr class="warning" >
							@elseif($r->status=='FAILED') 
								<tr class="danger" >
							@endif
								
							<td class="text-center" id="text-middle"> <small>{{ $r->id_policy }}</small></td>
							<td class="text-center" id="text-middle"> <small>{{ $r->hostname }}</small></td>
							<td class="text-center" id="text-middle"> <small>{{ $r->db_name }}</small></td>
							<td class="text-center" id="text-middle"> <small>{{ $r->schedule_start }}</small></td>
							<td class="text-center" id="text-middle"> <small>{{ $r->start_r }}</small></td>							
							<td class="text-center" id="text-middle"> <small>{{ $r->duration_r }}</small></td>
							<td class="text-center" id="text-middle"> <small>{{ $r->status }}</small></td>
							<td class="text-center" id="text-middle"> <small>{{ $r->destination }}</small></td>
							<td class="text-center" id="text-middle"> <small>{{ $r->backup_type }}</small></td>

							<td class="text-center" id="text-middle">

								@if ( !empty($r->session_key) )
									<a class="glyphicon glyphicon-eye-open" href="{{ action('ReportsController@readLogDetail', [ $r->id_policy, $r->db_key, $r->session_key] ) }}" />
								@else
									<span class="glyphicon glyphicon-eye-close" />
								@endif									
							</td>
							</tr>
						@endforeach
					</table>
				
			</div>	
		</div>
	</div>

@stop