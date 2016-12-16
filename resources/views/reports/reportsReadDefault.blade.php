@extends('layout.principal')

@section('title', 'Reports')

@section('content')
<div>
	<div class="container container-fluid">
		
		@if(old('empty_session_key'))
		  <div class="alert alert-warning">
		    <strong>Warning!</strong> 
		        The log for this scheduler not exist. Possible not run.
		  </div>
		@endif
		<div class="panel panel-default" >
			<div class="panel-heading text-center"><h3>Report Backup Policy</h3></div>	
		
				<table class="table table-striped table-responsive display" id="myTable" >
					<thead>
						<tr>
							<th class="text-center">Policy</th>
							<th class="text-center">Hostname</th>
							<th class="text-center">DB_NAME</th>				
							<th class="text-center">Expected<br>Start</th>
							<th class="text-center">Start<br>Realized</th>
							<th class="text-center">Executed<br>Time</th>
							<th class="text-center">Status</th>				
							<th class="text-center">Destination</th>	
							<th class="text-center">Backup<br>Type</th>						
							<th class="text-center">Details</th>
						</tr>
					</thead>

					<tfoot>
						<tr>
							<!-- space reserved for select-filter -->
							<th></th>
							<th></th>
							<th></th>
							<th></th>
							<th></th>
							<th></th>
							<th></th>
							<th></th>
							<th></th>
						</tr>
					</tfoot>

					<tbody>
					@foreach ($report as $r)

						@if($r->status=='COMPLETED') 
							@php $trStyle = 'success' @endphp
						@elseif($r->status=='SCHEDULED')
							@php $trStyle = 'info' @endphp				
						@elseif($r->status=='NOT RUN')
							@php $trStyle = 'danger' @endphp							
						@elseif($r->status=='RUNNING') 
							@php $trStyle = 'active' @endphp
						@elseif($r->status=='COMPLETED WITH WARNINGS') 
							@php $trStyle = 'warning' @endphp
						@elseif($r->status=='FAILED') 
							@php $trStyle = 'danger' @endphp
						@endif

						<tr class="{!! $trStyle !!}" style="font-size:12px">
						
							<td class="text-center" > {!! $r->id_policy !!} </td>
							<td class="text-center" > {!! $r->hostname !!} </td>
							<td class="text-center" > {!! $r->db_name !!} </td>
							<td class="text-center" > {!! $r->schedule_start !!} </td>
							<td class="text-center" > {!! $r->start_r !!} </td>							
							<td class="text-center" > {!! $r->duration_r !!} </td>
							<td class="text-center" > {!! $r->status !!} </td>
							<td class="text-center" > {!! $r->destination !!} </td>
							<td class="text-center" > {!! $r->backup_type !!} </td>

							<td class="text-center">

								@if ( !empty($r->session_key) )
									<a class="glyphicon glyphicon-eye-open" href="{!! action('ReportsController@readLogDetail', [ $r->id_policy, $r->db_key, $r->session_key] ) !!}" />
								@else
									<span class="glyphicon glyphicon-eye-close" />
								@endif									
							</td>
						</tr>
					@endforeach
					</tbody>
				</table>
				
			</div>	
		</div>
	</div>
</div>

<!-- modify select-filter of botton to top table -->
<style type="text/css">
	tfoot {
		display: table-header-group;
	}
</style>

@stop