(function () {
    
    var questions = [{
        question: "Choose the option (a – c) that best describes each picture.<br><img src='/static/images/post_test/playing_soccer.jpg'>",
        choices: ["My friend doesn’t play soccer.", "My friend plays soccer.", "My friend usually plays soccer at the stadium."]
    }, {
        question: "Choose the option (a – c) that best describes each picture. <br><img src='/static/images/post_test/shoping.jpg'>",
        choices: ["We usually go shopping once a month at the mall.", "We never go shopping.", "We go shopping once a month."]
    }, {
        question: "What’s the boy wearing? <br><img src='/static/images/post_test/kid.jpg'>",
        choices: ["He’s wearing a T-shirt and pants.", "He’s wearing a T-shirt, sneakers and shorts.", "He’s wearing a T-shirt."]
    }, {
        question: "What’s the girl wearing? <br><img src='/static/images/post_test/girl.jpg'>",
        choices: ["She’s wearing a T-shirt, a skirt and pumps.", "She’s wearing a T-shirt.", "She’s wearing a T-shirt and pants."]
    }, {
        question: "What pieces of clothes can you see in the picture above? <br><img src='/static/images/post_test/clothes.jpg'>",
        choices: ["Sneakers, sunglasses, a dress, a skirt, jeans and a jacket.", "Sunglasses, sneakers, a jacket, a sweater, shorts and a watch.", "I can see sneakers, a dress, sunglasses, a sweater, a skirt, jeans and a jacket."]
    }, {
        question: "Last Saturday morning I met Mary at the shopping mall. It ___ a holiday so everything ___ on sale. However, my favorite stores ___ closed until 12:00PM that day. We ___ very excited for them to open.",
        choices: ["was – was – were – were", "was – were – was – was", "was – was – was – were"]
    }, {
        question: "Yesterday ___ September 26th.NOTE: Today’s September 27th. <br><img src='/static/images/post_test/calendar.jpg'>",
        choices: ["was", "is", "were"]
    }, {
        question: "Last weekend ___ September 25th and 26th.",
        choices: ["was", "are", "were"]
    }, {
        question: "The day before yesterday ___ September 26th.",
        choices: ["is", "were", "was"]
    }, {
        question: "What did Nury do last Monday? <br><img src='/static/images/post_test/agenda.jpg'>",
        choices: ["Went shopping", "She went shopping for clothes and shoes.", "She went shopping for clothes."]
    }, {
        question: "How does the girl look like? <br><img src='/static/images/post_test/girls2.jpg'>",
        choices: ["Is tall.", "She is tall.", "She is tall and she has brown hair."]
    }, {
        question: "How does the man look like? <br><img src='/static/images/post_test/man.jpg'>",
        choices: ["Has brown hair.", "He has brown hair and he is muscular.", "He is muscular, he has a mustache, a beard and brown hair."]
    }, {
        question: "How does the woman look like? <br><img src='/static/images/post_test/old_woman.jpg'>",
        choices: ["She’s old.", "Old.", "Is old."]
    }, {
        question: "How do those sneakers look like? <br><img src='/static/images/post_test/shoes.jpg'>",
        choices: ["Are dirty.", "They’re dirty.", "Dirty."]
    }, {
        question: "How do those shoes look like? <br><img src='/static/images/post_test/new_shoes.jpg'>",
        choices: ["Are new.", "They’re new.", "New."]
    }, {
        question: "How often do you visit your uncle Tony?",
        choices: ["Once a month.", "I visit my uncle Tony once a month.", "I visit once a month."]
    }, {
        question: "How often does Susan go to the dentist?",
        choices: ["She goes to the dentist twice a year.", "Twice a year.", "She goes twice a year."]
    }, {
        question: "How often does Susan brush her teeth? <br><img src='/static/images/post_test/girl_brushing.jpg'>",
        choices: ["She always brushes her teeth in the morning.", "always.", "She always brushes."]
    }, {
        question: "How do you often listen to the radio? <br><img src='/static/images/post_test/man_listening.jpg'>",
        choices: ["I rarely.", "I rarely listen to the radio.", "I rarely listen."]
    }, {
        question: "How often does she read the newspaper? <br><img src='/static/images/post_test/woman_reading.jpg'>",
        choices: ["occasionally.", "She occasionally reads.", "She occasionally reads the newspaper."]
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
    

      $.getJSON($SCRIPT_ROOT + '/post_diagnostico', {
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
        score.append('De click en "Guardar" para ver el resultado de su post-test.');         
        
        return score;
    }
})();
