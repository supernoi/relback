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

		<div class="row">
			<div class="panel panel-default">
				<div class="panel-heading"><h3>Add new Host<h3></div>
					<div class="panel-body">
						<form class="form-horizontal" action="{{action('HostsController@createAdd')}}" method="POST">
							<input type="hidden" name="_token" value="{{csrf_token()}}" />
							
							<input type="hidden" name="created_id_user" value="{{ Auth::id() }}">
							
							<div class="form-group">
								<div class="col-md-6">
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
								<div class="col-md-6">
									<div class="input-group">									
										<span class="input-group-addon">Hostname</span>
										<input name="hostname" type="text" class="form-control" value="{{ old('hostname') }}">
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-6">
									<div class="input-group">					
											<span class="input-group-addon">IP</span>					
											<input name="ip" type="text" class="form-control" value="{{ old('ip') }}">
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-6">
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
									<a class="btn btn-default" href="{{action('HostsController@read')}}">Back</a>
								</div>
							</div>


						</form>
					</div>
			</div>
		</div>
	</div>
@stop