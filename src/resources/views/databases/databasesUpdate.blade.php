@extends('layout.principal')

@section('content')

	<div class="container container-fluid">
		<div class="row">
			<div class="col-md-8 col-md-offset-2">
				<div class="panel panel-default">
					<div class="panel-heading"><h3>Update Database</h3></div>
					<div class="panel-body">


					<form class="form-horizontal" action="{{action('DatabasesController@updateSave')}}" method="POST">
						<input type="hidden" name="_token" value="{{csrf_token()}}" />

						<input type="hidden" name="updated_id_user" value="{{ Auth::id() }}">
						<input type="hidden" name="id_database" value="{{ $database->id_database }}">

						<div class="form-group">
							<div class="col-md-6">
								<div class="input-group">
									<span class="input-group-addon">Client name</span>
									<select type="id_client" class="form-control" name="id_client">
											<option value="{{ $database->id_client }}">{{ $database->client->name }}</option>
											<option disabled>------</option>
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
									<select type="id_host" class="form-control" name="id_host">
											<option value="{{ $database->id_host }}">{{ $database->host->hostname }}</option>
											<option disabled>------</option>
										@foreach ($hosts as $h)
											<option value="{{ $h->hostname }}">{{ $h->hostname }}</option>
										@endforeach
									</select>
								</div>
							</div>
						</div>

						<div class="form-group">
							<div class="col-md-6">
								<div class="input-group">
									<span class="input-group-addon">Database(DB_NAME)</span>
									<input type="db_name" class="form-control" name="db_name" value="{{ $database->db_name }}">
								</div>
							</div>
						</div>							

						<div class="form-group">
							<div class="col-md-6">
								<div class="input-group">
									<span class="input-group-addon">DBID</span>
									<input type="dbid" class="form-control" name="dbid" value="{{ $database->dbid }}">
								</div>
							</div>
						</div>	

						<div class="form-group">
							<div class="col-md-6">
								<div class="input-group">
									<span class="input-group-addon">Description</span>
									<input type="description" class="form-control" name="description" value="{{ $database->description }}">
								</div>
							</div>
						</div>	

						<br>
						<div class="form-group">
							<div class="col-md-6">
								<button class="btn btn-primary" type="submit">Update</button> 
								<a class="btn btn-default" href="{{ action('DatabasesController@read') }}">Back</a>
							</div>
						</div>
					</form>

					</div>
				</div>
			</div>
		</div>
	</div>



@stop()