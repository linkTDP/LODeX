function updateAttributeSelect(){
	$('#parListAttForm')
    .find('option')
    .remove()
    .end();
	$('#parListAttForm2')
    .find('option')
    .remove()
    .end();
	$.each(qo.getAttrPrameters(), function (index,value) {
	    $('#parListAttForm').append($('<option/>', { 
	        value: value,
	        text : value 
	    }));
	    $('#parListAttForm2').append($('<option/>', { 
	        value: value,
	        text : value 
	    }));
	});  
}

function updateClassSelect(){
	$('#parListClassForm')
    .find('option')
    .remove()
    .end();
	$.each(qo.getClassPrameters(), function (index,value) {
	    $('#parListClassForm').append($('<option/>', { 
	        value: value,
	        text : value 
	    }));
	});  
	
	$("#parListClassForm").prepend("<option value='' selected='selected'></option>");
	
	
	
//	$("#parListClassForm").val($("#parListClassForm option:first").val());
}

function updateOrderSelect(){
	$('#orderingSel')
    .find('option')
    .remove()
    .end();
	$.each(qo.getParOrd(), function (index,value) {
	    $('#orderingSel').append($('<option/>', { 
	        value: value,
	        text : value 
	    }));
	});  

//	$("#parListClassForm").val($("#parListClassForm option:first").val());
}

function updateOrderDelete(){
	$('#orderingDel')
    .find('option')
    .remove()
    .end();
	$.each(qo.retOrdPar(), function (index,value) {
	    $('#orderingDel').append($('<option/>', { 
	        value: value,
	        text : value 
	    }));
	});  

//	$("#parListClassForm").val($("#parListClassForm option:first").val());
}

function AddOrder(){
	var values = {};
	$.each($('#ordering').serializeArray(), function(i, field) {
	    values[field.name] = field.value;
	});
//	console.log(values)
	qo.addOrdCond(values.orderingSel,values.ordVerso)
	updateOrderSelect();
	updateOrderDelete();
	qo.setCodemQuery();
}

function RemoveOAll(){
	qo.removeAllO();
	updateOrderSelect();
	updateOrderDelete();
	qo.setCodemQuery();
}

function RemoveSelO(){
	var values = {};
	$.each($('#orderingRem').serializeArray(), function(i, field) {
	    values[field.name] = field.value;
	});
	
	qo.removeOrdByPar(values.orderingDel);
	updateOrderSelect();
	updateOrderDelete();
	qo.setCodemQuery();
}

function DeleteAllFilter(){
	qo.deleteAllFilter();
	qo.setCodemQuery();
}


function goToQuery(){
	   
	updateAttributeSelect();
	updateOrderSelect();
	updateClassSelect();
	if(curQCN.length>0){
		qo.setCodemQuery();
	}
//	testworkingQuery();
	
	document.getElementById('goToQue').click();
}

//var errorQuery = function(){console.log('maronna')}

function ChangeP(){
	var values = {};
	$.each($('#paging').serializeArray(), function(i, field) {
	    values[field.name] = field.value;
	});
	if(!isNaN(values.pagingSize)){
		qo.changePageSize(parseInt(values.pagingSize))
		
		qo.setCodemQuery();
		
	}
	$(function () {
		  $('#pagingSize').val("");
	});
}

function DisableP(){
	qo.setPagination();
	qo.setCodemQuery();
}


function testworkingQuery(){
	$('#countRes').empty();
	$('#countRes').css("color", "black");
	$('#countRes').append("getting count...");
	
	var stringQuery=qo.getCountQuery().join('\n');
	var Qcount = new sgvizler.Query();
	
	var 
	
	mySuccessFunc = function (datatable) {
    /* Do what you want with the datatable */
	updateCount(datatable.Nf[0].c[0].v);
	
  },
  myFailFunc = function (datatable) {
    /* Handle the failue */
	console.log(datatable)
  };
  

  Qcount.query(stringQuery)
  .getDataTable(mySuccessFunc, myFailFunc);
}

function updateCount(count){
	if(count !== undefined && count >0){
		$('#countRes').empty();
		$('#countRes').css("color", "black");
		$('#countRes').append(count+" records");
		$('#lunchQuery').disable(false);
	}else{
		$('#countRes').empty();
		$('#countRes').append("0 record. Change query!!");
		$('#countRes').css("color", "red");
//		$('#lunchQuery').disable(true);
	}
}

function lunchQuery(){
	var sparqlQueryString = editor.getDoc().getValue(),
    containerID = "resultViz",
    Q = new sgvizler.Query()

//	,
//	mySuccessFunc = function (datatable) {
//	      /* Do what you want with the datatable */
//		console.log(datatable)
//	    },
//	    myFailFunc = function (datatable) {
//	      /* Handle the failue */
//	    	console.log(datatable)
//	    };
	
	
//	var charType = $('#sgvzlr_optChart option:selected').val();
//	console.log(charType)
	
	
	// Note that default values may be set in the sgvizler object.
//	    try {
//	    	Q.onFail(errorQuery);
//	    	Q.addListener('onFail',errorQuery);
	    	Q.query(sparqlQueryString)
	    	.chartHeight(parseInt(height*0.80))
	    	.chartWidth(parseInt(trueW*0.99))
//	    	.chartFunction(charType) 
//	    	.getDataTable(mySuccessFunc, myFailFunc);
	        .draw(containerID);//.onFail(function(d){console.log(d)});
//	    }
//	    catch(err) {
//	    	window.alert(err.message);
//	    	console.log(err.message);
////	        document.getElementById("demo").innerHTML = err.message;
//	    }
}


