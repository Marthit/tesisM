(function () {
    
    var questions = [{
        question: "<img src='/static/images/pre_test/1.jpg'> <br>My sister _______________ the dishes.",
        choices: ["Wash", "Washes", "Washing"]
    }, {
        question: "<img src='/static/images/pre_test/2.jpg'> <br>I _______________ my mother at home.",
        choices: ["Help", "Helps", "Helping"]
    }, {
        question: "I _______________ your sweater",
        choices: ["Like", "Likes", "Liking"]
    },
     
    {
        question: "Peter _______________ that jacket",
        choices: ["have", "has", "is"]
    },
    {
        question: "Janet _______________ this skirt",
        choices: ["needs", "need", "is needing"]
    },
     {
        question: "_______________ your grandparents _______________ in Sydney?",
        choices: ["Do-live", "Does-Lives", "Do-Lives"]
    },{
        question: "<img src='/static/images/pre_test/tv.jpg'> <br>My grandma _______________ watches TV in the afternoon.",
        choices: ["Always", "Usually", "Never"]
    },{
        question: "<img src='/static/images/pre_test/boy.jpg'> <br>My brother _______________ brushes his teeth in the morning.",
        choices: ["Always", "Usually", "Never"]
    },{
        question: "The weather _______________ warm.",
        choices: ["Was", "Were", "Weren't"]
    },{
        question: "¿Cuál es el pasado participio del verbo 'break'?",
        choices: ["Broken", "Broke", "Breaked"]
    }
    
    ];

    var questionCounter = 0; //Tracks question number
    var selections = []; //Array containing user choices
    var quiz = $('#quiz'); //Quiz div object
    
    // Display initial question
    displayNext();

    // Click handler for the 'next' button
    $('#next').on('click', function (e) {
        e.preventDefault();

        // Suspend click listener during fade animation
        if (quiz.is(':animated')) {
            return false;
        }
        choose();

        // If no user selection, progress is stopped
        if (isNaN(selections[questionCounter])) {
            swal({
              title: "Alerta",
              text: "Por favor haz una selección",
              icon: "warning",
            });        
        } else {
            questionCounter++;
            displayNext();
        }
    });

    // Click handler for the 'prev' button
    $('#prev').on('click', function (e) {
        e.preventDefault();

        if (quiz.is(':animated')) {
            return false;
        }
        choose();
        questionCounter--;
        displayNext();
    });


    $('#start').on('click', function (e) {
        e.preventDefault();

        if (quiz.is(':animated')) {
            return false;
        }
        questionCounter = 0;
        selections = [];
        $('#title.card-header').html("Selecciona la mejor respuesta ...se totalmente sincero!");
        $('#recomiendaPreTest').hide();
        displayNext();
        $('#start').hide();
    });


    $('#guardar').on('click', function (e) {
        e.preventDefault();
        if (quiz.is(':animated')) {
            return false;
        }
        $('#recomiendaPreTest').hide();
        //$('#start').hide();
        $('#guardar').hide();
    

      $.getJSON($SCRIPT_ROOT + '/pre_diagnostico', {
        //a: 5,
        //b: 10,
        selections: JSON.stringify(selections)
      }, function(data) {
            var score = $('<p>', {id: 'question'});
            score.append(data.result);
            quiz.html(score).fadeIn();                   
      });           
        
            swal({
              title: "Éxito",
              text: "Datos guardados correctamente",
              icon: "success",
            });         
        //url=$SCRIPT_ROOT + '/pythonlogin/home'  
        //setTimeout(function(){window.location = url;}, 2000);     
    });



    // Animates buttons on hover
    $('.button').on('mouseenter', function () {
        $(this).addClass('active');
    });
    $('.button').on('mouseleave', function () {
        $(this).removeClass('active');
    });

    // Creates and returns the div that contains the questions and
    // the answer selections
    function createQuestionElement(index) {
        var qElement = $('<div>', {
            id: 'question'
        });

        var header = $('<h2>Pregunta ' + (index + 1) + ':</h2>');
        qElement.append(header);
        console.log (questions[index].question)
        var question = $('<p>').append(questions[index].question);
        qElement.append(question);

        var radioButtons = createRadios(index);
        qElement.append(radioButtons);

        return qElement;
    }

    // Creates a list of the answer choices as radio inputs
    function createRadios(index) {
        var radioList = $('<ul>');
        var item;
        var input = '';
        for (var i = 0; i < questions[index].choices.length; i++) {
            item = $('<li>');
            input = '<input type="radio" name="answer" value=' + i + ' />';
            input += ' ' + questions[index].choices[i];
            item.append(input);
            radioList.append(item);
        }
        return radioList;
    }

    // Reads the user selection and pushes the value to an array
    function choose() {
        selections[questionCounter] = +$('input[name="answer"]:checked').val();
    }

    // Displays next requested element
    function displayNext() {
        quiz.fadeOut(function () {
            $('#question').remove();

            if (questionCounter < questions.length) {
                var nextQuestion = createQuestionElement(questionCounter);
                quiz.append(nextQuestion).fadeIn();
                if (!(isNaN(selections[questionCounter]))) {
                    $('input[value=' + selections[questionCounter] + ']').prop('checked', true);
                }

                // Controls display of 'prev' button
                if (questionCounter === 1) {
                    $('#prev').show();
                } else if (questionCounter === 0) {

                    $('#prev').hide();
                    $('#next').show();
                }
            } else {
            
                var scoreElem = displayScore();
                quiz.append(scoreElem).fadeIn();
                $('#next').hide();
                $('#prev').hide();
                //$('#start').show();
                $('#guardar').show();                
                $('#recomiendaPreTest').show();
            }
        });
    }

    // Computes score and returns a paragraph element to be displayed
    function displayScore() {
        $('#title.card-header').html("Resultados obtenidos");
        var score = $('<p>', {id: 'question'});
        score.append('De click en "Guardar" para ver el resultado de su pre-test.');         
        
        return score;
    }
})();
