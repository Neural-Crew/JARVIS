"""Gestion du débit (Rate Limiting) pour les appels aux modèles.

Ce module définit des stratégies de limitation de débit pour éviter de dépasser
les quotas des fournisseurs (ex: Mistral AI Free Plan).
"""

from langchain_core.rate_limiters import InMemoryRateLimiter

# Rate limiter pour le plan gratuit Mistral (1 req/sec).
# requests_per_second=0.5 : pour plus de sécurité.
mistral_rate_limiter: InMemoryRateLimiter = InMemoryRateLimiter(
    requests_per_second=0.5,
    check_every_n_seconds=0.1,
    max_bucket_size=1,
)
