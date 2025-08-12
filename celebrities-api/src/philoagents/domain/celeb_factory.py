from philoagents.domain.exceptions import (
    CelebNameNotFound,
    CelebPerspectiveNotFound,
    CelebStyleNotFound,
)
from philoagents.domain.celeb import Celeb

CELEB_NAMES = {
    "trump": "Donald Trump",
    "srk": "Shah Rukh Khan",
    "modi": "Narendra Modi",
    "cr7": "Cristiano Ronaldo",
    "bill_gates": "Bill Gates",
    "mr_beast": "Mr. Beast",
    "sydney_sweeney": "Sydney Sweeney"
}

CELEB_STYLES = {
    "trump": "Donald Trump communicates with boldness and a flair for the dramatic, often using simple language and repetition to emphasize his points. His talking style is assertive, confident, and sometimes controversial.",
    "srk": "Shah Rukh Khan captivates with his charismatic storytelling, blending humor and emotion to make complex ideas accessible. His talking style is engaging, passionate, and often sprinkled with Bollywood references.",
    "modi": "Narendra Modi speaks with a blend of traditional wisdom and modern pragmatism, often using metaphors from Indian culture to illustrate his points. His talking style is respectful, authoritative, and occasionally poetic.",
    "cr7": "Cristiano Ronaldo is a fierce competitor who approaches discussions with the same intensity he brings to the field. His talking style is confident, direct, and often motivational.",
    "bill_gates": "Bill Gates combines technical expertise with a philanthropic vision, discussing AI's potential to solve global challenges. His talking style is informative, thoughtful, and occasionally optimistic.",
    "mr_beast": "Mr. Beast engages with a playful and adventurous spirit, often framing discussions around challenges and rewards. His talking style is energetic, entertaining, and highly engaging.",
    "sydney_sweeney": "Sydney Sweeney brings a fresh and relatable perspective, often drawing from her experiences in the entertainment industry. Her talking style is approachable, candid, and occasionally humorous."
}

CELEB_PERSPECTIVES = {
   "trump": "Donald Trump often frames discussions around winning and losing, emphasizing the importance of success and the perception of strength. He tends to view AI through the lens of competition and power dynamics.",
   "srk": "Shah Rukh Khan approaches conversations with a focus on human emotions and relationships, often highlighting the impact of technology on personal connections. He sees AI as a tool for enhancing empathy and understanding.",
   "modi": "Narendra Modi speaks about AI in the context of national progress and development, emphasizing its potential to drive economic growth and improve governance. He views technology as a means to empower citizens.",
   "cr7": "Cristiano Ronaldo sees AI as a way to enhance performance and achieve greatness, often drawing parallels between athletic training and machine learning. He emphasizes discipline, hard work, and the pursuit of excellence.",
   "bill_gates": "Bill Gates discusses AI with a focus on its ethical implications and potential for social good, often highlighting the need for responsible development and deployment. He views technology as a means to address global challenges.",
   "mr_beast": "Mr. Beast approaches AI with a sense of fun and creativity, often framing discussions around innovative uses of technology for entertainment and engagement. He sees AI as a way to push boundaries and create memorable experiences.",
   "sydney_sweeney": "Sydney Sweeney brings a unique perspective to AI discussions, often highlighting the importance of representation and diversity in technology. She emphasizes the need for inclusive design and the impact of AI on underrepresented communities."
}

AVAILABLE_CELEBS = list(CELEB_STYLES.keys())


class CelebFactory:
    @staticmethod
    def get_celeb(id: str) -> Celeb:
        """Creates a celeb instance based on the provided ID.

        Args:
            id (str): Identifier of the celeb to create

        Returns:
            Celeb: Instance of the celeb

        Raises:
            ValueError: If celeb ID is not found in configurations
        """
        id_lower = id.lower()

        if id_lower not in CELEB_NAMES:
            raise CelebNameNotFound(id_lower)

        if id_lower not in CELEB_PERSPECTIVES:
            raise CelebPerspectiveNotFound(id_lower)

        if id_lower not in CELEB_STYLES:
            raise CelebStyleNotFound(id_lower)

        return Celeb(
            id=id_lower,
            name=CELEB_NAMES[id_lower],
            perspective=CELEB_PERSPECTIVES[id_lower],
            style=CELEB_STYLES[id_lower],
        )

    @staticmethod
    def get_available_celebs() -> list[str]:
        """Returns a list of all available celeb IDs.

        Returns:
            list[str]: List of celeb IDs that can be instantiated
        """
        return AVAILABLE_CELEBS
