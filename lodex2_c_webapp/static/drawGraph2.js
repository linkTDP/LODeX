function myGraph(el) {

    // Add and remove elements on the graph object
    this.addNode2 = function (id,color) {
        nodes2.push({"id":id,"color":color});
        update();
    }

    this.removeNode2 = function (id) {
        var i = 0;
        var n = findNode2(id);
        while (i < links2.length) {
            if ((links2[i]['source'] === n)||(links2[i]['target'] == n)) links2.splice(i,1);
            else i++;
        }
        var index2 = findNode2Index(id);
        if(index2 !== undefined) {
            nodes2.splice(index2, 1);
            update();
        }
    }

    this.addLink2 = function (sourceId, targetId) {
        var sourceNode2 = findNode2(sourceId);
        var targetNode2 = findNode2(targetId);

        if((sourceNode2 !== undefined) && (targetNode2 !== undefined)) {
            links2.push({"source": sourceNode2, "target": targetNode2});
            update();
        }
    }

    var findNode2 = function (id) {
        for (var i=0; i < nodes2.length; i++) {
            if (nodes2[i].id === id)
                return nodes2[i]
        };
    }

    var findNode2Index = function (id) {
        for (var i=0; i < nodes2.length; i++) {
            if (nodes2[i].id === id)
                return i
        };
    }

    // set up the D3 visualisation in the specified element
    var w = $(el).innerWidth(),
        h = $(el).innerHeight();

    var vis = this.vis = d3.select(el).append("svg:svg")
        .attr("width", w)
        .attr("height", h);

    var force2 = d3.layout.force()
        .gravity(.05)
        .distance(100)
        .charge(-100)
        .size([w, h]);

    var nodes2 = force2.nodes(),
        links2 = force2.links();

    var update = function () {

        

        var node2 = vis.selectAll("g.node")
            .data(nodes2, function(d) { return d.id;});

        var nodeEnter = node2.enter().append("g")
            .attr("class", "node")
            .call(force2.drag);

        
        nodeEnter.append("svg:circle")
	      .attr("class", "circle")
	      .attr("stroke","black" )
	      .attr("stroke-width", "1.5px")
	      .attr("r", 10)
	      .style("fill",function(d) {return d.color})
	      .on("mouseover",nodeMouseOver2)      
	      
//            .attr("xlink:href", "https://d3nwyuy0nl342s.cloudfront.net/images/icons/public.png")
//            .attr("x", "-8px")
//            .attr("y", "-8px")
//            .attr("width", "16px")
//            .attr("height", "16px");

        nodeEnter.append("text")
            .attr("class", "nodetext")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .style("font-family","Lato, sans-serif")
			.style("font-weight", 500)
			.attr("font-size", "15px")
			.attr("fill", "black")
            .text(function(d) {return d.id});

        node2.exit().remove();
        
        var link2 = vis.selectAll("line.link")
        .data(links2, function(d) { return d.source.id + "-" + d.target.id; });

    link2.enter().insert("line")
        .attr("class", "link");

    link2.exit().remove();

        force2.on("tick", function() {
          link2.attr("x1", function(d) { return d.source.x; })
              .attr("y1", function(d) { return d.source.y; })
              .attr("x2", function(d) { return d.target.x; })
              .attr("y2", function(d) { return d.target.y; });

          node2.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
        });

        // Restart the force layout.
        force2.start();
    }

    // Make it all go
    update();
}

function nodeMouseOver2(d){
	nodeMouseOver( _.find(ike.nodes,function(nod){return nod.index ==  _.find(curQCN,function(a){return d.id == a.param.substr(1) }).nodeId}),
			       '?'+d.id )
}

graph2 = new myGraph("#graph2");

// You can do this from the console as much as you like...
//graph2.addNode2("Cause");
//graph2.addNode2("Effect");
//graph2.addLink2("Cause", "Effect");
//graph2.addNode2("A");
//graph2.addNode2("B");
//graph2.addLink2("A", "B");
