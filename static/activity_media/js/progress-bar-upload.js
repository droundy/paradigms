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
      location.reload(true);
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
          "<tr><td><img src='" + data.result.url + "' width='100px'></td><td><a href='" + data.result.url + "'>" + data.result.name + "</a><br><a class='btn btn-warning btn-sm' role='button' href=\"/activity_media/delete_media/" + data.result.newMediaID + "\"><span class=\"oi oi-trash\" title=\"Delete this uploaded item.\" alt=\"Delete this uploaded item.\"></span> Delete</a></td></tr>"
        )
      }
    }

  });

});
