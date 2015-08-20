var FilterCond = Stapes.subclass({
    constructor : function(param,regex,expression,operator){
    	this.param=param;
    	this.regex=regex;
    	this.expression=expression;
    	this.operator=operator;
    	},
    getQueryFilt : function(){
    	var tmpFitQ="FILTER "
    	if(this.regex){
    		tmpFitQ=tmpFitQ+' REGEX('+this.param+', "'+this.expression+'" ,"i"). ';
    	}else{
    		tmpFitQ=tmpFitQ+' ('+this.param+' '+this.operator+' '+this.expression+' ). ';
    	}
    	return tmpFitQ;
    }
    });



var AttributeOfAClass = Stapes.subclass({
    constructor : function(name,property,optional,instance,tmpPaAt) {
        this.name = name;
        this.property = property;
        this.parameter = tmpPaAt;
        this.instance = instance;
        this.optional = optional;
        this.filters = new Array();
    },
    getFiltQuer : function(){
    	var queryRes="";
    	this.tmpArrfilt =_.map(this.filters,function(a){return a.getQueryFilt()});
    	queryRes=queryRes+this.tmpArrfilt.join('\n');
    	return queryRes;
    },
    addFilter : function(regex,expression,operator){
    	this.filters.push(new FilterCond(this.parameter,regex,expression,operator))
    },
    getName : function() {
        return this.name;
    },
    getParameter : function() {
        return this.parameter;
    },
    getProperty : function() {
        return this.property;
    },
    isFlterCond :function(){
    	return this.filters.length > 0;
    },
    getQueryPath : function() {
    	this.queryPathAttr=" ";
    	if (this.optional){
    		this.queryPathAttr=this.queryPathAttr+" OPTIONAL { "+this.instance+" <"+this.property+"> "+this.parameter+" ."
    		if (this.isFlterCond()){
    			this.queryPathAttr=this.queryPathAttr+'\n\t'+this.getFiltQuer()+" ";
    		}
    		this.queryPathAttr=this.queryPathAttr+" }";
    	}else{
    		this.queryPathAttr=this.queryPathAttr+this.instance+" <"+this.property+"> "+this.parameter+" . ";
    	}
    	return this.queryPathAttr;
    },
    deleteAllFilter : function(){
    	this.filters=new Array();
    }
});

var ClassNode = Stapes.subclass({
    constructor : function(URI,name,parEnabl) {
        this.URI = URI;
        this.name = name;
        this.parameter = '?'+name.replace('-','');
        this.enableParInSel=parEnabl;
        this.attributes=new Array();
        this.optional = false;
    },
    isFilterInAttributes:function(){
    	return _.some(this.attributes,function(a){return (a.isFlterCond() && !a.optional)})
    },
    getnotOptAtr : function(){
    	return _.filter(this.attributes,function(a){return !a.optional})
    },
    getName : function() {
        return this.name;
    },
    getURI : function() {
        return this.URI;
    },
    getParameter : function(){
    	return this.parameter;
    },
    getParameters : function() {
        return this.parameter+' '+this.getAttributesParameters();
    },
    getAttributesParameters : function() {
    	return _.map(this.attributes,function(a){return a.getParameter()}).join(' ')
    },
    getAttParList :function(){
    	return _.map(this.attributes,function(a){return a.getParameter()})
    },
    getAllParList :function(){
    	return _.map(this.attributes,function(a){return a.getParameter()}).concat(this.parameter)
    },
    isEnablePar : function(){
    	return this.enableParInSel;
    },
    getQueryPath : function() {
    	this.queryRes=this.parameter+' a <'+this.URI+'> .';
    	if(this.attributes.length>0){
    		this.queryRes=this.queryRes+'\n';
	    	var trasf = function(a){return a.getQueryPath(this.parameter)};
	    	this.tmpArrAtt=_.map(this.attributes,trasf);
	    	this.queryRes=this.queryRes+this.tmpArrAtt.join('\n');
//	    	console.log(this.isFilterInAttributes())
			if (this.isFilterInAttributes()){
//				console.log('-------------')
//				console.log(_.map(this.getnotOptAtr(),function(a){return a.getFiltQuer()}))
				this.queryRes=this.queryRes+'\n'+(_.compact(_.map(this.getnotOptAtr(),function(a){return a.getFiltQuer()}))).join('\n');
			}
	    	
    	}
    	return this.queryRes;
	    	
    },
    addAttributes : function(name,property,optional,tmpAtt) {
    	this.tmpAtt=new AttributeOfAClass(name,property,optional,this.parameter,tmpAtt);
    	this.attributes.push(this.tmpAtt);
    },
    getInxAttrByParam : function(param){
    	return _.indexOf(_.map(this.attributes,function(a){return a.parameter}),param);
    },
    addFiltCond:function(param,regex,expression,operator){
    	var ind=this.getInxAttrByParam(param);
    	this.attributes[ind].addFilter(regex,expression,operator);
    },
    removeAttributeByParam : function(param){
    	var ind=this.getInxAttrByParam(param);
    	this.attributes.splice(ind,1);
    },
    changeMandatoryAtt : function(param){
    	var ind=this.getInxAttrByParam(param);
    	this.attributes[ind].optional=!this.attributes[ind].optional;
    },
    isOptional : function(){
    	return this.optional;
    },
    deleteAllFilter : function(){
    	_.each(this.attributes,function(a){a.deleteAllFilter()})
    }
});

