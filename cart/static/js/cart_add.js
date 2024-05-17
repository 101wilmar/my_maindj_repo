$(document).ready(function() {
  $('.add_cart').submit(function(event) {
    event.preventDefault(); // Предотвращаем отправку формы

    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize();

    $.ajax({
      url: url,
      type: 'POST',
      data: data,
      dataType: 'json',
      success: function(response) {
        if (response.success) {
          // Обновляем информацию о корзине на текущей странице
          // Например, обновляем счётчик количества товаров в корзине или отображаем уведомление
          alert(response.message);
        } else {
          // Выводим сообщение об ошибке, если добавление товара не удалось
          alert(response.message);
        }
      },
      error: function(xhr, status, error) {
        // При возникновении ошибки в AJAX запросе выводим сообщение об ошибке
        alert('An error occurred while adding the product to the cart.');
      }
    });
  });
});