class Name:
    def __init__(self, value: str):
        if not value:
            raise ValueError("name must not be empty")
        forbidden_words = ["禁止", "NG", "不適切"]
        for word in forbidden_words:
            if word in value:
                raise ValueError(f"name must not contain forbidden word: {word}")
        self.value = value

class Description:
    def __init__(self, value: str):
        if len(value) > 255:
            raise ValueError("description must be 255 characters or less")
        self.value = value
