from itertools import cycle
from django.core.management.base import BaseCommand
from django.db import transaction
from materials.models import ClassLevel, Subject, Chapter, StudyMaterial
from assessments.models import Question, Quiz, QuizQuestion

CLASSES = {
    "Class 5": {
        "Mathematics": ["Whole Numbers and Place Value", "Factors and Multiples", "Fractions", "Decimals", "Geometry and Shapes", "Data Handling"],
        "Science": ["Living and Non-Living Things", "Plants and Their Parts", "Animals and Adaptations", "The Human Body", "Materials and Their Properties", "Environment and Conservation"],
        "English": ["Parts of Speech", "Nouns and Pronouns", "Verbs and Tenses", "Reading Comprehension", "Vocabulary and Synonyms", "Paragraph and Letter Writing"],
        "History": ["Early Humans and Sources", "First Farming Communities", "Early Indian Civilizations", "Ancient Indian Culture", "Early Kingdoms", "Understanding Historical Sources"],
        "Geography": ["Earth and Its Neighbours", "Globes and Maps", "Landforms", "Water on Earth", "Weather and Climate", "Natural Resources"],
        "Computer Science": ["Computer Fundamentals", "Input and Output Devices", "Operating Systems and Files", "Algorithms and Flowcharts", "Block Programming", "Internet Safety"],
    },
    "Class 6": {
        "Mathematics": ["Knowing Our Numbers", "Whole Numbers", "Integers", "Fractions and Decimals", "Ratio and Proportion", "Basic Geometry and Data"],
        "Science": ["Food and Components", "Materials and Their Properties", "Separation of Substances", "Plants and the Human Body", "Motion and Light", "Living Organisms and Environment"],
        "English": ["Grammar and Sentence Structure", "Tenses", "Subject-Verb Agreement", "Reading Comprehension", "Literature Skills", "Writing Skills"],
        "History": ["What, Where and How", "Early Humans", "First Cities", "Kingdoms and Empires", "Ashoka and the Mauryas", "Buildings and Books"],
        "Geography": ["The Earth in the Solar System", "Globe Latitudes and Longitudes", "Major Domains of the Earth", "Major Landforms", "India: Location and Features", "Natural Resources"],
        "Computer Science": ["Hardware and Software", "Files and Folders", "Algorithms and Flowcharts", "Python Basics", "Data and Information", "Cyber Safety"],
    },
    "Class 7": {
        "Mathematics": ["Integers and Rational Numbers", "Fractions and Decimals", "Simple Equations", "Lines and Angles", "Triangles and Congruence", "Data Handling and Probability"],
        "Science": ["Nutrition in Plants and Animals", "Heat and Temperature", "Acids Bases and Salts", "Physical and Chemical Changes", "Weather and Climate", "Electric Current and Light"],
        "English": ["Advanced Grammar", "Tenses and Modals", "Active and Passive Voice", "Reading and Inference", "Literary Devices", "Formal and Creative Writing"],
        "History": ["Medieval Period and Sources", "New Kings and Kingdoms", "The Delhi Sultans", "The Mughal Empire", "Towns Traders and Craftspersons", "Tribes and Regional Cultures"],
        "Geography": ["Environment", "Inside Our Earth", "Our Changing Earth", "Air", "Water", "Natural Vegetation and Wildlife"],
        "Computer Science": ["Computer Architecture", "Number Systems", "Algorithms and Problem Solving", "Python Conditions and Loops", "Data Representation", "Digital Citizenship"],
    },
    "Class 8": {
        "Mathematics": ["Rational Numbers", "Linear Equations in One Variable", "Understanding Quadrilaterals", "Squares and Square Roots", "Cubes and Cube Roots", "Data Handling and Graphs"],
        "Science": ["Crop Production and Management", "Microorganisms", "Synthetic Fibres and Plastics", "Materials: Metals and Non-Metals", "Coal and Petroleum", "Combustion and Flame"],
        "English": ["The Best Christmas Present", "The Tsunami", "Glimpses of the Past", "Grammar in Context", "Poetry and Literary Devices", "Writing and Comprehension"],
        "History": ["How When and Where", "From Trade to Territory", "Ruling the Countryside", "Tribals Dikus and the Vision of a Golden Age", "When People Rebel", "Civilising the Native Educating the Nation"],
        "Geography": ["Resources", "Land Soil Water Natural Vegetation", "Mineral and Power Resources", "Agriculture", "Industries", "Human Resources"],
        "Computer Science": ["Algorithms and Flowcharts", "Python Programming Basics", "Conditions and Loops", "Lists and Strings", "Computer Networks", "Cybersecurity and Digital Ethics"],
    },
    "Class 9": {
        "Mathematics": ["Number Systems", "Polynomials", "Coordinate Geometry", "Linear Equations in Two Variables", "Triangles", "Statistics and Probability"],
        "Science": ["Matter in Our Surroundings", "Atoms and Molecules", "The Fundamental Unit of Life", "Tissues", "Motion", "Force and Laws of Motion"],
        "English": ["Grammar and Editing", "Reading Comprehension", "Prose Analysis", "Poetry Analysis", "Vocabulary and Usage", "Analytical and Creative Writing"],
        "History": ["The French Revolution", "Socialism in Europe and the Russian Revolution", "Nazism and the Rise of Hitler", "Forest Society and Colonialism", "Pastoralists in the Modern World", "History: Evidence and Interpretation"],
        "Geography": ["India Size and Location", "Physical Features of India", "Drainage", "Climate", "Natural Vegetation and Wildlife", "Population"],
        "Computer Science": ["Algorithms and Complexity", "Python Data Types", "Control Flow in Python", "Lists Dictionaries and Strings", "Computer Networks", "Cybersecurity and Privacy"],
    },
    "Class 10": {
        "Mathematics": ["Real Numbers", "Polynomials", "Pair of Linear Equations", "Triangles", "Introduction to Trigonometry", "Statistics and Probability"],
        "Science": ["Chemical Reactions and Equations", "Acids Bases and Salts", "Metals and Non-Metals", "Carbon and Its Compounds", "Life Processes", "Electricity"],
        "English": ["Reading Comprehension and Inference", "Grammar and Error Correction", "Literature and Theme", "Poetry and Figures of Speech", "Vocabulary and Communication", "Formal and Analytical Writing"],
        "History": ["The Rise of Nationalism in Europe", "Nationalism in India", "The Making of a Global World", "The Age of Industrialisation", "Print Culture and the Modern World", "Historical Thinking and Sources"],
        "Geography": ["Resources and Development", "Forest and Wildlife Resources", "Water Resources", "Agriculture", "Minerals and Energy Resources", "Manufacturing Industries"],
        "Computer Science": ["Python Programming and Functions", "Lists Dictionaries and Data", "SQL and Database Fundamentals", "Computer Networks and the Web", "HTML and CSS Basics", "Cybersecurity and Ethical Computing"],
    },
}

