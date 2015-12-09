@extends('layout.principal')

@section('content')

	<div class="container container-fluid">

		@if (count($errors) > 0)
			<div class="alert alert-danger">
				<ul>
					@foreach ($errors->all() as $error)
					<li>{{$error}}</li>
					@endforeach
				</ul>
			</div>
		@endif

			<div class="panel panel-default">
				<div class="panel-heading"><h3>Add new Backup Policy<h3></div>
					<div class="panel-body">
						<form class="form-horizontal" action="{{action('PoliciesController@createAdd')}}" method="POST">
							<input type="hidden" name="_token" value="{{csrf_token()}}" />

							<input type="hidden" name="created_id_user" value="{{ Auth::id() }}">

							<div class="form-group">

								<div class="col-md-3">
									<div class="input-group">
											<span class="input-group-addon">Status</span>					
											<select type="status" class="form-control" name="status">
												<option value="ACTIVE">ACTIVE</option>
												<option value="INACTIVE">INACTIVE</option>
											</select>
									</div>
								</div>

								<div class="col-md-8">
									<div class="input-group">
											<span class="input-group-addon">Policy Name</span>					
											<input name="policy_name" type="text" class="form-control" value="{{ old('policy_name') }}">
									</div>
								</div>
							</div>
							
							<div class="form-group">

								<div class="col-md-3">
									<div class="input-group">									
										<span class="input-group-addon">Client name</span>
										<select type="id_client" class="form-control" name="id_client">
											@foreach ($clients as $c)
												<option value="{{ $c->id_client }}">{{ $c->name }}</option>
											@endforeach
										</select>
									</div>
								</div>

								<div class="col-md-5">
									<div class="input-group">									
										<span class="input-group-addon">Hostname</span>
										<select type="id_host" class="form-control" name="id_host">
											@foreach ($hostnames as $h)
												<option value="{{ $h->id_host }}">{{ $h->hostname }}</option>
											@endforeach
										</select>
									</div>
								</div>

								<div class="col-md-4">
									<div class="input-group">									
										<span class="input-group-addon">Database(DB_NAME)</span>
										<select type="id_database" class="form-control" name="id_database">
											@foreach ($databases as $d)
												<option value="{{ $d->id_database }}">{{ $d->db_name }}</option>
											@endforeach
										</select>
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-6">
									<div class="input-group">									
										<span class="input-group-addon">Backup Type</span>
										<select type="backup_type" class="form-control" name="backup_type">
											<option value="ARCHIVELOG">ARCHIVELOG</option>
											<option value="DB FULL">DB FULL</option>
											<option value="DB INCR">DB INCR</option>
											<option value="RECVR AREA">RECVR AREA</option>
											<option value="BACKUPSET">BACKUPSET</option>
										</select>
									</div>
								</div>

								<div class="col-md-6">
									<div class="input-group">									
										<span class="input-group-addon">Destination</span>
										<select type="destination" class="form-control" name="destination">
											<option value="SBT_TAPE">SBT_TAPE</option>
											<option value="DISK">DISK</option>
										</select>
									</div>
								</div>
							</div>

							<div class="form-group">

								<div class="col-md-2">
										<div class="input-group">
												<span class="input-group-addon">Minute</span>					
												<input name="minute" type="text" class="form-control" value="{{ old('minute') }}">
										</div>
									</div>

								<div class="col-md-2">
									<div class="input-group">
											<span class="input-group-addon">Hour</span>					
											<input name="hour" type="text" class="form-control" value="{{ old('hour') }}">
									</div>
								</div>

								<div class="col-md-2">
									<div class="input-group">
											<span class="input-group-addon">Day</span>					
											<input name="day" type="text" class="form-control" value="{{ old('day') }}">
									</div>
								</div>

								<div class="col-md-3">
									<div class="input-group">
											<span class="input-group-addon">Day Month</span>					
											<input name="month" type="text" class="form-control" value="{{ old('month') }}">
									</div>
								</div>

								<div class="col-md-3">
									<div class="input-group">
											<span class="input-group-addon">Day Week</span>					
											<input name="day_week" type="text" class="form-control" value="{{ old('day_week') }}">
									</div>
								</div>

							</div>

							<div class="form-group">
								<div class="col-md-6">
									<div class="input-group">
											<span class="input-group-addon">Duration Estimate</span>					
											<input name="duration" type="text" class="form-control" value="{{ old('duration') }}">
									</div>
								</div>

								<div class="col-md-6">
									<div class="input-group">
											<span class="input-group-addon">Backup Size Estimate</span>					
											<input name="size_backup" type="text" class="form-control" value="{{ old('size_backup') }}">
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-12">
									<div class="input-group">
											<span class="input-group-addon">Description</span>					
											<input name="description" type="text" class="form-control" value="{{ old('description') }}">
									</div>
								</div>
							</div>
										
							<br>
							<div class="form-group">
								<div class="col-md-6">
									<button class="btn btn-primary" type="submit">Add</button> 
									<a class="btn btn-default" href="{{action('PoliciesController@read')}}">Back</a>
								</div>
							</div>


						</form>
					</div>
			</div>
	</div>
	
@stop