var LinkedClassNode = ClassNode.subclass({
	constructor : function(URI,name,parEnabl,property,after,optional,linkPar) {
        this.URI = URI;
        this.name = name;
        this.parameter = name;
        this.enableParInSel=parEnabl;
        this.attributes=new Array();
        this.property=property;
        this.after=after;
        this.optional=optional;
        this.linkPar=linkPar;
    },
    
    getQueryPath : function() {
    	this.queryPathAttr=" ";
    	if (this.optional){
    		this.queryPathAttr=this.queryPathAttr+" OPTIONAL { ";
    	}
    	this.queryPathAttr=this.queryPathAttr+LinkedClassNode.parent.getQueryPath.apply(this,arguments)+'\n';
    	console.log(this.after)
    	if (!this.after){
    		this.queryPathAttr=this.queryPathAttr+' '+this.linkPar+' <'+this.property+'> '+this.parameter+' .';
    	}else{
    		this.queryPathAttr=this.queryPathAttr+' '+this.parameter+' <'+this.property+'> '+this.linkPar+' .';
    	}
    	if (this.optional){
    		if (this.isFilterInAttributes()){
    			this.queryPathAttr=this.queryPathAttr+'\n'+(_.compact(_.map(this.getnotOptAtr(),function(a){return a.getFiltQuer()}))).join('\n');
    		}
    		this.queryPathAttr=this.queryPathAttr+" } ";
    	}
    	return this.queryPathAttr;
    },
    getSimQueryPath : function() {
    	this.queryPathAttr=" ";
    	this.queryPathAttr=this.queryPathAttr+LinkedClassNode.parent.getQueryPath.apply(this,arguments)+'\n';
//    	console.log(this.after)
    	if (!this.after){
    		this.queryPathAttr=this.queryPathAttr+' '+this.linkPar+' <'+this.property+'> '+this.parameter+' .';
    	}else{
    		this.queryPathAttr=this.queryPathAttr+' '+this.parameter+' <'+this.property+'> '+this.linkPar+' .';
    	}

    	return this.queryPathAttr;
    },
    
    getLinkPar : function(){
    	return this.linkPar
    }
});


