// script.js

let playerHand = [];
let cpuHand = [];
let graveyard = [];
let deck = [];

const cardDescriptions = {
    "Fire": "炎:互いの手札から1種類を指定して燃やす（墓地に捨てる）ことが出来る。",
    "Wind": "風:相手の手札から1枚をランダムで墓地に飛ばす（墓地に捨てる）ことが出来る。",
    "Thief": "盗み:相手の場所を1箇所指定してその場所にあるカードを奪って手札に加える事が出来る。",
    "Water": "水:このカードは攻撃魔法カードの効果を一切受けない。",
    "Guardian": "守護者:このカードは攻撃魔法カードの効果を一切受けない。",
    "Freeze": "吹雪:相手を凍らせる。相手は次のターンを1度飛ばされ、もう一度君がカードを引くことが出来る。",
    "Open": "開示:相手の手札カードの場所をすべて見ることが出来る。",
    "Double": "二倍:次のターン、相手に2枚カードを引かれる。",
    "Declare": "宣言:このカードを墓地に送ったとき、何ターン目に試合が終わるかを予想し、宣言通り試合が終了した場合には勝利する。",
    "Rotate": "入れ替え:このカードが2枚そろって墓地に捨てられた瞬間、自分と相手の手札のカードをすべて交換する。",
    "Road_to_win": "勝利への道:このカードを墓地に送ったとき、自分がJokerを持っていた場合相手に渡す。",
    "Road_to_lose": "敗北への道:このカードを墓地に送ったとき、相手がJokerを持っている場合Jokerを受け取る。",
    "Joker": "道化師:最後に所持していた場合、原則負ける。"
};

function initializeGame() {
    deck = [
        "Fire", "Water", "Freeze", "Wind", "Thief", "Guardian", "Open", "Rotate", "Double", "Declare", "Road_to_win", "Road_to_lose",
        "Fire", "Water", "Freeze", "Wind", "Thief", "Guardian", "Open", "Rotate", "Double", "Declare", "Road_to_win", "Road_to_lose",
        "Fire", "Water", "Freeze", "Wind", "Thief", "Guardian", "Open", "Rotate", "Double", "Declare", "Road_to_win", "Road_to_lose",
        "Fire", "Water", "Freeze", "Wind", "Thief", "Guardian", "Open", "Rotate", "Double", "Declare", "Road_to_win", "Road_to_lose",
        "Joker"
    ];
    shuffle(deck);
    dealCards();
    updateHands();
}

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function dealCards() {
    playerHand = [];
    cpuHand = [];
    graveyard = [];
    for (let i = 0; i < deck.length; i++) {
        if (i % 2 === 0) {
            playerHand.push(deck[i]);
        } else {
            cpuHand.push(deck[i]);
        }
    }
}

function updateHands() {
    const playerHandElement = document.getElementById("player-hand");
    const cpuHandElement = document.getElementById("cpu-hand");
    playerHandElement.innerHTML = "";
    cpuHandElement.innerHTML = "";

    playerHand.forEach(card => {
        const cardElement = document.createElement("div");
        cardElement.className = "card";
        cardElement.textContent = card;
        cardElement.title = cardDescriptions[card];
        playerHandElement.appendChild(cardElement);
    });

    cpuHand.forEach(() => {
        const cardElement = document.createElement("div");
        cardElement.className = "card hidden";
        cpuHandElement.appendChild(cardElement);
    });
}

// ゲーム開始時はページを移動することにしたから、その時に小津さするか確認する
document.getElementById("start-game").addEventListener("click", initializeGame);
