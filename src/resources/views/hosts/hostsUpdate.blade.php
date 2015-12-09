@extends('layout.principal')

@section('content')

	<div class="container container-fluid">
		<div class="row">
			<div class="col-md-8 col-md-offset-2">
				<div class="panel panel-default">
					<div class="panel-heading"><h3>Update Hostname</h3></div>
					<div class="panel-body">


					<form class="form-horizontal" action="{{action('HostsController@updateSave')}}" method="POST">
						<input type="hidden" name="_token" value="{{csrf_token()}}" />

						<input type="hidden" name="id_host" value="{{ $host->id_host }}">

						<div class="form-group">
							<div class="col-md-6">
								<div class="input-group">									
									<span class="input-group-addon">Client name</span>
									<select type="id_client" class="form-control" name="id_client">
											<option value="{{ $host->id_client }}" selected>{{ $host->client->name }}</option>
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
									<input type="hostname" class="form-control" name="hostname" value="{{ $host->hostname }}">
								</div>
							</div>
						</div>

						<div class="form-group">
							<div class="col-md-6">
								<div class="input-group">
									<span class="input-group-addon">IP</span>
									<input type="ip" class="form-control" name="ip" value="{{ $host->ip }}">
								</div>
							</div>
						</div>								

						<div class="form-group">
							<div class="col-md-6">
								<div class="input-group">
									<span class="input-group-addon">Description</span>
									<input type="description" class="form-control" name="description" value="{{ $host->description }}">
								</div>
							</div>
						</div>	

						<br>
						<div class="form-group">
							<div class="col-md-6">
								<button class="btn btn-primary" type="submit">Update</button> 
								<a class="btn btn-default" href="{{ action('HostsController@read') }}">Back</a>
							</div>
						</div>
					</form>

					</div>
				</div>
			</div>
		</div>
	</div>



@stop()