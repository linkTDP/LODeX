function drawGraph(graph, svg){
    	//console.log(graph);
		var vocab=graph.vocab;
		
		
		for (a in vocab){
			color(vocab[a]);
		}
		// console.log(vocab[0]);
		var max_ni = graph.nodes[0].ni;
		var max_np = graph.links[0].np;
		
		
		
		
		var legend = svg.selectAll(".legend")
		.data(color.domain())
		.enter().append("g")
		.attr("class", "legend")
		.attr("transform", function(d, i) { return "translate(0," + i * 17 + ")"; });

// draw legend colored rectangles
	legend.append("rect")
			.attr("x", width - 15)
				.attr("width", 15)
			.attr("height", 15)
  			.style("fill", color);

// draw legend text
	legend.append("text")
	  		.attr("x", width - 21)
			.attr("y", 9)
			.attr("dy", ".35em")
			.style("text-anchor", "end")
			.style("font-family","Lato, sans-serif")
			.style("font-size", "14px")
			.style("font-weight", 900)
			.text(function(d) { return d;});
		
		
		
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
			.gravity(0.5).linkDistance([linkDistance])
			.charge(charge)
			.friction(0.4)
			.size([width, height])
			.start();
		
		
		var drag = force.drag()
	    .on("dragstart", dragstart);
	      
	      
		divTT = d3.select("#chart").append("div")   
			.attr("class", "tooltip")
			.style("position", "absolute")
			.style("top", 5)
			.style("left",5)
			// 	 .style("z-index",-1)
			.style("opacity", 1);
		
		var title = d3.select("#chart").append("div")
			.attr("class","titleEn")
			.attr("id","titleEndpoint")
			.style("position","absolute")
			.style("top", (height-50).toString()+'px')
			.style("left",'36vw')
// 			.style("z-index", -1)
			.style("opacity", 1)
			.text(graph.title);
		
//		var ancorPage2 = document.createElement('a');
//		ancorPage2.setAttribute('href',"#query");
//		ancorPage2.innerHTML = " V";

		//		console.log(ancorPage2)
		$("#titleEndpoint").append("<a id='goToQue' href='#query' ></a>");
		
		
		
		edgeLegend	= d3.select("#chart").append("div")   
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
		      .style("stroke-width", 1 )
		      .attr("x1", function(d) { return d.source.x; })
			  .attr("y1", function(d) { return d.source.y; })
		  	  .attr("x2", function(d) { return d.target.x; })
		  	  .attr("y2", function(d) { return d.target.y; })//;
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
//	    		console.log('autonode')
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
	      	.style("stroke",'black');
	      //.style("pointer-events", "none");
	      
	    var nodes = svg.selectAll("circle.node")
	      .data(graph.nodes)
	      .enter().append("svg:circle")
	      .attr("class", "node")
	      .attr("stroke", "black")
	      .attr("stroke-width", "1.5px")
	      .attr("r", function(d) { return (d.ni * 25 / max_ni)+5; }) //dimensione nodi
	      .style("fill", function(d) { return color(d.vocab); })
	      .on("dblclick", dblclick)
	      .on("click",nodeClick)
	      .call(drag)
	      .on("mouseover", nodeMouseOver);
	    
	    
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
			.style("font-weight", 500)
			.style("stroke","black")
			.attr("font-size", "15px")
			.attr("fill", "black")
	       .text(function(d){return d.name;});
	       
	    nodes.append("title")
			.text(function(d) { return d.fullName; });
		links.append("title")
			.text(function(d) { return d.name; });
			
		svg.style("opacity", 1e-6)
			.transition()
			.duration(1000)
			.style("opacity", 1);
			
		
	       
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
	    
	    function nodeClick(d){
//	    	console.log(d) //oggetto dati
//	    	console.log(this) //elemento svg
	    	
	    }
	    
	    function dblclick(d) {
	    	  d3.select(this).classed("fixed", d.fixed = false).attr("stroke-width","1.5px");
	    	}

	    function dragstart(d) {
	    	  d3.select(this).classed("fixed", d.fixed = true).attr("stroke-width","3px");
	    	}
	    
	    
	    
	    
	    
	    
    }

