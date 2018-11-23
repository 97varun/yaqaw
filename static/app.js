// materialize components initialization
$(document).ready(function() {
    // profile dropdown
    dropdownOptions = {
        alignment: 'right',
        constrainWidth: true,
        coverTrigger: false,
        autoTrigger: false
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
        },
        minLength: 0
    }
    $('input.autocomplete').autocomplete(autocompleteOptions);
    $('#ask-question').modal();
    $('#summary-modal').modal();
});

// angular app
var qaApp = angular.module('qaApp', []);

qaApp.controller('MainController', function MainController($scope, $http) {
    // some initialisation.
    $scope.initPosts = function (posts, showAnswers=false, showBtnText='show answers') {
        if (posts.length) {
            posts.forEach(post => {
                post.showAnswers = showAnswers;
                post.showBtnText = showBtnText;
                post.answering = false;
                post.userAnswer = '';
            });
        }
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
        var q = {'question': post.question, 'answer': post.userAnswer};
        $http.post('/addanswer', q).then(function(response) {
            if (response.data.status === 'success') {
                // alert('question added successfully');
            } else if (response.data.status === 'failed') {
                alert('unable to add answer. Try again later');
            } else {
                alert('Not logged in. Please login');
            }
        });
        post.answering = false;
        post.userAnswer = '';
    }
    // show/hide answer textarea
    $scope.openClose = function(post) {
        if (post.answering) {
            post.answering = false;
            post.userAnswer = '';
        } else {
            post.answering = true;
        }
    }
});

qaApp.controller('QAController', function QAController($scope, $http) {
    $scope.fetchQuestions = function() {
        $http.get('/getquestions?type=all').then(function(response) {
            $scope.posts = response.data;
            $scope.initPosts($scope.posts);
        });
    }
    $scope.fetchQuestions();

    // upvote/downvote
    $scope.vote = function(id, ans, isUp, idx) {
        var vote = {'id': id, 'answer': ans, 'vote': isUp ? 'upvote' : 'downvote'};
        $http.post('/vote', vote).then(function(response) {
            var res = response.data;
            var post = $scope.posts.find(x => x._id == id);
            post.answers[idx] = res.answer;
        });
    }

    $scope.answerQuestionWrapper = function(post) {
        $scope.answerQuestion(post);
        $http.get('/getquestions?type=all').then(function(response) {
            var res = response.data;
            post.answers = res.find(x => x._id == post._id).answers;
        });
    }

    $scope.summary = '';
    $scope.showSummary = function(answer) {
        $http.get('/getsummary?answer=' + answer).then(function(response) {
            $scope.summary = response.data;
            $('#summary-modal').modal('open');
        });
    }
});

qaApp.controller('ProfController', function ProfController($scope, $http) {
    $scope.getProfInfo = function() {
        $http.get('/getinfo').then(function(response) {
            $scope.profInfo = response.data;
        });
    }
    $scope.getProfInfo();
    
    $scope.getUserPosts = function() {
        $http.get('/getquestions').then(function(response) {
            $scope.posts = response.data;
            $scope.initPosts($scope.posts);
        });
    }
    $scope.getUserPosts();

    $scope.getUserAnsweredPosts = function() {
        $http.get('/getanswers').then(function(response) {
            $scope.answeredPosts = response.data;
            $scope.initPosts($scope.answeredPosts, true, 'collapse');
        });
    }
    $scope.getUserAnsweredPosts();   
    
    $scope.questionView = true;
    $scope.switchToQuestionView = function() {
        $scope.getUserPosts();
        $scope.questionView = true;
    }
    $scope.switchToAnswerView = function() {
        $scope.getUserAnsweredPosts();
        $scope.questionView = false;
    }
    $scope.getPosts = function() {
        if ($scope.questionView) {
            return $scope.posts;
        } else {
            return $scope.answeredPosts;
        }
    }
    $scope.vote = function(id, ans, isUp, idx) {
        var vote = {'id': id, 'answer': ans, 'vote': isUp ? 'upvote' : 'downvote'};
        $http.post('/vote', vote).then(function(response) {
            var res = response.data;
            var post = null;
            if ($scope.quesitonView) {
                post = $scope.posts.find(x => x._id == id);
            } else {
                post = $scope.answeredPosts.find(x => x._id == id);
            }
            if (post) {
                post.answers[idx] = res.answer;
            }
        });
    }

    $scope.answerQuestionWrapper = function(post) {
        $scope.answerQuestion(post);
        $http.get('/getquestions').then(function(response) {
            var res = response.data;
            post.answers = res.find(x => x._id == post._id).answers; 
        });
        $scope.getUserAnsweredPosts();
    }
});

qaApp.controller('UserController', function UserController($scope,$http) {
    $scope.login = function() {
        $http.post('/login',{username:$scope.username,password:$scope.password}).then(function(response){
            if(response.data.message=="Success"){
                window.open('/questions',"_self");
            }
            else{
                $scope.resp=response.data.comment;
                console.log("Failed",response.comment);
            }
        });
    }
    $scope.register = function(e) {
        e.preventDefault();
        $http.post('/register',{username:$scope.newuser.username,password:$scope.newuser.password,about:$scope.newuser.about}).then(function(response){
            if(response.data.message=="Success"){
                window.open('/login',"_self");
            }
            else{
                $scope.resp=response.data.comment;
                console.log("Failed",response.comment);
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
            } else if (response.data.status == "failed") {
                alert('error adding question');
            } else {
                alert('you should be logged in to add a question');
            }
        });
        if ($scope.fetchQuestions) {
            $scope.fetchQuestions();
        } else {
            $scope.getUserAnsweredPosts();
            $scope.getUserPosts();
        }
    }
    $scope.cancel = function() {
        var m = $('#ask-question');
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
        var autocompleteData = {}
        $http.post('/search', search).then(function(response) {
            console.log(response.data);
            response.data.forEach(function(x) {
                autocompleteData[x.question] = null;
            });
            ac.autocomplete('updateData', autocompleteData);
            ac.autocomplete('open');
        });
        console.log(autocompleteData);
    }
    $scope.askQuestion = function() {
        var m = $('#ask-question');
        m.modal('open');
        M.updateTextFields();
    }
});
