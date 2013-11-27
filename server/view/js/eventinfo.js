$(document).ready(function() {
    var events = [
        {name: "foo", next: "sometime", repeat: "Every time", start: "now", end: "whenever"},
        {name: "bar", next: "sometime", repeat: "Every time", start: "now", end: "whenever"},
    ];
    var info = $("#info");
    $.each(events, function(i, v) {
        $(info).append($('<h3>').text(v.name));

        var div = $('<div>'); 
        $(info).append(div);

        $(div)
        .append($('<table>')
            .append($('<tr>')
                .append($('<td>')
                    .text("Next Event Date:")
                )
                .append($('<td>')
                    .text(v.next)
                )
            )
            .append($('<tr>')
                .append($('<td>')
                    .text("Recurring Event")
                )
                .append($('<td>')
                    .text(v.repeat)
                )
            )
            .append($('<tr>')
                .append($('<td>')
                    .text("Start Date:")
                )
                .append($('<td>')
                    .text(v.start)
                )
            )
            .append($('<tr>')
                .append($('<td>')
                    .text("End Date:")
                )
                .append($('<td>')
                    .text(v.end)
                )
            )
        );
        $(div)
        .append($('<input>')
            .attr("type", "button")
            .attr("value", "View Attendees")
            .attr("name", v.name)
            .click(function() {
                alert("Viewing Attendees for " + v.name)
            })
        );
    });
    $("#info").accordion();
});
