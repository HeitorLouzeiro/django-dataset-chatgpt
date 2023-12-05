$(document).ready(function () {
  var t = 0;
  $("#send").click(function (e) {
    e.preventDefault();
    var prompt = $("#prompt").val().trimEnd();
    console.log(prompt);
    if (prompt == "") {
      $("#response").text("Please ask a question.");
    } else {
      function myTimer() {
        $("#response").html("<p>Waiting for response ... " + t + "s</p>");
        t++;
      }
      const myInterval = setInterval(myTimer, 1000);

      var id = window.location.pathname.split('/').pop();

      $.ajax({
        url: "/query/" + id,
        method: "POST",
        data: JSON.stringify({ input: prompt }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
          if (data.success) {
            $("#response").html("<pre>" + data.response + "<pre>");
            $("#response").append(
              "<small class='text-secondary'>Responded in " +
                t +
                " seconds</small>"
            );
            $("#source").html(
              "<small class='text-secondary'>" + data.source + "</small>"
            );
          } else {
            // Se houver um erro, exiba a mensagem de erro
            $("#response").html("<p>Error: " + data.error + "</p>");
          }
          clearInterval(myInterval);
          t = 0;
        },
        error: function (xhr, status, error) {
          // Lidar com erros de requisição AJAX
          console.error('Erro AJAX:', error);
          $("#response").html("<p>Error: " + error + "</p>");
          clearInterval(myInterval);
          t = 0;
        },
      });
    }
  });
});