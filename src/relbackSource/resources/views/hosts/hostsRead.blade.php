@extends('layout.principal')

@section('title', 'Hosts')

@section('content')
<div class="container container-fluid"> 
	<h1>Hosts list</h1>  
	
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

	<!-- Modal of addNew -->

		<div class="modal fade" id="modalAddNew" role="dialog" aria-labelledby="ModalLabel-AddNew">
			<div class="modal-dialog">
				<div class="modal-content">
				 	<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h2 class="modal-title">Add new Host</h2>
					</div>
					<div class="modal-body">

						<form class="form-horizontal" action="{{action('HostsController@createAdd')}}" method="POST">
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
										<input name="hostname" type="text" class="form-control" value="{{ old('hostname') }}">
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-8">
									<div class="input-group">					
											<span class="input-group-addon">IP</span>					
											<input name="ip" type="text" class="form-control" value="{{ old('ip') }}">
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

	@if(old('hostname'))
	  <div class="alert alert-success">
	    <strong>Sucess!</strong> 
	        The host {{ old('hostname') }} was created or updated.
	  </div>
	@endif

	<div class="panel panel-default">
		<table class="table table-striped">
			<tr>
				<td class="text-center"><h4><strong>Client Name</strong></h4></td>
				<td class="text-center"><h4><strong>Hostname</strong></h4></td>
				<td class="text-center"><h4><strong>Description</strong></h4></td>
				<td class="text-center"><h4><strong>Options</strong></h4></td>
			</tr>
		@foreach ($hosts as $h) 
			<tr>
				<td class="text-center">{{$h->client->name}}</td>
			    <td class="text-center">{{$h->hostname}}</td>
			    <td class="text-center">{{$h->description}}</td>
			    <td class="text-center">
					<a href="" data-target="#modalReadDetail-{{ $h->id_host }}" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-search"></span></a>
					&nbsp&nbsp<a href="" data-target="#modalUpdate-{{ $h->id_host }}" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-pencil"></span></a>
					&nbsp&nbsp<a href="" data-target="#modalDelete-{{ $h->id_host }}" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-trash"></span></a>	
			    </td>	
			</tr>

			<!-- Modal of ReadDetail -->

				<div class="modal fade" id="modalReadDetail-{{ $h->id_host }}" role="dialog" aria-labelledby="ModalLabel-ReadDetail">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title">{{$h->hostname}}</h2>
							</div>
							<div class="modal-body">								
								<ul>
									<li>
										<b>Client name:</b> {{$h->client->name}} 
									</li>
									<li>
										<b>Hostname:</b> {{$h->hostname}}
									</li>
									<li>
										<b>IP Address:</b> {{$h->ip}}
									</li>
									<li>
										<b>Client description:</b> {{$h->description}}
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

				<div class="modal fade" id="modalUpdate-{{ $h->id_host }}" role="dialog" aria-labelledby="ModalLabel-Update">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title">{{$h->hostname}}</h2>
							</div>
							<form class="form-horizontal" action="{{action('HostsController@updateSave')}}" method="POST">
								<input type="hidden" name="_token" value="{{csrf_token()}}" />
								<input type="hidden" name="id_host" value="{{ $h->id_host }}"> 
								
								<div class="modal-body">
									<div class="row form-group">
										<div class="col-md-6">
											<div class="input-group">									
												<span class="input-group-addon">Client name</span>
												<select type="id_client" class="form-control" name="id_client">
														<option value="{{ $h->id_client }}" selected>{{ $h->client->name }}</option>
														<option disabled>------</option>
													@foreach ($clients as $c)
														<option value="{{ $c->id_client }}">{{ $c->name }}</option>
													@endforeach
												</select>
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-8 ">
											<div class="input-group">
												<span class="input-group-addon">Hostname</span>
												<input type="hostname" class="form-control" name="hostname" value="{{ $h->hostname }}">
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-6 ">
											<div class="input-group">
												<span class="input-group-addon">IP Address</span>
												<input t<input type="ip" class="form-control" name="ip" value="{{ $h->ip }}">
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-12 ">
											<div class="input-group">
												<span class="input-group-addon">Description</span>
												<input type="description" class="form-control" name="description" value="{{ $h->description }}">
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

			<div class="modal fade" id="modalDelete-{{ $h->id_host}}" role="dialog" aria-labelledby="SmallModalLabel-Delete">
				<div class="modal-dialog">
					<div class="modal-content">
					 	<div class="modal-header">
							<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
							<h4 class="modal-title">Confirmation</h4>
						</div>
						<div class="modal-body">
							<h5>Really want to delete the client <bolt>{{$h->hostname}}</bolt>?</h5>
						</div>
						<div class="modal-footer">
							<a class="btn btn-default" data-dismiss="modal">Close</a>
							<a href="{{ action('HostsController@delete', [$h->id_host]) }}" class="btn btn-danger">Delete</a>
						</div>
					</div>
				</div>
			</div>

		@endforeach
		</table>
	</div>
	
</div>
@stop