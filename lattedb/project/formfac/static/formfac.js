$(document).ready(function() {
    // Add footer with serach
    $('#table tfoot th').each(function() {
        var title = $(this).text();
        $(this).html('<input type="text" placeholder="' + title + '"/>');
    });
    // Create table
    var table = $('#table').DataTable({
        "lengthMenu": [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        "pageLength": 50,
        initComplete: function() {
            var r = $('#table tfoot tr');
            r.find('th').each(function() {
                $(this).css('padding', 8);
            });
            $('#table thead').append(r);
            $('#search_0').css('text-align', 'center');
        },
    });
    // Apply the search
    table.columns().every(function() {
        var that = this;
        $('input', this.footer()).on('keyup change clear', function() {
            if (that.search() !== this.value) {
                that.search(this.value).draw();
            }
        });
    });

});
