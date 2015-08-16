window.addEventListener('polymer-ready', function(e) {
	var app = document.querySelector('lodex-layout-test');
	//routing
	console.log(app)
	page.base('/lodex2/testCluster');
	
	page('/',home);
	page('/schemaSummary/:id',schemaSummary);
	page('/cSchemaSummary/:id',cSchemaSummary);
	page('/schemaSummary',schemaSummaryNoDat);
//	page('/refinementPanel',refinement);
	page({hashbang:true});

	
	

	function home(){
		console.log('home')
		document.querySelector('lodex-layout-test').selected=0;
		document.querySelector('lodex-layout-test').$.lodexMenu.selected=0;
	}

	function schemaSummary(ctx){
		console.log("ss called!")
		document.querySelector('lodex-layout-test').selected=1;
		document.querySelector('lodex-layout-test').fire('core-signal', {name: "gotoss", data: {id:ctx.params.id}});
		document.querySelector('lodex-layout-test').$.lodexMenu.selected=1;
	}
	function cSchemaSummary(ctx){
		console.log("ss called!")
		document.querySelector('lodex-layout-test').selected=1;
		document.querySelector('lodex-layout-test').fire('core-signal', {name: "gotocss", data: {id:ctx.params.id}});
		document.querySelector('lodex-layout-test').$.lodexMenu.selected=1;
	}
	function schemaSummaryNoDat(){
		document.querySelector('lodex-layout-test').selected=1;
		document.querySelector('lodex-layout-test').$.lodexMenu.selected=1;
		console.log("called ssnodat")
	}

//	function refinement(){
//		console.log(document.querySelector('lodex-layout').reachable)
//		if (document.querySelector('lodex-layout').reachable === false){			
//			console.log('good')
//			document.querySelector('lodex-layout').$.lodexMenu.selected=1;
//			document.querySelector('lodex-layout').$.endNotReach.show();
//			
//			document.location.href = "#!/schemaSummary";
//		}else{
//			console.log('bad')
//			document.querySelector('lodex-layout').selected=2;
//			document.querySelector('lodex-layout').$.lodexMenu.selected=2;
//		}
//	}
    });



