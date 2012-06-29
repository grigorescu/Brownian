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
    if (negated){
        $(query).val('!' + filter);
    }
    else {
        $(query).val(filter);
    }
    return true;
}