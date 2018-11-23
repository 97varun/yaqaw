// materialize components initialization
$(document).ready(function() {
    // profile dropdown
    dropdownOptions = {
        alignment: 'right',
        constrainWidth: false,
        coverTrigger: false
    };
    $('.dropdown-trigger').dropdown(dropdownOptions);
    $('.tabs').tabs();
    autocompleteOptions = {
        data: {
            "Apple": null,
            "Microsoft": null,
            "Google": 'https://placehold.it/250x250'
        },
        onAutocomplete: function (e) {
            console.log(e);
        }
    }
    $('input.autocomplete').autocomplete(autocompleteOptions);
    $('.modal').modal();
});

// angular app
var qaApp = angular.module('qaApp', []);

qaApp.controller('MainController', function MainController($scope, $http) {
    // some initialisation.
    $scope.initPosts = function (posts, showAnswers=false, showBtnText='show answers') {
        posts.forEach(post => {
            post.showAnswers = showAnswers;
            post.showBtnText = showBtnText;
            post.answering = false;
            post.userAnswer = '';
        });
    }
    // to show/hide answers
    $scope.switchView = function(post) {
        if (post.showAnswers) {
            post.showAnswers = false;
            post.showBtnText = 'show answers';
        } else {
            post.showAnswers = true;
            post.showBtnText = 'collapse';
        }
    }
    // submit answer to a question
    $scope.answerQuestion = function(post) {
        console.log(post.userAnswer);
        post.answering = false;
        post.userAnswer = '';
    }
    // show/hide answer textarea
    $scope.openClose = function(post) {
        if (post.answering) {
            post.answering = false;
            post.userAnswer = '';
            $('#answer-field').attr('rows', 0);
        } else {
            post.answering = true;
        }
    }
});

qaApp.controller('QAController', function QAController($scope, $http) {
    $scope.posts = [
        {
            _id: '1',
            question: "Can the speed of a particle ever be negative? Give an example.",
            username: "gb",
            answers: [
                "No. Speed is a scalar quantity and so is always positive. Hope you understood.", 
                "answer2", 
                "answer3"
            ]
        },
        {
            _id: '2',
            question: "What is the answer to life, the universe and everything?",
            username: "gb",
            answers: [
                "42", 
                "43", 
                "44"
            ]
        },
    ];
    $scope.fetchQuestions = function() {
        $http.get('/getquestions').then(function(response) {
            $scope.posts = resoponse.data;
            console.log(response.data);
        });
    }
    $scope.initPosts($scope.posts);
});

qaApp.controller('ProfController', function ProfController($scope, $http) {
    $scope.getProfInfo = function() {
        $http.get('/getinfo').then(function(response) {
            $scope.profInfo = resoponse.data;
            console.log(response.data);
        });
    }
    $scope.profInfo = {
        username: 'gb',
        about: 'About Me! I am a very simple card. I am good at containing small bits of information. I am convenient because I require little markup to use effectively.',
    };
    $scope.getUserPosts = function() {
        $http.get('/getquestions').then(function(response) {
            $scope.posts = resoponse.data;
            console.log(response.data);
        });
    }
    $scope.posts = [
        {
            _id: '1',
            question: "Can the speed of a particle ever be negative? Give an example.",
            username: "gb",
            answers: ["No. Speed is a scalar quantity and so is always positive. Hope you understood.", "answer2", "answer3"]
        },
        {
            _id: '2',
            question: "What is the answer to life, the universe and everything?",
            username: "gb",
            answers: ["42", "43", "44"]
        }
    ];
    $scope.getUserAnsweredPosts = function() {
        $http.get('/getanswers').then(function(response) {
            $scope.answeredPosts = response.data;
            console.log(response.data);
        });
    }   
    $scope.answeredPosts = [
        {
            _id: '1',
            question: "Can the speed of a particle ever be negative? Give an example.",
            username: "gb",
            answers: ["No. Speed is a scalar quantity and so is always positive. Hope you understood."]
        },
        {
            _id: '2',
            question: "What is the answer to life, the universe and everything?",
            username: "gb",
            answers: ["42"]
        }
    ];
    // some initialisation.
    $scope.initPosts($scope.posts);
    $scope.initPosts($scope.answeredPosts, true, 'collapse');

    $scope.questionView = true;
    $scope.switchToQuestionView = function() {
        $scope.questionView = true;
    }
    $scope.switchToAnswerView = function() {
        $scope.questionView = false;
    }
    $scope.getPosts = function() {
        if ($scope.questionView) {
            return $scope.posts;
        } else {
            return $scope.answeredPosts;
        }
    }
});
qaApp.controller('UserController', function UserController($scope,$http) {

    $scope.login = function() {
        $http.post('/login',{username:$scope.username,password:$scope.password}).then(function(response){
            if(response.data.message=="Success"){
                window.open('/question',"__self");
            }
            else{
                $scope.resp=response.data.comment;
                console.log("Failed shit",response.comment);
                
            }
        });
    }
    
    $scope.register = function(e) {
        e.preventDefault(); 
        $http.post('/register',{username:$scope.newuser.username,password:$scope.newuser.password,about:$scope.newuser.about}).then(function(response){
            if(response.data.message=="Success"){
                window.open('/login',"__self");
            }
            else{
                $scope.resp=response.data.comment;
                console.log("Failed shit",response.comment);
                
            }
        });
    }


});

qaApp.controller('SearchController', function SearchController($scope, $http) {
    $scope.query = '';
    $scope.addQuestion = function() {
        var question = {'question': $scope.query};
        $http.post('/addquestion', question).then(function(response) {
            if (response.data.status === "success") {
                alert('question added!');
            } else if (response.data.status == "faliure") {
                alert('error adding question');
            } else {
                alert('you should be logged in to add a question');
            }
        });
        console.log('addQuestion: ', $scope.query);
    }
    $scope.cancel = function() {
        var m = $('.modal');
        m.modal('close');
    }
    
    // submission throttling
    $scope.timer = null;
    $scope.getQuery = function() {
        if ($scope.timer) {
            clearTimeout($scope.timer);
        }
        $scope.timer = setTimeout($scope.sendQuery, 1000);
    }
    $scope.sendQuery = function() {
        console.log('sendQuery:', $scope.query);
        var search = {'query': $scope.query};
        var ac = $('input.autocomplete');
        // $http.post('/search', search).then(function(response) {
        //     console.log(response.data);
        //     var autocompleteData = response.data.map(x => {x.question: null});
        //     ac.autocomplete('updateData', autocompleteData);
        // });
        var autocompleteData = {
            'world': null,
            'hello': null
        };
        ac.autocomplete('updateData', autocompleteData);
    }
    $scope.askQuestion = function() {
        var m = $('.modal');
        m.modal('open');
        M.updateTextFields();
    }
});
