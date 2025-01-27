// Enhanced stats object with popup functionality
const questionCount = document.getElementById('total').textContent;
let stats = {
    attempted: 0,
    correct: 0,
    total: questionCount,
    selectedAnswers: new Map(),

    update: function (isCorrect, questionId, selectedAnswer, correctAnswer) {
        this.attempted++;
        if (isCorrect) this.correct++;
        this.selectedAnswers.set(questionId, {
            selected: selectedAnswer,
            correct: correctAnswer,
            isCorrect: isCorrect
        });
        this.updateDisplay();
        this.checkCompletion();
    },

    updateDisplay: function () {
        document.getElementById('attempted').textContent = this.attempted;
        document.getElementById('correct').textContent = this.correct;
        const percentage = this.attempted ? Math.round((this.correct / parseInt(this.attempted)) * 100) : 0;
        document.getElementById('percentage').textContent = percentage;
        document.getElementById('progress-fill').style.width = `${(this.attempted / this.total) * 100}%`;
    },

    checkCompletion: function () {
        console.log(this.attempted, this.total);
        if (this.attempted === parseInt(this.total)) {
            setTimeout(() => this.showCompletionPopup(), 2000);
        }
    },

    showCompletionPopup: function () {
        const popup = document.getElementById('completion-popup');

        // Update popup stats
        document.getElementById('popup-total').textContent = this.total;
        document.getElementById('popup-attempted').textContent = this.attempted;
        document.getElementById('popup-correct').textContent = this.correct;
        document.getElementById('popup-percentage').textContent =
            `${Math.round((this.correct / this.total) * 100)}%`;

        // Generate review items
        const reviewContainer = document.getElementById('answers-review');
        reviewContainer.innerHTML = ''; // Clear existing content

        document.querySelectorAll('.question-block').forEach((block, index) => {
            const questionId = block.dataset.questionId;
            const questionText = block.querySelector('h3').textContent;
            const answerData = this.selectedAnswers.get(questionId);

            const reviewItem = document.createElement('div');
            reviewItem.className = 'review-item';

            if (answerData) {
                // Question was answered
                reviewItem.innerHTML = `
                <div class="review-question">${questionText}</div>
                <div class="review-answer ${answerData.isCorrect ? 'correct' : 'incorrect'}">
                    <span>Your answer: ${answerData.selected}</span>
                    ${!answerData.isCorrect ?
                        `<div class="review-answer correct">
                        <span>Correct answer: ${answerData.correct}</span>
                    </div>` : ''
                    }
                </div>
            `;
            } else {
                // Question was not answered
                const correctAnswer = block.querySelector('.option-container[data-is-correct="true"] span').textContent;
                reviewItem.innerHTML = `
                <div class="review-question">${questionText}</div>
                <div class="review-answer incorrect">
                    <span>Not attempted</span>
                    <div class="review-answer correct">
                        <span>Correct answer: ${correctAnswer}</span>
                    </div>
                </div>
            `;
            }

            reviewContainer.appendChild(reviewItem);
        });

        popup.style.display = 'block';
    }
};

// Timer functionality
const timer = {
    totalSeconds: Math.ceil(questionCount * 0.7 * 60),
    // totalSeconds: Math.ceil(5),

    remainingSeconds: 0,
    timerId: null,

    initialize: function () {
        this.remainingSeconds = this.totalSeconds;
        this.update();
    },

    start: function () {
        this.timerId = setInterval(() => this.tick(), 1000);
    },

    tick: function () {
        this.remainingSeconds--;
        this.update();

        if (this.remainingSeconds <= 0) {
            clearInterval(this.timerId);
            this.timeUp();
        }
    },

    update: function () {
        const minutes = Math.floor(this.remainingSeconds / 60);
        const seconds = this.remainingSeconds % 60;
        document.getElementById('timer-display').textContent =
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    },

    timeUp: function () {
        // Disable all remaining unchecked radio buttons
        document.querySelectorAll('.radio-input:not(:checked)').forEach(radio => {
            radio.disabled = true;
        });

        // Mark all unanswered questions as incorrect
        document.querySelectorAll('.question-block').forEach(block => {
            const hasAnswer = block.querySelector('input:checked');
            if (!hasAnswer) {
                // Show correct answer for unanswered questions
                const correctOption = block.querySelector('.option-container[data-is-correct="true"]');
                correctOption.classList.add('correct');
                const feedbackSpan = correctOption.querySelector('.answer-feedback');
                feedbackSpan.textContent = '✓';
                feedbackSpan.classList.add('visible');
            }
        });

        // Show completion popup
        stats.showCompletionPopup();
    }
};