function goToResults(){
	$('#nextPage').disable(false);
	lunchQuery();
	document.getElementById('goToRes').click();
}





function disableQueryButtons(){
	$('#pervPage').disable(true);
	$('#nextPage').disable(true);
	$('#AddFilter').disable(true);
	$('#ChangeO').disable(true);
	$('#DeleteA').disable(true);
//	$('#lunchQuery').disable(true);
	$('#ChangeOC').disable(true);
	$('#DeleteAC').disable(true);

}

function prevPage(){
	qo.prevPage();
	if (qo.getPage() == 1){
		$('#pervPage').disable(true);
	}
	qo.setCodemQuery();
	lunchQuery();
	
}

function nextPage(){
	qo.nextPage();
	$('#pervPage').disable(false);
	qo.setCodemQuery();
	lunchQuery();
}

function AddFilt(){
	var values = {};
	$.each($('#filter').serializeArray(), function(i, field) {
	    values[field.name] = field.value;
	});
	qo.addFiltCondToPar(values.parListAttForm,values.filtOp=="regex",values.expression.trim(),(values.filtOp=="regex")?undefined:values.filtOp)
	qo.setCodemQuery();
}

function DeleteAtt(){
	var values = {};
	$.each($('#attrForm').serializeArray(), function(i, field) {
	    values[field.name] = field.value;
	});
	qo.deleteAttribute(values.parListAttForm);
	
	var indexClas=getClasVizinxContainAttPar(values.parListAttForm)
	var indexAtt =getAttVizIndxByInxClasPar(indexClas,values.parListAttForm)
	curQCN[indexClas].attributes.splice(indexAtt,1)
	
	updateAttributeSelect();
	qo.setCodemQuery();
	
}

function getClasVizinxContainAttPar(par){
	return _.indexOf(_.map(curQCN,function(a){return _.some(a.attributes,function(b){return b.param==par})}),true)
}

function getAttVizIndxByInxClasPar(inx,par){
	return _.indexOf(_.map(curQCN[inx].attributes,function(a){return a.param}),par)
}

function ChangeOM(){
	var values = {};
	$.each($('#attrForm').serializeArray(), function(i, field) {
	    values[field.name] = field.value;
	});
	qo.changeMandatoryToAtt(values.parListAttForm);
	
	var indexClas=getClasVizinxContainAttPar(values.parListAttForm)
	var indexAtt =getAttVizIndxByInxClasPar(indexClas,values.parListAttForm)
	curQCN[indexClas].attributes[indexAtt].opt=!curQCN[indexClas].attributes[indexAtt].opt
	
	qo.setCodemQuery();
}


function DeleteClass(){
	var values = {};
	$.each($('#classForm').serializeArray(), function(i, field) {
	    values[field.name] = field.value;
	});
	values.parListClassForm=values.parListClassForm.trim()

	if (values.parListClassForm.trim().length > 1){
	qo.deleteClass(values.parListClassForm);
	
	curQCN.splice(_.indexOf(_.map(curQCN,function(a){return a.param}),values.parListClassForm),1)
	
	graph2.removeNode2(values.parListClassForm.substring(1))

	
//	_.indeOf(propEdge,_.find(propEdge))
	
	updateClassSelect();
	updateOrderSelect();
	qo.setCodemQuery();
}
}



$('#parListClassForm').change(function() {
	
	
	console.log($(this).val())
	if ($(this).val() != ' '){
		$('#ChangeOC').disable(false);
		if(qo.isNodeLeaf($(this).val())){
			$('#DeleteAC').disable(false);
		}else{
			$('#DeleteAC').disable(true);
		}
	}else{
		$('#ChangeOC').disable(true);
		$('#DeleteAC').disable(true);
	}
	
});


function ChangeOMC(){
	var values = {};
	$.each($('#classForm').serializeArray(), function(i, field) {
	    values[field.name] = field.value;
	});
	qo.changeMandatoryToClass(values.parListClassForm);
	var inx=getClasVizinxByPar(values.parListClassForm)
	curQCN[inx].opt=!curQCN[inx].opt
	
	qo.setCodemQuery();
}

function getClasVizinxByPar(par){
	return _.indexOf(_.map(curQCN,function(a){return a.param}),par)
}


// Utility **************************


var falsy = /^(?:f(?:alse)?|no?|0+)$/i;
Boolean.parse = function(val) { 
    return !falsy.test(val) && !!val;
};

jQuery.extend(
	    {
	        loadStyleSheet: function(file, type) {
	            $('<link>').attr('rel', 'stylesheet')
	                .attr('type', type)
	                .attr('href', file)
	                .appendTo('head');
	        }
	    }
	);

jQuery.fn.extend({
    disable: function(state) {
        return this.each(function() {
            this.disabled = state;
        });
    }
});

