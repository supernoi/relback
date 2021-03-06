@extends('layout.principal')

@section('title', 'Backup Policies')

@section('content')

	<div class="container container-fluid"> 
		<h1>Backup Policy list</h1>  
		
		<br>
			<a href="" data-target="#modalAddNew" id="fetch" data-toggle="modal" class="btn btn-primary">Add New</a>
		<br><br>

		@if (count($errors) > 0)
			<div class="alert alert-danger">
				<ul>
					@foreach ($errors->all() as $error)
					<li>{{$error}}</li>
					@endforeach
				</ul>
			</div>
		@endif

		<!-- Modal of ReadDetail -->

		<div class="modal fade" id="modalAddNew" role="dialog" aria-labelledby="ModalLabel-ReadDetail">
			<div class="modal-dialog modal-lg">
				<div class="modal-content">
				 	<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h2 class="modal-title">Add new Backup Policy</h2>
					</div>
					<div class="modal-body">
						
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

								<div class="col-md-9">
									<div class="input-group">
										<span class="input-group-addon">Policy Name</span>					
										<input name="policy_name" type="text" class="form-control" value="{{ old('policy_name') }}">
									</div>
								</div>
							</div>
							
							<div class="form-group">

								<div class="col-md-4">
									<div class="input-group">									
										<span class="input-group-addon">Client name</span>
										<select type="id_client" class="form-control" name="id_client">
											@foreach ($clients as $c)
												<option value="{{ $c->id_client }}">{{ $c->name }}</option>
											@endforeach
										</select>
									</div>
								</div>

								<div class="col-md-4">
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
												<input name="minute" type="text" class="form-control" value="{{ old('minute', '*') }}">
										</div>
									</div>

								<div class="col-md-2">
									<div class="input-group">
											<span class="input-group-addon">Hour</span>					
											<input name="hour" type="text" class="form-control" value="{{ old('hour', '*') }}">
									</div>
								</div>

								<div class="col-md-2">
									<div class="input-group">
											<span class="input-group-addon">Day</span>					
											<input name="day" type="text" class="form-control" value="{{ old('day', '*') }}">
									</div>
								</div>

								<div class="col-md-3">
									<div class="input-group">
											<span class="input-group-addon">Day Month</span>					
											<input name="month" type="text" class="form-control" value="{{ old('month', '*') }}">
									</div>
								</div>

								<div class="col-md-3">
									<div class="input-group">
											<span class="input-group-addon">Day Week</span>					
											<input name="day_week" type="text" class="form-control" value="{{ old('day_week', '*') }}">
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

							<div class="modal-footer">
								<a class="btn btn-default" data-dismiss="modal">Close</a>
								<button class="btn btn-primary" type="submit">Add</button>							
							</div>

						</form>
					</div>
				</div>
			</div>
		</div>

		<!-- End Modal of ReadDetail -->

		@if(old('id_policy'))
		  <div class="alert alert-success">
		    <strong>Sucess!</strong> 
		        The Policy number {{ old('id_policy') }} was created or updated.
		  </div>
		@endif
		<div class="panel panel-default">
			<table class="table table-striped">
				<tr>
					<th class="text-center">Id Policy</th class="text-center">
					<th class="text-center">Hostname</th class="text-center">
					<th class="text-center">DB_NAME</th class="text-center">
					<th class="text-center">Backup Type</th class="text-center">
					<th class="text-center">Status</th class="text-center">
					<th class="text-center">Description</th class="text-center">
					<th class="text-center">Option</th class="text-center">	

				</tr>
			@foreach ($policies as $p) 
				<tr>
					<td class="text-center">{{ $p->id_policy }}</td>
					<td class="text-center">{{ $p->host->hostname }}</td>
					<td class="text-center">{{ $p->database->db_name }}</td>
					<td class="text-center">{{ $p->backup_type }}</td>
					<td class="text-center">{{ $p->status }}</td>
					<td class="text-center">{{ $p->description }}</td>
				    <td class="text-center">
						<a href="" data-target="#modalReadDetail-{{ $p->id_policy }}" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-search"></span></a>
						&nbsp&nbsp<a href="" data-target="#modalUpdate-{{ $p->id_policy }}" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-pencil"></span></a>
						&nbsp&nbsp<a href="" data-target="#modalDelete-{{ $p->id_policy }}" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-trash"></span></a>	
				    </td>	
				</tr>
				
				<!-- Modal of ReadDetail -->

				<div class="modal fade" id="modalReadDetail-{{ $p->id_policy }}" role="dialog" aria-labelledby="ModalLabel-ReadDetail">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title">{{$p->policy_name}}</h2>
							</div>
							<div class="modal-body">								
								<ul>
									<li>
										<b>Id Policy:</b> {{$p->id_policy}} 
									</li>
									<li>
										<b>Client name:</b> {{$p->client->name}} 
									</li>
									<li>
										<b>Database(DB_NAME):</b> {{$p->database->db_name}} 
									</li>
									<li>
										<b>Hostname:</b> {{$p->host->hostname}}
									</li>
									<li>
										<b>Backup Type:</b> {{$p->backup_type}}
									</li>
									<li>
										<b>Destination:</b> {{$p->destination}}
									</li>
									<li>
										<b>Minute:</b> {{$p->minute}}
									</li>
									<li>
										<b>Hour:</b> {{$p->hour}}
									</li>
									<li>
										<b>Day:</b> {{$p->day}}
									</li>
									<li>
										<b>Month:</b> {{$p->month}}
									</li>
									<li>
										<b>Day Week:</b> {{$p->day_week}}
									</li>
									<li>
										<b>Duration Estimate:</b> {{$p->duration}}
									</li>
									<li>
										<b>Backup Size Estimate:</b> {{$p->size_backup}}
									</li>
									<li>
										<b>Status:</b> {{$p->status}}
									</li>
									<li>
										<b>Description:</b> {{$p->description}}
									</li>
								</ul>
							</div>
							<div class="modal-footer">
								<a class="btn btn-default" data-dismiss="modal">Close</a>								
							</div>
						</div>
					</div>
				</div>	

			<!-- Modal of update -->

				<div class="modal fade" id="modalUpdate-{{ $p->id_policy }}" role="dialog" aria-labelledby="ModalLabel-Update">
					<div class="modal-dialog modal-lg">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title">{{$p->policy_name}}</h2>
							</div>

							<div class="modal-body">
								<form class="form-horizontal" action="{{action('PoliciesController@updateSave')}}" method="POST">
									<input type="hidden" name="_token" value="{{csrf_token()}}" />

									<input type="hidden" name="id_policy" value="{{ $p->id_policy }}">
									<input type="hidden" name="updated_id_user" value="{{ Auth::id() }}">

										<div class="row form-group">

											<div class="col-md-3">
												<div class="input-group">
														<span class="input-group-addon">Status</span>					
														<select type="status" class="form-control" name="status">
															<option value="{{ $p->status}}">{{ $p->status}}</option>
															<option value="">------</option>
															<option value="ACTIVE">ACTIVE</option>
															<option value="INACTIVE">INACTIVE</option>
														</select>
												</div>
											</div>

											<div class="col-md-9">
												<div class="input-group">
														<span class="input-group-addon">Policy Name</span>					
														<input name="policy_name" type="text" class="form-control" value="{{ $p->policy_name }}">
												</div>
											</div>
										</div>
										
										<div class="row form-group">

											<div class="col-md-4">
												<div class="input-group">									
													<span class="input-group-addon">Client name</span>
													<select type="id_client" class="form-control" name="id_client">
														<option value="{{ $p->id_client }}" selected>{{ $p->client->name }}</option>
														<option value="">------</option>
														@foreach ($clients as $c)
															<option value="{{ $c->id_client }}">{{ $c->name}}</option>
														@endforeach
													</select>
												</div>
											</div>

											<div class="col-md-4">
												<div class="input-group">									
													<span class="input-group-addon">Hostname</span>
													<select type="id_host" class="form-control" name="id_host">
														<option value="{{ $p->host->id_host }}" selected>{{ $p->host->hostname }}</option>
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
														<option value="{{ $p->id_database }}" selected>{{ $p->database->db_name }}</option>
														<option value="">------</option>
														@foreach ($databases as $d)
															<option value="{{ $d->id_database }}">{{ $d->db_name }}</option>
														@endforeach
													</select>
												</div>
											</div>
										</div>

										<div class="row form-group">
											<div class="col-md-6">
												<div class="input-group">									
													<span class="input-group-addon">Backup Type</span>
													<select type="backup_type" class="form-control" name="backup_type">
														<option value="{{ $p->backup_type }}">{{ $p->backup_type }}</option>
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
														<option value="{{ $p->destination }}">{{ $p->destination }}</option>
														<option value="">="">------</</option>
														<option value="SBT_TAPE">SBT_TAPE</option>
														<option value="DISK">DISK</option>
													</select>
												</div>
											</div>
										</div>

										<div class="row form-group">
											<div class="col-md-2">
												<div class="input-group">
														<span class="input-group-addon">Minute</span>					
														<input name="minute" type="text" class="form-control" value="{{ $p->minute }}">
												</div>
											</div>

											<div class="col-md-2">
												<div class="input-group">
														<span class="input-group-addon">Hour</span>					
														<input name="hour" type="text" class="form-control" value="{{ $p->hour }}">
												</div>
											</div>

											<div class="col-md-2">
												<div class="input-group">
														<span class="input-group-addon">Day</span>					
														<input name="day" type="text" class="form-control" value="{{ $p->day }}">
												</div>
											</div>

											<div class="col-md-2">
												<div class="input-group">
														<span class="input-group-addon">Month</span>					
														<input name="month" type="text" class="form-control" value="{{ $p->month }}">
												</div>
											</div>

											<div class="col-md-4">
												<div class="input-group">
														<span class="input-group-addon">Day Week</span>					
														<input name="day_week" type="text" class="form-control" value="{{ $p->day_week }}">
												</div>
											</div>
										</div>

										<div class="row form-group">
											<div class="col-md-6">
												<div class="input-group">
														<span class="input-group-addon">Duration Estimate</span>					
														<input name="duration" type="text" class="form-control" value="{{ $p->duration }}">
												</div>
											</div>							

											<div class="col-md-6">
												<div class="input-group">
														<span class="input-group-addon">Backup Size Estimate</span>					
														<input name="size_backup" type="text" class="form-control" value="{{ $p->size_backup }}">
												</div>
											</div>
										</div>

										<div class="row form-group">
											<div class="col-md-12">
												<div class="input-group">
														<span class="input-group-addon">Description</span>					
														<input name="description" type="text" class="form-control" value="{{ $p->description }}">
												</div>
											</div>
										</div>

									<div class="modal-footer">
										<a class="btn btn-default" data-dismiss="modal">Close</a>
										<button class="btn btn-warning" type="submit">Update</button> 
									</div>
								</form>
							</div>
						</div>
					</div>
				</div>

			<!-- Modal of Delete -->

				<div class="modal fade" id="modalDelete-{{ $p->id_policy}}" role="dialog" aria-labelledby="SmallModalLabel-Delete">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h4 class="modal-title">Confirmation</h4>
							</div>
							<div class="modal-body">
								<h5>Really want to delete the client <b>{{$p->policy_name}}</b>?</h5>
							</div>
							<div class="modal-footer">
								<a class="btn btn-default" data-dismiss="modal">Close</a>
								<a href="{{ action('PoliciesController@delete', [$p->id_policy]) }}" class="btn btn-danger">Delete</a>
							</div>
						</div>
					</div>
				</div>
			@endforeach
			</table>
		</div>
		
	</div>

@stop