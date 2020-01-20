import bcrypt


def generate_password_hash(password, rounds=14, prefix=b'2b'):
    """Generate password hash
    with bcrypt having default prefix being 2b if not parsed.
    Also default log rounds is 14.
    """
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(rounds=rounds, prefix=prefix)).decode('utf-8')


def check_password_hash(hashed, password):
    """To check for password against hash"""
    if bcrypt.checkpw(password.encode(), hashed.encode()):
        return True
    return False