from rest_framework.throttling import AnonRateThrottle


class AccountActivationThrottle(AnonRateThrottle):
    rate = '10/day'
