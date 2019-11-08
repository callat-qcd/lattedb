"""Functionality to render pandas data frame to table
"""
from pandas import DataFrame


def to_table(df: DataFrame, id_name: str) -> str:  # pylint: disable=C0103
    """Renders pandas dataframe to html sortable table
    """
    table = df.to_html(
        classes="table table-hover table-bordered table-compact table-sm",
        table_id=id_name,
        index=False,
    )
    table = table.replace(
        "</table>", f"<tfoot><th>{'</th><th>'.join(df.columns)}</th></tfoot></table>"
    )

    script = """<script>
    $(document).ready(function () {{
        // Define sum function
        $.fn.dataTable.Api.register( 'sum()', function () {{
            var sum = 0;
            var total = 0;
            for ( var i=0, ien=this.length ; i<ien ; i++ ) {{
                if (this[i] == 'True') {{ sum += 1;}}
                total += 1;
            }}
            return {{exists: sum, total: total}};
        }});
        // Add footer with serach
        $('#{id_name} tfoot th').each( function () {{
            var title = $(this).text();
            $(this).html( '<input type="text" placeholder="' + title + '"/>' );
        }});
        // Create table
        var table = $('#{id_name}').DataTable({{
            "lengthMenu": [ [10, 25, 50, -1], [10, 25, 50, "All"] ],
            "pageLength": 50,
            initComplete: function () {{
              var r = $('#{id_name} tfoot tr');
              r.find('th').each(function(){{
                $(this).css('padding', 8);
              }});
              $('#{id_name} thead').append(r);
              $('#search_0').css('text-align', 'center');
            }},
        }});
        // Apply the search
        table.columns().every( function () {{
            var that = this;
            $( 'input', this.footer() ).on( 'keyup change clear', function () {{
                if ( that.search() !== this.value ) {{
                    that.search( this.value ).draw();
                }}
            }});
        }});
        // Update progress bar
        table.on( 'search.dt', function () {{
            var info = table.column(9, {{ filter : 'applied'}} ).data().sum();
            if (info.total > 0){{
                var exists = info.exists/info.total*100;
                var pending = 100 - exists;
                $("#progress-success").attr("aria-valuenow", exists).css("width", exists.toString()+ "%");
                $("#progress-error").attr("aria-valuenow", pending).css("width", pending.toString()+ "%");
            }} else {{
                $("#progress-success").attr("aria-valuenow", 0).css("width", "0%");
                $("#progress-error").attr("aria-valuenow", 0).css("width", "0%");
            }}
        }});

    }});
    </script>""".format(
        id_name=id_name
    )

    return table, script
