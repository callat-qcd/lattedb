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
        $('#{id_name}').DataTable();
    }});
    </script>""".format(
        id_name=id_name
    )

    return table, script
