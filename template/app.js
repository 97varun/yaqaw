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
});

// angular app
var qaApp = angular.module('qaApp', []);

qaApp.controller('MainController', function MainController($scope) {
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

qaApp.controller('QAController', function QAController($scope) {
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
    $scope.initPosts($scope.posts);
});

qaApp.controller('ProfController', function ProfController($scope) {
    $scope.profInfo = {
        username: 'gb',
        about: 'About Me! I am a very simple card. I am good at containing small bits of information. I am convenient because I require little markup to use effectively.',
    };
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

qaApp.controller('SearchController', function SearchControlelr($scope) {
    $scope.query = '';
});
