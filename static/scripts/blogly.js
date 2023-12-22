$(function () {
  let c = $("h2").attr("class");
  if (c) {
    $("body").css("background-color", "#003049");
  }
  $("span").on("click", function (e) {
    $(this).parent().hide();
    $("body").css("background-color", "#fdf0d5");
  });
});
