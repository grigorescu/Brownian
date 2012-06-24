/** Local JS functions **/

function appendToQuery(query, filter, operator){
    if (operator == undefined){
        operator = "AND"
    }
    if ($(query) == undefined){
        return false;
    }

    var currentQuery = $(query).val();
    var newQuery;
    if (currentQuery == "*"){
        newQuery = filter;
    }
    else{
        newQuery = currentQuery + ' ' + operator + ' ' + filter;
    }
    $(query).val(newQuery);
    return true;
}