$(document).ready(function(){

    $('#edit-product-button').on('click', function() {
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
        if(productId) {
            fetchGraphData(productId);
        }
    });

});