function addClass(){
	var idClass=document.getElementById('addClassHidden').value;
	var clas=_.find(ike.nodes,function(nod){return nod.index == idClass})
	console.log(clas);
	var curClasNode = new ClassNode(clas.fullName,clas.name,true);
	
	qo.addNode(curClasNode);
	curQCN.push({index:qo.getIndex(),nodeId:idClass,name:clas.name,attributes:new Array(),opt:false,param:qo.getCurClasses()[0].getParameter(),property:null,qoQI:-1});
	console.log(curQCN);
	console.log(qo);
	nodeMouseOver(clas,qo.getCurClasses()[0].getParameter());
	graph2.addNode2(clas.name,color(clas.vocab));
//	console.log(clas)
	
}


function addAtt(index,name,property,optional){
	var paramId=qo.addAttributeToNode(index,name,property,optional);
	curQCN[index].attributes.push({opt:optional,name:name,param:paramId,fullName:property});
	var idClass = _.find(curQCN,function(a){return a.index==index}).nodeId;
	nodeMouseOver(_.find(ike.nodes,function(nod){return nod.index == idClass}),curQCN[index].param);
	$('#AddFilter').disable(false);
	$('#ChangeO').disable(false);
	$('#DeleteA').disable(false);
//	console.log(index)
//	console.log(name)
//	console.log(property)
//	console.log(optional)
}


function addLiNo(URI,name,parEnabl,property,after,optional,index,nodInd,otherInx){
//	console.log(index)
//	console.log(nodInd)
//	console.log(otherInx)
	var par=qo.addLinkedNode(URI,name,parEnabl,property,Boolean.parse(after),Boolean.parse(optional),index);
	curQCN.push({param:par,index:qo.getIndex(),nodeId:nodInd,name:name,attributes:new Array(),opt:Boolean.parse(optional),property:property,othInx:otherInx,qoQI:parseInt(index),othParam:qo.getCurClasses()[index].getParameter()});
	
	var idClass = _.find(curQCN,function(a){return a.param==par}).nodeId;
	nodeMouseOver(_.find(ike.nodes,function(nod){return nod.index == idClass}),par);
	
	propEdge.push({par1:par,par2:qo.getCurClasses()[index].getParameter(),propertu:property,ind1:otherInx,ind2:nodInd})
	
	graph2.addNode2(par.substr(1),color(_.find(ike.nodes,function(nod){return nod.index == nodInd}).vocab));
	graph2.addLink2(_.find(curQCN,function(a){return a.index==index}).param.substr(1), par.substr(1));
}



function clearQuery(){
	$("#graph2").html("<div id='textGraph2'>Query<input id='clearQ' type='button' onclick='clearQuery()' value='Clear'><input class='buttonLod' id='goToQ' type='button' onclick='goToQuery()' value='Generate'></div>");
	graph2 = new myGraph("#graph2");
	disableQueryButtons();
	propEdge=new Array();
	qo = new QuerOrchestrator();
	curQCN = new Array();
}


