document.addEventListener("DOMContentLoaded", function() {
    let cy = cytoscape({
        container: document.getElementById('graphArea'), // container to render in

        style: [ // the stylesheet for the graph
            {
                selector: 'node',
                style: {
                    'background-color': '#666',
                    'label': 'data(id)'
                }
            },

            {
                selector: 'edge',
                style: {
                    'width': 3,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            }
        ],
    });

    // Event listener to add a node
    document.getElementById("nodeForm").addEventListener("submit", function(e) {
        e.preventDefault();
        
        let nodeType = e.target.elements["node_type"].value;
        let nodeName = e.target.elements["node_name"].value;
        
        cy.add({
            group: 'nodes',
            data: { id: nodeName },
            position: { x: 200, y: 200 }  // You might want a method to place nodes at different positions
        });
    });

    // Event listener to add an edge
    document.getElementById("edgeForm").addEventListener("submit", function(e) {
        e.preventDefault();
        
        let prevNode = e.target.elements["prev_node"].value;
        let nextNode = e.target.elements["next_node"].value;
        
        cy.add({
            group: 'edges',
            data: { id: prevNode + "-" + nextNode, source: prevNode, target: nextNode }
        });
    });

    document.getElementById("clearGraph").addEventListener("click", function() {
        cy.elements().remove();
    });

    document.getElementById("saveGraph").addEventListener("click", function() {
        let data = cy.json();  // Convert graph to a save-able format
        // Use AJAX to send the data to the server for saving
    });
});
