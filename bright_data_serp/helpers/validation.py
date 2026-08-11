"""Configuration validation utilities."""

__VALID_SEARCH_ENGINES = {"google", "bing", "yandex"}
__VALID_RESPONSE_FORMATS = {"json", "html"}


def validate_configuration(configuration: dict) -> None:
    """
    Validate the configuration dictionary to ensure it contains all required parameters
    and that optional values have the expected types and constraints.

    Args:
        configuration: A dictionary that holds the configuration settings for the connector.

    Raises:
        ValueError: If any required configuration parameter is missing or a value is invalid.
    """
    required_configs = ["api_token", "search_query"]
    for key in required_configs:
        if key not in configuration or not configuration.get(key):
            raise ValueError(f"Missing required configuration value: {key}")

    api_token = configuration.get("api_token")
    if not isinstance(api_token, str):
        raise ValueError("api_token must be a string")

    search_query = configuration.get("search_query")
    if not isinstance(search_query, (str, list)):
        raise ValueError("search_query must be a string or list of strings")
    if isinstance(search_query, list) and (
        not search_query or not all(isinstance(item, str) and item.strip() for item in search_query)
    ):
        raise ValueError("search_query list must contain non-empty strings")

    search_engine = configuration.get("search_engine")
    if search_engine:
        if not isinstance(search_engine, str):
            raise ValueError("search_engine must be a string")
        if search_engine.lower() not in __VALID_SEARCH_ENGINES:
            raise ValueError(
                "search_engine must be one of: "
                f"{', '.join(sorted(__VALID_SEARCH_ENGINES))}"
            )

    response_format = configuration.get("format")
    if response_format:
        if not isinstance(response_format, str):
            raise ValueError("format must be a string")
        if response_format.lower() not in __VALID_RESPONSE_FORMATS:
            raise ValueError(
                f"format must be one of: {', '.join(sorted(__VALID_RESPONSE_FORMATS))}"
            )

    country = configuration.get("country")
    if country:
        if not isinstance(country, str):
            raise ValueError("country must be a string")
        if len(country) != 2 or not country.isalpha():
            raise ValueError("country must be a 2-letter ISO 3166-1 alpha-2 country code")

    search_zone = configuration.get("search_zone")
    if search_zone is not None and search_zone != "":
        if not isinstance(search_zone, str) or not search_zone.strip():
            raise ValueError("search_zone must be a non-empty string")
