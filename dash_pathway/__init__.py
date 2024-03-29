import dash_cytoscape as cyto
import plotly.graph_objs as go

import pathway2cyjs
import dash_table
import pandas as pd

GLOBAL_PATHWAY_IDS = ("01100", "01110", "01120", "01130")

def Pathway(
        pathwayid=None,
        title="dash-pathway",
        width=600,
        height=600,
        node_style=None,
        edge_style=None,
        id=None,
        df=None
):
    """Returns a figure for a KEGG pathway.

Keyword arguments:
- pathwayid (string; required): A string of pathway ID
- title (string; optional): Title of the graph. (Default: "KEGGscape")
- width (int; optional): The width of the graph, in px. (Default: 600)
- height (int; optional): The height of the graph, in px. (Default: 600)
- node_style (dictionary; optional): The style of the nodes. (Default: None)
- edge_style (dictionary; optional): The style of the edges. (Default: None)
- id (string; optional): The ID used to identify this component in Dash callbacks.
- df (pd.DataFrame; optional): The user data matrix. (Default: None)

    # ...
    Example 1: eco00020 Plot
    '''
    fig = create_keggscape("eco00020", title='TCA for E.coli plot')

    plotly.offline.plot(fig, image='png')
    '''

    """
    # print(pathwayid)

    ks = _Pathway(
        pathwayid,
        width=width,
        height=height,
        node_style=node_style,
        edge_style=edge_style,
        id=id,
        df=df
    )

    return ks.figure(
        title=title
    )

class _Pathway():
    """ A Dash Bio Pathway class.

Keyword arguments:

- pathwayid (string; required): A string of pathway ID
- width (int; optional): The width of the graph, in px. (Default: 600)
- height (int; optional): The height of the graph, in px. (Default: 600)
- node_style (dictionary; optional): The style of the nodes. (Default: None)
- edge_style (dictionary; optional): The style of the edges. (Default: None)
- id (string; optional): The ID used to identify this component in Dash callbacks.
- df (pd.DataFrame; optional): The user data matrix. (Default: None)"""

# Returns:
#     - object: A Dash Bio Pathway object.

    def __init__(
        self,
        x,
        width=600,
        height=600,
        node_style=None,
        edge_style=None,
        id=None,
        df=None
    ):
        # print(x)
        self.pathwayid = x
        self.width = width
        self.height = height
        self.node_style = node_style
        self.edge_style = edge_style
        self.id = id
        self.df = df

    def figure(
            self,
            title="Pathway Plot",
    ):
        """

    Keyword arguments:
    - title (string; optional): Title of the graph. (Default: "Pathway Plot")

    Returns:
    - object: A figure compatible with plotly.graph_objs."""

        if self.pathwayid.startswith("WP"):
            elems = pathway2cyjs.wp2cyelements(self.pathwayid)
        else:
            elems = pathway2cyjs.kegg2cyjs(self.pathwayid)
        
        # node_table = pathway2cyjs.cynodes2df(elems['nodes'])

        # if self.pathwayid[3:] not in GLOBAL_PATHWAY_IDS:
        #     gene_table = node_table[node_table['keggtype'] == "gene"]
        #     cynode_table = gene_table[['id', 'keggids', 'name']]
        #     tidy_table = cynode_table.assign(keggids=cynode_table.keggids.str.split(" ")).explode('keggids')

        # # result = pd.merge(tidy_table[['id', 'keggids', 'name']], self.df, on='keggids')

        #     if isinstance(self.df, pd.DataFrame):
        #         # print(self.df.shape)
        #         result = pd.merge(tidy_table[['id', 'keggids', 'name']], self.df, on='keggids')
        #         result = result.sort_values(by=['id'])
        #     else:
        #         result = tidy_table
        # else:
        #     result = pathway2cyjs.cynodes2df(elems['edges'])
        #     result = result.assign(genes=result.genes.str.split(" ")).explode('genes')

        #     if isinstance(self.df, pd.DataFrame):
        #         # print(self.df)
        #         result = pd.merge(result, self.df, on='genes')
        #         result = result.sort_values(by=['id'])

        if self.pathwayid.startswith("WP"):
            stylesheet = pathway2cyjs.WIKIPATHWAYS_STYLE[0]["style"]
        elif self.pathwayid[3:] in GLOBAL_PATHWAY_IDS:
            stylesheet = pathway2cyjs.KEGG_GLOBAL_STYLE[0]["style"]
        else:
            stylesheet = pathway2cyjs.KEGG_STYLE[0]["style"]
        
        if self.node_style:
            stylesheet[0]["css"] = {**stylesheet[0]["css"], **self.node_style}
        
        if self.edge_style:
            stylesheet[-2]["css"] = {**stylesheet[-2]["css"], **self.edge_style}
        
        return cyto.Cytoscape(
                    id = self.id,
                    style = {'width': str(self.width)+'px', 'height': str(self.height)+'px'},
                    stylesheet = stylesheet,
                    elements = elems['nodes'] + elems['edges'],
                    layout = {'name': 'preset'})
                # dash_table.DataTable(                                                                                                                                                                               id='cytoscape-node-table',
                #     columns=[{"name": i, "id": i} for i in result.columns],
                #     data=result.to_dict('records'))]
                #     # columns=[{"name": i, "id": i} for i in node_table.columns],
                #     # data=node_table.to_dict('records'))]