// Enhanced checkAnswer function
function checkAnswer(radioButton) {
    const optionContainer = radioButton.closest('.option-container');
    const questionBlock = radioButton.closest('.question-block');
    const allOptions = questionBlock.querySelectorAll('.option-container');
    const allRadios = questionBlock.querySelectorAll('.radio-input');
    const isCorrect = optionContainer.dataset.isCorrect === 'true';

    // Get selected and correct answer text
    const selectedAnswer = optionContainer.querySelector('span').textContent;
    let correctAnswer = '';
    allOptions.forEach(option => {
        if (option.dataset.isCorrect === 'true') {
            correctAnswer = option.querySelector('span').textContent;
        }
    });

    stats.update(isCorrect, questionBlock.dataset.questionId, selectedAnswer, correctAnswer);

    // Rest of the existing checkAnswer function remains the same
    allRadios.forEach(radio => radio.disabled = true);
    allOptions.forEach(option => {
        option.classList.add('disabled');
        option.classList.remove('correct', 'incorrect');
        option.querySelector('.answer-feedback').textContent = '';
        option.querySelector('.answer-feedback').classList.remove('visible');
    });

    const feedbackSpan = optionContainer.querySelector('.answer-feedback');
    if (isCorrect) {
        optionContainer.classList.add('correct');
        feedbackSpan.textContent = '✓';
    } else {
        optionContainer.classList.add('incorrect');
        feedbackSpan.textContent = '✗';

        allOptions.forEach(option => {
            if (option.dataset.isCorrect === 'true') {
                option.classList.add('correct');
                option.querySelector('.answer-feedback').textContent = '✓';
                option.querySelector('.answer-feedback').classList.add('visible');
            }
        });
    }
    feedbackSpan.classList.add('visible');

    // Scroll to next unanswered question
    const nextQuestionBlock = [...document.querySelectorAll('.question-block')]
        .find(block => !block.querySelector('input:disabled'));

    if (nextQuestionBlock) {
        setTimeout(() => {
            nextQuestionBlock.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 500);
    }
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', function () {
    stats.total = questionCount;
    stats.updateDisplay();

    // Handle any pre-checked answers
    const checkedInputs = document.querySelectorAll('input[type="radio"]:checked');
    checkedInputs.forEach(input => {
        checkAnswer(input);
    });

    // Initialize timer immediately to show the starting time
    timer.initialize();

    // Start timer after 2 seconds
    setTimeout(() => timer.start(), 2000);
});

document.getElementById("submit-data").addEventListener("click", function (e) {
    e.preventDefault();
    const quizResults = {
        total_questions: parseInt(stats.total),
        attempted_questions: stats.attempted,
        correct_answers: stats.correct,
        answers: Array.from(stats.selectedAnswers).map(([questionId, answerData]) => ({
            question_id: questionId,
            selected_answer_id: document.querySelector(`input[name="${questionId}"]:checked`).value,
            is_correct: answerData.isCorrect
        })),
        time_spent: timer.totalSeconds - timer.remainingSeconds,
        quiz_name: document.getElementById('quiz-name').textContent,
        quiz_id: document.getElementById('quiz-id').textContent
    };

    fetch('/save-quiz-results/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(quizResults)
    })
        .then(response => {
            if (response.ok) {
                window.location.href = '/';
            } else {
                console.error('Failed to save quiz results');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});