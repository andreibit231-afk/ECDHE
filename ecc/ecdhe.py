import secrets
from typing import Optional, Tuple

class EllipticCurve:
    def __init__(self, name: str, p: int, a: int, b: int,
                 g: Tuple[int, int], n: int, h: int):
        self.name = name
        self.p = p
        self.a = a
        self.b = b
        self.g = g
        self.n = n
        self.h = h

    def is_on_curve(self, point: Optional['Point']) -> bool:
        if point is None:
            return True

        x, y = point.x, point.y
        left_side = (y * y) % self.p
        right_side = (x * x * x + self.a * x + self.b) % self.p

        return left_side == right_side

    def generate_keypair(self) -> Tuple[int, 'Point']:
        secret_key = secrets.randbelow(self.n - 1) + 1
        public_key = self.g_point * secret_key
        return secret_key, public_key

    @property
    def g_point(self) -> 'Point':
        return Point(self.g[0], self.g[1], self)


class Point:
    def __init__(self, x: Optional[int], y: Optional[int], curve: EllipticCurve):
        self.x = x
        self.y = y
        self.curve = curve

    def is_infinity(self) -> bool:
        return self.x is None and self.y is None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        if self.is_infinity() and other.is_infinity():
            return True
        return self.x == other.x and self.y == other.y

    def __neg__(self) -> 'Point':
        if self.is_infinity():
            return self
        return Point(self.x, (-self.y) % self.curve.p, self.curve)

    def __add__(self, other: 'Point') -> 'Point':
        if self.curve != other.curve:
            raise ValueError("Points belong to different curves")

        if self.is_infinity():
            return other
        if other.is_infinity():
            return self

        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y

        if x1 == x2 and y1 != y2:
            return Point(None, None, self.curve)

        if x1 == x2 and y1 == y2:
            numerator = (3 * x1 * x1 + self.curve.a)
            denominator = (2 * y1)
        else:
            numerator = (y1 - y2)
            denominator = (x1 - x2)

        slope = (numerator * mod_inverse(denominator, self.curve.p)) % self.curve.p

        x3 = (slope * slope - x1 - x2) % self.curve.p
        y3 = (slope * (x1 - x3) - y1) % self.curve.p

        return Point(x3, y3, self.curve)

    def __rmul__(self, scalar: int) -> 'Point':
        if scalar == 0 or self.is_infinity():
            return Point(None, None, self.curve)

        if scalar < 0:
            return -((-scalar) * self)

        result = Point(None, None, self.curve)
        addend = self

        while scalar:
            if scalar & 1:
                result = result + addend
            addend = addend + addend
            scalar >>= 1

        return result

    def __mul__(self, scalar: int) -> 'Point':
        return self.__rmul__(scalar)

    def __repr__(self) -> str:
        if self.is_infinity():
            return "Point(Infinity)"
        return f"Point(0x{self.x:x}, 0x{self.y:x})"


def mod_inverse(k: int, p: int) -> int:
    if k == 0:
        raise ZeroDivisionError("Division by zero")

    if k < 0:
        return p - mod_inverse(-k, p)

    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x = old_r, old_s

    assert gcd == 1, "Inverse does not exist"
    assert (k * x) % p == 1

    return x % p



SECP256K1 = EllipticCurve(
    name='secp256k1',
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    a=0,
    b=7,
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    h=1,
)


if __name__ == '__main__':
    print(f'Кривая: {SECP256K1.name}')
    print('-' * 60)

    # 1. Алиса генерирует свою пару ключей
    alice_secret, alice_public = SECP256K1.generate_keypair()
    print(f"Секретный ключ Алисы: 0x{alice_secret:x}")
    print(f"Публичный ключ Алисы:   {alice_public}")

    # 2. Боб генерирует свою пару ключей
    bob_secret, bob_public = SECP256K1.generate_keypair()
    print(f"Секретный ключ Боба:    0x{bob_secret:x}")
    print(f"Публичный ключ Боба:    {bob_public}")
    print('-' * 60)

    # 3. Обмен публичными ключами и вычисление общего секрета
    # Алиса вычисляет: Secret = AliceSecret * BobPublic
    shared_secret_alice = alice_public * bob_secret
    
    # Боб вычисляет: Secret = BobSecret * AlicePublic
    shared_secret_bob = bob_public * alice_secret

    # 4. Проверка совпадения общих секретов
    assert shared_secret_alice == shared_secret_bob, "Ошибка: общие секреты не совпадают!"
    
    # Проверка, что точка лежит на кривой
    assert SECP256K1.is_on_curve(shared_secret_alice), "Ошибка: общая точка не на кривой"

    print("Общий секрет (Shared Secret):")
    print(f"  X: 0x{shared_secret_alice.x:x}")
    print(f"  Y: 0x{shared_secret_alice.y:x}")
    print('-' * 60)
    print("Успешно: протокол ECDHE завершен.")