// padding days/padding squares needed 

// keeps track of which month we are on
//-1 == december, jan = 0 etc...
let nav = 0;

//going to be whichever day we clicked on
let clicked = null;

//events - an array of event objects, can only store strings in local storage
//need to make sure 'events' exist in local storage, before we call Json.parse
//events are either going to be an array with event objects or an empty array with no events
let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];

// global constants

//weekdays is going to be an array that will let us determine the number of padding days

const calendar = document.getElementById('calendar');
const weekdays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Sunday'];

function load(){
    //dt is a constant OBJECT, therefore it has properties
    const dt = new Date();

    if(nav != 0){
        //we get the current month e.g. October == 10 and either add or subtract nav to get to the next or prev month
        dt.setMonth(new Date().getMonth + nav);
    }

    const day = dt.getDate();
    const month = dt.getMonth();
    const year = dt.getFullYear();

    //first day of January
    const firstDayofMonth = new Date(year,month,1);
    
    //if its jan 2021, daysinMonth will store whatever the date is for the last day in January
    const daysInMonth = new Date(year,month+1,0).getDate();

    const dateString = firstDayofMonth.toLocaleDateString('en-us', {
        
        weekday: 'long',
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
    });

    const paddingDays = weekdays.indexOf(dateString.split(',')[0]);

    //we want to change the month based on how the user clicks the next or back buttons
    document.getElementById('monthDisplay').innerText = `${dt.toLocaleDateString('en-us',{month: 'long'})} ${year}`;


    //need to wipe calendar out everytime we change the month
    calendar.innerHTML = '';



    for(let i=1;i <= paddingDays + daysInMonth; i++){
        const daySquare = document.createElement('div');
        daySquare.classList.add('day');

        

        if(i > paddingDays){
            //if we are on an actual day not a padding day
            daySquare.innerText = i - paddingDays;

            daySquare.addEventListener('click', () => console.log('click'));
        }

        else{
            daySquare.classList.add('padding');
        }

        calendar.appendChild(daySquare);
    }
}

//need event listeners for buttons
function initButtons(){
    document.getElementById('nextButton').addEventListener('click', () => {
        nav++;
        load();
    })

    //remember that nav is the month that we are on
    document.getElementById('backButton').addEventListener('click', () => {
        nav--;
        load();
    })


}

initButtons();
load();

