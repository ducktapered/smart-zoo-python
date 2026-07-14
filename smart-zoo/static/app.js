let jawabanBenarId = "";
let currentScore = 0;
let timerInterval = null;
let timeLeft = 20;
let gameVolume = 0.8;
let maxOptions = 4;
let synth = window.speechSynthesis;

// DOM Elements
const screenMainMenu = document.getElementById("screen-main-menu");
const screenGame = document.getElementById("screen-game");
const screenReward = document.getElementById("screen-reward");
const modalSetting = document.getElementById("modal-setting");
const optionsContainer = document.getElementById("options-container");
const questionText = document.getElementById("question-text");
const timerBadge = document.getElementById("timer");
const rewardVideo = document.getElementById("reward-video");
const rewardAudio = document.getElementById("reward-audio");

// Bind Events
document.getElementById("btn-play").addEventListener("click", () => { changeScreen(screenGame); generateRound(); });
document.getElementById("btn-setting").addEventListener("click", () => modalSetting.classList.add("active"));
document.getElementById("btn-close-setting").addEventListener("click", () => {
    gameVolume = document.getElementById("volume-control").value / 100;
    maxOptions = parseInt(document.getElementById("options-count").value);
    modalSetting.classList.remove("active");
});
document.getElementById("btn-exit").addEventListener("click", backToMenu);
document.getElementById("btn-reward-menu").addEventListener("click", backToMenu);
document.getElementById("btn-reward-next").addEventListener("click", generateRound);
document.getElementById("btn-tts-replay").addEventListener("click", () => speakText(questionText.innerText));

function changeScreen(target) {
    [screenMainMenu, screenGame, screenReward].forEach(s => s.classList.remove("active"));
    target.classList.add("active");
}

function backToMenu() {
    clearInterval(timerInterval);
    if(synth) synth.cancel();
    rewardVideo.pause(); rewardAudio.pause();
    changeScreen(screenMainMenu);
}

// MENGAMBIL DATA SOAL DARI SERVER PYTHON (FASTAPI)
async function generateRound() {
    rewardVideo.pause(); rewardAudio.pause();
    if(synth) synth.cancel();

    try {
        // Ambil data acak dari fungsi Python backend
        const response = await fetch(`/api/baru?jumlah_pilihan=${maxOptions}`);
        const data = await response.json();

        jawabanBenarId = data.hewan_id_benar;
        questionText.innerText = data.soal_deskripsi;
        setTimeout(() => { speakText(data.soal_deskripsi); }, 300);

        // Render Gambar Pilihan Jawaban yang dikirim oleh Python
        optionsContainer.innerHTML = "";
        data.opsi_gambar.forEach(hewan => {
            const card = document.createElement("div");
            card.className = "option-card";
            
            const img = document.createElement("img");
            img.src = `/static/assets/images/${hewan.id}.jpg`;
            img.onerror = () => { img.src = "https://placehold.co/150x150?text=" + hewan.nama; };

            card.appendChild(img);
            card.addEventListener("click", () => {
                if (hewan.id === jawabanBenarId) {
                    clearInterval(timerInterval);
                    confetti({ particleCount: 80, spread: 60, origin: { x: 0.1, y: 0.6 } });
                    confetti({ particleCount: 80, spread: 60, origin: { x: 0.9, y: 0.6 } });
                    setTimeout(() => {
                        changeScreen(screenReward);
                        rewardVideo.src = `/static/assets/videos/${jawabanBenarId}.mp4`;
                        rewardAudio.src = `/static/assets/audios/${jawabanBenarId}.mp3`;
                        rewardAudio.volume = gameVolume;
                        rewardVideo.play().catch(e => {});
                        rewardAudio.play().catch(e => {});
                    }, 500);
                } else {
                    card.style.animation = "shake 0.3s ease-in-out";
                    setTimeout(() => { card.style.animation = ""; }, 300);
                }
            });
            optionsContainer.appendChild(card);
        });

        resetTimer();
    } catch (error) {
        questionText.innerText = "Gagal memuat soal dari Python server.";
    }
}

function speakText(text) {
    if (!synth) return;
    synth.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "id-ID"; u.volume = gameVolume;
    synth.speak(u);
}

function resetTimer() {
    clearInterval(timerInterval);
    timeLeft = 20;
    timerBadge.innerText = `Waktu: ${timeLeft}s`;
    timerInterval = setInterval(() => {
        timeLeft--;
        timerBadge.innerText = `Waktu: ${timeLeft}s`;
        if (timeLeft <= 0) { clearInterval(timerInterval); generateRound(); }
    }, 1000);
}