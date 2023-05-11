from loader import dp
from .admins import AdminFilter
from .group_filter import IsGroupChat
from .private_chat import IsPrivate


if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroupChat)
    dp.filters_factory.bind(IsPrivate)
    pass
