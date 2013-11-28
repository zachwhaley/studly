$(document).ready(function() {
    $.getJSON("/reflectors.json", function(reflectors) {
        var refs = $("#refs");
        $.each(reflectors, function(i, v) {
            $(refs).append($('<h3>').text(v.name));

            var div = $('<div>'); 
            $(refs).append(div);

            var table = $('<table>');
            $(div).append(table);

            $.each(v.list, function(i, v) {
                $(table)
                .append($('<tr>')
                    .append($('<td>')
                        .text(v)
                    )
                    .append($('<td>')
                        .append($('<input>')
                            .attr("type", "button")
                            .attr("value", "Remove")
                            .attr("name", v)
                            .click(function() {
                                alert("Remove " + v + "?")
                            })
                        )
                    )
                )
            });
            $(div)
            .append($('<input>'))
            .append($('<input>')
                .attr("type", "button")
                .attr("value", "Add email")
            );
        });
    });
    $("#refs").accordion();
});
