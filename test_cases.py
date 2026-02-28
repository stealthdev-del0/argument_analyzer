"""
Test Cases für Argument Structure Analyzer

Beispiele zum Testen verschiedener Argument-Typen
"""

# Test Dataset mit verschiedenen argumentativen Strukturen


TEST_CASES = {
    "climate_change": """
    Climate change is one of the most pressing issues of our time. 
    We must take immediate action because scientific evidence overwhelmingly shows that global warming is real.
    Research from major institutions demonstrates rising temperatures and changing weather patterns.
    
    However, some people argue that climate change is a natural cycle.
    But this ignores the unprecedented rate of warming in recent decades.
    Therefore, we need stronger climate policies and international cooperation.
    """,
    
    "ai_ethics": """
    Artificial Intelligence poses both tremendous benefits and serious risks.
    We should invest in AI safety research because the technology is advancing rapidly.
    AI systems are increasingly making critical decisions in healthcare, criminal justice, and finance.
    
    Critics worry about job displacement and algorithmic bias.
    Yet AI has also created millions of new jobs and improved productivity.
    Therefore, we need comprehensive regulation that balances innovation with safety.
    """,
    
    "education": """
    Online education is the future of learning.
    Students should embrace digital learning because it offers flexibility and accessibility.
    Studies show that online learning can be as effective as traditional education.
    Virtual classrooms enable access for students in remote areas.
    
    However, some educators argue that in-person learning is superior.
    They claim that face-to-face interaction is essential for student development.
    On the other hand, quality online programs do foster meaningful interactions.
    Therefore, the best approach combines both online and traditional elements.
    """,
    
    "gun_control": """
    Gun violence is a serious public health crisis in America.
    We must implement stricter gun control laws because they reduce violence in countries that have them.
    Data from Australia and Japan shows that regulations work.
    
    However, Second Amendment advocates argue that guns are necessary for self-defense.
    But statistics show that countries with stricter laws have lower gun death rates.
    Moreover, most gun owners support background checks.
    Therefore, common-sense gun regulations are both constitutional and necessary.
    """,
    
    "social_media": """
    Social media has fundamentally changed how we communicate.
    We should be concerned about social media because it's addictive and harmful to mental health.
    Studies show that heavy social media use correlates with depression and anxiety.
    Young people are particularly vulnerable to these effects.
    
    Some argue that social media enables important social movements.
    Though it has enabled activism, the negative mental health effects are undeniable.
    Furthermore, algorithms are designed to maximize engagement, not user wellbeing.
    Therefore, we need stronger regulation of social media platforms.
    """
}


def get_test_case(name: str) -> str:
    """Get a test case by name"""
    if name in TEST_CASES:
        return TEST_CASES[name]
    else:
        available = list(TEST_CASES.keys())
        raise ValueError(f"Unknown test case: {name}. Available: {available}")


def list_test_cases():
    """List all available test cases"""
    return list(TEST_CASES.keys())


if __name__ == "__main__":
    print("Available test cases:")
    for case_name in list_test_cases():
        print(f"  - {case_name}")
    
    print("\nUsage:")
    print("  python test_cases.py --list")
    print("  python test_cases.py climate_change")
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != "--list":
        case_name = sys.argv[1]
        try:
            text = get_test_case(case_name)
            print(f"\n{case_name.upper()}:")
            print(text)
        except ValueError as e:
            print(f"Error: {e}")
