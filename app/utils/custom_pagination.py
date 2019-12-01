from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        try:
            custom = data.get('custom', True)
        except AttributeError:
            custom = True
        limit = self.limit
        count = self.count
        offset = self.offset
        current_page = int(offset / limit) + 1
        total_page = int(count / limit) + (0 if count % limit == 0 else 1)
        _data = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': count,
            'current': current_page,
            'total': total_page,
            'filter': self.request.GET,
            '_next': self.get_next_page(),
            '_previous': self.get_previous_page()
        }
        if custom:
            _data.update({
                "status": True,
                "code": status.HTTP_200_OK,
                "message": "",
                'data': data
            })
        else:
            _data.update(data)
        return Response(_data)

    def get_next_page(self):
        if self.get_next_link():
            return {
                'limit': self.limit,
                'offset': self.offset + self.limit
            }
        else:
            return {}

    def get_previous_page(self):
        if self.get_previous_link():
            return {
                'limit': self.limit,
                'offset': self.offset - self.limit
            }
        else:
            return {}