# Topic knowledge profiles. A profile contains reusable, school-appropriate concepts
# so materials/questions remain topic-specific while keeping the seed command maintainable.
PROFILES = {
    "number": {
        "focus": "number systems, place value, operations, estimation, and mathematical reasoning",
        "concepts": [
            ("Place value", "the value contributed by a digit according to its position", "In 5,482 the digit 4 has a place value of 400", "helps read, compare, and round numbers"),
            ("Factor", "a whole number that divides another number exactly", "3 is a factor of 12", "used to simplify products and fractions"),
            ("Multiple", "a number obtained by multiplying a given number by a whole number", "24 is a multiple of 6", "used in common multiples and LCM"),
            ("Prime number", "a number greater than 1 with exactly two positive factors", "13 has factors 1 and 13", "useful in prime factorisation"),
            ("Estimation", "finding a close value instead of an exact value", "49 can be estimated as 50", "useful for checking whether an answer is reasonable"),
        ],
    },
    "fraction": {
        "focus": "fractions, equivalent forms, comparison, and operations",
        "concepts": [
            ("Numerator", "the number above the fraction bar", "In 3/5, 3 is the numerator", "shows how many equal parts are selected"),
            ("Denominator", "the non-zero number below the fraction bar", "In 3/5, 5 is the denominator", "shows the number of equal parts in the whole"),
            ("Equivalent fractions", "fractions that represent the same value", "1/2 and 2/4 are equivalent", "help compare and calculate fractions"),
            ("Simplest form", "a fraction whose numerator and denominator have no common factor other than 1", "6/8 simplifies to 3/4", "keeps answers clear and standard"),
            ("Reciprocal", "the multiplicative inverse of a non-zero fraction", "the reciprocal of 2/3 is 3/2", "used when dividing fractions"),
        ],
    },
    "decimal": {
        "focus": "decimal place value, conversions, comparison, and operations",
        "concepts": [
            ("Tenths", "the first place to the right of the decimal point", "0.7 means seven tenths", "connects fractions such as 7/10 with decimals"),
            ("Hundredths", "the second place to the right of the decimal point", "0.35 has five hundredths", "used in money and precise measurements"),
            ("Terminating decimal", "a decimal with a finite number of digits", "0.75 is terminating", "can be written as a fraction with a denominator based on 10, 100, 1000, and so on"),
            ("Decimal comparison", "comparing numbers by equalising place values", "0.50 equals 0.5", "helps order measured quantities"),
            ("Conversion", "rewriting a number in another equivalent form", "0.25 = 25/100 = 1/4", "connects fractions, decimals, and percentages"),
        ],
    },
    "algebra": {
        "focus": "variables, expressions, equations, patterns, and logical manipulation",
        "concepts": [
            ("Variable", "a symbol representing an unknown or changing value", "x can represent an unknown number", "lets us write general mathematical relationships"),
            ("Coefficient", "the numerical factor multiplying a variable", "in 5x, 5 is the coefficient of x", "helps identify like terms and simplify expressions"),
            ("Constant", "a fixed number without a variable", "7 is a constant in 3x + 7", "represents a fixed quantity"),
            ("Equation", "a mathematical statement showing two expressions are equal", "2x + 3 = 11 is an equation", "can be solved to find unknown values"),
            ("Like terms", "terms with the same variables raised to the same powers", "3x and 7x are like terms", "can be combined by adding or subtracting coefficients"),
        ],
    },
    "geometry": {
        "focus": "shapes, angles, lines, properties, measurement, and spatial reasoning",
        "concepts": [
            ("Angle", "the amount of turn between two rays with a common endpoint", "90 degrees is a right angle", "measures direction and shape"),
            ("Parallel lines", "lines in the same plane that never meet", "opposite sides of a rectangle are parallel", "important in polygons and coordinate geometry"),
            ("Triangle", "a polygon with three sides and three angles", "a triangle has angle sum 180 degrees", "forms the basis of many geometric proofs"),
            ("Quadrilateral", "a polygon with four sides", "a rectangle is a quadrilateral", "has interior angle sum 360 degrees"),
            ("Symmetry", "a balanced correspondence across a line, point, or rotation", "a square has four lines of symmetry", "helps classify and design shapes"),
        ],
    },
    "statistics": {
        "focus": "collecting, organising, representing, and interpreting data",
        "concepts": [
            ("Data", "information collected for analysis", "heights of students form a data set", "supports evidence-based conclusions"),
            ("Mean", "the sum of observations divided by the number of observations", "mean of 2, 4, 6 is 4", "summarises a numerical data set"),
            ("Median", "the middle value after observations are ordered", "median of 2, 5, 8 is 5", "is useful when extreme values may distort the mean"),
            ("Mode", "the most frequently occurring value", "mode of 2, 3, 3, 5 is 3", "shows the most common observation"),
            ("Bar graph", "a chart using bars to compare categories", "a bar can show the number of students in each house", "makes category comparisons visual"),
        ],
    },
    "science": {
        "focus": "observation, evidence, scientific explanation, and relationships in the natural world",
        "concepts": [
            ("Observation", "information obtained using senses or instruments", "measuring temperature is an observation", "provides evidence for scientific reasoning"),
            ("Hypothesis", "a testable proposed explanation", "a plant may grow faster with more light", "guides investigations"),
            ("Variable", "a factor that can change in an investigation", "amount of light can be a variable", "must be controlled or measured carefully"),
            ("Evidence", "data that supports or challenges an explanation", "repeated measurements are evidence", "helps distinguish ideas from tested conclusions"),
            ("Adaptation", "a feature or behaviour that helps an organism survive", "thick fur can help in cold regions", "links organisms to their environments"),
        ],
    },
    "matter": {
        "focus": "states of matter, properties, changes, particles, and classification",
        "concepts": [
            ("Solid", "a state with definite shape and definite volume", "ice is a solid", "particles are closely packed"),
            ("Liquid", "a state with definite volume but no fixed shape", "water takes the shape of its container", "particles can flow past each other"),
            ("Gas", "a state with neither fixed shape nor fixed volume", "air is a gas", "particles are relatively far apart"),
            ("Melting", "change from solid to liquid due to heating", "ice melts to water", "is a physical change"),
            ("Evaporation", "surface change from liquid to gas", "wet clothes dry by evaporation", "can occur below the boiling point"),
        ],
    },
    "biology": {
        "focus": "cells, organisms, life processes, health, and biological relationships",
        "concepts": [
            ("Cell", "the basic structural and functional unit of life", "onion epidermis contains plant cells", "organisms are built from cells"),
            ("Tissue", "a group of similar cells performing a common function", "muscle tissue helps movement", "forms larger structures such as organs"),
            ("Organ", "a structure made of tissues working together", "the heart is an organ", "performs a specialised function"),
            ("Photosynthesis", "the process by which green plants make food using light", "plants use carbon dioxide and water to make glucose", "supports most food chains"),
            ("Respiration", "the process of releasing usable energy from food", "cells release energy from glucose", "powers cellular activities"),
        ],
    },
    "physics": {
        "focus": "motion, force, energy, light, heat, sound, and measurement",
        "concepts": [
            ("Distance", "the total path length travelled by an object", "a runner may cover 200 m", "is a scalar quantity"),
            ("Speed", "distance travelled per unit time", "speed = distance/time", "describes how fast an object moves"),
            ("Force", "a push or pull that can change motion or shape", "a kick can change a ball's motion", "measured in newtons"),
            ("Energy", "the capacity to do work or cause change", "moving objects have kinetic energy", "exists in different forms"),
            ("Reflection", "the bouncing back of light from a surface", "a mirror reflects light", "explains image formation in mirrors"),
        ],
    },
    "english": {
        "focus": "clear communication, grammar, vocabulary, reading, and writing",
        "concepts": [
            ("Noun", "a word naming a person, place, thing, or idea", "school is a noun", "helps identify subjects and objects"),
            ("Pronoun", "a word used in place of a noun", "she can replace a person's name", "reduces unnecessary repetition"),
            ("Verb", "a word expressing an action, occurrence, or state", "run is a verb", "forms the core of a predicate"),
            ("Tense", "a grammatical form showing time", "walked indicates past time", "helps readers understand when an event occurs"),
            ("Inference", "a conclusion drawn from evidence in a text", "a character carrying an umbrella may suggest rain", "supports deeper reading"),
        ],
    },
    "history": {
        "focus": "chronology, evidence, cause and effect, continuity, change, and historical interpretation",
        "concepts": [
            ("Chronology", "the arrangement of events in time order", "placing 1757 before 1857 creates chronology", "helps understand sequence and cause"),
            ("Primary source", "evidence created during the period being studied", "a contemporary letter is a primary source", "provides direct historical evidence"),
            ("Secondary source", "a later interpretation or analysis of past events", "a history textbook is a secondary source", "helps explain and compare evidence"),
            ("Cause", "a factor that contributes to an event", "economic pressure can be a cause of conflict", "helps explain why events happen"),
            ("Consequence", "an outcome that follows an event", "a law may have political consequences", "helps explain historical change"),
        ],
    },
    "geography": {
        "focus": "places, physical processes, human-environment interaction, maps, and resource use",
        "concepts": [
            ("Latitude", "angular distance north or south of the Equator", "the Equator is 0 degrees latitude", "helps locate places and understand climate"),
            ("Longitude", "angular distance east or west of the Prime Meridian", "the Prime Meridian is 0 degrees longitude", "helps locate places and determine time"),
            ("Landform", "a natural feature of Earth's surface", "mountains and plains are landforms", "reflects geological processes"),
            ("Resource", "something useful that can support human needs", "water is a natural resource", "must be managed sustainably"),
            ("Climate", "the long-term pattern of weather in a region", "a desert has a generally dry climate", "influences agriculture and settlement"),
        ],
    },
    "computer": {
        "focus": "digital literacy, algorithms, programming, data, networks, and safe technology use",
        "concepts": [
            ("Algorithm", "a finite sequence of clear steps for solving a problem", "steps for making tea can be written as an algorithm", "provides a plan before coding"),
            ("Variable", "a named storage location whose value can change", "age = 15 stores a value in age", "allows programs to work with changing data"),
            ("Loop", "a programming construct that repeats instructions", "a for loop can print numbers 1 to 10", "reduces repeated code"),
            ("Network", "a system connecting devices to communicate and share resources", "a school LAN connects classroom computers", "enables communication and resource sharing"),
            ("Cybersecurity", "practices that protect systems, data, and users from digital threats", "using strong passwords improves security", "reduces the risk of unauthorised access"),
        ],
    },
}

