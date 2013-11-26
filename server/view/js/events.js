$(document).ready(function() {
    var events = [
        {name: "foo", list: ["bar", "gii"]},
        {name: "bar", list: ["foo", "gii"]}
    ];
    var evts = $("#evts");
    $.each(events, function(i, v) {
        $(evts).append($('<h3>').text(v.name));

        var div = $('<div>'); 
        $(evts).append(div);

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
                            alert("Remove " + v + "?");
                        })
                    )
                )
            )
        });
        var select = $('<select>');
        $(div)
        .append(select);

        var refs = ["foo", "bar"];
        $.each(refs, function(i , v) {
            $(select)
            .append($('<option>')
                .text(v)
            );
        });
        $(div)
        .append($('<input>')
            .attr("type", "button")
            .attr("value", "Add List")
            .click(function() {
                alert("Add " + $(select).val() + "?");
            })
        );
    });
    $("#evts").accordion();
});
