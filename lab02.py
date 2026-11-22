"""Lab 02 — Control flow, functions, errors and modules.

Lab manual: docs/labs/lab02-control-flow-functions.md
Tests:      tests/test_lab02.py

    pytest tests/test_lab02.py -v

Replace each `raise NotImplementedError` with your own code. When a docstring
says "raise ValueError", the tests check that you do — use
`raise ValueError("a message that says what was wrong")`.
"""

# -- decisions --------------------------------------------------------------


def classify_triangle(a, b, c):
    """Classify a triangle based on its side lengths."""

    # التأكد أن أطوال الأضلاع موجبة
    if a <= 0 or b <= 0 or c <= 0:
        raise ValueError("Sides must be positive")

    # التأكد أن الأضلاع تحقق شروط تكوين المثلث
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("Invalid triangle")

    # لو الأضلاع الثلاثة متساوية
    if a == b == c:
        return "equilateral"

    # لو ضلعان متساويان على الأقل
    elif a == b or a == c or b == c:
        return "isosceles"

    # لو الأضلاع الثلاثة مختلفة
    else:
        return "scalene"
    
    """Name the triangle with side lengths a, b, c.

    Return "equilateral" (three equal sides), "isosceles" (exactly two) or
    "scalene" (none).

    Raise ValueError if any side is not positive, or if the sides break the
    triangle inequality: each side must be strictly shorter than the sum of
    the other two.

    classify_triangle(3, 3, 3)  -> "equilateral"
    classify_triangle(3, 3, 5)  -> "isoscelescals"
    classify_triangle(3, 4, 5)  -> "ene"
    classify_triangle(1, 2, 3)  -> ValueError   (1 + 2 is not > 3)
    """
    

def course_result(coursework, final, attendance):
    # التأكد من أن الدرجات ونسبة الحضور في النطاق الصحيح
    if not 0 <= coursework <= 40:
        raise ValueError("Invalid coursework grade")

    if not 0 <= final <= 60:
        raise ValueError("Invalid final exam grade")

    if not 0 <= attendance <= 100:
        raise ValueError("Invalid attendance percentage")

    # الطالب ممنوع من دخول الامتحان لو نسبة حضوره أقل من 75%
    if attendance < 75:
        return "barred"

    # لازم الطالب يحصل على 30% على الأقل من درجة النهائي
    if final < 18:
        return "fail"

    # مجموع درجات الطالب
    total = coursework + final

    # النجاح يتطلب مجموع 60 على الأقل
    if total >= 60:
        return "pass"

    return "fail"
    """Apply this course's pass rules to one student.

    coursework  marks out of 40
    final       marks out of 60
    attendance  percentage of sessions attended, 0 to 100

    Return, checking in this order:
        "barred"  if attendance is below 75       (محروم — no final exam)
        "fail"    if final is below 18            (under 30% of the final)
        "fail"    if coursework + final is below 60
        "pass"    otherwise

    Raise ValueError if any argument is outside its range.

    course_result(35, 25, 90)  -> "pass"
    course_result(38, 15, 100) -> "fail"     total 53, and final under 18
    course_result(40, 60, 70)  -> "barred"
    """



# -- loops ------------------------------------------------------------------


def fizzbuzz(n):
    # إنشاء قائمة لتخزين النتائج
    result = []

    # المرور على الأرقام من 1 إلى n
    for i in range(1, n + 1):
        # الأرقام التي تقبل القسمة على 3 و5
        if i % 3 == 0 and i % 5 == 0:
            result.append("FizzBuzz")

        # الأرقام التي تقبل القسمة على 3 فقط
        elif i % 3 == 0:
            result.append("Fizz")

        # الأرقام التي تقبل القسمة على 5 فقط
        elif i % 5 == 0:
            result.append("Buzz")

        # تحويل الأرقام العادية إلى نصوص
        else:
            result.append(str(i))

    # إرجاع القائمة
    return result
    """The FizzBuzz sequence from 1 to n, as a list of strings.

    Multiples of 3 -> "Fizz", of 5 -> "Buzz", of both -> "FizzBuzz",
    anything else -> the number itself as a string.

    fizzbuzz(5)  -> ["1", "2", "Fizz", "4", "Buzz"]
    fizzbuzz(0)  -> []
    """
    


def is_prime(n):
    """Return True if n is prime, otherwise return False."""

    # الأعداد الأقل من 2 ليست أولية
    if n < 2:
        return False

    # اختبار القسمة على الأعداد من 2 حتى الجذر التربيعي للعدد
    for d in range(2, int(n ** 0.5) + 1):

        # لو باقي القسمة يساوي صفرًا، فالعدد غير أولي
        if n % d == 0:
            return False

    # لو لم نجد أي قاسم، فالعدد أولي
    return True
    """True if n is a prime number.

    Numbers below 2 are not prime. It is enough to try divisors up to and
    including the square root of n — ask yourself why.

    is_prime(2) -> True ;  is_prime(9) -> False ;  is_prime(97) -> True
    """
    


def primes_below(n):
    """Return all prime numbers below n."""

    # إنشاء قائمة فارغة لتخزين الأعداد الأولية
    primes = []

    # المرور على الأعداد من 2 حتى n - 1
    for num in range(2, n):

        # استخدام الفانكشن السابقة لاختبار العدد
        if is_prime(num):

            # إضافة العدد إلى القائمة إذا كان أوليًا
            primes.append(num)

    # إرجاع قائمة الأعداد الأولية
    return primes
    """Every prime p with 2 <= p < n, in increasing order.

    primes_below(10) -> [2, 3, 5, 7]
    primes_below(2)  -> []
    """
    


