class CelebNameNotFound(Exception):
    """Exception raised when a celeb's name is not found."""

    def __init__(self, celeb_id: str):
        self.message = f"Celeb name for {celeb_id} not found."
        super().__init__(self.message)


class CelebPerspectiveNotFound(Exception):
    """Exception raised when a celeb's perspective is not found."""

    def __init__(self, celeb_id: str):
        self.message = f"Celeb perspective for {celeb_id} not found."
        super().__init__(self.message)


class CelebStyleNotFound(Exception):
    """Exception raised when a celeb's style is not found."""

    def __init__(self, celeb_id: str):
        self.message = f"Celeb style for {celeb_id} not found."
        super().__init__(self.message)


class CelebContextNotFound(Exception):
    """Exception raised when a celeb's context is not found."""

    def __init__(self, celeb_id: str):
        self.message = f"Celeb context for {celeb_id} not found."
        super().__init__(self.message)
