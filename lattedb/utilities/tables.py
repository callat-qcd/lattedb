"""Functionality to render pandas data frame to table
"""
from pandas import DataFrame


def to_table(df: DataFrame, id_name: str) -> str:  # pylint: disable=C0103
    """Renders pandas dataframe to html sortable table
    """
    table = df.to_html(
        classes="table table-striped table-bordered table-sm",
        table_id=id_name,
        index=False,
    )
    script = """<script>
    $(document).ready(function () {{
        $.fn.dataTable.Api.register( 'sum()', function () {{
            var sum = 0;
            var total = 0;

            for ( var i=0, ien=this.length ; i<ien ; i++ ) {{
                if (this[i] == 'True') {{ sum += 1;}}
                total += 1;
            }}

            return {{exists: sum, total: total}};
        }});
        var table = $('#{id_name}').DataTable();
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
