<html>  
	<head>  
		<title>relBack - Backup Schedule</title>  
		<meta http-equiv="content-type" content="text/html;charset=utf-8" />  
		<style type="text/css"> 
			#server 
			{ 
				font-family:"Trebuchet MS", Arial, Helvetica, sans-serif; 
				width:100%; 
				border-collapse:collapse; 
			} 
			#server td, #server th  
			{ 
				font-size:11px; 
				border-top: 1px solid #ddd; 
				padding:3px 7px 2px 7px;  
			} 
			#server th  
			{ 
				font-size:12px; 
				text-align:left;  
				padding-top:5px;  
				padding-bottom:4px; 
				background-color:#f5f5f5; 
				color:#333; 
			} 
			#server tr.alt td 
			{ 
				color:#000000;  
				background-color:#EAF2D3; 
			} 
			#server td.textcenter, 
			#server th.textcenter {
				text-align: center;
			}
		</style>  
	</head> 
	<body>  
		 
		<table id="server">
			<tr>
				<th colspan="15" bgcolor="#101010"> 
					<center>
						<font face="Courier" size=20 color="bdccd4">rel</font><font face="Courier New Bold,Courier" size=20 color="569bbe"><b>Back</b></font>
						<br>
					</center>
				</th>
			</tr>
			<tr>
				<th colspan="15">
					<center>
						<h4>Report date...............: {!! date('d/m/Y H:i:s'); !!} </h4>
					</center>
				</th>
			</tr>
		</table>
		<br>
		<table id="server">

			@php
			$l_title_cols=
					'<tr>				
						<h4>					
							<th class="textcenter" > POL </th>
							<th class="textcenter" > Hostname </th>
							<th class="textcenter" > db_name </th>
							<th class="textcenter" > Status </th>
							<th class="textcenter" > Start Estimate </th>
							<th class="textcenter" > Start Real </th>
							<th class="textcenter" > Time Max </th>
							<th class="textcenter" > Time Real </th>
							<th class="textcenter" > Size MAX(GB) </th>
							<th class="textcenter" > Size Real(GB) </th>
							<th class="textcenter" > Content </th>
							<th class="textcenter" > Destiny </th>
							<th class="textcenter" > Description </th>
						</h4>				
					</tr>'
			@endphp		

			@php 
				$dateRowSucess = date('d/m/Y')+1;
				$dateRowFailed = date('d/m/Y')+1;
			@endphp

			@foreach ($reportMailDefault as $r)

				@if($dateRowFailed != date('d/m/Y', strtotime($r->schedule_start)) && ($r->status == 'FAILED' || $r->status=='COMPLETED WITH WARNINGS'))
					@php $dateRowFailed = date('d/m/Y', strtotime($r->schedule_start)); @endphp				
						<tr>
							<th colspan="15">
								<center>
									<h4>
										Highlight of the backups initiated in {!! date('d/m/Y', strtotime($r->schedule_start)) !!} with WARNING or FAIL
									</h4>
								</center>
							</th>
						</tr>
						{!!	$l_title_cols !!}
				@endif	
						
				@if($dateRowFailed == date('d/m/Y', strtotime($r->schedule_start)) && ($r->status == 'FAILED' || $r->status=='COMPLETED WITH WARNINGS'))

					@if($r->status=='COMPLETED') 
						@php $trColor = '#dff0d8' @endphp
					@elseif($r->status=='SCHEDULED')
						@php $trColor = '#d9edf7' @endphp				
					@elseif($r->status=='NOT RUN')
						@php $trColor = '#f2dede' @endphp							
					@elseif($r->status=='RUNNING') 
						@php $trColor = '#f5f5f5' @endphp
					@elseif($r->status=='COMPLETED WITH WARNINGS') 
						@php $trColor = '#fcf8e3' @endphp
					@elseif($r->status=='FAILED') 
						@php $trColor = '#f2dede' @endphp
					@endif

					<tr style="background-color:{!! $trColor !!};">

						<td class="textcenter" > {!! $r->id_policy !!} </td>
						<td class="textcenter" > {!! $r->hostname !!} </td>
						<td class="textcenter" > {!! $r->db_name !!} </td>
						<td class="textcenter" > {!! $r->status !!} </td>
						<td class="textcenter" > {!! date('d/m H:i', strtotime($r->schedule_start)) !!} </td>
						<td class="textcenter" > {!! date('d/m H:i', strtotime($r->start_r)) !!} </td>			
						<td class="textcenter" > {!! $r->duration_e !!} </td>
						<td class="textcenter" > {!! $r->duration_r !!} </td>
						<td class="textcenter" > {!! $r->size_backup_p_gb !!} </td>
						<td class="textcenter" > {!! $r->size_backup_r_gb !!} </td>
						<td class="textcenter" > {!! $r->backup_type !!} </td>
						<td class="textcenter" > {!! $r->destination !!} </td>
						<td class="textcenter" > {!! $r->description !!} </td>
					</tr>
				@endif
			@endforeach

			@foreach ($reportMailDefault as $r)

				@if($dateRowFailed != date('d/m/Y', strtotime($r->schedule_start)))
					@php $dateRowFailed = date('d/m/Y', strtotime($r->schedule_start)); @endphp				
						<tr>
							<th colspan="15">
								<center>
									<h4>
										Complete list of backups initiated in {!! date('d/m/Y', strtotime($r->schedule_start)) !!}
									</h4>
								</center>
							</th>
						</tr>
						{!!	$l_title_cols !!}
				@endif	
						
				@if($dateRowFailed == date('d/m/Y', strtotime($r->schedule_start)))

					@if($r->status=='COMPLETED') 
						@php $trColor = '#dff0d8' @endphp
					@elseif($r->status=='SCHEDULED')
						@php $trColor = '#d9edf7' @endphp				
					@elseif($r->status=='NOT RUN')
						@php $trColor = '#f2dede' @endphp							
					@elseif($r->status=='RUNNING') 
						@php $trColor = '#f5f5f5' @endphp
					@elseif($r->status=='COMPLETED WITH WARNINGS') 
						@php $trColor = '#fcf8e3' @endphp
					@elseif($r->status=='FAILED') 
						@php $trColor = '#f2dede' @endphp
					@endif

					<tr style="background-color:{!! $trColor !!};">

						<td class="textcenter" > {!! $r->id_policy !!} </td>
						<td class="textcenter" > {!! $r->hostname !!} </td>
						<td class="textcenter" > {!! $r->db_name !!} </td>
						<td class="textcenter" > {!! $r->status !!} </td>
						<td class="textcenter" > {!! date('d/m H:i', strtotime($r->schedule_start)) !!} </td>
						<td class="textcenter" > {!! (empty($r->start_r) ? '' : date('d/m H:i', strtotime(($r->start_r)))) !!} </td>			
						<td class="textcenter" > {!! (empty($r->duration_r) ? '' : $r->duration_e) !!} </td>
						<td class="textcenter" > {!! $r->duration_r !!} </td>
						<td class="textcenter" > {!! (empty($r->size_backup_r_gb) ? '' : $r->size_backup_p_gb) !!} </td>
						<td class="textcenter" > {!! $r->size_backup_r_gb !!} </td>
						<td class="textcenter" > {!! $r->backup_type !!} </td>
						<td class="textcenter" > {!! $r->destination !!} </td>
						<td class="textcenter" > {!! $r->description !!} </td>
					</tr>
				@endif
			@endforeach	

		</table>  
		<br>
		<footer class="container-fluid textcenter">
			<center>
				<a href="#top" title="To Top">
					<span class="glyphicon glyphicon-chevron-up"></span>
				</a>
				<p><h4>Random Report Company</h4></p>
					<a target="_blank" href="https://github.com/supernoi/relback" alt="GitHub of relBack">
						github.com/relBack
					</a>
				<p>Created by <a href="{{action('HomeController@about')}}">Creators</a>, duh!</p>

				<br>
			</center>
		</footer>
	</body> 
</html>