PROFILE_ALIASES = [
    ("fraction", "fraction"), ("decimal", "decimal"), ("linear equations", "algebra"), ("equations", "algebra"),
    ("polynomial", "algebra"), ("algebra", "algebra"), ("rational", "fraction"), ("real numbers", "number"), ("number systems", "number"),
    ("square", "geometry"), ("cube", "geometry"), ("triangle", "geometry"), ("quadrilateral", "geometry"), ("geometry", "geometry"),
    ("trigonometry", "geometry"), ("statistics", "statistics"), ("probability", "statistics"), ("data", "statistics"),
    ("crop", "biology"), ("microorgan", "biology"), ("human body", "biology"), ("plant", "biology"), ("animals", "biology"),
    ("life", "biology"), ("cell", "biology"), ("tissue", "biology"), ("matter", "matter"), ("metals", "matter"), ("carbon", "matter"),
    ("acid", "matter"), ("chemical", "matter"), ("heat", "physics"), ("motion", "physics"), ("force", "physics"), ("electric", "physics"),
    ("light", "physics"), ("weather", "geography"), ("climate", "geography"), ("water", "geography"), ("earth", "geography"),
    ("resource", "geography"), ("map", "geography"), ("grammar", "english"), ("tense", "english"), ("reading", "english"),
    ("writing", "english"), ("poetry", "english"), ("literature", "english"), ("history", "history"), ("revolution", "history"),
    ("empire", "history"), ("kingdom", "history"), ("colonial", "history"), ("algorithm", "computer"), ("python", "computer"),
    ("programming", "computer"), ("network", "computer"), ("cyber", "computer"), ("database", "computer"), ("html", "computer"),
]

