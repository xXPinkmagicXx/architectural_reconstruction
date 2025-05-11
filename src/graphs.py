import networkx as nx
import constants as c
import utils
from processing import read_line, get_project_from_using, ignore_using, read_full_line
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import processing
import matplotlib.colors as mcolors

def create_digraph_all()->nx.DiGraph:
    G = nx.DiGraph()
    with open(c.USINGS_TXT_FILE_PATH, 'r') as f:
        while True:
            line = f.readline()
            if line == "" or line == "\n":
                print("End of file reached")
                break
            _, namespace, usings = read_line(line)

            project = get_project_from_using(namespace)

            if project is None:
                continue
            
            if project not in list(G.nodes):
                G.add_node(project)

            for using in usings:
                if ignore_using(using):
                    continue # Ignore this using and continue to the next one
                using_to_project = get_project_from_using(using)
                if using_to_project is None:
                    # print(f"Error for namespace '{namespace}' returned project: {using_to_project}")
                    continue
                # Add edge
                if G.has_edge(project, using_to_project):
                    G[project][using_to_project]['weight'] += 1
                else:
                    # print(f"Added Edge: {project} -> {using_to_project}")
                    G.add_edge(project, using_to_project, weight=1)
    return G

def do_abstraction_of_using(using: str, abstraction_level: int) -> str:
    splitted = using.split(".")
    if len(splitted) >= abstraction_level:
        return ".".join(splitted[:abstraction_level])
    return ".".join(splitted[:2])

def create_digraph_project(project_name: str, abstraction_level: int = None, ignore_circular_dep: bool = False) -> nx.DiGraph:
    G = nx.DiGraph()
    with open(c.USINGS_TXT_FILE_PATH, 'r') as f:
        all_lines = f.readlines()
    
    for line in all_lines:
        if line == "" or line == "\n":
            print("End of file reached")
            break
        _, namespace, usings = read_line(line)

        
        project = get_project_from_using(namespace)
        # If the project cannot be found, skip it this line
        if project is None:
            continue

        # Only process the project we are interested in
        if project != project_name: 
            continue
        
        # Add the project as node if it does not exist
        if project not in list(G.nodes):
            G.add_node(project)

        for using in usings:
            if ignore_using(using):
                continue # Ignore this using and continue to the next one
            
            if ignore_circular_dep:
                using_project = get_project_from_using(using)
                if using_project is not None and using_project == project:
                    continue # To ignore circular dependencies

            # Do abstraction of using
            if abstraction_level is not None:
                using = do_abstraction_of_using(using, abstraction_level)

            # Add edge
            if G.has_edge(project, using):
                G[project][using]['weight'] += 1
            else:
                G.add_edge(project, using, weight=1)

    return G

def create_digraph_namspace(project_name: str, abstraction_level: int = None, ignore_circular_dep: bool = False) -> nx.DiGraph:
    G = nx.DiGraph()
    with open(c.USINGS_TXT_FILE_PATH, 'r') as f:
        all_lines = f.readlines()
    
    for line in all_lines:
        if line == "" or line == "\n":
            print("End of file reached")
            break
        _, namespace, usings = read_line(line)

        
        project = get_project_from_using(namespace)
        # If the project cannot be found, skip it this line
        if project is None or project != project_name:
            continue
        
        # Add the project as node if it does not exist
        if namespace not in list(G.nodes):
            G.add_node(project)

        for using in usings:
            if ignore_using(using):
                continue # Ignore this using and continue to the next one
            
            if ignore_circular_dep:
                using_project = get_project_from_using(using)
                if using_project is not None and using_project == project:
                    continue # To ignore circular dependencies

            # Do abstraction of using
            if abstraction_level is not None:
                using = do_abstraction_of_using(using, abstraction_level)

            # Add edge
            if G.has_edge(namespace, using):
                G[namespace][using]['weight'] += 1
            else:
                G.add_edge(namespace, using, weight=1)

    return G

