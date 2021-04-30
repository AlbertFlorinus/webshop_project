$(function() {
  updateCart();
  $("#placeOrder").submit(function( event ) {
    $("#order_items").val(Cookies.get("cart"));
  });
});

function updateCart() {
  var items = Cookies.getJSON('cart');
  if (typeof items == 'undefined')
    return;
  $('.cart_size').html(items.length);
  for (item in jQuery.uniqueSort(items)) {
    item = items[item];
    var count = Cookies.getJSON('cart').filter(function(x){return x==item}).length;
    $('#item_count_' + item).html(count);
  }
}

function addToCart(item) {
  var items = Cookies.getJSON('cart');
  if (typeof items == 'undefined') {
    items = [item,];
  } else {
    var index = $.inArray(item, items);
    items.push(item);
  }
  console.log(items , ":" , index);
  Cookies.set('cart', items);
  $('.cart_size').html(items.length);
  var count = items.filter(function(x){return x==item}).length;
  $('#item_count_' + item).html(count);
}

function removeFromCart(item) {
  var items = Cookies.getJSON('cart');
  if (typeof items == 'undefined') {
    return -1;
  }
  console.log(item);
  var index = jQuery.inArray(item, items);
  console.log(item, items , index);
  if (index > -1 ) {
    items.splice(index, 1);
    Cookies.set('cart', items);
    $('.cart_size').html(items.length);
    var count = items.filter(function(x){return x==item}).length;
    if (count < 1)
      $('#item_' + item).hide();
    else
      $('#item_count_' + item).html(count);
    return 1;
  } else {
    return -1;
  }
}

function removeAllFromCart(item) {
  while( removeFromCart(item) == 1);
}

function emptyCart() {
  Cookies.remove('cart');
  $('.cart_size').html(0);
}
