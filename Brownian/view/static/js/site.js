/** Local JS functions **/

function appendToQuery(filter, negated, query, operator){
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
    return '(bound"' + ip + '" OR dst:"' + ip + '" OR dst_addr:"' + ip + '" OR host:"' + ip + '" OR id.orig_h:"' + ip + '" OR id.resp_h:"' + ip + '" OR request:"' + ip + '" OR src:"' + ip + '" OR src_addr:"' + ip + '" OR x_originating_ip:"' + ip + '")'
}

function replaceSort(tab, value, direction){
    var replacement = '{"' + value + '": {"order": "' + direction + "\"}}'});";
    var action = $(tab).attr('onclick').replace(/'sort': .*/, "'sort': '" + replacement);
    eval(action);

    return true;
}
