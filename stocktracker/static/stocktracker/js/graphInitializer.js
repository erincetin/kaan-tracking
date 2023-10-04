function fetchGraphData(productId) {
    $.ajax({
        url: $('#edit-product-section').data('fetch-url'), // You'll need a new Django view for this
        type: 'GET',
        data: {product_id: productId},
        success: function(response) {
            if(response.status === 'success') {
                // Assuming response.data contains nodes and edges for the graph
                let nodes = response.data.nodes;
                let edges = response.data.edges;

                let cy = cytoscape({
                    container: document.getElementById('cy'), // container where the graph will be rendered

                    elements: {
                        nodes: nodes.map(node => ({
                            data: {
                                id: node.node_id,
                                label: node.node_name,
                                description: node.node_desc
                            }
                        })),
                        edges: edges.map(edge => ({
                            data: {
                                id: edge.edge_id,
                                source: edge.prev_node,
                                target: edge.next_node,
                                label: edge.operation_description
                            }
                        }))
                    },

                    style: [ // You can customize the graph appearance here
                        {
                            selector: 'node',
                            style: {
                                'background-color': '#666',
                                'label': 'data(label)'
                            }
                        },
                        {
                            selector: 'edge',
                            style: {
                                'width': 3,
                                'line-color': '#ccc',
                                'target-arrow-color': '#ccc',
                                'target-arrow-shape': 'triangle',
                                'label': 'data(label)'
                            }
                        }
                    ],

                    layout: {
                        name: 'grid',
                        rows: 1
                    }
                });

            } else {
                alert('Failed to fetch graph data.');
            }
        }
    });
}