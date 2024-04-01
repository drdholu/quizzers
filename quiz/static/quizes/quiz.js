const url2 = window.location.href;
console.log(url2);

const quizBox = document.getElementById('quiz-box');
const timerBox = document.getElementById('timer-box');

let timer;

const activateTimer = (time) => {
    let storedTime = localStorage.getItem('timer');
    let remainingTime = time * 60;

    if (storedTime) {
        remainingTime = parseInt(storedTime, 10);
    }

    function updateTimerDisplay() {
        let minutes = Math.floor(remainingTime / 60);
        let seconds = remainingTime % 60;

        let displayMinutes = minutes < 10 ? '0' + minutes : minutes;
        let displaySeconds = seconds < 10 ? '0' + seconds : seconds;

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`;
    }

    updateTimerDisplay();

    timer = setInterval(() => {
        remainingTime--;

        // Update localStorage value every second
        localStorage.setItem('timer', remainingTime.toString());

        if (remainingTime < 0) {
            clearInterval(timer);
            timerBox.innerHTML = '<b>00:00</b>';
            alert('Time is over');
            sendData();
            
            // Reset localStorage value to initial state when timer is over
            localStorage.setItem('timer', (time * 60).toString());
        } else {
            updateTimerDisplay();
        }
    }, 1000);
};



$.ajax({
    type: 'GET',
    url: `${url2}/data`, // Gets data from JsonResponse
    success: function(response) {
        const data = response.data;
        const time = response.time;
        // console.log(response.data);
        data.forEach((element) => {
            for (const [question, answers] of Object.entries(element)) {
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `;
                answers.forEach((answer) => {
                    quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `;
                });
            }
        });
        activateTimer(time);
    },
    error: function(error) {
        console.log(error);
    },
});

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken') 

const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')

const sendData = () => {
    // TODO: stops the timer
    timerBox.remove()
     
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]){
                data[el.name] = null
            }
        }
    })


    $.ajax({
        type: 'POST',
        url: `${url2}/save`,
        data: data,
        success: function(response){
            const results = response.results
            const n_correct_answers = response.score
            const score = response.score.toFixed(2)
            const passed = response.passed

            // Removes the form 
            quizForm.remove()
            
            let scoreDiv = document.createElement('div')
            // scoreDiv.classList.add(...['container', 'my-auto', 'text-secondary'])
            
            console.log('Hello world')
            scoreDiv.innerHTML += `
                               <p> ${passed ? 'Congrats you passed the test!' : 'Sorry, you did not pass the test!'} Your result is ${score} %</p>
                               <p> Answered correctly: ${n_correct_answers}</p>
                               `

            scoreBox.append(scoreDiv)

            results.forEach(res =>{
                let resDiv = document.createElement('div')
                
                for (const [question, resp] of Object.entries(res)){
                    resDiv.innerHTML += question

                    const classes = ['container', 'p-3', 'text-light', 'h4']
                    resDiv.classList.add(...classes)

                    if (resp == 'not answered'){
                        resDiv.innerHTML += ' — Not answered'
                        resDiv.classList.add('bg-danger')
                    } else{
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if (answer == correct){
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` Answered: ${answer}`
                        } else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += `| Answered: ${answer}`
                            resDiv.innerHTML += `| Correct answer: ${correct}`
                        }
                    }
                }
                resultBox.append(resDiv)
            })
        },
        error: function(error){
            console.log(error)
        }
    })
}


quizForm.addEventListener('submit', (element) => {
    element.preventDefault();

    // Clear the timer from localStorage on form submission
    localStorage.removeItem('timer');

    sendData();
});