def first_repeated(values):
    """Return the first value that appears more than once."""

    # المرور على عناصر القائمة بالترتيب
    for i in range(len(values)):

        # البحث في العناصر التي تسبق العنصر الحالي
        for j in range(i):

            # مقارنة العنصر الحالي بالعناصر السابقة
            if values[i] == values[j]:
                return values[i]

    # لم نجد عنصرًا مكررًا
    return None
    """The first element that equals an element before it, or None.

    "First" means the repeat that happens earliest in the list.

    first_repeated([3, 1, 4, 1, 5, 9, 5])  -> 1
    first_repeated([1, 2, 3])              -> None

    Use loops and `break` or an early `return`. (In Lab 03 you will do this
    again with a set, and it will be much faster.)
    """
   

def count_pairs(n):
    count = 0  # بنبدأ عدّ الأزواج من صفر

    for i in range(n):  # بنختار العنصر الأول في كل زوج
        for j in range(i + 1, n):  # بنختار العنصر الثاني بعد العنصر الأول
            count += 1  # بنزود عدد الأزواج واحد

    return count  # بنرجع العدد النهائي للأزواج
    """How many times does the inner body run in this loop?

        for i in range(n):
            for j in range(i + 1, n):
                ...                       # <- count this

    count_pairs(0) -> 0 ;  count_pairs(4) -> 6 ;  count_pairs(10) -> 45

    First write it with the two loops and a counter. Then find a formula that
    gives the same answer without looping, and use that instead. Both pass —
    only one of them is O(1).
    """
    


def calculator(command):
    # تقسيم الأمر إلى كلمات
    parts = command.split()

    # تحديد العملية الحسابية
    match parts:
        # جمع عددين
        case ["add", a, b]:
            return int(a) + int(b)

        # ضرب عددين
        case ["mul", a, b]:
            return int(a) * int(b)

        # عكس إشارة عدد
        case ["neg", x]:
            return -int(x)

        # جمع عدد أو أكثر
        case ["sum", first, *rest]:
            return int(first) + sum(int(x) for x in rest)

        # أي أمر غير صحيح
        case _:
            raise ValueError("Invalid command")
    """Evaluate a tiny command language with a `match` statement.

    The command is words separated by spaces:

        "add A B"   -> A + B
        "mul A B"   -> A * B
        "neg A"     -> -A
        "sum A B C ..." (one or more numbers) -> their total

    A, B, C are integers written in decimal. Anything else raises ValueError.

    calculator("add 2 3")     -> 5
    calculator("neg 7")       -> -7
    calculator("sum 1 2 3 4") -> 10
    calculator("div 1 2")     -> ValueError
    """
   


# -- functions --------------------------------------------------------------


def parse_int(text, default=None):
    # محاولة تحويل النص إلى عدد صحيح
    try:
        return int(text)
    # لو التحويل فشل، نرجّع القيمة الافتراضية
    except ValueError:
        return default
    """Convert text to an int; return `default` if it is not a valid integer.

    parse_int("42")        -> 42
    parse_int(" -7 ")      -> -7
    parse_int("4.5")       -> None
    parse_int("abc", 0)    -> 0

    Use try/except — do not test the characters yourself.
    """
   


def stats(*numbers):
    # لازم يكون فيه رقم واحد على الأقل
    if not numbers:
        raise ValueError("At least one number is required")

    # حساب أصغر رقم
    smallest = min(numbers)

    # حساب أكبر رقم
    largest = max(numbers)

    # حساب المتوسط الحسابي
    average = sum(numbers) / len(numbers)

    # إرجاع الأصغر والأكبر والمتوسط
    return smallest, largest, average
    """Return (smallest, largest, mean) of any number of arguments.

    stats(3, 1, 2)  -> (1, 3, 2.0)
    stats(5)        -> (5, 5, 5.0)
    stats()         -> ValueError

    Write the loop yourself — no min(), max() or sum().
    """



def append_to(item, target=None):
    # إنشاء قائمة جديدة لو المستخدم مبعتش قائمة
    if target is None:
        target = []

    # إضافة العنصر إلى القائمة
    target.append(item)

    # إرجاع القائمة بعد التعديل
    return target
    """Append item to target and return target.

    If no list is given, start a NEW empty list every call.

    append_to(1)       -> [1]
    append_to(2)       -> [2]          not [1, 2]
    append_to(3, [0])  -> [0, 3]

    This is the mutable-default-argument trap from the manual. Do not write
    `target=[]`.
    """



def make_multiplier(k):
    # إرجاع دالة تضرب الرقم المدخل في k
    return lambda x: x * k
    """Return a FUNCTION that multiplies its argument by k.

    triple = make_multiplier(3)
    triple(5)  -> 15
    """
   


def apply_n(func, value, n):
    for _ in range(n):
        value = func(value)
    return value
    """Apply f to x, n times: f(f(...f(x)...)).

    apply_n(lambda v: v * 2, 1, 10)  -> 1024
    apply_n(str.upper, "hi", 0)      -> "hi"
    """
    
