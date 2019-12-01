const $ = jQuery;

$.datetimepicker.setLocale('fr');

$('#id_start_date').datetimepicker();
$('#id_end_date').datetimepicker();

function openForm(reservationId) {
    $(".form-container").show();
    $("#id_id").val(reservationId);
}

function closeForm() {
    $(".form-container").hide();
}

function cancelReservation(reservationId) {
    $("#id_cancel").val("True");
    $("#id_id").val(reservationId);
    const data = $(".form-container").serialize();
    const request = $.ajax({
        url: "",
        data: data,
        method: "POST",
    });
    request.done(function () {
        console.log("CANCEL SUcESS");
        $("#resa_"+reservationId).remove();
    })
}

function submitForm() {
    const data = $(".form-container").serialize();
    const request = $.ajax({
        url: "",
        data: data,
        method: "POST",
    });
    request.done(function (data) {
        console.log("SUBMIT SUcESS");
        console.log(data);
    })
    request.fail(function (response) {
        console.log("SUBMIT ERROR");
        console.log(response);
        $(".errors").html(response.errors);
    })
    $(".form-container").hide();
}

function newReservation() {
    $(".form-container").show();
    $("#id_id").val(null);
}

