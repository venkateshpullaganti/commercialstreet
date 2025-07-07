from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination



class DefaultPagination(LimitOffsetPagination):
    page_size=10
    default_limit = 10
    