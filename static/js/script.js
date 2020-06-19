$(document).ready(function () {
    $('.deleteButton').click(function (e) {
        e.preventDefault();
        $('.modale').addClass('opened');
        var value = $(this).val();
        $("#object_id_placeholder_div").html(`<input hidden="true" id="object_id_placeholder_input" value="` + value + `">`)
    });
    $('.closemodale').click(function (e) {
        e.preventDefault();
        $('.modale').removeClass('opened');
    });

    $("#modal_delete_button").click(function () {
        var object_id = $("#object_id_placeholder_input").val();
        var protocol = window.location.protocol
        var hostname = window.location.hostname
        var port = window.location.port
        var url = protocol + "//" + hostname + ":" + port + "/adminpanel" + "/form-delete" + "/" + object_id + "/"
        window.location.href = url
    });
});

$(document).ready(function () {
    $('.deleteButton').click(function (e) {
        e.preventDefault();
        $('.modale').addClass('opened');
        var value = $(this).val();
        $("#object_id_placeholder_div2").html(`<input hidden="true" id="object_id_placeholder_input2" value="` + value + `">`)
    });
    $('.closemodale').click(function (e) {
        e.preventDefault();
        $('.modale').removeClass('opened');
    });

    $("#modal_delete_button2").click(function () {
        var object_id = $("#object_id_placeholder_input2").val();
        var protocol = window.location.protocol
        var hostname = window.location.hostname
        var port = window.location.port
        var url = protocol + "//" + hostname + ":" + port + "/adminpanel" + "/contactus-delete" + "/" + object_id + "/"
        window.location.href = url
    });
});


$(document).ready(function () {
    $('.deleteButton').click(function (e) {
        e.preventDefault();
        $('.modale').addClass('opened');
        var value = $(this).val();
        $("#object_id_placeholder_div3").html(`<input hidden="true" id="object_id_placeholder_input3" value="` + value + `">`)
    });
    $('.closemodale').click(function (e) {
        e.preventDefault();
        $('.modale').removeClass('opened');
    });

    $("#modal_delete_button3").click(function () {
        var object_id = $("#object_id_placeholder_input3").val();
        var protocol = window.location.protocol
        var hostname = window.location.hostname
        var port = window.location.port
        var url = protocol + "//" + hostname + ":" + port + "/adminpanel" + "/customuser-delete" + "/" + object_id + "/"
        window.location.href = url
    });
});


$(document).ready(function () {
    $('.deleteButton').click(function (e) {
        e.preventDefault();
        $('.modale').addClass('opened');
        var value = $(this).val();
        $("#object_id_placeholder_div4").html(`<input hidden="true" id="object_id_placeholder_input4" value="` + value + `">`)
    });
    $('.closemodale').click(function (e) {
        e.preventDefault();
        $('.modale').removeClass('opened');
    });

    $("#modal_delete_button4").click(function () {
        var object_id = $("#object_id_placeholder_input4").val();
        var protocol = window.location.protocol
        var hostname = window.location.hostname
        var port = window.location.port
        var url = protocol + "//" + hostname + ":" + port + "/adminpanel" + "/notify-delete" + "/" + object_id + "/"
        window.location.href = url
    });
});


$(document).ready(function () {
    $('.deleteButton').click(function (e) {
        e.preventDefault();
        $('.modale').addClass('opened');
        var value = $(this).val();
        $("#object_id_placeholder_div5").html(`<input hidden="true" id="object_id_placeholder_input5" value="` + value + `">`)
    });
    $('.closemodale').click(function (e) {
        e.preventDefault();
        $('.modale').removeClass('opened');
    });

    $("#modal_delete_button5").click(function () {
        var object_id = $("#object_id_placeholder_input5").val();
        var protocol = window.location.protocol
        var hostname = window.location.hostname
        var port = window.location.port
        var url = protocol + "//" + hostname + ":" + port + "/adminpanel" + "/subscribenow-delete" + "/" + object_id + "/"
        window.location.href = url
    });
});