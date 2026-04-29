"""Tests for the Out the Window game."""

import pytest

from game import LANDING_SPOTS, OBJECTS, format_result, play_round, throw_object


class TestThrowObject:
    def test_returns_correct_keys(self):
        result = throw_object("textbook", "the parking lot", 3)
        assert set(result.keys()) == {"object", "spot", "floor", "score"}

    def test_object_and_spot_preserved(self):
        result = throw_object("pencil", "a puddle", 2)
        assert result["object"] == "pencil"
        assert result["spot"] == "a puddle"
        assert result["floor"] == 2

    def test_score_increases_with_floor(self):
        # Higher floor should yield a higher base score.
        scores_floor1 = [throw_object("eraser", "a bush", 1)["score"] for _ in range(50)]
        scores_floor5 = [throw_object("eraser", "a bush", 5)["score"] for _ in range(50)]
        assert min(scores_floor5) > max(scores_floor1) or (
            sum(scores_floor5) > sum(scores_floor1)
        )

    def test_perfect_spot_bonus(self):
        # "trash can (perfect score!)" contains the word "perfect" → +50 bonus.
        without_bonus = [throw_object("binder", "a bush", 1)["score"] for _ in range(100)]
        with_bonus = [
            throw_object("binder", "a trash can (perfect score!)", 1)["score"]
            for _ in range(100)
        ]
        assert min(with_bonus) > max(without_bonus)

    def test_score_is_non_negative(self):
        result = throw_object("calculator", "the gym roof", 1)
        assert result["score"] >= 0


class TestPlayRound:
    def test_object_in_known_list(self):
        result = play_round(floor=2)
        assert result["object"] in OBJECTS

    def test_spot_in_known_list(self):
        result = play_round(floor=2)
        assert result["spot"] in LANDING_SPOTS

    def test_floor_preserved(self):
        for floor in range(1, 6):
            result = play_round(floor=floor)
            assert result["floor"] == floor


class TestFormatResult:
    def test_contains_object(self):
        result = {"object": "laptop", "spot": "the flagpole", "floor": 4, "score": 77}
        text = format_result(result)
        assert "laptop" in text

    def test_contains_spot(self):
        result = {"object": "laptop", "spot": "the flagpole", "floor": 4, "score": 77}
        text = format_result(result)
        assert "flagpole" in text

    def test_contains_floor(self):
        result = {"object": "laptop", "spot": "the flagpole", "floor": 4, "score": 77}
        text = format_result(result)
        assert "4" in text

    def test_contains_score(self):
        result = {"object": "laptop", "spot": "the flagpole", "floor": 4, "score": 77}
        text = format_result(result)
        assert "77" in text
