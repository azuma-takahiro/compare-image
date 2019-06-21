$(function () {
    //画像ファイルプレビュー表示のイベント追加 fileを選択時に発火するイベントを登録
    $('form').on('change', 'input[type="file"]', function (e) {
        var file = e.target.files[0],
            reader = new FileReader(),
            $preview = $(".preview");
        t = this;

        // 画像ファイル以外の場合は何もしない
        if (file.type.indexOf("image") < 0) {
            return false;
        }

        // ファイル読み込みが完了した際のイベント登録
        reader.onload = (function (file) {
            return function (e) {
                //既存のプレビューを削除
                $preview.empty();
                // .prevewの領域の中にロードした画像を表示するimageタグを追加
                $preview.append($('<img>').attr({
                    src: e.target.result,
                    width: "150px",
                    class: "preview",
                    title: file.name
                }));
            };
        })(file);

        reader.readAsDataURL(file);
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function file_upload(button) {
    var form = $(button).parent('form').get(0);
    var formData = new FormData(form);
    if ($('#input_file')[0].files[0] === undefined) {
        alert('画像が選択されていません！！！')
        return false;
    }

    $.ajax({
        url: '/ajax/upload_file',
        method: 'post',
        dataType: 'json',
        data: formData,
        processData: false,
        contentType: false
    }).done(function (res) {
        console.log('SUCCESS', res)
        $('#input_file_id').val(res.file_id);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log('ERROR', jqXHR, textStatus, errorThrown);
    })

    return false;
}
