/** Local JS functions **/

function appendToQuery(filter, negated, query, operator){
    $('.dropdown.open .dropdown-toggle').dropdown('toggle');

    if (operator == undefined){
        operator = "AND"
    }
    if (negated == undefined){
        negated = false;
    }

    if (query == undefined){
        query = "#querytext";
    }

    if ($(query) == undefined){
        return false;
    }

    var currentQuery = $(query).val();
    var newQuery = '';
    if (negated){
        newQuery = '!';
    }
    newQuery += filter;
    if (currentQuery != "*" && currentQuery != ""){
        newQuery = currentQuery + ' ' + operator + ' ' + newQuery;
    }
    $(query).val(newQuery);
    return true;
}

function replaceQuery(query, filter, negated){
    $('.dropdown.open .dropdown-toggle').dropdown('toggle');

    if ($(query) == undefined){
        return false;
    }
    if (negated == undefined){
        negated = false;
    }
    var newQuery = filter;
    if (negated){
        $(query).val('!' + newQuery);
    }
    else {
        $(query).val(newQuery);
    }
    return true;
}

function ipanywhere(ip){
    return '(bound:"' + ip + '" OR dst:"' + ip + '" OR dst_addr:"' + ip + '" OR host:"' + ip + '" OR id.orig_h:"' + ip + '" OR id.resp_h:"' + ip + '" OR request:"' + ip + '" OR src:"' + ip + '" OR src_addr:"' + ip + '" OR x_originating_ip:"' + ip + '")'
}

function exportRow(rowNumber){
    var keys = new Array(0);
    var values = new Array(0);
    var count = 0;

    $('th > a[rel="popover"]').each(function(index, value) { keys.push($(this).html());} );
    $('#results > table > tbody > tr:eq(' + rowNumber + ') > td[class="fieldval"] > ul > li > a').each(function(index, value) {
        var value = $(this).html();
        if ( $(this).attr("title") )
            value = $(this).attr("title");
        values.push(value.replace('<b class="caret"></b>', '').replace(/(^\s*)|(\s*$)/gi,""));
    } );

    result = '';
    for (var i = 0; i < keys.length; i++) {
        if (i < values.length){
            if (/([0-9]|[A-Z]|[a-z])/.test(values[i])){
                result += keys[i] + ": " + values[i] + "\n";
                count += 1;
            }
        }
    }

    result = '<textarea rows=' + count + ' style="white-space:normal; width:90%">' + result;

    result += '</textarea>';
    return result;
}

function displayPluginOutput(output){
    $('#results').prepend('<div class="alert alert-info"><button type="button" class="close" data-dismiss="alert">×</button>' + output + '</div>');
}

function runPlugin(displayName, args){
    Dajaxice.Brownian.view.runPlugin(displayPluginOutput, {'displayName': displayName, 'args': args});
}

function replaceSort(tab, value, direction){
    var replacement = '{"' + value + '": {"order": "' + direction + "\"}}'});";
    var action = $(tab).attr('onclick').replace(/'sort': .*/, "'sort': '" + replacement);
    eval(action);

    return true;
}
