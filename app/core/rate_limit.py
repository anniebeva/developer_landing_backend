import time
from collections import defaultdict

requests_storage = defaultdict(list)


def check_rate_limit(
    client_id: str,
    limit: int = 5,
    period: int = 60,
) -> bool:
    """Check if client exceeded request limit."""

    now = time.time()

    requests_storage[client_id] = [
        timestamp
        for timestamp in requests_storage[client_id]
        if now - timestamp < period
    ]

    if len(requests_storage[client_id]) >= limit:
        return False

    requests_storage[client_id].append(now)

    return True