function nodeMouseOver(d,param) {      
    divTT.transition()        
        .duration(1000)      
        .style("opacity", 1);
    
    //attributes
    
//    console.log(param)
    
    s='<div class="attrTitle">Attributes</div>'
    s+='<hr align=�left� noshade  style="height:2px;color:#000000;background-color:#000000;">'
    s+='<div id=attributes class=attributes>'
    s+="<table>";
//     console.log(d.att)

//	for (var j = 0; j < d.att.length; j++)	ne voglio 12


//		maxAtt = 12;
//		if (d.att.length < 12){
//			maxAtt=d.att.length;
//		}
    for (var j = 0; j < d.att.length; j++){ 

    	
    	s+="<tr>";
//    	console.log(d.index == curQCN.nodeId)
//    	console.log(d.index )
//    	console.log(curQCN.nodeId)
//    	console.log(_.some(curQCN,function(a){return d.index == a.nodeId}))
    	var test = _.find(curQCN,function(a){return d.index == a.nodeId });
    	if (test !== undefined){    		
    		var tmpAtty=_.find(test.attributes,function(a){return a.fullName == d.att[j].fullName});
    		if ( tmpAtty !== undefined){
    			
        		s+="<td>";
//        		console.log(tmpAtty.opt)
        		s+="<b>"+ ((tmpAtty.opt)? "O":"M")+"</b>";
        		s+="</td>";
        		s+="<td>";
        		s+="</td>";
    		
    		}else{
	    		s+="<td>";
	    		s+='<input id="addAttButton" type="button" value="M" onclick="addAtt(\''+_.find(curQCN,function(a){return a.nodeId==d.index}).index+'\',\''+d.att[j].p+'\',\''+d.att[j].fullName+'\','+false+');" />';
	    		s+="</td>";
	    		s+="<td>";
	    		s+='<input id="addAttButton" type="button" value="O" onclick="addAtt(\''+_.find(curQCN,function(a){return a.nodeId==d.index}).index+'\',\''+d.att[j].p+'\',\''+d.att[j].fullName+'\','+true+');" />';
	    		s+="</td>";
    		}
    	}
    	s+="<td>";
    	s+='<svg width="8" height="8"> <rect width="8" height="8" style="fill:'+color(d.att[j].vocab)+';" /></svg></td>';
//     	console.log('<svg width="10" height="10"> <rect width="10" height="10" style="fill:'+d.att[j].vocab+';" /></svg>')
    	s+= '<td>'+d.att[j].p;
    	s+="</td>";
    	s+="<td>";
    	s+=d.att[j].n;
    	s+="</td>";
    	
    	s += "</tr>";
//    	console.log(color(d.att[j].vocab));
    }
    
    
    
    s+="</table></div>";
//    console.log(d);
    t='<table class="title"><tr><td>'+d.name+'</td><td>'+d.ni+'<span class="instances"> instances</span></td>';
    if(qo.getIndex() < 0){
    	t+='<td><input type="hidden" value='+d.index+' id="addClassHidden" /><input class="buttonLodblack" id="addClassButton" type="button" value="Add Class" onclick="addClass();" /></td><td><img src="static/arrow.jpg" alt="" height=30 width=30< valign="middle"></img></td></tr>'
    }
    
    if('cluster' in d ){
    	t+='<table><div style="margin-top: 5px; margin-bottom: 5px;">';
    	
    	for (i = 0; i < d.cluster.length; i++){
    		console.log(d.cluster[i].cluster.length)
    		t+='<span class="clusters">'
    		for (j=0;j<d.cluster[i].cluster.length;j++){
    			
    			if(d.cluster[i].cluster[j].uri!=d.fullName){
    				t+='<svg width="8" height="8"> <rect width="8" height="8" style="fill:'+color(d.cluster[i].cluster[j].vocab)+';" /></svg>'
    				t+=''+d.cluster[i].cluster[j].name+''
    			}
    			
    		}
    		t+=' '+(Math.floor(( d.cluster[i].n/ d.ni) * 100)>100? 96: Math.floor(( d.cluster[i].n/ d.ni) * 100))+'%'
//    		t+=d.cluster[i].n
    		t+='</span>'
    	}
    	t+='</div></table>'
//    	t+='</td></tr></table>'
    }else{
    	t+='<table><div style="margin-top: 5px; margin-bottom: 5px;"></div></table>'
    }
    
    
    t+='</table><div class="propTit">Properties</div><hr align=left noshade width=200 style="height:2px;color:#000000;background-color:#000000;">'
    entranti=[]
    uscenti=[]
    edges=ike.links
//    console.log(edges);
    for(i=0; i<edges.length;i++){
    	if(edges[i].source.index == d.index){
    		for(j=0;j<edges[i].label.length;j++){
    			tmp=edges[i].label[j]
    			tmp.target=edges[i].target.name
    			tmp.ClassfullName=edges[i].target.fullName
    			tmp.index=edges[i].target.index
    			uscenti.push(tmp)	
    		}
    	}
    	else{
    		if(edges[i].target.index == d.index){
    			for(j=0;j<edges[i].label.length;j++){
    				tmp=edges[i].label[j]
    				tmp.source=edges[i].source.name
    				tmp.ClassfullName=edges[i].source.fullName
    				tmp.index=edges[i].source.index
        			entranti.push(tmp)	
        		}
    		}
    	}
    }
    entranti.sort(function (a, b) {
    	return  b.np - a.np;
    });
    uscenti.sort(function (a, b) {
    	return  b.np - a.np;
    });
    
//    console.log(entranti)
    
//     if ((entranti.length + uscenti.length) > 12)
//     {
//     	toRemove=(entranti.length + uscenti.length) -12;
//     	for ( l = 0; l<=toRemove; l++){
//     		if (entranti[entranti.length-1].np > uscenti[uscenti.length-1].np){
//     			//console.log("rmove - > "+uscenti[uscenti.length-1].np);
//     			uscenti.pop();
    			
//     		}else{
//     			//console.log("rmove - > "+entranti[entranti.length-1].np);
//     			entranti.pop()
//     		}
//     	}
//     }
    var curNnodee;
//    console.log(param)
    if (_.isString(param)){
	    curNnodee=_.find(curQCN,function(a){return a.param==param})
    }else{
    	curNnodee=_.find(curQCN,function(a){return a.nodeId==param})
    }
    if (curNnodee !== undefined){
//	    console.log(curNnodee)
	    var connected=[]
	    for (i=0;i<curQCN.length;i++){
	    	if(curQCN[i].othParam==curNnodee.param){
	    		connected.push({nodeId:curQCN[i].nodeId,othInx:curQCN[i].othInx,property:curQCN[i].property,opt:curQCN[i].opt})
//	    		connected.push({nodeId:curQCN[i].nodeId,othInx:curNnodee.nodeId,property:curNnodee.property,opt:curNnodee.opt})
	    	}
	    	if(curQCN[i].param==curNnodee.othParam){
//	    		console.log(curNnodee.opt)
//	    		console.log(curQCN[i].opt)
	    		connected.push({nodeId:curNnodee.nodeId,othInx:curNnodee.othInx,property:curNnodee.property,opt:curNnodee.opt})
//		    	connected.push({nodeId:curQCN[i].othInx,othInx:curQCN[i].nodeId,property:curQCN[i].property,opt:curNnodee.opt})
	    	}
	    }
    }
	    
//	    var connected=_.compact(_.map(curQCN,function(a){if(a.index==curNnodee.qoQI)return a;}))
//        connected=connected.concat(_.compact(_.map(curQCN,function(a){if(a.qoQI==curNnodee.index){
//        var b=_.clone( a );
//        b.property=curNnodee.property;
//        return b;}})));
//	    console.log(connected)
    
    t+="<div id=properties class=properties><table>"
    
    if(curNnodee!== undefined){
    	t+='<tr>'
    		t+='Query node name:'+curNnodee.param.substr(1)
    	t+='</tr>'
    }
    
    if(entranti.length > 0){
    	for(i=0; i<entranti.length;i++){
    		t+='<tr>';
//    		var test = _.find(curQCN,function(a){return d.index == a.nodeId});
    		if ( curNnodee !== undefined ){
//    			console.log(entranti[i].index)
//    			console.log(entranti[i].fullName)
//    			var tmpProppy=_.find(curQCN,function(a){return  (a.nodeId == entranti[i].index || a.othInx == entranti[i].index) && a.property == entranti[i].fullName});
    			var tmpProppy=_.find(connected,function(a){return (parseInt(a.nodeId) == entranti[i].index || parseInt(a.othInx) == entranti[i].index) && a.property == entranti[i].fullName})
    			if ( tmpProppy === undefined){	
	    			t+="<td>";
	        		t+='<input id="addLikNodeButton" type="button" value="M" onclick="addLiNo(\''+entranti[i].ClassfullName+'\',\''+entranti[i].source+'\',\''+false+'\',\''+entranti[i].fullName+'\',\''+true+'\',\''+false+'\',\''+curNnodee.index+'\',\''+entranti[i].index+'\',\''+d.index+'\');" />';
	        		t+="</td>";
	        		t+="<td>";
	        		t+='<input id="addLikNodeButton" type="button" value="O" onclick="addLiNo(\''+entranti[i].ClassfullName+'\',\''+entranti[i].source+'\',\''+false+'\',\''+entranti[i].fullName+'\',\''+true+'\',\''+true+'\',\''+curNnodee.index+'\',\''+entranti[i].index+'\',\''+d.index+'\');" />';
	        		t+="</td>";
	    		}else{
	    			t+="<td>";
	        		t+="<b>"+((tmpProppy.opt)?"O":"M")+"</b>";
	        		t+="</td>";
	        		t+="<td>";
	        		t+="</td>";
	    		}
    		}
    		t+='<td><svg width="8" height="8"> <rect width="8" height="8" style="fill:'+color(entranti[i].vocab)+';" /></svg></td>'
    		t+='<td>'+entranti[i].name+'</td>'
    		t+='<td><div title="Code: 0xe800" class="the-icons"><i class="icon-left-open-outline"></i></div></td>';
    		tmp=entranti[i].np/d.ni
    		t+='<td>'+entranti[i].source+'</td>'
    		t+='<td>'+tmp.toFixed(2)+'</td>'
    		t+='</tr>'
    		
    		
    		
//    		t+='<td><svg width="8" height="8"> <rect width="8" height="8" style="fill:'+color(entranti[i].vocab)+';" /></svg></td>'
//    		t+='<td><a href="/lodex2/intensional?s='+d.name+'&p='+entranti[i].name+'&o='+entranti[i].source+'&id='+ike.id+'" target="_blank">'+entranti[i].name+'</a></td>'
//    		t+='<td><a href="/lodex2/intensional?s='+d.name+'&p='+entranti[i].name+'&o='+entranti[i].source+'&id='+ike.id+'" target="_blank"><div title="Code: 0xe800" class="the-icons"><i class="icon-left-open-outline"></i></div></a></td>';
//    		tmp=entranti[i].np/d.ni
//    		t+='<td><a href="/lodex2/intensional?s='+d.name+'&p='+entranti[i].name+'&o='+entranti[i].source+'&id='+ike.id+'" target="_blank">'+entranti[i].source+'</a></td>'
//    		t+='<td><a href="/lodex2/intensional?s='+d.name+'&p='+entranti[i].name+'&o='+entranti[i].source+'&id='+ike.id+'" target="_blank">'+tmp.toFixed(2)+'</a></td>'
//    		t+='</tr>'
    	}
    }
    if(uscenti.length > 0){
    	for(i=0; i<uscenti.length;i++){
    		t+='<tr>';
//    		var tmpProppy = _.find(curQCN,function(a){return d.index == a.nodeId});
    		if ( curNnodee !== undefined ){
//    		if ( tmpProppy !== undefined ){
    			
//    			var tmpProppy=_.find(curQCN,function(a){return (a.nodeId == uscenti[i].index || a.othInx == uscenti[i].index)&& a.property== uscenti[i].fullName});
    			
    			
    			
    			
//    			var tmpProppy=_.find(connected,function(a){return (a.nodeId == uscenti[i].index || a.othInx == uscenti[i].index)&& a.property== uscenti[i].fullName})
    			
    			var tmpProppy=_.find(connected,function(a){return (a.nodeId == uscenti[i].index || a.othInx == uscenti[i].index)&& a.property== uscenti[i].fullName})
    			
    			
    			if ( tmpProppy === undefined){			
        		t+="<td>";
        		t+='<input id="addLikNodeButton" type="button" value="M" onclick="addLiNo(\''+uscenti[i].ClassfullName+'\',\''+uscenti[i].target+'\',\''+false+'\',\''+uscenti[i].fullName+'\',\''+false+'\',\''+false+'\',\''+curNnodee.index+'\',\''+uscenti[i].index+'\',\''+d.index+'\');" />';
        		t+="</td>";
        		t+="<td>";
        		t+='<input id="addLikNodeButton" type="button" value="O" onclick="addLiNo(\''+uscenti[i].ClassfullName+'\',\''+uscenti[i].target+'\',\''+false+'\',\''+uscenti[i].fullName+'\',\''+false+'\',\''+true+'\',\''+curNnodee.index+'\',\''+uscenti[i].index+'\',\''+d.index+'\');" />';
        		t+="</td>";
    		}else{
    			t+="<td>";
        		t+="<b>"+((tmpProppy.opt)?"O":"M")+"</b>";
        		t+="</td>";
        		t+="<td>";
        		t+="</td>";
    		}
    		}
    		t+='<td><svg width="8" height="8"> <rect width="8" height="8" style="fill:'+color(uscenti[i].vocab)+';" /></svg></td>'
    		t+='<td>'+uscenti[i].name+'</td>'
    		t+='<td><div title="Code: 0xe800" class="the-icons"><i class="icon-right-open-outline"></i></div></td>';
    		tmp=uscenti[i].np/d.ni
    		t+='<td>'+uscenti[i].target+'</td>'
    		t+='<td>'+tmp.toFixed(2)+'</td>'
    		t+='</tr>'
    		
    		
//    		t+='<td><svg width="8" height="8"> <rect width="8" height="8" style="fill:'+color(uscenti[i].vocab)+';" /></svg></td>'
//    		t+='<td><a href="/lodex2/intensional?s='+d.name+'&p='+uscenti[i].name+'&o='+uscenti[i].target+'&id='+ike.id+'" target="_blank">'+uscenti[i].name+'</a></td>'
//    		t+='<td><a href="/lodex2/intensional?s='+d.name+'&p='+uscenti[i].name+'&o='+uscenti[i].target+'&id='+ike.id+'" target="_blank"><div title="Code: 0xe800" class="the-icons"><i class="icon-right-open-outline"></i></div></a></td>';
//    		tmp=uscenti[i].np/d.ni
//    		t+='<td><a href="/lodex2/intensional?s='+d.name+'&p='+uscenti[i].name+'&o='+uscenti[i].target+'&id='+ike.id+'" target="_blank">'+uscenti[i].target+'</a></td>'
//    		t+='<td><a href="/lodex2/intensional?s='+d.name+'&p='+uscenti[i].name+'&o='+uscenti[i].target+'&id='+ike.id+'" target="_blank">'+tmp.toFixed(2)+'</a></td>'
//    		t+='</tr>'
    	}
    }
    t+='</table></div>'
//    console.log('entranti');
//    console.log(entranti);

     
    divTT.html(s)  
        .style("left", "1px" )    //(d3.event.pageX)
         .style("bottom", "1px" )
          .style("font-family","Lato, sans-serif")
          .style("font-size", "12px")
          .style("font-weight",900);
    
     $('#attributes').perfectScrollbar();
          
     edgeLegend.html(t)  
        .style("left", "1px" )    //(d3.event.pageX)
         .style("top", "1px" )
          .style("font-family","Lato, sans-serif")
          .style("font-size", "12px")
          .style("font-weight",900);
     
     $('#properties').perfectScrollbar();
     
     // opacize links
     svg.selectAll('.link')
     .style('opacity', function(o) {
         if (o.source === d || o.target === d) 
//             console.log(o, d);
         return o.source === d || o.target === d ? 1 : 0.3;
     })
     .style("stroke-width", function(o) {
         if (o.source === d || o.target === d) 
//           console.log(o, d);
       return o.source === d || o.target === d ? 3 : 1;
   });
     
     

     svg.selectAll('.node')
     .style('opacity', function(ld) {

         if (ld.fullName == d.fullName) return 1;
//			console.log(ld)
//			console.log(d)
         if (_.some(ike.links,function(el){
//         	 console.log(el.target);
        	 return (el.source===d && el.target===ld)||(el.source===ld && el.target===d);
         })) {
         return 1;
         }	
         else return .4;
     });
     

     
     

     
     
     svg.selectAll('.nodelabel')
     .style('opacity', function(ld) {
//		console.log(d)
//		console.log(ld)
         if (ld.fullName == d.fullName) return 1;
//			console.log(ld)
//			console.log(d)
         if (_.some(ike.links,function(el){
//         	 console.log(el.target);
        	 return (el.source===d && el.target===ld)||(el.source===ld && el.target===d);
         })) {
         return 1;
         }	
         else return .4;
     }).style('font-weight', function(ld) { if (ld.name == d.name) return 900;
		//		console.log(ld)
		//		console.log(d)
		if (_.some(ike.links,function(el){
		//	 console.log(el.target);
			 return (el.source===d && el.target===ld)||(el.source===ld && el.target===d);
		})) {
		return 900;
		}	
		else return 500;});
     
     
     
	}


