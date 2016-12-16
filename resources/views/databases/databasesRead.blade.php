@extends('layout.principal')

@section('title', 'Databases')

@section('content')

	<div class="container container-fluid"> 
		<h1>Databases list</h1>  
		
		<br>
		<a href="" data-target="#modalAddNew" id="fetch" data-toggle="modal"  class="btn btn-primary">Add New</a>
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

	<!-- Modal of addNew -->

		<div class="modal fade" id="modalAddNew" role="dialog" aria-labelledby="ModalLabel-AddNew">
			<div class="modal-dialog">
				<div class="modal-content">
				 	<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h2 class="modal-title">Add new Database</h2>
					</div>
					<div class="modal-body">

						<form class="form-horizontal" action="{{action('DatabasesController@createAdd')}}" method="POST">
							<input type="hidden" name="_token" value="{{csrf_token()}}" />
							
							<input type="hidden" name="created_id_user" value="{{ Auth::id() }}">
							
							<div class="form-group">
								<div class="col-md-10">
									<div class="input-group">									
										<span class="input-group-addon">Client name</span>
										<select type="id_client" class="form-control" name="id_client">
											@foreach ($clients as $c)
												<option value="{{ $c->id_client }}">{{ $c->name }}</option>
											@endforeach
										</select>
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-10">
									<div class="input-group">									
										<span class="input-group-addon">Hostname</span>
										<select type="id_host" class="form-control" name="id_host">
											@foreach ($hosts as $h)
												<option value="{{ $h->id_host}}">{{ $h->hostname }}</option>
											@endforeach
										</select>
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-10">
									<div class="input-group">					
											<span class="input-group-addon">Database(DB_NAME)</span>					
											<input name="db_name" type="text" class="form-control" value="{{ old('db_name') }}">
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-8">
									<div class="input-group">					
											<span class="input-group-addon">DBID</span>					
											<input name="dbid" type="text" class="form-control" value="{{ old('dbid') }}">
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
	<!-- End Modal of addNew -->

		@if(old('db_name'))
		  <div class="alert alert-success">
		    <strong>Sucess!</strong> 
		        The host {{ old('db_name') }} was created or updated.
		  </div>
		@endif

		<div class="panel panel-default">
			<table class="table table-striped">
				<tr>
					<th class="text-center"><h4><strong>Client Name</strong></h4></th>
					<th class="text-center"><h4><strong>Hostname</strong></h4></th>
					<th class="text-center"><h4><strong>DB_NAME</strong></h4></th>
					<th class="text-center"><h4><strong>DBID</strong></h4></th>			
					<th class="text-center"><h4><strong>Description</strong></h4></th>
					<th class="text-center"><h4><strong>Options</strong></h4></th>
				</tr>
			@foreach ($databases as $d) 
				<tr>
					<td class="text-center">{{$d->client->name}}</td>
				    <td class="text-center">{{$d->host->hostname}}</td>
				    <td class="text-center">{{$d->db_name}}</td>
				    <td class="text-center">{{$d->dbid}}</td>
				    <td class="text-center">{{$d->description}}</td>
				    <td class="text-center">
						<a href="" data-target="#modalReadDetail-{{ $d->id_database }}" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-search"></span></a>
						&nbsp&nbsp<a href="" data-target="#modalUpdate-{{ $d->id_database }}" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-pencil"></span></a>
						&nbsp&nbsp<a href="" data-target="#modalDelete-{{ $d->id_database }}" id="fetch" data-toggle="modal" ><span class="glyphicon glyphicon-trash"></span></a>	
				    </td>	
				</tr>

			<!-- Modal of ReadDetail -->

				<div class="modal fade" id="modalReadDetail-{{ $d->id_database }}" role="dialog" aria-labelledby="ModalLabel-ReadDetail">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title">{{$d->db_name}}</h2>
							</div>
							<div class="modal-body">								
								<ul>
									<li>
										<b>Client name:</b> {{$d->client->name}} 
									</li>
									<li>
										<b>Hostname:</b> {{$d->host->hostname}}
									</li>
									<li>
										<b>DB_NAME:</b> {{$d->db_name}}
									</li>
									<li>
										<b>DBID:</b> {{$d->dbid}}
									</li>
									<li>
										<b>Client description:</b> {{$d->description}}
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

				<div class="modal fade" id="modalUpdate-{{ $d->id_database }}" role="dialog" aria-labelledby="ModalLabel-Update">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title">{{$d->db_name}}</h2>
							</div>
							<form class="form-horizontal" action="{{action('DatabasesController@updateSave')}}" method="POST">
								<input type="hidden" name="_token" value="{{csrf_token()}}" />
								<input type="hidden" name="id_database" value="{{ $d->id_database }}"> 
								
								<div class="modal-body">
									<div class="row form-group">
										<div class="col-md-6">
											<div class="input-group">									
												<span class="input-group-addon">Client name</span>
												<select type="id_client" class="form-control" name="id_client">
														<option value="{{ $d->id_client }}" selected>{{ $d->client->name }}</option>
														<option disabled>------</option>
													@foreach ($clients as $c)
														<option value="{{ $c->id_client }}">{{ $c->name }}</option>
													@endforeach
												</select>
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-6">
											<div class="input-group">
												<span class="input-group-addon">Hostname</span>
												<select type="id_host" class="form-control" name="id_host">
														<option value="{{ $d->id_host }}">{{ $d->host->hostname }}</option>
														<option disabled>------</option>
													@foreach ($hosts as $h)
														<option value="{{ $h->id_host }}">{{ $h->hostname }}</option>
													@endforeach
												</select>
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-8 ">
											<div class="input-group">
												<span class="input-group-addon">Hostname</span>
												<input type="db_name" class="form-control" name="db_name" value="{{ $d->db_name }}">
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-6 ">
											<div class="input-group">
												<span class="input-group-addon">DBID</span>
												<input t<input type="dbid" class="form-control" name="dbid" value="{{ $d->dbid }}">
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-12 ">
											<div class="input-group">
												<span class="input-group-addon">Description</span>
												<input type="description" class="form-control" name="description" value="{{ $d->description }}">
											</div>
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

			<!-- Modal of Delete -->

				<div class="modal fade" id="modalDelete-{{ $d->id_database }}" role="dialog" aria-labelledby="SmallModalLabel-Delete">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h4 class="modal-title">Confirmation</h4>
							</div>
							<div class="modal-body">
								<h5>Really want to delete the client <b>{{$d->db_name}}</b>?</h5>
							</div>
							<div class="modal-footer">
								<a class="btn btn-default" data-dismiss="modal">Close</a>
								<a href="{{ action('DatabasesController@delete', [$d->id_database]) }}" class="btn btn-danger">Delete</a>
							</div>
						</div>
					</div>
				</div>

			@endforeach
			</table>
		</div>
		
	</div>

@stop