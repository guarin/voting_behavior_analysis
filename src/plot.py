import holoviews as hv
from bokeh.embed import file_html

# from bokeh.embed import autoload_static
from bokeh.resources import CDN
from bokeh.models import HoverTool
import metadata
import pandas as pd
import numpy as np
import networkx as nx

hv.extension("bokeh")


PLOT_FOLDER = "../docs/"
SCRIPT_FOLDER = "assets/js/"
ELEMENT_FOLDER = "assets/plot_elements/"
HTML_FOLDER = "assets/html/"


def save_plot(plot, name, print_element=True):
    """Saves a holoviews plot to be used for the data story."""

    renderer = hv.renderer("bokeh")
    plot = renderer.get_plot(plot)
    html = file_html(plot.state, CDN, name)
    with open(PLOT_FOLDER + HTML_FOLDER + name + ".html", "w+") as file:
        file.write(html)

    src = HTML_FOLDER + name + ".html"
    element = f"""<iframe src="{src}" width="100%" height="500" scrolling="no" seamless="seamless" frameborder="0"></iframe>"""
    with open(PLOT_FOLDER + ELEMENT_FOLDER + name + ".html", "w+") as file:
        file.write(element)
    if print_element:
        print(element)

    # plot = plot.options(sizing_mode="scale_both")
    # renderer = hv.renderer("bokeh")
    # plot_state = renderer.get_plot(plot).state
    #
    # if isinstance(plot, hv.Layout):
    #     plot_state.children[0].toolbar.logo = None
    #
    # script_path = SCRIPT_FOLDER + name + ".js"
    # script, element = autoload_static(plot_state, CDN, script_path)
    #
    # with open(PLOT_FOLDER + SCRIPT_FOLDER + name + ".js", "w+") as file:
    #     file.write(script)
    #
    #
    #
    # if print_element:
    #     print(element.strip())
    #
    # return script, element


def _disable_logo(plot, element):
    plot.state.toolbar.logo = None


def _hover_text(display_name, column):
    if display_name:
        return f"""
        <div>
            <span style="font-size: 12px;"><b>{display_name}:</b> @{column}</span>
        </div> 
        """
    else:
        return f"""
        <div>
            <span style="font-size: 12px;">@{column}</span>
        </div> 
        """


def _hover_img(column):
    return f"""
    <div>
        <img
            src="@{column}" height="42" alt="{column}" width="42"
            style="float: left; margin: 0px 15px 15px 0px;"
            border="2"
        ></img>
    <div>
    """


def hover_tool(columns=None, img_columns=None):
    """Creates a new hover tool with custom columns."""
    html = ""
    if img_columns:
        for column in img_columns:
            html += _hover_img(column)
    if columns:
        if isinstance(columns, list):
            columns = {col: col for col in columns}
        for column, name in columns.items():
            html += _hover_text(name, column)
    if len(html) > 0:
        return HoverTool(tooltips=[("", html)])
    else:
        return None


DEFAULT_HOVER = hover_tool(columns={"FullName": "", "PartyAbbreviation": ""})


def _node_info(nodes_array, df=None):
    if df is None:
        df = pd.DataFrame(index=np.arange(len(nodes_array)))
    info = df.copy()
    info["x"] = nodes_array[:, 0]
    info["y"] = nodes_array[:, 1]
    info["index"] = info.index.values
    return info


def _nodes(node_positions, info_df=None):
    """Returns a Nodes object from a networkx graph or a list of node positions."""
    if isinstance(node_positions, dict):
        indices = np.array(list(node_positions.keys()))
        node_positions = np.array(list(node_positions.values()))[indices]

    info = _node_info(node_positions, info_df)
    kdims = ["x", "y", "index"]
    vdims = list(info.columns.drop(kdims))
    return hv.Nodes(info, kdims=kdims, vdims=vdims)


DEFAULT_NODE_OPTS = {
    "xaxis": None,
    "yaxis": None,
    "width": 400,
    "height": 400,
    "size": 10,
    "padding": 0.05,
    "show_legend": False,
    "default_tools": ["pan", "box_zoom", "reset"],
    "finalize_hooks": [_disable_logo],
    "active_tools": ["box_zoom"],
}


def _default_info_df_opts(info_df=None, cluster_column=None, hover="default"):
    opts = dict()
    if info_df is not None:
        if cluster_column == "SimplePartyAbbreviation":
            opts["cmap"] = metadata.PARTY_COLOR

        elif cluster_column == "Group":
            opts["cmap"] = metadata.GROUP_COLOR

        if hover == "default":
            opts["tools"] = [DEFAULT_HOVER]

        elif hover is not None:
            opts["tools"] = [hover]
    return opts


def _nodes_opts(nodes, info_df=None, cluster_column=None, hover="default", **kwargs):
    opts = dict()
    opts.update(DEFAULT_NODE_OPTS)
    if isinstance(cluster_column, str) and (info_df is not None):
        opts["color"] = cluster_column

    info_df_opts = _default_info_df_opts(info_df, cluster_column, hover)
    opts.update(info_df_opts)
    opts.update(kwargs)
    return nodes.options(**opts)


