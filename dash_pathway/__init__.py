import dash_cytoscape as cyto
import plotly.graph_objs as go

import kegg2cyjs
import dash_table
import pandas as pd

GLOBAL_PATHWAY_IDS = ("01100", "01110", "01120", "01130")

def KeggScape(
        pathwayid=None,
        title="KEGGscape",
        width=600,
        height=600,
        df=None
):
    """Returns a figure for a KEGG pathway.

Keyword arguments:
- pathwayid (string; required): A string of KEGG pathway ID
- title (string; optional): Title of the graph. (Default: "KEGGscape")
- width (int; optional): The width of the graph, in px. (Default: 600)
- height (int; optional): The height of the graph, in px. (Default: 600)
- df (pd.DataFrame; optional): The user data matrix. (Default: None)

    # ...
    Example 1: eco00020 Plot
    '''
    fig = create_keggscape("eco00020", title='TCA for E.coli plot')

    plotly.offline.plot(fig, image='png')
    '''

    """
    # print(pathwayid)

    ks = _KeggScape(
        pathwayid,
        width=width,
        height=height,
        df=df
    )

    return ks.figure(
        title=title
    )

class _KeggScape():
    """ A Dash Bio KeggScape class.

Keyword arguments:

- pathwayid (string; required): A string of KEGG pathway ID
- width (int; optional): The width of the graph, in px. (Default: 600)
- height (int; optional): The height of the graph, in px. (Default: 600)
- df (pd.DataFrame; optional): The user data matrix. (Default: None)"""

# Returns:
#     - object: A Dash Bio KEGGscape object.

    def __init__(
        self,
        x,
        width=600,
        height=600,
        df=None
    ):
        # print(x)
        self.pathwayid = x
        self.width = width
        self.height = height
        self.df = df

    def figure(
            self,
            title="KEGGscape Plot",
    ):
        """

    Keyword arguments:
    - title (string; optional): Title of the graph. (Default: "KEGGscape Plot")

    Returns:
    - object: A figure compatible with plotly.graph_objs."""

        elems = kegg2cyjs.kegg2cyjs(self.pathwayid)
        node_table = kegg2cyjs.nodes2df(elems['nodes'])

        if self.pathwayid[3:] not in GLOBAL_PATHWAY_IDS:
            gene_table = node_table[node_table['keggtype'] == "gene"]
            cynode_table = gene_table[['id', 'keggids', 'name']]
            tidy_table = cynode_table.assign(keggids=cynode_table.keggids.str.split(" ")).explode('keggids')

        # result = pd.merge(tidy_table[['id', 'keggids', 'name']], self.df, on='keggids')

            if isinstance(self.df, pd.DataFrame):
                # print(self.df.shape)
                result = pd.merge(tidy_table[['id', 'keggids', 'name']], self.df, on='keggids')
                result = result.sort_values(by=['id'])
            else:
                result = tidy_table
        else:
            result = kegg2cyjs.nodes2df(elems['edges'])
            result = result.assign(genes=result.genes.str.split(" ")).explode('genes')

            if isinstance(self.df, pd.DataFrame):
                # print(self.df)
                result = pd.merge(result, self.df, on='genes')
                result = result.sort_values(by=['id'])

        if self.pathwayid[3:] in GLOBAL_PATHWAY_IDS:
            stylesheet = kegg2cyjs.KEGG_GLOBAL_STYLE[0]["style"]
        else:
            stylesheet = kegg2cyjs.KEGG_STYLE[0]["style"]
        
        return [cyto.Cytoscape(
                    id='cytoscape',
                    style= {'width': str(self.width)+'px', 'height': str(self.height)+'px'},
                    stylesheet=stylesheet,
                    elements=elems['nodes'] + elems['edges'],
                    layout={'name': 'preset'}),
                dash_table.DataTable(                                                                                                                                                                               id='cytoscape-node-table',
                    columns=[{"name": i, "id": i} for i in result.columns],
                    data=result.to_dict('records'))]
                    # columns=[{"name": i, "id": i} for i in node_table.columns],
                    # data=node_table.to_dict('records'))]
