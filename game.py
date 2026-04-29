"""Out the Window - a simple text-based throwing game."""

import random

OBJECTS = [
    "textbook",
    "pencil",
    "backpack",
    "laptop",
    "homework assignment",
    "calculator",
    "eraser",
    "binder",
]

LANDING_SPOTS = [
    "the parking lot",
    "a puddle",
    "a bush",
    "someone's car",
    "the principal's head",
    "the gym roof",
    "a trash can (perfect score!)",
    "the flagpole",
]


def throw_object(obj: str, spot: str, floor: int) -> dict:
    """Simulate throwing an object out a window.

    Args:
        obj: The object being thrown.
        spot: Where the object lands.
        floor: Which floor the window is on (1-5).

    Returns:
        A dict with 'object', 'spot', 'floor', and 'score' keys.
    """
    base_score = floor * 10
    bonus = 50 if "perfect" in spot else 0
    score = base_score + bonus + random.randint(0, 20)
    return {"object": obj, "spot": spot, "floor": floor, "score": score}


def play_round(floor: int = 1) -> dict:
    """Play a single round by randomly picking an object and a landing spot.

    Args:
        floor: Which floor to throw from (1-5).

    Returns:
        The result dict from :func:`throw_object`.
    """
    obj = random.choice(OBJECTS)
    spot = random.choice(LANDING_SPOTS)
    return throw_object(obj, spot, floor)


def format_result(result: dict) -> str:
    """Return a human-readable description of a throw result.

    Args:
        result: A result dict as returned by :func:`throw_object`.

    Returns:
        A formatted string describing the throw.
    """
    return (
        f"You threw your {result['object']} from floor {result['floor']} "
        f"and it landed on {result['spot']}. "
        f"Score: {result['score']}"
    )


def run_game(rounds: int = 3) -> int:
    """Run the full game for a given number of rounds.

    Args:
        rounds: Number of rounds to play.

    Returns:
        The total score accumulated across all rounds.
    """
    print("=== Out the Window ===")
    print("Time to throw your school supplies!\n")

    total_score = 0
    for i in range(1, rounds + 1):
        floor = random.randint(1, 5)
        result = play_round(floor)
        print(f"Round {i}: {format_result(result)}")
        total_score += result["score"]

    print(f"\nGame over! Total score: {total_score}")
    return total_score


if __name__ == "__main__":
    run_game()