SUBJECT_PROFILES = {
    "Mathematics": "number", "Science": "science", "English": "english", "History": "history", "Geography": "geography", "Computer Science": "computer"
}

DIFFICULTIES = ["easy", "easy", "medium", "medium", "hard"]


def profile_for(subject, title):
    low = title.lower()
    for needle, profile in PROFILE_ALIASES:
        if needle in low:
            return PROFILES[profile]
    return PROFILES[SUBJECT_PROFILES[subject]]


def material_for(class_name, subject, topic, profile):
    concept_lines = []
    for term, definition, example, use in profile["concepts"]:
        concept_lines.append(
            f"### {term}\n{definition.capitalize()}.\nExample: {example}.\nWhy it matters: {use}."
        )
    return (
        f"# {class_name} • {subject} • {topic}\n\n"
        f"## Learning Goal\nThis topic develops {profile['focus']}. Students should be able to define key ideas, explain them in their own words, solve or analyse basic problems, and apply the ideas to familiar situations.\n\n"
        "## Core Concepts\n" + "\n\n".join(concept_lines) + "\n\n"
        "## Study Strategy\n"
        "1. Read the definition of each key term.\n"
        "2. Rewrite the idea in your own words.\n"
        "3. Work through the example without looking at the answer.\n"
        "4. Create one real-life example of the concept.\n"
        "5. Practise the question bank and review every incorrect answer.\n\n"
        "## Common Mistakes to Avoid\n"
        "- Memorising a definition without understanding the example.\n"
        "- Skipping units, signs, conditions, or important words in the question.\n"
        "- Giving a final answer without checking whether it is reasonable.\n"
        "- Confusing a related term with the exact term asked in the question.\n\n"
        "## Exam Focus\n"
        "Expect definition, identification, application, comparison, reasoning, and short problem-solving questions. For higher difficulty questions, combine two or more concepts and justify the answer with evidence or a calculation.\n\n"
        "## Quick Revision\n"
        + "; ".join(term for term, *_ in profile["concepts"]) + ".\n"
    )