def nodes(node_positions, info_df=None, cluster_column=None, hover="default", **kwargs):
    """Creates a new nodes plot."""
    info_df, cluster_column = _add_cluster_column(info_df, cluster_column)
    n = _nodes(node_positions, info_df)
    n = _nodes_opts(n, info_df, cluster_column, hover, **kwargs)
    return n


def _graph(edges, node_positions, info_df=None, cluster_column=None):
    # have to add clusters explicitly
    if isinstance(cluster_column, np.ndarray):
        info_df = info_df.copy()
        info_df["node_color"] = cluster_column.astype(int)

    nodes = _nodes(node_positions, info_df)
    source, target = edges.T
    graph = hv.Graph(((source, target), nodes))
    return graph


def _graph_from_nx(
    nx_graph, node_positions=nx.spring_layout, info_df=None, cluster_column=None
):
    edges = np.asarray(nx_graph.edges)
    if callable(node_positions):
        node_positions = node_positions(nx_graph)
    graph = _graph(edges, node_positions, info_df, cluster_column)
    return graph


DEFAULT_GRAPH_OPTS = {
    "xaxis": None,
    "yaxis": None,
    "width": 400,
    "height": 400,
    "node_size": 10,
    "edge_line_width": 1,
    "padding": 0.05,
    "default_tools": ["pan", "box_zoom", "reset", "tap"],
    "finalize_hooks": [_disable_logo],
    "active_tools": ["box_zoom"],
}


def _graph_opts(graph, info_df=None, cluster_column=None, hover="default", **kwargs):
    opts = dict()
    opts.update(DEFAULT_GRAPH_OPTS)
    if isinstance(cluster_column, str) and (info_df is not None):
        opts["node_color"] = cluster_column

    info_df_opts = _default_info_df_opts(info_df, cluster_column, hover)
    opts.update(info_df_opts)
    opts.update(kwargs)
    return graph.options(**opts)


def _add_cluster_column(info_df=None, cluster_column=None):
    if isinstance(cluster_column, np.ndarray):
        if info_df is None:
            info_df = pd.DataFrame({"cluster_color": cluster_column})
        else:
            info_df = info_df.copy()
            info_df["cluster_color"] = cluster_column.astype(int)
        cluster_column = "cluster_color"
    return info_df, cluster_column


def graph_from_nx(
    nx_graph,
    node_positions=nx.spring_layout,
    info_df=None,
    cluster_column=None,
    hover="default",
    **opts,
):
    """Creates a new graph from a networkx graph."""
    info_df, cluster_column = _add_cluster_column(info_df, cluster_column)
    g = _graph_from_nx(nx_graph, node_positions, info_df)
    g = _graph_opts(g, info_df, cluster_column, hover, **opts)
    return g


def graph(
    edges, node_positions, info_df=None, cluster_column=None, hover="default", **opts
):
    """Creates a new graph from a set of edges and node positions."""
    info_df, cluster_column = _add_cluster_column(info_df, cluster_column)
    g = _graph(edges, node_positions, info_df)
    g = _graph_opts(g, info_df, cluster_column, hover, **opts)
    return g


LEGEND_POINT_OPTS = {
    "color": "color",
    "size": 15,
    "xaxis": None,
    "yaxis": None,
    "data_aspect": 1,
    "default_tools": [],
    "hooks": [_disable_logo],
    "show_frame": False,
}

LEGEND_TEXT_OPTS = {
    "text_align": "left",
    "default_tools": [],
    "data_aspect": 1,
}

LEGEND_OVERLAY_OPTS = {
    "shared_axes": False,
    "data_aspect": 1,
}


def legend(names, colors, positions=None):
    n = len(names)
    x = np.zeros(n)
    if positions is None:
        y = np.arange(n)[::-1]
    else:
        y = positions
    df = pd.DataFrame({"x": x, "y": y, "name": names, "color": colors})

    points = _legend_points(df)
    texts = _legend_texts(df)
    width = _max_width(df)
    overlay_opts = LEGEND_OVERLAY_OPTS.copy()
    overlay_opts.update({"xlim": (-1, width), "frame_height": n * 40})
    overlay = hv.Overlay([points, *texts]).opts(**overlay_opts)
    return overlay


def _max_width(df):
    width = int(max(df["name"].map(len)) / 3)
    return width


def _legend_points(df):
    point_opts = LEGEND_POINT_OPTS.copy()
    min_y = df["y"].min() - 1
    max_y = df["y"].max() + 1
    point_opts.update(
        {"xlim": (-1, 1), "ylim": (min_y, max_y),}
    )
    points = hv.Points(df, kdims=["x", "y"], vdims=["name", "color"]).opts(**point_opts)
    return points


def _legend_texts(df):
    width = _max_width(df)
    text_opts = LEGEND_TEXT_OPTS.copy()
    text_opts.update({"xlim": (-1, width)})
    texts = []
    for _, r in df.iterrows():
        texts.append(hv.Text(r["x"] + 1, r["y"], r["name"]).opts(**text_opts))
    return texts


def group_legend(names=None, colors=None):
    if names is None:
        names = []
        colors = []
    names = [*list(metadata.GROUP_NAME_EN.values()), *names]
    colors = [*list(metadata.GROUP_COLOR.values()), *colors]
    return legend(names, colors)
