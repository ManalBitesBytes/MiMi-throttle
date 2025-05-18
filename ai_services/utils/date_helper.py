from datetime import datetime


def convert_date_to_format(date_str, target_date_format="%Y-%m-%d"):

    if not date_str:
        return None

    date_str = str(date_str)

    # Define a list of possible date formats
    date_formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y.%m.%d",
        "%d.%m.%Y",
        "%b %d, %Y",
        "%d %b %Y",
        "%Y/%m/%d",
        "%B %d, %Y",
        "%Y-%m",
        "%Y %m",
        "%m %Y",
        "%m/%Y",
        "%Y/%m",
        "%B %Y",
        "%Y %B",
        "%Y",
    ]

    for date_format in date_formats:
        try:
            # Try to parse the date using the current format
            date_obj = datetime.strptime(date_str, date_format)
            # If parsing is successful, format it as "%Y-%m-%d"
            return date_obj.strftime(target_date_format)
        except ValueError:
            # If parsing fails, try the next format
            continue

    # If none of the formats match, raise an error
    return None