def _rotated_options(correct, distractors, shift):
    options = [correct] + list(distractors[:3])
    shift = shift % 4
    rotated = options[shift:] + options[:shift]
    letters = ["A", "B", "C", "D"]
    return rotated, letters[rotated.index(correct)]


def build_questions(chapter, profile, topic):
    concepts = profile["concepts"]
    questions = []
    # Four question forms per concept = exactly 20 questions per topic.
    for idx, (term, definition, example, use) in enumerate(concepts):
        others = [c for j, c in enumerate(concepts) if j != idx]

        # 1: definition identification
        opts, correct = _rotated_options(term, [c[0] for c in others], idx)
        questions.append((
            f"Which term best matches this description: {definition}?",
            opts, correct, f"The correct term is {term} because it means {definition}.", DIFFICULTIES[idx % len(DIFFICULTIES)]
        ))

        # 2: example identification
        distractors = [c[2] for c in others]
        opts, correct = _rotated_options(example, distractors, idx + 1)
        questions.append((
            f"Which statement is the correct example or application of {term}?",
            opts, correct, f"{example} is the correct example for {term}.", DIFFICULTIES[(idx + 1) % len(DIFFICULTIES)]
        ))

        # 3: purpose/application
        distractors = [c[3] for c in others]
        opts, correct = _rotated_options(use, distractors, idx + 2)
        questions.append((
            f"Why is {term} important when studying {topic}?",
            opts, correct, f"{use.capitalize()}.", DIFFICULTIES[(idx + 2) % len(DIFFICULTIES)]
        ))

        # 4: distinguish from another concept
        other_term = concepts[(idx + 1) % len(concepts)][0]
        other_def = concepts[(idx + 1) % len(concepts)][1]
        third_def = concepts[(idx + 2) % len(concepts)][1]
        distractors = [other_def, third_def, "It has no accepted meaning in the topic"]
        opts, correct = _rotated_options(definition, distractors, idx + 3)
        questions.append((
            f"Which statement correctly describes {term}, rather than {other_term}?",
            opts, correct, f"{term} is defined as {definition}. {other_term} instead means {other_def}.", "hard"
        ))
    return questions


