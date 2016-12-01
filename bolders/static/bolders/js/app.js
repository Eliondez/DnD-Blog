(function(){
	var app = angular.module('char-app', []);

	app.controller('StoreController', function() {
		this.products = gems;
	});

	var gems = [
	{
		name: 'Dodec',
		price: 1.23,
		description: 'azaza',
		images: [
		{
			full: "data:image/jpeg;base64,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",
			thumb: "http://www.imarvintpa.com/Mapping/Objects/Items/Treasure/Gems/Gem-A.png"
		},
		{
			full: "",
			thumb: ""
		}
		],
		canPurchase: true,
	},
	{
		name: 'Ikos',
		price: 5.13,
		description: 'ozozo',
		images: [
		{
			full: "",
			thumb: ""
		},
		{
			full: "",
			thumb: ""
		}
		],
		canPurchase: true,
	},
	];
})();
