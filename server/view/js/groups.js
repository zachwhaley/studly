$(document).ready(function() {
    var groups = [
        {name: "foo", list: ["bar", "gii"]},
        {name: "bar", list: ["foo", "gii"]}
    ];
    var grp = $("#grp");
    $.each(groups, function(i, v) {
        $(grp).append($('<h3>').text(v.name));

        var div = $('<div>'); 
        $(grp).append(div);

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
                        .attr("value", "View Event Info")
                        .attr("name", v)
                        .click(function() {
                            alert("View Event Info for " + v)
                        })
                    )
                )
            );
        });
        $(div)
        .append($('<input>'));
        $(div)
        .append($('<input>')
            .attr("type", "button")
            .attr("value", "Join")
            .attr("name", v)
            .click(function() {
                alert("Join " + v);
            })
        );
    });
    $("#grp").accordion();
});
