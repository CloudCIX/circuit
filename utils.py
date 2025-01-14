# stdlib
from typing import List
# libs
from cloudcix.api.membership import Membership
from jaeger_client import Span
from rest_framework.request import Request
# local


def get_addresses_in_member(request: Request, span: Span) -> List[int]:
    """
    Given a token, make requests to Membership to fetch all the Addresses in the Member that the token is from
    """
    params = {
        'page': 0,
        'limit': 50,
        'search[member_id]': request.user.member['id'],
    }
    response = Membership.address.list(
        token=request.user.token,
        params=params,
        span=span,
    )
    address_ids = [a['id'] for a in response.json()['content']]

    total_records = response.json()['_metadata']['total_records']
    while len(address_ids) < total_records:  # pragma: no cover
        params['page'] += 1
        response = Membership.address.list(
            token=request.user.token,
            params=params,
            span=span,
        )
        address_ids.extend([a['id'] for a in response.json()['content']])

    return address_ids