var QuerOrchestrator = Stapes.subclass({
	constructor : function() {
		this.classNodes = new Array();
		this.index=-1;
        this.page = 1;
        this.nForP = 50;
        this.paginationEnable=true;
        this.order=new Array();
    },
    changeMandatoryToAtt: function(param){
    	var ind=this.getClasInxByAttPar(param);
    	this.classNodes[ind].changeMandatoryAtt(param);
    },
    deleteAttribute : function(param){
    	var ind=this.getClasInxByAttPar(param);
    	this.classNodes[ind].removeAttributeByParam(param);
    },
    getRemainingFiltCond : function(){
    	return _.flatten(_.map(_.filter(this.classNodes,function(c){return !c.optional && c.isFilterInAttributes()}),function(c){return _.compact(_.map(c.getnotOptAtr(),function(a){return a.getFiltQuer()}))})).join('\n')
    },
    isFiltRemCond : function(){
    	return _.some(this.classNodes,function(c){return !c.optional && c.isFilterInAttributes()})
    },
    getClasInxByAttPar: function(param){
    	return _.indexOf(_.map(this.classNodes,function(c){return _.some(c.getAttParList(),function(a){console.log(a);return a==param})}),true);
    },
    addFiltCondToPar:function(parName,regex,expression,operator){
    	var ind=this.getClasInxByAttPar(parName);
    	this.classNodes[ind].addFiltCond(parName,regex,expression,operator);
    },
    nextPage : function(){
    	this.page+=1;
    },
    prevPage : function(){
    	this.page-=1;
    },
    addNode : function(node){
    	
    	//controllare com'è il nuovo nodo da aggiungere?
    	this.classNodes.push(node);
    	this.index = this.classNodes.length - 1;
    },
    addLinkedNode : function(URI,name,parEnabl,property,after,optional,index){
    	var tmpPaAt='?'+name.replace('-','');
    	count=0
    	while(_.some(this.getParList(),function(a){return a==tmpPaAt+((count==0)?'':count)})){
    		count++
    	}
    	tmpPaAt=tmpPaAt+((count==0)?'':count)
    	
    	this.classNodes.push(new LinkedClassNode(URI,tmpPaAt,parEnabl,property,after,optional,this.classNodes[index].getParameter()));
    	this.index = this.classNodes.length - 1;
    	return this.classNodes[this.index].getParameter()
    },
    addAttributeToNode : function(index,name,property,optional){
    	var tmpPaAt='?'+name.replace('-','');
//    	console.log(name)
    	count=0
    	while(_.some(this.getAttrPrameters(),function(a){return a==tmpPaAt+((count==0)?'':count)})){
    		count++
    	}
    	tmpPaAt=tmpPaAt+((count==0)?'':count)
//    	if (_.some(this.getParList(),function(a){return a==tmpPaAt})){
//    		tmpPaAt=tmpPaAt+'1'
//    	}

    	this.classNodes[index].addAttributes(name,property,optional,tmpPaAt);
    	return tmpPaAt;
    	
    },
    getParOrd : function(){
    	var ordPar = this.getAttrPrameters().concat(_.map(this.classNodes,function(a){return a.getParameter()}))
//    	console.log(ordPar)
////    	var minus=
//    	console.log(_.without(ordPar,_.map(this.order,function(a){return a.param})))
    	return _.difference(ordPar,_.map(this.order,function(a){return a.param}))
    },
    getParameters : function(){
    	return _.compact(_.map(this.classNodes,function(nod){
    		if(nod.isEnablePar())
    		{return nod.getParameters()}}
    		));
    },
    getParList : function(){
    	
    	return _.flatten(_.map(this.classNodes,function(nod){ return nod.getAllParList()}));
    },
    getAttrPrameters : function(){
    	return _.flatten(_.map(this.classNodes,function(nod){ return nod.getAttParList()}));
    	
    },
    getClassPrameters : function(){
    	console.log(_.map(_.rest(this.classNodes),function(nod){ return nod.getParameter()}))
    	return _.map(_.rest(this.classNodes),function(nod){ return nod.getParameter()});
    	
    },
    getQueryBody : function(){
    	this.queryStringBodyLines=new Array();
    	this.queryStringBodyLines.push('WHERE {');
//    	this.queryStringBodyLines=this.queryStringBodyLines.concat(_.map(this.classNodes,function(nod){ return nod.getQueryPath()}));

    	this.queryStringBodyLines=this.queryStringBodyLines.concat(this.traslateChildsQuery());
  //    	if(this.isFiltRemCond()){
//    		console.log(this.getRemainingFiltCond())
//    		this.queryStringBodyLines.push(this.getRemainingFiltCond());
//    	}
    	this.queryStringBodyLines.push('}');
    	return this.queryStringBodyLines;
    	
    },
    getCountQuery :function(){
    	var queryCount= new Array();
    	queryCount.push('SELECT COUNT(*)');
    	queryCount=queryCount.concat(this.getQueryBody());
    	return queryCount;
    },
    getQuery : function(){
    	this.tmpPar = this.getParameters();
    	this.queryStringLines=new Array();
    	this.queryStringLines.push('SELECT '+this.tmpPar.join(' '));
    	
//    	this.queryStringLines=this.queryStringLines.concat(this.getQueryBody());
    	this.queryStringLines=this.queryStringLines.concat(this.getQueryBody());
    	if(this.order.length >0){
    		var OrderLine="ORDER BY "
    		for(u=0;u<this.order.length;u++){
    			if(this.order[u].ord == "DESC"){
    				OrderLine=OrderLine+" DESC("+this.order[u].param+") ";
    			}else{
    				OrderLine=OrderLine+" "+this.order[u].param+" "
    			}
    		}
    		this.queryStringLines.push(OrderLine);
    	}
    	if(this.paginationEnable){
	    	if (this.page == 1){
	    		this.queryStringLines.push('LIMIT '+this.nForP);
	    	}else{
	    		this.queryStringLines.push('LIMIT '+(this.nForP));
	    		this.queryStringLines.push('OFFSET '+(this.nForP*(this.page-1)));
	    	}
    	}
    	return this.queryStringLines;
    },
    
    setCodemQuery : function(){
//    	console.log(editor);
    	editor.setValue(this.getQuery().join('\n'));
    	testworkingQuery();
//    	editor.swapDoc(CodeMirror.Doc(this.getQuery().join('\n')),"application/x-sparql-query");
//    	editor.getDoc().markClean();
    },
    getIndex : function(){
    	return this.index;
    },
    getPage : function(){
    	return this.page;
    },
    getClassInxByClassParam : function(param){
    	return _.indexOf(_.map(this.classNodes,function(c){return c.parameter}),param)
    },
    deleteClass: function(param){
    	var ind=this.getClassInxByClassParam(param);
    	this.classNodes.splice(ind,1);
    },
    changeMandatoryToClass : function(param){
    	var ind=this.getClassInxByClassParam(param);
    	this.classNodes[ind].optional=!this.classNodes[ind].optional
    },
    isNodeLeaf : function(param){
//    	var inx=getClassInxByClassParam(param);
    	return !_.some(_.rest(this.classNodes),function(a){return a.getLinkPar()==param})
    },
    getCurClasses : function(){
    	return this.classNodes;
    },
    getChilds : function(index){
    	var childs=new Array()
    	var curNo = _.find(curQCN,function(a){return a.index==index})
    	var lev1Childs = _.compact(_.map(curQCN,function(a){if(a.qoQI==curNo.index)return a}))
    	console.log(lev1Childs)
    	childs=childs.concat(lev1Childs)
    	for (i=0;i<lev1Childs.length;i++){
    		if(!this.isNodeLeaf(lev1Childs[i].param)){
    			childs=childs.concat(this.getChilds(lev1Childs[i].index))
    		}
    	}
//    	_.each(lev1Childs,function(a){if(!this.isNodeLeaf(a.param))childs.concat(this.getChilds(a.index))})
    	return childs
    	
    },
    getLevel1Child :function(index){
    	var curNo = _.find(curQCN,function(a){return a.index==index})
    	var lev1Childs = _.compact(_.map(curQCN,function(a){if(a.qoQI==curNo.index)return a.index}))
    	return lev1Childs;
    },
    traslateChildsQuery :function(childs){
    	var quer=""
    	if (childs === undefined){
    		quer=quer+this.classNodes[0].getQueryPath()
    		console.log('ok')
    		quer=quer+this.traslateChildsQuery(this.getLevel1Child(0))
    		
    		
    	}else{
    		var i=0;
    		while(i<childs.length){
//    			console.log(childs)
//    			console.log(childs[i])
//    			console.log(this.classNodes[childs[i]])
    			quer=quer+'\n'
    			if (this.classNodes[childs[i]].isOptional()){
    				quer=quer+' OPTIONAL {'
    			}
//    			console.log(this.classNodes[childs[i]].getParameter())
    			if(this.isNodeLeaf( this.classNodes[childs[i]].getParameter())){
    				quer=quer+this.classNodes[childs[i]].getSimQueryPath()
    			}else{
//    				console.log('qui')
    				quer=quer+this.classNodes[childs[i]].getSimQueryPath()+this.traslateChildsQuery(this.getLevel1Child(childs[i]))
    			}
//    			console.log('secChild '+childs[i])
    			if (this.classNodes[childs[i]].isOptional()){
    				quer=quer+' }'
    			}
    			i++;
    		}
//    		for(i=0;i<childs.length;i++){
//    			
//    		}
    	}
    	return quer;
    },
    setPagination : function(){
    	this.paginationEnable=!this.paginationEnable;
    },
    changePageSize : function(page){
    	this.nForP=page;
    	this.page=1;
    },
    addOrdCond : function(par,ord){
    	var o={param:par,ord:ord}
    	this.order.push(o)
    },
    retOrdPar : function(){
    	return _.map(this.order,function(a){return a.param})
    },
    removeOrdByPar : function(par){
    	this.order.splice(_.indexOf(_.map(this.order,function(a){return a.param}),par),1)
    },
    removeAllO : function(){
    	this.order=new Array();
    },
    deleteAllFilter : function(){
    	_.each(this.classNodes,function(a){a.deleteAllFilter()})
    }
//    getAllFiltCond: function(){
//    	var filter=new Array()
//    	for(r=0;r<this.classNodes.length;r++){
//    		for(a=0;this.classNodes[r].attributes.length<a;a++){
//    			
//    			if(this.classNodes[r].attributes[a].filters!==undefined){
//	    			if (this.classNodes[r].attributes[a].filters.length>0){
//	    				filter=filter.concat(this.classNodes[r].attributes[a].filters)
//	    			}
//    			}
//    		}
//    	}
//    	return filter
//    }
    
    
});

