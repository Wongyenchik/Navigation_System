console.log("hallo");
$(document).ready(function (){    
    $(".update-checkbox").on("click", function() {
        // Check if any checkbox is checked
        let filter_object = {}
        let stock_num = {}
        var confirmation = confirm("Are you sure you want to update the stock?");
    
        // If the user confirms, proceed with updating the stock
        if (confirmation) {
            // If at least one checkbox is checked, change the text of the add button to update button
            $(".update-box").each(function(){
                let filter_value = $(this).val()
                let filter_key = $(this).data("filter") 

                console.log("Filter value is: ",filter_value);
                console.log("Filter key is: ",filter_key);

                filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key + ']')).map(function(element){
                    return element.value
                })
            })
            $(".qty-input").each(function(){
                let filter_value = $(this).val()
                let filter_key = $(this).data("filter") 

                console.log("Filter value is: ",filter_value);
                console.log("Filter key is: ",filter_key);

                stock_num[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key + ']')).map(function(element){
                    return element.value
                })
            })

            console.log("Filter object", filter_object);
            console.log("stock_num", stock_num);

            $.ajax({
                url: '/update-stock',
                data: {
                    product: filter_object.product,  
                    stock: stock_num.stock,          
                },
                dataType: 'json',
                beforeSend: function(){
                    console.log("Sending Data...");
                },
                success: function(response){
                    console.log(response);
                    console.log("Sent data");
                    location.reload();
                }
            });
        } else {
            // If the user cancels, display an alert
            alert("Update canceled.");
        }
    });
});

$(document).ready(function (){    
    //Add to picking list
    $(".add-to-pick-btn").on("click", function(){
        let this_val = $(this)
        let index = this_val.attr("data-index")
        console.log(index)
        let name = $(".product-name-" + index).val()
        console.log(name)
        let stock = $(".product-stock-" + index).val()
        console.log(stock)
        let category = $(".product-category-" + index).val()
        console.log(category)
        let location = $(".product-location-" + index).val()
        console.log(location)
        let image = $(".product-image-" + index).val()
        console.log(image)


        $.ajax({
            url: '/add-to-pick',
            data: {
                'id': index,
                'name': name,
                'stock':stock,
                'category':category,
                'location':location,
                'image':image
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding product to cart");
            },
            success: function(response){
                this_val.html("✅")
                console.log("Added product to cart");
                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    })
    $(".delete-product").on("click", function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let id = $(".prod-id-" + product_id)
        let name = $(".prod-name-" + product_id)
        let stock = $(".prod-stock-" + product_id)

        console.log("Product ID: ", product_id);
        var confirmation = confirm("Are you sure to remove this picking item?");
        if (confirmation) {

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id" : product_id,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
                id.hide()
                name.hide()
                stock.hide()
            },
            success: function(response){
                console.log(response)
                if (response.totalcartitems === 0) {
                    window.location.href = "../"; // Redirect to homepage
                }else{
                    location.reload()
                }
            }
        })
    }
    })
    $(".create-list").on("click", function(){
        $.ajax({
            url: "/product-list",
            success: function(response){
                console.log(response)
            }
        })
    })
    $(".exit-navigation").on("click", function() {
        var confirmation = confirm("Are you sure you want to exit the navigation?");
        if (confirmation) {

        $.ajax({
            url: "/clear-session/",
            type: "GET",
            dataType: "json",
            success: function(response) {
                console.log(response.message);
                // Redirect to the homepage after clearing the session
                window.location.href = "../";
            },
            error: function(xhr, status, error) {
                // console.error("Error clearing session:", error);
            }
        });
    } 
    });
    $(".navigation-pick").on("click", function(){
        let product_id = $(".delete-product").attr("data-product"); // Get data-product from the delete-product button

        console.log("Product ID: ", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id" : product_id,
            },
            dataType: "json",
            beforeSend: function(){
     
            },
            success: function(response){
                console.log(response)
                    window.location.href = "/navigation-pick/"+ product_id; // Redirect to homepage
                    // click="window.location.href = '/navigation';" 
            }
        })
    })
    $(".depart-button").on("click", function(){
        let this_val = $(this)
        let index = this_val.attr("data-index")
        console.log(index)

        $.ajax({
            url: '/depart',
            data: {
                'depart': index,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Departing");
            },
            success: function(response){
                console.log("Reached");
            }
        })
    })
    $(".picking-button").on("click", function(){
        let qty_pick = $(".qty-input-picking").val()
        console.log(qty_pick)
        let product_pick = $(".picking-product").val()

        $.ajax({
            url: '/item-pick',
            data: {
                'pickingqty': qty_pick,
                'pickproduct':product_pick,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding product to cart");
            },
            success: function(response){
                console.log("Added product to cart");
                // $(".cart-items-count").text(response.totalcartitems)
                if (response.message) {
                    $(".error-message1").show();
                } else {
                    $(".error-message1").hide(); // Hide error message if no error
                    window.location.href = '/navigation';
                }
            }
        })
    })
    $(".picking-button1").on("click", function(){
        let qty_pick = $(".qty-input-picking").val()
        console.log(qty_pick)
        let product_pick = $(".picking-product").val()

        $.ajax({
            url: '/item-pick-scan',
            data: {
                'pickingqty': qty_pick,
                'pickproduct':product_pick,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding product to cart");
            },
            success: function(response){
                console.log("Added product to cart");
                // $(".cart-items-count").text(response.totalcartitems)
                if (response.message) {
                    $(".error-message1").show();
                } else {
                    $(".error-message1").hide(); // Hide error message if no error
                    window.location.href = '../';
                }
            }
        })
    })
    $(".update-detail-button").on("click", function(){
        let product_id_main = $(".product-id-main").val()
        let product_id = $(".product-id").val()
        let product_name = $(".product-name").val()
        let update_stock = $(".update-stock").val()
        let product_category = $(".product-category").val();
        $.ajax({
            url: '/update-detail-done',
            data: {
                'product-id-main':product_id_main,
                'product_id': product_id,
                'product_name':product_name,
                'update_stock':update_stock,
                'product_category':product_category,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding product to cart");
            },
            success: function(response){
                console.log("hahaha");
                window.location.href = "../";

            }
        })
    })
    $(".add-to-pick-list-btn").on("click", function(){
        var container = $(this).closest('.product-container'); // Find the closest container
        var itemsArray = [];
    
        // Iterate through each item within the container
        container.find(".item-id").each(function(index) {
            var id = $(this).val();
            var name = container.find(".item-name").eq(index).val();
            var stock = container.find(".stock").eq(index).val();
            var category = container.find(".category").eq(index).val();
            var location = container.find(".location").eq(index).val();
            var image = container.find(".image").eq(index).val();

            console.log(location)
    
            var itemDetails = {
                'id': id,
                'name': name,
                'stock': stock,
                'category':category,
                'location':location,
                'image':image,
            };
            itemsArray.push(itemDetails);
        });
        $.ajax({
            url: '/add-to-pick-list',
            data: {
                'itemsArray': JSON.stringify(itemsArray),
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding product to cart");
            },
            success: function(response){
                console.log("Added product to cart");
                $(".cart-items-count").text(response.totalcartitems)

            }
        })
    });
});

function confirmCancel() {
    var confirmation = confirm("Are you confirm to cancel pickup?");
    if (confirmation) {
        window.location.href = '/navigation';
    }
}

