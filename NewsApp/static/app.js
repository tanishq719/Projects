document.addEventListener('DOMContentLoaded', function()
{
	let displayCard = document.querySelector('.my-newsapp-feed');
	fetch('/getNews')
	.then(response=>
	{
		response.json()
		.then(resObj=>
		{
			console.log(resObj);
			let data = resObj.content;
			console.log(`working properly`, data);
			let cards = document.createElement('ol');
			for(let i=0; i<resObj.length; i++)
			{
				cardi = document.createElement('li');
				cardi.innerHTML = 
				`<div class="card text-center my-5 mx-auto" style = "width: 50%">								  
				<div class="card-header">
					    `+data[0].tag+`
					  </div>
					  <div class="card-body">
					    <h5 class="card-title">`+data[0].title+`</h5>
					    <img src=`+data[0].image+`>
					    <p class="card-text">`+data[0].text+`</p>
					    <a href=`+data[0].link+` class="btn btn-primary">Read Full....</a>
					  </div>
					  <div class="card-footer text-muted">
					   `+data[0].time+`
					  </div>
					</div>`;
					cards.appendChild(cardi);	
			}
			displayCard.appendChild(cards) ;
			console.log('here', displayCard);
		});
		console.log(resObj);
		return response;
	})
	.catch(err=> console.log(err));
	console.log('here', displayCard);
});
