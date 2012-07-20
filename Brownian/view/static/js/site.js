/** Local JS functions **/

function appendToQuery(query, filter, operator, negated){
    if (operator == undefined){
        operator = "AND"
    }
    if (negated == undefined){
        negated = false;
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

function replaceSort(tab, value, direction){
    var replacement = '{"' + value + '": {"order": "' + direction + "\"}}'});";
    var action = $(tab).attr('onclick').replace(/'sort': .*/, "'sort': '" + replacement);
    eval(action);

    return true;
}
