const $ = jQuery;

$.datetimepicker.setLocale('fr');

$('#id_start_date').datetimepicker();
$('#id_end_date').datetimepicker();

function openForm(reservationId) {
    $("form").trigger("reset");
    $(".form-container").css("display", "flex");
    $("#id_add_reservation").hide();
    $("#id_id").val(reservationId);
    $(".errors-list, .errors").html("");
    const request = $.ajax({
        url: reservationId + "/",
        method: "GET",
    });
    request.done(function (data) {
        for (const [key, value] of Object.entries(data)) {
            $("#id_" + key).val(value);
        }
    })
}

function closeForm() {
    $(".form-container").hide();
    $("#id_add_reservation").show();
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
        $("#resa_" + reservationId).remove();
    })
}

function submitForm() {
    const data = $(".form-container form").serialize();
    const request = $.ajax({
        url: "",
        data: data,
        method: "POST",
    });
    request.done(function (data) {
        if (data.errors) {
            for (const [key, value] of Object.entries(data.errors)) {
                let html = '<p>' + value + '</p>';
                $("#id_error_" + key).html(html);
            }
        } else {
            if (data.id) {
                const newReservation =
                    '<div class="reservation-container">' +
                    '<div id="resa_"' + data.id + '>' +
                    '<p>' + data.title + '</p>' +
                    '<button onclick="openForm(' + data.id + ')">Modify</button>' +
                    '<button onclick="cancelReservation(' + data.id + ')">Cancel</button>' +
                    '</div>' +
                    '</div>';
                $(".future-container").append(newReservation);
            }

            $(".form-container").hide();
            $("#id_add_reservation").show();
        }

    })
    request.fail(function (response) {
        $(".errors").html("<p>An error occured.</p>");
    })

}

function addReservation() {
    $(".form-container").css("display", "flex");
    $("form").trigger("reset");
    $("#id_add_reservation").hide();
    $("#id_id").val(null);
    $(".errors-list, .errors").html("");
}

