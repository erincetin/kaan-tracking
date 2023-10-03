function populateProductDropdown() {
    $.ajax({
        url: '{% url "stocktracker:fetch_products" %}',
        type: 'GET',
        success: function(response) {
            if(response.status === 'success') {
                let products = response.products;
                for(let product of products) {
                    $('#product-list').append(
                        `<option value="${product.produt_id}">${product.name} (${product.code})</option>`
                    );
                }
            }
        }
    });
}

$(document).ready(function(){
    
    populateProductDropdown();

    $("#productForm").submit(function(e){
        e.preventDefault();

        // Serialize form data
        let formData = $(this).serialize();

        // AJAX call to save product
        $.ajax({
            type: "POST",
            url: "{% url 'stocktracker:create_new_product' %}",
            data: formData,
            success: function(response){
                if(response.status === 'success'){
                    alert(response.message);
                    
                    $('#current-product').html(
                        `<strong>Product:</strong> ${response.product_name} - <strong>Code:</strong> ${response.product_code}`
                    );
                    $("#productForm").hide();
                }
                else {
                    alert('Failed to save product. Please try again.');
                }
            },
            error: function(){
                alert('There was an error. Please try again later.');
            }
        });
    });    
});
