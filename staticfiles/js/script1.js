window.addEventListener("load", function(evt) {

    $('.category_select').on("change", (e)=>{
        $(document).on('change', '.category_select', (e) => {
            let t_href = e.target;

            $.ajax({
                url: '/prod_list/?category_id=' + t_href.value,
                success: function(data){
                    if (data){
                        $(".products_list").html(data)
                    }
                },
            });
            e.preventDefault();
        });
    });
    // поиск товара по наименованию
    $('.product_search').on("input","input[type='text']", (e)=>{
        $(document).on('input', '.product_search', (e) => {
            let t_href = e.target;

            $.ajax({
                url: '/prod_list/?prod_name=' + t_href.value,
                success: function(data){
                    if (data){
                        $(".products_list").html(data)
                    }
                },
            });
            e.preventDefault();
        });
    });
});










