@extends('layout.principal')

@section('content')

	<div class="container container-fluid">
				<div class="panel panel-default">
					<div class="panel-heading"><h3>Update Backup Policy</h3></div>
					<div class="panel-body">
					<form class="form-horizontal" action="{{action('PoliciesController@updateSave')}}" method="POST">
						<input type="hidden" name="_token" value="{{csrf_token()}}" />

						<input type="hidden" name="id_policy" value="{{ $policy->id_policy }}">
						<input type="hidden" name="updated_id_user" value="{{ Auth::id() }}">

							<div class="form-group">

								<div class="col-md-3">
									<div class="input-group">
											<span class="input-group-addon">Status</span>					
											<select type="status" class="form-control" name="status">
												<option value="{{ $policy->status}}">{{ $policy->status}}</option>
												<option value="">------</option>
												<option value="ACTIVE">ACTIVE</option>
												<option value="INACTIVE">INACTIVE</option>
											</select>
									</div>
								</div>

								<div class="col-md-8">
									<div class="input-group">
											<span class="input-group-addon">Policy Name</span>					
											<input name="policy_name" type="text" class="form-control" value="{{ $policy->policy_name }}">
									</div>
								</div>
							</div>
							
							<div class="form-group">

								<div class="col-md-3">
									<div class="input-group">									
										<span class="input-group-addon">Client name</span>
										<select type="id_client" class="form-control" name="id_client">
											<option value="{{ $policy->id_client }}" selected>{{ $policy->client->name }}</option>
											<option value="">------</option>
											@foreach ($clients as $c)
												<option value="{{ $c->id_client }}">{{ $c->name}}</option>
											@endforeach
										</select>
									</div>
								</div>

								<div class="col-md-5">
									<div class="input-group">									
										<span class="input-group-addon">Hostname</span>
										<select type="id_host" class="form-control" name="id_host">
											<option value="{{ $policy->host->id_host }}" selected>{{ $policy->host->hostname }}</option>
											<option value="">------</option>
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
											<option value="{{ $policy->id_database }}" selected>{{ $policy->database->db_name }}</option>
											<option value="">------</option>
											@foreach ($databases as $d)
												<option value="{{ $d->db_name }}">{{ $d->db_name }}</option>
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
											<option value="{{ $policy->backup_type }}">{{ $policy->backup_type }}</option>
											<option value="">------</option>
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
											<option value="{{ $policy->destination }}">{{ $policy->destination }}</option>
											<option value="">="">------</</option>
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
											<input name="minute" type="text" class="form-control" value="{{ $policy->minute }}">
									</div>
								</div>

								<div class="col-md-2">
									<div class="input-group">
											<span class="input-group-addon">Hour</span>					
											<input name="hour" type="text" class="form-control" value="{{ $policy->hour }}">
									</div>
								</div>

								<div class="col-md-2">
									<div class="input-group">
											<span class="input-group-addon">Day</span>					
											<input name="day" type="text" class="form-control" value="{{ $policy->day }}">
									</div>
								</div>

								<div class="col-md-2">
									<div class="input-group">
											<span class="input-group-addon">Month</span>					
											<input name="month" type="text" class="form-control" value="{{ $policy->month }}">
									</div>
								</div>

								<div class="col-md-2">
									<div class="input-group">
											<span class="input-group-addon">Day Week</span>					
											<input name="day_week" type="text" class="form-control" value="{{ $policy->day_week }}">
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-6">
									<div class="input-group">
											<span class="input-group-addon">Duration Estimate</span>					
											<input name="duration" type="text" class="form-control" value="{{ $policy->duration }}">
									</div>
								</div>							

								<div class="col-md-6">
									<div class="input-group">
											<span class="input-group-addon">Backup Size Estimate</span>					
											<input name="size_backup" type="text" class="form-control" value="{{ $policy->size_backup }}">
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-12">
									<div class="input-group">
											<span class="input-group-addon">Description</span>					
											<input name="description" type="text" class="form-control" value="{{ $policy->description }}">
									</div>
								</div>
							</div>
							
						<br>
						<div class="form-group">
							<div class="col-md-6">
								<button class="btn btn-primary" type="submit">Update</button> 
								<a class="btn btn-default" href="{{ action('PoliciesController@read') }}">Back</a>
							</div>
						</div>
					</form>

					</div>
				</div>
	</div>

@stop