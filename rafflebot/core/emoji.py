GOOD_JOB = "👍"
SUCCESS = "✨"
FAILURE = "🔴"
OH_NO = "😭"
WHAT = "⁉️"
DENIED = "🚫"

PRIZE_AWARDED = "🎉"
PRIZE_AVAILABLE = "🎁"
PRIZE_WINNER = "💝"

SETTING = "🛠"


def emoji_status(needle, haystack, match, default=None):
    default = default or FAILURE
    return match if needle in haystack else default