qo=new QuerOrchestrator();


//console.log(qo);

//console.log(module.getQueryPath()); // 'emmylou'



//var module = new ClassNode('http://kaiko.getalp.org/dbnary/approximateSynonym','approximateSynonym',true);
//module.addAttributes("attri1","http://kaiko.getalp.org/dbnary/attri1",false);
//module.addAttributes("attri2","http://kaiko.getalp.org/dbnary/attri2",true);


//var moduleL = new LinkedClassNode('http://kaiko.getalp.org/dbnary/approximateSynonym','b',true,'propery',false,false,'?a');
//moduleL.addAttributes("attri1","http://kaiko.getalp.org/dbnary/attri1",false);
//moduleL.addAttributes("attri2","http://kaiko.getalp.org/dbnary/attri2",true);
//moduleL.addAttributes("attri3","http://kaiko.getalp.org/dbnary/attri3",false);

//console.log(moduleL.getQueryPath())

//console.log(module.isEnablePar()); // 'emmylou'


//var att1=new AttributeOfAClass("attri1","http://kaiko.getalp.org/dbnary/attri1",false);
//
//var att2=new AttributeOfAClass("attri2","http://kaiko.getalp.org/dbnary/attri2",true);
//
//var att3=new AttributeOfAClass("attri3","http://kaiko.getalp.org/dbnary/attri3",false);


//module.addAttributes("attri1","http://kaiko.getalp.org/dbnary/attri1",false);
//module.addAttributes("attri2","http://kaiko.getalp.org/dbnary/attri2",true);
//module.addAttributes("attri3","http://kaiko.getalp.org/dbnary/attri3",false);

//console.log(module);
//
//console.log(module.getParameters());

//qo.addNode(module);
//
//qo.addAttributeToNode(0,"attri1","http://kaiko.getalp.org/dbnary/attri1",false);
//qo.addAttributeToNode(0,"attri2","http://kaiko.getalp.org/dbnary/attri2",true);
//qo.addAttributeToNode(0,"attri3","http://kaiko.getalp.org/dbnary/attri3",false);
//
//qo.addLinkedNode('http://kaiko.getalp.org/dbnary/approximateSynonym','b',true,'propery',false,false);
//
//qo.addAttributeToNode(1,"attri1","http://kaiko.getalp.org/dbnary/attri1",false);
//qo.addAttributeToNode(1,"attri3","http://kaiko.getalp.org/dbnary/attri3",false);


//console.log(qo.getQuery());



//qo.setCodemQuery();

