from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from collections import OrderedDict
from rest_framework.response import Response

class LimitOffsetTPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class PageNumberTPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
            ('status', 'success'),
            ('message', "News List")
        ]))

