from config import DISPOSABLE_DOMAINS, ROLE_BASED_PREFIXES
from utils.caching import mx_cache
import dns.resolver

def is_disposable(email):
    domain = email.split('@')[1].lower()
    return domain in DISPOSABLE_DOMAINS

def is_role_based(email):
    prefix = email.split('@')[0].lower()
    return prefix in ROLE_BASED_PREFIXES

def has_mx_record(domain):
    if domain in mx_cache:
        return mx_cache[domain]
    try:
        answers = dns.resolver.resolve(domain, 'MX', lifetime=3)
        mx_cache[domain] = len(answers) > 0
        return mx_cache[domain]
    except:
        mx_cache[domain] = False
        return False
