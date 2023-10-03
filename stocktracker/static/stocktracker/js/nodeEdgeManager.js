$(document).ready(function(){

    $("#nodeForm").submit(function(e){
        e.preventDefault();

        let formData = $(this).serialize();

        $.ajax({
            type: "POST",
            url: "{% url 'stocktracker:create_new_product' %}",
            data: formData,
            success: function(response){
                if(response.status === 'success'){
                    alert(response.message);
                    
                    // Add node to graph using Cytoscape.js
                    let newNode = {
                        group: 'nodes',
                        data: {
                            id: response.node_id, // Assuming you send back the node's id from your server
                            name: response.node_name
                            // Add any other data attributes you need
                        }
                    };
                    cy.add(newNode);
                }
                else {
                    alert('Failed to save node. Please try again.');
                }
            },
            error: function(){
                alert('There was an error. Please try again later.');
            }
        });
    });

    $("#edgeForm").submit(function(e){
        e.preventDefault();

        let formData = $(this).serialize();

        $.ajax({
            type: "POST",
            url: "{% url 'stocktracker:create_new_product' %}",
            data: formData,
            success: function(response){
                if(response.status === 'success'){
                    alert(response.message);

                    let newEdge = {
                    group: 'edges',
                    data: {
                        id: response.edge_id,
                        source: response.source_node_id,
                        target: response.target_node_id,
                        label: response.edge_label,
                        //... other edge properties
                        }
                    };
                    cy.add(newEdge);
                }
                else {
                    alert('Failed to save node. Please try again.');
                }
            },
            error: function(){
                alert('There was an error. Please try again later.');
            }
        });
    });


});