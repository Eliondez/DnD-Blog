(function(){
	var app = angular.module('char-app', []);
	app.controller('CharPanelController', function() {
		this.tab = 1;
		this.selectTab = function(setTab) {
		    this.tab = setTab;
		};
		this.isSelected = function(checkTab){
		    return this.tab === checkTab;
		};
	});
})();
