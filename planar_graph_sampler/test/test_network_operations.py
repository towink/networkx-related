from planar_graph_sampler.bijections.network_substitution import EdgeByNetworkSubstitution
from planar_graph_sampler.bijections.network_merge_in_series import NetworkMergeInSeries
from planar_graph_sampler.bijections.network_paralel_merge import NetworkMergeInParallel
from planar_graph_sampler.bijections.halfedge import  HalfEdge
from planar_graph_sampler.combinatorial_classes.network import NetworkClass
from planar_graph_sampler.combinatorial_classes.three_connected_graph import EdgeRootedThreeConnectedPlanarGraph

def test_edge_by_netwrok_substitution():
    '''
    Tests the edge by network substitution operation.
    :return:
    '''
    three_connected_graph = create_three_connected_graph()
    fifth = three_connected_graph.root_half_edge.next.opposite.next
    sixth = fifth.next
    seventh = fifth.opposite
    eighth = seventh.next

    network_edges_list = []
    network_vertices_list = []

    network_root_edge = HalfEdge()

    network_root_edge_opposite = HalfEdge()
    network_root_edge.opposite = network_root_edge_opposite
    network_root_edge_opposite.opposite = network_root_edge

    net_second = HalfEdge()
    net_second.prior = network_root_edge
    net_second.next = network_root_edge
    network_root_edge.next = net_second
    network_root_edge.prior = net_second
    network_edges_list.append(net_second)

    net_third = HalfEdge()
    net_second.opposite = net_third
    net_third.opposite = net_second
    network_vertices_list.append(net_third)

    net_fourth = HalfEdge()
    net_fourth.prior = net_third
    net_fourth.next = net_third
    net_third.next = net_fourth
    net_third.prior = net_fourth
    network_edges_list.append(net_fourth)

    net_fifth = HalfEdge()
    net_fifth.opposite = net_fourth
    net_fourth.opposite = net_fifth
    net_fifth.next = network_root_edge_opposite
    net_fifth.prior = network_root_edge_opposite
    network_root_edge_opposite.prior = net_fifth
    network_root_edge_opposite.next = net_fifth

    net_seventh = HalfEdge()
    net_seventh.prior = net_second
    net_second.next = net_seventh
    net_seventh.next = network_root_edge
    network_root_edge.prior = net_seventh
    network_edges_list.append(net_seventh)

    net_eighth = HalfEdge()
    net_eighth.opposite = net_seventh
    net_seventh.opposite = net_eighth
    network_vertices_list.append(net_eighth)

    net_nineth = HalfEdge()
    net_nineth.prior = net_eighth
    net_eighth.next = net_nineth
    net_nineth.next = net_eighth
    net_eighth.prior = net_nineth
    network_edges_list.append(net_nineth)

    net_tenth = HalfEdge()
    net_tenth.prior = network_root_edge_opposite
    network_root_edge_opposite.next = net_tenth
    net_tenth.next = net_fifth
    net_fifth.prior = net_tenth
    net_tenth.opposite = net_nineth
    net_nineth.opposite = net_tenth


    network = NetworkClass(network_vertices_list, network_edges_list, network_root_edge)

    edge_for_substitution = fifth
    EdgeByNetworkSubstitution().substitute_edge_by_network(three_connected_graph, edge_for_substitution, network)
    # Check vertices
    assert len(three_connected_graph.vertices_list) == 4

    # Check Edges
    assert len(three_connected_graph.edges_list) == 7
    # First node with zero pole merging
    assert fifth.opposite == net_third
    assert net_third.opposite == fifth
    assert sixth.prior == net_seventh
    assert net_seventh.next == sixth
    assert fifth.next == net_seventh
    assert net_seventh.prior == fifth

    # Second node with inf-pole merging
    assert seventh.opposite == net_nineth
    assert net_nineth.opposite == seventh
    assert eighth.prior == net_fifth
    assert net_fifth.next == eighth
    assert seventh.next == net_fifth
    assert net_fifth.prior == seventh

    # Check the node numbers updates
    half_edge_walker = edge_for_substitution.next
    assert edge_for_substitution.node_nr == 3
    while half_edge_walker != edge_for_substitution:
        assert half_edge_walker.node_nr == edge_for_substitution.node_nr
        half_edge_walker = half_edge_walker.next

    half_edge_walker = seventh.next
    assert seventh.node_nr == 4
    while half_edge_walker != seventh:
        assert half_edge_walker.node_nr == seventh.node_nr
        half_edge_walker = half_edge_walker.next


