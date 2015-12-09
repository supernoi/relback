@extends('layout.principal')

@section('content')

	<div class="container container-fluid">
		<div class="row">
			<div class="col-md-8 col-md-offset-2">
				<div class="panel panel-default">
					<div class="panel-heading"><h3>Update Client</h3></div>
					<div class="panel-body">

					<form class="form-Vertica" action="{{action('ClientsController@updateSave')}}" method="POST">
						<input type="hidden" name="_token" value="{{csrf_token()}}" />

						<input type="hidden" name="id_client" value="{{ $client->id_client }}">

						<div class="form-group">
							<div class="col-md-6">
								<div class="input-group">
									<span class="input-group-addon">Client name</span>
									<input type="name" class="form-control" name="name" value="{{ $client->name }}">
								</div>
							</div>
						</div>					

						<div class="form-group">
							<div class="col-md-6">
								<div class="input-group">
									<span class="input-group-addon">Description</span>
									<input type="description" class="form-control" name="description" value="{{ $client->description }}">
								</div>
							</div>
						</div>	

						<br>
						<div class="form-group">
							<div class="col-md-6">
								<button class="btn btn-primary" type="submit">Update</button> 
								<a class="btn btn-default" href="{{ action('ClientsController@read') }}">Back</a>
							</div>
						</div>
					</form>

					</div>
				</div>
			</div>
		</div>
	</div>



@stop()