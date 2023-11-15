// Создаем массив counts_like и заполняем его нулями
let counts_like = [0, 0, 0, 0];

function updateCounter(counter, elementId) {
    document.getElementById(elementId).innerText = counter;
    console.log(counter, elementId);
}

function like(buttonNumber) {
    counts_like[buttonNumber]++;
    updateCounter(counts_like[buttonNumber], 'count' + buttonNumber);
    console.log(buttonNumber);
}

function dislike(buttonNumber) {
    counts_like[buttonNumber]--;
    updateCounter(counts_like[buttonNumber], 'count' + buttonNumber);
    console.log(buttonNumber);
}