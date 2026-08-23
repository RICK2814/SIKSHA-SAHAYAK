from django.core.management.base import BaseCommand
from materials.models import ClassLevel, Subject, Chapter, StudyMaterial
from assessments.models import Question, Quiz, QuizQuestion

class Command(BaseCommand):
    help = "Seed the database with complete sample data for Siksha Sahayak"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding complete data..."))

        # 1. Create Classes
        classes_data = [
            ("Class 5", "Fifth Grade"),
            ("Class 6", "Sixth Grade"),
            ("Class 7", "Seventh Grade"),
            ("Class 8", "Eighth Grade"),
            ("Class 9", "Ninth Grade"),
            ("Class 10", "Tenth Grade"),
        ]
        class_objects = {}
        for name, desc in classes_data:
            obj, _ = ClassLevel.objects.get_or_create(name=name, defaults={"description": desc})
            class_objects[name] = obj
            self.stdout.write(f"  Class: {name}")

        # 2. Create Subjects for Class 8
        c8 = class_objects["Class 8"]
        subjects_data = [
            ("Mathematics", "Study of numbers, shapes, and patterns"),
            ("Science", "Study of the natural world"),
            ("English", "Study of English language and literature"),
            ("History", "Study of past events"),
            ("Geography", "Study of Earth and its features"),
            ("Computer Science", "Study of computers and computing"),
        ]
        subject_objects = {}
        for name, desc in subjects_data:
            obj, _ = Subject.objects.get_or_create(name=name, class_level=c8, defaults={"description": desc})
            subject_objects[name] = obj
            self.stdout.write(f"  Subject: {name}")

        # 3. Create Chapters
        chapters_data = [
            ("Mathematics", "Chapter 1 - Rational Numbers", 1, "Understanding rational numbers and their properties"),
            ("Mathematics", "Chapter 2 - Linear Equations", 2, "Solving linear equations in one variable"),
            ("Mathematics", "Chapter 3 - Understanding Quadrilaterals", 3, "Properties of different quadrilaterals"),
            ("Science", "Chapter 1 - Crop Production", 1, "Methods of crop production and management"),
            ("Science", "Chapter 2 - Microorganisms", 2, "Friends and foes of microorganisms"),
            ("Science", "Chapter 3 - Synthetic Fibres", 3, "Types and uses of synthetic fibres"),
            ("English", "Chapter 1 - The Best Christmas Present", 1, "A heartwarming story about Christmas"),
            ("English", "Chapter 2 - The Tsunami", 2, "Story of courage during the tsunami"),
            ("History", "Chapter 1 - How, When and Where", 1, "Understanding how history is recorded"),
            ("History", "Chapter 2 - From Trade to Territory", 2, "The East India Company in India"),
            ("Geography", "Chapter 1 - Resources", 1, "Types and development of resources"),
            ("Geography", "Chapter 2 - Land, Soil, Water", 2, "Natural resources and conservation"),
            ("Computer Science", "Chapter 1 - Algorithms", 1, "Introduction to algorithms and flowcharts"),
            ("Computer Science", "Chapter 2 - Programming in Python", 2, "Basics of Python programming"),
        ]
        chapter_objects = {}
        for subj_name, title, order, desc in chapters_data:
            subj = subject_objects[subj_name]
            obj, _ = Chapter.objects.get_or_create(subject=subj, title=title, defaults={"order": order, "description": desc})
            chapter_objects[title] = obj
            self.stdout.write(f"  Chapter: {title}")

        # 4. Create Study Materials for ALL chapters
        materials_data = []
        # Mathematics - Chapter 1: Rational Numbers
        materials_data.append(("Chapter 1 - Rational Numbers", "Introduction to Rational Numbers", "Basic concepts of rational numbers.",
            "A rational number is a number that can be expressed in the form p/q, where p and q are integers and q is not equal to 0.\n\n"
            "Key Properties:\n"
            "- Every integer is a rational number (e.g., 5 = 5/1)\n"
            "- Rational numbers can be positive or negative\n"
            "- Zero is also a rational number (0 = 0/1)\n\n"
            "Examples: 1/2, -3/4, 7, 0, -2/5\n\n"
            "A rational number is in standard form if its denominator is positive and the numerator and denominator have no common factors other than 1."))

        materials_data.append(("Chapter 1 - Rational Numbers", "Operations on Rational Numbers", "How to add, subtract, multiply and divide rational numbers.",
            "Addition: To add two rational numbers with the same denominator, add the numerators and keep the denominator same.\n"
            "Example: 1/4 + 2/4 = 3/4\n\n"
            "Subtraction: Similar to addition, subtract the numerators.\n"
            "Example: 3/5 - 1/5 = 2/5\n\n"
            "Multiplication: Multiply numerators and denominators separately.\n"
            "Example: 2/3 x 3/5 = 6/15 = 2/5\n\n"
            "Division: Multiply by the reciprocal of the divisor.\n"
            "Example: 2/3 / 4/5 = 2/3 x 5/4 = 10/12 = 5/6"))

        materials_data.append(("Chapter 1 - Rational Numbers", "Representation on Number Line", "How to represent rational numbers on a number line.",
            "Rational numbers can be represented on a number line just like integers.\n\n"
            "Steps to represent a rational number on number line:\n"
            "1. Draw a number line and mark 0 in the middle.\n"
            "2. Divide the segment between two integers into equal parts based on the denominator.\n"
            "3. Count the parts according to the numerator from 0.\n\n"
            "Example: To represent 3/4, divide the segment between 0 and 1 into 4 equal parts and mark the 3rd part."))

        # Mathematics - Chapter 2: Linear Equations
        materials_data.append(("Chapter 2 - Linear Equations", "Introduction to Linear Equations", "Understanding linear equations in one variable.",
            "A linear equation in one variable is an equation that can be written in the form ax + b = 0, where a and b are constants and a is not 0.\n\n"
            "Steps to solve:\n"
            "1. Simplify both sides of the equation\n"
            "2. Move variable terms to one side and constants to the other\n"
            "3. Divide by the coefficient of the variable\n\n"
            "Example: Solve 2x + 5 = 15\n"
            "2x = 15 - 5\n"
            "2x = 10\n"
            "x = 5"))

        materials_data.append(("Chapter 2 - Linear Equations", "Word Problems", "Solving real-life problems using linear equations.",
            "Linear equations can be used to solve many real-life problems.\n\n"
            "Example 1: The sum of two numbers is 50. If one number is 10 more than the other, find the numbers.\n"
            "Let the smaller number be x. Then the larger number is x + 10.\n"
            "x + (x + 10) = 50\n"
            "2x + 10 = 50\n"
            "2x = 40\n"
            "x = 20\n"
            "So the numbers are 20 and 30.\n\n"
            "Example 2: A man is 4 times as old as his son. After 5 years, he will be 3 times as old as his son. Find their present ages.\n"
            "Let sons age be x. Then fathers age is 4x.\n"
            "4x + 5 = 3(x + 5)\n"
            "4x + 5 = 3x + 15\n"
            "x = 10\n"
            "Son is 10 years old, father is 40 years old."))

        # Mathematics - Chapter 3: Understanding Quadrilaterals
        materials_data.append(("Chapter 3 - Understanding Quadrilaterals", "Types of Quadrilaterals", "Learn about different types of quadrilaterals.",
            "A quadrilateral is a polygon with four sides and four angles. The sum of all interior angles of a quadrilateral is 360 degrees.\n\n"
            "Types of Quadrilaterals:\n\n"
            "1. Parallelogram: Both pairs of opposite sides are parallel. Opposite sides are equal, opposite angles are equal, diagonals bisect each other.\n\n"
            "2. Rectangle: A parallelogram with all angles equal to 90 degrees. Diagonals are equal in length.\n\n"
            "3. Square: A rectangle with all sides equal. All angles are 90 degrees, diagonals are equal and bisect at 90 degrees.\n\n"
            "4. Rhombus: A parallelogram with all sides equal. Diagonals bisect each other at 90 degrees.\n\n"
            "5. Trapezium: A quadrilateral with one pair of parallel sides.\n\n"
            "6. Kite: A quadrilateral with two distinct pairs of adjacent sides equal."))

        materials_data.append(("Chapter 3 - Understanding Quadrilaterals", "Properties of Parallelogram", "Detailed properties of parallelograms.",
            "Properties of a Parallelogram:\n\n"
            "1. Opposite sides are equal in length.\n"
            "2. Opposite angles are equal in measure.\n"
            "3. Consecutive angles are supplementary (add up to 180 degrees).\n"
            "4. Diagonals bisect each other.\n"
            "5. Each diagonal divides the parallelogram into two congruent triangles.\n\n"
            "Example: In parallelogram ABCD, if angle A = 70 degrees, then angle C = 70 degrees and angle B = angle D = 110 degrees."))

        # Science - Chapter 1: Crop Production
        materials_data.append(("Chapter 1 - Crop Production", "Agricultural Practices", "Basic practices for growing crops.",
            "Agricultural practices include all activities involved in growing crops. The main steps are:\n\n"
            "1. Preparation of Soil: Tilling and loosening the soil to allow roots to penetrate and water to be retained.\n\n"
            "2. Sowing: Placing seeds in the soil at appropriate depth and distance.\n\n"
            "3. Adding Manure and Fertilizers: To provide nutrients to the crops.\n\n"
            "4. Irrigation: Supplying water to crops at regular intervals.\n\n"
            "5. Weeding: Removing unwanted plants that compete with crops.\n\n"
            "6. Harvesting: Cutting and gathering mature crops.\n\n"
            "7. Storage: Keeping harvested grains safe from pests and moisture."))

        materials_data.append(("Chapter 1 - Crop Production", "Types of Crops", "Kharif and Rabi crops explained.",
            "Crops in India are classified into two main types based on the season:\n\n"
            "1. Kharif Crops: Grown during the monsoon season (June to October).\n"
            "   Examples: Rice, Maize, Cotton, Groundnut, Soybean\n\n"
            "2. Rabi Crops: Grown during the winter season (October to March).\n"
            "   Examples: Wheat, Barley, Peas, Gram, Mustard\n\n"
            "Kharif crops need a lot of water and warm weather. Rabi crops need cool climate and less water."))

        # Science - Chapter 2: Microorganisms
        materials_data.append(("Chapter 2 - Microorganisms", "Useful Microorganisms", "How microorganisms help us in daily life.",
            "Microorganisms are beneficial in many ways:\n\n"
            "1. Making Curd and Cheese: Bacteria like Lactobacillus convert milk into curd.\n\n"
            "2. Baking: Yeast is used to make bread fluffy by producing carbon dioxide.\n\n"
            "3. Alcohol Production: Yeast ferments sugar to produce alcohol.\n\n"
            "4. Medicine Production: Antibiotics like penicillin are made from fungi.\n\n"
            "5. Nitrogen Fixation: Bacteria in legume roots convert atmospheric nitrogen into usable form.\n\n"
            "6. Decomposition: Bacteria and fungi decompose dead organic matter, recycling nutrients."))

        materials_data.append(("Chapter 2 - Microorganisms", "Harmful Microorganisms", "Diseases caused by microorganisms.",
            "Some microorganisms cause diseases in humans, animals and plants. These are called pathogens.\n\n"
            "Diseases caused by Bacteria:\n"
            "- Tuberculosis (TB)\n"
            "- Cholera\n"
            "- Typhoid\n"
            "- Tetanus\n\n"
            "Diseases caused by Viruses:\n"
            "- Common Cold\n"
            "- Influenza (Flu)\n"
            "- Chickenpox\n"
            "- COVID-19\n\n"
            "Diseases caused by Protozoa:\n"
            "- Malaria\n"
            "- Amoebiasis\n\n"
            "Diseases caused by Fungi:\n"
            "- Ringworm\n"
            "- Athletes foot"))

        # Science - Chapter 3: Synthetic Fibres
        materials_data.append(("Chapter 3 - Synthetic Fibres", "Types of Fibres", "Natural and synthetic fibres compared.",
            "Fibres are thread-like structures that can be spun into yarn and woven into fabric.\n\n"
            "Natural Fibres:\n"
            "- Cotton: Obtained from cotton plants. Soft, breathable, absorbent.\n"
            "- Wool: Obtained from sheep. Warm, insulating.\n"
            "- Silk: Obtained from silkworms. Smooth, shiny, strong.\n"
            "- Jute: Obtained from jute plants. Strong, coarse.\n\n"
            "Synthetic Fibres:\n"
            "- Nylon: Strong, elastic, used in socks, ropes, parachutes.\n"
            "- Polyester: Durable, wrinkle-resistant, used in shirts, bottles.\n"
            "- Acrylic: Wool-like, lightweight, used in sweaters.\n"
            "- Rayon: Semi-synthetic, soft, used in dresses."))

        materials_data.append(("Chapter 3 - Synthetic Fibres", "Plastics", "Properties and uses of plastics.",
            "Plastic is a synthetic material that can be molded into any shape.\n\n"
            "Properties of Plastics:\n"
            "1. Lightweight and strong\n"
            "2. Poor conductors of heat and electricity\n"
            "3. Non-reactive to chemicals\n"
            "4. Can be molded into any shape\n"
            "5. Durable and long-lasting\n\n"
            "Types of Plastics:\n"
            "1. Thermoplastics: Can be melted and reshaped. Example: Polythene, PVC, Polystyrene.\n"
            "2. Thermosetting Plastics: Cannot be remelted. Example: Bakelite, Melamine.\n\n"
            "Plastic Pollution: Plastics are non-biodegradable. They cause soil and water pollution. We should reduce, reuse and recycle plastics."))

        # English - Chapter 1: The Best Christmas Present
        materials_data.append(("Chapter 1 - The Best Christmas Present", "Summary", "A summary of the heartwarming story.",
            "The story is set during World War I. On Christmas morning, soldiers from opposing armies (British and German) come out of their trenches and celebrate Christmas together in No Mans Land. They play football, share food, and sing carols. This shows that even in the midst of war, humanity and goodwill can prevail. The author describes this moment as the best Christmas present - the gift of peace and friendship.\n\n"
            "Key Characters:\n"
            "- British soldiers\n"
            "- German soldiers\n"
            "- The officers who allowed the truce\n\n"
            "Theme: Peace, humanity, and the spirit of Christmas can overcome hatred and war."))

        materials_data.append(("Chapter 1 - The Best Christmas Present", "Important Questions", "Questions and answers for exam preparation.",
            "Q1. When and where is the story set?\n"
            "Ans: The story is set during World War I on Christmas morning.\n\n"
            "Q2. What did the soldiers do in No Mans Land?\n"
            "Ans: The soldiers from both sides came out of their trenches, shook hands, exchanged gifts, played football, and celebrated Christmas together.\n\n"
            "Q3. Why is it called the best Christmas present?\n"
            "Ans: Because the soldiers experienced peace and friendship even during war, which was the greatest gift they could receive.\n\n"
            "Q4. What does the story teach us?\n"
            "Ans: The story teaches us that humanity and goodwill can overcome hatred and war."))

        # English - Chapter 2: The Tsunami
        materials_data.append(("Chapter 2 - The Tsunami", "Summary", "Story of courage during the 2004 tsunami.",
            "The Tsunami is a story about the devastating earthquake and tsunami that hit the Indian Ocean on December 26, 2004. The chapter describes the experiences of people who survived the disaster and shows acts of courage and kindness during the tragedy.\n\n"
            "Key Stories:\n"
            "1. Ignesious and his family tried to save themselves when the earthquake struck.\n"
            "2. Sanjeev, a policeman, saved many lives but lost his own.\n"
            "3. Meghna was swept away by the waves but survived by holding onto a wooden door.\n"
            "4. Almas lost her entire family but was saved by a hospital.\n"
            "5. Tilly Smith, a 10-year-old British girl, recognized the signs of a tsunami and saved many lives on a beach in Thailand.\n\n"
            "Theme: Courage, survival, and the power of knowledge."))

        materials_data.append(("Chapter 2 - The Tsunami", "Important Questions", "Questions and answers for exam preparation.",
            "Q1. Who was Tilly Smith?\n"
            "Ans: Tilly Smith was a 10-year-old British girl who recognized the signs of a tsunami from a geography lesson and warned people on a beach in Thailand, saving many lives.\n\n"
            "Q2. What were the signs of the approaching tsunami?\n"
            "Ans: The water receded from the shore, exposing the sea floor. The sea bubbled and made a loud roaring sound.\n\n"
            "Q3. How did animals sense the tsunami before humans?\n"
            "Ans: Animals have a sixth sense that helps them detect natural disasters. Many animals ran to higher ground before the tsunami hit.\n\n"
            "Q4. What lesson do we learn from this chapter?\n"
            "Ans: Knowledge and awareness can save lives during natural disasters."))

        # History - Chapter 1: How, When and Where
        materials_data.append(("Chapter 1 - How, When and Where", "Recording History", "How do we know about the past?",
            "History is recorded through various sources:\n\n"
            "1. Written Records: Official documents, letters, diaries, and books.\n\n"
            "2. Oral Traditions: Stories passed down through generations.\n\n"
            "3. Archaeological Evidence: Buildings, coins, inscriptions, and artifacts.\n\n"
            "4. Visual Sources: Paintings, photographs, and films.\n\n"
            "British historians in India divided history into three periods:\n"
            "- Ancient\n"
            "- Medieval\n"
            "- Modern\n\n"
            "This division was based on the belief that British rule represented modernity.\n\n"
            "James Mill, a Scottish economist and political philosopher, published A History of British India in 1817. He divided Indian history into Hindu, Muslim, and British periods."))

        materials_data.append(("Chapter 1 - How, When and Where", "Important Dates", "Key dates in Indian history.",
            "Important Dates:\n\n"
            "1600: East India Company gets charter from Queen Elizabeth I\n"
            "1764: Battle of Buxar\n"
            "1765: East India Company gets Diwani rights\n"
            "1857: The Revolt (First War of Independence)\n"
            "1858: British Crown takes over India\n"
            "1885: Indian National Congress founded\n"
            "1906: Muslim League founded\n"
            "1947: India gains independence\n\n"
            "Archives: Places where historical documents are preserved. The National Archives of India is in New Delhi."))

        # History - Chapter 2: From Trade to Territory
        materials_data.append(("Chapter 2 - From Trade to Territory", "The East India Company", "How the East India Company came to rule India.",
            "The East India Company was established in 1600 with a royal charter from Queen Elizabeth I. Initially, it came to India for trade in spices, cotton, and silk.\n\n"
            "How Trade Led to Territory:\n\n"
            "1. The Company set up trading posts called factories in Surat, Madras, Bombay, and Calcutta.\n\n"
            "2. After the Battle of Plassey (1757), the Company gained control over Bengal.\n\n"
            "3. After the Battle of Buxar (1764), the Company got the Diwani rights (right to collect revenue) of Bengal, Bihar, and Orissa.\n\n"
            "4. The Company used subsidiary alliances to bring Indian states under its control.\n\n"
            "5. By 1857, the Company ruled most of India."))

        materials_data.append(("Chapter 2 - From Trade to Territory", "Important Battles", "Key battles that changed Indian history.",
            "Battle of Plassey (1757):\n"
            "- Fought between Siraj-ud-Daulah (Nawab of Bengal) and Robert Clive.\n"
            "- The Nawab was betrayed by Mir Jafar.\n"
            "- British victory led to control over Bengal.\n\n"
            "Battle of Buxar (1764):\n"
            "- Fought between the British and a combined army of Mir Qasim, Shuja-ud-Daulah, and Shah Alam II.\n"
            "- British victory gave them Diwani rights.\n\n"
            "Subsidiary Alliance:\n"
            "- Introduced by Lord Wellesley.\n"
            "- Indian rulers had to accept British troops in their territory and pay for them.\n"
            "- The British would protect the ruler from external and internal threats."))

        # Geography - Chapter 1: Resources
        materials_data.append(("Chapter 1 - Resources", "Types of Resources", "Understanding natural, human-made and human resources.",
            "Resources are classified into three types:\n\n"
            "1. Natural Resources: Resources obtained from nature like air, water, soil, minerals, forests.\n\n"
            "2. Human-made Resources: Resources created by humans using natural resources like buildings, roads, machinery.\n\n"
            "3. Human Resources: People and their skills, knowledge, and abilities.\n\n"
            "Sustainable development means using resources wisely so that future generations can also use them. We must conserve our resources through:\n"
            "- Reducing consumption\n"
            "- Reusing items\n"
            "- Recycling materials"))

        materials_data.append(("Chapter 1 - Resources", "Conservation of Resources", "Why and how to conserve resources.",
            "Resource conservation is the practice of using resources carefully and giving them time to get renewed.\n\n"
            "Why conserve resources?\n"
            "1. Resources are limited\n"
            "2. Overuse leads to depletion\n"
            "3. Future generations need them\n"
            "4. Conservation protects the environment\n\n"
            "Methods of Conservation:\n"
            "1. Water Conservation: Rainwater harvesting, drip irrigation, fixing leaks\n"
            "2. Soil Conservation: Terrace farming, contour ploughing, afforestation\n"
            "3. Forest Conservation: Afforestation, banning deforestation, wildlife sanctuaries\n"
            "4. Energy Conservation: Using solar energy, LED bulbs, turning off unused appliances\n\n"
            "The 3 Rs of Conservation:\n"
            "- Reduce: Use less\n"
            "- Reuse: Use again\n"
            "- Recycle: Convert waste into useful products"))

        # Geography - Chapter 2: Land, Soil, Water
        materials_data.append(("Chapter 2 - Land, Soil, Water", "Land Resources", "How land is used in India.",
            "Land is one of the most important natural resources. In India, land is used for various purposes:\n\n"
            "1. Agriculture: About 43% of land is used for farming. India has fertile plains in the north and black soil in the Deccan plateau.\n\n"
            "2. Forests: About 22% of land is under forests. The government aims to have 33% forest cover.\n\n"
            "3. Pastures: Land used for grazing animals.\n\n"
            "4. Built-up Areas: Land used for houses, roads, industries, and cities.\n\n"
            "5. Wasteland: Land that cannot be used for agriculture or other purposes.\n\n"
            "Land Degradation: The process by which fertile land becomes desert-like. Causes include deforestation, overgrazing, and excessive use of fertilizers."))

        materials_data.append(("Chapter 2 - Land, Soil, Water", "Soil Conservation", "Types of soil and how to protect them.",
            "Soil is the thin layer of material on the Earths surface that supports plant growth.\n\n"
            "Types of Soil in India:\n"
            "1. Alluvial Soil: Found in river plains (Ganga, Brahmaputra). Very fertile, good for wheat and rice.\n\n"
            "2. Black Soil: Found in Deccan plateau. Good for cotton (also called black cotton soil).\n\n"
            "3. Red Soil: Found in Tamil Nadu, Karnataka, Andhra Pradesh. Good for millets and groundnuts.\n\n"
            "4. Laterite Soil: Found in tropical regions with heavy rainfall. Good for tea, coffee, and cashew.\n\n"
            "5. Mountain Soil: Found in hilly areas. Good for forests and orchards.\n\n"
            "Soil Conservation Methods:\n"
            "- Terrace farming on slopes\n"
            "- Contour ploughing\n"
            "- Crop rotation\n"
            "- Afforestation\n"
            "- Avoiding overgrazing"))

        # Computer Science - Chapter 1: Algorithms
        materials_data.append(("Chapter 1 - Algorithms", "What is an Algorithm?", "Introduction to step-by-step problem solving.",
            "An algorithm is a step-by-step procedure to solve a problem or accomplish a task. Characteristics of a good algorithm:\n\n"
            "1. Input: It should take zero or more inputs.\n"
            "2. Output: It should produce at least one output.\n"
            "3. Definiteness: Each step must be clear and unambiguous.\n"
            "4. Finiteness: It must terminate after a finite number of steps.\n"
            "5. Effectiveness: Each step must be basic enough to be carried out.\n\n"
            "Example: Algorithm to add two numbers\n"
            "Step 1: Start\n"
            "Step 2: Read numbers A and B\n"
            "Step 3: Calculate SUM = A + B\n"
            "Step 4: Display SUM\n"
            "Step 5: Stop\n\n"
            "Flowcharts: A visual representation of an algorithm using symbols like rectangles (process), diamonds (decision), and arrows (flow)."))

        materials_data.append(("Chapter 1 - Algorithms", "Types of Algorithms", "Different types of algorithms and their uses.",
            "Types of Algorithms:\n\n"
            "1. Sequential Algorithm: Steps are executed one after another in order.\n\n"
            "2. Conditional Algorithm: Uses decision-making (if-else).\n"
            "   Example: Check if a number is even or odd.\n\n"
            "3. Looping Algorithm: Uses repetition (for, while loops).\n"
            "   Example: Print numbers from 1 to 10.\n\n"
            "4. Recursive Algorithm: A function that calls itself.\n"
            "   Example: Calculate factorial of a number.\n\n"
            "Pseudocode: A simplified way of writing algorithms using plain English and programming-like structure.\n\n"
            "Example Pseudocode for finding the largest number:\n"
            "START\n"
            "READ A, B, C\n"
            "IF A > B AND A > C THEN\n"
            "   DISPLAY A is largest\n"
            "ELSE IF B > C THEN\n"
            "   DISPLAY B is largest\n"
            "ELSE\n"
            "   DISPLAY C is largest\n"
            "END IF\n"
            "STOP"))

        # Computer Science - Chapter 2: Programming in Python
        materials_data.append(("Chapter 2 - Programming in Python", "Introduction to Python", "Getting started with Python programming.",
            "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991. It is known for its simple syntax and readability.\n\n"
            "Features of Python:\n"
            "1. Easy to learn and read\n"
            "2. Free and open-source\n"
            "3. Platform independent (runs on Windows, Mac, Linux)\n"
            "4. Large standard library\n"
            "5. Supports multiple programming paradigms\n\n"
            "Writing your first Python program:\n"
            "print(Hello World)\n\n"
            "Variables in Python:\n"
            "name = Alice\n"
            "age = 14\n"
            "height = 5.4\n\n"
            "Data Types:\n"
            "- int: Integer numbers (e.g., 10, -5)\n"
            "- float: Decimal numbers (e.g., 3.14, -0.5)\n"
            "- str: Text strings (e.g., Hello)\n"
            "- bool: True or False\n"
            "- list: Ordered collection (e.g., [1, 2, 3])"))

        materials_data.append(("Chapter 2 - Programming in Python", "Python Control Structures", "If-else, loops and functions in Python.",
            "If-Else Statement:\n"
            "age = 16\n"
            "if age >= 18:\n"
            "    print(You are an adult)\n"
            "else:\n"
            "    print(You are a minor)\n\n"
            "For Loop:\n"
            "for i in range(5):\n"
            "    print(i)\n"
            "Output: 0, 1, 2, 3, 4\n\n"
            "While Loop:\
"
            "count = 0\n"
            "while count < 5:\n"
            "    print(count)\n"
            "    count = count + 1\n\n"
            "Functions:\n"
            "def greet(name):\n"
            "    return Hello + name\n\n"
            "message = greet(Alice)\n"
            "print(message)\n"
            "Output: Hello Alice\n\n"
            "Lists in Python:\n"
            "fruits = [apple, banana, cherry]\n"
            "print(fruits[0])  # Output: apple\n"
            "fruits.append(date)\n"
            "print(fruits)  # Output: [apple, banana, cherry, date]"))

        # Save all materials
        for ch_title, mat_title, desc, content in materials_data:
            ch = chapter_objects[ch_title]
            StudyMaterial.objects.get_or_create(
                chapter=ch, title=mat_title,
                defaults={"description": desc, "content": content}
            )
            self.stdout.write(f"  Material: {mat_title}")

        # 5. Create Questions
        questions_data = [
            # Mathematics - Rational Numbers
            ("Chapter 1 - Rational Numbers", "What is the standard form of 12/18?", "B", "6/9", "2/3", "3/2", "18/12", "Divide numerator and denominator by GCD(12,18)=6. So 12/18 = 2/3.", "easy"),
            ("Chapter 1 - Rational Numbers", "Which of the following is NOT a rational number?", "B", "0", "1/0", "-5/2", "3.14", "1/0 is undefined because division by zero is not allowed.", "easy"),
            ("Chapter 1 - Rational Numbers", "The additive inverse of -3/7 is:", "A", "3/7", "-3/7", "7/3", "-7/3", "Additive inverse of a number is the number that when added gives zero. -3/7 + 3/7 = 0.", "easy"),
            ("Chapter 1 - Rational Numbers", "What is 3/4 + 1/4?", "C", "1/2", "4/8", "1", "3/16", "3/4 + 1/4 = (3+1)/4 = 4/4 = 1", "easy"),
            ("Chapter 1 - Rational Numbers", "The reciprocal of -2/5 is:", "C", "2/5", "5/2", "-5/2", "2/-5", "Reciprocal of a/b is b/a. So reciprocal of -2/5 is -5/2.", "medium"),
            ("Chapter 1 - Rational Numbers", "What is 2/3 of 27?", "B", "9", "18", "6", "12", "2/3 x 27 = 54/3 = 18", "easy"),
            ("Chapter 1 - Rational Numbers", "Which is the smallest rational number?", "A", "-1/2", "0", "1/2", "-1/3", "On the number line, -1/2 is to the left of -1/3, so it is smaller.", "medium"),
            # Mathematics - Linear Equations
            ("Chapter 2 - Linear Equations", "Solve: 2x + 5 = 15", "A", "5", "10", "7.5", "20", "2x = 15 - 5 = 10, so x = 5.", "easy"),
            ("Chapter 2 - Linear Equations", "If 3x - 7 = 14, then x = ?", "A", "7", "21", "3", "9", "3x = 14 + 7 = 21, so x = 7.", "easy"),
            ("Chapter 2 - Linear Equations", "The solution of x/2 + 3 = 5 is:", "A", "4", "2", "8", "16", "x/2 = 5 - 3 = 2, so x = 4.", "easy"),
            ("Chapter 2 - Linear Equations", "If 2(x + 3) = 16, then x = ?", "B", "4", "5", "8", "11", "x + 3 = 8, so x = 5.", "medium"),
            # Mathematics - Quadrilaterals
            ("Chapter 3 - Understanding Quadrilaterals", "The sum of all interior angles of a quadrilateral is:", "B", "180", "360", "270", "540", "Sum of interior angles of a quadrilateral = (4-2) x 180 = 360 degrees.", "easy"),
            ("Chapter 3 - Understanding Quadrilaterals", "Which of the following is NOT a parallelogram?", "A", "Trapezium", "Rectangle", "Rhombus", "Square", "A trapezium has only one pair of parallel sides, so it is not a parallelogram.", "easy"),
            ("Chapter 3 - Understanding Quadrilaterals", "In a rectangle, diagonals are:", "B", "Unequal", "Equal", "Perpendicular", "Bisect at 90 degrees", "In a rectangle, both diagonals are equal in length.", "easy"),
            ("Chapter 3 - Understanding Quadrilaterals", "A rhombus has:", "C", "All angles equal", "Diagonals equal", "All sides equal", "Opposite sides parallel only", "A rhombus is a parallelogram with all four sides equal in length.", "medium"),
            # Science - Crop Production
            ("Chapter 1 - Crop Production", "Which tool is used for tilling the soil?", "B", "Sickle", "Plough", "Hoe", "Seed drill", "A plough is used for tilling and loosening the soil.", "easy"),
            ("Chapter 1 - Crop Production", "Which of these is a Kharif crop?", "B", "Wheat", "Rice", "Mustard", "Pea", "Rice is a Kharif crop grown during the monsoon season.", "medium"),
            ("Chapter 1 - Crop Production", "The process of removing unwanted plants is called:", "C", "Harvesting", "Sowing", "Weeding", "Irrigation", "Weeding is the process of removing unwanted plants that compete with crops for nutrients.", "easy"),
            ("Chapter 1 - Crop Production", "Which nutrient is provided by nitrogen fertilizers?", "A", "Nitrogen", "Phosphorus", "Potassium", "Calcium", "Nitrogen fertilizers provide nitrogen which is essential for plant growth and leaf development.", "easy"),
            # Science - Microorganisms
            ("Chapter 2 - Microorganisms", "Which microorganism is used to make curd?", "B", "Yeast", "Lactobacillus", "Rhizobium", "Penicillium", "Lactobacillus bacteria convert milk sugar into lactic acid, turning milk into curd.", "easy"),
            ("Chapter 2 - Microorganisms", "Antibiotics are produced from:", "B", "Bacteria", "Fungi", "Algae", "Virus", "Antibiotics like penicillin are produced from fungi (Penicillium).", "medium"),
            ("Chapter 2 - Microorganisms", "Which disease is caused by protozoa?", "A", "Malaria", "Tuberculosis", "Cholera", "Ringworm", "Malaria is caused by Plasmodium, a protozoan transmitted by female Anopheles mosquito.", "medium"),
            ("Chapter 2 - Microorganisms", "Yeast is used in the production of:", "B", "Curd", "Bread", "Vinegar", "Cheese", "Yeast produces carbon dioxide during fermentation, which makes bread fluffy.", "easy"),
            # Science - Synthetic Fibres
            ("Chapter 3 - Synthetic Fibres", "Which is a synthetic fibre?", "B", "Cotton", "Nylon", "Wool", "Silk", "Nylon is a synthetic fibre made from chemicals. Cotton, wool and silk are natural fibres.", "easy"),
            ("Chapter 3 - Synthetic Fibres", "Which plastic is used for making electrical switches?", "A", "Bakelite", "Polythene", "PVC", "Polystyrene", "Bakelite is a thermosetting plastic that is a poor conductor of electricity, making it ideal for electrical switches.", "medium"),
            ("Chapter 3 - Synthetic Fibres", "Plastics are:", "C", "Biodegradable", "Natural", "Non-biodegradable", "Edible", "Plastics do not decompose naturally, so they are non-biodegradable and cause pollution.", "easy"),
            # English - The Best Christmas Present
            ("Chapter 1 - The Best Christmas Present", "When is the story set?", "B", "World War II", "World War I", "Cold War", "French Revolution", "The story is set during World War I on Christmas morning.", "easy"),
            ("Chapter 1 - The Best Christmas Present", "What did the soldiers do in No Mans Land?", "B", "Fought", "Celebrated Christmas together", "Built trenches", "Exchanged weapons", "The soldiers from both sides came out and celebrated Christmas together.", "easy"),
            ("Chapter 1 - The Best Christmas Present", "What is the best Christmas present in the story?", "C", "Gifts", "Food", "Peace and friendship", "Football", "The soldiers experienced peace and friendship, which was the greatest gift.", "easy"),
            # English - The Tsunami
            ("Chapter 2 - The Tsunami", "Who saved many lives by recognizing tsunami signs?", "B", "Sanjeev", "Tilly Smith", "Meghna", "Almas", "Tilly Smith, a 10-year-old girl, recognized the signs from a geography lesson and warned people.", "easy"),
            ("Chapter 2 - The Tsunami", "What was the first sign of the approaching tsunami?", "A", "Water receded from shore", "Loud thunder", "Dark clouds", "Strong wind", "The water receded from the shore, exposing the sea floor, which is a warning sign of a tsunami.", "easy"),
            ("Chapter 2 - The Tsunami", "When did the Indian Ocean tsunami occur?", "C", "2002", "2003", "2004", "2005", "The Indian Ocean tsunami occurred on December 26, 2004.", "easy"),
            # History - How, When and Where
            ("Chapter 1 - How, When and Where", "Who divided Indian history into Ancient, Medieval and Modern?", "B", "Indian historians", "British historians", "French historians", "German historians", "British historians divided Indian history into three periods.", "easy"),
            ("Chapter 1 - How, When and Where", "Where is the National Archives of India located?", "A", "New Delhi", "Mumbai", "Kolkata", "Chennai", "The National Archives of India is located in New Delhi.", "easy"),
            ("Chapter 1 - How, When and Where", "What are primary sources of history?", "B", "Textbooks", "Official documents and letters", "Movies", "Novels", "Primary sources include official documents, letters, diaries, and artifacts from the time period.", "medium"),
            # History - From Trade to Territory
            ("Chapter 2 - From Trade to Territory", "In which year was the Battle of Plassey fought?", "B", "1756", "1757", "1764", "1857", "The Battle of Plassey was fought in 1757 between Siraj-ud-Daulah and Robert Clive.", "easy"),
            ("Chapter 2 - From Trade to Territory", "Who introduced the Subsidiary Alliance?", "C", "Robert Clive", "Warren Hastings", "Lord Wellesley", "Dalhousie", "Lord Wellesley introduced the Subsidiary Alliance system to bring Indian states under British control.", "medium"),
            ("Chapter 2 - From Trade to Territory", "The Diwani rights were given to the East India Company after:", "B", "Battle of Plassey", "Battle of Buxar", "Revolt of 1857", "Treaty of Allahabad", "After the Battle of Buxar in 1764, the Company got the Diwani rights of Bengal, Bihar and Orissa.", "medium"),
            # Geography - Resources
            ("Chapter 1 - Resources", "Which of these is a renewable resource?", "C", "Coal", "Petroleum", "Solar energy", "Natural gas", "Solar energy is renewable as it is continuously available from the sun.", "easy"),
            ("Chapter 1 - Resources", "What does sustainable development mean?", "B", "Using all resources quickly", "Using resources wisely for future generations", "Only using natural resources", "Stopping all development", "Sustainable development means using resources wisely so future generations can also use them.", "medium"),
            ("Chapter 1 - Resources", "Which of the following is a human-made resource?", "B", "Water", "Roads", "Forests", "Minerals", "Roads are built by humans using natural materials, so they are human-made resources.", "easy"),
            # Geography - Land, Soil, Water
            ("Chapter 2 - Land, Soil, Water", "Which soil is called black cotton soil?", "B", "Alluvial soil", "Black soil", "Red soil", "Laterite soil", "Black soil is also called black cotton soil because it is good for growing cotton.", "easy"),
            ("Chapter 2 - Land, Soil, Water", "Which method is used to prevent soil erosion on slopes?", "A", "Terrace farming", "Crop rotation", "Irrigation", "Fertilizers", "Terrace farming creates flat steps on slopes, which prevents soil from being washed away by rain.", "easy"),
            ("Chapter 2 - Land, Soil, Water", "Alluvial soil is found in:", "A", "River plains", "Mountain tops", "Deserts", "Plateaus", "Alluvial soil is deposited by rivers in their plains and is very fertile.", "easy"),
            # Computer Science - Algorithms
            ("Chapter 1 - Algorithms", "Which of these is NOT a characteristic of an algorithm?", "B", "Finiteness", "Ambiguity", "Definiteness", "Effectiveness", "Each step of an algorithm must be clear and unambiguous, not ambiguous.", "easy"),
            ("Chapter 1 - Algorithms", "What is the first step of an algorithm?", "C", "Process", "Output", "Start", "Stop", "Every algorithm begins with a Start step.", "easy"),
            ("Chapter 1 - Algorithms", "A flowchart uses which shape for decision making?", "B", "Rectangle", "Diamond", "Circle", "Oval", "A diamond shape is used in flowcharts to represent decision-making steps.", "easy"),
            ("Chapter 1 - Algorithms", "Which type of algorithm uses repetition?", "C", "Sequential", "Conditional", "Looping", "Recursive", "Looping algorithms use repetition (for loops, while loops) to repeat steps.", "medium"),
            # Computer Science - Python
            ("Chapter 2 - Programming in Python", "Which symbol is used for single-line comments in Python?", "C", "//", "/*", "#", "--", "In Python, the # symbol is used for single-line comments.", "easy"),
            ("Chapter 2 - Programming in Python", "What is the output of print(2 + 3 * 4)?", "C", "20", "24", "14", "10", "According to BODMAS, multiplication happens first: 3*4=12, then 2+12=14.", "medium"),
            ("Chapter 2 - Programming in Python", "Which data type is used for decimal numbers in Python?", "B", "int", "float", "str", "bool", "The float data type is used for decimal numbers like 3.14, -0.5, etc.", "easy"),
            ("Chapter 2 - Programming in Python", "What does the len() function do?", "A", "Returns the length", "Returns the type", "Returns the value", "Returns the index", "The len() function returns the number of items in an object like a string or list.", "easy"),
        ]
        question_objects = {}
        for ch_title, q_text, correct, opt_a, opt_b, opt_c, opt_d, explanation, difficulty in questions_data:
            ch = chapter_objects[ch_title]
            obj, _ = Question.objects.get_or_create(
                chapter=ch, question_text=q_text,
                defaults={
                    "option_a": opt_a, "option_b": opt_b, "option_c": opt_c, "option_d": opt_d,
                    "correct_answer": correct, "explanation": explanation, "difficulty": difficulty
                }
            )
            question_objects[q_text] = obj
            self.stdout.write(f"  Question: {q_text[:40]}...")

        # 6. Create Quizzes
        quizzes_data = [
            ("Math Quiz - Rational Numbers", "Chapter 1 - Rational Numbers", "Test your knowledge of rational numbers", 10, 5),
            ("Math Quiz - Linear Equations", "Chapter 2 - Linear Equations", "Test your knowledge of linear equations", 10, 4),
            ("Math Quiz - Quadrilaterals", "Chapter 3 - Understanding Quadrilaterals", "Test your knowledge of quadrilaterals", 10, 4),
            ("Science Quiz - Crop Production", "Chapter 1 - Crop Production", "Test your knowledge of crop production", 10, 4),
            ("Science Quiz - Microorganisms", "Chapter 2 - Microorganisms", "Test your knowledge of microorganisms", 10, 4),
            ("Science Quiz - Synthetic Fibres", "Chapter 3 - Synthetic Fibres", "Test your knowledge of synthetic fibres and plastics", 10, 3),
            ("English Quiz - The Best Christmas Present", "Chapter 1 - The Best Christmas Present", "Test your understanding of the story", 5, 3),
            ("English Quiz - The Tsunami", "Chapter 2 - The Tsunami", "Test your understanding of the tsunami story", 5, 3),
            ("History Quiz - Recording History", "Chapter 1 - How, When and Where", "Test your knowledge of historical sources", 5, 3),
            ("History Quiz - East India Company", "Chapter 2 - From Trade to Territory", "Test your knowledge of British rule in India", 5, 3),
            ("Geography Quiz - Resources", "Chapter 1 - Resources", "Test your knowledge of natural resources", 5, 3),
            ("Geography Quiz - Land and Soil", "Chapter 2 - Land, Soil, Water", "Test your knowledge of land and soil resources", 5, 3),
            ("Computer Science Quiz - Algorithms", "Chapter 1 - Algorithms", "Test your understanding of algorithms", 5, 4),
            ("Computer Science Quiz - Python Basics", "Chapter 2 - Programming in Python", "Test your knowledge of Python programming", 5, 3),
        ]
        for title, ch_title, desc, time_limit, total_marks in quizzes_data:
            ch = chapter_objects[ch_title]
            quiz, _ = Quiz.objects.get_or_create(
                title=title, chapter=ch,
                defaults={"description": desc, "time_limit": time_limit, "total_marks": total_marks}
            )
            questions = Question.objects.filter(chapter=ch)[:total_marks]
            for idx, q in enumerate(questions):
                QuizQuestion.objects.get_or_create(quiz=quiz, question=q, defaults={"order": idx + 1, "marks": 1})
            self.stdout.write(f"  Quiz: {title}")

        self.stdout.write(self.style.SUCCESS("\n✅ All sample data seeded successfully!"))
        self.stdout.write(self.style.WARNING("You can now register as a student and start learning!"))

