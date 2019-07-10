import app
from routes.index import profile
import cProfile
from pstats import Stats


def profile_request(path, cookie, f):
    a = app.configured_app()
    pr = cProfile.Profile()
    headers = {'Cookie': cookie}

    with a.test_request_context(path, headers=headers):
        pr.enable()

        # r = f()
        # assert type(r) == str, r
        f()

        pr.disable()

    # pr.dump_stats('profile.out')
    # pr.create_stats()
    # s = Stats(pr)
    pr.create_stats()
    s = Stats(pr).sort_stats('cumulative')
    s.dump_stats('profile.pstat')

    s.print_stats('.*bbs.*')
    # s.print_callers()


if __name__ == '__main__':
    path = '/profile'
    cookie = 'session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyX2lkIjoyfQ.XRDPOA.FC8i71rfWvH8__3Lcbx_Jf0YJ9Y'
    profile_request(path, cookie, profile)
