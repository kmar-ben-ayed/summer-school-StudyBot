from app.ai import prompts


def test_general_prompt_contains_question():
    messages = prompts.build_general_prompt("What is a thread?")
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "What is a thread?" in messages[1]["content"]