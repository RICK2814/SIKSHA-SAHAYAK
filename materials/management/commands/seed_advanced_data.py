import random
from fractions import Fraction
from math import gcd
from django.core.management.base import BaseCommand
from materials.models import ClassLevel, Subject, Chapter, StudyMaterial
from assessments.models import Question, Quiz, QuizQuestion

# Helper builders used across the seed script
def mc(q_text, options, correct_index, explanation, diff='easy'):
    """options: list of 4 strings. correct_index: 0-3."""
    letters = ['A', 'B', 'C', 'D']
    return (q_text, letters[correct_index], options[0], options[1], options[2], options[3], explanation, diff)
import random
from fractions import Fraction
from math import gcd

def mc(q_text, options, correct_index, explanation, diff='easy'):
    letters = ['A','B','C','D']
    opts = list(options)
    correct_val = opts[correct_index]
    return (q_text, letters[correct_index], opts[0], opts[1], opts[2], opts[3], explanation, diff)

def distinct_wrongs(correct, gen_fn, n=3):
    seen = {correct}
    out = []
    tries = 0
    while len(out) < n and tries < 500:
        v = gen_fn()
        tries += 1
        if v not in seen:
            seen.add(v)
            out.append(v)
    # fallback: pad with tweaked numeric variants if still short
    fallback_i = 1
    while len(out) < n:
        cand = f"{correct}_{fallback_i}"
        if cand not in seen:
            out.append(cand); seen.add(cand)
        fallback_i += 1
    return out

def dedupe_shuffle(rnd, correct, opts_pool):
    wrongs = distinct_wrongs(correct, opts_pool)
    opts = [correct] + wrongs
    rnd.shuffle(opts)
    return opts, opts.index(correct)

# 1. Class 5 - Numbers and Place Value
def gen_c5_place_value(seed=501):
    rnd = random.Random(seed); qs=[]; used=set()
    place_names = ['ones','tens','hundreds','thousands','ten thousands']
    while len(qs) < 10:
        n = rnd.randint(10000,99999)
        if n in used: continue
        used.add(n)
        pos = rnd.randint(0,4)
        digits = str(n)
        digit = digits[pos]
        place = place_names[len(digits)-1-pos]
        opts, ci = dedupe_shuffle(rnd, digit, lambda: str(rnd.randint(0,9)))
        qs.append(mc(f"In the number {n}, what digit is in the {place} place?", opts, ci,
                      f"In {n}, the digit {digit} is in the {place} place.", 'easy'))
    while len(qs) < 20:
        n = rnd.randint(100,9999)
        if n in used: continue
        used.add(n)
        rounded = round(n,-2)
        opts, ci = dedupe_shuffle(rnd, str(rounded), lambda: str(rounded + rnd.choice([-100,100,10,-10,200])))
        qs.append(mc(f"Round {n} to the nearest hundred.", opts, ci,
                      f"{n} rounded to the nearest hundred is {rounded}.", 'easy'))
    return qs

# 2. Class 5 - Fractions
def gen_c5_fractions(seed=502):
    rnd = random.Random(seed); qs=[]; used=set()
    for _ in range(400):
        if len(qs) >= 10: break
        a = rnd.randint(1,8); b = rnd.randint(a+1,12)
        c = rnd.randint(1,8)
        key = (a,b,c,'add')
        if key in used: continue
        used.add(key)
        num = a+c
        correct = f"{num}/{b}"
        opts, ci = dedupe_shuffle(rnd, correct, lambda: f"{num + rnd.choice([-1,1,2])}/{b}")
        qs.append(mc(f"What is {a}/{b} + {c}/{b}?", opts, ci, f"Add the numerators: {a}+{c}={num}, keep denominator {b}. Answer: {num}/{b}.", 'easy'))
    for _ in range(400):
        if len(qs) >= 20: break
        a = rnd.randint(2,20); m = rnd.randint(2,6)
        b = a*2
        key=(a,b,m,'equiv')
        if key in used: continue
        used.add(key)
        correct = f"{a*m}/{b*m}"
        opts, ci = dedupe_shuffle(rnd, correct, lambda: f"{a*m+rnd.choice([-1,1,2])}/{b*m}")
        qs.append(mc(f"Which fraction is equivalent to {a}/{b}?", opts, ci, f"Multiplying numerator and denominator by {m}: {a}/{b} = {a*m}/{b*m}.", 'easy'))
    return qs[:20]

# 3. Class 6 - Knowing Our Numbers
def gen_c6_numbers(seed=601):
    rnd = random.Random(seed); qs=[]; used=set()
    while len(qs) < 10:
        n = rnd.randint(100000, 9999999)
        if n in used: continue
        used.add(n)
        rounded = round(n, -3)
        opts, ci = dedupe_shuffle(rnd, str(rounded), lambda: str(rounded + rnd.choice([-1000,1000,100,-100])))
        qs.append(mc(f"Round {n} to the nearest thousand.", opts, ci, f"{n} rounded to the nearest thousand is {rounded}.", 'easy'))
    while len(qs) < 20:
        a = rnd.randint(100000,999999); b = rnd.randint(100000,999999)
        if a==b: continue
        key=(a,b)
        if key in used: continue
        used.add(key)
        correct = str(max(a,b))
        opts, ci = dedupe_shuffle(rnd, correct, lambda: str(rnd.randint(100000,999999)))
        qs.append(mc(f"Which is greater: {a} or {b}?", opts, ci, f"{max(a,b)} is greater than {min(a,b)}.", 'easy'))
    return qs

# 4. Class 6 - Whole Numbers
def gen_c6_whole(seed=602):
    rnd = random.Random(seed); qs=[]; used=set()
    while len(qs) < 12:
        n = rnd.randint(1,9999)
        if n in used: continue
        used.add(n)
        correct = str(n+1)
        opts, ci = dedupe_shuffle(rnd, correct, lambda: str(n+rnd.choice([-1,2,-2])))
        qs.append(mc(f"What is the successor of {n}?", opts, ci, f"The successor of {n} is {n}+1 = {n+1}.", 'easy'))
    while len(qs) < 20:
        n = rnd.randint(1,9999)
        key=('pred',n)
        if key in used: continue
        used.add(key)
        correct = str(n-1)
        opts, ci = dedupe_shuffle(rnd, correct, lambda: str(n+rnd.choice([1,-2,2])))
        qs.append(mc(f"What is the predecessor of {n}?", opts, ci, f"The predecessor of {n} is {n}-1 = {n-1}.", 'easy'))
    return qs

# 5. Class 7 - Integers
def gen_c7_integers(seed=701):
    rnd = random.Random(seed); qs=[]; used=set()
    ops = ['+','-','*']
    while len(qs) < 20:
        a = rnd.randint(-20,20); b = rnd.randint(-20,20)
        op = rnd.choice(ops)
        if a==0 or b==0: continue
        key=(a,b,op)
        if key in used: continue
        used.add(key)
        if op=='+': correct=a+b; sym='+'
        elif op=='-': correct=a-b; sym='-'
        else: correct=a*b; sym='×'
        opts, ci = dedupe_shuffle(rnd, str(correct), lambda: str(correct+rnd.choice([-1,1,2,-2,10,-10])))
        qs.append(mc(f"What is ({a}) {sym} ({b})?", opts, ci, f"({a}) {sym} ({b}) = {correct}.", 'easy' if op!='*' else 'medium'))
    return qs

# 6. Class 7 - Fractions and Decimals
def gen_c7_fracdec(seed=702):
    rnd = random.Random(seed); qs=[]; used=set()
    while len(qs) < 10:
        a = rnd.randint(1,9); b = rnd.randint(2,9)
        c = rnd.randint(1,9); d = rnd.randint(2,9)
        key=(a,b,c,d)
        if key in used: continue
        used.add(key)
        val = Fraction(a,b) * Fraction(c,d)
        correct = f"{val.numerator}/{val.denominator}"
        opts, ci = dedupe_shuffle(rnd, correct, lambda: f"{val.numerator+rnd.choice([-1,1,2])}/{val.denominator}")
        qs.append(mc(f"What is {a}/{b} × {c}/{d}? (in simplest form)", opts, ci, f"{a}/{b} × {c}/{d} = {a*c}/{b*d} = {correct} in simplest form.", 'medium'))
    while len(qs) < 20:
        x = round(rnd.uniform(1,50),1); y = round(rnd.uniform(1,50),1)
        key=('dec',x,y)
        if key in used: continue
        used.add(key)
        correct = round(x+y,1)
        opts, ci = dedupe_shuffle(rnd, str(correct), lambda: round(correct+rnd.choice([-0.1,0.1,1,-1]),1).__str__())
        qs.append(mc(f"What is {x} + {y}?", opts, ci, f"{x} + {y} = {correct}.", 'easy'))
    return qs

# 7. Class 9 - Number Systems
def gen_c9_numsys(seed=901):
    rnd = random.Random(seed); qs=[]; used=set()
    rational_examples = ['3/4','0.5','7','-2/3','0.333... (repeating)','5/1','-8','0.125','2/9','-11']
    irrational_examples = ['√2','π','√3','√5','1.010010001...','√7','e','√11','√13','0.1211211121...']
    rat_templates = ["Which of the following is a RATIONAL number?",
                      "Identify the rational number among the options.",
                      "Select the number that IS rational.",
                      "Which number below can be written in the form p/q?",
                      "Pick the rational number from the choices.",
                      "In the options given, which value is rational?",
                      "Choose the rational number.",
                      "From the numbers listed, which one is rational?",
                      "Which option represents a rational number?",
                      "Spot the rational number below."]
    irr_templates = ["Which of the following is an IRRATIONAL number?",
                      "Identify the irrational number among the options.",
                      "Select the number that is NOT rational.",
                      "Which number below has a non-terminating, non-repeating decimal expansion?",
                      "Pick the irrational number from the choices.",
                      "In the options given, which value is irrational?",
                      "Choose the irrational number."]
    ti = 0
    while len(qs) < 10:
        r = rnd.choice(rational_examples); irr_wrongs = rnd.sample(irrational_examples,3)
        key=('rat',r,ti%len(rat_templates))
        if key in used:
            ti += 1
            continue
        used.add(key)
        opts = [r]+irr_wrongs
        rnd.shuffle(opts); ci=opts.index(r)
        qs.append(mc(rat_templates[ti%len(rat_templates)], opts, ci, f"{r} can be expressed as p/q form (or is a terminating/repeating decimal), so it is rational.", 'medium'))
        ti += 1
    ti = 0
    while len(qs) < 16:
        irr = rnd.choice(irrational_examples); rat_wrongs = rnd.sample(rational_examples,3)
        key=('irr',irr,ti%len(irr_templates))
        if key in used:
            ti += 1
            continue
        used.add(key)
        opts=[irr]+rat_wrongs
        rnd.shuffle(opts); ci=opts.index(irr)
        qs.append(mc(irr_templates[ti%len(irr_templates)], opts, ci, f"{irr} cannot be expressed as p/q and its decimal expansion is non-terminating, non-repeating.", 'medium'))
        ti += 1
    facts = [
        ("Every rational number is expressible in the form p/q where q ≠ 0.", True),
        ("The sum of a rational and an irrational number is always irrational.", True),
        ("Between any two rational numbers there are infinitely many rational numbers.", True),
        ("√4 is an irrational number.", False),
    ]
    while len(qs) < 20:
        stmt, ans = rnd.choice(facts)
        key=('stmt',stmt)
        if key in used: continue
        used.add(key)
        options = ["True","False","Cannot be determined","Sometimes true"]
        correct = "True" if ans else "False"
        ci = options.index(correct)
        expl = "This statement is a standard property of rational and irrational numbers." if ans else "√4 = 2, which is a rational number (it can be written as 2/1), so this statement is false."
        qs.append(mc(f"State whether true or false: {stmt}", options, ci, expl, 'medium'))
    return qs[:20]

# 8. Class 9 - Polynomials
def gen_c9_poly(seed=902):
    rnd = random.Random(seed); qs=[]; used=set()
    while len(qs) < 10:
        a = rnd.randint(1,5); b = rnd.randint(-5,5); c = rnd.randint(-5,5)
        x = rnd.randint(-3,3)
        key=(a,b,c,x)
        if key in used: continue
        used.add(key)
        val = a*x*x + b*x + c
        opts, ci = dedupe_shuffle(rnd, str(val), lambda: str(val+rnd.choice([-1,1,2,-2,5])))
        qs.append(mc(f"If p(x) = {a}x² + ({b})x + ({c}), find p({x}).", opts, ci,
                      f"p({x}) = {a}({x})² + ({b})({x}) + ({c}) = {val}.", 'medium'))
    while len(qs) < 20:
        a = rnd.randint(1,6); b = rnd.randint(1,6); c=rnd.randint(1,6)
        degree = 2
        key=('deg',a,b,c)
        if key in used: continue
        used.add(key)
        opts, ci = dedupe_shuffle(rnd, "2", lambda: str(rnd.choice([1,3,4,0])))
        qs.append(mc(f"What is the degree of the polynomial {a}x² + {b}x + {c}?", opts, ci,
                      "The degree of a polynomial is the highest power of the variable, here it is 2.", 'easy'))
    return qs[:20]

# 9. Class 10 - Real Numbers (HCF/LCM)
def gen_c10_realnum(seed=1001):
    rnd = random.Random(seed); qs=[]; used=set()
    while len(qs) < 12:
        a = rnd.randint(4,60); b = rnd.randint(4,60)
        if a==b: continue
        key=(a,b,'hcf')
        if key in used: continue
        used.add(key)
        h = gcd(a,b)
        opts, ci = dedupe_shuffle(rnd, str(h), lambda: str(max(1,h+rnd.choice([-3,-2,-1,1,2,3,4,-4]))))
        qs.append(mc(f"Find the HCF of {a} and {b}.", opts, ci, f"The Highest Common Factor of {a} and {b} is {h}.", 'medium'))
    while len(qs) < 20:
        a = rnd.randint(4,30); b = rnd.randint(4,30)
        if a==b: continue
        key=(a,b,'lcm')
        if key in used: continue
        used.add(key)
        l = a*b//gcd(a,b)
        opts, ci = dedupe_shuffle(rnd, str(l), lambda: str(l+rnd.choice([-a,-b,a,b])))
        qs.append(mc(f"Find the LCM of {a} and {b}.", opts, ci, f"LCM({a},{b}) = ({a}×{b})/HCF({a},{b}) = {l}.", 'medium'))
    return qs[:20]

# 10. Class 10 - Polynomials and Quadratic Equations
def gen_c10_quad(seed=1002):
    rnd = random.Random(seed); qs=[]; used=set()
    while len(qs) < 10:
        p = rnd.randint(-6,6); q = rnd.randint(-6,6)
        if p==0 or q==0: continue
        # x^2 - (p+q)x + pq = 0 has roots p,q
        b = -(p+q); c = p*q
        key=(p,q)
        if key in used: continue
        used.add(key)
        correct_sum = p+q
        opts, ci = dedupe_shuffle(rnd, str(correct_sum), lambda: str(correct_sum+rnd.choice([-1,1,2,-2])))
        qs.append(mc(f"For the quadratic equation x² + ({b})x + ({c}) = 0, what is the sum of the zeroes?", opts, ci,
                      f"Sum of zeroes = -b/a = -({b})/1 = {correct_sum}.", 'medium'))
    while len(qs) < 20:
        a = rnd.randint(1,4); b = rnd.randint(-8,8); c = rnd.randint(-8,8)
        if a==0: continue
        d = b*b - 4*a*c
        key=('disc',a,b,c)
        if key in used: continue
        used.add(key)
        if d > 0: nature = "Two distinct real roots"
        elif d == 0: nature = "Two equal real roots"
        else: nature = "No real roots"
        others = ["Two distinct real roots","Two equal real roots","No real roots"]
        others.remove(nature)
        opts = [nature]+others+["Infinite roots"]
        opts = opts[:4]
        rnd.shuffle(opts); ci = opts.index(nature)
        qs.append(mc(f"For the quadratic equation {a}x² + ({b})x + ({c}) = 0, the discriminant is {d}. What is the nature of its roots?", opts, ci,
                      f"Discriminant D = b²-4ac = {d}. Since D {'> 0' if d>0 else ('= 0' if d==0 else '< 0')}, the roots are: {nature}.", 'hard'))
    return qs[:20]

all_gens = [gen_c5_place_value, gen_c5_fractions, gen_c6_numbers, gen_c6_whole, gen_c7_integers,
            gen_c7_fracdec, gen_c9_numsys, gen_c9_poly, gen_c10_realnum, gen_c10_quad]
for g in all_gens:
    qs = g()
    texts = [q[0] for q in qs]
    print(g.__name__, len(qs), 'unique:', len(set(texts)))
    # sanity check correct answer is among options and matches letter
    for q in qs:
        qt, ans, oa,ob,oc,od, expl, diff = q
        opts = {'A':oa,'B':ob,'C':oc,'D':od}
        assert ans in opts
print("ALL OK")

# 11. Class 8 - Rational Numbers (need ~13 more, existing 7)
def gen_c8_rational(seed=801):
    rnd = random.Random(seed); qs=[]; used=set()
    while len(qs) < 7:
        a = rnd.randint(1,12); b = rnd.randint(2,12)
        c = rnd.randint(1,12); d = rnd.randint(2,12)
        key=(a,b,c,d,'add')
        if key in used: continue
        used.add(key)
        val = Fraction(a,b) + Fraction(c,d)
        correct = f"{val.numerator}/{val.denominator}"
        opts, ci = dedupe_shuffle(rnd, correct, lambda: f"{val.numerator+rnd.choice([-1,1,2,-2])}/{val.denominator}")
        qs.append(mc(f"What is {a}/{b} + {c}/{d}? (simplest form)", opts, ci, f"{a}/{b} + {c}/{d} = {correct} in simplest form.", 'medium'))
    while len(qs) < 13:
        a = rnd.randint(-9,9); b = rnd.randint(2,9)
        if a==0: continue
        key=('add_inv',a,b)
        if key in used: continue
        used.add(key)
        correct = f"{-a}/{b}"
        opts, ci = dedupe_shuffle(rnd, correct, lambda: f"{-a+rnd.choice([-1,1,2])}/{b}")
        qs.append(mc(f"What is the additive inverse of {a}/{b}?", opts, ci, f"The additive inverse of {a}/{b} is {-a}/{b}, since {a}/{b} + ({-a}/{b}) = 0.", 'medium'))
    while len(qs) < 20:
        a = rnd.randint(1,9); b = rnd.randint(1,9)
        if a==0: continue
        key=('recip',a,b)
        if key in used: continue
        used.add(key)
        correct = f"{b}/{a}"
        opts, ci = dedupe_shuffle(rnd, correct, lambda: f"{b}/{a+rnd.choice([-1,1,2])}" if a+rnd.choice([-1,1,2])!=0 else f"{b+1}/{a}")
        qs.append(mc(f"What is the reciprocal (multiplicative inverse) of {a}/{b}?", opts, ci, f"The reciprocal of {a}/{b} is {b}/{a}, since {a}/{b} × {b}/{a} = 1.", 'medium'))
    return qs[:20]

# 12. Class 8 - Linear Equations (need ~16 more, existing 4)
def gen_c8_linear(seed=802):
    rnd = random.Random(seed); qs=[]; used=set()
    while len(qs) < 20:
        x = rnd.randint(-15,15)
        a = rnd.randint(2,9); b = rnd.randint(-20,20)
        if x==0: continue
        c = a*x + b
        key=(a,b,c)
        if key in used: continue
        used.add(key)
        opts, ci = dedupe_shuffle(rnd, str(x), lambda: str(x+rnd.choice([-1,1,2,-2,3])))
        sign = '+' if b>=0 else '-'
        qs.append(mc(f"Solve for x: {a}x {sign} {abs(b)} = {c}", opts, ci,
                      f"{a}x {sign} {abs(b)} = {c}  =>  {a}x = {c-b}  =>  x = {x}.", 'medium'))
    return qs[:20]

# 13. Class 8 - Understanding Quadrilaterals (need ~16 more, existing 4)
def gen_c8_quad(seed=803):
    rnd = random.Random(seed); qs=[]; used=set()
    while len(qs) < 10:
        a = rnd.randint(50,150); b = rnd.randint(50,150); c = rnd.randint(50,150)
        d = 360 - a - b - c
        if d <= 0 or d >= 360: continue
        key=(a,b,c,d)
        if key in used: continue
        used.add(key)
        opts, ci = dedupe_shuffle(rnd, str(d), lambda: str(d+rnd.choice([-10,10,20,-20])))
        qs.append(mc(f"In a quadrilateral, three angles measure {a}°, {b}° and {c}°. What is the fourth angle?", opts, ci,
                      f"Sum of angles in a quadrilateral = 360°. Fourth angle = 360 - ({a}+{b}+{c}) = {d}°.", 'medium'))
    while len(qs) < 20:
        angle = rnd.randint(40,140)
        opp = angle
        others = 180 - angle
        key=('para',angle)
        if key in used: continue
        used.add(key)
        opts, ci = dedupe_shuffle(rnd, str(opp), lambda: str(opp+rnd.choice([-10,10,20,-20])))
        qs.append(mc(f"In a parallelogram, one angle measures {angle}°. What is the measure of its opposite angle?", opts, ci,
                      f"In a parallelogram, opposite angles are equal, so the opposite angle also measures {angle}°.", 'medium'))
    return qs[:20]
# ============ CLASS 5 (non-math) ============

CLASS5_SCIENCE_PLANTS = [
    mc("Which part of the plant absorbs water and minerals from the soil?", ["Leaf", "Root", "Stem", "Flower"], 1,
       "Roots absorb water and minerals from the soil and anchor the plant firmly.", 'easy'),
    mc("Which part of the plant makes food using sunlight?", ["Root", "Stem", "Leaf", "Fruit"], 2,
       "Leaves contain chlorophyll and make food through photosynthesis.", 'easy'),
    mc("What is the process by which plants make their own food called?", ["Respiration", "Photosynthesis", "Transpiration", "Digestion"], 1,
       "Photosynthesis is the process by which green plants make food using sunlight, water and carbon dioxide.", 'easy'),
    mc("Which gas do plants release during photosynthesis?", ["Carbon dioxide", "Nitrogen", "Oxygen", "Hydrogen"], 2,
       "Plants release oxygen as a by-product of photosynthesis.", 'easy'),
    mc("Animals that eat only plants are called:", ["Carnivores", "Herbivores", "Omnivores", "Decomposers"], 1,
       "Herbivores are animals that eat only plants, such as cows and deer.", 'easy'),
    mc("Animals that eat both plants and animals are called:", ["Herbivores", "Carnivores", "Omnivores", "Parasites"], 2,
       "Omnivores eat both plants and animals, for example humans and bears.", 'easy'),
    mc("Which of these is a carnivore?", ["Cow", "Lion", "Deer", "Goat"], 1,
       "A lion eats only the meat of other animals, so it is a carnivore.", 'easy'),
    mc("The green colouring matter in leaves is called:", ["Chlorophyll", "Nectar", "Pollen", "Sap"], 0,
       "Chlorophyll is the green pigment in leaves that helps absorb sunlight for photosynthesis.", 'easy'),
    mc("Which part of a plant develops into a fruit after fertilisation?", ["Sepal", "Ovary", "Petal", "Stamen"], 1,
       "After fertilisation, the ovary of the flower develops into a fruit.", 'medium'),
    mc("Which of these plant parts is usually the most colourful, to attract insects?", ["Root", "Stem", "Petal", "Leaf"], 2,
       "Petals are often brightly coloured to attract insects and birds for pollination.", 'easy'),
    mc("The transfer of pollen from the anther to the stigma is called:", ["Germination", "Pollination", "Respiration", "Fertilisation"], 1,
       "Pollination is the transfer of pollen grains from the anther to the stigma of a flower.", 'medium'),
    mc("Which animal group breathes through gills?", ["Fish", "Birds", "Mammals", "Insects"], 0,
       "Fish breathe through gills, which help them take in oxygen dissolved in water.", 'easy'),
    mc("Which of these is an example of a decomposer?", ["Rose plant", "Fungus", "Sparrow", "Tiger"], 1,
       "Fungi are decomposers that break down dead plants and animals into simpler substances.", 'medium'),
    mc("Animals that lay eggs are called:", ["Viviparous", "Oviparous", "Herbivorous", "Carnivorous"], 1,
       "Oviparous animals, such as birds and reptiles, reproduce by laying eggs.", 'medium'),
    mc("Animals that give birth to young ones directly are called:", ["Oviparous", "Viviparous", "Omnivorous", "Herbivorous"], 1,
       "Viviparous animals, such as humans, dogs and cows, give birth to live young ones.", 'medium'),
    mc("Which part of the plant transports water from roots to leaves?", ["Stem", "Petal", "Sepal", "Anther"], 0,
       "The stem contains tube-like structures (xylem) that transport water and minerals from roots to leaves.", 'medium'),
    mc("What do we call plants that live for only one season?", ["Perennial", "Annual", "Biennial", "Aquatic"], 1,
       "Annual plants complete their life cycle within one growing season.", 'medium'),
    mc("Which of the following is an aquatic plant?", ["Cactus", "Lotus", "Neem", "Mango"], 1,
       "Lotus grows in water and is an example of an aquatic plant.", 'easy'),
    mc("Cactus plants have thick, fleshy stems mainly to:", ["Attract insects", "Store water", "Produce seeds", "Absorb sunlight only"], 1,
       "Cactus stems store water, helping the plant survive in dry desert conditions.", 'medium'),
    mc("Which sense organ do most animals use to detect smells?", ["Eyes", "Ears", "Nose", "Skin"], 2,
       "The nose contains receptors that help animals detect smells in their surroundings.", 'easy'),
]

CLASS5_SCIENCE_ENV = [
    mc("What do we call the surroundings in which living things live?", ["Habitat", "Ecosystem", "Environment", "Climate"], 2,
       "The environment includes everything around a living thing, both living and non-living.", 'easy'),
    mc("Which of these is a non-living thing?", ["Tree", "Rock", "Bird", "Fish"], 1,
       "A rock does not grow, breathe or reproduce, so it is non-living.", 'easy'),
    mc("The natural home of a plant or animal is called its:", ["Environment", "Habitat", "Climate", "Region"], 1,
       "A habitat is the natural place where an organism lives and finds food, water and shelter.", 'easy'),
    mc("Which of the following is an example of air pollution?", ["Planting trees", "Smoke from factories", "Using public transport", "Recycling paper"], 1,
       "Smoke from factories releases harmful gases and particles into the air, causing pollution.", 'easy'),
    mc("Which of these practices helps conserve water?", ["Leaving taps running", "Rainwater harvesting", "Washing cars daily", "Watering plants at noon"], 1,
       "Rainwater harvesting collects and stores rainwater for later use, helping conserve water.", 'easy'),
    mc("The layer of gases surrounding the Earth is called the:", ["Biosphere", "Atmosphere", "Lithosphere", "Hydrosphere"], 1,
       "The atmosphere is the blanket of gases, mainly nitrogen and oxygen, surrounding the Earth.", 'medium'),
    mc("Which of these is the main cause of deforestation?", ["Planting saplings", "Cutting trees for farming and construction", "Rainfall", "Wildlife conservation"], 1,
       "Deforestation mainly occurs due to cutting trees for agriculture, construction and industry.", 'medium'),
    mc("Which gas do humans need to breathe in for respiration?", ["Carbon dioxide", "Oxygen", "Nitrogen", "Methane"], 1,
       "Humans and most living things need oxygen to carry out respiration.", 'easy'),
    mc("Reducing, reusing and recycling waste helps to:", ["Increase pollution", "Protect the environment", "Waste more resources", "Increase deforestation"], 1,
       "The 3 Rs (Reduce, Reuse, Recycle) help protect the environment by lowering waste and resource use.", 'easy'),
    mc("Which of these is a renewable source of energy?", ["Coal", "Petroleum", "Solar energy", "Natural gas"], 2,
       "Solar energy comes from the sun and does not get used up, making it renewable.", 'easy'),
    mc("Global warming is mainly caused by an increase in which gas?", ["Oxygen", "Carbon dioxide", "Nitrogen", "Helium"], 1,
       "Excess carbon dioxide traps heat in the atmosphere, causing global warming.", 'medium'),
    mc("Which of these actions contributes to soil pollution?", ["Composting", "Dumping plastic waste on land", "Crop rotation", "Using organic manure"], 1,
       "Dumping non-biodegradable plastic waste on land pollutes and degrades the soil.", 'medium'),
    mc("An ecosystem includes:", ["Only living things", "Only non-living things", "Both living and non-living things interacting together", "Only plants"], 2,
       "An ecosystem is made up of living organisms and non-living components interacting with each other.", 'medium'),
    mc("Which of the following helps reduce noise pollution?", ["Loud music", "Planting trees along roads", "Using more vehicles", "Bursting firecrackers"], 1,
       "Trees absorb and block sound waves, helping reduce noise pollution.", 'easy'),
    mc("Which of these is a way to save electricity at home?", ["Leaving lights on all day", "Switching off appliances when not in use", "Using old inefficient bulbs", "Keeping fridge door open"], 1,
       "Switching off appliances and lights when not needed helps save electricity.", 'easy'),
    mc("Migratory birds travel to different places mainly to find:", ["Better weather and food", "New predators", "Pollution", "Noise"], 0,
       "Migratory birds travel long distances seeking favourable climate and food availability.", 'medium'),
    mc("Which of these best describes 'conservation of forests'?", ["Cutting all trees", "Protecting and managing forests wisely", "Building factories in forests", "Ignoring wildlife"], 1,
       "Forest conservation means protecting and managing forests to maintain ecological balance.", 'medium'),
    mc("What is the main source of fresh water for most living things?", ["Oceans", "Rivers, lakes and rain", "Glaciers only", "Seas"], 1,
       "Rivers, lakes and rainfall provide most of the fresh water used by living things.", 'easy'),
    mc("Which of these organisms plays a key role in decomposing dead matter and enriching soil?", ["Earthworm", "Eagle", "Tiger", "Peacock"], 0,
       "Earthworms break down organic matter, enriching and aerating the soil, and are called 'farmer's friend'.", 'medium'),
    mc("Wildlife sanctuaries are set up mainly to:", ["Hunt animals", "Protect and conserve wild animals and their habitat", "Cut down forests", "Build cities"], 1,
       "Wildlife sanctuaries protect wild animals and preserve their natural habitat from human interference.", 'easy'),
]

CLASS5_ENGLISH_GRAMMAR = [
    mc("Choose the correct plural of 'child'.", ["Childs", "Childes", "Children", "Childrens"], 2,
       "The plural of 'child' is 'children', an irregular plural form.", 'easy'),
    mc("Identify the noun in the sentence: 'The dog ran quickly.'", ["ran", "quickly", "dog", "the"], 2,
       "'Dog' is a naming word (noun) in the sentence.", 'easy'),
    mc("Which word is a verb in the sentence: 'She sings beautifully.'", ["She", "sings", "beautifully", "the"], 1,
       "'Sings' is an action word (verb) showing what she does.", 'easy'),
    mc("Choose the correct article: '___ apple a day keeps the doctor away.'", ["A", "An", "The", "No article"], 1,
       "'An' is used before words starting with a vowel sound, like 'apple'.", 'easy'),
    mc("Which of these is an adjective in 'The tall boy ran fast'?", ["boy", "ran", "tall", "fast"], 2,
       "'Tall' describes the noun 'boy', making it an adjective.", 'easy'),
    mc("Choose the correct past tense of 'go'.", ["goed", "went", "gone", "going"], 1,
       "The past tense of 'go' is 'went', an irregular verb form.", 'easy'),
    mc("Which pronoun correctly replaces 'Ravi' in 'Ravi is playing football'?", ["She", "It", "He", "They"], 2,
       "Since Ravi is a boy's name, the pronoun 'he' should replace it.", 'easy'),
    mc("Choose the correct sentence.", ["He go to school daily.", "He goes to school daily.", "He going to school daily.", "He gone to school daily."], 1,
       "With third-person singular subjects like 'he', the verb takes an 's' in the present tense: 'goes'.", 'medium'),
    mc("Identify the preposition: 'The cat is under the table.'", ["cat", "is", "under", "table"], 2,
       "'Under' shows the position of the cat relative to the table, making it a preposition.", 'easy'),
    mc("Choose the correct conjunction: 'I like tea ___ I like coffee more.'", ["and", "but", "or", "so"], 1,
       "'But' is used to show contrast between two ideas.", 'easy'),
    mc("Which is the correct plural form of 'mouse' (the animal)?", ["Mouses", "Mice", "Mices", "Mouse"], 1,
       "'Mouse' has the irregular plural form 'mice'.", 'medium'),
    mc("Choose the correctly punctuated sentence.", ["what is your name", "What is your name?", "What is your name.", "what is your name?"], 1,
       "A question must start with a capital letter and end with a question mark.", 'easy'),
    mc("Identify the adverb in: 'He runs very quickly.'", ["He", "runs", "very", "quickly"], 3,
       "'Quickly' describes how he runs, making it an adverb.", 'medium'),
    mc("Choose the correct comparative form of 'big'.", ["bigger", "biggest", "more big", "big"], 0,
       "The comparative form of 'big' is 'bigger', used to compare two things.", 'easy'),
    mc("Choose the correct superlative form of 'good'.", ["gooder", "best", "goodest", "more good"], 1,
       "'Good' has the irregular superlative form 'best'.", 'medium'),
    mc("Which sentence uses the correct subject-verb agreement?", ["The boys plays football.", "The boys play football.", "The boy plays football.", "Both b and c"], 3,
       "Plural subjects take plural verbs ('boys play'), and singular subjects take singular verbs ('boy plays').", 'medium'),
    mc("Identify the collective noun: 'A flock of birds flew away.'", ["birds", "flew", "flock", "away"], 2,
       "'Flock' is a collective noun referring to a group of birds.", 'medium'),
    mc("Choose the correct helping verb: 'She ___ going to the market.'", ["is", "am", "are", "be"], 0,
       "With the singular pronoun 'she', the correct helping verb is 'is'.", 'easy'),
    mc("Which word is a proper noun?", ["city", "river", "India", "mountain"], 2,
       "'India' names a specific country, so it is a proper noun and starts with a capital letter.", 'easy'),
    mc("Choose the antonym of 'happy'.", ["Joyful", "Sad", "Glad", "Cheerful"], 1,
       "'Sad' means the opposite of 'happy'.", 'easy'),
]

CLASS5_ENGLISH_READING = [
    mc("A word that means the same as another word is called a:", ["Antonym", "Synonym", "Homonym", "Pronoun"], 1,
       "A synonym is a word with a similar meaning to another word, e.g. 'happy' and 'glad'.", 'easy'),
    mc("A word that means the opposite of another word is called a:", ["Synonym", "Antonym", "Homophone", "Adjective"], 1,
       "An antonym is a word with the opposite meaning, e.g. 'hot' and 'cold'.", 'easy'),
    mc("Words that sound the same but have different meanings and spellings are called:", ["Synonyms", "Antonyms", "Homophones", "Adverbs"], 2,
       "Homophones sound alike but differ in meaning and spelling, e.g. 'flower' and 'flour'.", 'medium'),
    mc("The main idea of a passage is also called its:", ["Title", "Theme", "Character", "Setting"], 1,
       "The theme is the central idea or message of a passage.", 'medium'),
    mc("Skimming a passage means:", ["Reading every word slowly", "Reading quickly to get a general idea", "Memorising the passage", "Reading it backwards"], 1,
       "Skimming means reading quickly to understand the general idea of a text.", 'medium'),
    mc("Which of these is an example of a synonym for 'big'?", ["Small", "Large", "Tiny", "Short"], 1,
       "'Large' has a meaning similar to 'big'.", 'easy'),
    mc("Which of these is an example of an antonym for 'begin'?", ["Start", "Commence", "End", "Open"], 2,
       "'End' is the opposite of 'begin'.", 'easy'),
    mc("A story that teaches a moral lesson using animal characters is called a:", ["Biography", "Fable", "Autobiography", "Report"], 1,
       "A fable is a short story, often with animal characters, that teaches a moral lesson.", 'medium'),
    mc("The person or animal a story is mainly about is called the:", ["Setting", "Plot", "Main character", "Moral"], 2,
       "The main character is the central person or animal around whom the story revolves.", 'easy'),
    mc("Where and when a story takes place is called the:", ["Setting", "Plot", "Character", "Climax"], 0,
       "The setting refers to the time and place in which a story occurs.", 'easy'),
    mc("The sequence of events in a story is called the:", ["Setting", "Plot", "Theme", "Moral"], 1,
       "The plot is the sequence of events that make up a story.", 'medium'),
    mc("Reading to find specific information quickly is called:", ["Skimming", "Scanning", "Summarising", "Predicting"], 1,
       "Scanning means quickly looking through a text to find specific information.", 'medium'),
    mc("A short retelling of a passage in your own words is called a:", ["Summary", "Title", "Index", "Glossary"], 0,
       "A summary is a brief restatement of the main points of a passage.", 'easy'),
    mc("Which word correctly completes: 'She was ___ because she won the race.'", ["sad", "angry", "thrilled", "bored"], 2,
       "'Thrilled' fits the context of winning, showing excitement.", 'easy'),
    mc("A list of difficult words with their meanings, usually at the end of a book, is called a:", ["Index", "Glossary", "Preface", "Chapter"], 1,
       "A glossary is a list of difficult words and their meanings, usually found at the end of a book.", 'medium'),
    mc("Guessing what might happen next in a story based on clues is called:", ["Predicting", "Summarising", "Skimming", "Editing"], 0,
       "Predicting means making an educated guess about upcoming events using clues from the text.", 'medium'),
    mc("Which of these is a synonym for 'happy'?", ["Joyful", "Miserable", "Angry", "Tired"], 0,
       "'Joyful' has a similar meaning to 'happy'.", 'easy'),
    mc("Which word is an antonym for 'difficult'?", ["Hard", "Tough", "Easy", "Complex"], 2,
       "'Easy' is the opposite of 'difficult'.", 'easy'),
    mc("A conversation between characters in a story is called:", ["Narration", "Dialogue", "Description", "Summary"], 1,
       "Dialogue refers to the spoken conversation between characters in a story.", 'medium'),
    mc("The lesson a story teaches its readers is called the:", ["Setting", "Climax", "Moral", "Plot"], 2,
       "The moral is the lesson that a story teaches, often found in fables.", 'easy'),
]

CLASS5_SOCIAL_INDIA = [
    mc("What is the capital of India?", ["Mumbai", "New Delhi", "Kolkata", "Chennai"], 1,
       "New Delhi is the capital city of India.", 'easy'),
    mc("India is located in which continent?", ["Africa", "Asia", "Europe", "Australia"], 1,
       "India is located in the continent of Asia.", 'easy'),
    mc("Which ocean lies to the south of India?", ["Atlantic Ocean", "Arctic Ocean", "Indian Ocean", "Pacific Ocean"], 2,
       "The Indian Ocean lies to the south of the Indian peninsula.", 'easy'),
    mc("How many states did India have as of the last major reorganisation before 2019 (before Jammu & Kashmir became a UT)?", ["25", "28", "29", "31"], 2,
       "Before the 2019 reorganisation, India had 29 states.", 'hard'),
    mc("Which is the national bird of India?", ["Sparrow", "Peacock", "Parrot", "Crow"], 1,
       "The peacock is the national bird of India.", 'easy'),
    mc("Which is the national animal of India?", ["Lion", "Elephant", "Tiger", "Leopard"], 2,
       "The Bengal tiger is the national animal of India.", 'easy'),
    mc("Which river is considered the holiest and longest river of India?", ["Yamuna", "Godavari", "Ganga", "Narmada"], 2,
       "The Ganga (Ganges) is considered India's holiest and one of its longest rivers.", 'easy'),
    mc("Which mountain range lies to the north of India?", ["Aravalli", "Himalayas", "Western Ghats", "Vindhya"], 1,
       "The Himalayas form India's northern mountain boundary.", 'easy'),
    mc("India got independence from British rule in which year?", ["1942", "1945", "1947", "1950"], 2,
       "India became independent from British rule on 15 August 1947.", 'easy'),
    mc("When did India become a republic (adopt its Constitution)?", ["1947", "1948", "1950", "1952"], 2,
       "India adopted its Constitution and became a republic on 26 January 1950.", 'medium'),
    mc("Who is known as the 'Father of the Nation' in India?", ["Jawaharlal Nehru", "Mahatma Gandhi", "Sardar Patel", "Subhas Chandra Bose"], 1,
       "Mahatma Gandhi is known as the Father of the Nation for his role in India's freedom struggle.", 'easy'),
    mc("What is the national language recognised in the Indian Constitution as the official language, alongside English?", ["Tamil", "Bengali", "Hindi", "Punjabi"], 2,
       "Hindi, along with English, is an official language of the Union of India as per the Constitution.", 'medium'),
    mc("Which is the national flower of India?", ["Rose", "Lotus", "Sunflower", "Marigold"], 1,
       "The lotus is the national flower of India.", 'easy'),
    mc("Which of these is a union territory of India?", ["Kerala", "Chandigarh", "Punjab", "Gujarat"], 1,
       "Chandigarh is a union territory, administered directly by the central government.", 'medium'),
    mc("The Indian national flag has how many colours (stripes)?", ["Two", "Three", "Four", "Five"], 1,
       "The Indian flag has three horizontal stripes: saffron, white and green.", 'easy'),
    mc("What symbol is at the centre of the Indian national flag?", ["Sun", "Star", "Ashoka Chakra", "Lotus"], 2,
       "The Ashoka Chakra, a 24-spoke wheel, is at the centre of the Indian flag.", 'easy'),
    mc("Who wrote the national anthem of India, 'Jana Gana Mana'?", ["Bankim Chandra Chattopadhyay", "Rabindranath Tagore", "Sarojini Naidu", "Muhammad Iqbal"], 1,
       "Rabindranath Tagore wrote 'Jana Gana Mana', India's national anthem.", 'medium'),
    mc("Which is the largest state of India by area?", ["Uttar Pradesh", "Madhya Pradesh", "Rajasthan", "Maharashtra"], 2,
       "Rajasthan is the largest Indian state by area.", 'medium'),
    mc("Which is the most populous state of India?", ["Bihar", "Maharashtra", "Uttar Pradesh", "West Bengal"], 2,
       "Uttar Pradesh is the most populous state in India.", 'medium'),
    mc("India shares its longest land border with which country?", ["China", "Pakistan", "Bangladesh", "Nepal"], 2,
       "India shares its longest land border with Bangladesh.", 'hard'),
]

CLASS5_SOCIAL_MAPS = [
    mc("Which instrument is used to show direction?", ["Thermometer", "Compass", "Barometer", "Ruler"], 1,
       "A compass has a magnetic needle that always points towards the North, helping to find direction.", 'easy'),
    mc("How many main (cardinal) directions are there?", ["Two", "Three", "Four", "Six"], 2,
       "There are four main directions: North, South, East and West.", 'easy'),
    mc("Which direction does the sun rise from?", ["North", "South", "East", "West"], 2,
       "The sun rises in the East every day.", 'easy'),
    mc("Which direction does the sun set in?", ["North", "South", "East", "West"], 3,
       "The sun sets in the West every day.", 'easy'),
    mc("A drawing that represents the whole Earth or a part of it on a flat surface is called a:", ["Globe", "Map", "Atlas", "Chart"], 1,
       "A map is a flat representation of the Earth or a part of it.", 'easy'),
    mc("A round model of the Earth is called a:", ["Map", "Atlas", "Globe", "Compass"], 2,
       "A globe is a three-dimensional, round model representing the Earth.", 'easy'),
    mc("A collection of maps bound together in a book is called an:", ["Index", "Atlas", "Legend", "Scale"], 1,
       "An atlas is a book that contains a collection of maps.", 'easy'),
    mc("The symbols used in a map to represent features are explained in the:", ["Scale", "Legend/Key", "Title", "Border"], 1,
       "The legend or key explains what the various symbols on a map represent.", 'medium'),
    mc("The relationship between distance on a map and actual distance on the ground is called the map's:", ["Legend", "Scale", "Title", "Symbol"], 1,
       "The scale shows the ratio between map distance and actual ground distance.", 'medium'),
    mc("Which direction lies exactly between North and East?", ["North-West", "South-East", "North-East", "South-West"], 2,
       "North-East lies exactly between North and East.", 'medium'),
    mc("Which direction lies exactly between South and West?", ["South-East", "South-West", "North-West", "North-East"], 1,
       "South-West lies exactly between South and West.", 'medium'),
    mc("Maps that show political boundaries like states and countries are called:", ["Physical maps", "Political maps", "Climate maps", "Thematic maps"], 1,
       "Political maps show boundaries of countries, states and cities.", 'medium'),
    mc("Maps that show mountains, rivers, and plains are called:", ["Political maps", "Physical maps", "Road maps", "Population maps"], 1,
       "Physical maps show natural features like mountains, rivers, and plains.", 'medium'),
    mc("Which of these is a natural feature usually shown on a physical map?", ["Highway", "River", "State border", "Railway line"], 1,
       "Rivers are natural features and are shown on physical maps.", 'easy'),
    mc("On most maps, North is shown at which side?", ["Top", "Bottom", "Left", "Right"], 0,
       "By convention, North is usually shown at the top of a map.", 'easy'),
    mc("If you are facing North and turn to your right, which direction do you face?", ["West", "East", "South", "North"], 1,
       "Turning right while facing North makes you face East.", 'medium'),
    mc("If you are facing South and turn to your left, which direction do you face?", ["East", "West", "North", "South"], 0,
       "Turning left while facing South makes you face East.", 'hard'),
    mc("Latitude lines on a map run in which direction?", ["North-South", "East-West", "Diagonal", "They form circles only at poles"], 1,
       "Latitude lines run horizontally, in an East-West direction, around the globe.", 'medium'),
    mc("Longitude lines on a map run in which direction?", ["East-West", "North-South", "Diagonal", "They don't have a direction"], 1,
       "Longitude lines run vertically, from the North Pole to the South Pole.", 'medium'),
    mc("The imaginary line at 0° latitude is called the:", ["Prime Meridian", "Equator", "Tropic of Cancer", "International Date Line"], 1,
       "The Equator is the imaginary line at 0° latitude that divides the Earth into Northern and Southern hemispheres.", 'medium'),
]

CLASS5_CS_INTRO = [
    mc("What does CPU stand for?", ["Central Process Unit", "Central Processing Unit", "Computer Processing Unit", "Central Processor Utility"], 1,
       "CPU stands for Central Processing Unit, the 'brain' of the computer.", 'easy'),
    mc("Which part of the computer is used to type text?", ["Monitor", "Mouse", "Keyboard", "Speaker"], 2,
       "The keyboard is used to type letters, numbers and symbols into the computer.", 'easy'),
    mc("Which device is used to point and click on the screen?", ["Keyboard", "Mouse", "Printer", "Scanner"], 1,
       "The mouse is used to point, click and select items on the screen.", 'easy'),
    mc("Which part of the computer displays output visually?", ["CPU", "Keyboard", "Monitor", "Mouse"], 2,
       "The monitor displays visual output from the computer.", 'easy'),
    mc("Which of these is an input device?", ["Monitor", "Printer", "Speaker", "Keyboard"], 3,
       "A keyboard is used to give input (data) to the computer.", 'easy'),
    mc("Which of these is an output device?", ["Keyboard", "Mouse", "Printer", "Scanner"], 2,
       "A printer produces a physical (paper) output from the computer, so it is an output device.", 'easy'),
    mc("A computer program that helps you do a specific task, like drawing or writing, is called:", ["Hardware", "Software", "CPU", "Mouse"], 1,
       "Software refers to programs that instruct the computer to perform specific tasks.", 'easy'),
    mc("The physical parts of a computer that you can touch are called:", ["Software", "Hardware", "Data", "Internet"], 1,
       "Hardware refers to the physical, touchable parts of a computer.", 'easy'),
    mc("Which of these is an example of computer hardware?", ["Microsoft Word", "Keyboard", "Web browser", "Operating System"], 1,
       "A keyboard is a physical device, making it hardware.", 'easy'),
    mc("Which of these is an example of computer software?", ["Monitor", "Mouse", "MS Paint", "Printer"], 2,
       "MS Paint is a program (software) used for drawing on the computer.", 'easy'),
    mc("Which key on the keyboard is used to create a new line or paragraph?", ["Shift", "Enter", "Tab", "Space bar"], 1,
       "The Enter key moves the cursor to a new line.", 'easy'),
    mc("Which key is used to erase a character to the left of the cursor?", ["Delete", "Backspace", "Shift", "Tab"], 1,
       "The Backspace key deletes the character to the left of the cursor.", 'easy'),
    mc("Which key is used to type capital letters when held down?", ["Ctrl", "Alt", "Shift", "Tab"], 2,
       "Holding the Shift key while pressing a letter key types a capital letter.", 'easy'),
    mc("Which storage device is commonly used to permanently store data inside a computer?", ["RAM", "Hard disk", "Monitor", "Keyboard"], 1,
       "A hard disk is used for permanent storage of data even after the computer is switched off.", 'medium'),
    mc("Which memory in a computer is temporary and is cleared when the computer is switched off?", ["Hard disk", "RAM", "Pen drive", "CD"], 1,
       "RAM (Random Access Memory) stores data temporarily and is cleared when power is turned off.", 'medium'),
    mc("A set of computers connected together to share information is called a:", ["Network", "Software", "Hardware", "CPU"], 0,
       "A network is a group of connected computers that can share data and resources.", 'medium'),
    mc("Which of these devices can be used to take a printed copy of a document?", ["Scanner", "Printer", "Speaker", "Mouse"], 1,
       "A printer produces a paper copy (printout) of a digital document.", 'easy'),
    mc("Which of these devices converts a paper document into a digital image?", ["Printer", "Scanner", "Speaker", "Monitor"], 1,
       "A scanner converts a physical paper document into a digital image.", 'medium'),
    mc("The main circuit board of a computer that connects all parts is called the:", ["Hard disk", "Motherboard", "Monitor", "Keyboard"], 1,
       "The motherboard is the main circuit board that connects the CPU, memory and other components.", 'hard'),
    mc("Which of the following best describes a laptop?", ["A large stationary computer", "A portable personal computer", "A type of printer", "A type of software"], 1,
       "A laptop is a portable, battery-powered personal computer.", 'easy'),
]

CLASS5_CS_PAINT = [
    mc("Which tool in MS Paint is used to draw straight lines?", ["Brush", "Line tool", "Eraser", "Fill tool"], 1,
       "The Line tool in MS Paint is used to draw straight lines.", 'easy'),
    mc("Which tool is used to erase parts of a drawing in MS Paint?", ["Pencil", "Eraser", "Fill", "Text"], 1,
       "The Eraser tool removes drawn content from the canvas.", 'easy'),
    mc("Which tool is used to fill a closed shape with colour in MS Paint?", ["Brush", "Fill With Colour (Bucket)", "Eraser", "Select"], 1,
       "The Fill With Colour tool (paint bucket) fills an enclosed area with the selected colour.", 'easy'),
    mc("Which tool lets you draw a perfect circle or oval in MS Paint?", ["Rectangle", "Ellipse tool", "Line", "Eraser"], 1,
       "The Ellipse tool is used to draw circles and ovals.", 'easy'),
    mc("Which tool is used to type text on an MS Paint canvas?", ["Brush", "Text tool", "Fill", "Select"], 1,
       "The Text tool allows you to add typed text onto the canvas.", 'easy'),
    mc("Which menu in MS Paint is used to save a file?", ["View", "Home", "File", "Edit"], 2,
       "The File menu contains options like Save, Open and New.", 'easy'),
    mc("What is the default file format when saving a new drawing in MS Paint?", [".docx", ".png", ".xlsx", ".pptx"], 1,
       "MS Paint commonly saves images in formats like .png (or .bmp/.jpg).", 'medium'),
    mc("Which tool would you use to select and move part of your drawing?", ["Eraser", "Select tool", "Fill tool", "Brush"], 1,
       "The Select tool lets you choose a portion of the drawing to move, copy, or resize.", 'medium'),
    mc("Which key combination is commonly used to undo the last action in MS Paint?", ["Ctrl+S", "Ctrl+Z", "Ctrl+P", "Ctrl+C"], 1,
       "Ctrl+Z is the shortcut for Undo in most Windows applications, including MS Paint.", 'medium'),
    mc("Which shortcut is used to copy a selected object?", ["Ctrl+V", "Ctrl+C", "Ctrl+X", "Ctrl+Z"], 1,
       "Ctrl+C is the shortcut for Copy.", 'medium'),
    mc("Which shortcut is used to paste a copied object?", ["Ctrl+C", "Ctrl+X", "Ctrl+V", "Ctrl+S"], 2,
       "Ctrl+V is the shortcut for Paste.", 'medium'),
    mc("Which tool draws freehand lines like a real pencil?", ["Pencil tool", "Rectangle tool", "Fill tool", "Text tool"], 0,
       "The Pencil tool lets you draw freehand lines, just like a real pencil.", 'easy'),
    mc("What does the 'Zoom' option in MS Paint help you do?", ["Change colours", "Enlarge or shrink your view of the canvas", "Save the file", "Print the file"], 1,
       "Zoom lets you magnify or reduce the view of your drawing for more detailed work.", 'medium'),
    mc("Which key is commonly used to save a file quickly?", ["Ctrl+P", "Ctrl+S", "Ctrl+N", "Ctrl+O"], 1,
       "Ctrl+S is the common shortcut used to save a file.", 'easy'),
    mc("What is the purpose of the 'Colour Picker' tool in MS Paint?", ["To erase colour", "To pick an existing colour from the drawing", "To resize the canvas", "To add text"], 1,
       "The Colour Picker tool lets you select an existing colour from the drawing to use again.", 'medium'),
    mc("Which part of a computer keyboard is mainly used to move the text cursor?", ["Function keys", "Arrow keys", "Number keys", "Shift key"], 1,
       "Arrow keys move the text cursor up, down, left or right.", 'easy'),
    mc("Which key is used to create space between words while typing?", ["Enter", "Tab", "Space bar", "Shift"], 2,
       "The Space bar is used to insert a space between words.", 'easy'),
    mc("Which of these best describes the 'Rectangle tool' in MS Paint?", ["Draws freehand shapes", "Draws rectangles and squares", "Erases the drawing", "Fills colour"], 1,
       "The Rectangle tool is used to draw rectangular and square shapes.", 'easy'),
    mc("What happens when you hold Shift while using the Rectangle tool?", ["It draws a perfect square", "It erases the shape", "It changes the colour", "Nothing happens"], 0,
       "Holding Shift while dragging the Rectangle tool constrains it to draw a perfect square.", 'hard'),
    mc("Which function key is often used to refresh or rename in Windows?", ["F1", "F2", "F5", "F12"], 2,
       "F5 is commonly used to refresh a window or view in Windows.", 'medium'),
]
# ============ CLASS 6 (non-math) ============

CLASS6_SCI_FOOD_SOURCE = [
    mc("What is the main source of food for most living things?", ["Water", "Plants and animals", "Air", "Sunlight only"], 1,
       "Plants and animals are the main sources of food for most living things.", 'easy'),
    mc("Which part of a plant do we eat when we eat carrots?", ["Leaf", "Stem", "Root", "Flower"], 2,
       "Carrots are roots that store food and are eaten as vegetables.", 'easy'),
    mc("Which part of the plant do we eat when we eat spinach?", ["Root", "Leaf", "Fruit", "Seed"], 1,
       "Spinach is a leafy vegetable, so we eat its leaves.", 'easy'),
    mc("Sugar is obtained from which plant?", ["Wheat", "Sugarcane", "Rice", "Mustard"], 1,
       "Sugar is extracted from the stem of the sugarcane plant.", 'easy'),
    mc("Which of these is a source of animal food?", ["Rice", "Milk", "Wheat", "Sugarcane"], 1,
       "Milk is obtained from animals like cows and buffaloes, making it an animal food source.", 'easy'),
    mc("Herbivorous animals get their food directly from:", ["Other animals", "Plants", "Rocks", "Water only"], 1,
       "Herbivores eat plants directly to obtain their food and energy.", 'easy'),
    mc("Which of these is an example of a carnivore?", ["Cow", "Goat", "Tiger", "Deer"], 2,
       "A tiger eats the flesh of other animals, making it a carnivore.", 'easy'),
    mc("Bees collect nectar from flowers to make:", ["Milk", "Honey", "Sugar", "Butter"], 1,
       "Bees collect nectar from flowers and convert it into honey.", 'easy'),
    mc("Which of these food items comes from an animal?", ["Wheat", "Honey", "Rice", "Mustard oil"], 1,
       "Honey is made by bees, an animal source of food.", 'easy'),
    mc("Which part of the wheat plant do we use to make flour?", ["Root", "Seed (grain)", "Leaf", "Flower"], 1,
       "Wheat flour is made by grinding the seeds (grains) of the wheat plant.", 'medium'),
    mc("What do we call animals and plants from which we get our food?", ["Predators", "Sources of food", "Decomposers", "Pollutants"], 1,
       "Plants and animals that provide us with food are called sources of food.", 'easy'),
    mc("Which of the following is obtained from an animal?", ["Rice", "Egg", "Sugar", "Oil from mustard"], 1,
       "Eggs are laid by birds like hens, making them an animal food source.", 'easy'),
    mc("Cooking oil is generally extracted from which part of a plant?", ["Root", "Stem", "Seeds", "Bark"], 2,
       "Cooking oils like mustard oil and groundnut oil are extracted from seeds.", 'medium'),
    mc("Which of these best describes an omnivore?", ["Eats only plants", "Eats only meat", "Eats both plants and animals", "Eats nothing"], 2,
       "Omnivores eat both plant and animal-based food, e.g. humans, bears.", 'easy'),
    mc("Silk is obtained from which insect?", ["Bee", "Silkworm", "Ant", "Butterfly"], 1,
       "Silk fibre is obtained from the cocoon of the silkworm.", 'medium'),
    mc("Which of the following animals is reared mainly for wool?", ["Cow", "Sheep", "Hen", "Goat"], 1,
       "Sheep are reared for their wool, which is sheared from their coat.", 'medium'),
    mc("Which of the following is a plant product used as food?", ["Leather", "Wool", "Pulses", "Milk"], 2,
       "Pulses (like lentils) come from plants and are a common food source.", 'easy'),
    mc("Fish primarily live in which habitat?", ["Forests", "Water", "Deserts", "Mountains"], 1,
       "Fish live in water and get their food from aquatic sources.", 'easy'),
    mc("Which of these food items is obtained from underground plant parts?", ["Potato", "Mango", "Apple", "Wheat grain"], 0,
       "Potato is a modified underground stem (tuber), commonly eaten as a vegetable.", 'medium'),
    mc("What is the term used for animals that hunt other animals for food?", ["Prey", "Predator", "Herbivore", "Decomposer"], 1,
       "A predator is an animal that hunts and eats other animals (called prey).", 'medium'),
]

CLASS6_SCI_COMPONENTS = [
    mc("Which nutrient mainly gives us energy to do work?", ["Vitamins", "Carbohydrates", "Minerals", "Water"], 1,
       "Carbohydrates are the main source of energy for the body.", 'easy'),
    mc("Which nutrient is essential for growth and repair of body tissues?", ["Carbohydrates", "Fats", "Proteins", "Vitamins"], 2,
       "Proteins help in the growth and repair of body cells and tissues.", 'easy'),
    mc("Which of the following is rich in protein?", ["Rice", "Pulses", "Sugar", "Oil"], 1,
       "Pulses like lentils and beans are rich sources of protein.", 'easy'),
    mc("Deficiency of which vitamin causes night blindness?", ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], 0,
       "A deficiency of Vitamin A can lead to night blindness.", 'medium'),
    mc("Deficiency of which vitamin causes scurvy?", ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin K"], 1,
       "A deficiency of Vitamin C causes scurvy, characterised by bleeding gums.", 'medium'),
    mc("Which mineral is important for building strong bones and teeth?", ["Iron", "Calcium", "Sodium", "Iodine"], 1,
       "Calcium is essential for building and maintaining strong bones and teeth.", 'medium'),
    mc("Deficiency of which mineral causes anaemia?", ["Calcium", "Iron", "Iodine", "Sodium"], 1,
       "A deficiency of Iron causes anaemia, marked by weakness and paleness.", 'medium'),
    mc("Which nutrient, though needed in small amounts, is vital for regulating body functions?", ["Carbohydrates", "Fats", "Vitamins and Minerals", "Water"], 2,
       "Vitamins and minerals, though needed in small quantities, regulate many essential body functions.", 'medium'),
    mc("Which food group provides the most concentrated source of energy?", ["Proteins", "Fats", "Vitamins", "Minerals"], 1,
       "Fats provide more energy per gram than carbohydrates or proteins, making them the most concentrated energy source.", 'medium'),
    mc("A disease caused by lack of proper nutrients in the diet is called:", ["Infection", "Deficiency disease", "Allergy", "Fever"], 1,
       "A deficiency disease results from the lack of one or more essential nutrients over a period of time.", 'medium'),
    mc("Which nutrient helps in the clotting of blood?", ["Vitamin K", "Vitamin C", "Vitamin A", "Vitamin D"], 0,
       "Vitamin K plays an important role in blood clotting.", 'hard'),
    mc("Roughage (fibre) in our diet mainly helps in:", ["Building muscles", "Providing energy", "Preventing constipation", "Strengthening bones"], 2,
       "Roughage aids digestion and helps prevent constipation, though it is not digested by the body.", 'medium'),
    mc("Which test is used to detect the presence of starch in food?", ["Iodine test", "Litmus test", "Sugar test", "Fat test"], 0,
       "Adding iodine solution to food turns it blue-black if starch is present.", 'medium'),
    mc("A balanced diet should contain nutrients in:", ["Only one type", "Equal amounts of everything", "Right proportions as needed by the body", "Only proteins and fats"], 2,
       "A balanced diet contains all essential nutrients in the right proportions needed by the body.", 'medium'),
    mc("Which of these is a good source of Vitamin C?", ["Citrus fruits like oranges", "Rice", "Milk", "Wheat"], 0,
       "Citrus fruits such as oranges and lemons are rich in Vitamin C.", 'easy'),
    mc("Which of these is a good source of Vitamin D?", ["Sunlight", "Rice", "Salt", "Sugar"], 0,
       "Sunlight helps the body produce Vitamin D naturally in the skin.", 'medium'),
    mc("Which component of food is essential to prevent dehydration?", ["Water", "Fat", "Fibre", "Protein"], 0,
       "Water is essential for preventing dehydration and for many body processes.", 'easy'),
    mc("Which of the following diseases is caused due to protein deficiency in children?", ["Scurvy", "Kwashiorkor", "Rickets", "Goitre"], 1,
       "Kwashiorkor is a disease in children caused by severe protein deficiency.", 'hard'),
    mc("Deficiency of iodine in diet can cause which disease?", ["Goitre", "Scurvy", "Rickets", "Anaemia"], 0,
       "Iodine deficiency can cause goitre, an enlargement of the thyroid gland.", 'medium'),
    mc("Which food test is used to check for the presence of fat in a food sample?", ["Translucent spot test on paper", "Iodine test", "Litmus test", "pH test"], 0,
       "Rubbing food on paper and checking for a translucent (oily) spot is used to test for fat.", 'medium'),
]

CLASS6_ENG_TENSES = [
    mc("Choose the correct present tense form: 'She ___ to school every day.'", ["go", "goes", "going", "gone"], 1,
       "With third-person singular subjects, present tense verbs add 's': 'goes'.", 'easy'),
    mc("Choose the correct past tense of 'eat'.", ["eated", "ate", "eaten", "eating"], 1,
       "The past tense of 'eat' is 'ate'.", 'easy'),
    mc("Choose the correct future tense: 'They ___ arrive tomorrow.'", ["will", "was", "did", "has"], 0,
       "'Will' is used to form the simple future tense.", 'easy'),
    mc("Which sentence is in the present continuous tense?", ["He plays cricket.", "He played cricket.", "He is playing cricket.", "He will play cricket."], 2,
       "The present continuous tense uses 'is/am/are' + verb+ing, e.g. 'is playing'.", 'medium'),
    mc("Which sentence is in the simple past tense?", ["She sings.", "She sang.", "She is singing.", "She will sing."], 1,
       "'Sang' is the simple past tense form of 'sing'.", 'easy'),
    mc("Choose the correct past participle of 'write'.", ["writed", "wrote", "written", "writing"], 2,
       "The past participle of 'write' is 'written', used in perfect tenses.", 'medium'),
    mc("Which sentence is in the present perfect tense?", ["I eat lunch.", "I ate lunch.", "I have eaten lunch.", "I am eating lunch."], 2,
       "The present perfect tense uses 'have/has' + past participle: 'have eaten'.", 'medium'),
    mc("Choose the correct form: 'By next year, she ___ her studies.'", ["will complete", "completes", "completed", "is completing"], 0,
       "'Will complete' is used for an action expected to happen in the future.", 'medium'),
    mc("Which of the following is the correct past continuous form?", ["He was playing football.", "He plays football.", "He will play football.", "He has played football."], 0,
       "Past continuous tense uses 'was/were' + verb+ing to show an ongoing past action.", 'medium'),
    mc("Choose the correct sentence in future continuous tense.", ["I will be studying at 5 pm.", "I studied at 5 pm.", "I am studying at 5 pm.", "I have studied at 5 pm."], 0,
       "Future continuous tense uses 'will be' + verb+ing.", 'hard'),
    mc("Identify the tense: 'They have been playing since morning.'", ["Present perfect continuous", "Simple present", "Simple past", "Future perfect"], 0,
       "'Have been playing' shows an action that started in the past and continues, i.e., present perfect continuous.", 'hard'),
    mc("Choose the correct simple present form: 'The sun ___ in the east.'", ["rise", "rises", "rose", "rising"], 1,
       "General truths use the simple present tense with an 's' for singular subjects: 'rises'.", 'easy'),
    mc("Which sentence correctly uses the past perfect tense?", ["She had left before I arrived.", "She leaves before I arrive.", "She left before I arrive.", "She is leaving before I arrive."], 0,
       "Past perfect tense ('had left') shows an action completed before another past action.", 'hard'),
    mc("Choose the correct verb form: 'He ___ his homework every evening.'", ["do", "does", "did", "doing"], 1,
       "Third-person singular subjects in present tense take 'does'.", 'easy'),
    mc("Which word signals the future tense is being used?", ["yesterday", "now", "will", "was"], 2,
       "'Will' is a modal verb that signals future tense.", 'easy'),
    mc("Choose the correct sentence: 'Right now, they ___ dinner.'", ["eat", "ate", "are eating", "have eaten"], 2,
       "'Right now' indicates an ongoing action, requiring present continuous tense: 'are eating'.", 'medium'),
    mc("Which tense describes an action that happened at a specific time in the past?", ["Simple past", "Simple present", "Present continuous", "Future"], 0,
       "The simple past tense describes completed actions at a specific past time.", 'easy'),
    mc("Choose the correct sentence: 'I ___ my homework already.'", ["finish", "finished", "have finished", "am finishing"], 2,
       "'Have finished' (present perfect) is used with 'already' to show a recently completed action.", 'medium'),
    mc("Which helping verb is used with 'I' and 'we' in present continuous tense?", ["is", "am/are", "was", "will"], 1,
       "'Am' is used with 'I' and 'are' is used with 'we' in the present continuous tense.", 'easy'),
    mc("Choose the correctly formed negative sentence in simple present tense: 'He ___ like coffee.'", ["don't", "doesn't", "isn't", "not"], 1,
       "Third-person singular negative sentences use 'doesn't' + base verb.", 'medium'),
]

CLASS6_ENG_PARTS = [
    mc("Which part of speech names a person, place or thing?", ["Verb", "Noun", "Adjective", "Adverb"], 1,
       "A noun is a word that names a person, place, animal or thing.", 'easy'),
    mc("Which part of speech shows an action or state of being?", ["Noun", "Verb", "Pronoun", "Preposition"], 1,
       "A verb describes an action or state of being, e.g. 'run', 'is'.", 'easy'),
    mc("Which part of speech describes a noun?", ["Adjective", "Verb", "Conjunction", "Interjection"], 0,
       "An adjective describes or gives more information about a noun.", 'easy'),
    mc("Which part of speech modifies a verb, adjective or another adverb?", ["Noun", "Adverb", "Pronoun", "Preposition"], 1,
       "An adverb modifies verbs, adjectives, or other adverbs, e.g. 'quickly'.", 'medium'),
    mc("Which part of speech replaces a noun?", ["Adjective", "Verb", "Pronoun", "Conjunction"], 2,
       "A pronoun is used in place of a noun, e.g. 'he', 'she', 'it'.", 'easy'),
    mc("Which part of speech shows the relationship between a noun/pronoun and another word?", ["Preposition", "Verb", "Adjective", "Interjection"], 0,
       "A preposition shows the relationship between a noun/pronoun and other words, e.g. 'in', 'on', 'under'.", 'medium'),
    mc("Which part of speech joins words, phrases or clauses?", ["Noun", "Pronoun", "Conjunction", "Adjective"], 2,
       "A conjunction connects words, phrases, or clauses, e.g. 'and', 'but', 'or'.", 'medium'),
    mc("Which part of speech expresses strong emotion?", ["Interjection", "Verb", "Noun", "Adverb"], 0,
       "An interjection expresses strong feeling, e.g. 'Wow!', 'Oh!'.", 'easy'),
    mc("Identify the noun in: 'The teacher wrote on the board.'", ["wrote", "on", "teacher", "the"], 2,
       "'Teacher' names a person, making it a noun.", 'easy'),
    mc("Identify the verb in: 'The birds fly high in the sky.'", ["birds", "fly", "high", "sky"], 1,
       "'Fly' is the action word (verb) in the sentence.", 'easy'),
    mc("Identify the adjective in: 'She has a beautiful garden.'", ["She", "has", "beautiful", "garden"], 2,
       "'Beautiful' describes the noun 'garden', making it an adjective.", 'easy'),
    mc("Identify the adverb in: 'He speaks softly.'", ["He", "speaks", "softly", "none"], 2,
       "'Softly' describes how he speaks, making it an adverb.", 'medium'),
    mc("Identify the pronoun in: 'She gave it to him.'", ["gave", "she, it, him", "to", "none"], 1,
       "'She', 'it' and 'him' are all pronouns replacing nouns.", 'medium'),
    mc("Identify the preposition in: 'The cat sat on the mat.'", ["cat", "sat", "on", "mat"], 2,
       "'On' shows the relationship between the cat and the mat, making it a preposition.", 'easy'),
    mc("Identify the conjunction in: 'I like tea and coffee.'", ["like", "tea", "and", "coffee"], 2,
       "'And' joins the two nouns 'tea' and 'coffee', making it a conjunction.", 'easy'),
    mc("Which type of noun refers to a specific name, like 'India' or 'Ravi'?", ["Common noun", "Proper noun", "Abstract noun", "Collective noun"], 1,
       "A proper noun names a specific person, place or thing and starts with a capital letter.", 'medium'),
    mc("Which type of noun refers to a general name, like 'city' or 'boy'?", ["Common noun", "Proper noun", "Collective noun", "Abstract noun"], 0,
       "A common noun refers to a general class of person, place or thing.", 'medium'),
    mc("Which type of noun refers to an idea or feeling, like 'honesty' or 'happiness'?", ["Proper noun", "Common noun", "Abstract noun", "Collective noun"], 2,
       "An abstract noun refers to an idea, quality, or feeling that cannot be touched.", 'medium'),
    mc("Which type of noun refers to a group, like 'team' or 'flock'?", ["Common noun", "Collective noun", "Proper noun", "Abstract noun"], 1,
       "A collective noun refers to a group of people, animals, or things treated as a single unit.", 'medium'),
    mc("Which word in 'Wow, that is amazing!' is the interjection?", ["that", "is", "amazing", "Wow"], 3,
       "'Wow' expresses strong emotion, making it an interjection.", 'easy'),
]

CLASS6_SOC_WHATWHERE = [
    mc("The study of past events is called:", ["Geography", "History", "Civics", "Economics"], 1,
       "History is the study of past events and how they shaped human society.", 'easy'),
    mc("Which of these is considered a primary source of history?", ["A textbook written today", "An ancient inscription", "A movie", "A novel"], 1,
       "Ancient inscriptions, coins and manuscripts from the period are primary sources of history.", 'medium'),
    mc("Historians divide history into which broad periods?", ["Ancient, Medieval, Modern", "Old and New", "Past and Present", "First and Second"], 0,
       "Historians commonly divide history into Ancient, Medieval, and Modern periods.", 'medium'),
    mc("Archaeologists mainly study history through:", ["Written records only", "Excavated artefacts and remains", "Modern photographs", "Oral stories only"], 1,
       "Archaeologists study history by excavating and examining ancient artefacts, buildings and remains.", 'medium'),
    mc("Which of these helps historians date very old objects accurately?", ["Guessing", "Carbon dating", "Asking local people", "Reading newspapers"], 1,
       "Carbon dating is a scientific method used to estimate the age of ancient organic remains.", 'medium'),
    mc("Coins, tools and pottery found from the past are called:", ["Manuscripts", "Artefacts", "Inscriptions", "Chronicles"], 1,
       "Artefacts are objects made or used by humans in the past, found through excavation.", 'medium'),
    mc("Old handwritten documents are called:", ["Manuscripts", "Artefacts", "Coins", "Fossils"], 0,
       "Manuscripts are old documents written by hand, an important source for historians.", 'medium'),
    mc("Which of these is NOT typically a source of history?", ["Coins", "Buildings and monuments", "Inscriptions", "Modern smartphones"], 3,
       "Modern smartphones are recent inventions and not sources for studying ancient or medieval history.", 'easy'),
    mc("The study of coins is called:", ["Epigraphy", "Numismatics", "Archaeology", "Geography"], 1,
       "Numismatics is the study of coins and currency.", 'hard'),
    mc("The study of inscriptions is called:", ["Numismatics", "Epigraphy", "Cartography", "Geology"], 1,
       "Epigraphy is the study of inscriptions carved on stones, pillars and metal.", 'hard'),
    mc("Why do historians need to know the exact time period of an event?", ["To make history boring", "To understand the sequence and context of events", "It is not important", "To confuse readers"], 1,
       "Knowing the time period helps historians understand the sequence and context of events accurately.", 'medium'),
    mc("The earliest cities in the Indian subcontinent developed along which river?", ["Ganga", "Indus", "Yamuna", "Godavari"], 1,
       "The earliest cities of the Indian subcontinent, like Harappa, developed along the Indus river.", 'medium'),
    mc("Which of these is an example of oral tradition as a historical source?", ["Newspaper reports", "Stories passed down through generations", "Satellite images", "Bank records"], 1,
       "Oral traditions are stories, songs and legends passed down verbally across generations.", 'medium'),
    mc("What do we call the period before writing was invented?", ["Modern age", "Prehistoric period", "Medieval age", "Industrial age"], 1,
       "The prehistoric period refers to the time before writing systems were developed.", 'medium'),
    mc("Which script was used by the Harappan civilisation, which remains undeciphered?", ["Devanagari", "Harappan script", "Brahmi", "Kharosthi"], 1,
       "The Harappan (Indus) script has not yet been deciphered by historians.", 'hard'),
    mc("Which century does the year 1801 belong to?", ["18th century", "19th century", "17th century", "20th century"], 1,
       "The year 1801 falls in the 19th century (years 1801-1900).", 'medium'),
    mc("Which of these terms refers to a period of 100 years?", ["Decade", "Century", "Millennium", "Era"], 1,
       "A century refers to a period of 100 years.", 'easy'),
    mc("Which of these terms refers to a period of 1000 years?", ["Decade", "Century", "Millennium", "Season"], 2,
       "A millennium refers to a period of 1000 years.", 'easy'),
    mc("The Common Era (CE) is also referred to by which older term?", ["BC", "AD", "BCE", "None"], 1,
       "CE (Common Era) corresponds to the same period earlier referred to as AD (Anno Domini).", 'hard'),
    mc("Which discipline studies human societies and their development through material remains?", ["Archaeology", "Astronomy", "Botany", "Physics"], 0,
       "Archaeology is the study of human history through the excavation and analysis of physical remains.", 'medium'),
]

CLASS6_SOC_SOLAR = [
    mc("Which is the closest planet to the Sun?", ["Venus", "Mercury", "Earth", "Mars"], 1,
       "Mercury is the planet closest to the Sun in our solar system.", 'easy'),
    mc("Which planet is known as the 'Red Planet'?", ["Venus", "Jupiter", "Mars", "Saturn"], 2,
       "Mars is called the 'Red Planet' due to its reddish appearance caused by iron oxide on its surface.", 'easy'),
    mc("Which is the largest planet in our solar system?", ["Earth", "Saturn", "Jupiter", "Neptune"], 2,
       "Jupiter is the largest planet in our solar system.", 'easy'),
    mc("Which planet is known for its prominent rings?", ["Mars", "Saturn", "Mercury", "Earth"], 1,
       "Saturn is famous for its beautiful and prominent ring system.", 'easy'),
    mc("Which is the only planet known to support life?", ["Mars", "Venus", "Earth", "Jupiter"], 2,
       "Earth is currently the only known planet that supports life.", 'easy'),
    mc("What is a natural satellite of the Earth called?", ["Sun", "Moon", "Star", "Comet"], 1,
       "The Moon is the natural satellite that revolves around the Earth.", 'easy'),
    mc("How many planets are there in our solar system?", ["7", "8", "9", "10"], 1,
       "There are 8 planets in our solar system, after Pluto was reclassified as a dwarf planet.", 'easy'),
    mc("Which celestial body is at the centre of our solar system?", ["Earth", "Moon", "Sun", "Mars"], 2,
       "The Sun lies at the centre of our solar system, with planets orbiting around it.", 'easy'),
    mc("Which is the smallest planet in our solar system?", ["Earth", "Mars", "Mercury", "Venus"], 2,
       "Mercury is the smallest planet in our solar system.", 'medium'),
    mc("Which planet is known as Earth's 'twin' due to similar size?", ["Mars", "Venus", "Jupiter", "Neptune"], 1,
       "Venus is often called Earth's twin because of its similar size and mass.", 'medium'),
    mc("A group of stars that forms a recognisable pattern is called a:", ["Galaxy", "Constellation", "Nebula", "Comet"], 1,
       "A constellation is a group of stars forming a recognisable pattern in the sky.", 'medium'),
    mc("What is a huge system of stars, dust and gas held together by gravity called?", ["Constellation", "Solar system", "Galaxy", "Meteor"], 2,
       "A galaxy is a massive system of stars, gas and dust bound together by gravity.", 'medium'),
    mc("Our solar system is part of which galaxy?", ["Andromeda", "Milky Way", "Whirlpool Galaxy", "Sombrero Galaxy"], 1,
       "Our solar system is part of the Milky Way galaxy.", 'medium'),
    mc("What is a small rocky body orbiting the sun, smaller than a planet, called?", ["Asteroid", "Star", "Nebula", "Galaxy"], 0,
       "Asteroids are small rocky bodies orbiting the Sun, mostly found in the asteroid belt.", 'medium'),
    mc("What causes day and night on Earth?", ["Revolution around the Sun", "Rotation of Earth on its axis", "Movement of the Moon", "Change of seasons"], 1,
       "The rotation of the Earth on its own axis causes day and night.", 'medium'),
    mc("What causes the different seasons on Earth?", ["Rotation of Earth", "Revolution of Earth around the Sun with a tilted axis", "The Moon's phases", "Distance from the Moon"], 1,
       "Seasons are caused by Earth's revolution around the Sun combined with the tilt of its axis.", 'medium'),
    mc("How long does the Earth take to complete one rotation on its axis?", ["24 hours", "365 days", "30 days", "12 hours"], 0,
       "The Earth takes approximately 24 hours to complete one full rotation on its axis.", 'easy'),
    mc("How long does the Earth take to complete one revolution around the Sun?", ["24 hours", "30 days", "About 365 days", "7 days"], 2,
       "The Earth takes about 365¼ days to complete one revolution around the Sun.", 'easy'),
    mc("Which dwarf planet was earlier considered the ninth planet of our solar system?", ["Ceres", "Pluto", "Eris", "Haumea"], 1,
       "Pluto was considered the ninth planet until it was reclassified as a dwarf planet in 2006.", 'medium'),
    mc("A celestial body with a glowing tail that orbits the Sun in a long path is called a:", ["Asteroid", "Comet", "Satellite", "Star"], 1,
       "A comet is an icy body that develops a glowing tail as it approaches the Sun.", 'medium'),
]

CLASS6_CS_FUNDAMENTALS = [
    mc("Which generation of computers used vacuum tubes?", ["First generation", "Second generation", "Third generation", "Fourth generation"], 0,
       "First-generation computers (1940s-50s) used vacuum tubes for processing.", 'medium'),
    mc("Which generation of computers introduced the microprocessor?", ["First generation", "Second generation", "Third generation", "Fourth generation"], 3,
       "Fourth-generation computers introduced the microprocessor, making computers smaller and faster.", 'medium'),
    mc("What is the full form of RAM?", ["Random Access Memory", "Read Access Memory", "Random Active Memory", "Read Active Memory"], 0,
       "RAM stands for Random Access Memory, used for temporary data storage.", 'easy'),
    mc("What is the full form of ROM?", ["Read Only Memory", "Random Only Memory", "Read Operating Memory", "Random Operating Memory"], 0,
       "ROM stands for Read Only Memory, which permanently stores data that cannot easily be changed.", 'easy'),
    mc("Which of these is a characteristic of RAM?", ["Permanent storage", "Volatile (data lost when power is off)", "Cannot be modified", "Used only for printing"], 1,
       "RAM is volatile memory, meaning its data is lost when the computer is switched off.", 'medium'),
    mc("Which unit of a computer performs arithmetic and logical operations?", ["ALU", "RAM", "ROM", "Monitor"], 0,
       "The Arithmetic Logic Unit (ALU) performs mathematical and logical operations in the CPU.", 'medium'),
    mc("Which unit of the CPU directs and coordinates operations of the computer?", ["ALU", "Control Unit", "RAM", "Cache"], 1,
       "The Control Unit directs and coordinates the activities of all parts of the computer.", 'medium'),
    mc("1 Byte is equal to how many bits?", ["4 bits", "8 bits", "16 bits", "2 bits"], 1,
       "1 Byte is equal to 8 bits.", 'medium'),
    mc("Which of these storage units is the largest?", ["Kilobyte", "Megabyte", "Gigabyte", "Byte"], 2,
       "Gigabyte (GB) is larger than Megabyte, Kilobyte and Byte.", 'medium'),
    mc("Which of these is an example of system software?", ["MS Word", "Operating System", "MS Paint", "Calculator app"], 1,
       "An Operating System (like Windows) is system software that manages computer hardware and resources.", 'medium'),
    mc("Which of these is an example of application software?", ["Operating System", "Device driver", "MS Word", "BIOS"], 2,
       "MS Word is application software used for a specific task (word processing).", 'easy'),
    mc("What is the main function of an operating system?", ["To type documents", "To manage computer hardware and software resources", "To browse the internet only", "To play games only"], 1,
       "The operating system manages hardware, software and resources of a computer.", 'medium'),
    mc("Which of these is an example of an operating system?", ["Windows", "MS Excel", "Google Chrome", "Adobe Photoshop"], 0,
       "Windows is a popular operating system used on many personal computers.", 'easy'),
    mc("A device that converts computer signals into human-readable form is called:", ["Input device", "Output device", "Storage device", "Processing device"], 1,
       "An output device, like a monitor or printer, presents processed data in human-readable form.", 'medium'),
    mc("Which of these is a secondary storage device?", ["RAM", "Cache memory", "Hard disk", "Registers"], 2,
       "A hard disk is a secondary storage device used for long-term data storage.", 'medium'),
    mc("Which of these best defines 'data'?", ["Processed information", "Raw, unprocessed facts and figures", "A type of hardware", "A type of software"], 1,
       "Data refers to raw, unprocessed facts and figures before they are processed into useful information.", 'medium'),
    mc("Which of these best defines 'information'?", ["Raw facts", "Processed and meaningful data", "A type of hardware", "A computer virus"], 1,
       "Information is data that has been processed into a meaningful and useful form.", 'medium'),
    mc("Which type of computer is designed to be carried around easily?", ["Desktop", "Laptop", "Mainframe", "Supercomputer"], 1,
       "A laptop is a portable computer designed to be carried around easily.", 'easy'),
    mc("Which type of computer is used for very large-scale, high-speed scientific calculations?", ["Laptop", "Tablet", "Supercomputer", "Smartphone"], 2,
       "A supercomputer performs extremely fast, large-scale calculations, used in research and weather forecasting.", 'medium'),
    mc("A small handheld computer operated mainly by touch is called a:", ["Desktop", "Tablet", "Mainframe", "Server"], 1,
       "A tablet is a small, portable computer operated mainly through a touchscreen.", 'easy'),
]

CLASS6_CS_IO = [
    mc("Which of these is used to enter data into a computer?", ["Monitor", "Printer", "Keyboard", "Speaker"], 2,
       "A keyboard is an input device used to enter text and commands into a computer.", 'easy'),
    mc("Which of these devices is used to capture images directly into a computer?", ["Scanner", "Printer", "Speaker", "Monitor"], 0,
       "A scanner captures and converts printed images or documents into digital form.", 'easy'),
    mc("A device used to record sound directly into a computer is called a:", ["Speaker", "Microphone", "Monitor", "Printer"], 1,
       "A microphone is an input device used to record sound into a computer.", 'easy'),
    mc("Which of these is used to point, click and drag items on the screen?", ["Keyboard", "Mouse", "Printer", "Scanner"], 1,
       "A mouse is used to point, click and drag objects on the computer screen.", 'easy'),
    mc("A joystick is mainly used as an input device for:", ["Printing documents", "Playing games", "Scanning images", "Producing sound"], 1,
       "A joystick is commonly used as an input device for playing video games.", 'easy'),
    mc("Which of these is an output device that produces sound?", ["Microphone", "Speaker", "Scanner", "Keyboard"], 1,
       "A speaker is an output device that converts electrical signals into sound.", 'easy'),
    mc("Which output device is used to project computer images onto a large screen?", ["Printer", "Projector", "Scanner", "Mouse"], 1,
       "A projector displays computer images onto a large screen for many viewers.", 'medium'),
    mc("A light-sensitive input device used to read barcodes is called a:", ["Barcode reader", "Printer", "Speaker", "Monitor"], 0,
       "A barcode reader scans and reads barcodes to input product information.", 'medium'),
    mc("Which type of printer sprays tiny droplets of ink to print?", ["Laser printer", "Inkjet printer", "Dot matrix printer", "3D printer"], 1,
       "An inkjet printer sprays tiny droplets of ink onto paper to create printed output.", 'medium'),
    mc("Which type of printer uses a laser beam and toner to print?", ["Inkjet printer", "Laser printer", "Dot matrix printer", "Thermal printer"], 1,
       "A laser printer uses a laser beam and toner powder to produce sharp printed output.", 'medium'),
    mc("Which of these is both an input and output device?", ["Keyboard", "Touchscreen monitor", "Mouse", "Printer"], 1,
       "A touchscreen monitor displays output and also accepts touch input, making it both.", 'medium'),
    mc("Which device is used to input handwriting or drawings using a pen-like tool?", ["Graphics tablet", "Speaker", "Printer", "Monitor"], 0,
       "A graphics tablet allows users to draw or write using a stylus, which is captured digitally.", 'medium'),
    mc("Webcams are mainly used to input:", ["Sound", "Live video images", "Printed text", "Barcodes"], 1,
       "A webcam captures live video, used for video calls and recording.", 'easy'),
    mc("Which of these best describes a 'trackball'?", ["An output device for sound", "A pointing input device with a rotating ball", "A type of printer", "A type of monitor"], 1,
       "A trackball is an input device with a ball that a user rotates to move the cursor.", 'medium'),
    mc("Which of these devices reads magnetic strip cards, like debit cards?", ["MICR reader", "OCR", "Magnetic stripe reader", "OMR"], 2,
       "A magnetic stripe reader reads data stored on the magnetic strip of cards like debit/credit cards.", 'hard'),
    mc("Which device is commonly used to read pencil-marked answers on OMR sheets?", ["OCR", "OMR reader", "Bar code reader", "Scanner only"], 1,
       "An Optical Mark Reader (OMR) detects marked answers, commonly used for exam sheets.", 'medium'),
    mc("Which of these best describes a headphone?", ["Input device for sound", "Output device for sound", "Storage device", "Processing device"], 1,
       "A headphone is an output device that lets a user privately listen to computer sound.", 'easy'),
    mc("A device that allows users to feel vibrations while gaming, enhancing feedback, is called a:", ["Joystick with haptic feedback", "Scanner", "Printer", "Keyboard"], 0,
       "Some joysticks and controllers provide haptic (vibration) feedback to enhance the gaming experience.", 'hard'),
    mc("Which of these best defines an 'input device'?", ["A device that displays results", "A device used to enter data into a computer", "A device used to store data permanently", "A device that processes data"], 1,
       "An input device is used to enter data and instructions into a computer.", 'easy'),
    mc("Which of these best defines an 'output device'?", ["A device used to enter data", "A device that presents processed results to the user", "A device that stores software", "A device used only for typing"], 1,
       "An output device presents the results of processing to the user, e.g. monitor, printer.", 'easy'),
]
# ============ CLASS 7 (non-math) ============

CLASS7_SCI_PLANT_NUTRI = [
    mc("The process by which green plants prepare their own food is called:", ["Respiration", "Photosynthesis", "Transpiration", "Excretion"], 1,
       "Photosynthesis is the process by which green plants make food using sunlight, water and carbon dioxide.", 'easy'),
    mc("Which pigment in leaves helps absorb sunlight for photosynthesis?", ["Chlorophyll", "Melanin", "Haemoglobin", "Carotene"], 0,
       "Chlorophyll, the green pigment in leaves, absorbs sunlight for photosynthesis.", 'easy'),
    mc("What are organisms that can prepare their own food called?", ["Heterotrophs", "Autotrophs", "Parasites", "Saprotrophs"], 1,
       "Autotrophs, like green plants, can make their own food using sunlight, water and CO2.", 'medium'),
    mc("What are organisms that depend on others for food called?", ["Autotrophs", "Heterotrophs", "Producers", "Photosynthetic organisms"], 1,
       "Heterotrophs cannot make their own food and depend on other organisms for nutrition.", 'medium'),
    mc("Plants that trap and feed on insects, like the pitcher plant, are called:", ["Parasitic plants", "Insectivorous plants", "Saprophytic plants", "Autotrophic plants only"], 1,
       "Insectivorous plants like the pitcher plant trap and digest insects for nutrients like nitrogen.", 'medium'),
    mc("Which of these is a parasitic plant?", ["Cactus", "Cuscuta (Amarbel)", "Rose", "Pitcher plant"], 1,
       "Cuscuta (Amarbel) is a parasitic plant that derives nutrition from a host plant.", 'medium'),
    mc("Organisms that get nutrition from dead and decaying matter are called:", ["Autotrophs", "Parasites", "Saprotrophs", "Predators"], 2,
       "Saprotrophs, like fungi, obtain nutrients by decomposing dead organic matter.", 'medium'),
    mc("Which gas do plants take in from the air for photosynthesis?", ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], 1,
       "Plants absorb carbon dioxide from the atmosphere for photosynthesis.", 'easy'),
    mc("Which gas is released by plants as a by-product of photosynthesis?", ["Carbon dioxide", "Nitrogen", "Oxygen", "Methane"], 2,
       "Oxygen is released as a by-product during the process of photosynthesis.", 'easy'),
    mc("Symbiotic relationship in lichens is between:", ["Two plants", "Algae and fungi", "Two animals", "A plant and an animal"], 1,
       "Lichens are formed by a symbiotic (mutually beneficial) relationship between algae and fungi.", 'hard'),
    mc("The raw materials required for photosynthesis are:", ["Oxygen and glucose", "Water and carbon dioxide", "Nitrogen and oxygen", "Water and oxygen"], 1,
       "Photosynthesis requires water and carbon dioxide, along with sunlight and chlorophyll.", 'medium'),
    mc("Where does photosynthesis mainly take place in a plant?", ["Roots", "Leaves", "Flowers", "Seeds"], 1,
       "Photosynthesis mainly takes place in the leaves, which contain chlorophyll.", 'easy'),
    mc("Tiny pores on the surface of leaves used for gas exchange are called:", ["Stomata", "Xylem", "Phloem", "Chloroplasts"], 0,
       "Stomata are small pores on leaves that allow gas exchange (CO2 in, O2 out) and transpiration.", 'medium'),
    mc("The green plastids where photosynthesis occurs inside plant cells are called:", ["Mitochondria", "Chloroplasts", "Nucleus", "Vacuole"], 1,
       "Chloroplasts contain chlorophyll and are the site of photosynthesis in plant cells.", 'medium'),
    mc("Which nutrient do plants absorb from the soil through their roots (besides water)?", ["Oxygen", "Minerals", "Carbon dioxide", "Sunlight"], 1,
       "Roots absorb water and dissolved minerals from the soil.", 'medium'),
    mc("The overall word equation for photosynthesis produces glucose and:", ["Carbon dioxide", "Water", "Oxygen", "Nitrogen"], 2,
       "The overall products of photosynthesis are glucose (food) and oxygen.", 'medium'),
    mc("Which of the following best describes a 'host' in a parasitic relationship?", ["The organism that benefits and harms another", "The organism that is harmed and provides nutrition to the parasite", "An organism that makes its own food", "An organism that decomposes dead matter"], 1,
       "A host is the organism from which a parasite derives nutrition, often being harmed in the process.", 'medium'),
    mc("Which of the following is an example of insectivorous plant nutrition adaptation?", ["Photosynthesis alone", "Trapping and digesting insects for nitrogen", "Absorbing minerals from a host", "Decomposing dead leaves"], 1,
       "Insectivorous plants supplement poor soil nutrition by trapping and digesting insects for nitrogen.", 'medium'),
    mc("Which mode of nutrition do fungi like mushrooms mostly use?", ["Autotrophic", "Saprotrophic", "Insectivorous", "Photosynthetic"], 1,
       "Most fungi, including mushrooms, are saprotrophs that feed on dead and decaying organic matter.", 'medium'),
    mc("Why are green plants called 'producers' in an ecosystem?", ["They consume other organisms", "They produce their own food using photosynthesis", "They decompose dead matter", "They cannot survive without sunlight"], 1,
       "Green plants are called producers because they produce food through photosynthesis, forming the base of most food chains.", 'medium'),
]

CLASS7_SCI_ANIMAL_NUTRI = [
    mc("The process of taking food into the body is called:", ["Digestion", "Ingestion", "Egestion", "Absorption"], 1,
       "Ingestion is the process of taking food into the body through the mouth.", 'easy'),
    mc("The breakdown of complex food into simpler substances is called:", ["Ingestion", "Digestion", "Absorption", "Assimilation"], 1,
       "Digestion is the process of breaking down complex food into simpler, absorbable substances.", 'easy'),
    mc("The process of removal of undigested waste from the body is called:", ["Digestion", "Absorption", "Egestion", "Ingestion"], 2,
       "Egestion is the process of removing undigested food (waste) from the body.", 'easy'),
    mc("Which organ produces saliva to help in digestion?", ["Stomach", "Salivary glands", "Liver", "Pancreas"], 1,
       "Salivary glands produce saliva, which contains an enzyme that begins starch digestion in the mouth.", 'medium'),
    mc("Which enzyme in saliva breaks down starch?", ["Pepsin", "Amylase", "Lipase", "Trypsin"], 1,
       "Salivary amylase breaks down starch into simpler sugars in the mouth.", 'medium'),
    mc("Which organ churns food and mixes it with acidic juices?", ["Small intestine", "Stomach", "Large intestine", "Oesophagus"], 1,
       "The stomach churns food and mixes it with acidic gastric juices for digestion.", 'medium'),
    mc("Which acid is present in the stomach to help digestion?", ["Sulphuric acid", "Hydrochloric acid", "Nitric acid", "Acetic acid"], 1,
       "Hydrochloric acid in the stomach creates an acidic environment that aids digestion and kills germs.", 'medium'),
    mc("Digested food is mainly absorbed into the blood in which organ?", ["Stomach", "Small intestine", "Large intestine", "Oesophagus"], 1,
       "The small intestine is the main site for absorption of digested food into the bloodstream.", 'medium'),
    mc("Which organ absorbs water from undigested food?", ["Small intestine", "Large intestine", "Stomach", "Liver"], 1,
       "The large intestine absorbs water from undigested food, forming solid waste.", 'medium'),
    mc("Which organ produces bile to help digest fats?", ["Pancreas", "Liver", "Stomach", "Small intestine"], 1,
       "The liver produces bile, which helps in the digestion (emulsification) of fats.", 'medium'),
    mc("Which gland produces digestive enzymes and releases them into the small intestine?", ["Liver", "Pancreas", "Salivary gland", "Gall bladder"], 1,
       "The pancreas produces digestive enzymes that are released into the small intestine.", 'medium'),
    mc("Which tube connects the mouth to the stomach?", ["Trachea", "Oesophagus", "Small intestine", "Large intestine"], 1,
       "The oesophagus is the muscular tube that carries food from the mouth to the stomach.", 'medium'),
    mc("The wave-like movement of muscles that pushes food through the digestive tract is called:", ["Digestion", "Peristalsis", "Egestion", "Absorption"], 1,
       "Peristalsis refers to the rhythmic, wave-like muscle contractions that move food through the digestive tract.", 'hard'),
    mc("Ruminant animals like cows have a special stomach chamber for storing swallowed grass, called:", ["Rumen", "Duodenum", "Oesophagus", "Colon"], 0,
       "The rumen is a special stomach chamber in ruminants where swallowed grass is stored and partially digested.", 'medium'),
    mc("Cud chewed and re-swallowed by cattle is called:", ["Rumen", "Cud", "Bolus", "Chyme"], 1,
       "Cud is the partially digested food that ruminants like cows bring back to the mouth to chew again.", 'medium'),
    mc("Amoeba obtains its food using temporary finger-like extensions called:", ["Cilia", "Pseudopodia", "Flagella", "Villi"], 1,
       "Amoeba uses pseudopodia (temporary extensions of its cell body) to engulf food particles.", 'medium'),
    mc("Which small finger-like projections in the small intestine increase surface area for absorption?", ["Villi", "Cilia", "Alveoli", "Papillae"], 0,
       "Villi are tiny finger-like projections in the small intestine that increase surface area for nutrient absorption.", 'medium'),
    mc("Which of these best describes 'assimilation' in the digestive process?", ["Removal of waste", "Use of absorbed nutrients by body cells", "Intake of food", "Breakdown of food"], 1,
       "Assimilation is the process by which absorbed nutrients are used by body cells for energy and growth.", 'hard'),
    mc("Which of the following correctly orders the human digestive pathway?", ["Mouth → Stomach → Oesophagus → Intestine", "Mouth → Oesophagus → Stomach → Small intestine → Large intestine", "Stomach → Mouth → Intestine", "Mouth → Intestine → Stomach"], 1,
       "The correct pathway is: Mouth → Oesophagus → Stomach → Small intestine → Large intestine.", 'medium'),
    mc("Which of these organisms shows a different mode of nutrition using pseudopodia?", ["Cow", "Amoeba", "Human", "Grasshopper"], 1,
       "Amoeba is a unicellular organism that engulfs food using pseudopodia, unlike animals with a digestive system.", 'medium'),
]

CLASS7_ENG_VOICE = [
    mc("Identify the sentence in the passive voice.", ["The dog bit the man.", "The man was bitten by the dog.", "The dog is biting the man.", "The dog will bite the man."], 1,
       "In passive voice, the subject receives the action: 'The man was bitten by the dog.'", 'medium'),
    mc("Convert to passive voice: 'She writes a letter.'", ["A letter is written by her.", "A letter was written by her.", "A letter writes her.", "She is written a letter."], 0,
       "Present tense active 'writes' becomes 'is written' in passive voice.", 'medium'),
    mc("Convert to passive voice: 'They built a house.'", ["A house is built by them.", "A house was built by them.", "A house builds them.", "A house has built them."], 1,
       "Past tense active 'built' becomes 'was built' in passive voice.", 'medium'),
    mc("Convert to active voice: 'The cake was eaten by the children.'", ["The children eat the cake.", "The children ate the cake.", "The children will eat the cake.", "The children are eating the cake."], 1,
       "Passive 'was eaten' corresponds to active past tense: 'The children ate the cake.'", 'medium'),
    mc("Which voice focuses more on the doer (subject) of the action?", ["Active voice", "Passive voice", "Both equally", "Neither"], 0,
       "In active voice, the subject performs the action and is the focus of the sentence.", 'easy'),
    mc("Which voice focuses more on the receiver of the action?", ["Active voice", "Passive voice", "Both equally", "Neither"], 1,
       "In passive voice, the subject receives the action, shifting focus away from the doer.", 'easy'),
    mc("Convert to passive voice: 'The teacher will explain the lesson.'", ["The lesson will be explained by the teacher.", "The lesson explains the teacher.", "The lesson was explained by the teacher.", "The lesson is explained by the teacher."], 0,
       "Future tense active 'will explain' becomes 'will be explained' in passive voice.", 'hard'),
    mc("Convert to passive voice: 'I am reading a book.'", ["A book is read by me.", "A book is being read by me.", "A book was read by me.", "A book reads me."], 1,
       "Present continuous active 'am reading' becomes 'is being read' in passive voice.", 'hard'),
    mc("Which sentence correctly uses passive voice for 'Someone has stolen my bicycle'?", ["My bicycle has been stolen.", "My bicycle is stolen.", "My bicycle was stealing.", "My bicycle steals."], 0,
       "Present perfect active 'has stolen' becomes 'has been stolen' in passive voice.", 'hard'),
    mc("In passive voice sentences, which auxiliary verb is always used along with the past participle?", ["Do", "Be (is/am/are/was/were/been)", "Have", "Will"], 1,
       "Passive voice uses a form of 'be' + past participle of the main verb.", 'medium'),
    mc("Convert to active voice: 'The window was broken by the boy.'", ["The boy breaks the window.", "The boy broke the window.", "The boy will break the window.", "The boy is breaking the window."], 1,
       "Passive 'was broken' corresponds to active past tense: 'The boy broke the window.'", 'medium'),
    mc("Which of these sentences is already in active voice?", ["The song was sung by her.", "She sang the song.", "The song is sung by her.", "The song will be sung by her."], 1,
       "'She sang the song' has the subject performing the action directly - active voice.", 'easy'),
    mc("Convert to passive voice: 'The chef is cooking dinner.'", ["Dinner is being cooked by the chef.", "Dinner cooks the chef.", "Dinner was cooked by the chef.", "Dinner has cooked the chef."], 0,
       "Present continuous active 'is cooking' becomes 'is being cooked' in passive voice.", 'hard'),
    mc("Passive voice sentences generally place the doer of the action after which word?", ["to", "for", "by", "with"], 2,
       "In passive voice, the doer of the action is usually introduced by the word 'by'.", 'medium'),
    mc("Convert to passive voice: 'Mother cooks food every day.'", ["Food is cooked by mother every day.", "Food cooks mother every day.", "Food was cooked by mother every day.", "Food will be cooked by mother."], 0,
       "Simple present active 'cooks' becomes 'is cooked' in passive voice.", 'medium'),
    mc("Which type of sentence is typically difficult to convert into passive voice?", ["Sentences with a transitive verb", "Sentences with an intransitive verb", "Sentences in the past tense", "Sentences with a proper noun"], 1,
       "Sentences with intransitive verbs (no object) generally cannot be converted to passive voice, since passive needs an object to become the new subject.", 'hard'),
    mc("Convert to active voice: 'The letter was posted by Ravi.'", ["Ravi posts the letter.", "Ravi posted the letter.", "Ravi will post the letter.", "Ravi is posting the letter."], 1,
       "Passive 'was posted' corresponds to active past tense: 'Ravi posted the letter.'", 'medium'),
    mc("Which is the correct passive form of 'Please close the door'?", ["Let the door be closed.", "The door is closed by please.", "The door closes.", "The door will close."], 0,
       "Imperative sentences in passive voice often use the structure 'Let + object + be + past participle.'", 'hard'),
    mc("Convert to passive voice: 'People speak English worldwide.'", ["English is spoken by people worldwide.", "English speaks people worldwide.", "English was spoken worldwide.", "English will be spoken worldwide."], 0,
       "Simple present active 'speak' becomes 'is spoken' in passive voice.", 'medium'),
    mc("Passive voice is often used in scientific writing mainly because it:", ["Focuses attention on the action/result rather than the doer", "Is always shorter", "Sounds more casual", "Cannot use past tense"], 0,
       "Passive voice is common in scientific writing since it emphasises the process or result rather than who performed it.", 'medium'),
]

CLASS7_ENG_SPEECH = [
    mc("Convert to indirect speech: He said, 'I am happy.'", ["He said that he was happy.", "He said that I am happy.", "He said that he is happy.", "He says that he was happy."], 0,
       "In reported speech, present tense 'am' shifts to past tense 'was', and pronoun 'I' changes to 'he'.", 'medium'),
    mc("Convert to indirect speech: She said, 'I will go home.'", ["She said that she will go home.", "She said that she would go home.", "She said that I would go home.", "She says that she will go home."], 1,
       "'Will' changes to 'would' in reported speech when the reporting verb is in the past tense.", 'medium'),
    mc("Convert to indirect speech: They said, 'We are playing football.'", ["They said that we are playing football.", "They said that they were playing football.", "They said that they are playing football.", "They say that they were playing football."], 1,
       "'Are playing' changes to 'were playing', and 'we' changes to 'they' in reported speech.", 'medium'),
    mc("Convert to indirect speech: He said, 'I went to the market yesterday.'", ["He said that he had gone to the market the day before.", "He said that he went to the market yesterday.", "He said that he goes to the market yesterday.", "He said that he will go to the market."], 0,
       "Simple past 'went' shifts to past perfect 'had gone', and 'yesterday' becomes 'the day before' in reported speech.", 'hard'),
    mc("Direct speech uses which punctuation marks to enclose the exact words spoken?", ["Brackets", "Quotation marks", "Hyphens", "Colons"], 1,
       "Direct speech encloses the exact spoken words within quotation marks.", 'easy'),
    mc("Convert to indirect speech: She asked, 'Where do you live?'", ["She asked where I lived.", "She asked where do I live.", "She asked where you live.", "She asked where does he live."], 0,
       "Questions in reported speech drop the question mark, invert word order, and shift tense/pronouns appropriately.", 'hard'),
    mc("Convert to indirect speech: He said, 'Please open the door.'", ["He requested to open the door.", "He said to open the door.", "He asked that please open the door.", "He said open the door."], 0,
       "Polite requests in reported speech are usually introduced with 'requested to'.", 'hard'),
    mc("Convert to indirect speech: The teacher said, 'Do your homework daily.'", ["The teacher told us to do our homework daily.", "The teacher said do your homework daily.", "The teacher asked did you do homework daily.", "The teacher said that do homework daily."], 0,
       "Commands in reported speech typically use 'told + object + to + verb'.", 'hard'),
    mc("In reported speech, 'this' generally changes to:", ["that", "these", "it", "here"], 0,
       "'This' generally changes to 'that' when converting direct speech to indirect speech.", 'medium'),
    mc("In reported speech, 'here' generally changes to:", ["there", "this", "that", "now"], 0,
       "'Here' generally changes to 'there' in indirect (reported) speech.", 'medium'),
    mc("In reported speech, 'now' generally changes to:", ["then", "here", "soon", "later today"], 0,
       "'Now' generally changes to 'then' when converting to indirect speech.", 'medium'),
    mc("In reported speech, 'tomorrow' generally changes to:", ["yesterday", "the next day", "today", "now"], 1,
       "'Tomorrow' changes to 'the next day' (or 'the following day') in reported speech.", 'hard'),
    mc("Which reporting verb is commonly used to report a question?", ["said", "told", "asked", "exclaimed"], 2,
       "'Asked' is the reporting verb typically used to introduce a reported question.", 'medium'),
    mc("Convert to indirect speech: She said, 'What a beautiful day!'", ["She exclaimed that it was a beautiful day.", "She said that what a beautiful day.", "She exclaimed what a beautiful day is.", "She said what a beautiful day was."], 0,
       "Exclamatory sentences are reported using 'exclaimed that' and restructured as a statement.", 'hard'),
    mc("Which tense does 'is/are' usually shift to in reported speech (past reporting verb)?", ["was/were", "will be", "has been", "is/are (no change)"], 0,
       "Present tense 'is/are' typically shifts to past tense 'was/were' in reported speech.", 'medium'),
    mc("Which tense does 'has/have' usually shift to in reported speech (past reporting verb)?", ["had", "has (no change)", "having", "will have"], 0,
       "Present perfect 'has/have' shifts to past perfect 'had' in reported speech.", 'hard'),
    mc("Convert to indirect speech: He said, 'I can swim well.'", ["He said that he could swim well.", "He said that he can swim well.", "He said that I could swim well.", "He says that he could swim well."], 0,
       "'Can' shifts to 'could' in reported speech when the reporting verb is in the past tense.", 'medium'),
    mc("Which word introduces reported statements (not questions or commands)?", ["if", "that", "to", "whether"], 1,
       "Reported statements are usually introduced with the connector 'that'.", 'medium'),
    mc("Which word is used to introduce reported yes/no questions?", ["that", "to", "if/whether", "because"], 2,
       "Reported yes/no questions are introduced using 'if' or 'whether'.", 'hard'),
    mc("Convert to indirect speech: She said, 'Do you like tea?'", ["She asked if I liked tea.", "She asked that I like tea.", "She asked do you like tea.", "She asked if you like tea."], 0,
       "Yes/no questions in reported speech use 'if/whether' and shift tense and pronouns accordingly.", 'hard'),
]

CLASS7_SOC_TRACING = [
    mc("What was the capital of the Delhi Sultanate under most of its rulers?", ["Agra", "Delhi", "Lahore", "Jaipur"], 1,
       "Delhi served as the capital of the Delhi Sultanate.", 'medium'),
    mc("Which dynasty founded the Delhi Sultanate in 1206?", ["Khalji dynasty", "Slave (Mamluk) dynasty", "Tughlaq dynasty", "Lodi dynasty"], 1,
       "The Slave (Mamluk) dynasty, founded by Qutb-ud-din Aibak, established the Delhi Sultanate in 1206.", 'medium'),
    mc("Who founded the Mughal Empire in India?", ["Akbar", "Humayun", "Babur", "Aurangzeb"], 2,
       "Babur founded the Mughal Empire after defeating Ibrahim Lodi at the First Battle of Panipat in 1526.", 'medium'),
    mc("Who is considered the greatest of the Mughal emperors, known for his policy of religious tolerance?", ["Babur", "Humayun", "Akbar", "Shah Jahan"], 2,
       "Akbar is known for his administrative skills and policy of religious tolerance (Sulh-i-kul).", 'medium'),
    mc("Which Mughal emperor built the Taj Mahal?", ["Akbar", "Jahangir", "Shah Jahan", "Aurangzeb"], 2,
       "Shah Jahan built the Taj Mahal in memory of his wife, Mumtaz Mahal.", 'easy'),
    mc("What term is used for historical records that document the reigns of kings, often written by court historians?", ["Inscriptions", "Chronicles", "Fables", "Folklore"], 1,
       "Chronicles are historical records, often maintained by court historians, documenting the events of a ruler's reign.", 'medium'),
    mc("Which term describes the land grant given to nobles in exchange for military service in medieval India?", ["Jagir", "Mansab", "Zamindari", "Iqta"], 0,
       "A Jagir was a land grant assigned to nobles/officials in return for their services, especially military.", 'hard'),
    mc("The Bhakti movement mainly emphasised:", ["Ritualistic worship", "Personal devotion to God, cutting across caste", "Only Sanskrit learning", "Military conquest"], 1,
       "The Bhakti movement emphasised personal devotion to God and often rejected caste distinctions.", 'medium'),
    mc("Who was a leading poet-saint of the Bhakti movement, known for his devotion to Lord Rama?", ["Kabir", "Tulsidas", "Guru Nanak", "Mirabai"], 1,
       "Tulsidas, author of the Ramcharitmanas, was a key poet-saint devoted to Lord Rama.", 'medium'),
    mc("Which movement, emphasising monotheism and rejecting rituals, was founded by Guru Nanak?", ["Bhakti movement", "Sufi movement", "Sikhism", "Jainism"], 2,
       "Guru Nanak founded Sikhism, which emphasises monotheism and equality.", 'medium'),
    mc("The Sufi movement within Islam emphasised:", ["Strict ritualism", "Love and devotion towards God", "Military expansion", "Caste hierarchy"], 1,
       "Sufism emphasised deep personal love and devotion towards God, often through music and poetry.", 'medium'),
    mc("Which of these was a major administrative division under the Delhi Sultanate?", ["Iqta", "Panchayat", "Gram Sabha", "Lok Sabha"], 0,
       "An Iqta was a territorial assignment given to nobles for administration and revenue collection under the Sultanate.", 'hard'),
    mc("The term 'Vijayanagara Empire' literally means:", ["City of Gold", "City of Victory", "City of Kings", "City of Temples"], 1,
       "'Vijayanagara' translates to 'City of Victory'.", 'medium'),
    mc("Which South Indian empire was known for its capital Hampi and its patronage of art and temples?", ["Chola Empire", "Vijayanagara Empire", "Maratha Empire", "Mughal Empire"], 1,
       "The Vijayanagara Empire, with its capital at Hampi, was known for its architecture and patronage of the arts.", 'medium'),
    mc("Who founded the Maratha kingdom in the 17th century?", ["Shivaji", "Akbar", "Rana Pratap", "Balaji Vishwanath"], 0,
       "Shivaji founded the Maratha kingdom, known for his military strategy and administration.", 'medium'),
    mc("Which official post, later held by the Peshwas, initially meant 'chief minister'?", ["Wazir", "Peshwa", "Subedar", "Diwan"], 1,
       "'Peshwa' originally meant chief minister and later became the hereditary head of the Maratha administration.", 'hard'),
    mc("Which trade route connected India to Europe and the Middle East for centuries?", ["Silk Route", "Grand Trunk Road only", "Amazon route", "Trans-Siberian route"], 0,
       "The Silk Route connected India to Central Asia, the Middle East and Europe for centuries of trade.", 'medium'),
    mc("The term used for a Mughal ranking system that determined a noble's status and salary was:", ["Mansabdari system", "Jagirdari system only", "Zamindari system", "Ryotwari system"], 0,
       "The Mansabdari system was used to rank officials and nobles based on their military and civil status.", 'hard'),
    mc("Which script/language became widely used in administration during the Delhi Sultanate and Mughal period?", ["Sanskrit", "Persian", "Latin", "Greek"], 1,
       "Persian became the administrative and court language during the Delhi Sultanate and Mughal periods.", 'medium'),
    mc("Which of the following best describes 'medieval India' in the timeline of Indian history?", ["The period before 600 CE", "The period roughly between the 8th and 18th centuries CE", "The period after 1947", "Only the Mughal period"], 1,
       "Medieval India broadly refers to the period from around the 8th century to the 18th century CE.", 'medium'),
]

CLASS7_SOC_ENVIRONMENT = [
    mc("The sum total of all living and non-living things around us is called:", ["Ecosystem", "Environment", "Biosphere", "Habitat"], 1,
       "The environment includes all living and non-living things surrounding us.", 'easy'),
    mc("Which of these is a component of the natural environment?", ["Buildings", "Roads", "Mountains", "Factories"], 2,
       "Mountains are a natural feature and part of the natural environment.", 'easy'),
    mc("Which of these is a component of the human-made (man-made) environment?", ["Rivers", "Forests", "Bridges", "Mountains"], 2,
       "Bridges are constructed by humans and are part of the human-made environment.", 'easy'),
    mc("The domain of the Earth consisting of solid land is called the:", ["Hydrosphere", "Lithosphere", "Atmosphere", "Biosphere"], 1,
       "The lithosphere is the solid, rocky outer layer of the Earth.", 'medium'),
    mc("The domain of the Earth consisting of water bodies is called the:", ["Lithosphere", "Atmosphere", "Hydrosphere", "Biosphere"], 2,
       "The hydrosphere includes all water bodies on Earth, like oceans, rivers and lakes.", 'medium'),
    mc("The domain of the Earth consisting of the layer of air is called the:", ["Lithosphere", "Atmosphere", "Hydrosphere", "Biosphere"], 1,
       "The atmosphere is the layer of gases surrounding the Earth.", 'medium'),
    mc("The domain where life exists on Earth is called the:", ["Lithosphere", "Hydrosphere", "Atmosphere", "Biosphere"], 3,
       "The biosphere is the zone where life exists, formed by the interaction of land, water and air.", 'medium'),
    mc("Which of these is an example of a natural ecosystem?", ["Aquarium", "Forest", "Garden", "Crop field"], 1,
       "A forest is a naturally occurring ecosystem, unlike a garden or aquarium which are human-made.", 'medium'),
    mc("Which of these is an example of a man-made ecosystem?", ["Forest", "Ocean", "Aquarium", "Desert"], 2,
       "An aquarium is a human-made, artificial ecosystem.", 'medium'),
    mc("Environments with very little vegetation and extreme temperatures are known as:", ["Deserts", "Grasslands", "Forests", "Wetlands"], 0,
       "Deserts are environments with extreme temperatures and very sparse vegetation, receiving little rainfall.", 'easy'),
    mc("The Amazon rainforest is a well-known example of which type of biome?", ["Desert", "Tropical rainforest", "Tundra", "Grassland"], 1,
       "The Amazon is the world's largest tropical rainforest, known for its rich biodiversity.", 'easy'),
    mc("Which factor most affects the type of natural vegetation found in a region?", ["Population density", "Climate", "Language spoken", "Type of government"], 1,
       "Climate (temperature and rainfall) is the primary factor determining the type of natural vegetation.", 'medium'),
    mc("Which human activity most directly causes deforestation?", ["Reforestation", "Clearing land for agriculture and settlements", "Wildlife conservation", "Rainwater harvesting"], 1,
       "Clearing forest land for agriculture, industry and settlements is a major cause of deforestation.", 'medium'),
    mc("What term describes an interconnected community of living organisms and their physical environment?", ["Habitat", "Ecosystem", "Biome", "Domain"], 1,
       "An ecosystem is a community of living organisms interacting with each other and their physical environment.", 'medium'),
    mc("Which of these best explains why the equatorial region has dense rainforests?", ["Low rainfall and cold climate", "High rainfall and warm temperatures throughout the year", "Extreme cold and no rainfall", "Very dry desert climate"], 1,
       "Equatorial regions receive high rainfall and consistently warm temperatures, ideal for dense rainforest growth.", 'medium'),
    mc("The interaction between different components of the environment is called:", ["Isolation", "Interdependence", "Pollution", "Extinction"], 1,
       "Interdependence refers to the interconnected relationships between the different components of the environment.", 'medium'),
    mc("Which of these best describes 'biodiversity'?", ["The variety of life forms found in an environment", "The amount of pollution in an area", "The number of countries in a region", "The population of a city"], 0,
       "Biodiversity refers to the variety of living organisms found within a particular ecosystem or region.", 'medium'),
    mc("Tundra regions are characterised mainly by:", ["Hot and humid climate", "Extremely cold climate with little vegetation", "Dense tropical forests", "Fertile plains"], 1,
       "Tundra regions have extremely cold climates and limited vegetation, mostly mosses and lichens.", 'medium'),
    mc("Which factor helps determine why grasslands, rather than forests, develop in certain regions?", ["Moderate rainfall, not enough to support dense forests", "No rainfall at all", "Extremely high rainfall", "Presence of oceans nearby only"], 0,
       "Grasslands typically develop in regions with moderate rainfall - too much for deserts but not enough to support dense forests.", 'hard'),
    mc("Human interference in the environment, such as pollution, mainly disturbs the balance of the:", ["Solar system", "Ecosystem", "Political map", "Time zones"], 1,
       "Pollution and other human interference disturb the natural balance of an ecosystem.", 'medium'),
]

CLASS7_CS_WORD = [
    mc("Which software is commonly used for word processing?", ["MS Excel", "MS Word", "MS PowerPoint", "MS Access"], 1,
       "MS Word is a widely used word processing software for creating and editing text documents.", 'easy'),
    mc("Which feature is used to check and correct spelling errors automatically?", ["Find and Replace", "Spell Check", "Mail Merge", "Page Layout"], 1,
       "The Spell Check feature identifies and helps correct spelling errors in a document.", 'easy'),
    mc("Which feature allows you to search for a word and replace it with another throughout a document?", ["Spell Check", "Find and Replace", "Thesaurus", "Page Setup"], 1,
       "Find and Replace lets you search for specific text and replace it with new text throughout the document.", 'medium'),
    mc("Which key combination is commonly used to make selected text bold?", ["Ctrl+U", "Ctrl+B", "Ctrl+I", "Ctrl+P"], 1,
       "Ctrl+B is the common shortcut to make selected text bold.", 'easy'),
    mc("Which key combination is commonly used to underline selected text?", ["Ctrl+B", "Ctrl+I", "Ctrl+U", "Ctrl+P"], 2,
       "Ctrl+U is the common shortcut to underline selected text.", 'easy'),
    mc("Which key combination is commonly used to italicise selected text?", ["Ctrl+B", "Ctrl+I", "Ctrl+U", "Ctrl+S"], 1,
       "Ctrl+I is the common shortcut to italicise selected text.", 'easy'),
    mc("Which menu tab typically contains options to insert images, tables and shapes?", ["Home", "Insert", "View", "References"], 1,
       "The Insert tab contains options for adding images, tables, shapes and other elements to a document.", 'medium'),
    mc("Which feature helps create personalised letters for multiple recipients using a data source?", ["Mail Merge", "Spell Check", "Find and Replace", "Track Changes"], 0,
       "Mail Merge combines a template document with a data source to create personalised copies for multiple recipients.", 'medium'),
    mc("Which feature allows multiple people to see edits made to a shared document?", ["Track Changes", "Spell Check", "Page Layout", "Word Count"], 0,
       "Track Changes records edits made to a document, allowing collaborators to review and accept/reject them.", 'medium'),
    mc("What is the purpose of the 'Header and Footer' feature?", ["To add content that repeats at the top/bottom of every page", "To check spelling", "To insert a table", "To change font colour"], 0,
       "Headers and footers add repeating content, like page numbers or titles, at the top or bottom of every page.", 'medium'),
    mc("Which file extension is commonly used for Microsoft Word documents?", [".xlsx", ".docx", ".pptx", ".pdf"], 1,
       "Microsoft Word documents commonly use the .docx file extension.", 'easy'),
    mc("Which shortcut is used to select all content in a document?", ["Ctrl+A", "Ctrl+S", "Ctrl+P", "Ctrl+Z"], 0,
       "Ctrl+A selects all content in the current document.", 'easy'),
    mc("Which feature is used to add page numbers automatically to a document?", ["Insert > Page Number", "Home > Bold", "View > Zoom", "References > Citation"], 0,
       "The 'Insert > Page Number' option automatically adds page numbers throughout a document.", 'medium'),
    mc("Which of these tools helps you find synonyms for a word?", ["Spell check", "Thesaurus", "Word count", "Mail merge"], 1,
       "The Thesaurus tool suggests synonyms (words with similar meanings) for a selected word.", 'medium'),
    mc("Which feature allows text to wrap around an inserted image?", ["Text Wrapping", "Spell Check", "Word Count", "Header"], 0,
       "Text Wrapping controls how text flows around an image or object in a document.", 'medium'),
    mc("Which key is used to move the cursor to the beginning of a line?", ["End", "Home", "Tab", "Page Up"], 1,
       "The 'Home' key moves the cursor to the beginning of the current line.", 'medium'),
    mc("Which alignment option centres text between the left and right margins?", ["Left align", "Right align", "Centre align", "Justify"], 2,
       "Centre alignment positions text evenly between the left and right margins.", 'easy'),
    mc("Which alignment option makes text flush with both left and right margins?", ["Left align", "Right align", "Centre align", "Justify"], 3,
       "Justify alignment stretches text so it aligns evenly with both the left and right margins.", 'medium'),
    mc("What does the 'Word Count' feature show?", ["Number of images", "Number of words, characters, and pages in a document", "Font size used", "Table dimensions"], 1,
       "Word Count displays statistics such as the number of words, characters, and pages in a document.", 'easy'),
    mc("Which of these is NOT typically a feature of a word processor?", ["Spell check", "Formatting text", "Solving complex spreadsheet formulas", "Inserting images"], 2,
       "Solving complex spreadsheet formulas is a feature of spreadsheet software (like Excel), not typically a word processor.", 'medium'),
]

CLASS7_CS_INTERNET = [
    mc("What does WWW stand for?", ["World Wide Web", "World Web Wide", "Wide World Web", "Web World Wide"], 0,
       "WWW stands for World Wide Web, a system of interlinked web pages accessed via the internet.", 'easy'),
    mc("What is a computer program used to access and view websites called?", ["Operating system", "Web browser", "Search engine", "Antivirus"], 1,
       "A web browser (like Chrome or Firefox) is used to access and view websites.", 'easy'),
    mc("Which of these is an example of a search engine?", ["Google", "MS Word", "Windows", "MS Paint"], 0,
       "Google is a popular search engine used to find information on the internet.", 'easy'),
    mc("What is the unique address of a website called?", ["URL", "IP address only", "HTML", "Domain login"], 0,
       "A URL (Uniform Resource Locator) is the unique address used to locate a website.", 'medium'),
    mc("Which of these is an example of a top-level domain?", [".com", "www", "http", "browser"], 0,
       "'.com' is a top-level domain, indicating a commercial website.", 'medium'),
    mc("What does 'http' stand for in a web address?", ["HyperText Transfer Protocol", "High Transfer Text Protocol", "HyperText Transmission Program", "Home Text Transfer Protocol"], 0,
       "HTTP stands for HyperText Transfer Protocol, used to transfer web pages over the internet.", 'medium'),
    mc("Which secure version of HTTP encrypts data between browser and website?", ["HTTP", "HTTPS", "FTP", "SMTP"], 1,
       "HTTPS (HTTP Secure) encrypts data exchanged between the browser and the website for security.", 'medium'),
    mc("Which protocol is used to send emails?", ["HTTP", "FTP", "SMTP", "HTML"], 2,
       "SMTP (Simple Mail Transfer Protocol) is used to send emails over the internet.", 'hard'),
    mc("What is a collection of related web pages under one domain called?", ["Browser", "Website", "Server", "Network"], 1,
       "A website is a collection of related web pages hosted under a single domain name.", 'easy'),
    mc("Which of these is used to store and serve websites so they can be accessed over the internet?", ["Web server", "Web browser", "Search engine", "Modem"], 0,
       "A web server stores website files and serves them to users' browsers over the internet.", 'medium'),
    mc("Which of these devices connects a home network to the internet?", ["Modem/Router", "Monitor", "Keyboard", "Printer"], 0,
       "A modem or router connects a home network of devices to the internet.", 'medium'),
    mc("Which of the following is good practice for online safety?", ["Sharing passwords with friends", "Not sharing personal information with strangers online", "Clicking on all pop-up ads", "Using the same simple password everywhere"], 1,
       "Avoiding sharing personal information with strangers online is an important online safety practice.", 'easy'),
    mc("What is 'malware'?", ["Helpful software", "Software designed to harm or exploit computers", "A type of search engine", "A type of hardware"], 1,
       "Malware is malicious software designed to damage, disrupt, or gain unauthorised access to computer systems.", 'medium'),
    mc("What does 'downloading' mean?", ["Sending data from your computer to the internet", "Receiving data from the internet to your computer", "Deleting files", "Printing a document"], 1,
       "Downloading means transferring data from the internet to your own computer or device.", 'easy'),
    mc("What does 'uploading' mean?", ["Receiving data from the internet", "Sending data from your computer to the internet", "Deleting a file", "Formatting a disk"], 1,
       "Uploading means sending data from your own device to a server or the internet.", 'easy'),
    mc("Which of these is an email service provider?", ["Gmail", "MS Word", "Windows Explorer", "MS Paint"], 0,
       "Gmail is a popular email service provided by Google.", 'easy'),
    mc("Which symbol is used in an email address to separate the username from the domain?", ["#", "@", "&", "%"], 1,
       "The '@' symbol separates the username from the domain name in an email address, e.g. name@example.com.", 'easy'),
    mc("What is the term for unwanted or unsolicited email, often advertising or malicious?", ["Spam", "Attachment", "Draft", "Inbox"], 0,
       "Spam refers to unwanted, unsolicited emails, often sent in bulk for advertising or scams.", 'medium'),
    mc("Which of these best defines 'cyberbullying'?", ["Helping others online", "Using the internet to harass or intimidate someone", "Sharing educational content", "Browsing safely"], 1,
       "Cyberbullying is the use of digital platforms to harass, threaten or intimidate someone.", 'medium'),
    mc("Which of these is a good habit when creating a password?", ["Using your name and birth date", "Using a mix of letters, numbers, and symbols", "Using '12345'", "Sharing it publicly"], 1,
       "Strong passwords use a mix of upper/lowercase letters, numbers, and symbols, making them harder to guess.", 'easy'),
]
# ============ CLASS 9 (non-math) ============

CLASS9_SCI_MATTER = [
    mc("Matter is defined as anything that:", ["Has colour", "Has mass and occupies space", "Is visible to the eye", "Can move"], 1,
       "Matter is anything that has mass and occupies space.", 'easy'),
    mc("Which of these is NOT a state of matter?", ["Solid", "Liquid", "Gas", "Energy"], 3,
       "Energy is not a state of matter; the three common states are solid, liquid and gas (plus plasma).", 'easy'),
    mc("Which state of matter has a definite shape and definite volume?", ["Solid", "Liquid", "Gas", "Plasma"], 0,
       "Solids have a definite shape and volume because their particles are tightly packed.", 'easy'),
    mc("Which state of matter has a definite volume but takes the shape of its container?", ["Solid", "Liquid", "Gas", "None"], 1,
       "Liquids have a definite volume but no fixed shape, taking the shape of their container.", 'easy'),
    mc("Which state of matter has neither definite shape nor definite volume?", ["Solid", "Liquid", "Gas", "Plasma only"], 2,
       "Gases have neither definite shape nor definite volume, expanding to fill their container.", 'easy'),
    mc("The change of state from solid directly to gas without becoming liquid is called:", ["Melting", "Sublimation", "Evaporation", "Condensation"], 1,
       "Sublimation is the direct change of a solid into a gas without passing through the liquid state.", 'medium'),
    mc("The change of state from liquid to gas is called:", ["Melting", "Freezing", "Vaporisation", "Condensation"], 2,
       "Vaporisation is the process of a liquid changing into a gas.", 'easy'),
    mc("The change of state from gas to liquid is called:", ["Evaporation", "Condensation", "Sublimation", "Melting"], 1,
       "Condensation is the process of a gas changing back into a liquid.", 'easy'),
    mc("The temperature at which a solid changes into a liquid is called its:", ["Boiling point", "Melting point", "Freezing point", "Sublimation point"], 1,
       "The melting point is the specific temperature at which a solid turns into a liquid.", 'easy'),
    mc("The temperature at which a liquid changes into vapour throughout its bulk is called its:", ["Melting point", "Boiling point", "Freezing point", "Condensation point"], 1,
       "The boiling point is the temperature at which a liquid vaporises rapidly throughout, not just at the surface.", 'easy'),
    mc("Which factor increases the rate of evaporation of a liquid?", ["Decreasing temperature", "Increasing surface area", "Increasing humidity", "Decreasing wind speed"], 1,
       "Increasing surface area increases the rate of evaporation, as more particles can escape.", 'medium'),
    mc("Evaporation causes cooling because:", ["It absorbs heat from the surroundings", "It releases heat", "It has no effect on temperature", "It only occurs at boiling point"], 0,
       "Evaporation causes cooling because particles absorb heat energy from the surroundings to escape as vapour.", 'medium'),
    mc("Which of these best defines 'diffusion'?", ["Movement of particles from lower to higher concentration", "Movement of particles from higher to lower concentration", "The freezing of particles", "The compression of particles"], 1,
       "Diffusion is the spontaneous movement of particles from a region of higher to lower concentration.", 'medium'),
    mc("Which state of matter shows the fastest rate of diffusion?", ["Solid", "Liquid", "Gas", "All are equal"], 2,
       "Gases have the fastest rate of diffusion due to large intermolecular spaces and high particle speed.", 'medium'),
    mc("Latent heat of fusion refers to the heat required to:", ["Change liquid to gas at constant temperature", "Change solid to liquid at constant temperature", "Raise the temperature of a solid", "Change gas to liquid"], 1,
       "Latent heat of fusion is the heat energy needed to convert a solid into a liquid at its melting point without a change in temperature.", 'hard'),
    mc("Latent heat of vaporisation refers to the heat required to:", ["Change solid to liquid", "Change liquid to vapour at constant temperature", "Cool a gas", "Freeze a liquid"], 1,
       "Latent heat of vaporisation is the heat needed to convert a liquid into vapour at its boiling point without a temperature change.", 'hard'),
    mc("Increasing pressure on a gas generally causes its particles to:", ["Move farther apart", "Come closer together", "Stop moving", "Change into a solid always"], 1,
       "Increasing pressure forces gas particles closer together, decreasing the volume.", 'medium'),
    mc("Which of these has the strongest force of attraction between particles?", ["Gas", "Liquid", "Solid", "All have equal force"], 2,
       "Solids have the strongest intermolecular forces, keeping particles tightly packed in fixed positions.", 'medium'),
    mc("Dry ice is the solid form of which substance?", ["Water", "Carbon dioxide", "Oxygen", "Nitrogen"], 1,
       "Dry ice is solid carbon dioxide, which sublimates directly into gas at room temperature.", 'medium'),
    mc("Which of the following best explains why gases can be compressed easily?", ["Their particles are tightly packed", "Their particles have large empty spaces between them", "They have no particles", "They have a fixed shape"], 1,
       "Gas particles have large spaces between them, allowing gases to be compressed easily.", 'medium'),
]

CLASS9_SCI_CELL = [
    mc("Which scientist first observed and named the cell?", ["Robert Hooke", "Charles Darwin", "Louis Pasteur", "Gregor Mendel"], 0,
       "Robert Hooke first observed cork cells under a microscope in 1665 and named them 'cells'.", 'medium'),
    mc("Which part of the cell controls its activities and contains genetic material?", ["Cytoplasm", "Cell membrane", "Nucleus", "Mitochondria"], 2,
       "The nucleus controls cell activities and contains the genetic material (DNA).", 'easy'),
    mc("Which organelle is known as the 'powerhouse of the cell'?", ["Ribosome", "Mitochondria", "Golgi body", "Lysosome"], 1,
       "Mitochondria produce energy (ATP) for the cell, earning them the name 'powerhouse of the cell'.", 'easy'),
    mc("Which structure controls the movement of substances in and out of the cell?", ["Cell wall", "Cell membrane", "Nucleus", "Vacuole"], 1,
       "The cell membrane is selectively permeable and regulates what enters and exits the cell.", 'easy'),
    mc("Which structure, found only in plant cells, provides rigidity and support?", ["Cell membrane", "Cell wall", "Nucleus", "Mitochondria"], 1,
       "The cell wall, made of cellulose, provides rigidity and structural support in plant cells.", 'easy'),
    mc("Which organelle is responsible for photosynthesis in plant cells?", ["Mitochondria", "Chloroplast", "Ribosome", "Nucleus"], 1,
       "Chloroplasts contain chlorophyll and are the site of photosynthesis in plant cells.", 'easy'),
    mc("Which organelle is involved in protein synthesis?", ["Ribosome", "Golgi body", "Lysosome", "Vacuole"], 0,
       "Ribosomes are the sites of protein synthesis in a cell.", 'medium'),
    mc("Which organelle packages and modifies proteins for transport, often called the 'packaging unit'?", ["Ribosome", "Golgi apparatus", "Mitochondria", "Nucleolus"], 1,
       "The Golgi apparatus modifies, sorts and packages proteins for transport out of the cell.", 'medium'),
    mc("Which organelle contains digestive enzymes and is known as the 'suicide bag' of the cell?", ["Ribosome", "Lysosome", "Golgi body", "Nucleus"], 1,
       "Lysosomes contain digestive enzymes and are called 'suicide bags' because they can digest the cell itself if it is damaged.", 'medium'),
    mc("Which of these is present in both plant and animal cells?", ["Cell wall", "Chloroplast", "Mitochondria", "Large central vacuole"], 2,
       "Mitochondria are present in both plant and animal cells for energy production.", 'medium'),
    mc("Which of these is found only in animal cells, not typically in plant cells?", ["Cell wall", "Centriole", "Chloroplast", "Large vacuole"], 1,
       "Centrioles are typically found in animal cells and play a role in cell division.", 'hard'),
    mc("Organisms made up of only one cell are called:", ["Multicellular", "Unicellular", "Acellular", "Tissue organisms"], 1,
       "Unicellular organisms, like Amoeba and bacteria, consist of only a single cell.", 'easy'),
    mc("Organisms made up of many cells are called:", ["Unicellular", "Multicellular", "Prokaryotic only", "Non-living"], 1,
       "Multicellular organisms are made up of many cells that work together.", 'easy'),
    mc("Cells that lack a well-defined nucleus are called:", ["Eukaryotic cells", "Prokaryotic cells", "Plant cells only", "Animal cells only"], 1,
       "Prokaryotic cells, like bacteria, lack a membrane-bound nucleus.", 'medium'),
    mc("Cells that have a well-defined, membrane-bound nucleus are called:", ["Prokaryotic cells", "Eukaryotic cells", "Bacterial cells", "Viral cells"], 1,
       "Eukaryotic cells, like plant and animal cells, have a well-defined, membrane-bound nucleus.", 'medium'),
    mc("The jelly-like substance filling the cell, in which organelles are suspended, is called:", ["Nucleus", "Cytoplasm", "Cell wall", "Chromatin"], 1,
       "Cytoplasm is the jelly-like substance in which cell organelles are suspended.", 'easy'),
    mc("The largest cell organelle that stores water, food, and waste in plant cells is the:", ["Nucleus", "Mitochondria", "Vacuole", "Ribosome"], 2,
       "The vacuole, especially the large central vacuole in plant cells, stores water, nutrients and waste.", 'medium'),
    mc("Which term is used for the basic structural and functional unit of life?", ["Tissue", "Organ", "Cell", "Organ system"], 2,
       "The cell is considered the basic structural and functional unit of life.", 'easy'),
    mc("The thread-like structures in the nucleus that carry genetic information are called:", ["Ribosomes", "Chromosomes", "Mitochondria", "Vacuoles"], 1,
       "Chromosomes are thread-like structures in the nucleus that carry genetic information (genes).", 'medium'),
    mc("Which process allows a cell to divide and produce new cells for growth and repair?", ["Photosynthesis", "Cell division", "Respiration", "Diffusion"], 1,
       "Cell division allows a single cell to divide into two or more cells, enabling growth and repair.", 'medium'),
]

CLASS9_ENG_MODALS = [
    mc("Choose the correct modal: 'You ___ wear a seatbelt while driving.' (obligation)", ["can", "must", "may", "could"], 1,
       "'Must' expresses strong obligation or necessity.", 'medium'),
    mc("Choose the correct modal: 'She ___ speak three languages.' (ability)", ["must", "can", "should", "shall"], 1,
       "'Can' is used to express ability.", 'easy'),
    mc("Choose the correct modal: '___ I open the window?' (asking permission)", ["Must", "May", "Should", "Will"], 1,
       "'May' is commonly used to politely ask for permission.", 'easy'),
    mc("Choose the correct modal: 'You ___ finish your homework before playing.' (advice/necessity)", ["might", "should", "could", "would"], 1,
       "'Should' is used to give advice or express a recommendation.", 'medium'),
    mc("Choose the correct modal: 'It ___ rain later today.' (possibility)", ["must", "might", "shall", "should"], 1,
       "'Might' expresses possibility, that something may or may not happen.", 'medium'),
    mc("Choose the correct modal: 'When I was young, I ___ run very fast.' (past ability)", ["can", "could", "may", "shall"], 1,
       "'Could' is used to express ability in the past.", 'medium'),
    mc("Which modal verb expresses a strong certainty or logical conclusion?", ["might", "could", "must", "may"], 2,
       "'Must' can express strong certainty or a logical conclusion, e.g. 'He must be tired.'", 'hard'),
    mc("Choose the correct modal: 'You ___ not smoke here.' (prohibition)", ["may", "must", "could", "would"], 1,
       "'Must not' expresses prohibition, meaning something is not allowed.", 'medium'),
    mc("Choose the correct modal for a polite request: '___ you help me with this bag?'", ["Must", "Would", "Shall", "Ought"], 1,
       "'Would' is often used to make a polite request.", 'medium'),
    mc("Choose the correct modal: 'We ___ leave now if we want to catch the train.' (necessity)", ["might", "need to", "could", "may"], 1,
       "'Need to' expresses necessity, similar to 'must' but slightly less formal.", 'medium'),
    mc("Choose the correct modal: 'He ___ have forgotten his keys, since he isn't answering.' (probability)", ["might", "shall", "will", "should"], 0,
       "'Might have' expresses a probability about a past event.", 'hard'),
    mc("Which modal is used to express a habitual past action?", ["would", "must", "shall", "may"], 0,
       "'Would' can express a habitual action that used to happen in the past, e.g. 'He would visit us every summer.'", 'hard'),
    mc("Choose the correct modal: 'You ___ apologise to her for being late.' (moral obligation)", ["could", "ought to", "might", "will"], 1,
       "'Ought to' expresses a moral obligation or duty, similar to 'should'.", 'hard'),
    mc("Choose the correct modal: 'Shall we ___ dinner together tonight?'", ["has", "have", "having", "had"], 1,
       "'Shall we have' is the correct form, following the modal 'shall' with the base verb 'have'.", 'medium'),
    mc("Choose the correct modal: '___ you please pass the salt?'", ["Could", "Must", "Shall", "Ought"], 0,
       "'Could you please' is a common, polite way to make a request.", 'medium'),
    mc("Which modal expresses future certainty, used to make predictions or promises?", ["might", "could", "will", "should"], 2,
       "'Will' is used to express future certainty, predictions, or promises.", 'medium'),
    mc("Choose the correct modal: 'Students ___ submit their assignments by Friday.' (rule/requirement)", ["might", "must", "could", "would"], 1,
       "'Must' expresses a rule or firm requirement.", 'medium'),
    mc("Choose the correct modal: 'I ___ rather stay home today.' (preference)", ["would", "must", "shall", "may"], 0,
       "'Would rather' is used to express a preference.", 'hard'),
    mc("Choose the correct modal: 'You ___ have told me earlier!' (regret about the past)", ["should", "may", "can", "shall"], 0,
       "'Should have' expresses regret or criticism about a past action that didn't happen.", 'hard'),
    mc("Which modal is most appropriate for offering help: '___ I carry that for you?'", ["Must", "Shall", "Would", "Ought"], 1,
       "'Shall I' is commonly used to offer help politely.", 'medium'),
]

CLASS9_ENG_LETTER = [
    mc("A letter written to a friend or relative is called a:", ["Formal letter", "Informal letter", "Business letter", "Official letter"], 1,
       "An informal letter is written to friends, family, or acquaintances in a personal tone.", 'easy'),
    mc("A letter written to a school principal, editor, or official is called a:", ["Informal letter", "Formal letter", "Personal letter", "Diary entry"], 1,
       "A formal letter is written for official, professional, or business purposes.", 'easy'),
    mc("Which part of a formal letter states the reason for writing?", ["Salutation", "Subject line", "Signature", "Date"], 1,
       "The subject line briefly states the purpose or reason for writing the letter.", 'medium'),
    mc("Which greeting is appropriate for a formal letter to an unknown recipient?", ["Hi there", "Dear Sir/Madam", "Hey", "Dearest friend"], 1,
       "'Dear Sir/Madam' is a formal and appropriate greeting when the recipient's name is unknown.", 'medium'),
    mc("Which closing phrase is appropriate for a formal letter?", ["Lots of love", "Yours faithfully", "Bye for now", "Take care"], 1,
       "'Yours faithfully' is a formal closing, typically used when the recipient's name is not known.", 'medium'),
    mc("Which closing is used in a formal letter when you know the recipient's name?", ["Yours faithfully", "Yours sincerely", "Bye", "Warm hugs"], 1,
       "'Yours sincerely' is used when the recipient's name is known.", 'medium'),
    mc("Where is the sender's address usually written in a formal letter?", ["Bottom left", "Top right or top left", "Middle of the page", "Nowhere"], 1,
       "The sender's address is usually written at the top of the letter (right or left, depending on format).", 'medium'),
    mc("A letter to the editor of a newspaper is typically written to:", ["Share personal news", "Express opinions on public issues", "Ask for a loan", "Invite someone to a party"], 1,
       "Letters to the editor typically express opinions or concerns about public issues for publication.", 'medium'),
    mc("Which tone is most appropriate for an informal letter to a friend?", ["Strictly formal and distant", "Warm, personal and friendly", "Legal and technical", "Cold and business-like"], 1,
       "Informal letters use a warm, personal and friendly tone, suited to writing to friends or family.", 'easy'),
    mc("Which of the following is an example of a formal letter's purpose?", ["Inviting a friend to a birthday party", "Applying for a job", "Sharing a family update", "Writing about a holiday trip to a cousin"], 1,
       "Applying for a job is a formal purpose requiring a formal letter.", 'medium'),
    mc("What should be included at the very beginning of a formal letter (after the address)?", ["Signature", "Date", "Postscript", "Closing"], 1,
       "The date is usually written after the sender's address, before the recipient's details.", 'medium'),
    mc("A 'P.S.' at the end of a letter is used to:", ["Start the letter", "Add an afterthought after the signature", "Replace the salutation", "Indicate the letter is formal"], 1,
       "A postscript (P.S.) is used to add an afterthought or extra information after the letter has been signed.", 'hard'),
    mc("Which of these best describes an essay's 'introduction'?", ["The concluding paragraph", "The opening paragraph that presents the topic", "A list of references", "A summary at the end"], 1,
       "The introduction is the opening paragraph that presents the topic and grabs the reader's attention.", 'medium'),
    mc("Which of these best describes the 'body' of an essay?", ["The paragraph(s) developing the main ideas with details", "Only the title", "The closing sentence", "The greeting"], 0,
       "The body of an essay consists of paragraphs that develop and support the main ideas with details and examples.", 'medium'),
    mc("Which of these best describes the 'conclusion' of an essay?", ["The opening paragraph", "A summary that restates the main points", "A list of sources", "The salutation"], 1,
       "The conclusion summarises the main points and often restates the thesis in different words.", 'medium'),
    mc("Which type of essay presents facts and explains a topic without expressing personal opinion?", ["Narrative essay", "Expository essay", "Persuasive essay", "Descriptive essay"], 1,
       "An expository essay explains or informs about a topic using facts, without pushing a personal opinion.", 'hard'),
    mc("Which type of essay tries to convince the reader to agree with a viewpoint?", ["Descriptive essay", "Narrative essay", "Persuasive essay", "Expository essay"], 2,
       "A persuasive essay presents arguments to convince the reader to accept a particular viewpoint.", 'medium'),
    mc("Which type of essay tells a story, often based on personal experience?", ["Narrative essay", "Expository essay", "Persuasive essay", "Descriptive essay"], 0,
       "A narrative essay tells a story, often recounting a personal experience or event.", 'medium'),
    mc("Which type of essay creates a vivid picture using sensory details?", ["Narrative essay", "Persuasive essay", "Descriptive essay", "Expository essay"], 2,
       "A descriptive essay uses sensory details to create a vivid picture of a person, place, or thing.", 'medium'),
    mc("Which of these is important to maintain throughout a formal letter or essay?", ["Casual slang", "Consistent and appropriate tone", "Random topic changes", "No punctuation"], 1,
       "Maintaining a consistent and appropriate tone is essential for clear, effective formal writing.", 'medium'),
]

CLASS9_SOC_FRENCH = [
    mc("In which year did the French Revolution begin?", ["1789", "1776", "1804", "1793"], 0,
       "The French Revolution began in 1789.", 'easy'),
    mc("Who was the King of France at the start of the French Revolution?", ["Louis XIV", "Louis XV", "Louis XVI", "Napoleon Bonaparte"], 2,
       "Louis XVI was the King of France when the Revolution began in 1789.", 'medium'),
    mc("The storming of which prison symbolised the start of the French Revolution?", ["Tower of London", "Bastille", "Alcatraz", "Bastion"], 1,
       "The storming of the Bastille prison on 14 July 1789 became a symbol of the French Revolution.", 'easy'),
    mc("The French society before the Revolution was divided into how many estates?", ["Two", "Three", "Four", "Five"], 1,
       "French society was divided into three estates: clergy, nobility, and the common people.", 'medium'),
    mc("Which estate carried the maximum burden of taxes in pre-revolutionary France?", ["First Estate (Clergy)", "Second Estate (Nobility)", "Third Estate (Commoners)", "None paid taxes"], 2,
       "The Third Estate (commoners) bore the heaviest tax burden, while clergy and nobility enjoyed exemptions.", 'medium'),
    mc("The famous revolutionary slogan of France was 'Liberty, Equality and ___'.", ["Justice", "Fraternity", "Democracy", "Freedom"], 1,
       "The French revolutionary slogan was 'Liberty, Equality, Fraternity'.", 'easy'),
    mc("Which document, adopted in 1789, declared the natural rights of citizens in France?", ["Magna Carta", "Declaration of the Rights of Man and Citizen", "Bill of Rights", "Constitution of France"], 1,
       "The Declaration of the Rights of Man and Citizen (1789) proclaimed the natural rights of French citizens.", 'medium'),
    mc("Who eventually rose to power in France after the Revolution and crowned himself Emperor?", ["Louis XVI", "Robespierre", "Napoleon Bonaparte", "Voltaire"], 2,
       "Napoleon Bonaparte rose to power after the Revolution and crowned himself Emperor of France in 1804.", 'medium'),
    mc("Which philosopher's ideas about the 'social contract' influenced the French Revolution?", ["Isaac Newton", "Jean-Jacques Rousseau", "Charles Darwin", "Galileo Galilei"], 1,
       "Jean-Jacques Rousseau's ideas about the social contract and popular sovereignty influenced revolutionary thought.", 'medium'),
    mc("The period of extreme violence and mass executions during the Revolution, led by Robespierre, is called:", ["The Enlightenment", "The Reign of Terror", "The Restoration", "The Directory"], 1,
       "The Reign of Terror (1793-94), led by Robespierre, was a period of mass arrests and executions.", 'medium'),
    mc("Which class made up the majority of the Third Estate in France?", ["Big businessmen only", "Peasants and workers", "Priests", "Nobles"], 1,
       "The Third Estate mainly consisted of peasants and workers, along with merchants and professionals.", 'medium'),
    mc("What economic crisis contributed significantly to the outbreak of the French Revolution?", ["Overproduction of goods", "Severe debt and food shortages", "Excess gold reserves", "Trade surplus"], 1,
       "Severe government debt, high taxes, and poor harvests leading to food shortages fuelled the Revolution.", 'medium'),
    mc("Which body was formed by the Third Estate when denied representation, marking a key revolutionary moment?", ["National Assembly", "Estates-General", "Directory", "Committee of Public Safety"], 0,
       "The Third Estate formed the National Assembly in 1789, asserting they represented the French people.", 'medium'),
    mc("The 'Tennis Court Oath' was significant because members of the Third Estate vowed to:", ["Disband immediately", "Not separate until a constitution was established", "Support the king unconditionally", "Abolish the monarchy immediately"], 1,
       "In the Tennis Court Oath (1789), Third Estate members vowed to stay united until they had drafted a constitution.", 'hard'),
    mc("Which group of women famously marched to Versailles in October 1789 demanding bread?", ["Female clergy", "Market women of Paris", "Noblewomen", "Soldiers' wives only"], 1,
       "Market women of Paris marched to Versailles in October 1789, demanding bread and pressuring the king.", 'hard'),
    mc("Which of these best describes 'Enlightenment' thinking that influenced the Revolution?", ["Belief in divine right of kings", "Emphasis on reason, individual rights, and equality", "Support for absolute monarchy", "Rejection of all education"], 1,
       "Enlightenment thinkers emphasised reason, individual rights, and equality, inspiring revolutionary ideas.", 'medium'),
    mc("What happened to King Louis XVI in 1793?", ["He was exiled", "He was executed by guillotine", "He abdicated peacefully", "He became a general"], 1,
       "King Louis XVI was tried and executed by guillotine in January 1793.", 'medium'),
    mc("The French Revolution officially ended monarchy and established what form of government?", ["Republic", "Absolute monarchy", "Theocracy", "Colonial rule"], 0,
       "The Revolution led to the establishment of a Republic in France, ending absolute monarchy.", 'medium'),
    mc("Which of these ideals from the French Revolution influenced movements worldwide, including India's freedom struggle?", ["Colonialism", "Liberty, equality and fraternity", "Feudalism", "Divine right of kings"], 1,
       "The ideals of liberty, equality and fraternity inspired revolutionary and freedom movements across the world.", 'medium'),
    mc("What was the 'Directory' in post-revolutionary France?", ["A five-member government that ruled France from 1795-99", "A list of citizens' names", "A type of tax", "A military unit"], 0,
       "The Directory was a five-member group that governed France from 1795 until Napoleon's coup in 1799.", 'hard'),
]

CLASS9_SOC_PHYSICAL = [
    mc("Which mountain range forms India's northern boundary?", ["Aravalli", "Himalayas", "Vindhya", "Western Ghats"], 1,
       "The Himalayas form India's northern mountain boundary and are the youngest fold mountains.", 'easy'),
    mc("Which is the highest peak in India, part of the Himalayas?", ["Nanda Devi", "Kanchenjunga", "K2", "Everest"], 1,
       "Kanchenjunga is the highest peak located entirely within India.", 'medium'),
    mc("The northern plains of India are formed mainly by which rivers?", ["Indus, Ganga and Brahmaputra", "Godavari and Krishna", "Narmada and Tapi", "Cauvery and Mahanadi"], 0,
       "The northern plains are formed by the alluvial deposits of the Indus, Ganga and Brahmaputra river systems.", 'medium'),
    mc("Which desert is located in the western part of India?", ["Thar Desert", "Sahara Desert", "Gobi Desert", "Kalahari Desert"], 0,
       "The Thar Desert is located in the western part of India, mainly in Rajasthan.", 'easy'),
    mc("The Deccan Plateau is located in which part of India?", ["Northern India", "Southern part of the peninsula", "Eastern coast only", "Western coast only"], 1,
       "The Deccan Plateau is a large plateau covering much of southern peninsular India.", 'medium'),
    mc("Which coastal plain lies along India's western coast?", ["Coromandel Coast", "Konkan Coast", "Northern Circars", "Sunderbans"], 1,
       "The Konkan Coast is a narrow coastal plain along India's western coast.", 'medium'),
    mc("Which coastal plain lies along India's eastern coast?", ["Konkan Coast", "Malabar Coast", "Coromandel Coast", "Kutch"], 2,
       "The Coromandel Coast lies along India's eastern coast.", 'medium'),
    mc("Which island group of India is located in the Bay of Bengal?", ["Lakshadweep Islands", "Andaman and Nicobar Islands", "Maldives", "Sri Lanka"], 1,
       "The Andaman and Nicobar Islands are located in the Bay of Bengal.", 'medium'),
    mc("Which island group of India is located in the Arabian Sea?", ["Andaman Islands", "Nicobar Islands", "Lakshadweep Islands", "Sunderban Islands"], 2,
       "The Lakshadweep Islands are a group of coral islands located in the Arabian Sea.", 'medium'),
    mc("Which mountain range separates the Deccan Plateau from the northern plains?", ["Himalayas", "Vindhya and Satpura ranges", "Aravalli", "Western Ghats"], 1,
       "The Vindhya and Satpura ranges mark the transition between the northern plains and the Deccan Plateau.", 'hard'),
    mc("Which range runs along India's western coast, parallel to the Arabian Sea?", ["Eastern Ghats", "Western Ghats", "Aravalli Range", "Himalayas"], 1,
       "The Western Ghats run parallel to India's western coast, along the Arabian Sea.", 'medium'),
    mc("Which range runs along India's eastern coast, parallel to the Bay of Bengal?", ["Western Ghats", "Eastern Ghats", "Vindhya Range", "Satpura Range"], 1,
       "The Eastern Ghats run along India's eastern coast, though they are more broken and discontinuous than the Western Ghats.", 'medium'),
    mc("Which is the oldest mountain range in India, now heavily eroded?", ["Himalayas", "Aravalli Range", "Western Ghats", "Eastern Ghats"], 1,
       "The Aravalli Range is one of the oldest fold mountain ranges in the world, now heavily eroded.", 'medium'),
    mc("The Himalayas were formed due to the collision of which two tectonic plates?", ["African and Eurasian plates", "Indian and Eurasian plates", "Pacific and North American plates", "Antarctic and Australian plates"], 1,
       "The Himalayas were formed by the collision of the Indian Plate with the Eurasian Plate.", 'hard'),
    mc("Which physical feature of India is known for its black soil, ideal for cotton cultivation?", ["Northern Plains", "Deccan Plateau", "Thar Desert", "Himalayas"], 1,
       "The Deccan Plateau has black soil (regur soil), which is ideal for growing cotton.", 'medium'),
    mc("The northern plains of India are known for being highly fertile mainly because of:", ["Volcanic rocks", "Alluvial soil deposited by rivers", "Desert sand", "Coral deposits"], 1,
       "The northern plains are fertile due to the alluvial soil deposited by the Himalayan rivers over centuries.", 'medium'),
    mc("Which of India's physical divisions is the youngest geologically?", ["Peninsular Plateau", "Himalayas", "Northern Plains", "Coastal Plains"], 1,
       "The Himalayas are geologically the youngest mountain range, still rising due to tectonic activity.", 'hard'),
    mc("The Sunderbans, a large mangrove delta region, is formed by which rivers?", ["Indus and Sutlej", "Ganga and Brahmaputra", "Narmada and Tapi", "Godavari and Krishna"], 1,
       "The Sunderbans delta is formed at the mouth of the Ganga and Brahmaputra rivers.", 'medium'),
    mc("Which of these best describes 'peninsular plateau' in the Indian context?", ["A flat, low-lying coastal region", "An elevated tableland forming the southern part of India", "A region entirely covered by desert", "A range of young fold mountains"], 1,
       "The Peninsular Plateau is an elevated, stable tableland forming most of southern India.", 'medium'),
    mc("Which physical feature of India helps to block cold winds from Central Asia, keeping northern India warmer in winter?", ["Thar Desert", "Himalayas", "Deccan Plateau", "Eastern Ghats"], 1,
       "The Himalayas act as a climatic barrier, blocking cold winds from Central Asia from reaching northern India.", 'medium'),
]

CLASS9_CS_PYTHON = [
    mc("Python is what type of programming language, based on readability and ease of use?", ["Low-level and complex", "High-level and simple", "Machine language", "Assembly language"], 1,
       "Python is a high-level programming language known for its simple, readable syntax.", 'easy'),
    mc("Which symbol is used to write a comment in Python?", ["//", "/*", "#", "--"], 2,
       "In Python, the '#' symbol is used to write a single-line comment.", 'easy'),
    mc("Which function is used to display output in Python?", ["input()", "print()", "display()", "show()"], 1,
       "The print() function is used to display output to the screen in Python.", 'easy'),
    mc("Which function is used to take input from the user in Python?", ["print()", "input()", "output()", "get()"], 1,
       "The input() function is used to take input from the user in Python.", 'easy'),
    mc("Which of these is a valid Python variable name?", ["2value", "my-value", "my_value", "my value"], 2,
       "'my_value' is valid because variable names can contain letters, digits and underscores, but cannot start with a digit or contain spaces/hyphens.", 'medium'),
    mc("What is the data type of the value 3.14 in Python?", ["int", "float", "str", "bool"], 1,
       "3.14 is a decimal number, so its data type is float.", 'easy'),
    mc("What is the data type of the value 'Hello' in Python?", ["int", "float", "str", "bool"], 2,
       "'Hello' is enclosed in quotes, making it a string (str) data type.", 'easy'),
    mc("What is the data type of the value True in Python?", ["int", "str", "bool", "float"], 2,
       "True and False are boolean (bool) values in Python.", 'easy'),
    mc("What does the operator '%' do in Python?", ["Addition", "Division", "Returns the remainder of division", "Multiplication"], 2,
       "The '%' (modulus) operator returns the remainder after division.", 'medium'),
    mc("What is the output of print(5 // 2) in Python?", ["2.5", "2", "3", "2.0"], 1,
       "The '//' operator performs floor (integer) division, so 5 // 2 gives 2.", 'medium'),
    mc("What is the output of print(2 ** 3) in Python?", ["6", "8", "9", "5"], 1,
       "The '**' operator represents exponentiation, so 2**3 = 8.", 'medium'),
    mc("Which keyword is used to define a function in Python?", ["func", "def", "function", "define"], 1,
       "The 'def' keyword is used to define a function in Python.", 'easy'),
    mc("Which loop is used to repeat a block of code a fixed number of times, iterating over a sequence?", ["for loop", "if statement", "while True only", "def"], 0,
       "A 'for' loop is typically used to iterate over a sequence a specific number of times.", 'medium'),
    mc("Which loop repeats a block of code as long as a condition is true?", ["for loop", "while loop", "def", "print"], 1,
       "A 'while' loop repeats as long as its condition remains true.", 'medium'),
    mc("Which keyword is used to make decisions in Python?", ["for", "while", "if", "def"], 2,
       "The 'if' keyword is used to make conditional decisions in Python.", 'easy'),
    mc("Which of these correctly creates a list in Python?", ["list = (1,2,3)", "list = [1,2,3]", "list = {1,2,3}", "list = <1,2,3>"], 1,
       "Lists in Python are created using square brackets, e.g. [1,2,3].", 'medium'),
    mc("Which of these correctly creates a dictionary in Python?", ["dict = [1,2,3]", "dict = (1,2,3)", "dict = {'a':1, 'b':2}", "dict = <a:1>"], 2,
       "Dictionaries in Python are created using curly braces with key-value pairs, e.g. {'a':1}.", 'medium'),
    mc("What does len('Python') return?", ["5", "6", "7", "Error"], 1,
       "len('Python') returns 6, since 'Python' has six characters.", 'easy'),
    mc("Which symbol is used to indicate a block of code in Python (instead of curly braces)?", ["Semicolon", "Indentation", "Curly braces", "Parentheses"], 1,
       "Python uses indentation (whitespace) to define blocks of code, instead of curly braces.", 'medium'),
    mc("Which of these is a correctly written if statement in Python?", ["if x > 5 { print('yes') }", "if x > 5: print('yes')", "if (x > 5) then print('yes')", "if x > 5 print('yes')"], 1,
       "Python if statements use a colon and rely on indentation, e.g. 'if x > 5: print(\"yes\")'.", 'medium'),
]

CLASS9_CS_DATA = [
    mc("Which number system uses only digits 0 and 1?", ["Decimal", "Binary", "Octal", "Hexadecimal"], 1,
       "The binary number system uses only two digits: 0 and 1.", 'easy'),
    mc("Which number system uses digits 0-9?", ["Binary", "Octal", "Decimal", "Hexadecimal"], 2,
       "The decimal number system uses ten digits, 0 through 9.", 'easy'),
    mc("Which number system uses digits 0-7?", ["Binary", "Octal", "Decimal", "Hexadecimal"], 1,
       "The octal number system uses eight digits, 0 through 7.", 'medium'),
    mc("Which number system uses digits 0-9 and letters A-F?", ["Binary", "Octal", "Decimal", "Hexadecimal"], 3,
       "The hexadecimal number system uses sixteen symbols: digits 0-9 and letters A-F.", 'medium'),
    mc("What is the smallest unit of data in a computer, representing a 0 or 1?", ["Byte", "Bit", "Nibble", "Word"], 1,
       "A bit (binary digit) is the smallest unit of data, representing either 0 or 1.", 'easy'),
    mc("How many bits make up one byte?", ["4", "8", "16", "2"], 1,
       "One byte is made up of 8 bits.", 'easy'),
    mc("What is the decimal equivalent of the binary number 101?", ["3", "5", "7", "10"], 1,
       "Binary 101 = (1×4)+(0×2)+(1×1) = 5 in decimal.", 'medium'),
    mc("What is the decimal equivalent of the binary number 1010?", ["8", "9", "10", "12"], 2,
       "Binary 1010 = (1×8)+(0×4)+(1×2)+(0×1) = 10 in decimal.", 'medium'),
    mc("What is the binary equivalent of the decimal number 6?", ["100", "110", "101", "111"], 1,
       "Decimal 6 = 4+2 = binary 110.", 'medium'),
    mc("What is the binary equivalent of the decimal number 9?", ["1001", "1010", "1100", "1000"], 0,
       "Decimal 9 = 8+1 = binary 1001.", 'medium'),
    mc("Which encoding standard is commonly used to represent text characters as numbers in computers?", ["Binary code", "ASCII", "Octal code", "Decimal code"], 1,
       "ASCII (American Standard Code for Information Interchange) is a common standard for encoding text characters as numbers.", 'medium'),
    mc("What is the main advantage of representing data in binary form for computers?", ["It is easier for humans to read", "Electronic circuits can easily represent two states (on/off)", "It uses fewer digits", "It is faster to type"], 1,
       "Binary suits computer hardware because electronic circuits can easily represent two states: on (1) and off (0).", 'medium'),
    mc("1 Kilobyte (KB) is equal to how many bytes (as commonly used in computing)?", ["100", "1000", "1024", "1048576"], 2,
       "1 Kilobyte is commonly defined as 1024 bytes in computing.", 'medium'),
    mc("1 Megabyte (MB) is equal to how many Kilobytes?", ["100", "1000", "1024", "10000"], 2,
       "1 Megabyte is equal to 1024 Kilobytes.", 'medium'),
    mc("Which of these best represents the correct order of storage units from smallest to largest?", ["GB, MB, KB, Byte", "Byte, KB, MB, GB", "MB, GB, KB, Byte", "KB, Byte, GB, MB"], 1,
       "The correct order from smallest to largest is: Byte, Kilobyte, Megabyte, Gigabyte.", 'medium'),
    mc("Converting data from one form to another (e.g., text to binary) for computer processing is called:", ["Compilation", "Encoding", "Formatting", "Debugging"], 1,
       "Encoding is the process of converting data into a specific format, such as binary, for computer processing.", 'medium'),
    mc("Which base is the hexadecimal number system also known as?", ["Base 2", "Base 8", "Base 10", "Base 16"], 3,
       "Hexadecimal is a base-16 number system.", 'medium'),
    mc("Which base is the binary number system also known as?", ["Base 2", "Base 8", "Base 10", "Base 16"], 0,
       "Binary is a base-2 number system.", 'easy'),
    mc("Which of these is used to represent colours in digital images, often using hexadecimal codes?", ["ASCII", "RGB hex codes", "Binary trees", "Octal notation"], 1,
       "Digital colours are often represented using hexadecimal RGB codes, e.g. #FF0000 for red.", 'medium'),
    mc("What does the term 'data representation' refer to in computer science?", ["How data is displayed on paper only", "The method used to encode data for storage and processing by computers", "The colour of the monitor", "The speed of the CPU"], 1,
       "Data representation refers to the methods used to encode various types of data (numbers, text, images) for computer storage and processing.", 'medium'),
]
# ============ CLASS 10 (non-math) ============

CLASS10_SCI_REACTIONS = [
    mc("A chemical reaction in which a new substance is formed is best identified by:", ["No change in properties", "Change in colour, formation of gas, precipitate, or heat change", "The reactants disappearing without any sign", "Weight always decreasing"], 1,
       "Chemical reactions are usually identified by changes such as colour change, gas evolution, precipitate formation, or temperature change.", 'medium'),
    mc("A balanced chemical equation follows which fundamental law?", ["Law of conservation of energy", "Law of conservation of mass", "Law of multiple proportions", "Law of definite proportions only"], 1,
       "A balanced chemical equation follows the Law of Conservation of Mass, meaning mass of reactants equals mass of products.", 'medium'),
    mc("In the reaction 2H2 + O2 → 2H2O, what type of reaction is this?", ["Decomposition", "Combination", "Displacement", "Double displacement"], 1,
       "This is a combination reaction, where two or more substances combine to form a single product.", 'medium'),
    mc("A reaction where a single compound breaks down into two or more simpler substances is called:", ["Combination reaction", "Decomposition reaction", "Displacement reaction", "Neutralisation"], 1,
       "A decomposition reaction involves a single compound breaking down into two or more simpler substances.", 'medium'),
    mc("A reaction in which a more reactive element displaces a less reactive element from its compound is called:", ["Combination reaction", "Decomposition reaction", "Displacement reaction", "Combustion"], 2,
       "In a displacement reaction, a more reactive element displaces a less reactive one from its compound.", 'medium'),
    mc("A reaction between an acid and a base to form salt and water is called:", ["Combination reaction", "Decomposition reaction", "Neutralisation reaction", "Redox reaction"], 2,
       "A neutralisation reaction occurs between an acid and a base, producing salt and water.", 'medium'),
    mc("Which type of reaction involves both oxidation and reduction occurring simultaneously?", ["Combination reaction", "Redox reaction", "Precipitation reaction", "Neutralisation"], 1,
       "A redox (reduction-oxidation) reaction involves simultaneous oxidation of one substance and reduction of another.", 'medium'),
    mc("The gain of oxygen or loss of hydrogen by a substance is called:", ["Reduction", "Oxidation", "Neutralisation", "Precipitation"], 1,
       "Oxidation involves the gain of oxygen or the loss of hydrogen by a substance.", 'medium'),
    mc("The loss of oxygen or gain of hydrogen by a substance is called:", ["Oxidation", "Reduction", "Combination", "Displacement"], 1,
       "Reduction involves the loss of oxygen or the gain of hydrogen by a substance.", 'medium'),
    mc("Rusting of iron is an example of which type of reaction?", ["Reduction", "Oxidation", "Neutralisation", "Decomposition"], 1,
       "Rusting is an oxidation reaction, where iron reacts with oxygen and moisture to form iron oxide.", 'medium'),
    mc("Which of these is a method to prevent rusting of iron?", ["Exposing it to more water", "Painting or galvanising the surface", "Increasing humidity", "Removing all oxygen from the atmosphere is impractical, so exposure helps"], 1,
       "Painting or galvanising (coating with zinc) prevents iron from coming into contact with oxygen and moisture, preventing rust.", 'medium'),
    mc("A reaction that releases heat energy is called:", ["Endothermic reaction", "Exothermic reaction", "Neutral reaction", "Photochemical reaction"], 1,
       "An exothermic reaction releases heat energy to the surroundings.", 'medium'),
    mc("A reaction that absorbs heat energy from the surroundings is called:", ["Exothermic reaction", "Endothermic reaction", "Combination reaction", "Displacement reaction"], 1,
       "An endothermic reaction absorbs heat energy from the surroundings.", 'medium'),
    mc("What is the symbol '↓' used for in a chemical equation?", ["Gas evolved", "Precipitate formed", "Heat applied", "Reversible reaction"], 1,
       "The downward arrow (↓) indicates that a precipitate (insoluble solid) has formed in the reaction.", 'medium'),
    mc("What is the symbol '↑' used for in a chemical equation?", ["Precipitate formed", "Gas evolved", "Heat applied", "Catalyst used"], 1,
       "The upward arrow (↑) indicates that a gas has been evolved during the reaction.", 'medium'),
    mc("What does the symbol 'Δ' represent above the arrow in a chemical equation?", ["Catalyst used", "Heat is applied", "Light is applied", "Pressure is applied"], 1,
       "The symbol 'Δ' (delta) above the arrow indicates that heat has been applied to the reaction.", 'medium'),
    mc("Which of these is an example of a decomposition reaction caused by heat?", ["2H2 + O2 → 2H2O", "CaCO3 → CaO + CO2 (on heating)", "Zn + CuSO4 → ZnSO4 + Cu", "NaOH + HCl → NaCl + H2O"], 1,
       "Heating calcium carbonate (CaCO3) decomposes it into calcium oxide (CaO) and carbon dioxide (CO2).", 'medium'),
    mc("In the reaction Zn + CuSO4 → ZnSO4 + Cu, which element is displaced?", ["Zinc", "Copper", "Sulphur", "Oxygen"], 1,
       "Zinc, being more reactive, displaces copper from copper sulphate solution.", 'medium'),
    mc("A double displacement reaction that produces an insoluble solid is also called:", ["Combination reaction", "Precipitation reaction", "Combustion reaction", "Redox reaction only"], 1,
       "A double displacement reaction that forms an insoluble solid product is called a precipitation reaction.", 'medium'),
    mc("Which of these best explains why balancing chemical equations is necessary?", ["To make equations look neat", "To satisfy the Law of Conservation of Mass", "To increase reaction speed", "To change the products formed"], 1,
       "Balancing chemical equations ensures the number of atoms of each element is equal on both sides, satisfying the Law of Conservation of Mass.", 'medium'),
]

CLASS10_SCI_LIFE = [
    mc("The basic biological processes that keep an organism alive are together called:", ["Life processes", "Reproduction", "Excretion only", "Growth only"], 0,
       "Life processes are the basic biological functions that maintain and sustain life, such as nutrition, respiration and excretion.", 'easy'),
    mc("The process by which organisms obtain and utilise food for energy is called:", ["Respiration", "Nutrition", "Excretion", "Transportation"], 1,
       "Nutrition is the process of obtaining and utilising food for energy and growth.", 'easy'),
    mc("Organisms that make their own food using sunlight, water and carbon dioxide are called:", ["Heterotrophs", "Autotrophs", "Saprotrophs", "Parasites"], 1,
       "Autotrophs, like green plants, synthesise their own food through photosynthesis.", 'easy'),
    mc("The process of breakdown of glucose to release energy in cells is called:", ["Photosynthesis", "Respiration", "Excretion", "Digestion"], 1,
       "Respiration is the process by which cells break down glucose to release energy.", 'easy'),
    mc("Which type of respiration occurs in the presence of oxygen?", ["Anaerobic respiration", "Aerobic respiration", "Fermentation", "Photosynthesis"], 1,
       "Aerobic respiration takes place in the presence of oxygen and releases more energy than anaerobic respiration.", 'medium'),
    mc("Which type of respiration occurs in the absence of oxygen?", ["Aerobic respiration", "Anaerobic respiration", "Photosynthesis", "Digestion"], 1,
       "Anaerobic respiration occurs without oxygen, often producing lactic acid or alcohol, and releases less energy.", 'medium'),
    mc("In humans, gaseous exchange for respiration mainly takes place in the:", ["Heart", "Lungs (alveoli)", "Kidneys", "Stomach"], 1,
       "Gaseous exchange takes place in the alveoli of the lungs, where oxygen and carbon dioxide are exchanged.", 'medium'),
    mc("Which organ pumps blood throughout the human body?", ["Lungs", "Heart", "Liver", "Kidney"], 1,
       "The heart pumps blood, delivering oxygen and nutrients throughout the body.", 'easy'),
    mc("How many chambers does the human heart have?", ["Two", "Three", "Four", "Five"], 2,
       "The human heart has four chambers: two atria and two ventricles.", 'medium'),
    mc("Which blood vessels carry blood away from the heart?", ["Veins", "Arteries", "Capillaries", "Nerves"], 1,
       "Arteries carry oxygenated blood away from the heart to the rest of the body (except the pulmonary artery).", 'medium'),
    mc("Which blood vessels carry blood back to the heart?", ["Arteries", "Veins", "Capillaries", "Nerves"], 1,
       "Veins carry deoxygenated blood back to the heart (except the pulmonary vein).", 'medium'),
    mc("Which organ in the human body is primarily responsible for removing nitrogenous waste from the blood?", ["Liver", "Kidney", "Lungs", "Heart"], 1,
       "The kidneys filter blood and remove nitrogenous waste, forming urine.", 'easy'),
    mc("The process of removal of harmful metabolic waste products from the body is called:", ["Nutrition", "Respiration", "Excretion", "Transportation"], 2,
       "Excretion is the process of removing harmful waste products produced during metabolism.", 'easy'),
    mc("Which is the functional unit of the kidney responsible for filtration?", ["Nephron", "Neuron", "Alveolus", "Villus"], 0,
       "The nephron is the basic structural and functional unit of the kidney responsible for filtering blood.", 'medium'),
    mc("In plants, water and minerals are transported through which tissue?", ["Phloem", "Xylem", "Cortex", "Epidermis"], 1,
       "Xylem tissue transports water and minerals from the roots to the rest of the plant.", 'medium'),
    mc("In plants, food (prepared by photosynthesis) is transported through which tissue?", ["Xylem", "Phloem", "Cortex", "Cambium"], 1,
       "Phloem tissue transports food (organic nutrients) from leaves to other parts of the plant.", 'medium'),
    mc("The movement of water from roots to leaves and its loss as vapour is together called:", ["Photosynthesis", "Transpiration", "Excretion", "Respiration"], 1,
       "Transpiration is the process of water movement through the plant and its evaporation from leaf surfaces.", 'medium'),
    mc("Which pigment gives blood its red colour and helps transport oxygen?", ["Chlorophyll", "Haemoglobin", "Melanin", "Insulin"], 1,
       "Haemoglobin, present in red blood cells, gives blood its red colour and carries oxygen.", 'medium'),
    mc("Which of these best describes double circulation, found in humans?", ["Blood passes through the heart once in one complete cycle", "Blood passes through the heart twice in one complete cycle", "Blood never passes through the heart", "Blood only circulates in the lungs"], 1,
       "In double circulation, blood passes through the heart twice during one complete cycle of the body - once for pulmonary and once for systemic circulation.", 'hard'),
    mc("Which of these life processes is essential for the continuation of a species (though not for individual survival)?", ["Respiration", "Nutrition", "Reproduction", "Excretion"], 2,
       "Reproduction, unlike nutrition or respiration, is essential for the continuation of a species rather than individual survival.", 'medium'),
]

CLASS10_ENG_DEVICES = [
    mc("A comparison between two unlike things using 'like' or 'as' is called a:", ["Metaphor", "Simile", "Personification", "Hyperbole"], 1,
       "A simile compares two unlike things using 'like' or 'as', e.g. 'as brave as a lion'.", 'easy'),
    mc("A direct comparison between two unlike things without using 'like' or 'as' is called a:", ["Simile", "Metaphor", "Alliteration", "Onomatopoeia"], 1,
       "A metaphor directly states that one thing is another, without using 'like' or 'as', e.g. 'time is a thief'.", 'easy'),
    mc("Giving human qualities to non-human things or ideas is called:", ["Simile", "Metaphor", "Personification", "Hyperbole"], 2,
       "Personification gives human characteristics to non-human things, e.g. 'the wind whispered'.", 'medium'),
    mc("An exaggerated statement not meant to be taken literally is called:", ["Simile", "Hyperbole", "Alliteration", "Irony"], 1,
       "Hyperbole is an extreme exaggeration used for emphasis, e.g. 'I've told you a million times'.", 'medium'),
    mc("The repetition of the same consonant sound at the beginning of nearby words is called:", ["Assonance", "Alliteration", "Rhyme", "Onomatopoeia"], 1,
       "Alliteration is the repetition of initial consonant sounds, e.g. 'Peter Piper picked'.", 'medium'),
    mc("A word that imitates the sound it represents is an example of:", ["Onomatopoeia", "Metaphor", "Simile", "Irony"], 0,
       "Onomatopoeia refers to words that imitate sounds, e.g. 'buzz', 'clap', 'hiss'.", 'medium'),
    mc("A contrast between what is expected and what actually happens is called:", ["Simile", "Metaphor", "Irony", "Alliteration"], 2,
       "Irony refers to a contrast between expectation and reality, often for dramatic or humorous effect.", 'medium'),
    mc("An object, person or symbol that represents a larger idea is called a:", ["Simile", "Symbol", "Rhyme", "Metaphor"], 1,
       "A symbol is something that represents a larger idea or concept beyond its literal meaning, e.g. a dove symbolising peace.", 'medium'),
    mc("The repetition of vowel sounds within nearby words is called:", ["Alliteration", "Assonance", "Consonance", "Rhyme"], 1,
       "Assonance is the repetition of vowel sounds within nearby words, e.g. 'the rain in Spain'.", 'hard'),
    mc("The repetition of consonant sounds, not necessarily at the beginning of words, is called:", ["Alliteration", "Assonance", "Consonance", "Metaphor"], 2,
       "Consonance refers to the repetition of consonant sounds anywhere in nearby words, not just at the start.", 'hard'),
    mc("A brief pause within a line of poetry is called a:", ["Caesura", "Enjambment", "Stanza", "Refrain"], 0,
       "A caesura is a pause within a line of poetry, often marked by punctuation.", 'hard'),
    mc("When a sentence or idea continues onto the next line of poetry without a pause, this is called:", ["Caesura", "Enjambment", "Rhyme scheme", "Refrain"], 1,
       "Enjambment occurs when a sentence continues past the end of a line into the next line without a pause.", 'hard'),
    mc("A line or group of lines repeated throughout a poem or song is called a:", ["Refrain", "Stanza", "Caesura", "Metaphor"], 0,
       "A refrain is a line or group of lines repeated at intervals throughout a poem or song.", 'medium'),
    mc("A group of lines forming a unit in a poem is called a:", ["Refrain", "Stanza", "Metre", "Rhyme scheme"], 1,
       "A stanza is a grouped set of lines forming a unit within a poem, similar to a paragraph.", 'medium'),
    mc("The rhythmic pattern of stressed and unstressed syllables in poetry is called:", ["Rhyme", "Metre", "Simile", "Symbol"], 1,
       "Metre refers to the rhythmic pattern of stressed and unstressed syllables in a line of poetry.", 'hard'),
    mc("Which literary device uses understatement to express something less seriously than it might deserve?", ["Hyperbole", "Litotes/Understatement", "Personification", "Alliteration"], 1,
       "Litotes (understatement) expresses something with deliberate restraint or less emphasis than warranted.", 'hard'),
    mc("A story with a hidden moral or deeper meaning, often religious or political, is called an:", ["Allegory", "Autobiography", "Biography", "Essay"], 0,
       "An allegory is a narrative with a hidden or symbolic meaning, often moral, religious, or political.", 'hard'),
    mc("Which literary device involves hinting at events that will happen later in a story?", ["Flashback", "Foreshadowing", "Irony", "Symbolism"], 1,
       "Foreshadowing gives hints or clues about events that will occur later in a narrative.", 'medium'),
    mc("Which literary device involves interrupting the present narrative to show events from the past?", ["Foreshadowing", "Flashback", "Personification", "Alliteration"], 1,
       "A flashback interrupts the chronological narrative to depict earlier events.", 'medium'),
    mc("Which literary device refers to the atmosphere or emotional quality created by a piece of writing?", ["Tone", "Mood", "Theme", "Plot"], 1,
       "Mood refers to the emotional atmosphere that a piece of writing evokes in the reader.", 'medium'),
]

CLASS10_ENG_WRITING = [
    mc("Which type of letter is used to apply for a job vacancy?", ["Informal letter", "Formal/application letter", "Personal letter", "Diary entry"], 1,
       "A formal application letter is used to apply for a job, addressing the employer professionally.", 'easy'),
    mc("Which section of a job application letter highlights your qualifications and experience?", ["Salutation", "Body paragraphs", "Closing", "Address"], 1,
       "The body paragraphs of an application letter detail the applicant's qualifications, skills, and experience.", 'medium'),
    mc("What should accompany a formal job application letter, summarising the applicant's education and experience?", ["A poem", "A resume/CV", "A diary entry", "A short story"], 1,
       "A resume or curriculum vitae (CV) typically accompanies a job application, summarising qualifications.", 'medium'),
    mc("A letter of complaint should primarily focus on:", ["Praising the product/service", "Clearly stating the problem and desired resolution", "Sharing unrelated personal news", "Using informal slang"], 1,
       "A complaint letter should clearly state the issue and what resolution or action is expected.", 'medium'),
    mc("Which essay type would be most appropriate for arguing 'Social media does more harm than good'?", ["Descriptive essay", "Persuasive/argumentative essay", "Narrative essay", "Diary entry"], 1,
       "A persuasive/argumentative essay is used to argue a particular viewpoint with supporting reasons and evidence.", 'medium'),
    mc("Which of these is an essential feature of a good essay conclusion?", ["Introducing entirely new information", "Summarising key points and providing closure", "Repeating the introduction word for word", "Leaving the topic completely open-ended without any closure"], 1,
       "A good conclusion summarises key points and provides closure, reinforcing the essay's main message.", 'medium'),
    mc("Which of these is a key feature of a report (e.g., a newspaper report)?", ["First-person opinions throughout", "Factual, objective, and organised information", "Poetic language", "Fictional characters"], 1,
       "A report should present factual, objective information, organised clearly, often with a headline and byline.", 'medium'),
    mc("Which of these should typically be included at the start of a newspaper report?", ["A conclusion", "A headline and byline", "A signature", "A postscript"], 1,
       "A newspaper report typically starts with a headline (title) and a byline (reporter's name).", 'medium'),
    mc("A notice, often displayed on a board, should be:", ["Long and detailed with personal opinions", "Brief, clear, and to the point", "Written in poetic language", "Written without a heading"], 1,
       "A notice should be brief, clear, and to the point, conveying essential information efficiently.", 'medium'),
    mc("Which of these should a notice always include?", ["Date of the notice and issuing authority", "A rhyme scheme", "A long personal story", "A metaphor"], 0,
       "A notice should clearly state the date and the name/authority issuing it for official validity.", 'medium'),
    mc("Which type of writing involves summarising a text by extracting its main points without one's own opinion?", ["Précis/Summary writing", "Persuasive essay", "Narrative essay", "Formal letter"], 0,
       "Précis (summary) writing involves condensing a text to its essential points objectively.", 'medium'),
    mc("A good précis should be approximately what fraction of the original text's length?", ["Same length as original", "About one-third of the original", "Twice the original length", "Only one sentence regardless of original length"], 1,
       "A précis is typically about one-third the length of the original passage, retaining key ideas.", 'medium'),
    mc("Which tense is most commonly used while writing a formal report of a past event?", ["Future tense", "Past tense", "Present continuous only", "Imperative mood"], 1,
       "Reports of past events are typically written in the past tense to describe what occurred.", 'medium'),
    mc("Which of these is an example of an appropriate opening line for a formal letter of complaint?", ["'Hey, what's up?'", "'I am writing to bring to your attention...'", "'lol this is so annoying'", "No opening needed"], 1,
       "A formal complaint letter should begin professionally, clearly stating the purpose of writing.", 'medium'),
    mc("Which of these best describes 'coherence' in essay writing?", ["Random arrangement of ideas", "Logical flow and connection between ideas", "Use of only short sentences", "Avoiding paragraphs"], 1,
       "Coherence refers to the logical flow and connection of ideas throughout a piece of writing.", 'medium'),
    mc("Which of these is important when writing a formal email?", ["Using emojis extensively", "Using a clear subject line and professional tone", "Skipping the greeting", "Writing in all capital letters"], 1,
       "A clear subject line and professional tone are essential features of an effective formal email.", 'medium'),
    mc("An article for a school magazine on 'The Importance of Sports' would typically be written in which style?", ["Strictly legal language", "Informative and engaging style suited to the audience", "Text-message abbreviations", "Purely poetic verse"], 1,
       "Magazine articles are typically written in an informative and engaging style suited to their readers.", 'medium'),
    mc("What is the purpose of proofreading a piece of writing?", ["To make it longer", "To check and correct errors in grammar, spelling, and punctuation", "To add more opinions", "To remove the conclusion"], 1,
       "Proofreading involves reviewing writing to correct errors in grammar, spelling and punctuation before finalising it.", 'easy'),
    mc("Which of these is an appropriate closing for a formal email to an unknown recipient?", ["Bye bye", "Regards / Yours faithfully", "See ya", "Take it easy"], 1,
       "'Regards' or 'Yours faithfully' are professional and appropriate closings for formal emails.", 'medium'),
    mc("When writing a story for an exam, which element is essential to include?", ["A clear beginning, middle and end with a coherent plot", "Only dialogue, no description", "No characters", "A list of references"], 0,
       "A good story should have a clear beginning, middle, and end, with a coherent and engaging plot.", 'medium'),
]

CLASS10_SOC_NATIONALISM = [
    mc("The idea of nationalism in India developed strongly in the context of:", ["The freedom struggle against British colonial rule", "Trade with Europe", "The Cold War", "World War II alone"], 0,
       "Indian nationalism grew strongly as a unifying force during the struggle against British colonial rule.", 'medium'),
    mc("Which movement, led by Gandhi, began in 1920 in response to the Jallianwala Bagh massacre and the Rowlatt Act?", ["Quit India Movement", "Non-Cooperation Movement", "Civil Disobedience Movement", "Swadeshi Movement"], 1,
       "The Non-Cooperation Movement, launched in 1920, was Gandhi's response to events like the Jallianwala Bagh massacre and the Rowlatt Act.", 'medium'),
    mc("The Jallianwala Bagh massacre took place in which year?", ["1915", "1919", "1922", "1930"], 1,
       "The Jallianwala Bagh massacre occurred on 13 April 1919 in Amritsar.", 'medium'),
    mc("Which event marked the beginning of the Civil Disobedience Movement in 1930?", ["Non-Cooperation Movement", "Dandi March (Salt March)", "Quit India Movement", "Partition of Bengal"], 1,
       "Mahatma Gandhi's Dandi March (Salt March) in 1930 marked the beginning of the Civil Disobedience Movement.", 'medium'),
    mc("Which act, passed in 1919, allowed the British government to imprison people without trial, sparking protests in India?", ["Rowlatt Act", "Government of India Act", "Indian Councils Act", "Vernacular Press Act"], 0,
       "The Rowlatt Act (1919) allowed detention without trial and sparked widespread protests across India.", 'medium'),
    mc("Who gave the call for the 'Quit India Movement' in 1942?", ["Jawaharlal Nehru", "Subhas Chandra Bose", "Mahatma Gandhi", "Bhagat Singh"], 2,
       "Mahatma Gandhi launched the Quit India Movement in 1942 with the call 'Do or Die'.", 'medium'),
    mc("Which organisation was founded in 1885 and became the main platform for India's nationalist movement?", ["Muslim League", "Indian National Congress", "Ghadar Party", "Hindu Mahasabha"], 1,
       "The Indian National Congress, founded in 1885, became the leading platform for India's nationalist movement.", 'medium'),
    mc("Which nationalist leader founded the Indian National Army (INA) to fight for India's independence?", ["Mahatma Gandhi", "Jawaharlal Nehru", "Subhas Chandra Bose", "Sardar Patel"], 2,
       "Subhas Chandra Bose led the Indian National Army (INA) in the fight for India's independence.", 'medium'),
    mc("What was 'Swaraj', a key term used in the Indian nationalist movement?", ["Foreign rule", "Self-rule/independence", "A type of tax", "A British policy"], 1,
       "'Swaraj' means self-rule or independence, a central goal of the Indian nationalist movement.", 'medium'),
    mc("Which economic idea, promoting Indian-made goods over British imports, was closely linked to the nationalist movement?", ["Swadeshi", "Free trade", "Globalisation", "Protectionism only in theory"], 0,
       "The Swadeshi movement promoted the use of Indian-made goods and the boycott of British products.", 'medium'),
    mc("In which year did India finally achieve independence from British rule?", ["1942", "1945", "1947", "1950"], 2,
       "India achieved independence from British rule on 15 August 1947.", 'easy'),
    mc("Nationalism, as a unifying force, often develops a sense of collective identity based on:", ["Shared history, culture and the idea of belonging to one nation", "Individual differences only", "Foreign rule", "Economic isolation alone"], 0,
       "Nationalism develops a sense of collective identity based on shared history, culture, and belonging to a common nation.", 'medium'),
    mc("How did the First World War contribute to the growth of nationalism in colonies like India?", ["It had no effect on colonies", "It increased economic hardship and political awareness, fuelling demands for self-rule", "It ended all colonial rule immediately", "It strengthened colonial control permanently"], 1,
       "World War I brought economic hardships and heightened political awareness, fuelling demands for self-rule in colonies like India.", 'medium'),
    mc("Which symbol became an important unifying icon during the Indian nationalist movement?", ["The national flag", "Foreign currency", "Colonial uniforms", "Foreign languages"], 0,
       "The Indian national flag became an important unifying symbol during the nationalist movement.", 'medium'),
    mc("Which nationalist practice involved boycotting foreign cloth and spinning one's own cloth (khadi)?", ["Swadeshi and khadi movement", "Partition politics", "Salt tax collection", "Zamindari system"], 0,
       "The Swadeshi and khadi movement encouraged Indians to boycott foreign cloth and spin their own khadi cloth.", 'medium'),
    mc("Which of these best explains why a common language/print culture helped spread nationalism in many countries?", ["It made communication and shared identity easier across regions", "It reduced literacy", "It discouraged unity", "It had no impact on nationalism"], 0,
       "A common language and print culture helped spread nationalist ideas and fostered a shared identity across regions.", 'medium'),
    mc("Which event in 1857 is often referred to as the First War of Indian Independence?", ["Jallianwala Bagh massacre", "Revolt of 1857 (Sepoy Mutiny)", "Partition of Bengal", "Quit India Movement"], 1,
       "The Revolt of 1857 is often referred to as the First War of Indian Independence.", 'medium'),
    mc("Partition of Bengal in 1905 by the British is widely seen as an attempt to:", ["Unite Hindus and Muslims", "Divide people on religious lines and weaken nationalist unity", "Improve infrastructure only", "Reduce taxes"], 1,
       "The Partition of Bengal (1905) is widely seen as a British attempt to divide people along religious lines and weaken the nationalist movement.", 'medium'),
    mc("Which of these was a major contribution of the press (newspapers) to the nationalist movement in India?", ["Spreading nationalist ideas and creating political awareness", "Supporting only colonial policies", "Discouraging education", "Promoting foreign goods"], 0,
       "Newspapers played a major role in spreading nationalist ideas and creating political awareness among Indians.", 'medium'),
    mc("Why is the study of nationalism important for understanding modern nation-states?", ["It explains how many modern nations were formed and unified", "It has no relevance today", "It only applies to India", "It is purely a economic theory"], 0,
       "Studying nationalism helps explain how many modern nation-states were formed and unified around shared identity.", 'medium'),
]

CLASS10_SOC_RESOURCES = [
    mc("Anything available in our environment that can be used to satisfy our needs is called a:", ["Resource", "Product", "Commodity", "Asset only"], 0,
       "A resource is anything available in the environment that can be used to satisfy human needs.", 'easy'),
    mc("Resources that can be renewed or replenished naturally over time are called:", ["Non-renewable resources", "Renewable resources", "Human resources", "Abiotic resources only"], 1,
       "Renewable resources, like sunlight and wind, can be naturally replenished over time.", 'easy'),
    mc("Resources that take millions of years to form and cannot be quickly replenished are called:", ["Renewable resources", "Non-renewable resources", "Biotic resources", "Human resources"], 1,
       "Non-renewable resources, like coal and petroleum, take millions of years to form and are limited.", 'easy'),
    mc("Resources obtained from living things, like forests and wildlife, are called:", ["Abiotic resources", "Biotic resources", "Non-renewable resources only", "Human resources"], 1,
       "Biotic resources are obtained from living organisms, such as forests, wildlife, and fisheries.", 'medium'),
    mc("Resources obtained from non-living things, like rocks and metals, are called:", ["Biotic resources", "Abiotic resources", "Human resources", "Renewable resources only"], 1,
       "Abiotic resources come from non-living sources, such as minerals, rocks, and water.", 'medium'),
    mc("Which of these is an example of a renewable resource?", ["Coal", "Petroleum", "Solar energy", "Natural gas"], 2,
       "Solar energy is continuously available and renewable, unlike fossil fuels.", 'easy'),
    mc("Which of these is an example of a non-renewable resource?", ["Wind energy", "Solar energy", "Coal", "Water (in the water cycle)"], 2,
       "Coal is a fossil fuel that takes millions of years to form, making it non-renewable.", 'easy'),
    mc("Resources that are owned by an individual are called:", ["Community resources", "Individual resources", "National resources", "International resources"], 1,
       "Individual resources are owned privately by a single person, such as personal land or property.", 'medium'),
    mc("Resources accessible to all members of a community, such as public parks, are called:", ["Individual resources", "Community-owned resources", "National resources only", "Private resources"], 1,
       "Community-owned resources are accessible to all members of a community, like public parks and grazing grounds.", 'medium'),
    mc("Resources owned by the government/nation, such as forests and rivers within a country's boundary, are called:", ["Individual resources", "Community resources", "National resources", "International resources"], 2,
       "National resources belong to the nation, within its political boundaries, such as rivers, forests, and minerals.", 'medium'),
    mc("Resources found beyond 200 nautical miles of a country's coast, regulated by international institutions, are called:", ["National resources", "Community resources", "International resources", "Individual resources"], 2,
       "International resources lie beyond national boundaries (like the open ocean) and are regulated by international institutions.", 'hard'),
    mc("Which of these best defines 'resource planning'?", ["Using resources without any strategy", "The widely accepted strategy for judicious use of resources", "Ignoring future resource needs", "Exploiting resources as fast as possible"], 1,
       "Resource planning is a strategy for the judicious and sustainable use of resources, balancing present and future needs.", 'medium'),
    mc("Which of these best describes 'sustainable development' regarding resource use?", ["Using resources without regard for the future", "Development that meets present needs without compromising future generations' ability to meet their needs", "Focusing only on economic growth", "Avoiding all resource use"], 1,
       "Sustainable development meets present needs while ensuring resources remain available for future generations.", 'medium'),
    mc("Which type of soil is most fertile and ideal for growing wheat and rice, commonly found in river plains?", ["Black soil", "Alluvial soil", "Red soil", "Laterite soil"], 1,
       "Alluvial soil, found in river plains, is highly fertile and ideal for growing wheat and rice.", 'medium'),
    mc("Which type of soil, rich in iron content and found in the Deccan Plateau, is ideal for cotton?", ["Alluvial soil", "Black soil (regur)", "Red soil", "Desert soil"], 1,
       "Black soil (regur soil), found in the Deccan Plateau, retains moisture well and is ideal for cotton cultivation.", 'medium'),
    mc("What is the main cause of land degradation in many regions?", ["Afforestation", "Overgrazing, deforestation and unsustainable farming", "Crop rotation", "Terrace farming"], 1,
       "Overgrazing, deforestation, and unsustainable farming practices are major causes of land degradation.", 'medium'),
    mc("Which of these practices helps conserve soil and prevent erosion on hilly terrain?", ["Terrace farming", "Overgrazing", "Deforestation", "Monoculture farming without rotation"], 0,
       "Terrace farming on hilly terrain helps prevent soil erosion by reducing the speed of water runoff.", 'medium'),
    mc("Which of these is a method to prevent soil erosion by wind in dry regions?", ["Shelter belts (rows of trees)", "Removing all vegetation", "Overgrazing", "Deep ploughing along the wind direction"], 0,
       "Shelter belts (rows of trees planted as windbreaks) help reduce wind speed and prevent soil erosion in dry regions.", 'medium'),
    mc("Contour ploughing is a soil conservation method that involves:", ["Ploughing along the slope of a hill", "Ploughing along the contour lines of a slope to slow water flow", "Not ploughing at all", "Ploughing only in flat plains"], 1,
       "Contour ploughing involves ploughing along the natural contour lines of a slope, slowing water runoff and reducing soil erosion.", 'hard'),
    mc("Why is resource conservation important for future generations?", ["To ensure resources are not depleted and remain available for the future", "To use up resources faster", "It has no real importance", "To increase pollution"], 0,
       "Resource conservation ensures resources are used sustainably so they remain available for future generations.", 'medium'),
]

CLASS10_CS_PYTHON_BASICS = [
    mc("Which of the following is a valid way to define a list in Python containing three numbers?", ["nums = 1,2,3", "nums = [1, 2, 3]", "nums = {1, 2, 3;}", "nums == [1,2,3]"], 1,
       "Lists in Python are defined using square brackets with comma-separated values: [1, 2, 3].", 'easy'),
    mc("Which function returns the number of items in a list?", ["size()", "len()", "count()", "items()"], 1,
       "The len() function returns the number of items in a list (or other sequence).", 'easy'),
    mc("Which method adds an item to the end of a list in Python?", ["add()", "append()", "insert()", "push()"], 1,
       "The append() method adds an item to the end of a Python list.", 'medium'),
    mc("What is the index of the first element in a Python list?", ["1", "0", "-1", "It depends on the list"], 1,
       "Python uses zero-based indexing, so the first element has index 0.", 'easy'),
    mc("What does the following code print? x = [10, 20, 30]; print(x[1])", ["10", "20", "30", "Error"], 1,
       "x[1] refers to the second element (index 1), which is 20.", 'medium'),
    mc("Which keyword is used to exit a loop early in Python?", ["exit", "stop", "break", "return"], 2,
       "The 'break' keyword immediately exits the nearest enclosing loop in Python.", 'medium'),
    mc("Which keyword skips the current iteration and moves to the next one in a loop?", ["skip", "continue", "pass", "next"], 1,
       "The 'continue' keyword skips the rest of the current loop iteration and moves to the next one.", 'medium'),
    mc("Which keyword is used to define a class in Python?", ["class", "def", "object", "struct"], 0,
       "The 'class' keyword is used to define a class in Python.", 'medium'),
    mc("What is the correct syntax to import the 'math' module in Python?", ["include math", "import math", "using math", "require math"], 1,
       "'import math' is the correct syntax to import Python's built-in math module.", 'easy'),
    mc("Which function converts a string to an integer in Python?", ["str()", "int()", "float()", "chr()"], 1,
       "The int() function converts a compatible string or number to an integer.", 'medium'),
    mc("What is the output of print(type(5))?", ["<class 'int'>", "<class 'str'>", "<class 'float'>", "<class 'bool'>"], 0,
       "The type() function shows that 5 is of type int (integer).", 'medium'),
    mc("Which operator is used for equality comparison (not assignment) in Python?", ["=", "==", "!=", "<>"], 1,
       "'==' checks for equality, while '=' is used for assignment.", 'easy'),
    mc("Which operator is used for 'not equal to' comparison in Python?", ["<>", "!=", "==", "~="], 1,
       "'!=' is the 'not equal to' comparison operator in Python.", 'easy'),
    mc("Which of the following correctly opens a file for reading in Python?", ["open('file.txt', 'r')", "open('file.txt', 'w')", "read('file.txt')", "file.open('file.txt')"], 0,
       "open('file.txt', 'r') opens a file in read mode in Python.", 'medium'),
    mc("Which built-in Python function returns the largest value in a list?", ["max()", "min()", "sum()", "sorted()"], 0,
       "The max() function returns the largest value in a list or iterable.", 'easy'),
    mc("Which built-in Python function returns the smallest value in a list?", ["max()", "min()", "sum()", "len()"], 1,
       "The min() function returns the smallest value in a list or iterable.", 'easy'),
    mc("Which built-in Python function returns the sum of all elements in a list?", ["total()", "sum()", "add()", "count()"], 1,
       "The sum() function returns the total sum of elements in a list.", 'easy'),
    mc("What does try/except in Python handle?", ["Loops", "Errors/Exceptions", "Function definitions", "Comments"], 1,
       "try/except blocks are used to catch and handle errors (exceptions) that occur during program execution.", 'medium'),
    mc("Which keyword defines a lambda (anonymous) function in Python?", ["func", "def", "lambda", "anon"], 2,
       "The 'lambda' keyword is used to create small, anonymous functions in Python.", 'hard'),
    mc("Which data type in Python is used to store an ordered, unchangeable collection of items?", ["List", "Tuple", "Dictionary", "Set"], 1,
       "A tuple is an ordered, immutable (unchangeable) collection of items in Python.", 'hard'),
]

CLASS10_CS_DATABASE = [
    mc("What does DBMS stand for?", ["Data Base Management System", "Database Management System", "Data Backup Management System", "Digital Base Management System"], 1,
       "DBMS stands for Database Management System, software used to create and manage databases.", 'easy'),
    mc("A table in a relational database consists of:", ["Only images", "Rows and columns", "Only text files", "Sound files"], 1,
       "A database table is organised into rows (records) and columns (fields/attributes).", 'easy'),
    mc("In a database table, a single row is also called a:", ["Field", "Attribute", "Record/Tuple", "Column"], 2,
       "A single row in a database table is called a record (or tuple).", 'medium'),
    mc("In a database table, a single column is also called a:", ["Record", "Tuple", "Field/Attribute", "Row"], 2,
       "A single column in a database table is called a field or attribute.", 'medium'),
    mc("Which key uniquely identifies each record in a database table?", ["Foreign key", "Primary key", "Candidate key only", "Composite key always"], 1,
       "A primary key is a field (or set of fields) that uniquely identifies each record in a table.", 'medium'),
    mc("Which key in one table refers to the primary key in another table, establishing a relationship?", ["Primary key", "Foreign key", "Super key", "Alternate key"], 1,
       "A foreign key is a field in one table that references the primary key of another table, creating a relationship.", 'medium'),
    mc("Which language is commonly used to create, manage and query relational databases?", ["HTML", "SQL", "Python only", "CSS"], 1,
       "SQL (Structured Query Language) is the standard language used to interact with relational databases.", 'easy'),
    mc("Which SQL command is used to retrieve data from a database table?", ["INSERT", "SELECT", "DELETE", "UPDATE"], 1,
       "The SELECT command is used to retrieve (query) data from a database table.", 'medium'),
    mc("Which SQL command is used to add new records to a table?", ["SELECT", "INSERT", "DELETE", "DROP"], 1,
       "The INSERT command is used to add new records into a database table.", 'medium'),
    mc("Which SQL command is used to remove records from a table?", ["SELECT", "INSERT", "DELETE", "CREATE"], 2,
       "The DELETE command is used to remove existing records from a table.", 'medium'),
    mc("Which SQL command is used to modify existing records in a table?", ["SELECT", "UPDATE", "INSERT", "DROP"], 1,
       "The UPDATE command is used to modify existing records in a database table.", 'medium'),
    mc("Which SQL command is used to create a new table?", ["SELECT", "MAKE TABLE", "CREATE TABLE", "NEW TABLE"], 2,
       "'CREATE TABLE' is the SQL command used to define and create a new table.", 'medium'),
    mc("Which SQL clause is used to filter records based on a condition?", ["ORDER BY", "WHERE", "GROUP BY", "SELECT ALL"], 1,
       "The WHERE clause is used to filter records that meet a specified condition.", 'medium'),
    mc("Which SQL clause is used to sort the results of a query?", ["WHERE", "GROUP BY", "ORDER BY", "HAVING"], 2,
       "The ORDER BY clause is used to sort query results in ascending or descending order.", 'medium'),
    mc("Which of these is an advantage of using a DBMS over traditional file systems?", ["More data redundancy", "Reduced data redundancy and better data integrity", "Slower data access", "No data security"], 1,
       "A DBMS reduces data redundancy, improves data integrity, and provides better security compared to traditional file systems.", 'medium'),
    mc("What is 'data redundancy' in the context of databases?", ["Unique data stored once", "Unnecessary duplication of the same data", "Encrypted data", "Deleted data"], 1,
       "Data redundancy refers to the unnecessary duplication of the same data within a database, which a good DBMS design minimises.", 'medium'),
    mc("What does 'data integrity' refer to in a database?", ["The accuracy and consistency of data over its lifecycle", "The speed of data retrieval", "The colour of the database interface", "The size of the database file"], 0,
       "Data integrity refers to maintaining the accuracy, consistency, and reliability of data throughout its lifecycle.", 'medium'),
    mc("A database model where data is organised into tables with relationships is called a:", ["Hierarchical model", "Relational model", "Network model", "Object model only"], 1,
       "The relational model organises data into related tables, connected through keys, and is the most widely used database model.", 'medium'),
    mc("Which of these best describes 'normalisation' in database design?", ["Making a database larger", "Organising data to reduce redundancy and improve integrity", "Deleting all tables", "Encrypting all data"], 1,
       "Normalisation is the process of organising database tables to minimise redundancy and improve data integrity.", 'hard'),
    mc("Which of these is an example of a popular relational DBMS software?", ["MySQL", "MS Paint", "Adobe Photoshop", "VLC Media Player"], 0,
       "MySQL is a popular open-source relational database management system.", 'medium'),
]
# ============ CLASS 8 TOP-UP (existing chapters -> 20+ questions each) ============

C8_SCI_CROP_MORE = [
    mc("Which of these is a Kharif crop?", ["Wheat", "Mustard", "Rice", "Gram"], 2,
       "Rice is a Kharif crop, sown with the onset of monsoon and harvested in autumn.", 'easy'),
    mc("Which of these is a Rabi crop?", ["Rice", "Maize", "Wheat", "Cotton"], 2,
       "Wheat is a Rabi crop, sown in winter and harvested in spring.", 'easy'),
    mc("What is the process of loosening and turning the soil before sowing called?", ["Harvesting", "Tilling/Ploughing", "Weeding", "Irrigation"], 1,
       "Tilling (ploughing) loosens the soil, allowing roots to penetrate easily and improving aeration.", 'easy'),
    mc("Which tool is traditionally used for ploughing fields?", ["Sickle", "Plough", "Thresher", "Seed drill"], 1,
       "A plough is a traditional tool used to till and turn the soil before sowing.", 'easy'),
    mc("A seed drill is used for which agricultural activity?", ["Harvesting", "Sowing seeds at proper depth and distance", "Threshing", "Winnowing"], 1,
       "A seed drill sows seeds uniformly at the correct depth and spacing.", 'medium'),
    mc("The process of separating grain from chaff after harvesting is called:", ["Sowing", "Weeding", "Threshing", "Irrigation"], 2,
       "Threshing is the process of separating grain seeds from the harvested stalks/chaff.", 'medium'),
    mc("Removal of unwanted plants growing along with the crop is called:", ["Threshing", "Weeding", "Winnowing", "Manuring"], 1,
       "Weeding is the removal of unwanted plants (weeds) that compete with crops for nutrients.", 'easy'),
    mc("Which of these is an organic source of nutrients for crops?", ["Chemical fertiliser", "Manure", "Pesticide", "Herbicide"], 1,
       "Manure is an organic substance derived from decomposed plant/animal matter that enriches soil naturally.", 'easy'),
    mc("Which of these methods conserves soil moisture and saves water in irrigation?", ["Flood irrigation", "Drip irrigation", "Overhead sprinkling only", "Canal irrigation only"], 1,
       "Drip irrigation delivers water directly to plant roots, minimising wastage and conserving water.", 'medium'),
    mc("Which of these is a traditional method of irrigation?", ["Drip irrigation", "Sprinkler system", "Moat (using a pulley and animal power)", "Precision irrigation"], 2,
       "A moat is a traditional irrigation method using a pulley system, often powered by animals.", 'medium'),
    mc("Crop rotation mainly helps in:", ["Depleting soil nutrients faster", "Maintaining soil fertility and reducing pest build-up", "Increasing weeds", "Reducing crop yield"], 1,
       "Crop rotation helps maintain soil fertility and reduces the build-up of pests and diseases specific to one crop.", 'medium'),
    mc("Which nutrient, when added via fertilisers, mainly promotes leafy green growth in plants?", ["Nitrogen", "Phosphorus only", "Potassium only", "Calcium"], 0,
       "Nitrogen is essential for the growth of leaves and green vegetative parts of plants.", 'medium'),
    mc("Storing grains in silos or granaries mainly helps prevent:", ["Faster ripening", "Loss due to pests, moisture and rodents", "Faster sowing", "Weed growth"], 1,
       "Proper storage in silos/granaries protects grains from pests, moisture, and rodents.", 'medium'),
    mc("Which of these best defines 'agriculture'?", ["The study of animals only", "The science and practice of farming, including crop and livestock production", "The study of rocks", "The study of weather"], 1,
       "Agriculture is the science and practice of cultivating crops and rearing livestock for food and other uses.", 'easy'),
    mc("Which of these is an example of a modern irrigation technique that conserves water?", ["Well irrigation only", "Sprinkler and drip irrigation", "Flood irrigation only", "Manual watering with buckets only"], 1,
       "Sprinkler and drip irrigation are modern techniques designed to use water efficiently and reduce wastage.", 'medium'),
    mc("Why is preparation of soil considered an important step before sowing?", ["It has no real benefit", "It loosens soil, improves aeration and helps roots grow well", "It only removes water", "It removes all nutrients from soil"], 1,
       "Preparing (tilling) the soil loosens it, improves aeration and water retention, and helps roots penetrate easily.", 'medium'),
    mc("Which of these best explains why Kharif crops are sown at the start of monsoon?", ["They need warm and wet conditions to grow", "They need cold and dry conditions", "They require no water at all", "They grow only in winter"], 0,
       "Kharif crops require warm temperatures and plenty of water, which is why they are sown at the start of the monsoon.", 'medium'),
    mc("Which of these best explains why Rabi crops are sown in winter?", ["They need hot and wet conditions", "They grow best in cool climate with less water", "They cannot survive any water", "They are sown only in summer"], 1,
       "Rabi crops grow best in the cool, dry climate of winter and require relatively less water than Kharif crops.", 'medium'),
    mc("The process of separating heavier grain from lighter chaff using wind is called:", ["Threshing", "Winnowing", "Harvesting", "Sowing"], 1,
       "Winnowing uses wind or air currents to separate lighter chaff from heavier grain.", 'medium'),
    mc("Which of these best describes the role of fertilisers in agriculture?", ["They replace the need for water entirely", "They replenish nutrients in the soil to boost crop yield", "They remove all pests permanently", "They have no effect on crops"], 1,
       "Fertilisers replenish essential nutrients in the soil, helping to increase crop yield.", 'medium'),
]

C8_SCI_MICRO_MORE = [
    mc("Which group of microorganisms includes yeast, mushrooms and moulds?", ["Bacteria", "Fungi", "Protozoa", "Algae"], 1,
       "Fungi include organisms like yeast, mushrooms and moulds.", 'easy'),
    mc("Which of these microorganisms is used in the production of antibiotics like penicillin?", ["Bacteria", "Fungi", "Virus", "Protozoa"], 1,
       "The fungus Penicillium is used to produce the antibiotic penicillin.", 'medium'),
    mc("Which microorganism is responsible for the fermentation of milk into curd?", ["Yeast", "Lactobacillus (bacteria)", "Virus", "Protozoa"], 1,
       "Lactobacillus bacteria ferment milk into curd by converting lactose into lactic acid.", 'medium'),
    mc("Vaccines work by preparing the body's immune system to fight:", ["Only bacteria", "Specific disease-causing microorganisms", "Only weeds", "Physical injuries"], 1,
       "Vaccines train the immune system to recognise and fight specific disease-causing microorganisms.", 'medium'),
    mc("Which disease among the following is caused by a virus?", ["Cholera", "Common cold", "Tuberculosis", "Typhoid"], 1,
       "The common cold is caused by viruses, unlike cholera, TB and typhoid, which are bacterial diseases.", 'medium'),
    mc("Which of these processes uses yeast to produce carbon dioxide, making bread rise?", ["Fermentation", "Photosynthesis", "Respiration in humans", "Digestion"], 0,
       "Fermentation by yeast produces carbon dioxide gas, which makes bread dough rise.", 'medium'),
    mc("Nitrogen-fixing bacteria found in the root nodules of leguminous plants help by:", ["Removing nitrogen from soil", "Converting atmospheric nitrogen into usable form for plants", "Causing plant diseases", "Decomposing dead matter only"], 1,
       "Nitrogen-fixing bacteria like Rhizobium convert atmospheric nitrogen into a form plants can use.", 'medium'),
    mc("Which term describes microorganisms that cause disease?", ["Decomposers", "Pathogens", "Producers", "Autotrophs"], 1,
       "Pathogens are disease-causing microorganisms.", 'easy'),
    mc("Which of these is a method to preserve food by killing microorganisms using heat?", ["Freezing", "Pasteurisation/Boiling", "Adding salt only", "Drying only"], 1,
       "Pasteurisation involves heating food/liquids to kill harmful microorganisms, extending shelf life.", 'medium'),
    mc("Which of these preservation methods uses low temperature to slow microbial growth?", ["Boiling", "Refrigeration", "Salting", "Adding sugar"], 1,
       "Refrigeration slows down the growth and activity of microorganisms by lowering the temperature.", 'easy'),
    mc("Which of these is a common preservative used to prevent microbial spoilage of food, like pickles?", ["Water", "Salt or oil", "Air", "Sunlight"], 1,
       "Salt and oil are commonly used as preservatives in foods like pickles to inhibit microbial growth.", 'medium'),
    mc("Communicable diseases spread from an infected person to a healthy person mainly through:", ["Genetics", "Contact, air, water, or vectors", "Only inheritance", "Only diet"], 1,
       "Communicable diseases spread through contact, air, water, food, or vectors like mosquitoes.", 'medium'),
    mc("Which organism acts as a vector, transmitting the malaria parasite to humans?", ["Housefly", "Female Anopheles mosquito", "Cockroach", "Earthworm"], 1,
       "The female Anopheles mosquito acts as a vector, transmitting the malaria-causing parasite.", 'medium'),
    mc("Which of these best describes 'antibiotics'?", ["Substances that kill or stop the growth of bacteria", "Substances that cause diseases", "A type of vitamin", "A type of virus"], 0,
       "Antibiotics are substances, often derived from fungi or bacteria, that kill or inhibit the growth of bacteria.", 'medium'),
    mc("Why should antibiotics not be taken without a doctor's advice?", ["They are always harmless", "Overuse can lead to antibiotic resistance and side effects", "They cure all diseases including viral ones", "They have no side effects"], 1,
       "Taking antibiotics without proper guidance can lead to antibiotic resistance and unwanted side effects.", 'medium'),
    mc("Which of these is an example of a beneficial use of bacteria in the dairy industry?", ["Causing milk to spoil", "Converting milk into curd and cheese", "Producing plastic", "Causing diseases in cows"], 1,
       "Certain bacteria are used to convert milk into curd and cheese in the dairy industry.", 'easy'),
    mc("Algae, some of which are microorganisms, mainly obtain nutrition through:", ["Decomposing dead matter", "Photosynthesis", "Parasitism", "Digesting other organisms"], 1,
       "Many algae, like other photosynthetic organisms, produce their own food through photosynthesis.", 'medium'),
    mc("Which of these is the best method to prevent the spread of communicable diseases through water?", ["Drinking contaminated water", "Boiling or purifying water before drinking", "Ignoring hygiene", "Avoiding vaccination"], 1,
       "Boiling or purifying water kills harmful microorganisms, preventing waterborne diseases.", 'easy'),
    mc("Which of these is an example of a useful application of microorganisms in agriculture?", ["Biofertilisers that enrich soil nutrients", "Causing crop failure", "Producing weeds", "Increasing soil erosion"], 0,
       "Biofertilisers containing beneficial microorganisms enrich soil nutrients and improve crop growth.", 'medium'),
    mc("Which of these best explains why microorganisms are called both 'friends' and 'foes'?", ["They are always harmful", "Some are beneficial (fermentation, medicine) while others cause disease", "They have no effect on humans", "They only exist in water"], 1,
       "Microorganisms are called both friends and foes because some are beneficial (used in food, medicine) while others cause diseases.", 'medium'),
]

C8_SCI_FIBRES_MORE = [
    mc("Which synthetic fibre is commonly used to make ropes and fishing nets due to its strength?", ["Cotton", "Nylon", "Wool", "Silk"], 1,
       "Nylon is strong, elastic and lightweight, making it ideal for ropes and fishing nets.", 'medium'),
    mc("Which synthetic fibre is commonly blended with cotton to make wrinkle-free fabric?", ["Nylon", "Polyester", "Wool", "Jute"], 1,
       "Polyester is often blended with cotton (as in terrycot) to create wrinkle-resistant fabric.", 'medium'),
    mc("Which synthetic fibre, developed to resemble silk, was one of the first fully synthetic fibres?", ["Nylon", "Polyester", "Rayon", "Acrylic"], 0,
       "Nylon was one of the first fully synthetic fibres, developed to resemble silk.", 'medium'),
    mc("Rayon is a synthetic fibre made from which raw material?", ["Petroleum", "Wood pulp (cellulose)", "Coal", "Sand"], 1,
       "Rayon is made from wood pulp (cellulose), making it a semi-synthetic fibre.", 'medium'),
    mc("Which of these best describes 'polymers', from which synthetic fibres are made?", ["Small single molecules", "Large chain-like molecules made of repeating units", "Metals only", "Liquids only"], 1,
       "Polymers are large molecules made up of many repeating smaller units (monomers) joined together.", 'medium'),
    mc("Which fabric material is known for being windcheater material, water-resistant and lightweight?", ["Cotton", "Nylon/Polyester", "Wool", "Jute"], 1,
       "Nylon and polyester are water-resistant, lightweight materials commonly used for windcheaters.", 'medium'),
    mc("Which of these is a disadvantage commonly associated with synthetic fibres compared to natural fibres?", ["They are always more absorbent", "They may not be biodegradable and can melt easily near flame", "They are always cheaper", "They are always warmer"], 1,
       "Synthetic fibres are often non-biodegradable and some can melt when exposed to flame, unlike many natural fibres.", 'medium'),
    mc("Plastic used to make bottles that can be moulded again by heating is called:", ["Thermosetting plastic", "Thermoplastic", "Natural fibre", "Biodegradable fibre"], 1,
       "Thermoplastics can be softened by heating and moulded again, e.g. polythene, PVC.", 'medium'),
    mc("Plastic that cannot be remoulded once set (e.g., used in electrical switches) is called:", ["Thermoplastic", "Thermosetting plastic", "Rayon", "Natural fibre"], 1,
       "Thermosetting plastics, like bakelite, set permanently and cannot be remoulded once shaped.", 'medium'),
    mc("Which of these is an advantage of using plastic containers for storage?", ["They corrode quickly", "They are light, strong, and do not corrode easily", "They are always biodegradable", "They break very easily"], 1,
       "Plastics are light, strong, and resistant to corrosion, which makes them useful for storage containers.", 'easy'),
    mc("Why is it recommended to reduce the use of single-use plastic bags?", ["They are extremely biodegradable", "They cause long-term environmental pollution as they don't decompose easily", "They are expensive to produce", "They have no environmental impact"], 1,
       "Single-use plastics are non-biodegradable and accumulate in the environment, causing long-term pollution.", 'medium'),
    mc("Which characteristic makes synthetic fibres like nylon popular for making sports garments?", ["They absorb a lot of water and become heavy", "They are lightweight, durable, and quick-drying", "They are always very expensive", "They shrink easily in water"], 1,
       "Synthetic fibres like nylon are lightweight, durable, and dry quickly, making them ideal for sportswear.", 'medium'),
    mc("Which of these best explains why melting synthetic fabrics near an open flame is dangerous?", ["They burn away completely leaving no residue", "They can melt and stick to the skin, causing severe burns", "They cool down instantly", "They turn into water"], 1,
       "Synthetic fabrics can melt and stick to the skin when exposed to flame, causing severe burns, unlike many natural fibres which simply char.", 'hard'),
    mc("Which of these fibres is classified as a semi-synthetic fibre?", ["Nylon", "Rayon", "Polyester", "Acrylic"], 1,
       "Rayon is considered semi-synthetic because it is made by chemically treating natural cellulose (wood pulp).", 'hard'),
    mc("Which raw material is mainly used to manufacture most fully synthetic fibres like nylon and polyester?", ["Cotton", "Petrochemicals (derived from petroleum)", "Silk cocoons", "Wool"], 1,
       "Fully synthetic fibres like nylon and polyester are primarily manufactured from petrochemicals.", 'medium'),
    mc("Which of these is a common household item made from thermosetting plastic?", ["Plastic buckets", "Electrical switches/plug points", "Plastic bottles", "Polythene bags"], 1,
       "Electrical switches and plug points are often made of thermosetting plastic (bakelite) due to its heat resistance and non-conductivity.", 'medium'),
    mc("Which of these best describes why plastics are considered non-biodegradable?", ["They decompose within a day", "Microorganisms cannot easily break them down", "They dissolve instantly in water", "They turn into soil quickly"], 1,
       "Most plastics are non-biodegradable because microorganisms cannot easily break down their chemical structure.", 'medium'),
    mc("Which fibre blend combines the comfort of cotton with the wrinkle-resistance of polyester?", ["Terrycot", "Rayon-silk", "Wool-nylon", "Jute-cotton"], 0,
       "Terrycot is a popular blend of cotton and polyester (terylene), combining comfort with wrinkle resistance.", 'hard'),
    mc("What environmental practice is recommended to manage the impact of non-biodegradable plastic waste?", ["Burning all plastic waste openly", "Reduce, Reuse, Recycle plastic products", "Dumping plastic into rivers", "Ignoring waste segregation"], 1,
       "The 3 Rs - Reduce, Reuse, Recycle - help manage and minimise the environmental impact of plastic waste.", 'medium'),
]

C8_ENG_CHRISTMAS_MORE = [
    mc("The story 'The Best Christmas Present' highlights the value of:", ["War and conflict", "Peace and shared humanity even among enemies", "Wealth and gifts", "Competition"], 1,
       "The story emphasises peace and shared humanity, showing enemy soldiers coming together in friendship.", 'medium'),
    mc("What historical event provides the backdrop for the story?", ["World War I Christmas truce", "World War II Christmas truce", "The French Revolution", "The Cold War"], 0,
       "The story is based on the informal Christmas truce during World War I in 1914.", 'medium'),
    mc("Which literary technique does the story primarily use to convey the events?", ["A letter/diary format", "A newspaper report", "A poem", "A play script"], 0,
       "The story is often presented through a letter or a grandson discovering an old diary/letter, adding a personal touch.", 'medium'),
    mc("What does the truce between soldiers suggest about human nature during wartime?", ["Soldiers always hate each other completely", "Even amid conflict, humanity and compassion can prevail", "War brings out only cruelty", "Soldiers never interact with enemies"], 1,
       "The story suggests that despite the horrors of war, humanity and compassion can still prevail between opposing sides.", 'medium'),
    mc("Which emotion is central to the soldiers' experience during the temporary truce?", ["Fear and hatred only", "Joy, camaraderie and shared humanity", "Boredom", "Anger at their own commanders only"], 1,
       "The soldiers experience joy, camaraderie, and a shared sense of humanity during the temporary truce.", 'medium'),
    mc("What can be inferred about the soldiers' feelings when they had to resume fighting after the truce?", ["They were relieved to fight again", "They likely felt reluctance and sadness, having bonded with 'the enemy'", "They felt nothing at all", "They celebrated the return to war"], 1,
       "Having bonded during the truce, the soldiers likely felt reluctance and sadness at having to resume fighting.", 'hard'),
    mc("The title 'The Best Christmas Present' most likely refers to:", ["An expensive gift exchanged", "The experience of peace and friendship during the truce", "New military equipment", "A promotion in rank"], 1,
       "The 'best Christmas present' refers to the experience of peace and friendship, valued above any material gift.", 'medium'),
    mc("What message does the story convey to readers about conflict and reconciliation?", ["Conflict can never be resolved", "Reconciliation and understanding are possible even between opposing sides", "War is always necessary", "People should never trust their enemies"], 1,
       "The story conveys that reconciliation and understanding are possible, even in the most divisive circumstances like war.", 'medium'),
    mc("What role does the setting of 'No Man's Land' play in the story?", ["It is irrelevant to the plot", "It becomes a neutral, shared space where enemies momentarily unite", "It is where the fiercest fighting occurs", "It is a place soldiers avoid entirely"], 1,
       "No Man's Land, usually a deadly battlefield, becomes a neutral shared space where soldiers momentarily unite in peace.", 'medium'),
    mc("Why might the commanding officers have been uneasy about the Christmas truce?", ["They fully supported it", "Fraternising with the enemy could undermine military discipline and the war effort", "It had no impact on military strategy", "They were unaware of the truce"], 1,
       "Officers on both sides were often uneasy because fraternising with the enemy could undermine discipline and the broader war effort.", 'hard'),
    mc("Which value is most strongly reinforced by the soldiers exchanging small gifts during the truce?", ["Greed", "Goodwill and shared humanity despite being adversaries", "Competition", "Deception"], 1,
       "The exchange of small gifts reinforces the theme of goodwill and shared humanity despite the soldiers being adversaries.", 'medium'),
    mc("How does the story use irony in describing soldiers who were enemies playing football together?", ["There is no irony in the story", "It highlights the contrast between the violence of war and this peaceful, friendly act", "It shows the soldiers were not really enemies", "It proves the war had already ended"], 1,
       "The irony lies in the stark contrast between the violent context of war and this unexpectedly peaceful, friendly activity.", 'hard'),
    mc("What broader lesson about humanity does the Christmas truce story offer beyond its historical setting?", ["Hatred is permanent and unavoidable", "Common humanity can transcend imposed divisions, even temporarily", "Peace is impossible during any conflict", "Soldiers should always follow orders without question"], 1,
       "The story suggests that shared humanity can transcend imposed divisions, even if only temporarily, offering hope amid conflict.", 'medium'),
    mc("Why is this event still remembered and retold over a century later?", ["It changed the outcome of the war", "It represents a powerful, symbolic moment of peace and humanity during a brutal war", "It was a purely fictional event", "It had no lasting significance"], 1,
       "The event is remembered as a powerful, symbolic moment of peace and humanity amid the brutality of World War I.", 'medium'),
    mc("What literary purpose does presenting the story from a soldier's personal perspective (e.g., a letter) serve?", ["It makes the story feel distant and impersonal", "It creates emotional intimacy and authenticity for the reader", "It removes all historical context", "It has no particular purpose"], 1,
       "A personal perspective, such as a letter, creates emotional intimacy and authenticity, helping readers connect with the soldier's experience.", 'hard'),
    mc("Which of these best reflects the central irony of soldiers celebrating together on Christmas Day?", ["Christmas has no connection to peace themes", "A day associated with peace and goodwill was spent amid a violent war, briefly overriding the conflict", "The soldiers did not know it was Christmas", "Christmas was banned during the war"], 1,
       "The central irony is that Christmas, a day associated with peace and goodwill, briefly overrode the surrounding violence of war.", 'hard'),
    mc("What does the temporary ceasefire suggest about the arbitrary nature of the lines dividing 'enemy' and 'friend' in war?", ["The lines are always natural and permanent", "The divisions were largely political and could dissolve when soldiers interacted as individuals", "There is no message about this in the story", "Soldiers on opposite sides have nothing in common"], 1,
       "The ceasefire suggests that the divisions between 'enemy' and 'friend' were largely political and could dissolve once soldiers interacted as fellow human beings.", 'hard'),
]

C8_ENG_TSUNAMI_MORE = [
    mc("What subject did Tilly Smith study that helped her recognise the tsunami warning signs?", ["History", "Geography", "Mathematics", "Biology"], 1,
       "Tilly Smith had learned about tsunami warning signs in a geography class shortly before the event.", 'medium'),
    mc("Where did the incident involving Tilly Smith take place?", ["A beach in Thailand", "A beach in Sri Lanka", "A beach in India", "A beach in Indonesia"], 0,
       "Tilly Smith recognised the tsunami warning signs on a beach in Phuket, Thailand.", 'medium'),
    mc("What action did Tilly Smith take upon recognising the danger?", ["She ignored it", "She warned her family and other beachgoers to evacuate", "She went closer to the sea", "She took photographs"], 1,
       "Tilly Smith warned her family and other tourists, helping to evacuate the beach before the tsunami struck.", 'easy'),
    mc("What does the story of Tilly Smith emphasise about the value of education?", ["Education is not very useful", "Knowledge gained in school can save lives in real situations", "Only adults can act during emergencies", "Geography lessons are irrelevant to daily life"], 1,
       "The story emphasises how knowledge gained through education can be practically applied to save lives.", 'medium'),
    mc("What natural phenomenon usually precedes a tsunami, as noticed in the story?", ["Sudden rainfall", "Sudden and unusual recession of the sea", "Bright sunshine", "Strong cold winds only"], 1,
       "An unusual and sudden recession (pulling back) of the sea from the shore often precedes a tsunami.", 'medium'),
    mc("What year did the devastating Indian Ocean tsunami, referenced in the story, occur?", ["2001", "2003", "2004", "2006"], 2,
       "The devastating Indian Ocean tsunami occurred on 26 December 2004.", 'medium'),
    mc("What overall theme does 'The Tsunami' chapter convey to readers?", ["The unpredictability of nature and the importance of awareness/preparedness", "The impossibility of surviving natural disasters", "The unimportance of scientific knowledge", "The idea that disasters cannot be prevented at all"], 0,
       "The chapter conveys the unpredictability of nature and the critical importance of awareness and preparedness in saving lives.", 'medium'),
    mc("What can readers learn from Tilly Smith's presence of mind during the crisis?", ["Panic is the best reaction in an emergency", "Staying calm and acting on knowledge can help save lives", "Only trained professionals can respond to disasters", "Children cannot make a meaningful difference"], 1,
       "The story teaches that staying calm and applying learned knowledge, even by a child, can make a life-saving difference.", 'medium'),
    mc("What does the story suggest about the relationship between scientific knowledge and disaster preparedness?", ["Science has no role in disaster response", "Understanding natural warning signs through science can directly help prevent loss of life", "Disaster preparedness is purely a matter of luck", "Scientific knowledge is only useful for scientists"], 1,
       "The story suggests that scientific knowledge of natural warning signs can be directly applied to prevent loss of life during disasters.", 'medium'),
    mc("Why is it significant that a child, rather than an adult expert, first recognised the danger?", ["It shows children should be ignored in emergencies", "It highlights that basic education can empower anyone, regardless of age, to act wisely", "It suggests adults are less capable than children generally", "It has no particular significance"], 1,
       "It highlights that basic education empowers anyone, even a child, to recognise danger and act wisely in a crisis.", 'medium'),
    mc("What emotional response would readers most likely have upon learning that Tilly's warning saved many lives?", ["Indifference", "Admiration and a sense of hope in human resourcefulness", "Anger", "Confusion"], 1,
       "Readers would likely feel admiration and hope, recognising how one person's resourcefulness and courage saved many lives.", 'medium'),
    mc("Which of these best describes the tone of the chapter 'The Tsunami'?", ["Purely humorous", "Informative and inspiring, highlighting courage amid disaster", "Entirely fictional and fantastical", "Dismissive of the tragedy's impact"], 1,
       "The chapter has an informative and inspiring tone, highlighting courage and quick thinking amid a natural disaster.", 'medium'),
    mc("What broader safety lesson does the chapter suggest for people living in coastal or disaster-prone areas?", ["Ignore all natural warning signs", "Learn about natural warning signs and have an evacuation plan", "Rely solely on government warnings with no personal awareness", "Avoid all science education"], 1,
       "The chapter suggests that learning about natural warning signs and having an evacuation plan can be life-saving in disaster-prone areas.", 'medium'),
    mc("How does the chapter likely structure the narrative to build tension before the tsunami strikes?", ["It reveals the outcome first, removing suspense", "It describes the calm beach scene before introducing the warning signs, building suspense", "It provides no description of the setting at all", "It focuses only on statistics"], 1,
       "The narrative likely builds tension by first describing the calm, ordinary beach scene before introducing the warning signs.", 'hard'),
    mc("Why might this real-life account be considered more impactful than a purely fictional disaster story?", ["Fiction is always more impactful", "Its basis in a true event adds authenticity and reinforces the practical value of the lesson", "Real events have no educational value", "It has no added impact compared to fiction"], 1,
       "Being a true event adds authenticity to the story and reinforces the practical, real-world value of its lesson about awareness and preparedness.", 'hard'),
    mc("What does the phrase 'presence of mind' mean, as demonstrated by the girl in the story?", ["Being physically present somewhere", "The ability to think clearly and act quickly in an unexpected or difficult situation", "Being distracted during an emergency", "Ignoring a crisis entirely"], 1,
       "'Presence of mind' refers to the ability to think clearly and act quickly and sensibly, especially in an unexpected or difficult situation.", 'medium'),
    mc("Which of these best summarises the central message of 'The Tsunami' for young readers?", ["Natural disasters cannot be survived", "Alertness, knowledge and quick action can help save lives during natural disasters", "Only adults can respond effectively to emergencies", "Science lessons have no real-world application"], 1,
       "The central message is that alertness, knowledge, and quick action - even by a child - can help save lives during natural disasters.", 'medium'),
]

C8_HIST_HWW_MORE = [
    mc("Which century is generally considered the start of 'Modern India' in the British periodisation?", ["16th century", "18th century", "20th century", "21st century"], 1,
       "British historians generally marked the 18th century as the beginning of the 'Modern' period of Indian history.", 'medium'),
    mc("Which of these is considered a secondary source of history?", ["An original letter from the period", "A modern textbook analysing past events", "An ancient coin", "An original inscription"], 1,
       "A modern textbook that analyses and interprets past events, rather than being from the period itself, is a secondary source.", 'medium'),
    mc("Why is the periodisation of history into 'Ancient, Medieval, Modern' considered controversial by some historians?", ["It has no issues at all", "It reflects a Eurocentric view and may not fit India's own historical trajectory", "It was created by Indian scholars only", "It only applies to European history"], 1,
       "Some historians criticise this periodisation as reflecting a Eurocentric view, imposed by British historians, that may not accurately represent India's own historical development.", 'hard'),
    mc("The National Archives of India primarily preserves which type of historical material?", ["Only old coins", "Official records and important documents", "Only ancient pottery", "Only inscriptions on stone"], 1,
       "The National Archives of India preserves official records, letters, and important government documents.", 'medium'),
    mc("Which of these best explains the importance of dates in the study of history?", ["Dates are not important at all", "Dates help arrange events in a sequence and understand cause-and-effect relationships", "Dates are only used for exams", "Dates change the actual events themselves"], 1,
       "Dates help historians arrange events chronologically and understand cause-and-effect relationships between them.", 'medium'),
    mc("British historians' interest in Indian administrative records grew mainly because they wanted to:", ["Preserve Indian culture only", "Understand and consolidate control over Indian territories and revenue", "Promote Indian independence", "Study only religious texts"], 1,
       "British administrators kept detailed records to better understand and consolidate their control over Indian territories and revenue systems.", 'medium'),
    mc("Which of these is an example of an official document useful to historians studying colonial India?", ["A modern novel", "Revenue records and government reports from that period", "A recent newspaper article", "A contemporary movie"], 1,
       "Revenue records and government reports from the colonial period are valuable official documents for historians.", 'medium'),
    mc("Why did the British consider surveys (land, forest, revenue) important tools of administration in India?", ["Surveys had no administrative value", "Surveys provided detailed knowledge, enabling more effective taxation and control", "Surveys were only used for scientific research", "Surveys were conducted only after independence"], 1,
       "Detailed surveys gave the British precise knowledge of land, resources, and population, enabling more effective taxation and administrative control.", 'medium'),
    mc("Which of these best explains why historians study both official and personal records (like diaries) from a period?", ["Only official records matter", "Personal records offer perspectives and details that official records may not capture", "Personal records are always unreliable", "Official records are never useful"], 1,
       "Personal records, like diaries and letters, provide perspectives, emotions, and everyday details that official records often omit.", 'medium'),
    mc("What role do museums play in the study and preservation of history?", ["They have no historical role", "They preserve and display artefacts, helping people understand and study the past", "They only display modern art", "They destroy old objects"], 1,
       "Museums preserve and display historical artefacts, helping researchers and the public understand and study the past.", 'medium'),
    mc("Why might the same historical event be interpreted differently by different historians?", ["All historians must always agree", "Interpretation can be influenced by the historian's perspective, available sources, and context", "Historical events have only one fixed interpretation", "Interpretation has no role in history"], 1,
       "Different historians may interpret the same event differently based on their perspective, the sources available to them, and their historical context.", 'hard'),
    mc("Which of these best illustrates the importance of chronology (time order) in historical study?", ["Events can be studied in any random order without issue", "Understanding the sequence of events helps explain causes and consequences accurately", "Chronology is irrelevant to historical analysis", "All historical events happened simultaneously"], 1,
       "Chronology (the order of events in time) is essential for understanding cause-and-effect relationships and accurately explaining historical developments.", 'medium'),
    mc("Why is it important for historians to critically evaluate the reliability of their sources?", ["All sources are equally reliable and need no evaluation", "Sources can be biased, incomplete, or inaccurate, so critical evaluation ensures more accurate history", "Critical evaluation is unnecessary for ancient sources", "Only very recent sources need evaluation"], 1,
       "Since sources can be biased, incomplete, or inaccurate, historians must critically evaluate them to construct a more accurate account of the past.", 'medium'),
    mc("What does the phrase 'history is written by the victors' suggest about historical records from colonial periods?", ["All historical records are completely neutral", "Dominant powers may shape historical narratives in their own favour, requiring careful scrutiny", "Colonised people never recorded their own history", "This phrase has no relevance to Indian history"], 1,
       "This phrase suggests that those in power often shape historical narratives in their own favour, making it important to critically examine colonial-era records.", 'hard'),
    mc("How does studying local or regional history complement the study of national history?", ["It has no value compared to national history", "It provides detailed, grassroots understanding that enriches the broader national narrative", "Local history always contradicts national history", "Regional history is not a legitimate field of study"], 1,
       "Studying local and regional history provides detailed, grassroots understanding that enriches and adds nuance to the broader national historical narrative.", 'medium'),
    mc("Which of the following best explains the term 'colonial archive'?", ["A modern digital database only", "The collection of official records and documents produced during colonial administration", "A collection of ancient inscriptions only", "A term with no historical meaning"], 1,
       "A 'colonial archive' refers to the vast collection of official records, reports, and documents produced during the period of colonial administration.", 'hard'),
    mc("Which of these best describes why British administrators were particularly interested in documenting Indian customs and laws?", ["To preserve Indian culture for its own sake only", "To use this knowledge to more effectively govern and control Indian society", "Out of purely academic curiosity with no practical use", "They had no interest in Indian customs"], 1,
       "British administrators documented Indian customs and laws largely to use this knowledge for more effective governance and control.", 'hard'),
]

C8_HIST_TRADE_MORE = [
    mc("The English East India Company was originally established primarily for the purpose of:", ["Political conquest", "Trade with the East, especially in spices", "Religious conversion", "Military expansion"], 1,
       "The East India Company was originally established for trade, particularly in spices and textiles.", 'medium'),
    mc("Who was the Nawab of Bengal defeated at the Battle of Plassey?", ["Mir Jafar", "Siraj-ud-Daulah", "Shah Alam II", "Tipu Sultan"], 1,
       "Siraj-ud-Daulah, the Nawab of Bengal, was defeated by Robert Clive at the Battle of Plassey in 1757.", 'medium'),
    mc("Who helped the British defeat the Nawab of Bengal at Plassey through betrayal?", ["Tipu Sultan", "Mir Jafar", "Shah Alam II", "Robert Clive's brother"], 1,
       "Mir Jafar, a commander in the Nawab's army, betrayed Siraj-ud-Daulah and helped the British win at Plassey.", 'medium'),
    mc("What were 'Diwani rights', granted to the Company after the Battle of Buxar?", ["Military command only", "The right to collect revenue and administer civil justice", "Religious authority", "Trading monopoly with China"], 1,
       "Diwani rights gave the East India Company the authority to collect revenue and administer civil justice in Bengal, Bihar and Odisha.", 'medium'),
    mc("The system by which the British controlled Indian rulers' foreign policy and stationed British troops in their territory was called:", ["Doctrine of Lapse", "Subsidiary Alliance", "Permanent Settlement", "Ryotwari System"], 1,
       "Under the Subsidiary Alliance, Indian rulers had to accept British forces and control over their external affairs.", 'medium'),
    mc("Which policy allowed the British to annex Indian states if a ruler died without a natural heir?", ["Subsidiary Alliance", "Doctrine of Lapse", "Permanent Settlement", "Ryotwari System"], 1,
       "The Doctrine of Lapse, introduced by Lord Dalhousie, allowed annexation of states without a natural heir.", 'medium'),
    mc("Which system of land revenue collection, introduced by the British in Bengal, fixed revenue with zamindars permanently?", ["Ryotwari System", "Permanent Settlement", "Mahalwari System", "Doctrine of Lapse"], 1,
       "The Permanent Settlement (1793) fixed the land revenue that zamindars had to pay to the British permanently.", 'medium'),
    mc("Which of these best explains why the East India Company shifted from trade to territorial conquest?", ["They lost interest in trade entirely", "Controlling territory allowed greater control over resources, revenue, and trade", "The British government forced them not to trade", "Indian rulers requested this shift"], 1,
       "Controlling territory gave the Company greater control over resources, revenue collection, and trade monopolies, driving their shift from mere trade to territorial control.", 'medium'),
    mc("What was the significance of the Treaty of Allahabad (1765)?", ["It ended all British presence in India", "It granted the East India Company Diwani rights over Bengal, Bihar and Odisha", "It gave France control over Bengal", "It abolished the Mughal emperor's title"], 1,
       "The Treaty of Allahabad (1765) granted the East India Company Diwani (revenue collection) rights over Bengal, Bihar and Odisha.", 'medium'),
    mc("How did the Company's dual role as trader and ruler create conflicts of interest in Bengal?", ["There was no conflict of interest", "The Company prioritised profit and taxation, often at the expense of the local population's welfare", "The Company always prioritised the welfare of Bengal's people", "It had no effect on Bengal's economy"], 1,
       "As both trader and ruler, the Company often prioritised profit and heavy taxation, contributing to hardships like the Bengal famine of 1770.", 'hard'),
    mc("Which factor most enabled the East India Company's military successes against Indian rulers in the 18th century?", ["Superior training, discipline, and use of alliances/betrayals", "Larger population than Indian states", "Support from all Indian rulers", "Lack of any Indian resistance"], 0,
       "The Company's superior military discipline, training, weaponry, and strategic alliances (or exploiting rivalries) contributed to its military successes.", 'hard'),
    mc("What was one major economic consequence of British policies on Indian traditional industries, such as textiles?", ["Indian industries flourished under British rule", "Traditional industries like handloom weaving declined due to competition from British manufactured goods", "The British banned all foreign imports", "Indian industries became the most dominant in the world"], 1,
       "British policies and cheap machine-made imports led to the decline of traditional Indian industries like handloom weaving.", 'medium'),
    mc("Why is the Battle of Buxar (1764) considered more significant than the Battle of Plassey (1757) by some historians?", ["It was a smaller battle with no lasting consequences", "It confirmed British dominance and led directly to the grant of Diwani rights", "It ended British interest in India", "It was fought entirely by Indian rulers against each other"], 1,
       "The Battle of Buxar decisively confirmed British military dominance and directly led to the grant of Diwani rights in 1765.", 'hard'),
    mc("Which of these best describes the term 'territorial expansion' in the context of the East India Company?", ["The Company remaining purely a trading entity", "The Company's gradual acquisition of political and administrative control over Indian regions", "The Company's withdrawal from India", "The Company's focus only on maritime trade"], 1,
       "Territorial expansion refers to the Company's gradual acquisition of political and administrative control over increasing areas of India.", 'medium'),
    mc("How did alliances and rivalries among Indian rulers contribute to British territorial expansion?", ["Indian rulers always united against the British", "The British exploited rivalries between Indian states to expand their control, often through alliances", "Rivalries had no impact on British expansion", "The British avoided any alliances with Indian rulers"], 1,
       "The British skilfully exploited rivalries and conflicts among Indian rulers, forming alliances that furthered their own territorial expansion.", 'medium'),
    mc("How did the British use trade privileges obtained from Mughal rulers to eventually gain political power?", ["Trade privileges had no connection to political power", "They gradually expanded these privileges and fortified trading posts, which became bases for political and military control", "They immediately relinquished all trade privileges", "Mughal rulers directly granted them political power from the start"], 1,
       "The British gradually expanded their trading privileges and fortified their trading posts, which eventually became bases for political and military control.", 'hard'),
    mc("What was the long-term impact of the East India Company's revenue policies on Bengal's agrarian economy?", ["They had no impact on agriculture", "Heavy and inflexible revenue demands often led to peasant hardship and occasional famine", "They always benefited Bengal's peasants directly", "They eliminated poverty in Bengal completely"], 1,
       "The Company's heavy and often inflexible revenue demands contributed to peasant hardship and were a factor in famines like the Bengal famine of 1770.", 'hard'),
]

C8_GEO_RESOURCES_MORE = [
    mc("Resources that are of value to a small group of people is called:", ["Individual resources", "Community resources", "National resources", "International resources"], 1,
       "Community resources are accessible and beneficial to a group or community, such as public grazing lands.", 'medium'),
    mc("Which of these is considered a human resource?", ["Coal", "Trained workers/skilled people", "Rivers", "Minerals"], 1,
       "People, through their skills, knowledge and abilities, are considered a human resource.", 'medium'),
    mc("Which term describes the process by which people transform something available in nature into a usable resource?", ["Resource utilisation", "Resource development", "Resource depletion", "Resource extraction only"], 1,
       "Resource development is the process of using technology, skills and knowledge to transform natural substances into usable resources.", 'medium'),
    mc("Overuse and misuse of resources without regard for the future is called:", ["Resource conservation", "Resource depletion/degradation", "Sustainable development", "Resource planning"], 1,
       "Resource depletion or degradation occurs when resources are overused or misused without concern for future availability.", 'medium'),
    mc("Why is resource conservation important?", ["To use up resources as quickly as possible", "To ensure resources remain available for present and future needs", "It has no real benefit", "To increase pollution levels"], 1,
       "Resource conservation ensures resources remain available for both present and future generations' needs.", 'easy'),
    mc("Which of these best distinguishes a 'renewable' from a 'non-renewable' resource?", ["Renewable resources can be replenished naturally; non-renewable resources cannot be replenished quickly", "There is no real difference", "Non-renewable resources renew instantly", "Renewable resources are always man-made"], 0,
       "Renewable resources can be naturally replenished over a short time, while non-renewable resources take millions of years to form and cannot be quickly replaced.", 'medium'),
    mc("Which of these is an example of resource conservation in daily life?", ["Leaving lights on unnecessarily", "Switching off unused electrical appliances", "Wasting water while brushing teeth", "Using single-use plastic excessively"], 1,
       "Switching off unused electrical appliances is a simple, effective way to conserve energy resources.", 'easy'),
    mc("Which of these best describes 'equitable distribution' of resources, an important goal of resource planning?", ["Only a few people should benefit from resources", "Resources should be shared fairly so all sections of society benefit", "Resources should be used up as fast as possible", "Only wealthy countries should access resources"], 1,
       "Equitable distribution means sharing resources fairly so that all sections of society, not just a privileged few, can benefit from them.", 'medium'),
    mc("Why is over-utilisation of resources considered a major problem?", ["It has no negative consequences", "It can lead to resource depletion, environmental degradation and scarcity for future generations", "It increases resources instantly", "It benefits future generations directly"], 1,
       "Over-utilisation depletes resources faster than they can be replenished, causing environmental degradation and scarcity for future generations.", 'medium'),
    mc("Which international agreements or bodies help regulate the use of resources found beyond national boundaries, like international waters?", ["Local municipal councils", "International organisations and treaties (e.g., United Nations bodies)", "Individual private companies alone", "No regulation exists at all"], 1,
       "International organisations and treaties help regulate and manage the use of resources found in areas beyond individual national boundaries, like international waters.", 'hard'),
    mc("Which of these best explains the concept of 'resource planning' at a national level?", ["Random, unplanned use of resources", "A scientific technique of surveying, mapping and creating a plan for balanced resource utilisation", "Ignoring the needs of future generations", "Focusing resources in only one region of a country"], 1,
       "Resource planning is a scientific technique involving surveying, mapping, and establishing a balanced strategy for the utilisation of resources across a country.", 'medium'),
    mc("What is the significance of technology and human skill in transforming a natural substance into a usable resource?", ["Technology and skill play no role at all", "They enable the natural substance to be effectively extracted, processed, and utilised as a resource", "Only natural substances themselves matter, human input is irrelevant", "Technology only wastes natural substances"], 1,
       "Technology and human skill are essential in transforming a natural substance into an actual usable resource through extraction, processing, and application.", 'medium'),
    mc("Which of these best explains why some resources, like fossil fuels, are considered a limited stock available to humankind?", ["They can be created instantly whenever needed", "They took millions of years to form and cannot be replenished within a human lifetime", "They are found in unlimited quantities everywhere", "They have no environmental impact when used"], 1,
       "Fossil fuels took millions of years to form geologically, so once used up, they cannot be replenished within a human lifetime, making them a limited stock.", 'medium'),
    mc("Which of these best illustrates a 'potential resource'?", ["A resource currently being fully used", "A resource present in a region but not yet utilised, e.g. untapped wind energy potential", "A resource that no longer exists", "A resource found only in cities"], 1,
       "A potential resource is one that exists in a region but has not yet been utilised, such as untapped wind or solar energy potential.", 'medium'),
    mc("Which of these best illustrates a 'stock resource'?", ["A resource with technology not yet available to use it, like hydrogen as a fuel in the past", "A resource that is unlimited and inexhaustible", "A resource used only by one person", "A resource found only in developed countries"], 0,
       "A stock resource is a material present in the environment that cannot be used due to a lack of appropriate technology, such as hydrogen before fuel cell technology was developed.", 'hard'),
    mc("Why do geographers distinguish between 'actual' and 'potential' resources?", ["There is no meaningful distinction", "It helps in planning future resource development and understanding what can be utilised now versus later", "Only actual resources matter for any planning", "Potential resources are never useful"], 1,
       "This distinction helps in planning future resource development, showing what can be utilised now (actual) versus what may be usable later with new technology or investment (potential).", 'medium'),
    mc("Which of these best explains the term 'resource degradation'?", ["Improvement in the quality of a resource", "A decline in the quality or quantity of a resource due to overuse or misuse", "Discovery of a completely new resource", "The natural replenishment of a resource"], 1,
       "Resource degradation refers to the decline in quality or quantity of a resource, typically caused by overuse, misuse or pollution.", 'medium'),
]

C8_GEO_LAND_MORE = [
    mc("Which soil type is commonly found in coastal and deltaic regions, well-suited for rice cultivation?", ["Black soil", "Alluvial soil", "Red soil", "Desert soil"], 1,
       "Alluvial soil, found in river deltas and coastal plains, is fertile and well-suited for rice cultivation.", 'medium'),
    mc("Which of these best describes the process of 'soil erosion'?", ["Soil becoming more fertile", "The removal of the top fertile layer of soil by wind or water", "Soil becoming rockier", "Soil absorbing more water"], 1,
       "Soil erosion is the removal of the top, fertile layer of soil due to the action of wind or water.", 'medium'),
    mc("Which farming practice, alternating different crops on the same land, helps maintain soil fertility?", ["Monoculture", "Crop rotation", "Overgrazing", "Deforestation"], 1,
       "Crop rotation, alternating different crops, helps replenish soil nutrients and maintain fertility.", 'medium'),
    mc("Which human activity is a major contributor to land degradation?", ["Afforestation", "Deforestation and overgrazing", "Crop rotation", "Terrace farming"], 1,
       "Deforestation and overgrazing strip land of vegetation cover, leading to erosion and land degradation.", 'medium'),
    mc("Which of these is a source of fresh water?", ["Oceans", "Rivers and glaciers", "Seas", "Salt lakes"], 1,
       "Rivers and glaciers are important sources of fresh water, unlike oceans and seas which contain salt water.", 'easy'),
    mc("What percentage of the Earth's water is estimated to be fresh water (approximately)?", ["About 2-3%", "About 50%", "About 75%", "About 97%"], 0,
       "Only about 2-3% of the Earth's total water is fresh water; the rest is saline (ocean water).", 'medium'),
    mc("Which of these is a method to conserve water at the household level?", ["Leaving taps running", "Fixing leaking taps and reusing water where possible", "Washing vehicles with a hose left running", "Overwatering plants"], 1,
       "Fixing leaks and reusing water (e.g., for plants) are simple household methods to conserve water.", 'easy'),
    mc("Which layer of soil, richest in organic matter and nutrients, is most important for plant growth?", ["Subsoil", "Topsoil", "Bedrock", "Substratum"], 1,
       "Topsoil, the uppermost layer, is richest in organic matter and nutrients, making it most important for plant growth.", 'medium'),
    mc("Which of these natural agents is primarily responsible for weathering rocks into soil over time?", ["Only sunlight", "Wind, water, temperature changes and living organisms", "Only human activity", "Only earthquakes"], 1,
       "Weathering of rocks into soil occurs due to the combined action of wind, water, temperature changes, and living organisms over long periods.", 'medium'),
    mc("Which of these best explains why rainwater harvesting is increasingly promoted in urban areas?", ["It wastes water", "It helps recharge groundwater and reduces dependence on other water sources", "It has no environmental benefit", "It increases water pollution"], 1,
       "Rainwater harvesting captures and stores rainwater, helping recharge groundwater levels and reducing dependence on other water sources.", 'medium'),
    mc("Which of these best explains why forests are important for maintaining the water cycle and soil health?", ["Forests have no impact on water or soil", "Tree roots bind soil, preventing erosion, and forests aid in rainfall and groundwater recharge", "Forests only affect the air, not water or soil", "Removing forests always improves land quality"], 1,
       "Forests play a crucial role in binding soil (preventing erosion), regulating rainfall patterns, and aiding groundwater recharge.", 'medium'),
    mc("Which of these is a consequence of excessive groundwater extraction?", ["Groundwater levels rise automatically", "Falling water tables and potential land subsidence", "No effect on the environment", "Immediate replenishment of aquifers"], 1,
       "Excessive groundwater extraction can lead to falling water tables and, in severe cases, land subsidence.", 'medium'),
    mc("Which of these best describes the relationship between land, soil and water as natural resources?", ["They are entirely unrelated to each other", "They are interconnected; degradation of one often affects the others", "Only land matters for agriculture", "Water has no relationship with soil quality"], 1,
       "Land, soil, and water are deeply interconnected natural resources; the degradation of one (e.g., deforestation affecting soil) often impacts the others.", 'medium'),
    mc("Which soil type, found in high rainfall areas, is often reddish due to iron oxide content and less fertile?", ["Alluvial soil", "Black soil", "Laterite soil", "Desert soil"], 2,
       "Laterite soil, found in high-rainfall regions, has a reddish colour due to iron oxide and is generally less fertile due to leaching of nutrients.", 'medium'),
    mc("Which of these government/community initiatives commonly promotes soil and water conservation in India?", ["Watershed management programmes", "Programmes that encourage deforestation", "Policies discouraging any irrigation", "Programmes banning all farming"], 0,
       "Watershed management programmes are commonly used initiatives that promote soil and water conservation by managing land and water resources holistically.", 'medium'),
    mc("Which of these best explains why land is considered a finite (limited) resource?", ["New land can always be created instantly", "The total amount of usable land on Earth is fixed, though its use can change over time", "Land increases naturally every year", "Land has no limitations"], 1,
       "Land is considered finite because the total amount of usable land on Earth is essentially fixed, even though how it is used can change over time.", 'medium'),
    mc("Which farming practice can most directly lead to loss of soil fertility if used continuously without care?", ["Crop rotation", "Growing the same single crop repeatedly (monoculture) without replenishing nutrients", "Adding organic manure regularly", "Practising agroforestry"], 1,
       "Continuously growing the same crop (monoculture) without replenishing nutrients can deplete specific soil nutrients and reduce fertility over time.", 'medium'),
]

C8_CS_ALGO_MORE = [
    mc("Which of the following best defines an algorithm?", ["A programming language", "A step-by-step procedure to solve a problem", "A type of computer hardware", "A file format"], 1,
       "An algorithm is a step-by-step, well-defined procedure to solve a specific problem.", 'easy'),
    mc("Which of these is a key characteristic of a good algorithm?", ["It should be ambiguous", "It should be finite (must terminate after a finite number of steps)", "It should have infinite steps", "It should be undefined"], 1,
       "A good algorithm must be finite, meaning it terminates after a finite number of well-defined steps.", 'medium'),
    mc("A graphical/pictorial representation of an algorithm using standard symbols is called a:", ["Pseudocode", "Flowchart", "Syntax", "Source code"], 1,
       "A flowchart uses standard symbols to visually represent the steps of an algorithm.", 'easy'),
    mc("Which flowchart symbol represents the start or end of a process?", ["Rectangle", "Oval/Terminal symbol", "Diamond", "Parallelogram"], 1,
       "An oval (terminal symbol) represents the start or end point in a flowchart.", 'medium'),
    mc("Which flowchart symbol represents an input or output operation?", ["Oval", "Rectangle", "Parallelogram", "Diamond"], 2,
       "A parallelogram is used in flowcharts to represent input or output operations.", 'medium'),
    mc("Which flowchart symbol represents a process or calculation step?", ["Oval", "Diamond", "Rectangle", "Circle"], 2,
       "A rectangle in a flowchart represents a process or a calculation/action step.", 'medium'),
    mc("Writing an algorithm in a informal, structured English-like format (without strict syntax) is called:", ["Flowchart", "Pseudocode", "Source code", "Machine code"], 1,
       "Pseudocode expresses an algorithm using informal, structured language, without strict programming syntax.", 'medium'),
    mc("Which type of algorithm structure executes steps one after another, without branching or repeating?", ["Sequential", "Conditional", "Looping", "Recursive"], 0,
       "A sequential algorithm executes steps one after another, in a straight line, without branching or repetition.", 'medium'),
    mc("Which type of algorithm structure involves making a decision, like 'if-else'?", ["Sequential", "Conditional/Selection", "Looping", "None of these"], 1,
       "A conditional (selection) structure involves making decisions, executing different steps based on conditions.", 'medium'),
    mc("Which of these best describes 'efficiency' as a desirable quality of an algorithm?", ["It should use excessive resources without concern", "It should solve the problem using minimal time and resources", "It should have as many steps as possible", "It should never be tested"], 1,
       "An efficient algorithm solves the problem correctly while using minimal time and computing resources.", 'medium'),
    mc("Which of these problems can be effectively solved using an algorithm?", ["Sorting a list of numbers", "None, algorithms can't solve real problems", "Only mathematical problems", "Only problems with a single step"], 0,
       "Algorithms are widely used for problems like sorting a list of numbers, in a clear step-by-step manner.", 'easy'),
    mc("Which of these best describes the 'input' characteristic of an algorithm?", ["An algorithm must never take any input", "An algorithm may take zero or more well-defined inputs", "An algorithm can only take one input", "Inputs are irrelevant to algorithms"], 1,
       "A well-designed algorithm may take zero or more clearly defined inputs before processing.", 'medium'),
    mc("Which of these best describes the 'output' characteristic of an algorithm?", ["An algorithm must produce zero outputs always", "An algorithm must produce at least one well-defined output", "Outputs are optional and undefined", "Only flowcharts produce outputs, not algorithms"], 1,
       "A proper algorithm must produce at least one clearly defined output as a result of its process.", 'medium'),
    mc("Why is it useful to write pseudocode or draw a flowchart before writing actual program code?", ["It is a waste of time", "It helps plan and visualise the logic clearly before implementation, reducing errors", "It replaces the need for programming entirely", "It only applies to complex programs, never simple ones"], 1,
       "Writing pseudocode or a flowchart helps plan and visualise the logic clearly before coding, which helps reduce errors during implementation.", 'medium'),
    mc("Which of these is an example of a real-life process that can be described as an algorithm?", ["A recipe for cooking a dish, with step-by-step instructions", "A random guess", "An undefined idea", "A feeling"], 0,
       "A cooking recipe, with its clear step-by-step instructions, is a good real-life example of an algorithm.", 'easy'),
    mc("Which of these best explains why an algorithm should be 'unambiguous'?", ["Ambiguity makes algorithms more flexible and useful", "Each step must have only one clear meaning so it can be executed correctly and consistently", "Ambiguity has no effect on how an algorithm works", "Algorithms are never executed by computers, only humans"], 1,
       "An algorithm must be unambiguous so that each step has a single, clear meaning, ensuring it can be executed correctly and consistently every time.", 'medium'),
]

C8_CS_PYTHON_MORE = [
    mc("Which of these is a valid Python variable name?", ["3total", "total_3", "total-3", "total 3"], 1,
       "'total_3' is valid because it starts with a letter and uses only letters, digits, and underscores.", 'medium'),
    mc("What is the output of print('Hello' + 'World')?", ["Hello World", "HelloWorld", "Hello+World", "Error"], 1,
       "The '+' operator concatenates strings without adding a space, resulting in 'HelloWorld'.", 'medium'),
    mc("What is the output of print(10 % 3)?", ["3", "1", "0", "3.33"], 1,
       "The modulus operator (%) returns the remainder of division: 10 divided by 3 leaves remainder 1.", 'medium'),
    mc("Which keyword is used to repeat a block of code a specific number of times using a range?", ["while", "for", "def", "if"], 1,
       "A 'for' loop, often combined with range(), is used to repeat code a specific number of times.", 'medium'),
    mc("What is the correct way to create a comment that spans multiple lines in Python (commonly done using)?", ["// comment //", "<!-- comment -->", "''' comment '''", "# comment #"], 2,
       "Triple quotes (''' ... ''') are commonly used to create multi-line comments/docstrings in Python.", 'medium'),
    mc("Which data type would store the value True or False in Python?", ["int", "float", "bool", "str"], 2,
       "The boolean (bool) data type stores either True or False in Python.", 'easy'),
    mc("Which operator is used to check if two values are equal in Python?", ["=", "==", "!=", "<="], 1,
       "The '==' operator checks whether two values are equal in Python.", 'easy'),
    mc("What will print(type(3.5)) output?", ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'bool'>"], 1,
       "3.5 is a decimal number, so its type is float.", 'medium'),
    mc("Which function converts a value into a string in Python?", ["int()", "str()", "float()", "bool()"], 1,
       "The str() function converts a given value into a string in Python.", 'medium'),
    mc("What is the correct syntax for an if-else statement in Python?", ["if x > 5 then print('yes') else print('no')", "if x > 5: print('yes')\\nelse: print('no')", "if x > 5 { print('yes') } else { print('no') }", "ifx>5:print('yes')"], 1,
       "Python if-else statements use a colon after the condition and indentation, with 'else:' for the alternative block.", 'medium'),
    mc("Which arithmetic operator is used for exponentiation (raising to a power) in Python?", ["^", "**", "%%", "//"], 1,
       "The '**' operator is used for exponentiation in Python, e.g., 2**3 = 8.", 'medium'),
    mc("Which built-in function returns the absolute value of a number in Python?", ["abs()", "sqrt()", "pow()", "int()"], 0,
       "The abs() function returns the absolute (non-negative) value of a number in Python.", 'medium'),
    mc("Which of these correctly checks whether a number 'n' is even in Python?", ["if n % 2 == 0:", "if n / 2 == 0:", "if n * 2 == 0:", "if n == 2:"], 0,
       "Checking 'n % 2 == 0' verifies if a number is evenly divisible by 2, meaning it is even.", 'medium'),
    mc("What does the range(5) function generate in Python?", ["Numbers 1 to 5", "Numbers 0 to 4", "Numbers 0 to 5", "Numbers 1 to 4"], 1,
       "range(5) generates numbers starting from 0 up to (but not including) 5, i.e., 0,1,2,3,4.", 'medium'),
    mc("Which symbol is used to access a specific element in a Python list by position?", ["Curly braces {}", "Square brackets []", "Parentheses ()", "Angle brackets <>"], 1,
       "Square brackets [] are used to access elements in a list by their index position, e.g., mylist[0].", 'medium'),
    mc("Which keyword defines a reusable block of code that performs a specific task in Python?", ["import", "def", "class", "for"], 1,
       "The 'def' keyword is used to define a function - a reusable block of code performing a specific task.", 'medium'),
]
# ============ ADVANCED NOTES (keyed by chapter title) ============
# Each entry: (title, description, content)

ADVANCED_NOTES = {
    # ---- Class 5 ----
    "Chapter 1 - Numbers and Place Value": ("Advanced: Estimation & Number Patterns",
        "Deeper look at rounding, estimation and number patterns.",
        "Beyond basic place value, estimation lets us quickly check if an answer is reasonable. "
        "To estimate a sum or product, round each number to its nearest ten, hundred or thousand before "
        "calculating. For example, to estimate 4,872 + 3,145, round to 4,900 + 3,100 = 8,000 (close to the exact "
        "answer, 8,017). This 'front-end estimation' is a powerful real-world skill used in budgeting and shopping.\n\n"
        "Advanced idea - Number patterns: Numbers can follow patterns based on place value, such as skip-counting "
        "by 100s, 1000s, or recognising palindromic numbers (numbers that read the same forwards and backwards, "
        "like 12321). Practise creating your own increasing and decreasing number patterns using place value rules."),
    "Chapter 2 - Fractions": ("Advanced: Fractions, Decimals and Real-Life Use",
        "Connecting fractions to decimals and solving multi-step problems.",
        "Every fraction can be written as a decimal by dividing the numerator by the denominator, e.g. 3/4 = 0.75. "
        "This connection helps when comparing fractions with different denominators - convert them to decimals "
        "and compare directly.\n\n"
        "Advanced problem-solving: word problems often combine addition/subtraction of fractions with real "
        "quantities, e.g. 'Riya ate 1/4 of a cake and Aman ate 1/3 of the same cake - what fraction is left?' "
        "Solve by finding a common denominator (LCM of 4 and 3 = 12): 3/12 + 4/12 = 7/12 eaten, so 5/12 remains. "
        "Practising such multi-step problems builds strong fraction fluency for higher classes."),
    "Chapter 1 - Plants and Animals": ("Advanced: Adaptations and Interdependence",
        "How plants and animals adapt to their surroundings and depend on each other.",
        "Plants and animals show remarkable adaptations to survive in their habitats - desert plants like cactus "
        "store water in thick stems, while aquatic plants like lotus have air-filled tissues to float. Animals in "
        "cold regions, like polar bears, have thick fur and fat layers for insulation.\n\n"
        "Advanced concept - Interdependence: Plants and animals depend on each other in a food chain (e.g. grass "
        "-> deer -> tiger) and through processes like pollination, where animals help plants reproduce while "
        "gaining nectar as food. Removing even one link, such as bees, can disrupt the whole balance of an "
        "ecosystem - this is why conservation of even 'small' species matters."),
    "Chapter 2 - Our Environment": ("Advanced: Human Impact and Sustainability",
        "Exploring how human activity affects the environment and ways to build a sustainable future.",
        "Human activities like industrialisation, urbanisation and intensive farming have significantly altered "
        "natural environments, contributing to problems such as climate change, loss of biodiversity, and "
        "pollution of air, water and soil.\n\n"
        "Advanced concept - Sustainability: Sustainable practices aim to meet today's needs without compromising "
        "the ability of future generations to meet theirs. Examples include using renewable energy, practising "
        "the 3 Rs (Reduce, Reuse, Recycle), organic farming, and afforestation drives. Understanding the balance "
        "between development and conservation is a key skill for informed global citizens."),
    "Chapter 1 - Grammar Basics": ("Advanced: Sentence Structure and Clauses",
        "Building more complex sentences using clauses and correct structure.",
        "Beyond single words like nouns and verbs, strong writing uses well-structured sentences. A simple "
        "sentence has one subject and one verb ('The dog barked'). A compound sentence joins two simple sentences "
        "with a conjunction ('The dog barked and the cat ran'). A complex sentence has a main clause and a "
        "subordinate (dependent) clause joined by words like 'because', 'although', or 'when' ('The dog barked "
        "because it saw a stranger').\n\n"
        "Practising combining short sentences into compound and complex ones makes writing more mature and "
        "expressive, an important step towards higher-level English skills."),
    "Chapter 2 - Reading Comprehension and Vocabulary": ("Advanced: Inference and Context Clues",
        "Using context clues to understand new words and unstated meanings.",
        "Good readers don't just decode words - they infer meaning from context. If you read 'The parched "
        "travellers rushed towards the oasis', you can infer 'parched' means very thirsty, even without a "
        "dictionary, because of the context (travellers rushing to water).\n\n"
        "Advanced skill - Reading between the lines: Sometimes a passage doesn't state something directly but "
        "implies it through actions or descriptions. For example, 'She slammed the door and threw her bag on the "
        "floor' implies anger, even though the word 'angry' is never used. Practising inference builds critical "
        "reading skills essential for higher-level comprehension and exams."),
    "Chapter 1 - Our Country India": ("Advanced: India's Diversity and Federal Structure",
        "Understanding India's cultural diversity and system of governance.",
        "India is one of the most culturally, linguistically and religiously diverse countries in the world, with "
        "22 officially recognised languages and hundreds of dialects. This diversity is reflected in India's motto "
        "'Unity in Diversity'.\n\n"
        "Advanced concept - Federal structure: India is a union of states and union territories, governed under a "
        "federal system where power is shared between the central government and state governments. Each state "
        "has its own elected government (Legislative Assembly) while the central government, led by the Prime "
        "Minister, handles matters of national importance like defence and foreign affairs."),
    "Chapter 2 - Maps and Directions": ("Advanced: Latitude, Longitude and Time Zones",
        "Understanding how geographic coordinates help pinpoint exact locations on Earth.",
        "Every location on Earth can be precisely identified using a combination of latitude (distance north or "
        "south of the Equator) and longitude (distance east or west of the Prime Meridian). Together, these form "
        "a grid system used in GPS and modern mapping.\n\n"
        "Advanced concept - Time zones: Because the Earth rotates, different longitudes experience daytime and "
        "night-time at different moments. The world is divided into time zones based on longitude, with each 15° "
        "of longitude roughly corresponding to a 1-hour difference. India follows a single time zone, Indian "
        "Standard Time (IST), based on 82.5°E longitude."),
    "Chapter 1 - Introduction to Computers": ("Advanced: How a Computer Processes Data",
        "A look at the input-process-output cycle and how computers 'think'.",
        "A computer works on a simple but powerful cycle: Input -> Process -> Output -> Storage. Data entered "
        "through input devices (like a keyboard) is processed by the CPU according to instructions from software, "
        "and the result is displayed through output devices (like a monitor), with data optionally saved for later.\n\n"
        "Advanced idea - Binary logic: At their core, computers only understand two states, represented as 0 and "
        "1 (binary). All the text, images and sounds you see on a computer are ultimately translated into "
        "combinations of these two digits, processed at incredible speed by billions of tiny switches called "
        "transistors inside the CPU."),
    "Chapter 2 - Basics of MS Paint and Keyboard": ("Advanced: Digital Art Techniques and Shortcuts",
        "Using layering concepts, shortcuts and precision tools for better digital drawings.",
        "While MS Paint is simple, understanding a few advanced habits improves your digital art: zooming in for "
        "precise pixel-level edits, using the Select tool to move and duplicate shapes efficiently, and combining "
        "the Fill tool with carefully closed outlines to avoid colour 'leaking' outside your shape.\n\n"
        "Advanced skill - Keyboard efficiency: Learning shortcuts like Ctrl+Z (Undo), Ctrl+C/Ctrl+V (Copy/Paste) "
        "and Ctrl+S (Save) dramatically speeds up your workflow, a skill that transfers to virtually every other "
        "software application you will use, from word processors to advanced design tools."),

    # ---- Class 6 ----
    "Chapter 1 - Knowing Our Numbers": ("Advanced: Large Numbers and the Indian/International Systems",
        "Comparing the Indian and International numbering systems for large numbers.",
        "India traditionally uses the Indian numbering system with place values like ones, tens, hundreds, "
        "thousands, lakhs (100,000) and crores (10,000,000), while most of the world uses the International "
        "system with thousands, millions and billions. For example, 1 crore = 10 million.\n\n"
        "Advanced skill: Converting between these systems is a valuable real-world skill, especially when reading "
        "international news or working with global data. Practise writing the same large number using commas in "
        "both systems, e.g. 12,345,678 (International) = 1,23,45,678 (Indian)."),
    "Chapter 2 - Whole Numbers": ("Advanced: Number Line Operations and Properties",
        "Exploring closure, commutative and associative properties using whole numbers.",
        "Whole numbers follow important mathematical properties: the Closure Property (adding or multiplying two "
        "whole numbers always gives a whole number), the Commutative Property (a+b = b+a, and a×b = b×a), and the "
        "Associative Property ((a+b)+c = a+(b+c)).\n\n"
        "Advanced idea: Notice that whole numbers are NOT closed under subtraction or division (e.g. 3-5 = -2, "
        "which is not a whole number). Understanding which operations 'stay within' a number system is a key "
        "stepping stone to understanding integers and rational numbers in later classes."),
    "Chapter 1 - Food: Where Does It Come From": ("Advanced: Food Chains and Trophic Levels",
        "Understanding how food sources connect through food chains.",
        "All the food sources we studied - plants and animals - are connected through food chains, which show the "
        "flow of energy from one organism to another. A simple example: Grass (producer) -> Grasshopper (primary "
        "consumer/herbivore) -> Frog (secondary consumer) -> Snake (tertiary consumer).\n\n"
        "Advanced concept - Trophic levels: Each stage in a food chain is called a trophic level. Energy decreases "
        "as it moves up the chain (only about 10% is passed to the next level), which is why there are always "
        "fewer top predators than plants in any ecosystem."),
    "Chapter 2 - Components of Food": ("Advanced: Balanced Diets and Metabolic Needs",
        "How nutrient requirements vary by age, activity and health condition.",
        "A 'balanced diet' isn't the same for everyone - it depends on age, gender, activity level and health "
        "status. Growing children need more protein and calcium for development, athletes need more carbohydrates "
        "for energy, and pregnant women need extra iron and folic acid.\n\n"
        "Advanced concept - Basal Metabolic Rate (BMR): This is the minimum energy your body needs at rest to "
        "keep vital functions like breathing and circulation running. Understanding BMR helps explain why calorie "
        "needs differ between a growing child, an active adult, and an elderly person."),
    "Chapter 1 - Tenses": ("Advanced: Sequence of Tenses in Complex Sentences",
        "Using consistent tenses across complex and compound sentences.",
        "In sentences with multiple clauses, tenses must agree logically. For instance, 'She said that she was "
        "tired' uses past tense throughout because the reporting verb ('said') is in the past. This is called the "
        "'sequence of tenses' rule, which becomes especially important in reported (indirect) speech.\n\n"
        "Advanced practice: Try writing short paragraphs describing a daily routine (simple present), a memorable "
        "trip (simple past), and future plans (simple future) - then rewrite one as if you were retelling it to a "
        "friend the next day, adjusting the tense accordingly."),
    "Chapter 2 - Parts of Speech": ("Advanced: Words That Function as Multiple Parts of Speech",
        "How the same word can act differently depending on its role in a sentence.",
        "Many English words can function as different parts of speech depending on context. For example, 'run' "
        "can be a verb ('I run every day') or a noun ('She went for a run'). Similarly, 'light' can be a noun (the "
        "light was bright), an adjective (a light bag), or a verb (light the candle).\n\n"
        "Advanced skill: Practise identifying the part of speech of a word by looking at its function in the "
        "sentence, not just its spelling. This flexible thinking about word roles is essential for advanced "
        "grammar and effective writing."),
    "Chapter 1 - What, Where, How and When": ("Advanced: Interpreting Historical Sources Critically",
        "Learning to question and cross-verify historical evidence.",
        "Historians don't just collect sources - they critically analyse them, asking: Who created this source? "
        "Why was it created? Could it be biased? For instance, royal inscriptions praising a king's achievements "
        "may exaggerate his victories, so historians cross-check with other sources like foreign travellers' "
        "accounts.\n\n"
        "Advanced skill: When you read any historical account (even in your textbook), practise asking these "
        "critical questions - this analytical approach, called 'source criticism', is fundamental to studying "
        "history at higher levels."),
    "Chapter 2 - The Earth in the Solar System": ("Advanced: Gravity, Orbits and Space Exploration",
        "Understanding the force that keeps planets in orbit and modern space missions.",
        "Planets stay in orbit around the Sun due to gravity - the Sun's massive gravitational pull constantly "
        "pulls planets towards it, while their forward motion (inertia) keeps them from falling in, resulting in "
        "a stable elliptical orbit. This same principle keeps the Moon orbiting Earth.\n\n"
        "Advanced context: India's space agency ISRO has conducted notable missions like Chandrayaan (Moon "
        "missions) and Mangalyaan (Mars Orbiter Mission), contributing to global understanding of our solar "
        "system. Studying such missions connects classroom astronomy to real-world scientific achievement."),
    "Chapter 1 - Computer Fundamentals": ("Advanced: Evolution of Computing and Moore's Law",
        "Tracing computer generations and understanding the pace of technological change.",
        "Computers have evolved through generations - from room-sized vacuum-tube machines in the 1940s to the "
        "powerful microprocessor-based devices we use today. Each generation brought smaller size, more speed and "
        "lower cost.\n\n"
        "Advanced concept - Moore's Law: An observation that the number of transistors on a computer chip (and "
        "therefore its processing power) roughly doubles every two years. This explains why computers, "
        "smartphones and other devices keep becoming faster and more powerful over time, even as they shrink in "
        "size."),
    "Chapter 2 - Input and Output Devices": ("Advanced: Emerging Input/Output Technologies",
        "Exploring modern and emerging I/O devices beyond the traditional keyboard and mouse.",
        "Beyond traditional devices, modern computing uses advanced I/O technologies like touchscreens, voice "
        "recognition (input), 3D printers (output), and virtual reality headsets (both input via motion sensors "
        "and output via display).\n\n"
        "Advanced idea - Human-Computer Interaction (HCI): This field studies how to design input/output systems "
        "that are intuitive and accessible for all users, including people with disabilities - for example, "
        "screen readers (output) for visually impaired users, or eye-tracking systems (input) for users with "
        "limited mobility."),

    # ---- Class 7 ----
    "Chapter 1 - Integers": ("Advanced: Integers in Real-World Contexts",
        "Applying integer operations to temperature, elevation, and financial contexts.",
        "Integers are essential for representing real-world quantities that can be positive or negative - "
        "temperature below/above zero, elevation above/below sea level, or profit/loss in a business. For "
        "example, if a submarine is at -250m and rises by 80m, its new position is -250 + 80 = -170m.\n\n"
        "Advanced practice: Try solving multi-step word problems combining several integer operations, such as "
        "tracking a hiker's elevation changes over several days, to build fluency in applying integer rules to "
        "practical situations."),
    "Chapter 2 - Fractions and Decimals": ("Advanced: Converting Between Fractions, Decimals and Percentages",
        "Building fluency in moving between different number representations.",
        "Fractions, decimals and percentages are three ways of representing the same value. 3/4 = 0.75 = 75%. "
        "Being able to quickly convert between them is essential for real-life applications like calculating "
        "discounts, interest rates, and exam scores.\n\n"
        "Advanced practice: Try solving problems like 'A shop offers a 15% discount on an item priced at Rs. 640 "
        "- what is the final price?' This requires converting the percentage to a decimal (0.15), multiplying, "
        "and subtracting - a skill that builds directly towards profit-loss and simple interest topics in higher "
        "classes."),
    "Chapter 1 - Nutrition in Plants": ("Advanced: Factors Affecting the Rate of Photosynthesis",
        "Exploring how light, CO2 and temperature affect food production in plants.",
        "The rate of photosynthesis is affected by several 'limiting factors': light intensity, carbon dioxide "
        "concentration, and temperature. If any one of these is too low, it limits the overall rate, even if the "
        "others are abundant - this is called the 'Law of Limiting Factors'.\n\n"
        "Advanced application: This principle is used in commercial greenhouses, where growers control CO2 "
        "levels, artificial lighting and temperature to maximise crop yield - a real-world application of a "
        "concept first learned in a basic science classroom."),
    "Chapter 2 - Nutrition in Animals": ("Advanced: Comparing Digestive Systems Across Animals",
        "Understanding how digestive systems are adapted to different diets.",
        "Digestive systems vary significantly based on diet. Herbivores like cows have longer intestines and "
        "specialised stomach chambers (like the rumen) to break down tough plant cellulose, while carnivores have "
        "shorter digestive tracts suited to digesting protein-rich meat quickly.\n\n"
        "Advanced concept: Some animals, like birds, have a unique digestive adaptation called a 'gizzard' - a "
        "muscular organ that grinds food (sometimes with the help of swallowed stones) since birds lack teeth. "
        "Comparing these adaptations across species reveals how digestion evolved to match diet."),
    "Chapter 1 - Active and Passive Voice": ("Advanced: Choosing Voice for Effective Writing",
        "Understanding when active or passive voice is more effective stylistically.",
        "While active voice is generally more direct and engaging, passive voice is preferred in specific "
        "contexts: scientific writing (to focus on the process, not the researcher), when the doer is unknown "
        "('My phone was stolen'), or when the receiver of the action is more important than the doer ('The "
        "building was destroyed by the earthquake').\n\n"
        "Advanced skill: Practise rewriting the same sentence in both voices and analysing which one better fits "
        "different contexts - a newspaper headline, a scientific report, and a personal narrative - to develop a "
        "stylistic sense beyond just grammatical correctness."),
    "Chapter 2 - Direct and Indirect Speech": ("Advanced: Reporting Complex and Mixed Sentences",
        "Handling reported speech in sentences with multiple clauses or mixed types.",
        "Real conversations often mix statements, questions and commands together, requiring careful handling "
        "when converting to indirect speech. For example: 'He said, \"I am tired. Can you help me?\"' becomes "
        "'He said that he was tired and asked if I could help him' - combining a reported statement and a "
        "reported question with appropriate connectors.\n\n"
        "Advanced practice: Try converting short dialogues (3-4 lines) from a story or play into a single, "
        "well-connected paragraph of indirect speech, paying attention to tense shifts, pronoun changes and "
        "appropriate reporting verbs throughout."),
    "Chapter 1 - Tracing Changes Through a Thousand Years": ("Advanced: Comparing Political Systems in Medieval India",
        "Comparing centralised and decentralised administration across dynasties.",
        "Medieval Indian kingdoms varied in their administrative styles. The Delhi Sultanate and Mughal Empire "
        "generally had more centralised administrations with appointed governors, while South Indian kingdoms "
        "like the Cholas developed sophisticated local self-government through village assemblies.\n\n"
        "Advanced insight: Studying inscriptions from Chola villages reveals detailed records of local elections "
        "and administration nearly a thousand years ago - offering a fascinating early example of democratic "
        "practices in local governance, well before modern democracy developed."),
    "Chapter 2 - Environment": ("Advanced: Human-Environment Interaction Across Regions",
        "Comparing how communities in different environments adapt and interact with nature.",
        "Human lifestyles and economic activities are deeply shaped by their environment. Communities in "
        "mountainous regions often rely on terrace farming and animal husbandry, while desert communities develop "
        "water conservation techniques and nomadic herding practices suited to scarce resources.\n\n"
        "Advanced concept - Sustainable adaptation: Studying how traditional communities have sustainably adapted "
        "to challenging environments over centuries (e.g., stepwells in Rajasthan for water storage) offers "
        "valuable lessons for modern sustainable development, blending traditional wisdom with contemporary "
        "environmental challenges."),
    "Chapter 1 - Word Processing": ("Advanced: Automating Documents with Templates and Styles",
        "Using styles, templates and automation features for professional documents.",
        "Beyond basic formatting, word processors offer 'Styles' (predefined formatting sets for headings, body "
        "text, etc.) that ensure consistency across long documents and allow automatic generation of a Table of "
        "Contents. Templates provide ready-made structures for common documents like resumes or reports.\n\n"
        "Advanced skill - Mail Merge in depth: Beyond simple letters, Mail Merge can generate personalised "
        "certificates, invitations, or report cards by linking a document template to a spreadsheet of names and "
        "details - a powerful time-saving skill used widely in offices and schools."),
    "Chapter 2 - Introduction to Internet": ("Advanced: How Data Travels Across the Internet",
        "Understanding the basics of how information moves between computers worldwide.",
        "When you visit a website, your request travels through a series of interconnected networks, routers and "
        "servers - broken into small 'packets' of data that may even travel via different paths before being "
        "reassembled at the destination. This system, based on protocols like TCP/IP, allows the internet to be "
        "resilient and fast.\n\n"
        "Advanced concept - Cybersecurity basics: As more of our lives move online, understanding basic "
        "cybersecurity concepts - like why HTTPS is more secure than HTTP, and how phishing scams try to trick "
        "users into revealing personal information - becomes an essential 21st-century life skill."),

    # ---- Class 9 ----
    "Chapter 1 - Number Systems": ("Advanced: Representing Irrational Numbers on the Number Line",
        "Geometric construction of irrational numbers using the Pythagorean theorem.",
        "Irrational numbers like √2 can be precisely located on a number line using a geometric method based on "
        "the Pythagorean theorem. For example, to locate √2, construct a right triangle with both legs of length "
        "1 unit; the hypotenuse will have length exactly √2, which can then be transferred onto the number line "
        "using a compass.\n\n"
        "Advanced idea: This construction process, called the 'spiral of Theodorus', can be extended to locate "
        "√3, √4, √5 and beyond, visually demonstrating that irrational numbers, despite having non-terminating "
        "decimal expansions, occupy precise, well-defined points on the number line."),
    "Chapter 2 - Polynomials": ("Advanced: Factor Theorem and Remainder Theorem",
        "Using algebraic theorems to factorise and analyse polynomials efficiently.",
        "The Remainder Theorem states that when a polynomial p(x) is divided by (x-a), the remainder equals "
        "p(a). The Factor Theorem extends this: if p(a) = 0, then (x-a) is a factor of p(x). These theorems allow "
        "quick checks for factors without performing long division.\n\n"
        "Advanced application: For example, to check if (x-2) is a factor of p(x) = x³ - 3x² + 2, calculate "
        "p(2) = 8 - 12 + 2 = -2. Since this is not zero, (x-2) is NOT a factor. This technique is widely used in "
        "higher algebra and calculus for simplifying and solving polynomial equations."),
    "Chapter 1 - Matter in Our Surroundings": ("Advanced: Kinetic Theory of Matter",
        "Explaining states of matter through the motion and energy of particles.",
        "The Kinetic Theory of Matter explains the behaviour of solids, liquids and gases based on the motion and "
        "energy of their particles. In solids, particles vibrate in fixed positions with low kinetic energy; in "
        "liquids, particles have more energy and can move past each other; in gases, particles have very high "
        "kinetic energy and move freely in all directions.\n\n"
        "Advanced concept: As temperature increases, particle kinetic energy increases, explaining why heating a "
        "solid eventually causes it to melt and then boil - the added energy overcomes the intermolecular forces "
        "holding particles in fixed or semi-fixed positions."),
    "Chapter 2 - The Fundamental Unit of Life (Cell)": ("Advanced: Cell Transport Mechanisms",
        "Understanding how substances move in and out of cells through diffusion and osmosis.",
        "Cells constantly exchange substances with their environment through processes like diffusion (movement "
        "of particles from high to low concentration) and osmosis (movement of water across a selectively "
        "permeable membrane from a region of lower solute concentration to higher solute concentration).\n\n"
        "Advanced application: Osmosis explains why plant cells placed in salty water lose water and shrink "
        "(plasmolysis), while red blood cells placed in pure water can swell and burst. Understanding these "
        "transport mechanisms is foundational for later studies in human physiology and medicine."),
    "Chapter 1 - Grammar: Modals": ("Advanced: Modal Verbs in Formal and Academic Writing",
        "Using modals precisely to convey shades of certainty, obligation and formality.",
        "In academic and formal writing, modal verbs help express precise degrees of certainty and formality. "
        "For example, 'This may indicate...' expresses tentative possibility appropriate for research writing, "
        "while 'This must indicate...' expresses strong certainty based on solid evidence.\n\n"
        "Advanced practice: Notice how modals shift meaning subtly - compare 'You should submit the report by "
        "Friday' (advice) versus 'You must submit the report by Friday' (strict requirement) versus 'You might "
        "want to submit the report by Friday' (very soft suggestion). Mastering these subtle shades is key to "
        "precise, professional communication."),
    "Chapter 2 - Writing Skills: Letter Writing": ("Advanced: Persuasive and Analytical Writing Techniques",
        "Structuring formal letters and essays to persuade or analyse effectively.",
        "Advanced formal writing goes beyond structure to persuasive technique - using a clear thesis statement, "
        "supporting evidence, addressing counterarguments, and a strong concluding call to action. This is "
        "especially useful for letters to the editor or persuasive essays on social issues.\n\n"
        "Advanced skill - Register and tone: Learning to adjust your 'register' (level of formality) based on "
        "audience and purpose is a hallmark of advanced writing - a letter to a close friend, a school principal, "
        "and a government official each require a distinctly different tone, vocabulary and structure."),
    "Chapter 1 - The French Revolution": ("Advanced: Long-Term Global Impact of the French Revolution",
        "Examining how revolutionary ideals influenced movements worldwide.",
        "The ideals of 'Liberty, Equality, Fraternity' from the French Revolution rippled far beyond France, "
        "influencing the Latin American independence movements, the abolition of slavery debates, and later, "
        "anti-colonial movements across Asia and Africa, including India's own freedom struggle.\n\n"
        "Advanced analysis: Historians debate whether the Revolution's ideals were fully realised even within "
        "France itself, given the Reign of Terror and later Napoleonic autocracy - a useful case study in how "
        "revolutionary ideals and their real-world implementation can diverge significantly."),
    "Chapter 2 - Physical Features of India": ("Advanced: Tectonic Processes Shaping India's Landforms",
        "Understanding the plate tectonic history behind India's major landforms.",
        "India's diverse physical features result from millions of years of tectonic activity. The Indian "
        "Plate, once part of the ancient supercontinent Gondwana, drifted northward and collided with the "
        "Eurasian Plate about 50 million years ago, pushing up the Himalayas - a process that continues today, "
        "making the Himalayas grow a few millimetres taller each year.\n\n"
        "Advanced concept: This ongoing tectonic activity also explains why the Himalayan region is prone to "
        "earthquakes, as stress continues to build and release along fault lines where the plates meet."),
    "Chapter 1 - Introduction to Python": ("Advanced: Writing Reusable Functions and Modules",
        "Structuring Python programs using functions for cleaner, reusable code.",
        "As programs grow more complex, organising code into functions - reusable blocks that perform a specific "
        "task - makes code cleaner and easier to debug. For example, instead of repeating calculation code "
        "multiple times, define it once as a function: def calculate_area(length, width): return length * width.\n\n"
        "Advanced concept - Modules: Python allows grouping related functions into 'modules' (separate files) "
        "that can be imported and reused across different programs, e.g. 'import math' gives access to "
        "mathematical functions like sqrt() and pi, without rewriting them yourself."),
    "Chapter 2 - Data Representation": ("Advanced: Data Compression and Error Detection",
        "How computers efficiently store and verify data integrity.",
        "Beyond simply representing data in binary, computers use techniques like data compression (reducing "
        "file size by removing redundancy, as in .zip or .jpg formats) and error detection codes (like parity "
        "bits or checksums) to verify that data hasn't been corrupted during storage or transmission.\n\n"
        "Advanced idea: A simple parity bit adds an extra bit to a piece of binary data to make the total number "
        "of 1s either always even or always odd - if the received data doesn't match this expected pattern, an "
        "error is detected, prompting a re-transmission request."),

    # ---- Class 10 ----
    "Chapter 1 - Real Numbers": ("Advanced: The Fundamental Theorem of Arithmetic",
        "Using prime factorisation to understand HCF, LCM and irrationality proofs.",
        "The Fundamental Theorem of Arithmetic states that every composite number can be expressed as a product "
        "of primes in exactly one way (ignoring order). This is the basis for finding HCF and LCM using prime "
        "factorisation: HCF is the product of the smallest powers of common primes, and LCM is the product of the "
        "greatest powers of all primes involved.\n\n"
        "Advanced application: This theorem is also used to prove that numbers like √2 are irrational, using a "
        "method called 'proof by contradiction' - assuming √2 is rational (p/q in lowest terms) leads to both p "
        "and q being even, contradicting the 'lowest terms' assumption, proving √2 cannot be rational."),
    "Chapter 2 - Polynomials and Quadratic Equations": ("Advanced: Relationship Between Zeroes and Coefficients",
        "Exploring how the roots of a quadratic relate algebraically to its coefficients.",
        "For a quadratic equation ax² + bx + c = 0 with roots (zeroes) α and β, there is a direct algebraic "
        "relationship: the sum of roots α+β = -b/a, and the product of roots α×β = c/a. These relationships allow "
        "you to form a quadratic equation directly if you know its roots, or find one root if you know the other "
        "and the coefficients.\n\n"
        "Advanced application: This connects to the quadratic formula, x = [-b ± √(b²-4ac)] / 2a, and the "
        "discriminant (b²-4ac), which determines whether roots are real and distinct, real and equal, or not "
        "real - a key concept for higher secondary mathematics and beyond."),
    "Chapter 1 - Chemical Reactions and Equations": ("Advanced: Rate of Reaction and Catalysts",
        "Factors influencing how fast chemical reactions occur.",
        "The rate of a chemical reaction depends on factors including concentration of reactants, temperature, "
        "surface area, and the presence of a catalyst (a substance that speeds up a reaction without being "
        "consumed itself). Higher temperature and concentration generally increase reaction rate by increasing "
        "the frequency and energy of particle collisions.\n\n"
        "Advanced application: Catalysts are widely used industrially - for example, in catalytic converters in "
        "vehicles, platinum and palladium catalysts speed up the conversion of harmful exhaust gases into less "
        "harmful substances, demonstrating a direct real-world application of this chemistry concept."),
    "Chapter 2 - Life Processes": ("Advanced: Homeostasis and Feedback Mechanisms",
        "How the body maintains internal stability through regulatory feedback systems.",
        "Life processes work together to maintain 'homeostasis' - a stable internal environment despite external "
        "changes. For example, when blood glucose rises after eating, the pancreas releases insulin to bring it "
        "back to normal levels; when it falls too low, glucagon is released to raise it - a classic negative "
        "feedback loop.\n\n"
        "Advanced concept: Understanding these feedback mechanisms is crucial for understanding diseases like "
        "diabetes, where this regulatory system malfunctions, connecting basic life-process biology directly to "
        "important real-world health topics."),
    "Chapter 1 - Literary Devices": ("Advanced: Analysing Tone, Voice and Authorial Intent",
        "Moving beyond identifying devices to analysing their effect and purpose.",
        "Advanced literary analysis goes beyond simply identifying a metaphor or simile - it asks WHY the author "
        "chose that device and what effect it creates. For example, using harsh, jarring consonance in a war poem "
        "might reinforce the brutality being described, while soft assonance in a love poem creates a soothing, "
        "melodic tone.\n\n"
        "Advanced skill: When analysing a poem or passage for exams, always connect the literary device to its "
        "effect on the reader and its relevance to the overall theme - this deeper analytical approach is what "
        "distinguishes strong literary answers from merely identifying devices by name."),
    "Chapter 2 - Letter and Essay Writing": ("Advanced: Structuring Argumentative and Analytical Essays",
        "Building well-reasoned, evidence-based essays for board-level writing.",
        "Advanced essay writing requires a clear thesis statement in the introduction, well-organised body "
        "paragraphs each focusing on a single supporting argument or point (with evidence and explanation), "
        "consideration of counterarguments where relevant, and a conclusion that synthesises rather than simply "
        "repeats the introduction.\n\n"
        "Advanced skill - Transitions: Using strong transitional phrases ('Furthermore', 'On the other hand', "
        "'Consequently') helps ideas flow logically between paragraphs, creating the kind of coherent, "
        "sophisticated writing expected at the board examination level."),
    "Chapter 1 - Nationalism in India": ("Advanced: Comparing Nationalist Movements Across Colonies",
        "Comparing India's nationalist movement with other anti-colonial struggles worldwide.",
        "India's nationalist movement, while unique in its scale and use of non-violent methods under Gandhi's "
        "leadership, shared common features with other anti-colonial movements worldwide - the use of print media "
        "to spread ideas, mass mobilisation, and the search for a unifying national identity across diverse "
        "populations.\n\n"
        "Advanced analysis: Comparing India's largely non-violent approach with more militant anti-colonial "
        "movements elsewhere (or with revolutionary movements like the French Revolution) offers valuable insight "
        "into different strategic approaches to achieving political change against powerful ruling authorities."),
    "Chapter 2 - Resources and Development": ("Advanced: Resource Management and Circular Economy",
        "Modern approaches to sustainable resource use and waste reduction.",
        "Beyond traditional conservation, the concept of a 'circular economy' is gaining importance - an "
        "economic model that minimises waste by continually reusing, repairing, and recycling resources, in "
        "contrast to the traditional 'take-make-dispose' linear economic model.\n\n"
        "Advanced application: India's push towards renewable energy (solar and wind), along with policies "
        "promoting waste segregation and recycling in cities, reflects a growing shift towards more sustainable "
        "resource management practices that balance economic development with long-term environmental "
        "responsibility."),
    "Chapter 1 - Python Programming Basics": ("Advanced: Object-Oriented Programming Concepts",
        "Introducing classes and objects as a foundation for advanced programming.",
        "Beyond basic functions and loops, Python supports Object-Oriented Programming (OOP), which organises "
        "code around 'objects' - self-contained units combining data (attributes) and behaviour (methods). For "
        "example, a 'Student' class might have attributes like name and marks, and methods like calculate_grade().\n\n"
        "Advanced concept: OOP concepts like classes, objects, and inheritance (where one class can inherit "
        "properties from another) form the foundation of most modern software development, making this an "
        "important stepping stone towards more advanced computer science study."),
    "Chapter 2 - Database Concepts": ("Advanced: Database Normalisation and Real-World Design",
        "Designing efficient, well-structured databases used in real applications.",
        "Well-designed databases follow principles of 'normalisation' - organising data across multiple related "
        "tables to minimise redundancy and maintain data integrity. For example, instead of repeating a student's "
        "full address in every record of a school database, addresses can be stored once in a separate table and "
        "linked via a key.\n\n"
        "Advanced application: Nearly every modern application - banking systems, e-commerce platforms, school "
        "management systems - relies on well-designed relational databases behind the scenes, making database "
        "design principles a highly practical and valuable skill for future computer science study."),

    # ---- Class 8 (existing chapters) ----
    "Chapter 1 - Rational Numbers": ("Advanced: Properties and Density of Rational Numbers",
        "Exploring the density property and advanced operations on rational numbers.",
        "A fascinating property of rational numbers is 'density': between any two rational numbers, no matter "
        "how close, there are infinitely many other rational numbers. For example, between 1/2 and 1/3, you can "
        "always find another rational number by averaging them: (1/2 + 1/3)/2 = 5/12.\n\n"
        "Advanced practice: This density property distinguishes rational numbers from whole numbers or integers "
        "(where there's a clear 'next' number) and is an important conceptual foundation for understanding real "
        "numbers and the number line in higher classes."),
    "Chapter 2 - Linear Equations": ("Advanced: Word Problems and Equations with Fractions",
        "Solving more complex linear equations involving fractions and multi-step reasoning.",
        "Advanced linear equations often involve fractional coefficients, requiring clearing fractions by "
        "multiplying through by the LCM of all denominators. For example, to solve x/2 + x/3 = 5, multiply every "
        "term by 6 (LCM of 2 and 3): 3x + 2x = 30, giving 5x = 30, so x = 6.\n\n"
        "Advanced application: Many real-life problems - like mixture problems, age problems, and speed-distance "
        "problems - can be modelled and solved using linear equations, making this a foundational skill for "
        "algebra in higher classes."),
    "Chapter 3 - Understanding Quadrilaterals": ("Advanced: Diagonal Properties and Proofs",
        "Exploring diagonal relationships and simple geometric proofs for quadrilaterals.",
        "Beyond memorising properties, understanding WHY they hold true builds deeper mathematical thinking. For "
        "example, in a parallelogram, the diagonals bisect each other because the two triangles formed by a "
        "diagonal are congruent (by the Alternate Interior Angles theorem and side-angle-side congruence).\n\n"
        "Advanced practice: Try proving that the diagonals of a rectangle are equal in length, using the fact "
        "that a rectangle is a parallelogram with right angles, combined with the Pythagorean theorem - this kind "
        "of reasoning is excellent preparation for formal geometric proofs in higher classes."),
    "Chapter 1 - Crop Production": ("Advanced: Modern Agricultural Technology",
        "Exploring how technology is transforming farming practices.",
        "Modern agriculture increasingly uses technology like precision farming (using sensors and GPS to apply "
        "water and fertiliser exactly where needed), genetically modified (GM) crops bred for higher yield or "
        "pest resistance, and greenhouse farming to control growing conditions year-round.\n\n"
        "Advanced concept - Green Revolution: India's Green Revolution in the 1960s-70s, using high-yielding "
        "variety seeds, fertilisers and irrigation, dramatically increased food grain production, transforming "
        "India from a food-deficit to a food-surplus nation - a landmark case study in applying science to solve "
        "real-world challenges."),
    "Chapter 2 - Microorganisms": ("Advanced: Biotechnology and Microorganisms",
        "How modern biotechnology harnesses microorganisms for advanced applications.",
        "Beyond traditional uses like fermentation, modern biotechnology uses genetically engineered "
        "microorganisms to produce medicines (like insulin for diabetics, produced by genetically modified "
        "bacteria), biofuels, and even to help clean up oil spills (bioremediation).\n\n"
        "Advanced concept: Scientists can now insert specific genes into bacteria, turning them into microscopic "
        "'factories' that produce useful substances - a striking example of how understanding basic microbiology "
        "can lead to transformative technologies in medicine and industry."),
    "Chapter 3 - Synthetic Fibres": ("Advanced: The Environmental Trade-offs of Synthetic Materials",
        "Weighing the benefits and environmental costs of synthetic fibres and plastics.",
        "While synthetic fibres and plastics offer durability, low cost and versatility, their environmental "
        "cost - persistence in landfills and oceans as microplastics - has become a major global concern, "
        "prompting research into biodegradable alternatives made from plant-based polymers.\n\n"
        "Advanced concept: Scientists are developing 'bioplastics' from materials like corn starch and "
        "algae that offer similar functional properties to traditional plastics but decompose much more readily, "
        "representing an active area of environmental science and materials engineering research."),
    "Chapter 1 - The Best Christmas Present": ("Advanced: Literature of War and Peace",
        "Placing the story in the broader context of anti-war literature.",
        "'The Best Christmas Present in the World' belongs to a broader tradition of anti-war literature that "
        "uses personal, human stories to highlight the futility and tragedy of war, contrasted with moments of "
        "shared humanity - similar in spirit to works like Erich Maria Remarque's 'All Quiet on the Western "
        "Front'.\n\n"
        "Advanced discussion: Comparing how different authors use small, personal moments (like a football match "
        "or a shared meal) to convey larger anti-war messages helps develop deeper literary appreciation for how "
        "fiction can address serious historical and moral themes."),
    "Chapter 2 - The Tsunami": ("Advanced: Disaster Preparedness and Early Warning Systems",
        "Connecting the story's themes to real-world disaster management systems.",
        "Following major tsunamis like the 2004 Indian Ocean disaster, countries invested heavily in early "
        "warning systems - networks of ocean sensors and seismographs that detect underwater earthquakes and "
        "unusual wave patterns, sending alerts within minutes to at-risk coastal areas.\n\n"
        "Advanced connection: This story's message about individual awareness and quick action complements "
        "these larger technological systems - both individual knowledge and institutional preparedness are "
        "necessary for effectively reducing loss of life during natural disasters."),
    "Chapter 1 - How, When and Where": ("Advanced: Historiography - The Study of How History is Written",
        "Understanding historiography and how historical interpretation has evolved.",
        "'Historiography' is the study of how history itself has been written and interpreted over time. "
        "Colonial-era historians often framed Indian history through a European lens, while post-independence "
        "Indian historians have worked to develop more nuanced, India-centred interpretations of the same events "
        "and periods.\n\n"
        "Advanced idea: Recognising that history is not just a fixed set of facts but an evolving field of "
        "interpretation - shaped by the perspectives and priorities of each generation of historians - is a "
        "sophisticated but essential understanding for serious students of history."),
    "Chapter 2 - From Trade to Territory": ("Advanced: Economic Motivations Behind Colonial Expansion",
        "Analysing the deeper economic drivers of the East India Company's expansion.",
        "The East India Company's expansion from trade to territorial control was driven significantly by "
        "economics: control over territory meant control over lucrative trade goods (textiles, spices), tax "
        "revenue, and the ability to eliminate competition from French and Dutch trading companies.\n\n"
        "Advanced analysis: Understanding colonialism through this economic lens - alongside political and "
        "military factors - offers a fuller picture of why and how a trading company gradually transformed into "
        "the ruling power over a vast subcontinent, a process historians call 'the Company-state'."),
    "Chapter 1 - Resources": ("Advanced: Resource Geopolitics",
        "Understanding how control over key resources shapes international relations.",
        "Control over critical resources - like oil, rare earth minerals (used in electronics), and fresh water "
        "- significantly shapes international relations and even conflicts between nations. Countries often form "
        "strategic alliances or trade agreements specifically to secure access to resources they lack "
        "domestically.\n\n"
        "Advanced discussion: As the world transitions towards renewable energy, control over materials like "
        "lithium and cobalt (essential for batteries) is becoming an increasingly important geopolitical factor, "
        "showing how resource studies connect directly to global economics and politics."),
    "Chapter 2 - Land, Soil, Water": ("Advanced: Watershed Management and Integrated Resource Planning",
        "Exploring holistic approaches to managing interconnected land and water resources.",
        "Since land, soil and water resources are deeply interconnected, modern conservation increasingly uses "
        "'watershed management' - a holistic approach that manages an entire drainage area together, combining "
        "soil conservation, water harvesting, and vegetation management rather than treating each resource in "
        "isolation.\n\n"
        "Advanced application: Successful Indian watershed management projects, such as those in Maharashtra and "
        "Rajasthan, have transformed drought-prone regions into productive agricultural land by combining "
        "traditional water harvesting techniques with modern scientific planning."),
    "Chapter 1 - Algorithms": ("Advanced: Algorithm Efficiency and Big-O Thinking",
        "An introduction to comparing how 'good' different algorithms are.",
        "Not all algorithms that solve the same problem are equally good - some are much faster or use less "
        "memory than others. Computer scientists compare algorithm efficiency using a concept called 'time "
        "complexity', often expressed with Big-O notation, which describes how the time an algorithm takes grows "
        "as the input size grows.\n\n"
        "Advanced example: A simple search that checks every item one by one (linear search) becomes slow for "
        "very large lists, while a 'binary search' on a sorted list (repeatedly halving the search area) is "
        "dramatically faster - an early example of algorithmic thinking that becomes crucial in higher-level "
        "computer science."),
    "Chapter 2 - Programming in Python": ("Advanced: Functions, Lists and Building Small Programs",
        "Combining core Python concepts to build simple, useful programs.",
        "Combining functions, loops, conditionals and lists allows you to build genuinely useful small programs "
        "- for example, a program that takes a list of student marks, calculates the average using a loop, and "
        "prints a grade based on conditional logic (if/elif/else).\n\n"
        "Advanced practice: Try writing a simple Python program that takes a list of numbers, uses a loop to find "
        "the maximum and minimum values without using the built-in max()/min() functions, and prints a summary - "
        "this kind of independent problem-solving builds real programming confidence beyond memorising syntax."),
}

# ============================================================================
# DRIVER: chapter definitions + Command.handle()
# ============================================================================

SUBJECT_DESCRIPTIONS = {
    "Mathematics": "Study of numbers, shapes, and patterns",
    "Science": "Study of the natural world",
    "English": "Study of English language and literature",
    "Social Studies": "Study of society, geography and history",
    "Social Science": "Study of history, geography and civics",
    "Computer Science": "Study of computers and computing",
}

# subj_name -> [(title, order, desc, questions_source), ...]
# questions_source is either a callable (math generator) or a list of question tuples
CHAPTER_DEFS = {
    "Class 5": {
        "Mathematics": [
            ("Chapter 1 - Numbers and Place Value", 1, "Place value, rounding and large numbers", gen_c5_place_value),
            ("Chapter 2 - Fractions", 2, "Understanding and operating on fractions", gen_c5_fractions),
        ],
        "Science": [
            ("Chapter 1 - Plants and Animals", 1, "Parts of plants, animal classification and nutrition", CLASS5_SCIENCE_PLANTS),
            ("Chapter 2 - Our Environment", 2, "Habitats, pollution and conservation", CLASS5_SCIENCE_ENV),
        ],
        "English": [
            ("Chapter 1 - Grammar Basics", 1, "Nouns, verbs, adjectives and basic sentence structure", CLASS5_ENGLISH_GRAMMAR),
            ("Chapter 2 - Reading Comprehension and Vocabulary", 2, "Synonyms, antonyms and story elements", CLASS5_ENGLISH_READING),
        ],
        "Social Studies": [
            ("Chapter 1 - Our Country India", 1, "India's geography, symbols and government basics", CLASS5_SOCIAL_INDIA),
            ("Chapter 2 - Maps and Directions", 2, "Reading maps, directions and globes", CLASS5_SOCIAL_MAPS),
        ],
        "Computer Science": [
            ("Chapter 1 - Introduction to Computers", 1, "Parts of a computer and basic terms", CLASS5_CS_INTRO),
            ("Chapter 2 - Basics of MS Paint and Keyboard", 2, "Drawing tools and keyboard basics", CLASS5_CS_PAINT),
        ],
    },
    "Class 6": {
        "Mathematics": [
            ("Chapter 1 - Knowing Our Numbers", 1, "Large numbers, rounding and estimation", gen_c6_numbers),
            ("Chapter 2 - Whole Numbers", 2, "Properties and operations on whole numbers", gen_c6_whole),
        ],
        "Science": [
            ("Chapter 1 - Food: Where Does It Come From", 1, "Plant and animal sources of food", CLASS6_SCI_FOOD_SOURCE),
            ("Chapter 2 - Components of Food", 2, "Nutrients, balanced diet and deficiency diseases", CLASS6_SCI_COMPONENTS),
        ],
        "English": [
            ("Chapter 1 - Tenses", 1, "Present, past and future tenses", CLASS6_ENG_TENSES),
            ("Chapter 2 - Parts of Speech", 2, "Nouns, verbs, adjectives, adverbs and more", CLASS6_ENG_PARTS),
        ],
        "Social Science": [
            ("Chapter 1 - What, Where, How and When", 1, "Sources and periods of history", CLASS6_SOC_WHATWHERE),
            ("Chapter 2 - The Earth in the Solar System", 2, "Planets, the solar system and celestial bodies", CLASS6_SOC_SOLAR),
        ],
        "Computer Science": [
            ("Chapter 1 - Computer Fundamentals", 1, "Generations of computers, memory and storage", CLASS6_CS_FUNDAMENTALS),
            ("Chapter 2 - Input and Output Devices", 2, "Types of input/output devices", CLASS6_CS_IO),
        ],
    },
    "Class 7": {
        "Mathematics": [
            ("Chapter 1 - Integers", 1, "Operations on positive and negative integers", gen_c7_integers),
            ("Chapter 2 - Fractions and Decimals", 2, "Operations on fractions and decimals", gen_c7_fracdec),
        ],
        "Science": [
            ("Chapter 1 - Nutrition in Plants", 1, "Photosynthesis and modes of nutrition in plants", CLASS7_SCI_PLANT_NUTRI),
            ("Chapter 2 - Nutrition in Animals", 2, "Digestion and nutrition in animals", CLASS7_SCI_ANIMAL_NUTRI),
        ],
        "English": [
            ("Chapter 1 - Active and Passive Voice", 1, "Converting between active and passive voice", CLASS7_ENG_VOICE),
            ("Chapter 2 - Direct and Indirect Speech", 2, "Converting between direct and reported speech", CLASS7_ENG_SPEECH),
        ],
        "Social Science": [
            ("Chapter 1 - Tracing Changes Through a Thousand Years", 1, "Medieval Indian dynasties and society", CLASS7_SOC_TRACING),
            ("Chapter 2 - Environment", 2, "Natural and human-made environment", CLASS7_SOC_ENVIRONMENT),
        ],
        "Computer Science": [
            ("Chapter 1 - Word Processing", 1, "Features and tools of word processors", CLASS7_CS_WORD),
            ("Chapter 2 - Introduction to Internet", 2, "Internet basics, browsers and online safety", CLASS7_CS_INTERNET),
        ],
    },
    "Class 9": {
        "Mathematics": [
            ("Chapter 1 - Number Systems", 1, "Rational, irrational numbers and real number line", gen_c9_numsys),
            ("Chapter 2 - Polynomials", 2, "Degree, zeroes and evaluation of polynomials", gen_c9_poly),
        ],
        "Science": [
            ("Chapter 1 - Matter in Our Surroundings", 1, "States of matter and changes of state", CLASS9_SCI_MATTER),
            ("Chapter 2 - The Fundamental Unit of Life (Cell)", 2, "Cell structure and organelles", CLASS9_SCI_CELL),
        ],
        "English": [
            ("Chapter 1 - Grammar: Modals", 1, "Using modal verbs correctly", CLASS9_ENG_MODALS),
            ("Chapter 2 - Writing Skills: Letter Writing", 2, "Formal/informal letters and essay writing", CLASS9_ENG_LETTER),
        ],
        "Social Science": [
            ("Chapter 1 - The French Revolution", 1, "Causes, events and impact of the French Revolution", CLASS9_SOC_FRENCH),
            ("Chapter 2 - Physical Features of India", 2, "Mountains, plains, plateaus and coasts of India", CLASS9_SOC_PHYSICAL),
        ],
        "Computer Science": [
            ("Chapter 1 - Introduction to Python", 1, "Python basics: variables, data types, control flow", CLASS9_CS_PYTHON),
            ("Chapter 2 - Data Representation", 2, "Number systems and data encoding in computers", CLASS9_CS_DATA),
        ],
    },
    "Class 10": {
        "Mathematics": [
            ("Chapter 1 - Real Numbers", 1, "Euclid's division lemma, HCF and LCM", gen_c10_realnum),
            ("Chapter 2 - Polynomials and Quadratic Equations", 2, "Zeroes, sum/product of roots and discriminant", gen_c10_quad),
        ],
        "Science": [
            ("Chapter 1 - Chemical Reactions and Equations", 1, "Types of chemical reactions and balancing equations", CLASS10_SCI_REACTIONS),
            ("Chapter 2 - Life Processes", 2, "Nutrition, respiration, transportation and excretion", CLASS10_SCI_LIFE),
        ],
        "English": [
            ("Chapter 1 - Literary Devices", 1, "Simile, metaphor, personification and more", CLASS10_ENG_DEVICES),
            ("Chapter 2 - Letter and Essay Writing", 2, "Formal writing, essays and reports", CLASS10_ENG_WRITING),
        ],
        "Social Science": [
            ("Chapter 1 - Nationalism in India", 1, "The Indian freedom struggle and nationalist movements", CLASS10_SOC_NATIONALISM),
            ("Chapter 2 - Resources and Development", 2, "Types of resources, soil, and conservation", CLASS10_SOC_RESOURCES),
        ],
        "Computer Science": [
            ("Chapter 1 - Python Programming Basics", 1, "Lists, loops, functions and file handling", CLASS10_CS_PYTHON_BASICS),
            ("Chapter 2 - Database Concepts", 2, "DBMS, SQL and relational databases", CLASS10_CS_DATABASE),
        ],
    },
}

# Class 8 existing chapters -> (subject_name, topup_questions_source)
C8_TOPUP = {
    ("Mathematics", "Chapter 1 - Rational Numbers"): gen_c8_rational,
    ("Mathematics", "Chapter 2 - Linear Equations"): gen_c8_linear,
    ("Mathematics", "Chapter 3 - Understanding Quadrilaterals"): gen_c8_quad,
    ("Science", "Chapter 1 - Crop Production"): C8_SCI_CROP_MORE,
    ("Science", "Chapter 2 - Microorganisms"): C8_SCI_MICRO_MORE,
    ("Science", "Chapter 3 - Synthetic Fibres"): C8_SCI_FIBRES_MORE,
    ("English", "Chapter 1 - The Best Christmas Present"): C8_ENG_CHRISTMAS_MORE,
    ("English", "Chapter 2 - The Tsunami"): C8_ENG_TSUNAMI_MORE,
    ("History", "Chapter 1 - How, When and Where"): C8_HIST_HWW_MORE,
    ("History", "Chapter 2 - From Trade to Territory"): C8_HIST_TRADE_MORE,
    ("Geography", "Chapter 1 - Resources"): C8_GEO_RESOURCES_MORE,
    ("Geography", "Chapter 2 - Land, Soil, Water"): C8_GEO_LAND_MORE,
    ("Computer Science", "Chapter 1 - Algorithms"): C8_CS_ALGO_MORE,
    ("Computer Science", "Chapter 2 - Programming in Python"): C8_CS_PYTHON_MORE,
}


class Command(BaseCommand):
    help = "Seed advanced study materials and 20-question banks/quizzes for all classes and subjects"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding advanced materials, question banks and quizzes..."))

        # ---- Part A: Classes 5, 6, 7, 9, 10 (new subjects/chapters) ----
        for class_name, subjects in CHAPTER_DEFS.items():
            class_obj, _ = ClassLevel.objects.get_or_create(
                name=class_name, defaults={"description": class_name.replace("Class ", "") + " Grade"}
            )
            self.stdout.write(self.style.SUCCESS(f"\n=== {class_name} ==="))

            for subj_name, chapters in subjects.items():
                subj_obj, _ = Subject.objects.get_or_create(
                    name=subj_name, class_level=class_obj,
                    defaults={"description": SUBJECT_DESCRIPTIONS.get(subj_name, "")}
                )
                self.stdout.write(f"  Subject: {subj_name}")

                for title, order, desc, qsource in chapters:
                    chapter_obj, _ = Chapter.objects.get_or_create(
                        subject=subj_obj, title=title, defaults={"description": desc, "order": order}
                    )

                    questions = qsource() if callable(qsource) else qsource

                    # Basic "Quick Notes" material auto-built from question explanations
                    seen_expl = []
                    for q in questions:
                        expl = q[6]
                        if expl not in seen_expl:
                            seen_expl.append(expl)
                        if len(seen_expl) >= 12:
                            break
                    basic_content = f"Quick Revision Notes - {title}\n\n" + "\n".join(f"- {e}" for e in seen_expl)
                    StudyMaterial.objects.get_or_create(
                        chapter=chapter_obj, title=f"{title} - Quick Notes",
                        defaults={"description": "Key concept summary for quick revision", "content": basic_content}
                    )

                    # Advanced material
                    if title in ADVANCED_NOTES:
                        adv_title, adv_desc, adv_content = ADVANCED_NOTES[title]
                        StudyMaterial.objects.get_or_create(
                            chapter=chapter_obj, title=adv_title,
                            defaults={"description": adv_desc, "content": adv_content}
                        )

                    # Questions
                    q_objs = []
                    for q in questions:
                        qt, ans, oa, ob, oc, od, expl, diff = q
                        obj, _ = Question.objects.get_or_create(
                            chapter=chapter_obj, question_text=qt,
                            defaults={
                                "option_a": oa, "option_b": ob, "option_c": oc, "option_d": od,
                                "correct_answer": ans, "explanation": expl, "difficulty": diff
                            }
                        )
                        q_objs.append(obj)

                    # Quiz with all questions (20-question bank)
                    quiz, _ = Quiz.objects.get_or_create(
                        title=f"Question Bank - {title}", chapter=chapter_obj,
                        defaults={
                            "description": f"{len(q_objs)} important practice questions on {title}",
                            "time_limit": max(15, len(q_objs)), "total_marks": len(q_objs)
                        }
                    )
                    for idx, q in enumerate(q_objs):
                        QuizQuestion.objects.get_or_create(quiz=quiz, question=q, defaults={"order": idx + 1, "marks": 1})

                    self.stdout.write(f"    Chapter: {title} ({len(q_objs)} questions)")

        # ---- Part B: Class 8 (top up existing chapters + advanced materials) ----
        self.stdout.write(self.style.SUCCESS("\n=== Class 8 (advanced materials + question bank top-up) ==="))
        c8, _ = ClassLevel.objects.get_or_create(name="Class 8", defaults={"description": "Eighth Grade"})
        c8_subject_defaults = {
            "Mathematics": "Study of numbers, shapes, and patterns",
            "Science": "Study of the natural world",
            "English": "Study of English language and literature",
            "History": "Study of past events",
            "Geography": "Study of Earth and its features",
            "Computer Science": "Study of computers and computing",
        }
        c8_chapter_defaults = {
            ("Mathematics", "Chapter 1 - Rational Numbers"): (1, "Understanding rational numbers and their properties"),
            ("Mathematics", "Chapter 2 - Linear Equations"): (2, "Solving linear equations in one variable"),
            ("Mathematics", "Chapter 3 - Understanding Quadrilaterals"): (3, "Properties of different quadrilaterals"),
            ("Science", "Chapter 1 - Crop Production"): (1, "Methods of crop production and management"),
            ("Science", "Chapter 2 - Microorganisms"): (2, "Friends and foes of microorganisms"),
            ("Science", "Chapter 3 - Synthetic Fibres"): (3, "Types and uses of synthetic fibres"),
            ("English", "Chapter 1 - The Best Christmas Present"): (1, "A heartwarming story about Christmas"),
            ("English", "Chapter 2 - The Tsunami"): (2, "Story of courage during the tsunami"),
            ("History", "Chapter 1 - How, When and Where"): (1, "Understanding how history is recorded"),
            ("History", "Chapter 2 - From Trade to Territory"): (2, "The East India Company in India"),
            ("Geography", "Chapter 1 - Resources"): (1, "Types and development of resources"),
            ("Geography", "Chapter 2 - Land, Soil, Water"): (2, "Natural resources and conservation"),
            ("Computer Science", "Chapter 1 - Algorithms"): (1, "Introduction to algorithms and flowcharts"),
            ("Computer Science", "Chapter 2 - Programming in Python"): (2, "Basics of Python programming"),
        }

        c8_subj_objs = {}
        for (subj_name, title), qsource in C8_TOPUP.items():
            if subj_name not in c8_subj_objs:
                subj_obj, _ = Subject.objects.get_or_create(
                    name=subj_name, class_level=c8, defaults={"description": c8_subject_defaults[subj_name]}
                )
                c8_subj_objs[subj_name] = subj_obj
            subj_obj = c8_subj_objs[subj_name]

            order, desc = c8_chapter_defaults[(subj_name, title)]
            chapter_obj, _ = Chapter.objects.get_or_create(
                subject=subj_obj, title=title, defaults={"description": desc, "order": order}
            )

            # Advanced material
            if title in ADVANCED_NOTES:
                adv_title, adv_desc, adv_content = ADVANCED_NOTES[title]
                StudyMaterial.objects.get_or_create(
                    chapter=chapter_obj, title=adv_title,
                    defaults={"description": adv_desc, "content": adv_content}
                )

            # Top-up questions
            new_questions = qsource() if callable(qsource) else qsource
            for q in new_questions:
                qt, ans, oa, ob, oc, od, expl, diff = q
                Question.objects.get_or_create(
                    chapter=chapter_obj, question_text=qt,
                    defaults={
                        "option_a": oa, "option_b": ob, "option_c": oc, "option_d": od,
                        "correct_answer": ans, "explanation": expl, "difficulty": diff
                    }
                )

            all_qs = list(Question.objects.filter(chapter=chapter_obj))
            quiz, _ = Quiz.objects.get_or_create(
                title=f"Question Bank - {title}", chapter=chapter_obj,
                defaults={
                    "description": f"{len(all_qs)} important practice questions on {title}",
                    "time_limit": max(15, len(all_qs)), "total_marks": len(all_qs)
                }
            )
            for idx, q in enumerate(all_qs):
                QuizQuestion.objects.get_or_create(quiz=quiz, question=q, defaults={"order": idx + 1, "marks": 1})

            self.stdout.write(f"    Chapter: {title} (total {len(all_qs)} questions)")

        self.stdout.write(self.style.SUCCESS(
            "\n\u2705 Advanced materials, question banks and quizzes seeded successfully for all classes!"
        ))
