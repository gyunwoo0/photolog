u"""세션 잘봐라잉."""
# -*- coding: utf-8 -*-
from datetime import timedelta
from uuid import uuid4
from werkzeug.contrib.cache import NullCache, SimpleCache, RedisCache
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin


class CacheSession(CallbackDict, SessionMixin):
    u"""CacheSessionInterface 클래스의 session_class 로 인터페이싱.

    후에 CacheSessionInterface의 open_session 메서드가 호출될때,
    호출자에게 주는 객체다.
    """

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True

        Callbackdict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class CacheSessionInterface(SessionInterface):
    u"""서버 측 세션 구현에 가장 중요한 클래스.

    open_session() 메서드와 save_session() 메서드를 캐시를 이용해 오버라이드 한다.
    """

    session_class = CacheSession

    def __init__(self, cache=None, prefix='cache_session:'):
        if cache is None:
            cache = NullCache()
        self.cache = cache
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_cache_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(day=1)

    def open_session(self, app, request):
        u"""세션을 반환한다.

        이전 요청에 사용된 쿠키값인 sid가 있는지 확인한다.
        sid가 없으면 새로운 요청이므로 새 sid와 그 sid에 대한 세션을 생성한다.
        그리고 세션 저장소로 사용되는 캐시에 지정한 접두어와 sid에 대한 값을 확인하고,
        값이 있으면 그 값으로 세션을 만들어서 요청으로 넘기고,
        캐시에 그 키에 대한 값이 없으면 값이 없는 세션을 생성한다.
        """
        sid = request.cookies.get(app.session_cookie_name)

        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)

        val = self.cache.get(self.prefix + sid)
        if val is not None:
            return self.session_class(val, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        u"""요청이 완료되는 시점에 호출된다.

        세션에 값이 없으면(딕셔너리 형태의 세션에 어떤 값도 없으면),
        캐시에서 그 세션에 대해 저장된 값을 삭제한다.
        그리고 세션에 값도 없으며 그 세션의 내용이 변경됐다면 쿠키를 삭제한다.
        세션의 내용이 변경됐다는 얘기는 세션의 값이 삭제된 경우다.(보통 로그아웃을 하며 세션에 저장된 사용자 정보를 삭제)
        세션에 값이 있는 경우라면 그 값을 다시 캐시에 넣고 만료 시간도 다시 설정한다.
        마지막으로 응답으로 전달할 쿠키와 속성값을 설정한다.
        """
        domain = self.get_cookie_domain(app)

        if not session:
            self.cache.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return

        cache_esp = self.get_cache_expiration_time(app, session)

        val = dict(session)
        self.cache.set(self.prefix + session.sid, val,
                       int(cache_exp.total_seconds()))

        response.set_cookie(app.session_cookie_name,
                            session.sid,
                            httponly=True,
                            domain=domain)


class SimpleCacheSessionInterface(CacheSessionInterface):
    u"""1 process 일때 사용하는 인터페이스.

    포토로그 애플리케이션을 하나의 프로세스에서 운영한다면 간단한 캐시인
    SimpleCache 클래스를 사용하는 이 클래스를 플라스크 애플리케이션의
    session_interface 속성으로 설정.
    """

    def __init__(self):
        SimpleCacheSessionInterface.__init__(self,
                                             cache=SimpleCache(),
                                             prefix="simple_cache_session:")


class RedisCacheSessionInterface(CacheSessionInterface):
    u"""별도의 프로세스나 하나 이상의 애플리케이션에서 세션을 공유하려면 사용.

    NoSQL 서버인 레디스를 캐시로 이용하는 RedisCache 클래스를 세션으로 사용한다.
    """

    def __init__(self, host="localhost", port=6379):
        cache = RedisCache(host=host, port=port)
        CacheSessionInterface.__init__(self,
                                       cache,
                                       prefix="redis_cache_session:")
