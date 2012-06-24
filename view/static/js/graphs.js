function displayNumber(x) {
    // Simple function to denote millions (M) and thousands (K).
    // TODO: Add a decimal point or two to M/K?

    if (x > 1000000) {return Math.floor(x/1000000) + "M";}
    if (x > 1000) {return Math.floor(x/1000) + "K";}
    return x;
}

function createHistogram(orig, name)
{
    // Creates a histogram style SVG graph at object with id name with data from orig.

    var width = 900;    // Graph width
    var height = 400;   // Graph height

    var data = [];    // Orig is a JSON object, and is split up into
    var labels = [];  // these arrays by key/value.
    d3.map(orig).forEach(function (d, i) { data.push(i["count"]); labels.push(i["time"]);});

    var chart = d3.select("#" + name) // Select the right object,
                  .append("svg")      // add an SVG to it,
                  .attr("class", "chart").attr("width", width).attr("height", height); // and create a chart.

    var x = d3.scale.ordinal()
                    .domain(labels)
                    .rangeBands([0, width]); // Split the keys up into distinct bands.

    var y = d3.scale.linear()
                    .domain([0, d3.max(data)])
                    .range([height, 0]);     // y = 0 is at the top of the graph, so we scale and flip the value.

    chart.append("line")                         // Create a line
         .attr("x1", 0).attr("x2", width)        // going across the graph
         .attr("y1", height).attr("y2", height)  // at the bottom
         .style("stroke", "#aaa");

    chart.selectAll("rect").data(data).enter()                             // Create the bars
        .append("a")                                                       // with links
        .attr("xlink:href", function(d, i) {return "/time/" + labels[i];}) // that link to /time/$timestamp. TODO
        .append("rect").attr("x", x).attr("y", height)                     // The bars start at the bottom
        .attr("height", 0)                                                 // with no height for now
        .attr("width", x.rangeBand() - 3)                                  // leave 3px of padding between them
        .attr("rel", "tooltip_top")                                        // and add a tooltip with the value.
        .attr("data-original-title", function(d, i) {return displayNumber(data[i]);});

    chart.selectAll("rect").data(data)
        .transition().duration(1000)           // Finally, create a 1-second transition
        .attr("height", height).attr("y", y);  // of the bars rising up to their real height.
}

function createTopGraph(orig, name, url)
{
    // Create a top X entries horizontal SVG graph at object with id name with data from orig.
    // Each bar has a link to URL + the key of that bar (e.g. /ip/127.0.0.1)

    // TODO this should be generalized with createHistogram above - much duplication here.

    var width = 230;  // Graph width
    var height = 200;   // Graph height

    var data = [];    // Orig is a JSON object, and is split up into
    var labels = [];  // these arrays by key/value.
    d3.map(orig).forEach(function (d, i) { data.push(i["count"]); labels.push(i["term"]);});

    var chart = d3.select("#" + name) // Select the right object,
                  .append("svg")      // add an SVG to it,
                  .attr("class", "chart").attr("width", width).attr("height", height); // and create a chart.

    var x = d3.scale.linear()
        .domain([0, d3.max(data)])
        .range([0, height]);     // Scale linearly

    var y = d3.scale.ordinal()
        .domain(labels)
        .rangeBands([0, width]); // Split the keys up into distinct bands.

    chart.append("line")                        // Create a line
        .attr("y1", 0).attr("y2", height)       // going across the graph
        .attr("x1", 0).attr("x2", 0)            // at the left
        .style("stroke", "#aaa");

    chart.selectAll("rect").data(data).enter()                             // Create the bars
        .append("a")                                                       // with links
        .attr("xlink:href", function(d, i) {return url + labels[i];})   // that link to /ip/$ip. TODO
        .append("rect").attr("y", y).attr("x", 0)                          // The bars start on the left
        .attr("width", 0)                                                  // with no width for now
        .attr("height", y.rangeBand() - 3)                                 // leave 3px of padding between them
        .attr("rel", "tooltip_top")                                        // and add a tooltip with the value.
        .attr("data-original-title", function(d, i) {return displayNumber(data[i]);});

    chart.selectAll("rect").data(data)
        .transition().duration(1000)   // Create a 1-second transition
        .attr("width", x);             // of the bars growing to their real width.

    chart.selectAll("text").data(data).enter()
        .append("text").attr("x", width)                        // Finally, add some labels on the right
        .attr("y", function(d) {return y(d) + y.rangeBand();})
        .attr("dx", -3).attr("dy", "-.35em").attr("text-anchor", "end")
        .text(function(d, i) {return labels[i]});               // with the name.
}