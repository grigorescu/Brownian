/** Local JS functions **/

function appendToQuery(event, query, filter, operator){
    if (operator == undefined){
        operator = "AND"
    }
    if ($(query) == undefined){
        return false;
    }

    var currentQuery = $(query).val();
    var newQuery = '';

    if (event.shiftKey){
        <!-- If the user shift+clicked, we negate it. -->
        newQuery = '!';
    }
    newQuery += filter;
    if (currentQuery != "*" && currentQuery != ""){
        newQuery = currentQuery + ' ' + operator + ' ' + newQuery;
    }
    $(query).val(newQuery);
    return true;
}