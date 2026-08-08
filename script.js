async function updateDisplay() {

    try {

        const response = await fetch("/display_data");

        if (!response.ok) {
            throw new Error("Failed to fetch display data");
        }

        const data = await response.json();

        const questionElement =
            document.getElementById("question");

        const answerElement =
            document.getElementById("answer");


        if (data.question && data.question.trim() !== "") {

            questionElement.textContent =
                data.question;

        }


        if (data.answer && data.answer.trim() !== "") {

            answerElement.textContent =
                data.answer;

        }

    }

    catch (error) {

        console.error(
            "Display update error:",
            error
        );

    }

}


// Update immediately
updateDisplay();


// Check for new answer every 500 ms
setInterval(
    updateDisplay,
    500
);