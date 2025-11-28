'''
Compare various versions of anim_pos function.
'''
def impl_0_3_1(math_exp, mat, inv_mat, speed, min, max, dt):
    '''posani 0.3.1 implementation'''
    p = math_exp(-speed * dt)
    still_going = False

    if min < (diff := mat.x) < max:
        inv_mat.x = mat.x = 0.
    else:
        mat.x = diff = diff * p
        inv_mat.x = -diff
        still_going = True

    if min < (diff := mat.y) < max:
        inv_mat.y = mat.y = 0.
    else:
        mat.y = diff = diff * p
        inv_mat.y = -diff
        still_going = True

    return still_going


def impl_new(math_exp, mat, inv_mat, speed, min, max, dt):
    p = math_exp(-speed * dt)
    still_going = False

    if min < (x := mat.x) < max:
        x = inv_x = 0.
    else:
        x *= p
        inv_x = -x
        still_going = True

    if min < (y := mat.y) < max:
        y = inv_y = 0.
    else:
        y *= p
        inv_y = -y
        still_going = True

    mat.xy = x, y
    inv_mat.xy = inv_x, inv_y

    return still_going


def main():
    import math
    from functools import partial
    from timeit import timeit
    from kivy.graphics import Translate
    from kivy.metrics import dp

    def run_until_animation_ends(impl, dt=1/60):
        while impl(dt):
            pass

    impls = (impl_0_3_1, impl_new)
    for impl in impls:
        impl = partial(impl, math.exp, Translate(100, 600), Translate(800, 200), 10.0, -dp(2),dp(2))
        t = timeit(partial(run_until_animation_ends, impl))
        print(f'{impl.func.__name__:30}: {t} sec')


if __name__ == '__main__':
    main()
