import random
import time

from google.genai import errors


def generate_with_retry(
    client,
    model: str,
    contents: str,
    config=None,
    max_attempts: int = 3,
):
    """
    Call Gemini with retry handling for
    temporary server errors and rate limits.
    """

    for attempt in range(1, max_attempts + 1):
        try:
            kwargs = {
                "model": model,
                "contents": contents,
            }

            if config is not None:
                kwargs["config"] = config

            return client.models.generate_content(
                **kwargs
            )

        except (errors.ServerError, errors.ClientError) as error:
            status_code = getattr(error, "code", None)

            # Retry only temporary errors
            if status_code not in (
                429, 500, 502, 503, 504
            ):
                raise

            if attempt == max_attempts:
                raise RuntimeError(
                    f"Gemini request failed after "
                    f"{max_attempts} attempts. "
                    f"Last status: {status_code}"
                ) from error

            # Exponential backoff with jitter
            delay = min(2 ** attempt, 30)
            delay += random.uniform(0, 1)

            print(
                f"[Gemini] Status {status_code}. "
                f"Retry {attempt}/{max_attempts - 1} "
                f"in {delay:.1f}s..."
            )

            time.sleep(delay)
