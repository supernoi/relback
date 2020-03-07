// MaterializeCSS - Tab

$(document).ready(function(){
    $('.tabs').tabs({
        // swipeable : true,
        responsiveThreshold : 1920
    });
});

// MaterializeCSS - Modal

    $(document).ready(function(){
        $('.modal').modal();
    });

// MaterializeCSS - Form - Select

    $(document).ready(function(){
        $('select').formSelect();
    });

// MaterializeCSS - Form - Prefilled Input

    // $(document).ready(function() {
    //     M.updateTextFields();
    // });

    $(document).ready(function() {
        Materialize.updateTextFields(); 
    });

// Datatables used on Reports

$(document).ready(function() {

    $.fn.dataTable.moment( 'DD/MM/YY HH:mm' );

    $('#tableReport').DataTable( {
    
        "pageLength": 25,
        "lengthChange": true,
        "order": [[ 3, 'desc' ]],

        "columnDefs": [         
            { "searchable": false, "targets": 9 } ,
            { "orderable": false, "targets": 9 } ,
            { "searchable": false, "targets": 9 },

        ],

        initComplete: function () {
            this.api().columns([0,1,2,3,4,5,6,7,8]).every( function () {
                var column = this;
                var select = $('<select><option value="">All</option></select>')
                    .appendTo( $(column.footer()).empty() )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
 
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );
 
                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );
        }
    } );
} );