def draw_graph(G: nx.DiGraph, pos, node_size: int = 2000, with_labels: bool = False) -> None:
    plt.figure(figsize=(20, 20))
    nx.draw(
    G,
    pos,
    node_size=node_size,
    with_labels=with_labels,
    node_color="lightblue",
    font_size=6,
    font_color="black",
    arrows=True)
    
    if with_labels:
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)


def create_dependicy_graph_namespaces()->nx.DiGraph:
    G = nx.DiGraph()
    with open(c.USINGS_TXT_FILE_PATH, 'r') as f:
        while True:
            line = f.readline()
            if line == "" or line == "\n":
                print("End of file reached")
                break
            _, namespace, usings = read_line(line)

            for using in usings:
                if ignore_using(using):
                    continue # Ignore this using and continue to the next one
                # Add edge
                G.add_edge(namespace, using)
    return G


def create_model_view(project_name: str, depth: int = None):
    G = nx.DiGraph()
    with open(c.USINGS_TXT_FILE_PATH, 'r') as f:
        all_lines = f.readlines()
    
    G.add_node(project_name, count=1)

    for line in all_lines:
        if line == "" or line == "\n":
            print("End of file reached")
            break
        devops_file_path, namespace, _ = read_line(line)

        ## Only look at namespaces that are in the project
        project_for_namespace = get_project_from_using(namespace)
        
        if project_for_namespace != project_name:
            continue 


        abstracted_one = utils.abstract(namespace)
        # Add node or increment count
        # Add edge to project if namespace is not the project name
        if abstracted_one == project_name:
            G.add_edge(namespace, project_name)        
        
        G.add_edge(namespace, abstracted_one)

    return G

# make graph the point to the namespace
def create_digraph_files_to_namespace(project_name: str):
    G = nx.DiGraph()
    with open(c.USINGS_TXT_FILE_PATH, 'r') as f:
        all_lines = f.readlines()
    
    for line in all_lines:
        if line == "" or line == "\n":
            print("End of file reached")
            break
        
        devops_file_path, namespace, usings, n_lines = read_full_line(line)

        ## Only look at namespaces that are in the project
        project_for_namespace = get_project_from_using(namespace)
        
        if project_for_namespace != project_name:
            continue 


        # Add node or increment count
        # Add edge to project if namespace is not the project name
        file_path = utils.get_file_path_from_devops_url(devops_file_path)
        if not G.has_node(file_path):
            G.add_node(file_path, type="file", lines=n_lines)
        if not G.has_node(namespace):
            G.add_node(namespace, type="namespace")
        
        G.add_edge(namespace, file_path)

        for using in usings:
            if using == "" or using == "\n":
                continue
            if ignore_using(using):
                continue
            
            if not G.has_node(using):
                G.add_node(using, type="namespace")

            G.add_edge(file_path, using)
    return G



def create_dependicy_graph_file_names()->nx.DiGraph:
    G = nx.DiGraph()
    with open(c.USINGS_TXT_FILE_PATH, 'r') as f:
        while True:
            line = f.readline()
            if line == "" or line == "\n":
                print("End of file reached")
                break
            devops_path, namespace, usings = read_line(line)
            file_path = utils.get_file_path_from_devops_url(devops_path)

            for using in usings:
                if ignore_using(using):
                    continue # Ignore this using and continue to the next one
                # Add edge
                G.add_edge(file_path, using)
    return G

def get_file_nodes(G: nx.DiGraph) -> list[str]:
    return [node for node, attr in G.nodes(data=True) if attr['type'] == "file"]

def get_namespace_nodes(G: nx.DiGraph) -> list[str]:
    return [node for node, attr in G.nodes(data=True) if attr['type'] == "namespace"]

def get_in_degrees(G: nx.DiGraph, nodes: list[str]) -> list[int]:
    return [G.in_degree(node) for node in nodes]

