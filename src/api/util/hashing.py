import bcrypt


def hash_password(raw_password: str) -> str:
    """
    generate bcrypt hash from raw password string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(raw_password: str, hashed_password: str) -> bool:
    """
    check if raw password matches stored bcrypt hash
    """
    return bcrypt.checkpw(
        raw_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )