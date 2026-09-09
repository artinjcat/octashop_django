$(document).on("click", "#add-cart", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: "/api/site/cart/add/",
    data: {
      product_id: $(this).val(),
      "qty-to-cart": $("#qty-to-cart").val(),
      csrfmiddlewaretoken: $(this).attr("csrf"),
      action: "post",
    },
    caches: false,
    success: function (json) {
      $("#cart-quantity").html(json.qty);

      const message = $(`
        <div class="fixed top-5 right-5 z-50 p-4 text-sm text-fg-success-strong rounded-base bg-green-100 shadow-lg"
             role="alert">
            <span class="font-medium bg-green-500 text-white rounded-base px-3 py-1" >
                محصول با موفقیت به سبد خرید اضافه شد
            </span>
        </div>
    `);

      $("body").append(message);

      setTimeout(function () {
        message.fadeOut(300, function () {
          $(this).remove();
        });
      }, 2500);
    },
    error: function (xhr, errmsg, err) {},
  });
});
