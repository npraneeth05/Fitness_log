$(document).ready(function() {
    $('#log-form').submit(function(e) {
        var exercise = $('#exercise').val().trim();
        var reps = $('#reps').val();
        var sets = $('#sets').val();
        if (!exercise || !reps || !sets || reps <= 0 || sets <= 0) {
            alert('Please enter valid exercise, reps, and sets (all must be positive numbers).');
            e.preventDefault();
        }
    });
});