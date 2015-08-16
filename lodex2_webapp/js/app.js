window.addEventListener('polymer-ready', function(e) {
	var app = document.querySelector('lodex-layout');
	//routing
	console.log(app)
	page.base('/lodex2/ok');
	
	page('/',home);
	page('/schemaSummary/:id',schemaSummary);
	page('/test/schemaSummary/:id',testSchemaSummary);
	page('/schemaSummary',schemaSummaryNoDat);
	page('/refinementPanel',refinement);
	page({hashbang:true});

	
	

	function home(){
		console.log('home')
		document.querySelector('lodex-layout').selected=0;
		document.querySelector('lodex-layout').$.lodexMenu.selected=0;
	}

	function schemaSummary(ctx){
		console.log("ss called!")
		document.querySelector('lodex-layout').selected=1;
		document.querySelector('lodex-layout').fire('core-signal', {name: "gotoss", data: {id:ctx.params.id}});
		document.querySelector('lodex-layout').$.lodexMenu.selected=1;
	}
	
	function testSchemaSummary(ctx){
		console.log("ss called!")
		document.querySelector('lodex-layout').selected=1;
		document.querySelector('lodex-layout').fire('core-signal', {name: "gotosstest", data: {id:ctx.params.id}});
		document.querySelector('lodex-layout').$.lodexMenu.selected=1;
	}
	
	function schemaSummaryNoDat(){
		document.querySelector('lodex-layout').selected=1;
		document.querySelector('lodex-layout').$.lodexMenu.selected=1;
		console.log("called ssnodat")
	}

	function refinement(){
		console.log(document.querySelector('lodex-layout').reachable)
		if (document.querySelector('lodex-layout').reachable === false){			
			console.log('good')
			document.querySelector('lodex-layout').$.lodexMenu.selected=1;
			document.querySelector('lodex-layout').$.endNotReach.show();
			
			document.location.href = "#!/schemaSummary";
		}else{
			console.log('bad')
			document.querySelector('lodex-layout').selected=2;
			document.querySelector('lodex-layout').$.lodexMenu.selected=2;
		}
	}
    });



