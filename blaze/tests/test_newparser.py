import unittest
from unittest import skip

from blaze.datashape.parser import load_parser

tests = []

#------------------------------------------------------------------------

class TestNewParser(unittest.TestCase):

    def test_all_the_strings(self):
        parse = load_parser()
        parse('a')
        parse('a, b')
        parse('a, b, c')
        parse('a,      b')
        parse('a,      b  ,     d')
        parse('800, 600, RGBA')
        parse('type foo = c')
        parse('type foo    =    c')
        parse('type a b c = d,e,f')
        parse('type   a b c = d, e   ')
        parse('type foo a b = c, d')
        parse('type foo a b = c,d,e')
        parse('type foo a b = c,d,e,   f')
        parse('type foo a b = c,   d,   e,   f')
        parse('type foo b = c,   d,   e,   f')
        parse('type a b c = d, e')
        parse('type a b c = bar, foo')
        parse('type bar A = A')
        parse('type bar A = A, B')
        parse('type bar A = 800, 600, A, A')
        parse('type bar A B = 800, 600, A, B')
        parse('type bar A B = {}')
        parse('type bar A B = {A:B}')

        #parse('type baz = F(A,B)')
        #parse('type baz = F(A,F(A))')

        parse('''
        type foo = {
            A: B;
            C: D;
            E: (A,B)
        }
        ''')

        parse('''
        type bar a b = {
            A : B;
            C : D;
            E : (a,b)
        }
        ''')

        parse('type empty = {} ')

        parse('''
        type Stock = {
          name   : string;
          min    : int64;
          max    : int64;
          mid    : int64;
          volume : float;
          close  : float;
          open   : float
        }
        ''')

    def test_trailing_semi(self):
        parse = load_parser()
        a = parse('''
        type a = {
            a: int;
            b: float;
            c: (5,int32)
        }
        ''')

        b = parse('''
        type a = {
            a: int;
            b: float;
            c: (5,int32);
        }
        ''')

        assert a == b

    def test_multiline(self):
        parse = load_parser()
        a = parse('''

        type f a = b
        type g a = b

        type a = {
            a: int;
            b: float;
            c: (5,int32);
        }

        ''')

    def test_inline(self):
        parse = load_parser()
        a = parse('''
        type Point = {
            x : int32;
            y : int32
        }

        type Space = {
            a: Point;
            b: Point
        }

        ''')

        a = parse('''
        type Person = {
            name   : string;
            age    : int;
            height : int;
            weight : int
        }

        type RGBA = {
            r: int32;
            g: int32;
            b: int32;
            a: int8
        }
        ''')

    def test_nested(self):
        parse = load_parser()
        a = parse('''
        type Space = {
            a: { x: int; y: int };
            b: { x: int; y: int }
        }
        ''')

    def test_parameterized(self):
        parse = load_parser()
        a = parse('''
        type T x y = {
            a: x;
            b: y
        }
        ''')

    def test_option(self):
        parse = load_parser()
        a = parse(''' Option(int32) ''')

    def test_union(self):
        parse = load_parser()
        a = parse(''' Union(a,b,c,d) ''')

    def test_either1(self):
        parse = load_parser()
        a = parse(''' Either(int32, float32) ''')

    def test_either2(self):
        parse = load_parser()
        a = parse(''' Either({x: int}, {y: float}) ''')

    @skip('')
    def test_either3(self):
        parse = load_parser()
        a = parse(''' Either( (2, 2, T), (T, 2, int) ) ''')

    def test_stress(self):
        parse = load_parser()
        parse('type big = Union(Union(Union(Union(Union(Union(Union(Union(x)))))))) ')
        parse('type big = {x:{x:{x:{x:{x:{x:{x:{x:{x:{x:int32}}}}}}}}}}')

        # whitespace insensitivity
        parse('''type big = {
                x:{         x
                    :{
                            x:
                {x:{x:
                    {x:{x:{  x:{x
            :{x
            :int32
                }}}
                    }}    }}}}}
        ''')

tests.append(TestNewParser)

#------------------------------------------------------------------------

def run(verbosity=1, repeat=1):
    suite = unittest.TestSuite()
    for cls in tests:
        for _ in range(repeat):
            suite.addTest(unittest.makeSuite(cls))

    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)

if __name__ == '__main__':
    run()