@transaction.atomic
def seed():
    stats = {"classes": 0, "subjects": 0, "chapters": 0, "materials": 0, "questions": 0, "quizzes": 0}
    for class_name, subjects in CLASSES.items():
        class_obj, _ = ClassLevel.objects.update_or_create(
            name=class_name,
            defaults={"description": f"Comprehensive learning programme for {class_name}."},
        )
        stats["classes"] += 1
        for subject_name, topics in subjects.items():
            subject_obj, _ = Subject.objects.update_or_create(
                name=subject_name, class_level=class_obj,
                defaults={"description": f"Structured {subject_name} curriculum for {class_name}."},
            )
            stats["subjects"] += 1
            for order, topic in enumerate(topics, start=1):
                chapter, _ = Chapter.objects.update_or_create(
                    subject=subject_obj, title=topic,
                    defaults={"description": f"Important concepts, advanced study notes, and assessment preparation for {topic}.", "order": order},
                )
                stats["chapters"] += 1
                profile = profile_for(subject_name, topic)
                StudyMaterial.objects.update_or_create(
                    chapter=chapter,
                    title=f"Advanced Study Material — {topic}",
                    defaults={
                        "description": f"Detailed study notes for {class_name} {subject_name}: {topic}.",
                        "content": material_for(class_name, subject_name, topic, profile),
                    },
                )
                stats["materials"] += 1

                for old in Question.objects.filter(chapter=chapter):
                    # Keep the chapter clean so every run produces exactly 20 current questions.
                    old.delete()
                qs = []
                for qtext, opts, correct, explanation, difficulty in build_questions(chapter, profile, topic):
                    qs.append(Question.objects.create(
                        chapter=chapter,
                        question_text=qtext,
                        option_a=opts[0], option_b=opts[1], option_c=opts[2], option_d=opts[3],
                        correct_answer=correct, explanation=explanation, difficulty=difficulty,
                    ))
                stats["questions"] += len(qs)

                Quiz.objects.filter(chapter=chapter).delete()
                quiz = Quiz.objects.create(
                    title=f"20-Question Quiz — {topic}",
                    chapter=chapter,
                    description=f"Important 20-question assessment for {class_name} {subject_name}: {topic}. Includes easy, medium, and hard questions.",
                    time_limit=25,
                    total_marks=20,
                )
                QuizQuestion.objects.bulk_create([
                    QuizQuestion(quiz=quiz, question=q, order=i, marks=1)
                    for i, q in enumerate(qs, start=1)
                ])
                stats["quizzes"] += 1

    return stats


class Command(BaseCommand):
    help = "Seed a full Class 5-10, six-subject curriculum with advanced materials, 20 questions per topic, and 20-question quizzes."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Building comprehensive Siksha Sahayak curriculum..."))
        stats = seed()
        self.stdout.write(self.style.SUCCESS("\n✅ Curriculum build complete."))
        for key, value in stats.items():
            self.stdout.write(f"   {key.capitalize():<10}: {value}")
        self.stdout.write(self.style.SUCCESS(
            "\nEach topic now has one advanced study material, exactly 20 question-bank entries, and a 20-question quiz."
        ))
