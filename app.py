
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


# Returns the correct emoji for a given move.
def findIcon(move):
    icons = {
        "rock": "✊",
        "paper": "✋",
        "scissors": "✌️"
    }

    return icons.get(move, "❔")


# Randomly selects one of the three possible moves.
def randomChoose():
    choices = ["rock", "paper", "scissors"]

    return random.choice(choices)


# Determines the winner based on both players' moves.
def decideWinner(player, computer):

    # If both moves are identical, the round is a tie.
    if player == computer:
        return "tie"

    # Check all three combinations in which the player wins.
    elif (
        (player == "rock" and computer == "scissors")
        or
        (player == "paper" and computer == "rock")
        or
        (player == "scissors" and computer == "paper")
    ):
        return "player"

    # If neither a tie nor a player victory occurs,
    # the computer must have won.
    else:
        return "computer"


# Stores the scores while the server is running.
player_score = 0
computer_score = 0
ties = 0


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/play", methods=["POST"])
def play():
    global player_score, computer_score, ties

    data = request.get_json()
    player = data["move"]

    # Validate the player's selection.
    if player not in ["rock", "paper", "scissors"]:
        return jsonify({"error": "Invalid move"}), 400

    computer = randomChoose()

    # Determine the outcome.
    winner = decideWinner(player, computer)

    if winner == "player":
        player_score += 1
        message = "You won this round!"

    elif winner == "computer":
        computer_score += 1
        message = "The computer won this round!"

    else:
        ties += 1
        message = "It's a tie!"

    return jsonify({
        "player": player,
        "computer": computer,
        "player_icon": findIcon(player),
        "computer_icon": findIcon(computer),
        "winner": winner,
        "message": message,
        "player_score": player_score,
        "computer_score": computer_score,
        "ties": ties
    })


@app.route("/reset", methods=["POST"])
def reset():
    global player_score, computer_score, ties

    player_score = 0
    computer_score = 0
    ties = 0

    return jsonify({
        "player_score": 0,
        "computer_score": 0,
        "ties": 0
    })


if __name__ == "__main__":
    app.run(debug=True)
