from langchain_core.rate_limiters import InMemoryRateLimiter

# Rate limiter pour le free plan Mistral (1 req/sec).
# Utilise le token bucket natif de LangChain, intégré directement
# dans le modèle via le paramètre `rate_limiter`.
# - requests_per_second=0.8 : légèrement sous 1 req/s pour garder une marge
# - check_every_n_seconds=0.1 : vérifie toutes les 100ms si un token est dispo
# - max_bucket_size=5 : autorise un petit burst si le bucket s'est rempli
mistral_rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.5,
    check_every_n_seconds=0.1,
    max_bucket_size=1,
)
