$('#slider1, #slider2, #slider3, #slider4, #slider6').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 4,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


// cart product quantity increasing
$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    // console.log(id)

    var eml = this.parentNode.children[2]

    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },

        success: function (data) {
            // console.log(data)
            // console.log('Success')

            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        }  
    })
})


// cart product quantity decreasing
$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    // console.log(id)

    var eml = this.parentNode.children[2]

    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },

        success: function (data) {
            // console.log(data)
            // console.log('Success')

            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        }  
    })
})


// cart product remove
$('.removecart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this
    console.log(id)

    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },

        success: function (data) {
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }  
    })
})