def create_three_connected_graph():
    first_net_vertices_list = []
    first_net_edges_list = []

    first_net_root_edge = HalfEdge()
    first_net_root_edge.node_nr = 1

    first_net_root_edge_opposite = HalfEdge()
    first_net_root_edge_opposite.node_nr = 2
    first_net_root_edge.opposite = first_net_root_edge_opposite
    first_net_root_edge_opposite.opposite = first_net_root_edge

    third = HalfEdge()
    third.node_nr = 1
    first_net_root_edge.next = third
    first_net_root_edge.prior = third
    third.prior = first_net_root_edge
    third.next = first_net_root_edge
    first_net_edges_list.append(third)

    fourth = HalfEdge()
    fourth.node_nr = 3
    third.opposite = fourth
    fourth.opposite = third
    first_net_vertices_list.append(fourth)

    fifth = HalfEdge()
    fifth.node_nr = 3
    fifth.prior = fourth
    fourth.next = fifth
    first_net_edges_list.append(fifth)

    sixth = HalfEdge()
    sixth.node_nr = 3
    sixth.next = fourth
    fourth.prior = sixth
    sixth.prior = fifth
    fifth.next = sixth
    first_net_edges_list.append(sixth)

    seventh = HalfEdge()
    seventh.node_nr = 4
    seventh.opposite = fifth
    fifth.opposite = seventh
    first_net_vertices_list.append(seventh)

    eighth = HalfEdge()
    eighth.node_nr = 4
    eighth.next = seventh
    eighth.prior = seventh
    seventh.next = eighth
    seventh.prior = eighth
    first_net_edges_list.append(eighth)

    ninth = HalfEdge()
    ninth.node_nr = 2
    ninth.opposite = eighth
    eighth.opposite = ninth
    ninth.next = first_net_root_edge_opposite
    first_net_root_edge_opposite.prior = ninth

    tenth = HalfEdge()
    tenth.node_nr = 2
    tenth.opposite = sixth
    sixth.opposite = tenth
    tenth.next = ninth
    ninth.prior = tenth
    tenth.prior = first_net_root_edge_opposite
    first_net_root_edge_opposite.next = tenth

    return EdgeRootedThreeConnectedPlanarGraph(first_net_vertices_list, first_net_edges_list, first_net_root_edge)


def create_sample_network():
    graph = create_three_connected_graph()
    return NetworkClass(graph.vertices_list, graph.edges_list, graph.root_half_edge)


def test_series_merge_of_networks():
    '''
    Tests the merging of two networks in series.
    :return:
    '''
    first_network = create_sample_network()
    first_net_inf_pole = first_network.root_half_edge.opposite

    second_network = create_sample_network()
    second_net_zero_pole = second_network.root_half_edge

    merged = NetworkMergeInSeries().merge_networks_in_series(first_network, second_network)
    # Check the root edge
    assert merged.root_half_edge == first_network.root_half_edge
    assert merged.root_half_edge.opposite == second_network.root_half_edge.opposite

    # Check the number of elements in vertices and edges list
    assert len(merged.vertices_list) == 5
    assert len(merged.edges_list) == 8

    # Check the the pointers
    assert first_net_inf_pole.next.prior == second_net_zero_pole.prior
    assert second_net_zero_pole.prior.next == first_net_inf_pole.next
    assert first_net_inf_pole.prior.next == second_net_zero_pole.next
    assert second_net_zero_pole.next.prior == first_net_inf_pole.prior

    # Check the node numbers of the merged edge
    expected_node_number = first_net_inf_pole.node_nr
    assert expected_node_number == 2
    half_edge_walker = first_net_inf_pole.prior.next
    assert first_net_inf_pole.prior.node_nr == expected_node_number
    while half_edge_walker != first_net_inf_pole.prior:
        assert half_edge_walker.node_nr == expected_node_number
        half_edge_walker = half_edge_walker.next



def test_parallel_merge_of_networks():
    '''
    Tests the merging of two networks in parallel.
    :return:
    '''
    first_network = create_sample_network()
    first_net_zero_pole = first_network.root_half_edge
    first_net_zero_pole_prior_old = first_net_zero_pole.prior
    first_net_inf_pole = first_net_zero_pole.opposite
    first_net_inf_pole_next_old = first_net_inf_pole.next

    second_network = create_sample_network()
    second_net_zero_pole = second_network.root_half_edge
    second_net_inf_pole = second_net_zero_pole.opposite
    # Change the node numbers for testing
    second_net_zero_pole.node_nr = -1
    second_net_zero_pole.next.node_nr = -1
    second_net_inf_pole.node_nr = -1
    second_net_inf_pole.next.node_nr = -1
    second_net_inf_pole.next.next.node_nr = -1

    result = NetworkMergeInParallel().merge_networks_in_parallel(first_network, second_network)

    # Check the sizes of the resulted network
    assert len(result.vertices_list) == 4
    assert len(result.edges_list) == 8

    # Check the pointers updates in the zero pole
    assert first_net_zero_pole.prior == second_net_zero_pole.prior
    assert second_net_zero_pole.prior.next == first_net_zero_pole
    assert first_net_zero_pole_prior_old.next == second_net_zero_pole.next
    assert second_net_zero_pole.next.prior == first_net_zero_pole_prior_old

    # Check the pointers updates in the inf pole
    assert first_net_inf_pole.next == second_net_inf_pole.next
    assert second_net_inf_pole.next.prior == first_net_inf_pole
    assert first_net_inf_pole_next_old.prior == second_net_inf_pole.prior
    assert second_net_inf_pole.prior.next == first_net_inf_pole_next_old

    # Check the node numbers update
    assert first_net_zero_pole.node_nr == 1
    half_edge_walker = first_net_zero_pole.next
    while half_edge_walker != first_net_zero_pole:
        assert half_edge_walker.node_nr == first_net_zero_pole.node_nr
        half_edge_walker = half_edge_walker.next

    assert first_net_inf_pole.node_nr == 2
    half_edge_walker = first_net_inf_pole.next
    while half_edge_walker != first_net_inf_pole:
        assert half_edge_walker.node_nr == first_net_inf_pole.node_nr
        half_edge_walker = half_edge_walker.next



if __name__ == "__main__":
    test_edge_by_netwrok_substitution()
    test_parallel_merge_of_networks()
    test_series_merge_of_networks()