var margin = {top: 20, right: 20, bottom: 30, left: 40};
	var width = document.documentElement.clientWidth - margin.right;// - margin.left - margin.right;
	var height = document.documentElement.clientHeight;// - margin.top - margin.bottom;
	var fill = d3.scale.category20();
	var stroke_width = 1.5;
	var offset_x = 10;
	var offset_y = 12;
	var color = d3.scale.category20();	
	var tick = false;
	var linkDistance=200;
	var div = d3.select("body").append("div")   
    .attr("class", "tooltip")
    .style("position", "absolute")
	 .style("top", 5)
	 .style("left",5)
// 	 .style("z-index",-1)
    .style("opacity", 1);
    
// 	var tooltip = d3.select("body")
// 	.append("div")
// 	.style("position", "absolute")
// 	.style("z-index", "10")
// 	.style("visibility", "hidden")
// 	.text(function(d) {return d.att});
// 	 var tip = d3.tip()
// 	  .attr('class', 'd3-tip')
// 	  .offset([-10, 0])
// 	  .html(function(d) {
// 	    return "<strong>Frequency:</strong> <span style='color:red'>" + d.ni + "</span>";
// 	  }); 
	
	function drawGraph(graph, svg){
    	console.log(graph);
		var vocab=graph.vocab;
		for (a in vocab){
			color(vocab[a]);
		}
		// console.log(vocab[0]);
		var max_ni = graph.nodes[0].ni;
		var max_np = graph.links[0].np;
		for(i = 1; i < graph.nodes.length; i++){
			if(graph.nodes[i].ni > max_ni)
				max_ni = graph.nodes[i].ni;
		}
		//console.log(min_ni);
		//console.log(max_ni);
		for(i = 1; i < graph.links.length; i++){
			if(graph.links[i].np > max_np)
				max_np = graph.links[i].np;
		}
		// console.log(max_np);
		// console.log((2500) * 31 / graph.nodes.length);
		// console.log(graph.nodes.length);
		//debugger;	
		var charge = (-3800) * 31 / graph.nodes.length;
 
	    // var svg = d3.select("body").append("svg").attr({"width":width,"height":height});
	    
		var force = d3.layout.force()
			.nodes(graph.nodes)
			.links(graph.links)
			.gravity(1).linkDistance([linkDistance])
			.charge(charge)
			.size([width, height])
			.start();
	      
	      
		var div = d3.select("body").append("div")   
			.attr("class", "tooltip")
			.style("position", "absolute")
			.style("top", 5)
			.style("left",5)
			// 	 .style("z-index",-1)
			.style("opacity", 1);
			
		var edgeLegend	= d3.select("body").append("div")   
		    .attr("class", "edgeLegend")
		    .attr({
		    	'width': '20px',
		    	'height': '10px', 
		    	'position': 'absolute',
		    	'overflow-y': 'auto'
		    })
		    .style("position", "absolute")
		// 	 .style("z-index",-1)
		    .style("opacity", 1);
	 
	
	    // var links = svg.selectAll("line.link")
	      // .data(graph.links)
	      // .enter().append("svg:path") //
	      // .attr("class", "link")
	      // .attr("id",function(d,i) {return 'edge'+i;})
	      // //.style("stroke-width", function(d) { return (d.np * 10 / max_np) + 1;; })
	      // .style("stroke-width", "1.5px")
	      // .attr("fill", "none")
	      // .attr('marker-end',function(d){if(d.source.x != d.target.x && d.source.y != d.target.y){return 'url(#arrowhead)'}})
	      // // .attr('marker-end','url(#arrowhead)')
	      // .style("stroke",'black');
	      // //.style("pointer-events", "none");

	      
	    var links = svg.selectAll("line.link")
		      .data(graph.links)
		      .enter().append("svg:line") //
		      .attr("class", "link")
		      .attr("id",function(d,i) {return 'edge'+i;})
		      .attr('marker-end','url(#arrowhead)')
		      // .style("stroke-width", function(d) { return (d.np * 10 / max_np) + 1;; })
		      .attr("x1", function(d) { return d.source.x; })
			  .attr("y1", function(d) { return d.source.y; })
		  	  .attr("x2", function(d) { return d.target.x; })
		  	  .attr("y2", function(d) { return d.target.y; });
		  	  // .append(function(d){
		  	  	// s='<table>'
		  	  	// for(i=0;i<d.label.length;i++){
		  	  		// console.log(d.label[i].name);
		  	  		// s+="<tr><td>"+d.label[i].name+"</tr></td>";
		  	  	// }
		  	  	// s+="</table>"
		  	  	// return s
		  	  // }, function(d,i) {return 'edge'+i;});
		  	  
		// var edgelabels = svg.selectAll(".edgelabel")
	        // .data(graph.links)
	        // .enter()
	        // .append('text')
	        // .style("pointer-events", "none")
	        // .attr({'class':'edgelabel',
	               // 'id':function(d,i){return 'edgelabel'+i},
	               // 'dx':80,
	               // 'dy':0,
	               // 'font-size':15,
	               // 'fill':'#aaa'});
	    autoedges=[]         
	    for(i=0;i<graph.links.length;i++){
	    	if(graph.links[i].source == graph.links[i].target){
	    		console.log('autonode')
	    		autoedges.push(graph.links[i])
	    	} 
	    }
	    
	    var autoedges = svg.selectAll('.autoedges')
	    	.data(autoedges)
	    	.enter().append("svg:path") //
	      	.attr("class", "link")
	      	.attr("id",function(d,i) {return 'autoedge'+i;})
	      //.style("stroke-width", function(d) { return (d.np * 10 / max_np) + 1;; })
	      	.style("stroke-width", "1.5px")
	      	.attr("fill", "none")
	      // .attr('marker-end','url(#arrowhead)')
	      	.style("stroke",'silver');
	      //.style("pointer-events", "none");
	      
	    var nodes = svg.selectAll("circle.node")
	      .data(graph.nodes)
	      .enter().append("svg:circle")
	      .attr("class", "node")
	      .attr("r", function(d) { return (d.ni * 25 / max_ni)+5; }) //dimensione nodi
	      .style("fill", function(d) { return color(d.vocab); })
	      .call(force.drag)
	      .on("mouseover", function(d) {      
            div.transition()        
                .duration(1000)      
                .style("opacity", 1); 
            s="<table>";
//             console.log(d.att)
            for (var j = 0; j < d.att.length; j++){
            	s+="<tr>";
            	s+="<td>";
            	s+='<svg width="8" height="8"> <rect width="8" height="8" style="fill:'+color(d.att[j].vocab)+';" /></svg></td>';
//             	console.log('<svg width="10" height="10"> <rect width="10" height="10" style="fill:'+d.att[j].vocab+';" /></svg>')
            	s+= '<td>'+d.att[j].p;
            	s+="</td>";
            	s+="<td>";
            	s+=d.att[j].n;
            	s+="</td>";
            	s += "</tr>";
            	console.log(color(d.att[j].vocab));
            }
            s+="</table>";
            
            t='<table class="title"><tr><td>'+d.name+'</td><td>'+d.ni+'<span class="instances"> instances</span></td></tr></table><br>'
            entranti=[]
            uscenti=[]
            edges=graph.links
            for(i=0; i<edges.length;i++){
            	if(edges[i].source.index == d.index){
            		for(j=0;j<edges[i].label.length;j++){
            			tmp=edges[i].label[j]
            			tmp.target=edges[i].target.name
            			uscenti.push(tmp)	
            		}
            	}
            	else{
            		if(edges[i].target.index == d.index){
            			for(j=0;j<edges[i].label.length;j++){
            				tmp=edges[i].label[j]
            				tmp.source=edges[i].source.name
	            			entranti.push(tmp)	
	            		}
            		}
            	}
            }
            t+="<table>"
            if(entranti.length > 0){
            	for(i=0; i<entranti.length;i++){
            		t+='<tr><td><svg width="8" height="8"> <rect width="8" height="8" style="fill:'+color(entranti[i].vocab)+';" /></svg></td>'
            		t+='<td>'+entranti[i].name+'</td>'
            		t+='<td><div title="Code: 0xe800" class="the-icons"><i class="icon-left-open-outline"></i></div></td>';
            		tmp=entranti[i].np/d.ni
            		t+='<td>'+entranti[i].source+'</td>'
            		t+='<td>'+tmp.toFixed(2)+'</td>'
            		t+='</tr>'
            	}
            }
            if(uscenti.length > 0){
            	for(i=0; i<uscenti.length;i++){
            		t+='<tr><td><svg width="8" height="8"> <rect width="8" height="8" style="fill:'+color(uscenti[i].vocab)+';" /></svg></td>'
            		t+='<td>'+uscenti[i].name+'</td>'
            		t+='<td><div title="Code: 0xe800" class="the-icons"><i class="icon-right-open-outline"></i></div></td>';
            		tmp=uscenti[i].np/d.ni
            		t+='<td>'+uscenti[i].target+'</td>'
            		t+='<td>'+tmp.toFixed(2)+'</td>'
            		t+='</tr>'
            	}
            }
            t+='</table>'
            console.log('entranti');
            console.log(entranti);

             
            div.html(s)  
                .style("left", "5px" )    //(d3.event.pageX)
                 .style("bottom", "5px" )
                  .style("font-family","Lato, sans-serif")
                  .style("font-size", "15px")
                  .style("font-weight",500);   
                  
             edgeLegend.html(t)  
                .style("left", "5px" )    //(d3.event.pageX)
                 .style("top", "5px" )
                  .style("font-family","Lato, sans-serif")
                  .style("font-size", "15px")
                  .style("font-weight",500);   
			});
			// .on("mouseout", function(d) {       
	            // div.transition()        
	                // .duration(500)      
	                // .style("opacity", 0);
//  
	       // });
	        
	        
	    var nodelabels = svg.selectAll(".nodelabel") 
	       .data(graph.nodes)
	       .enter()
	       .append("text")
	       .attr({"x":function(d){return d.x+ (d.ni * 25 / max_ni) + 5  + stroke_width; },
	              "y":function(d){return d.y;},
	              "class":"nodelabel"})
			.style("font-family","Lato, sans-serif")
			.attr("font-size", "15px")
			.attr("fill", "black")
	       .text(function(d){return d.name;});
	       
	    nodes.append("title")
			.text(function(d) { return d.name; });
		links.append("title")
			.text(function(d) { return d.name; });
			
		svg.style("opacity", 1e-6)
			.transition()
			.duration(1000)
			.style("opacity", 1);
			
		var legend = svg.selectAll(".legend")
			.data(color.domain())
			.enter().append("g")
			.attr("class", "legend")
			.attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  // draw legend colored rectangles
		legend.append("rect")
				.attr("x", width - 18)
  				.attr("width", 18)
				.attr("height", 18)
      			.style("fill", color);

  // draw legend text
		legend.append("text")
		  		.attr("x", width - 24)
				.attr("y", 9)
				.attr("dy", ".35em")
				.style("text-anchor", "end")
				.style("font-family","Lato, sans-serif")
				.style("font-size", "15px")
				.style("font-weight", 500)
				.text(function(d) { return d;});
	       
	    var edgepaths = svg.selectAll(".edgepath")
	        .data(graph.links)
	        .enter()
	        .append('path')
	        .attr({'d': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
	               'class':'edgepath',
	               'fill-opacity':0,
	               'stroke-opacity':0,
	               'fill':'blue',
	               'stroke':'red',
	               'id':function(d,i) {return 'edgepath'+i}})
	        .style("pointer-events", "none");
	
	    // var edgelabels = svg.selectAll(".edgelabel")
	        // .data(graph.links)
	        // .enter()
	        // .append('text')
	        // .style("pointer-events", "none")
	        // .attr({'class':'edgelabel',
	               // 'id':function(d,i){return 'edgelabel'+i},
	               // 'dx':80,
	               // 'dy':0,
	               // 'font-size':15,
	               // 'fill':'#aaa'});
	             
		
	    // edgelabels.append('textPath')
	        // .attr('xlink:href',function(d,i) {return '#edgepath'+i})
	        // .style("pointer-events", "none")
	        // .attr('fill', 'black')
	        // .attr('class', 'textPath')
	        // .attr('id', function(d,i) {return 'textPath'+i})
	        // .text(function(d){return "label"})
	        // .append('tspan')
	        // .text('fuck')
	        // .call(function(d){
	        	// console.log(d)
	        	// debugger
	        	// for(i=0; i<d.label.length;i++){
		        	// edgelabels.append('tspan')
		        	// edgelabels.text(d.label[i].name)
	        	// }
	        // });
	        // .call(function(d){
	        	// list=[];
	        	// for(i=0; i < d.label.length;i++){
	        		// // console.log(d.label[i].dir)
	        		// list.push(d.label[i].name);
// 	        		
	        	// }
	        	// console.log(list)
	        	// return list;
        	// });
        
		
		// console.log(list)
	
	
	    force.on("tick", function(){
	        links.attr({"x1": function(d){return d.source.x;},
	                    "y1": function(d){return d.source.y;},
	                    "x2": function(d){return d.target.x;},
	                    "y2": function(d){return d.target.y;}
	        });
	
	        nodes.attr({"cx":function(d){return d.x;},
	                    "cy":function(d){return d.y;}
	        });
	
	        nodelabels.attr("x", function(d){return d.x+ (d.ni * 25 / max_ni) + 5  + stroke_width;}) 
	                  .attr("y", function(d) { return d.y; });
	
	        edgepaths.attr('d', function(d) { var path='M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y;
	                                           //console.log(d)
	                                           return path});  
	                                           
	        // edgerects.attr('x', function(d){return d.source.x - (d.source.x - d.target.x)/2 })
	        		 // .attr("y", function(d){
						// return d.source.y + (d.source.y - d.target.y)/2;  
					  // });

	                                           
	        // edgepaths.attr("d", function(d) {
		        // var dx = d.target.x - d.source.x,
		            // dy = d.target.y - d.source.y,
		            // dr = Math.sqrt(dx * dx + dy * dy);
		        // return "M" + 
		            // d.source.x + "," + 
		            // d.source.y + "A" + 
		            // dr + "," + dr + " 0 0,1 " + 
		            // d.target.x + "," + 
		            // d.target.y;
		    // }); 
	
	        // edgelabels.attr('transform',function(d,i){
	            // if (d.target.x<d.source.x){toedges
	                // bbox = this.getBBox();
	                // rx = bbox.x+bbox.width/2;
	                // ry = bbox.y+bbox.height/2;
	                // return 'rotate(180 '+rx+' '+ry+')';
	                // }
	            // else {
	                // return 'rotate(0)';
	                // }
	        // });
	        
	         autoedges.attr("d", function(d) {
	         	var dx = d.target.x - d.source.x,
	            	dy = d.target.y - d.source.y,
	            	dr = Math.sqrt(dx * dx + dy * dy),
	            	x1 = d.source.x,
					y1 = d.source.y,
					x2 = d.target.x,
					y2 = d.target.y;
	         
				var xRotation = 0, // degrees
					largeArc = 0, // 1 or 0
					sweep = 1; // 1 or 0
					xRotation = -45;

       				 // Needs to be 1.
		            largeArc = 1;
		
		            // Change sweep to change orientation of loop. 
		            //sweep = 0;
		
		            // Make drx and dry different to get an ellipse
		            // instead of a circle.
		            drx = 30;
		            dry = 20;
		            
		            // For whatever reason the arc collapses to a point if the beginning
		            // and ending points of the arc are the same, so kludge it.
		            x2 = x2 + 1;
		            y2 = y2 + 1;
					return "M" + x1 + "," + y1 + "A" + drx + "," + dry + " " + xRotation + "," + largeArc + "," + sweep + " " + x2 + "," + y2;
		        
		    });
	        
	    });
    }

	d3.json("getData/{{endpoint_id}}", function(error, graph) {
		var svg = d3.select("#chart")
			.append("svg:svg")
			    .attr("width", width)
			    .attr("height", height)
			    .attr("pointer-events", "all")
		    .append('svg:g')
				//.call(d3.behavior.zoom().on("zoom", redraw)) //bug quando viene chiamat la funzione tick, si scatena anche redraw
			.append('svg:g');
			
			svg.append('svg:rect')
		    .attr('width', width)
		    .attr('height', height)
		    .attr('fill', 'white');
    	//console.log(graph);
    	
    	// links=graph.links;
    	// console.log(links);
    	// edges=[];
    	// for(i=0;i<links.length;i++){
    		// link={};
    		// for(j=0; j<links[i].label.length;j++){
    			// link.name=links[i].label[j].name;
    			// link.np=links[i].label[j].np;
    			// link.vocab=links[i].label[j].vocab;
    			// link.source=links[i].source;
    			// link.target=links[i].target;
    			// edges.push(link);
    			// link={};
    			// console.log(links[i].target);
    			// debugger;
    		// }
    	// }
    	// console.log(edges);
    	// debugger;
    	
    	drawGraph(graph, svg);
    });