def get_in_degrees_as_dict(G: nx.DiGraph, nodes: list[str]) -> dict[str, int]:
    return {node: G.in_degree(node) for node in nodes}

def get_out_degrees_as_dict(G: nx.DiGraph, nodes: list[str]) -> dict[str, int]:
    return {node: G.out_degree(node) for node in nodes}

def get_out_degrees(G: nx.DiGraph, nodes: list[str]) -> list[int]:
    return [G.out_degree(node) for node in nodes]

def get_file_sizes(G: nx.DiGraph) -> list[int]:
    return [attr['lines'] for _, attr in G.nodes(data=True) if attr['type'] == "file"]


def has_any_in_degree(G: nx.DiGraph, node: str) -> bool:
    return G.in_degree(node) > 0

def draw_critcal_files_graph(G = None, n_critical_files: int = 10, with_labels = False) -> tuple[nx.DiGraph]:

    cmap = cm.RdYlGn_r  # Reverse colormap to go from green to red
    plt.figure(figsize=(20, 20))

    # Create the graph
    if G is None:
        G = create_digraph_files_to_namespace(c.PROJECT_NAME_INCOME_BASE)

    # Separate nodes by type
    namespace_nodes = get_namespace_nodes(G)
    file_nodes = get_file_nodes(G)
    # Get the in-degree and out-degree values for the nodes
        
    # Get the in-degree and out-degree values for the nodes
    data_out_degree_filenames = get_out_degrees(G, file_nodes)
    data_in_degree_namespace_dict = get_in_degrees_as_dict(G, namespace_nodes)
    data_file_sizes = get_file_sizes(G)

    normalizer_file_sizes = processing.create_normalizer(data_file_sizes)
    normalizer_file_out_degrees = processing.create_normalizer(data_out_degree_filenames)

    norm_file_sizes = [processing.use_normalizer(normalizer_file_sizes, value) for value in data_file_sizes]
    norm_file_out_degrees = [processing.use_normalizer(normalizer_file_out_degrees, value) for value in data_out_degree_filenames]

    # Normalize the bin counts for the colormap
    
    # node_colors_filenames = [cmap(value) for value in norm_file_out_degrees]
    
    # Combine the file node metrics into a single value for sorting
    comb = [(size + out_degree)/2 for size, out_degree in zip(norm_file_sizes, norm_file_out_degrees)]

    # Add as attributes to the graph
    i = 0
    for node, attr in G.nodes(data=True): 
        if attr["type"] == c.NAMESPACE:
            continue
        attr["combined"] = comb[i]
        i += 1

        
    file_nodes.sort(key=lambda x: G.nodes[x]["combined"], reverse=True)
    top_critical_nodes = file_nodes[:n_critical_files]
    # Remove all nodes that are not in the top critical nodes
    for node in file_nodes:
        if node not in top_critical_nodes:
            G.remove_node(node)


    top_nodes_comb = [G.nodes[node]["combined"] for node in top_critical_nodes]
    comb_file_colors = [cmap(value) for value in top_nodes_comb]
    top_file_sizes = get_file_sizes(G)
    
    # Create default normalizer with mean 0.5 max 1.0 and min 0.0
    normalizer_comb = mcolors.Normalize(vmin=0, vmax=1.0, clip=True)

    top_namespace_nodes = get_namespace_nodes(G)
    top_namespace_nodes_with_in_degree = [node for node in top_namespace_nodes if has_any_in_degree(G, node)]

    # top_in_degree_namespace = get_in_degrees(G, top_namespace_nodes)
    node_sizes_namespace = [max(data_in_degree_namespace_dict[value] * 20, 50) for value  in top_namespace_nodes_with_in_degree]

    # Define positions for the graph
    pos = nx.spring_layout(G, k=1.3, iterations=30, threshold=0.01)

    # Draw file nodes as circles
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=top_critical_nodes,
        node_shape="o",
        node_color=comb_file_colors,
        node_size=top_file_sizes)

    # # Draw namespace nodes as squares
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=top_namespace_nodes_with_in_degree,
        node_shape="s",
        # node_color=node_colors_namespace,
        node_size=node_sizes_namespace)


    # # Draw edges
    nx.draw_networkx_edges(
        G,
        pos,
        alpha=0.5,
        arrows=True)

    # plt.title(f"Dependency graph for critical files in {c.PROJECT_NAME_INCOME_BASE}")

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # # add legned for the nodes
    # # Add a colorbar
    # sm.set_array(data_out_degree_filenames)
    # plt.colorbar(sm, label="Node Value")
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=normalizer_comb)
    sm.set_array([0,1])  # Set the data for the color map
    cbar = plt.colorbar(sm, ax=ax, label="Combined Metric", shrink=0.2)

    if with_labels:

        file_labels = {node: get_label(node, attr) for node, attr in G.nodes(data=True) if attr['type'] == "file"}
        namespace_labels = {node: get_label(node, attr) if G.in_degree(node) > 2 else '' for node, attr in G.nodes(data=True) if attr['type'] == "namespace"}
        
        combined_labels = {**file_labels, **namespace_labels}
        nx.draw_networkx_labels(G, pos, labels=combined_labels, font_size=10)

    return G


