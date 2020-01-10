$(document).ready(function () {
    function delete_button(idx) {
        return '<a href="/delete/' + idx + '">' +
            '<button type="button" class="btn btn-red btn-sm m-0" >Delete</button>' +
        '</a>';
    };

    var table = $('#requests').DataTable({
        "ajax": "/data",
        "buttons": ["clear"],
        "columns": [
            {
                "className": "details-control",
                "defaultContent": '<i class="fas fa-expand-arrows-alt"></i>',
                "data": null,
                "orderable": false
            },
            { "data": "datetime" },
            { "data": "method" },
            { "data": "path" },
            { "data": "params" },
            {
                "className": 'dt-body-right',
                "data": "idx",
                "orderable": false,
                "render": function(data, type, row, meta) {
                    return delete_button(data);
                }
            },
        ],
    });

    function format(data) {
        var headers = "";
        for (var [key, value] of Object.entries(data.headers)) {
            headers += '<tr>' +
                '<td class="title">' + key + '</td>' +
                '<td>' + value + '</td>' +
                '</tr>';
        };

        return '<div class="details-container">' +
            '<table cellpadding="5" cellspacing="0" border="0" class="details-table">' +
            '<tr>' +
            '<td class="title" colspan=2>Headers</td>' +
            '</tr>' +
            headers +
            '</table>' +
            '</div>';
    };

    $('.datatables tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr'),
            row = table.row(tr);

        if (row.child.isShown()) {
            tr.next('tr').removeClass('details-row');
            row.child.hide();
            tr.removeClass('shown');
            $(this.children[0]).removeClass('fa-compress-arrows-alt');
            $(this.children[0]).addClass('fa-expand-arrows-alt');
        }
        else {
            row.child(format(row.data())).show();
            tr.next('tr').addClass('details-row');
            tr.addClass('shown');
            $(this.children[0]).addClass('fa-compress-arrows-alt');
            $(this.children[0]).removeClass('fa-expand-arrows-alt');
        }
    });
});
