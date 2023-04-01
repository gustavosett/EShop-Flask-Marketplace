$(function () {
    $('.slider').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        infinite: true,
        arrows: true,
        autoplaySpeed: 600

    });

    $('.slider2').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        infinite: true,
        arrows: true,
        autoplaySpeed: 600

    });
    $('.news').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        vertical: true,
        arrows: false
    });

    $('.sidebar-menu i').click(function () {
        $(this).parents('.dropdown').find('.dropdown').not($(this).siblings('ul')).slideUp();
        $(this).siblings('ul').stop(true, true).slideToggle();
        $(this).toggleClass('active');
    });

    $('#btn-open-navbar, #btn-close-navbar, .overlay').click(function () {
        $('.overlay, .sidebar').toggleClass('active');
    });

   
    let table = document.querySelector('.tbody1');


    if (localStorage.getItem("basket") === null) {
        localStorage.setItem("basket", JSON.stringify([]))
    }


    let btnAdd = document.querySelectorAll('.btn-add');


    for (let btn of btnAdd) {
        btn.onclick = function (e) {
            e.preventDefault();

            if (JSON.parse(localStorage.getItem('basket')) === null) {
                localStorage.setItem('basket', JSON.stringify([]));
            }


            let basket = JSON.parse(localStorage.getItem("basket"));



            let id = this.getAttribute("data-id");
            let img = $(this).parents('.product').find('.img1').attr('src');
            let name = $(this).parents('.product').find('.prod-name').text();
            let existProd = basket.find(p => p.id == id);





            if (existProd === undefined) {
                basket.push({
                    id: id,
                    count: 1,
                    name: name,
                    image: img
                })
            }
            else {
                existProd.count += 1;
            }

            localStorage.setItem('basket', JSON.stringify(basket))
            // countBasket();
        }
    }

    // map,filter,reduce,forEach => High Order Functions

    function countBasket() {
        let basket = JSON.parse(localStorage.getItem('basket'));
        //document.getElementById('productCount').innerText = basket.reduce((x,y) => { return x+y.count},0)
        document.getElementById('productCount').innerText = basket.length
    }


    // countBasket();

    if (localStorage.getItem("basket") !== null) {
        let basket = JSON.parse(localStorage.getItem("basket"));
        createBasketItems();
    }

    function createBasketItems() {
        let basket = JSON.parse(localStorage.getItem("basket"));
        let table = document.querySelector('.tbody1');
        if (table) {
            for (let prod of basket) {
                table.innerHTML += `
            <tr data-index="${prod.id}">
            <td><img src="${prod.image}" alt=""></td>
            <td class="product-des product-name">
                <h6 class="mb-5"><a class="product-name" href="shop-product-right.html">${prod.name}</a></h6>
                <div class="product-rate">
                    <i class="fa-solid fa-star star"></i>
                    <i class="fa-solid fa-star star"></i>
                    <i class="fa-solid fa-star star"></i>
                    <i class="fa-solid fa-star star"></i>
                    <i class="fa-solid fa-star-half star"></i>
                    <span>(4.0)</span>
                </div>
            </td>
            <td>
                <h4>
                    $2.51
                </h4>
            </td>
            <td>
                <div class="detail-extra">
                    <div class="count">
                        <a href="" class="qty-down"><i class="fa-solid fa-angle-down"></i></a>
                        <span class="qty-val">1</span>
                        <a href="" class="qty-up"><i class="fa-solid fa-angle-up"></i></a>
                    </div>
                </div>
            </td>
            <td>
                <a class="text-body"><i class="fa-solid fa-trash-can remove-cart-item"></i></a>
            </td>
        </tr>    
            `
            }
        }


        $('.remove-cart-item').click(function (e) {
            e.preventDefault();
            let id = $(this).parents('tr').attr('data-index');
            if (localStorage.getItem("basket") !== null) {
                let basket = JSON.parse(localStorage.getItem("basket"));
                let index = basket.findIndex(b => b.id == id);
                basket.splice(index, 1);
                localStorage.setItem('basket', JSON.stringify(basket));
                table.innerHTML = "";
                createBasketItems();
            }
        });
    }
    $(document).ready(function(){
        $('div.tabmenu div').click(function(){
            var tab_id = $(this).attr('data-tab');
    
            $('div.tabmenu div').removeClass('current');
            $('.tab-content').removeClass('current');
    
            $(this).addClass('current');
            $("#"+tab_id).addClass('current');
        })
    
    })
});

// var headings = document.querySelectorAll(".tabmenu div")
// var contexts = document.querySelectorAll(".content div")
// for (var heading of headings) {
//     heading.addEventListener("click", function() {
//         var active = document.querySelector('.active');
//         active.classList.remove('active');
//         this.classList.add('active');

//         var id = this.getAttribute('data-id');

//         for (var context of contexts) {
//             if (context.getAttribute('data-id') == id) { context.classList.remove('d-none') } else(context.classList.add('d-none'))
//         }
//     })
// };
