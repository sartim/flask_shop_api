# Redis Session Key
SESSION = 'session'


class Version:
    """API versions urls"""
    V1_URL = 'api/v1'
    V2_URL = 'api/v2'


class Role:
    """Account roles"""
    ADMIN = 'ADMIN'
    SUPERUSER = 'SUPERUSER'


class Status:
    """Article status constants"""
    DRAFT = 1
    PENDING = 2
    REVIEW = 3
    REJECTED = 4
    PUBLISHED = 5
    DELETED = 6


class Location:
    """Locations"""
    ALL = 1
    NATIONAL = 2
    GARISSA = 3
    KIAMBU = 4
    NAIROBI = 5
    KIBERA = 6
    KISII = 7
    KISUMU= 8
    MACHAKOS = 9
    MOMBASA = 10
    NAKURU = 11
    NYAMIRA = 12
    UASIN_GISHU = 13


class Category:
    """Categories"""
    POLITICS = 1
    OPINION = 2
    BUSINESS = 3
    AGRICULTURE = 4
    CRIME = 5
    SPORT = 6
    ENTERTAINMENT = 7
    EVENT = 8
    EDUCATION = 9
    TRANSPORT = 10
    HEALTH = 11
    NEWS = 12
    ENVIRONMENT = 13
    RANDOM = 14
    TUBONGE = 15
    LIFESTYLE = 16


class Type:
    """Article body type constants"""
    TEXT_BODY_TYPE = 1
    HTML_BODY_TYPE = 2
    MARKDOWN_BODY_TYPE = 3


class ProfileConstants:
    """Profile processor constants"""
    INDEX = 'profiles'
    SIZE = 5000
    BODY = {}


class ArticleConstants:
    """Article processor constants"""
    INDEX = 'articles'
    SIZE = 2000
    BODY = {
    }