def draw_problem_graph(G = None, as_barpartite = False, with_labels = False) -> tuple[nx.DiGraph]:

    cmap = cm.RdYlGn_r  # Reverse colormap to go from green to red
    plt.figure(figsize=(20, 20))

    # Create the graph
    if G is None:
        G = create_digraph_files_to_namespace(c.PROJECT_NAME_INCOME_BASE)

    # Separate nodes by type
    namespace_nodes = [node for node, attr in G.nodes(data=True) if attr['type'] == "namespace"]
    file_nodes = [node for node, attr in G.nodes(data=True) if attr['type'] == "file"]

    # Get the in-degree and out-degree values for the nodes
    
        
    # Get the in-degree and out-degree values for the nodes
    # Normalize the bin counts for the colormap
    data_out_degree_filenames, norm_filenames, data_in_degree_namespace, norm_namespace = processing.get_normalized(G)

    node_sizes_namespace = [value * 100 for value  in data_in_degree_namespace]
    node_colors_filenames = [cmap(norm_filenames(value)) for value in data_out_degree_filenames]

    node_sizes_files = [attr['lines'] for _, attr in G.nodes(data=True) if attr['type'] == "file"]
    
    # Define positions for the graph
    if as_barpartite:
        pos = nx.bipartite_layout(G, nodes=file_nodes)  # positions for all nodes
    else:
        pos = nx.spring_layout(G, k=0.8, iterations=30)
    
    # Draw file nodes as circles
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=file_nodes,
        node_shape="o",
        node_color=node_colors_filenames,
        node_size=node_sizes_files)

    # Draw namespace nodes as squares
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=namespace_nodes,
        node_shape="s",
        # node_color=node_colors_namespace,
        node_size=node_sizes_namespace)


    # Draw edges
    nx.draw_networkx_edges(
        G,
        pos,
        alpha=0.5,
        arrows=True)

   

    plt.title(f"Dependency graph for critical files in {c.PROJECT_NAME_INCOME_BASE}")

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # add legned for the nodes
    # Add a colorbar
    # sm.set_array(data_out_degree_filenames)
    # plt.colorbar(sm, label="Node Value")
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_filenames)
    sm.set_array(data_out_degree_filenames)  # Set the data for the color map
    cbar = plt.colorbar(sm, ax=ax, label="Out-Degree", shrink=0.2)

    if with_labels:

        labels = {node: get_label(node, attr) for node, attr in G.nodes(data=True)}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

    return G

def get_label(node, attr) -> str:
    if attr['type'] == "namespace":
        return node
    _, class_name = processing.get_class_name(node)
    return class_name
