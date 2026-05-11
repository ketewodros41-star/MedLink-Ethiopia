import re
import unicodedata


def normalize_text(value: str) -> str:
    base = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-zA-Z0-9]+", " ", base.casefold())
    return re.sub(r"\s+", " ", cleaned).strip()
