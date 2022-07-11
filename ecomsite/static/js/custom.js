$(document).ready(function () {
    $('.increment-btn').click(function (e) {
        e.preventDefault();

        var increment_value = $(this).closest('.product-data').find('.qty-input').val()
        var value = parseInt(increment_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value<10)
        {
            value++;
            $(this).closest('.product-data').find('.qty-input').val(value);
        }


    });

    $('.decrement-btn').click(function (e) {
        e.preventDefault();

        var decrement_value = $(this).closest('.product-data').find('.qty-input').val()
        var value = parseInt(decrement_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1)
        {
            value--;
            $(this).closest('.product-data').find('.qty-input').val(value);
        }


    });

    $('.addtocartbtn').click(function (e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id' : product_id,
                'product_qty' :product_qty,
                csrfmiddlewaretoken : token
            },
            
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                
            }
        });
    });

    $('.changequantity').click(function (e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product-data').find('.prod_id').val();
        var product_qty = $(this).closest('.product-data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id' : product_id,
                'product_qty' :product_qty,
                csrfmiddlewaretoken : token
            },
            
            success: function (response) {
                // console.log(response)
                alertify.success(response.status)
                
            }
        });
    });

    $('.delete-cart-item').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product-data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-cart-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },

            success: function (response) {
                // console.log(response)
                alertify.success(response.status)
                $('.cartdata').load(location.href + " .cartdata");

            }
        });
    });

    $('.addtowishlist').click(function (e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id' : product_id,
                csrfmiddlewaretoken : token
            },
            
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                
            }
        });
    });

    // $('.delete-wishlist-item').click(function (e) {
    //     e.preventDefault();

    //     var product_id = $(this).closest('.product-data').find('.prod_id').val();
    //     var token = $('input[name=csrfmiddlewaretoken]').val();

    //     $.ajax({
    //         method: "POST",
    //         url: "/delete-wishlist-item",
    //         data: {
    //             'product_id': product_id,
    //             csrfmiddlewaretoken: token
    //         },

    //         success: function (response) {
    //             // console.log(response)
    //             alertify.success(response.status)
    //             $('.wishlistdata').load(location.href + " .wishlistdata");

    //         }
    //     });
    // });

    $(document).on('click','.delete-wishlist-item',function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product-data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-wishlist-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },

            success: function (response) {
                // console.log(response)
                alertify.success(response.status)
                $('.wishlistdata').load(location.href + " .wishlistdata");

            }
        });
    });


    // jquery code for razorpay

    $('.paywithrazorpaybtn').click(function (e) { 
        e.preventDefault();

        var fname = $("[name='fname']").val();
        var lname = $("[name='lname']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();
        
        if(fname == "" || lname == ""|| email == "" || phone == ""||address == "" || city == "" ||state == "" || country == "" || pincode =="" )
        {
            swal("Alert!!!", "All fields are mandatory..", "error");
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    console.log(response)

                    var options = {
                            "key": "rzp_test_UH4U13m0p716p8", // Enter the Key ID generated from the Dashboard
                            "amount":1*100, //response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                            "currency": "INR",
                            "name": "sham ambhore",
                            "description": "Thank you",
                            "image": "https://example.com/your_logo",
                            // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                            "handler": function (responseb){
                                alert(responseb.razorpay_payment_id);
                                data ={
                                'fname':fname,
                                'lname': lname,
                                'email': email,
                                'phone': phone,
                                'address':address,
                                'city':city,
                                'state':state,
                                'country':country,
                                'pincode': pincode,
                                'payment_mode':'Razorpay payment',
                                'payment_id': responseb.razorpay_payment_id,
                                csrfmiddlewaretoken : token,

                                }
                                $.ajax({
                                    method: "POST",
                                    url: "/place-order",
                                    data: data,
                                    dataType: "dataType",
                                    success: function (responsec) {
                                        swal('congratulations!!!', responsec.status, 'success').then((value) =>{
                                            window.location.href = '/my-orders';

                                        });
                                        
                                    }
                                });
                                
                            },
                            "prefill": {
                                "name": fname + " " + lname,
                                "email": email,
                                "contact": phone
                            },
                            
                            "theme": {
                                "color": "#3399cc"
                            }
                        };
                        var rzp1 = new Razorpay(options);
                        rzp1.open();
                    }
                    
                
            });

           

    }
        
    });
});