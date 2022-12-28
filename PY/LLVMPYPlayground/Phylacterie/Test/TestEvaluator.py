

class TestEvaluator(unittest.TestCase):
    def test_var_expr(self):
        e = KaleidoscopeEvaluator()
        e.evaluate('''
            def foo(x y z)
                var s1 = x + y, s2 = z + y in
                    s1 * s2
            ''')
        self.assertEqual(e.evaluate('foo(1, 2, 3)'), 15)

        e = KaleidoscopeEvaluator()
        e.evaluate('def binary : 1 (x y) y')
        e.evaluate('''
            def foo(step)
                var accum in
                    (for i = 0, i < 10, step in
                        accum = accum + i) : accum
            ''')
        # Note that Kaleidoscope's 'for' loop executes the last iteration even
        # when the condition is no longer fulfilled after the step is done.
        # 0 + 2 + 4 + 6 + 8 + 10
        self.assertEqual(e.evaluate('foo(2)'), 30)

    def test_nested_var_exprs(self):
        e = KaleidoscopeEvaluator()
        e.evaluate('''
            def foo(x y z)
                var s1 = x + y, s2 = z + y in
                    var s3 = s1 * s2 in
                        s3 * 100
            ''')
        self.assertEqual(e.evaluate('foo(1, 2, 3)'), 1500)

    def test_assignments(self):
        e = KaleidoscopeEvaluator()
        e.evaluate('def binary : 1 (x y) y')
        e.evaluate('''
            def foo(a b)
                var s, p, r in
                   s = a + b :
                   p = a * b :
                   r = s + 100 * p :
                   r
            ''')
        self.assertEqual(e.evaluate('foo(2, 3)'), 605)
        self.assertEqual(e.evaluate('foo(10, 20)'), 20030)

    def test_compiling_to_object_code(self):
        e = KaleidoscopeEvaluator()
        e.evaluate('def adder(a b) a + b')
        obj = e.compile_to_object_code()
        obj_format = llvm.get_object_format()
        
        # Check the magic number of object format.
        elf_magic = b'\x7fELF'
        macho_magic = b'\xfe\xed\xfa\xcf'
        if obj[:4] == elf_magic:
            self.assertEqual(obj_format, 'ELF')
        elif obj[:4] == macho_magic:
            self.assertEqual(obj_format, 'MachO')
        else:
            # There are too many variations of COFF magic number.
            # Assume all other formats are COFF.
            self.assertEqual(obj_format, 'COFF')
