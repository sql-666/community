/**
 * Created by 10840 on 2020/4/14.
 */


//跳转到商品详情页
$(".pro").on("click", function() {
    var pro_id=$(this).children('p.pro').text()
    window.location.href = "http://127.0.0.1:8000/myapp/productD?pro_id="+pro_id;;
});
