$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,

    start: function (e) {
      $("#modal-progress").modal("show");
    },

    stop: function (e) {
      $("#modal-progress").modal("hide");
    },

    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },

    done: function (e, data) {
      if (data.result.is_valid) {
        // alert('Data.result: ' + data.result.url + 'yyyyy' + data.result.name)
        $("#gallery tbody").prepend(
          "<tr><td><img src='" + data.result.url + "' width='100px'><a href='" + data.result.url + "'>" + data.result.name + "</a> <a class='btn btn-danger' role='button' href=\"/activity_media/delete_figure/" + data.result.newMediaID + "\">Delete</a></td></tr>"
        )
      }
    }

  });

});
