$(document).ready(function(){

    $("#productForm").submit(function(e){
        e.preventDefault();

        // Serialize form data
        let formData = $(this).serialize();

        // AJAX call to save product
        $.ajax({
            type: "POST",
            url: $('#create-product-button').data('url'),
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
