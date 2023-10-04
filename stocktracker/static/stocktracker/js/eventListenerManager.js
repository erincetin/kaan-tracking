function populateProductDropdown() {

    $.ajax({
        url: $('#edit-product-button').data('url'),
        type: 'GET',
        success: function(response) {
            if(response.status === 'success') {
                let products = response.products;
                for(let product of products) {
                    $('#product-list').append(
                        `<option value="${product.id}">${product.name} (${product.code})</option>`
                    );
                }
            }
        }
    });
}

$(document).ready(function(){

    $('#edit-product-button').on('click', function() {
        populateProductDropdown();
        $('#edit-product-section').show();
        $('#create-product-section').hide();
    });

    $('#create-product-button').on('click', function() {
        $('#create-product-section').show();
        $('#edit-product-section').hide();
        $("#productForm")[0].reset();
        $('#current-product').html('');
        $("#productForm").show();
    });
    
    $('#product-list').change(function() {
        let productId = $(this).val();
        console.log(productId)
        if(productId) {
            fetchGraphData(productId);
        }
    });
    

});